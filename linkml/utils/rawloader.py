import copy
import os
import time
from datetime import datetime
from io import StringIO
from typing import Union, TextIO, Optional
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import yaml
from jsonasobj2 import as_dict

from linkml_model.meta import SchemaDefinition, metamodel_version
from linkml.utils.mergeutils import merge_schemas, set_from_schema
from linkml_runtime.utils.namespaces import Namespaces
from linkml_runtime.utils.yamlutils import DupCheckYamlLoader, YAMLMark, TypedNode

yaml.error.Mark = YAMLMark


def load_raw_schema(data: Union[str, dict, TextIO],
                    source_file: Optional[str] = None,
                    source_file_date: Optional[str] = None,
                    source_file_size: Optional[int] = None,
                    base_dir: Optional[str] = None,
                    merge_modules: Optional[bool] = True,
                    emit_metadata: Optional[bool] = True) -> SchemaDefinition:
    """ Load and flatten SchemaDefinition from a file name, a URL or a block of text

    @param data: URL, file name or block of text YAML Object or open file handle
    @param source_file: Source file name for the schema if data is type TextIO
    @param source_file_date: timestamp of source file if data is type TextIO
    @param source_file_size: size of source file if data is type TextIO
    @param base_dir: Working directory or base URL of sources
    @param merge_modules: True means combine modules into one source, false means keep separate
    @param emit_metadata: True means add source file info to the output
    @return: Un-processed Schema Definition object
    """
    def _name_from_url(url) -> str:
        return urlparse(url).path.rsplit('/', 1)[-1].rsplit('.', 1)[0]

    if isinstance(data, str):
        # If passing the actual YAML
        if '\n' in data:
            return load_raw_schema(StringIO(data), source_file=source_file, base_dir=base_dir,
                                   source_file_date=source_file_date, source_file_size=source_file_size,
                                   emit_metadata=emit_metadata)

        # Passing a URL or file name
        assert source_file is None, "source_file parameter not allowed if data is a file or URL"
        assert source_file_date is None, "source_file_date parameter not allowed if data is a file or URL"
        assert source_file_size is None, "source_file_size parameter not allowed if data is a file or URL"

        if '://' in data or (base_dir and '://' in base_dir):
            # URL
            fname = Namespaces.join(base_dir, data) if '://' not in data else data
            req = Request(fname)
            req.add_header("Accept", "text/yaml, application/yaml;q=0.9")
            try:
                response = urlopen(req)
            except HTTPError as e:
                # This is here because the message out of urllib doesn't include the file name
                e.msg = f"{e.filename}"
                raise e
            with response:
                return load_raw_schema(response, fname, response.info()['Last-Modified'],
                                       response.info()['Content-Length'], emit_metadata=emit_metadata)

        else:
            # File name
            if not base_dir:
                fname = os.path.abspath(data)
                base_dir = os.path.dirname(fname)
            else:
                fname = data if os.path.isabs(data) else os.path.abspath(os.path.join(base_dir, data))
            with open(fname) as f:
                return load_raw_schema(f, fname, time.ctime(os.path.getmtime(fname)), os.path.getsize(fname), base_dir,
                                       emit_metadata=emit_metadata)
    else:
        # Loaded YAML or file handle that references YAML
        schemadefs = copy.deepcopy(data) if isinstance(data, dict) else yaml.load(data, DupCheckYamlLoader)
        if schemadefs is None:
            raise ValueError("Empty schema - cannot process")
        elif not isinstance(schemadefs, dict):
            raise ValueError("Unrecognized schema content - cannot process")

        # Convert the schema into a "name: definition" form
        if not all(isinstance(e, dict) for e in schemadefs.values()):
            if 'name' in schemadefs:
                schemaname = schemadefs.pop('name')
            elif 'id' in schemadefs:
                schemaname = _name_from_url(schemadefs['id'])
            else:
                raise ValueError("Unable to determine schema name")
            schema_body = [schemadefs]
            schemadefs = {schemaname: schemadefs}
        else:
            schema_body = list(schemadefs.values())

        def check_is_dict(element: str) -> None:
            """ Verify that element is an instance of a dictionary, mapping empty elements to dictionaries """
            for body_schemaname, body_body in schemadefs.items():
                if element in body_body:
                    if body_body[element] is None:
                        body_body[element] = dict()
                    elif not isinstance(body_body[element], dict):
                        raise ValueError(f'Schema: {body_schemaname} - Element: {element} must be a dictionary')

        def fix_multiples(container:  str, element: str) -> None:
            """
            A common error is representing a list object as a singleton.  This fixes this problem
            :param container: name of container to fix (e.g. a specific clas instance)
            :param element:  name or list element to adjust (e.g. notes"
            """
            # Note: multiple bodies in the schema are an at-risk feature.  Doesn't seem to have a real use case.
            for body_body in schema_body:
                if container in body_body:
                    for c in body_body[container].values():
                        if c and element in c and isinstance(c[element], str):
                            c[element] = [c[element]]

        for e in ['slots', 'classes', 'types', 'subsets']:
            """ Validate the basic categories, fixing multiples where appropriate """
            check_is_dict(e)
            fix_multiples(e, 'in_subset')
            fix_multiples(e, 'apply_to')

        for e in ['imports']:
            for body in schema_body:
                if e in body:
                    if isinstance(body[e], str):
                        body[e] = [body[e]]

        # Add the implicit domain to the slot usages
        for body in schema_body:
            for cname, cls in body.get('classes', {}).items():
                if cls is None:
                    cls = {}
                    body['classes'][cname] = cls
                elif not isinstance(cls, dict):
                    raise ValueError(f"{TypedNode.yaml_loc(cname)}: class definition is not a structure")
                for uname, usage in cls.get('slot usage', {}).items():
                    if usage is None:
                        usage = {}
                        cls['slot usage'][uname] = usage
                    if 'domain' not in usage:
                        usage['domain'] = cname

        schema: Optional[SchemaDefinition] = None
        for sname, sdef in {k: SchemaDefinition(name=k, **as_dict(v)) for k, v in schemadefs.items()}.items():
            if schema is None:
                schema = sdef
                if source_file:
                    schema.source_file = source_file
                if emit_metadata:
                    schema.source_file_date = source_file_date
                    schema.source_file_size = source_file_size
                    schema.generation_date = datetime.now().strftime("%Y-%m-%d %H:%M")
                schema.metamodel_version = metamodel_version
                set_from_schema(schema)
            else:
                merge_schemas(schema, sdef, merge_imports=merge_modules)
        return schema
