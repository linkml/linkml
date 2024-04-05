import os
from typing import Any, Iterator, Optional

import rdflib
from linkml_runtime.dumpers import rdflib_dumper

from linkml.generators import PythonGenerator, ShaclGenerator
from linkml.validator.plugins.validation_plugin import ValidationPlugin
from linkml.validator.report import Severity, ValidationResult
from linkml.validator.validation_context import ValidationContext

SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")


class ShaclValidationPlugin(ValidationPlugin):
    """A validation plugin which validates instances using SHACL.

    :param shacl_path: If provided, SHACL will not be generated from the schema,
        instead it will be read from this path.
    :param closed: If ``True``, additional properties are not allowed on instances.
        Defaults to ``False``.
    :param raise_on_conversion_error: If ``True``, raise an exception if the instance
        cannot be converted to a Python class. Otherwise, treat as a ValidationError.
        Defaults to ``False``.
    """

    def __init__(
        self,
        *,
        closed: bool = False,
        shacl_path: Optional[os.PathLike] = None,
        raise_on_conversion_error: bool = False,
    ) -> None:
        self.closed = closed
        self.shacl_path = shacl_path
        self.raise_on_conversion_error = raise_on_conversion_error
        self._loaded_graphs = {}

    def _shacl_graph(self, context: ValidationContext) -> Optional[rdflib.Graph]:
        g = rdflib.Graph()
        if self.shacl_path:
            g.parse(str(self.shacl_path))
        else:
            schema_hash = hash(str(context._schema))
            if schema_hash in self._loaded_graphs:
                g = self._loaded_graphs[schema_hash]
            else:
                gen = ShaclGenerator(context._schema)
                g = gen.as_graph()
                self._loaded_graphs[schema_hash] = g
        return g

    def process(self, instance: Any, context: ValidationContext) -> Iterator[ValidationResult]:
        """Perform SHACL Schema validation on the provided instance

        :param instance: The instance to validate
        :param context: The validation context which provides a SHACL artifact
        :return: Iterator over validation results
        :rtype: Iterator[ValidationResult]
        """
        import pyshacl

        shacl_graph = self._shacl_graph(context)
        if isinstance(instance, dict):
            pygen = PythonGenerator(context._schema)
            mod = pygen.compile_module()
            py_cls = getattr(mod, context._target_class)
            if self.raise_on_conversion_error:
                instance = py_cls(**instance)
            else:
                try:
                    instance = py_cls(**instance)
                except (ValueError, TypeError):
                    yield ValidationResult(
                        type="shacl validation",
                        severity=Severity.ERROR,
                        instance=instance,
                        instantiates=context.target_class,
                        message="failed at class instantiation stage",
                    )
                    return
        data_graph = rdflib_dumper.as_rdf_graph(instance, schemaview=context.schema_view)
        validator = pyshacl.Validator(
            shacl_graph=shacl_graph,
            data_graph=data_graph,
            inference="rdfs",
        )
        conforms, report_graph, report_text = validator.run()
        for s, _, o in report_graph.triples((None, SH.result, None)):
            msg = ""
            for p, o2 in report_graph.predicate_objects(o):
                msg += f"{p} {o2}\n"
            yield ValidationResult(
                type="shacl validation",
                severity=Severity.ERROR,
                instance=instance,
                instantiates=context.target_class,
                message=f"{msg}",
            )
