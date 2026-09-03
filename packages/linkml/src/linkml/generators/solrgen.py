"""
Generate Solr schema definitions from a LinkML schema.

The output is a JSON document representing Solr operations such as add-field.
Note that this makes a flattened 'union' schema for all classes, as Solr does not 
have the concept of classes/records.
"""

import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

import click
from linkml_runtime.linkml_model.meta import ClassDefinitionName, SlotDefinition
from linkml_runtime.utils.schemaview import SchemaView
from pydantic import BaseModel

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments


# Solr Schema Model Classes (inline Pydantic models)
class Field(BaseModel):
    """Represents a Solr field definition."""
    name: str
    type: str
    stored: Optional[bool] = None
    indexed: Optional[bool] = None
    multiValued: Optional[bool] = None


class DynamicField(BaseModel):
    """Represents a Solr dynamic field definition."""
    name: str
    type: str
    stored: Optional[bool] = None


class CopyField(BaseModel):
    """Represents a Solr copy field definition."""
    source: str
    dest: Union[str, List[str]]
    maxChars: Optional[int] = None


class FieldType(BaseModel):
    """Represents a Solr field type definition."""
    name: str
    class_: Optional[str] = None
    positionIncrementGap: Optional[str] = None


class Transaction(BaseModel):
    """Represents a Solr schema transaction with multiple operations."""
    add_field: List[Field] = []
    delete_field: List[str] = []
    replace_field: List[str] = []
    add_field_type: List[FieldType] = []
    delete_field_type: List[str] = []
    replace_field_type: List[str] = []
    add_dynamic_field: List[DynamicField] = []
    delete_dynamic_field: List[str] = []
    replace_dynamic_field: List[str] = []


# Map from underlying python data type to solr equivalent
# Note: The underlying types are a union of any built-in python datatype + any type defined in
#       linkml-runtime/utils/metamodelcore.py
# Note the keys are all lower case
solr_schema_types: Dict[str, str] = {
    "int": "int",
    "integer": "int",
    "str": "string",
    "string": "string",
    "bool": "boolean",
    "boolean": "boolean",
    "float": "pfloat",
    "double": "pdouble",
    "decimal": "pdouble",
    "xsddate": "date",
    "xsddatetime": "date",
    "xsdtime": "time"
}


@dataclass
class SolrSchemaGenerator(Generator):
    """
    Generates a Solr schema from a LinkML schema.

    The output is a JSON document representing Solr operations such as add-field.
    Note that this makes a flattened 'union' schema for all classes, as Solr does not
    have the concept of classes/records.
    """
    
    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = __version__
    valid_formats = ["json"]
    uses_schemaloader = False
    visit_all_class_slots = True
    
    # Instance variables
    schemaview: SchemaView = None
    transaction: Transaction = None

    def __post_init__(self) -> None:
        super().__post_init__()
        self.schemaview = SchemaView(self.schema)
        self.transaction = Transaction()

    def _transaction_json(self, transaction: Transaction) -> str:
        """Convert transaction to JSON format expected by Solr."""
        # Convert to dict and transform underscore keys to hyphen keys for Solr
        obj = transaction.model_dump(exclude_unset=True, exclude_none=True)
        obj = {k.replace('_', '-'): v for k, v in obj.items()}
        return json.dumps(obj, indent=2)

    def class_schema(self, class_name: Union[str, ClassDefinitionName]) -> str:
        """Generate schema for a single class."""
        transaction = self.get_transaction(class_name)
        return self._transaction_json(transaction)

    def serialize(self, **kwargs) -> str:
        """Generate schema for all classes."""
        transaction = self.get_transaction()
        return self._transaction_json(transaction)

    def get_transaction(self, class_name: Union[str, ClassDefinitionName] = None) -> Transaction:
        """Build transaction with fields from specified class or all classes."""
        transaction = Transaction()
        sv = self.schemaview
        field_dict = {}
        
        for cn in sv.all_classes():
            if class_name is None or str(cn) == str(class_name):
                for slot in sv.class_induced_slots(cn):
                    field = self.get_field(slot)
                    if field:
                        field_dict[field.name] = field
        
        transaction.add_field = list(field_dict.values())
        return transaction

    def get_field(self, slot: SlotDefinition) -> Optional[Field]:
        """Convert a LinkML slot to a Solr field definition."""
        sv = self.schemaview
        range_name = slot.range
        
        # Handle different range types
        if range_name in sv.all_classes():
            # Class reference - treat as string (foreign key)
            solr_type = "string"
        elif range_name in sv.all_enums():
            # Enum - treat as string
            solr_type = "string"
        elif range_name is None:
            # Use default range
            default_range = sv.schema.default_range or "string"
            solr_type = solr_schema_types.get(str(default_range).lower(), "string")
        elif range_name in sv.all_types():
            # LinkML type
            type_def = sv.get_type(range_name)
            base_type = type_def.typeof or type_def.base
            if type_def.repr == 'str':
                solr_type = "string"
            else:
                solr_type = solr_schema_types.get(str(base_type).lower(), "string")
        else:
            # Direct type mapping
            solr_type = solr_schema_types.get(str(range_name).lower(), "string")
        
        if solr_type not in solr_schema_types.values():
            # Unknown type, default to string
            solr_type = "string"
        
        return Field(
            name=slot.name,
            type=solr_type,
            multiValued=slot.multivalued
        )


@shared_arguments(SolrSchemaGenerator)
@click.option('--top-class', '-t',
              default=None,
              show_default=True,
              help='Generate schema for this specific class only')
@click.command()
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, top_class=None, **kwargs):
    """Generate Solr schema representation of a LinkML model."""
    generator = SolrSchemaGenerator(yamlfile, **kwargs)
    if top_class:
        output = generator.class_schema(top_class)
    else:
        output = generator.serialize(**kwargs)
    print(output)


if __name__ == '__main__':
    cli()