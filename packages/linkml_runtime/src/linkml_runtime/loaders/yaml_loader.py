from __future__ import annotations

import os
from io import StringIO
from typing import TYPE_CHECKING, TextIO

import yaml
from hbreader import FileInfo

from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.utils.yamlutils import DupCheckYamlLoader, YAMLRoot

if TYPE_CHECKING:
    from pathlib import Path

    from pydantic import BaseModel


class YAMLLoader(Loader):
    """
    A Loader that is capable of instantiating LinkML data objects from a YAML file
    """

    def load_as_dict(
        self, source: str | dict | TextIO | Path, *, base_dir: str | None = None, metadata: FileInfo | None = None
    ) -> dict | list[dict]:
        if metadata is None:
            metadata = FileInfo()
        if base_dir and not metadata.base_path:
            metadata.base_path = base_dir
        data = self._read_source(
            source, base_dir=base_dir, metadata=metadata, accept_header="text/yaml, application/yaml;q=0.9"
        )
        if isinstance(data, str):
            data = StringIO(data)
            if metadata and metadata.source_file:
                data.name = os.path.relpath(metadata.source_file, metadata.base_path)
            return yaml.load(data, DupCheckYamlLoader)
        return data

    def load_any(
        self,
        source: str | dict | TextIO | Path,
        target_class: type[YAMLRoot | BaseModel],
        *,
        base_dir: str | None = None,
        metadata: FileInfo | None = None,
        **_,
    ) -> YAMLRoot | list[YAMLRoot]:
        if metadata is None:
            metadata = FileInfo()
        data_as_dict = self.load_as_dict(source, base_dir=base_dir, metadata=metadata)
        result = self._construct_target_class(data_as_dict, target_class)
        # When the source was a file (or URL), ``hbread`` resolves and records it on the metadata.
        # Propagate that to ``source_file`` (e.g. on a SchemaDefinition) so relative imports can be
        # resolved against it. Inline string sources without caller-supplied metadata leave
        # ``source_file`` unset, so this naturally distinguishes a path from schema text.
        # Gated on SchemaDefinition specifically because it owns ``source_file`` in the metamodel;
        # this avoids injecting the loader path into other target classes that happen to have a
        # ``source_file`` slot.
        if metadata.source_file:
            # Lazy import is cheap, avoids circular dependency between loaders and metamodel.
            from linkml_runtime.linkml_model.meta import SchemaDefinition

            # Prefer the path exactly as the caller supplied it.  hbread always absolutizes, so
            # using metadata.source_file would stamp a machine-absolute path onto a schema that
            # was loaded via a relative path.  ``source`` is only the caller's *path* when its
            # absolutized form is what hbread resolved - inline text with a caller-supplied
            # ``source_file`` name is also a str, so an isinstance check alone would record the
            # whole document as the path.  Everything else (URLs, file-like objects, inline text,
            # base_dir joins) records the resolved location from the metadata.
            if (
                base_dir is None
                and isinstance(source, str | os.PathLike)
                and os.path.abspath(str(source)) == str(metadata.source_file)
            ):
                path_to_record = str(source)
            else:
                path_to_record = str(metadata.source_file)

            for target in result if isinstance(result, list) else [result]:
                # Always overwrite: the metamodel marks source_file as
                # ``readonly: supplied by the schema loader``.  A value
                # serialised into the YAML by a previous --metadata run is
                # stale content, not an authoritative path.
                if isinstance(target, SchemaDefinition):
                    target.source_file = path_to_record
        return result

    def loads_any(
        self, source: str, target_class: type[BaseModel | YAMLRoot], *, metadata: FileInfo | None = None, **_
    ) -> BaseModel | YAMLRoot | list[BaseModel] | list[YAMLRoot]:
        """
        Load source as a string
        @param source: source
        @param target_class: destination class
        @param metadata: metadata about the source
        @param _: extensions
        @return: instance of taarget_class
        """
        return self.load_any(source, target_class, metadata=metadata)
