import os
from typing import Union, TextIO

import click

from linkml_runtime.linkml_model.meta import ClassDefinition, SlotDefinition, SchemaDefinition
from linkml_runtime.utils.formatutils import camelcase, lcamelcase
from linkml.utils.generator import Generator, shared_arguments


class ProtoGenerator(Generator):
    """
    A `Generator` for creating Protobuf schemas from a linkml schema.

    """
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ['proto']
    visit_all_class_slots = True

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition], **kwargs) -> None:
        super().__init__(schema, **kwargs)
        self.relative_slot_num = 0

    def visit_class(self, cls: ClassDefinition) -> bool:
        if cls.mixin or cls.abstract or not cls.slots:
            return False
        if cls.description:
            for dline in cls.description.split('\n'):
                print(f'// {dline}')
        print(f'message {camelcase(cls.name)}')
        print(" {")
        self.relative_slot_num = 0
        return True

    def end_class(self, cls: ClassDefinition) -> None:
        print(" }")

    def visit_class_slot(self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition) -> None:
        qual = 'repeated ' if slot.multivalued else 'optional ' if not slot.required or slot.key else ''
        slotname = lcamelcase(aliased_slot_name)
        slot_range = camelcase(slot.range)
        self.relative_slot_num += 1
        print(f"  {qual}{slotname} {slot_range} = {self.relative_slot_num}")


@shared_arguments(ProtoGenerator)
@click.command()
def cli(yamlfile, **args):
    """ Generate proto representation of LinkML model """
    print(ProtoGenerator(yamlfile, **args).serialize(**args))


if __name__ == '__main__':
    cli()
