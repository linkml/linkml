from linkml.generators.markdowndatadictgen import MarkdownDataDictGen
from linkml.generators.markdowngen import MarkdownGenerator


def test_datadict_gen(kitchen_sink_path, tmp_path):
    gen = MarkdownGenerator(kitchen_sink_path)
    gen.serialize(directory=tmp_path)


def test_datadict_personinfo(input_path, snapshot):
    schema = str(input_path("personinfo.yaml"))
    gen = MarkdownDataDictGen(schema)
    generated = gen.serialize()
    assert generated == snapshot("personinfo.md")


def test_datadict_kitchensink(kitchen_sink_path, snapshot):
    gen = MarkdownDataDictGen(kitchen_sink_path)
    generated = gen.serialize()
    assert generated == snapshot("kitchen_sink.md")
