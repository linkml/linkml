import platform
from pathlib import Path

import pytest
from linkml_runtime.utils.compile_python import compile_python

from linkml import LOCAL_METAMODEL_LDCONTEXT_FILE, LOCAL_METAMODEL_YAML_FILE, METAMODEL_NAMESPACE
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.markdowngen import MarkdownGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.shexgen import ShExGenerator
from linkml.generators.sqlalchemygen import SQLAlchemyGenerator, TemplateEnum


@pytest.mark.slow
@pytest.mark.parametrize(
    "generator,extension,serialize_kwargs",
    [
        (MarkdownGenerator, "markdown", {}),
        pytest.param(
            OwlSchemaGenerator,
            ".owl",
            {},
            marks=[
                pytest.mark.skipif(
                    platform.system() == "Windows",
                    reason="prefix expansion issue. see: https://github.com/RDFLib/rdflib/issues/2606",
                ),
                pytest.mark.owlgen,
            ],
        ),
        pytest.param(RDFGenerator, ".ttl", {"context": LOCAL_METAMODEL_LDCONTEXT_FILE}, marks=pytest.mark.rdfgen),
        pytest.param(
            ContextGenerator, ".context.jsonld", {"base": METAMODEL_NAMESPACE}, marks=pytest.mark.jsonldcontextgen
        ),
        pytest.param(
            JSONLDGenerator,
            ".json",
            {"base": METAMODEL_NAMESPACE, "context_kwargs": {"model": True}},
            marks=pytest.mark.jsonldgen,
        ),
        pytest.param(PythonGenerator, ".py", {}, marks=pytest.mark.pythongen),
        pytest.param(
            SQLAlchemyGenerator, ".sqla.py", {"template": TemplateEnum.DECLARATIVE}, marks=pytest.mark.sqlalchemygen
        ),
    ],
)
def test_metamodel(generator, extension, serialize_kwargs, temp_dir, snapshot):
    if not extension.startswith("."):
        # is a directory!
        output_dir = Path(extension) / "meta"
        generator(LOCAL_METAMODEL_YAML_FILE, directory=str(temp_dir)).serialize(directory=str(temp_dir))
        assert temp_dir == snapshot(str(output_dir))
    else:
        generated = generator(LOCAL_METAMODEL_YAML_FILE).serialize(**serialize_kwargs)
        output_file = Path("meta").with_suffix(extension)
        if extension.endswith(".py"):
            compile_python(generated, "test")
        assert generated == snapshot(output_file)


@pytest.mark.slow
@pytest.mark.parametrize("format,extension", [("shex", ".shex"), ("json", ".shexj")])
def test_metamodel_shex(format, extension, snapshot):
    output_file = "meta" + extension
    generated = ShExGenerator(LOCAL_METAMODEL_YAML_FILE, format=format).serialize(format=format)
    assert generated == snapshot(output_file)
