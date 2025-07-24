import copy
from datetime import datetime
from pathlib import Path
from typing import Optional, TextIO, Union
from urllib.parse import urlparse

import yaml
from dateutil.parser import ParserError, parse
from hbreader import FileInfo, HBType, detect_type
from linkml_runtime.linkml_model.meta import SchemaDefinition, metamodel_version
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.yamlutils import YAMLMark, YAMLRoot

from linkml.utils.mergeutils import set_from_schema

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
yaml.error.Mark = YAMLMark


# Override the default linkml missing value tests
def mrf(self, field_name: str) -> None:
    if isinstance(self, SchemaDefinition) and field_name == "name" and self.id:
        id_parts = self.id.replace("#", "/").rsplit("/")
        self.name = id_parts[-1]
    else:
        YAMLRoot.MissingRequiredField(self, f"{type(self).__name__}.{field_name}")


SchemaDefinition.MissingRequiredField = mrf


def load_raw_schema(
    data: Union[str, dict, TextIO, Path],
    source_file: Optional[str] = None,
    source_file_date: Optional[str] = None,
    source_file_size: Optional[int] = None,
    base_dir: Optional[str] = None,
    merge_modules: Optional[bool] = True,
    emit_metadata: Optional[bool] = True,
) -> SchemaDefinition:
    """Load and flatten SchemaDefinition from a file name, a URL or a block of text

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
        return urlparse(url).path.rsplit("/", 1)[-1].rsplit(".", 1)[0]

    # Passing a URL or file name
    if detect_type(data, base_dir) not in (HBType.STRING, HBType.STRINGABLE):
        assert source_file is None, "source_file parameter not allowed if data is a file or URL"
        assert source_file_date is None, "source_file_date parameter not allowed if data is a file or URL"
        assert source_file_size is None, "source_file_size parameter not allowed if data is a file or URL"

    if isinstance(data, Path):
        data = str(data)

    # Convert the input into a valid SchemaDefinition
    if isinstance(data, (str, dict, TextIO)):
        # TODO: Build a generic loader that detects type from suffix or content and invokes the appropriate loader
        schema_metadata = FileInfo()
        schema_metadata.source_file = source_file
        schema_metadata.source_file_date = source_file_date
        schema_metadata.source_file_size = source_file_size
        schema_metadata.base_path = base_dir
        schema = yaml_loader.load(
            copy.deepcopy(data) if isinstance(data, dict) else data,
            SchemaDefinition,
            base_dir=base_dir,
            metadata=schema_metadata,
        )
    elif isinstance(data, SchemaDefinition):
        schema = copy.deepcopy(data)
    else:
        raise ValueError("Unrecognized input to raw loader")

    if schema is None:
        raise ValueError("Empty schema - cannot process")

    if schema.name is None:
        if schema.id is None:
            raise ValueError("Unable to determine schema name")
        else:
            schema.name = _name_from_url(schema.id)
    elif schema.id is None:
        # TODO: figure out how to generate this from the default_prefix and namespace map
        raise ValueError("Schema identifier must be supplied")

    if emit_metadata:
        schema.source_file = schema_metadata.source_file
        src_date = schema_metadata.source_file_date
        try:
            schema.source_file_date = parse(src_date).strftime(DATETIME_FORMAT) if src_date else None
        except ParserError:
            schema.source_file_date = src_date
        schema.source_file_size = schema_metadata.source_file_size
        schema.generation_date = datetime.now().strftime(DATETIME_FORMAT)
    schema.metamodel_version = metamodel_version

    set_from_schema(schema)

    return schema
