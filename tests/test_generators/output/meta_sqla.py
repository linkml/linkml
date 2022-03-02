
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()
metadata = Base.metadata


class CommonMetadata(Base):
    """
    Generic metadata shared across definitions
    """
    __tablename__ = 'common_metadata'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    
    
    # One-To-Many: OneToAnyMapping(source_class='common_metadata', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='common_metadata_id', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.common_metadata_id]")
    
    
    todos_rel = relationship( "CommonMetadataTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: CommonMetadataTodos(todos=x_))
    
    
    notes_rel = relationship( "CommonMetadataNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: CommonMetadataNotes(notes=x_))
    
    
    comments_rel = relationship( "CommonMetadataComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: CommonMetadataComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='common_metadata', source_slot='examples', mapping_type=None, target_class='example', target_slot='common_metadata_id', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.common_metadata_id]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="common_metadata_in_subset")
    
    
    see_also_rel = relationship( "CommonMetadataSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: CommonMetadataSeeAlso(see_also=x_))
    
    
    def __repr__(self):
        return f"common_metadata(id={self.id},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},)"
        
    
        
    


class Element(Base):
    """
    a named element in the model
    """
    __tablename__ = 'element'
    
    name = Column(Text(), primary_key=True)
    definition_uri = Column(Text())
    conforms_to = Column(Text())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    
    
    id_prefixes_rel = relationship( "ElementIdPrefixes" )
    id_prefixes = association_proxy("id_prefixes_rel", "id_prefixes",
                                  creator=lambda x_: ElementIdPrefixes(id_prefixes=x_))
    
    
    aliases_rel = relationship( "ElementAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: ElementAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='element', source_slot='local_names', mapping_type=None, target_class='local_name', target_slot='element_name', join_class=None, uses_join_table=None, multivalued=False)
    local_names = relationship( "LocalName", foreign_keys="[local_name.element_name]")
    
    
    mappings_rel = relationship( "ElementMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: ElementMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "ElementExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: ElementExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "ElementCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: ElementCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "ElementRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: ElementRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "ElementNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: ElementNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "ElementBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: ElementBroadMappings(broad_mappings=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='element', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='element_name', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.element_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='element', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='element_name', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.element_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='element', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='element_name', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.element_name]")
    
    
    todos_rel = relationship( "ElementTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: ElementTodos(todos=x_))
    
    
    notes_rel = relationship( "ElementNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: ElementNotes(notes=x_))
    
    
    comments_rel = relationship( "ElementComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: ElementComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='element', source_slot='examples', mapping_type=None, target_class='example', target_slot='element_name', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.element_name]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="element_in_subset")
    
    
    see_also_rel = relationship( "ElementSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: ElementSeeAlso(see_also=x_))
    
    
    def __repr__(self):
        return f"element(name={self.name},definition_uri={self.definition_uri},conforms_to={self.conforms_to},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},)"
        
    
        
    


class AnonymousTypeExpression(Base):
    """
    
    """
    __tablename__ = 'anonymous_type_expression'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    pattern = Column(Text())
    equals_string = Column(Text())
    equals_number = Column(Integer())
    
    
    equals_string_in_rel = relationship( "AnonymousTypeExpressionEqualsStringIn" )
    equals_string_in = association_proxy("equals_string_in_rel", "equals_string_in",
                                  creator=lambda x_: AnonymousTypeExpressionEqualsStringIn(equals_string_in=x_))
    
    
    # ManyToMany
    none_of = relationship( "AnonymousTypeExpression", secondary="anonymous_type_expression_none_of")
    
    
    # ManyToMany
    exactly_one_of = relationship( "AnonymousTypeExpression", secondary="anonymous_type_expression_exactly_one_of")
    
    
    # ManyToMany
    any_of = relationship( "AnonymousTypeExpression", secondary="anonymous_type_expression_any_of")
    
    
    # ManyToMany
    all_of = relationship( "AnonymousTypeExpression", secondary="anonymous_type_expression_all_of")
    
    
    def __repr__(self):
        return f"anonymous_type_expression(id={self.id},pattern={self.pattern},equals_string={self.equals_string},equals_number={self.equals_number},)"
        
    
        
    


class Expression(Base):
    """
    todo
    """
    __tablename__ = 'expression'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    
    
    def __repr__(self):
        return f"expression(id={self.id},)"
        
    
        
    


class AnonymousExpression(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_expression', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='anonymous_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.anonymous_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_expression', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='anonymous_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.anonymous_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_expression', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='anonymous_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.anonymous_expression_id]")
    
    
    todos_rel = relationship( "AnonymousExpressionTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: AnonymousExpressionTodos(todos=x_))
    
    
    notes_rel = relationship( "AnonymousExpressionNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: AnonymousExpressionNotes(notes=x_))
    
    
    comments_rel = relationship( "AnonymousExpressionComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: AnonymousExpressionComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_expression', source_slot='examples', mapping_type=None, target_class='example', target_slot='anonymous_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.anonymous_expression_id]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="anonymous_expression_in_subset")
    
    
    see_also_rel = relationship( "AnonymousExpressionSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: AnonymousExpressionSeeAlso(see_also=x_))
    
    
    def __repr__(self):
        return f"anonymous_expression(id={self.id},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},)"
        
    
        
    


class ClassExpression(Base):
    """
    A boolean expression that can be used to dynamically determine membership of a class
    """
    __tablename__ = 'class_expression'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    
    
    # ManyToMany
    any_of = relationship( "AnonymousClassExpression", secondary="class_expression_any_of")
    
    
    # ManyToMany
    exactly_one_of = relationship( "AnonymousClassExpression", secondary="class_expression_exactly_one_of")
    
    
    # ManyToMany
    none_of = relationship( "AnonymousClassExpression", secondary="class_expression_none_of")
    
    
    # ManyToMany
    all_of = relationship( "AnonymousClassExpression", secondary="class_expression_all_of")
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_expression', source_slot='slot_conditions', mapping_type=None, target_class='slot_definition', target_slot='class_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    slot_conditions = relationship( "SlotDefinition", foreign_keys="[slot_definition.class_expression_id]")
    
    
    def __repr__(self):
        return f"class_expression(id={self.id},)"
        
    
        
    


class ClassLevelRule(Base):
    """
    A rule that is applied to classes
    """
    __tablename__ = 'class_level_rule'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    
    
    def __repr__(self):
        return f"class_level_rule(id={self.id},)"
        
    
        
    


class Prefix(Base):
    """
    prefix URI tuple
    """
    __tablename__ = 'prefix'
    
    prefix_prefix = Column(Text(), primary_key=True)
    prefix_reference = Column(Text(), primary_key=True)
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"prefix(prefix_prefix={self.prefix_prefix},prefix_reference={self.prefix_reference},schema_definition_name={self.schema_definition_name},)"
        
    
        
    


class LocalName(Base):
    """
    an attributed label
    """
    __tablename__ = 'local_name'
    
    local_name_source = Column(Text(), primary_key=True)
    local_name_value = Column(Text(), primary_key=True)
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"local_name(local_name_source={self.local_name_source},local_name_value={self.local_name_value},element_name={self.element_name},schema_definition_name={self.schema_definition_name},type_definition_name={self.type_definition_name},subset_definition_name={self.subset_definition_name},definition_name={self.definition_name},enum_definition_name={self.enum_definition_name},slot_definition_name={self.slot_definition_name},class_definition_name={self.class_definition_name},)"
        
    
        
    


class Example(Base):
    """
    usage example and description
    """
    __tablename__ = 'example'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    value = Column(Text())
    description = Column(Text())
    common_metadata_id = Column(Text(), ForeignKey('common_metadata.id'))
    element_name = Column(Text(), ForeignKey('element.name'))
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'))
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'))
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'))
    definition_name = Column(Text(), ForeignKey('definition.name'))
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'))
    anonymous_expression_id = Column(Text(), ForeignKey('anonymous_expression.id'))
    anonymous_slot_expression_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'))
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'))
    anonymous_class_expression_id = Column(Text(), ForeignKey('anonymous_class_expression.id'))
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'))
    class_rule_id = Column(Text(), ForeignKey('class_rule.id'))
    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'))
    unique_key_id = Column(Text(), ForeignKey('unique_key.id'))
    
    
    def __repr__(self):
        return f"example(id={self.id},value={self.value},description={self.description},common_metadata_id={self.common_metadata_id},element_name={self.element_name},schema_definition_name={self.schema_definition_name},type_definition_name={self.type_definition_name},subset_definition_name={self.subset_definition_name},definition_name={self.definition_name},enum_definition_name={self.enum_definition_name},anonymous_expression_id={self.anonymous_expression_id},anonymous_slot_expression_id={self.anonymous_slot_expression_id},slot_definition_name={self.slot_definition_name},anonymous_class_expression_id={self.anonymous_class_expression_id},class_definition_name={self.class_definition_name},class_rule_id={self.class_rule_id},permissible_value_text={self.permissible_value_text},unique_key_id={self.unique_key_id},)"
        
    
        
    


class AltDescription(Base):
    """
    an attributed description
    """
    __tablename__ = 'alt_description'
    
    source = Column(Text(), primary_key=True)
    description = Column(Text(), primary_key=True)
    common_metadata_id = Column(Text(), ForeignKey('common_metadata.id'), primary_key=True)
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    anonymous_expression_id = Column(Text(), ForeignKey('anonymous_expression.id'), primary_key=True)
    anonymous_slot_expression_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    anonymous_class_expression_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    class_rule_id = Column(Text(), ForeignKey('class_rule.id'), primary_key=True)
    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    unique_key_id = Column(Text(), ForeignKey('unique_key.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"alt_description(source={self.source},description={self.description},common_metadata_id={self.common_metadata_id},element_name={self.element_name},schema_definition_name={self.schema_definition_name},type_definition_name={self.type_definition_name},subset_definition_name={self.subset_definition_name},definition_name={self.definition_name},enum_definition_name={self.enum_definition_name},anonymous_expression_id={self.anonymous_expression_id},anonymous_slot_expression_id={self.anonymous_slot_expression_id},slot_definition_name={self.slot_definition_name},anonymous_class_expression_id={self.anonymous_class_expression_id},class_definition_name={self.class_definition_name},class_rule_id={self.class_rule_id},permissible_value_text={self.permissible_value_text},unique_key_id={self.unique_key_id},)"
        
    
        
    


class PermissibleValue(Base):
    """
    a permissible value, accompanied by intended text and an optional mapping to a concept URI
    """
    __tablename__ = 'permissible_value'
    
    text = Column(Text(), primary_key=True)
    description = Column(Text())
    meaning = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'))
    
    
    # One-To-Many: OneToAnyMapping(source_class='permissible_value', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='permissible_value_text', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.permissible_value_text]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='permissible_value', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='permissible_value_text', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.permissible_value_text]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='permissible_value', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='permissible_value_text', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.permissible_value_text]")
    
    
    todos_rel = relationship( "PermissibleValueTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: PermissibleValueTodos(todos=x_))
    
    
    notes_rel = relationship( "PermissibleValueNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: PermissibleValueNotes(notes=x_))
    
    
    comments_rel = relationship( "PermissibleValueComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: PermissibleValueComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='permissible_value', source_slot='examples', mapping_type=None, target_class='example', target_slot='permissible_value_text', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.permissible_value_text]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="permissible_value_in_subset")
    
    
    see_also_rel = relationship( "PermissibleValueSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: PermissibleValueSeeAlso(see_also=x_))
    
    
    def __repr__(self):
        return f"permissible_value(text={self.text},description={self.description},meaning={self.meaning},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},enum_definition_name={self.enum_definition_name},)"
        
    
        
    


class UniqueKey(Base):
    """
    a collection of slots whose values uniquely identify an instance of a class
    """
    __tablename__ = 'unique_key'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'))
    
    
    # ManyToMany
    unique_key_slots = relationship( "SlotDefinition", secondary="unique_key_unique_key_slots")
    
    
    # One-To-Many: OneToAnyMapping(source_class='unique_key', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='unique_key_id', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.unique_key_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='unique_key', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='unique_key_id', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.unique_key_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='unique_key', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='unique_key_id', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.unique_key_id]")
    
    
    todos_rel = relationship( "UniqueKeyTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: UniqueKeyTodos(todos=x_))
    
    
    notes_rel = relationship( "UniqueKeyNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: UniqueKeyNotes(notes=x_))
    
    
    comments_rel = relationship( "UniqueKeyComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: UniqueKeyComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='unique_key', source_slot='examples', mapping_type=None, target_class='example', target_slot='unique_key_id', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.unique_key_id]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="unique_key_in_subset")
    
    
    see_also_rel = relationship( "UniqueKeySeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: UniqueKeySeeAlso(see_also=x_))
    
    
    def __repr__(self):
        return f"unique_key(id={self.id},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},class_definition_name={self.class_definition_name},)"
        
    
        
    


class Annotatable(Base):
    """
    mixin for classes that support annotations
    """
    __tablename__ = 'annotatable'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    
    
    # One-To-Many: OneToAnyMapping(source_class='annotatable', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='annotatable_id', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.annotatable_id]")
    
    
    def __repr__(self):
        return f"annotatable(id={self.id},)"
        
    
        
    


class Extension(Base):
    """
    a tag/value pair used to add non-model information to an entry
    """
    __tablename__ = 'extension'
    
    tag = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    anonymous_expression_id = Column(Text(), ForeignKey('anonymous_expression.id'), primary_key=True)
    anonymous_slot_expression_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    anonymous_class_expression_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    class_rule_id = Column(Text(), ForeignKey('class_rule.id'), primary_key=True)
    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    unique_key_id = Column(Text(), ForeignKey('unique_key.id'), primary_key=True)
    annotation_tag = Column(Text(), ForeignKey('annotation.tag'), primary_key=True)
    extension_tag = Column(Text(), ForeignKey('extension.tag'), primary_key=True)
    extensible_id = Column(Text(), ForeignKey('extensible.id'), primary_key=True)
    
    
    # One-To-Many: OneToAnyMapping(source_class='extension', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='extension_tag', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.extension_tag]")
    
    
    def __repr__(self):
        return f"extension(tag={self.tag},value={self.value},element_name={self.element_name},schema_definition_name={self.schema_definition_name},type_definition_name={self.type_definition_name},subset_definition_name={self.subset_definition_name},definition_name={self.definition_name},enum_definition_name={self.enum_definition_name},anonymous_expression_id={self.anonymous_expression_id},anonymous_slot_expression_id={self.anonymous_slot_expression_id},slot_definition_name={self.slot_definition_name},anonymous_class_expression_id={self.anonymous_class_expression_id},class_definition_name={self.class_definition_name},class_rule_id={self.class_rule_id},permissible_value_text={self.permissible_value_text},unique_key_id={self.unique_key_id},annotation_tag={self.annotation_tag},extension_tag={self.extension_tag},extensible_id={self.extensible_id},)"
        
    
        
    


class Extensible(Base):
    """
    mixin for classes that support extension
    """
    __tablename__ = 'extensible'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    
    
    # One-To-Many: OneToAnyMapping(source_class='extensible', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='extensible_id', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.extensible_id]")
    
    
    def __repr__(self):
        return f"extensible(id={self.id},)"
        
    
        
    


class CommonMetadataTodos(Base):
    """
    
    """
    __tablename__ = 'common_metadata_todos'
    
    common_metadata_id = Column(Text(), ForeignKey('common_metadata.id'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"common_metadata_todos(common_metadata_id={self.common_metadata_id},todos={self.todos},)"
        
    
        
    


class CommonMetadataNotes(Base):
    """
    
    """
    __tablename__ = 'common_metadata_notes'
    
    common_metadata_id = Column(Text(), ForeignKey('common_metadata.id'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"common_metadata_notes(common_metadata_id={self.common_metadata_id},notes={self.notes},)"
        
    
        
    


class CommonMetadataComments(Base):
    """
    
    """
    __tablename__ = 'common_metadata_comments'
    
    common_metadata_id = Column(Text(), ForeignKey('common_metadata.id'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"common_metadata_comments(common_metadata_id={self.common_metadata_id},comments={self.comments},)"
        
    
        
    


class CommonMetadataInSubset(Base):
    """
    
    """
    __tablename__ = 'common_metadata_in_subset'
    
    common_metadata_id = Column(Text(), ForeignKey('common_metadata.id'), primary_key=True)
    in_subset = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"common_metadata_in_subset(common_metadata_id={self.common_metadata_id},in_subset={self.in_subset},)"
        
    
        
    


class CommonMetadataSeeAlso(Base):
    """
    
    """
    __tablename__ = 'common_metadata_see_also'
    
    common_metadata_id = Column(Text(), ForeignKey('common_metadata.id'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"common_metadata_see_also(common_metadata_id={self.common_metadata_id},see_also={self.see_also},)"
        
    
        
    


class ElementIdPrefixes(Base):
    """
    
    """
    __tablename__ = 'element_id_prefixes'
    
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    id_prefixes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"element_id_prefixes(element_name={self.element_name},id_prefixes={self.id_prefixes},)"
        
    
        
    


class ElementAliases(Base):
    """
    
    """
    __tablename__ = 'element_aliases'
    
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"element_aliases(element_name={self.element_name},aliases={self.aliases},)"
        
    
        
    


class ElementMappings(Base):
    """
    
    """
    __tablename__ = 'element_mappings'
    
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"element_mappings(element_name={self.element_name},mappings={self.mappings},)"
        
    
        
    


class ElementExactMappings(Base):
    """
    
    """
    __tablename__ = 'element_exact_mappings'
    
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"element_exact_mappings(element_name={self.element_name},exact_mappings={self.exact_mappings},)"
        
    
        
    


class ElementCloseMappings(Base):
    """
    
    """
    __tablename__ = 'element_close_mappings'
    
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"element_close_mappings(element_name={self.element_name},close_mappings={self.close_mappings},)"
        
    
        
    


class ElementRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'element_related_mappings'
    
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"element_related_mappings(element_name={self.element_name},related_mappings={self.related_mappings},)"
        
    
        
    


class ElementNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'element_narrow_mappings'
    
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"element_narrow_mappings(element_name={self.element_name},narrow_mappings={self.narrow_mappings},)"
        
    
        
    


class ElementBroadMappings(Base):
    """
    
    """
    __tablename__ = 'element_broad_mappings'
    
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"element_broad_mappings(element_name={self.element_name},broad_mappings={self.broad_mappings},)"
        
    
        
    


class ElementTodos(Base):
    """
    
    """
    __tablename__ = 'element_todos'
    
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"element_todos(element_name={self.element_name},todos={self.todos},)"
        
    
        
    


class ElementNotes(Base):
    """
    
    """
    __tablename__ = 'element_notes'
    
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"element_notes(element_name={self.element_name},notes={self.notes},)"
        
    
        
    


class ElementComments(Base):
    """
    
    """
    __tablename__ = 'element_comments'
    
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"element_comments(element_name={self.element_name},comments={self.comments},)"
        
    
        
    


class ElementInSubset(Base):
    """
    
    """
    __tablename__ = 'element_in_subset'
    
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    in_subset = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"element_in_subset(element_name={self.element_name},in_subset={self.in_subset},)"
        
    
        
    


class ElementSeeAlso(Base):
    """
    
    """
    __tablename__ = 'element_see_also'
    
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"element_see_also(element_name={self.element_name},see_also={self.see_also},)"
        
    
        
    


class SchemaDefinitionImports(Base):
    """
    
    """
    __tablename__ = 'schema_definition_imports'
    
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    imports = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"schema_definition_imports(schema_definition_name={self.schema_definition_name},imports={self.imports},)"
        
    
        
    


class SchemaDefinitionEmitPrefixes(Base):
    """
    
    """
    __tablename__ = 'schema_definition_emit_prefixes'
    
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    emit_prefixes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"schema_definition_emit_prefixes(schema_definition_name={self.schema_definition_name},emit_prefixes={self.emit_prefixes},)"
        
    
        
    


class SchemaDefinitionDefaultCuriMaps(Base):
    """
    
    """
    __tablename__ = 'schema_definition_default_curi_maps'
    
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    default_curi_maps = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"schema_definition_default_curi_maps(schema_definition_name={self.schema_definition_name},default_curi_maps={self.default_curi_maps},)"
        
    
        
    


class SchemaDefinitionIdPrefixes(Base):
    """
    
    """
    __tablename__ = 'schema_definition_id_prefixes'
    
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    id_prefixes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"schema_definition_id_prefixes(schema_definition_name={self.schema_definition_name},id_prefixes={self.id_prefixes},)"
        
    
        
    


class SchemaDefinitionAliases(Base):
    """
    
    """
    __tablename__ = 'schema_definition_aliases'
    
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"schema_definition_aliases(schema_definition_name={self.schema_definition_name},aliases={self.aliases},)"
        
    
        
    


class SchemaDefinitionMappings(Base):
    """
    
    """
    __tablename__ = 'schema_definition_mappings'
    
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"schema_definition_mappings(schema_definition_name={self.schema_definition_name},mappings={self.mappings},)"
        
    
        
    


class SchemaDefinitionExactMappings(Base):
    """
    
    """
    __tablename__ = 'schema_definition_exact_mappings'
    
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"schema_definition_exact_mappings(schema_definition_name={self.schema_definition_name},exact_mappings={self.exact_mappings},)"
        
    
        
    


class SchemaDefinitionCloseMappings(Base):
    """
    
    """
    __tablename__ = 'schema_definition_close_mappings'
    
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"schema_definition_close_mappings(schema_definition_name={self.schema_definition_name},close_mappings={self.close_mappings},)"
        
    
        
    


class SchemaDefinitionRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'schema_definition_related_mappings'
    
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"schema_definition_related_mappings(schema_definition_name={self.schema_definition_name},related_mappings={self.related_mappings},)"
        
    
        
    


class SchemaDefinitionNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'schema_definition_narrow_mappings'
    
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"schema_definition_narrow_mappings(schema_definition_name={self.schema_definition_name},narrow_mappings={self.narrow_mappings},)"
        
    
        
    


class SchemaDefinitionBroadMappings(Base):
    """
    
    """
    __tablename__ = 'schema_definition_broad_mappings'
    
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"schema_definition_broad_mappings(schema_definition_name={self.schema_definition_name},broad_mappings={self.broad_mappings},)"
        
    
        
    


class SchemaDefinitionTodos(Base):
    """
    
    """
    __tablename__ = 'schema_definition_todos'
    
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"schema_definition_todos(schema_definition_name={self.schema_definition_name},todos={self.todos},)"
        
    
        
    


class SchemaDefinitionNotes(Base):
    """
    
    """
    __tablename__ = 'schema_definition_notes'
    
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"schema_definition_notes(schema_definition_name={self.schema_definition_name},notes={self.notes},)"
        
    
        
    


class SchemaDefinitionComments(Base):
    """
    
    """
    __tablename__ = 'schema_definition_comments'
    
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"schema_definition_comments(schema_definition_name={self.schema_definition_name},comments={self.comments},)"
        
    
        
    


class SchemaDefinitionInSubset(Base):
    """
    
    """
    __tablename__ = 'schema_definition_in_subset'
    
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    in_subset = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"schema_definition_in_subset(schema_definition_name={self.schema_definition_name},in_subset={self.in_subset},)"
        
    
        
    


class SchemaDefinitionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'schema_definition_see_also'
    
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"schema_definition_see_also(schema_definition_name={self.schema_definition_name},see_also={self.see_also},)"
        
    
        
    


class TypeExpressionEqualsStringIn(Base):
    """
    
    """
    __tablename__ = 'type_expression_equals_string_in'
    
    type_expression_id = Column(Text(), ForeignKey('type_expression.id'), primary_key=True)
    equals_string_in = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"type_expression_equals_string_in(type_expression_id={self.type_expression_id},equals_string_in={self.equals_string_in},)"
        
    
        
    


class TypeExpressionNoneOf(Base):
    """
    
    """
    __tablename__ = 'type_expression_none_of'
    
    type_expression_id = Column(Text(), ForeignKey('type_expression.id'), primary_key=True)
    none_of_id = Column(Text(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"type_expression_none_of(type_expression_id={self.type_expression_id},none_of_id={self.none_of_id},)"
        
    
        
    


class TypeExpressionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'type_expression_exactly_one_of'
    
    type_expression_id = Column(Text(), ForeignKey('type_expression.id'), primary_key=True)
    exactly_one_of_id = Column(Text(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"type_expression_exactly_one_of(type_expression_id={self.type_expression_id},exactly_one_of_id={self.exactly_one_of_id},)"
        
    
        
    


class TypeExpressionAnyOf(Base):
    """
    
    """
    __tablename__ = 'type_expression_any_of'
    
    type_expression_id = Column(Text(), ForeignKey('type_expression.id'), primary_key=True)
    any_of_id = Column(Text(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"type_expression_any_of(type_expression_id={self.type_expression_id},any_of_id={self.any_of_id},)"
        
    
        
    


class TypeExpressionAllOf(Base):
    """
    
    """
    __tablename__ = 'type_expression_all_of'
    
    type_expression_id = Column(Text(), ForeignKey('type_expression.id'), primary_key=True)
    all_of_id = Column(Text(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"type_expression_all_of(type_expression_id={self.type_expression_id},all_of_id={self.all_of_id},)"
        
    
        
    


class AnonymousTypeExpressionEqualsStringIn(Base):
    """
    
    """
    __tablename__ = 'anonymous_type_expression_equals_string_in'
    
    anonymous_type_expression_id = Column(Text(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    equals_string_in = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_type_expression_equals_string_in(anonymous_type_expression_id={self.anonymous_type_expression_id},equals_string_in={self.equals_string_in},)"
        
    
        
    


class AnonymousTypeExpressionNoneOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_type_expression_none_of'
    
    anonymous_type_expression_id = Column(Text(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    none_of_id = Column(Text(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_type_expression_none_of(anonymous_type_expression_id={self.anonymous_type_expression_id},none_of_id={self.none_of_id},)"
        
    
        
    


class AnonymousTypeExpressionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_type_expression_exactly_one_of'
    
    anonymous_type_expression_id = Column(Text(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    exactly_one_of_id = Column(Text(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_type_expression_exactly_one_of(anonymous_type_expression_id={self.anonymous_type_expression_id},exactly_one_of_id={self.exactly_one_of_id},)"
        
    
        
    


class AnonymousTypeExpressionAnyOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_type_expression_any_of'
    
    anonymous_type_expression_id = Column(Text(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    any_of_id = Column(Text(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_type_expression_any_of(anonymous_type_expression_id={self.anonymous_type_expression_id},any_of_id={self.any_of_id},)"
        
    
        
    


class AnonymousTypeExpressionAllOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_type_expression_all_of'
    
    anonymous_type_expression_id = Column(Text(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    all_of_id = Column(Text(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_type_expression_all_of(anonymous_type_expression_id={self.anonymous_type_expression_id},all_of_id={self.all_of_id},)"
        
    
        
    


class TypeDefinitionEqualsStringIn(Base):
    """
    
    """
    __tablename__ = 'type_definition_equals_string_in'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    equals_string_in = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_equals_string_in(type_definition_name={self.type_definition_name},equals_string_in={self.equals_string_in},)"
        
    
        
    


class TypeDefinitionNoneOf(Base):
    """
    
    """
    __tablename__ = 'type_definition_none_of'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    none_of_id = Column(Text(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_none_of(type_definition_name={self.type_definition_name},none_of_id={self.none_of_id},)"
        
    
        
    


class TypeDefinitionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'type_definition_exactly_one_of'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    exactly_one_of_id = Column(Text(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_exactly_one_of(type_definition_name={self.type_definition_name},exactly_one_of_id={self.exactly_one_of_id},)"
        
    
        
    


class TypeDefinitionAnyOf(Base):
    """
    
    """
    __tablename__ = 'type_definition_any_of'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    any_of_id = Column(Text(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_any_of(type_definition_name={self.type_definition_name},any_of_id={self.any_of_id},)"
        
    
        
    


class TypeDefinitionAllOf(Base):
    """
    
    """
    __tablename__ = 'type_definition_all_of'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    all_of_id = Column(Text(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_all_of(type_definition_name={self.type_definition_name},all_of_id={self.all_of_id},)"
        
    
        
    


class TypeDefinitionIdPrefixes(Base):
    """
    
    """
    __tablename__ = 'type_definition_id_prefixes'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    id_prefixes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_id_prefixes(type_definition_name={self.type_definition_name},id_prefixes={self.id_prefixes},)"
        
    
        
    


class TypeDefinitionAliases(Base):
    """
    
    """
    __tablename__ = 'type_definition_aliases'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_aliases(type_definition_name={self.type_definition_name},aliases={self.aliases},)"
        
    
        
    


class TypeDefinitionMappings(Base):
    """
    
    """
    __tablename__ = 'type_definition_mappings'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_mappings(type_definition_name={self.type_definition_name},mappings={self.mappings},)"
        
    
        
    


class TypeDefinitionExactMappings(Base):
    """
    
    """
    __tablename__ = 'type_definition_exact_mappings'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_exact_mappings(type_definition_name={self.type_definition_name},exact_mappings={self.exact_mappings},)"
        
    
        
    


class TypeDefinitionCloseMappings(Base):
    """
    
    """
    __tablename__ = 'type_definition_close_mappings'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_close_mappings(type_definition_name={self.type_definition_name},close_mappings={self.close_mappings},)"
        
    
        
    


class TypeDefinitionRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'type_definition_related_mappings'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_related_mappings(type_definition_name={self.type_definition_name},related_mappings={self.related_mappings},)"
        
    
        
    


class TypeDefinitionNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'type_definition_narrow_mappings'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_narrow_mappings(type_definition_name={self.type_definition_name},narrow_mappings={self.narrow_mappings},)"
        
    
        
    


class TypeDefinitionBroadMappings(Base):
    """
    
    """
    __tablename__ = 'type_definition_broad_mappings'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_broad_mappings(type_definition_name={self.type_definition_name},broad_mappings={self.broad_mappings},)"
        
    
        
    


class TypeDefinitionTodos(Base):
    """
    
    """
    __tablename__ = 'type_definition_todos'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_todos(type_definition_name={self.type_definition_name},todos={self.todos},)"
        
    
        
    


class TypeDefinitionNotes(Base):
    """
    
    """
    __tablename__ = 'type_definition_notes'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_notes(type_definition_name={self.type_definition_name},notes={self.notes},)"
        
    
        
    


class TypeDefinitionComments(Base):
    """
    
    """
    __tablename__ = 'type_definition_comments'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_comments(type_definition_name={self.type_definition_name},comments={self.comments},)"
        
    
        
    


class TypeDefinitionInSubset(Base):
    """
    
    """
    __tablename__ = 'type_definition_in_subset'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    in_subset = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_in_subset(type_definition_name={self.type_definition_name},in_subset={self.in_subset},)"
        
    
        
    


class TypeDefinitionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'type_definition_see_also'
    
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"type_definition_see_also(type_definition_name={self.type_definition_name},see_also={self.see_also},)"
        
    
        
    


class SubsetDefinitionIdPrefixes(Base):
    """
    
    """
    __tablename__ = 'subset_definition_id_prefixes'
    
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    id_prefixes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subset_definition_id_prefixes(subset_definition_name={self.subset_definition_name},id_prefixes={self.id_prefixes},)"
        
    
        
    


class SubsetDefinitionAliases(Base):
    """
    
    """
    __tablename__ = 'subset_definition_aliases'
    
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subset_definition_aliases(subset_definition_name={self.subset_definition_name},aliases={self.aliases},)"
        
    
        
    


class SubsetDefinitionMappings(Base):
    """
    
    """
    __tablename__ = 'subset_definition_mappings'
    
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subset_definition_mappings(subset_definition_name={self.subset_definition_name},mappings={self.mappings},)"
        
    
        
    


class SubsetDefinitionExactMappings(Base):
    """
    
    """
    __tablename__ = 'subset_definition_exact_mappings'
    
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subset_definition_exact_mappings(subset_definition_name={self.subset_definition_name},exact_mappings={self.exact_mappings},)"
        
    
        
    


class SubsetDefinitionCloseMappings(Base):
    """
    
    """
    __tablename__ = 'subset_definition_close_mappings'
    
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subset_definition_close_mappings(subset_definition_name={self.subset_definition_name},close_mappings={self.close_mappings},)"
        
    
        
    


class SubsetDefinitionRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'subset_definition_related_mappings'
    
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subset_definition_related_mappings(subset_definition_name={self.subset_definition_name},related_mappings={self.related_mappings},)"
        
    
        
    


class SubsetDefinitionNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'subset_definition_narrow_mappings'
    
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subset_definition_narrow_mappings(subset_definition_name={self.subset_definition_name},narrow_mappings={self.narrow_mappings},)"
        
    
        
    


class SubsetDefinitionBroadMappings(Base):
    """
    
    """
    __tablename__ = 'subset_definition_broad_mappings'
    
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subset_definition_broad_mappings(subset_definition_name={self.subset_definition_name},broad_mappings={self.broad_mappings},)"
        
    
        
    


class SubsetDefinitionTodos(Base):
    """
    
    """
    __tablename__ = 'subset_definition_todos'
    
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subset_definition_todos(subset_definition_name={self.subset_definition_name},todos={self.todos},)"
        
    
        
    


class SubsetDefinitionNotes(Base):
    """
    
    """
    __tablename__ = 'subset_definition_notes'
    
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subset_definition_notes(subset_definition_name={self.subset_definition_name},notes={self.notes},)"
        
    
        
    


class SubsetDefinitionComments(Base):
    """
    
    """
    __tablename__ = 'subset_definition_comments'
    
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subset_definition_comments(subset_definition_name={self.subset_definition_name},comments={self.comments},)"
        
    
        
    


class SubsetDefinitionInSubset(Base):
    """
    
    """
    __tablename__ = 'subset_definition_in_subset'
    
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    in_subset = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"subset_definition_in_subset(subset_definition_name={self.subset_definition_name},in_subset={self.in_subset},)"
        
    
        
    


class SubsetDefinitionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'subset_definition_see_also'
    
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"subset_definition_see_also(subset_definition_name={self.subset_definition_name},see_also={self.see_also},)"
        
    
        
    


class DefinitionMixins(Base):
    """
    
    """
    __tablename__ = 'definition_mixins'
    
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    mixins = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"definition_mixins(definition_name={self.definition_name},mixins={self.mixins},)"
        
    
        
    


class DefinitionApplyTo(Base):
    """
    
    """
    __tablename__ = 'definition_apply_to'
    
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    apply_to = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"definition_apply_to(definition_name={self.definition_name},apply_to={self.apply_to},)"
        
    
        
    


class DefinitionValuesFrom(Base):
    """
    
    """
    __tablename__ = 'definition_values_from'
    
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    values_from = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"definition_values_from(definition_name={self.definition_name},values_from={self.values_from},)"
        
    
        
    


class DefinitionIdPrefixes(Base):
    """
    
    """
    __tablename__ = 'definition_id_prefixes'
    
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    id_prefixes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"definition_id_prefixes(definition_name={self.definition_name},id_prefixes={self.id_prefixes},)"
        
    
        
    


class DefinitionAliases(Base):
    """
    
    """
    __tablename__ = 'definition_aliases'
    
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"definition_aliases(definition_name={self.definition_name},aliases={self.aliases},)"
        
    
        
    


class DefinitionMappings(Base):
    """
    
    """
    __tablename__ = 'definition_mappings'
    
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"definition_mappings(definition_name={self.definition_name},mappings={self.mappings},)"
        
    
        
    


class DefinitionExactMappings(Base):
    """
    
    """
    __tablename__ = 'definition_exact_mappings'
    
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"definition_exact_mappings(definition_name={self.definition_name},exact_mappings={self.exact_mappings},)"
        
    
        
    


class DefinitionCloseMappings(Base):
    """
    
    """
    __tablename__ = 'definition_close_mappings'
    
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"definition_close_mappings(definition_name={self.definition_name},close_mappings={self.close_mappings},)"
        
    
        
    


class DefinitionRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'definition_related_mappings'
    
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"definition_related_mappings(definition_name={self.definition_name},related_mappings={self.related_mappings},)"
        
    
        
    


class DefinitionNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'definition_narrow_mappings'
    
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"definition_narrow_mappings(definition_name={self.definition_name},narrow_mappings={self.narrow_mappings},)"
        
    
        
    


class DefinitionBroadMappings(Base):
    """
    
    """
    __tablename__ = 'definition_broad_mappings'
    
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"definition_broad_mappings(definition_name={self.definition_name},broad_mappings={self.broad_mappings},)"
        
    
        
    


class DefinitionTodos(Base):
    """
    
    """
    __tablename__ = 'definition_todos'
    
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"definition_todos(definition_name={self.definition_name},todos={self.todos},)"
        
    
        
    


class DefinitionNotes(Base):
    """
    
    """
    __tablename__ = 'definition_notes'
    
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"definition_notes(definition_name={self.definition_name},notes={self.notes},)"
        
    
        
    


class DefinitionComments(Base):
    """
    
    """
    __tablename__ = 'definition_comments'
    
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"definition_comments(definition_name={self.definition_name},comments={self.comments},)"
        
    
        
    


class DefinitionInSubset(Base):
    """
    
    """
    __tablename__ = 'definition_in_subset'
    
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    in_subset = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"definition_in_subset(definition_name={self.definition_name},in_subset={self.in_subset},)"
        
    
        
    


class DefinitionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'definition_see_also'
    
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"definition_see_also(definition_name={self.definition_name},see_also={self.see_also},)"
        
    
        
    


class EnumDefinitionIdPrefixes(Base):
    """
    
    """
    __tablename__ = 'enum_definition_id_prefixes'
    
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    id_prefixes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"enum_definition_id_prefixes(enum_definition_name={self.enum_definition_name},id_prefixes={self.id_prefixes},)"
        
    
        
    


class EnumDefinitionAliases(Base):
    """
    
    """
    __tablename__ = 'enum_definition_aliases'
    
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"enum_definition_aliases(enum_definition_name={self.enum_definition_name},aliases={self.aliases},)"
        
    
        
    


class EnumDefinitionMappings(Base):
    """
    
    """
    __tablename__ = 'enum_definition_mappings'
    
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"enum_definition_mappings(enum_definition_name={self.enum_definition_name},mappings={self.mappings},)"
        
    
        
    


class EnumDefinitionExactMappings(Base):
    """
    
    """
    __tablename__ = 'enum_definition_exact_mappings'
    
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"enum_definition_exact_mappings(enum_definition_name={self.enum_definition_name},exact_mappings={self.exact_mappings},)"
        
    
        
    


class EnumDefinitionCloseMappings(Base):
    """
    
    """
    __tablename__ = 'enum_definition_close_mappings'
    
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"enum_definition_close_mappings(enum_definition_name={self.enum_definition_name},close_mappings={self.close_mappings},)"
        
    
        
    


class EnumDefinitionRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'enum_definition_related_mappings'
    
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"enum_definition_related_mappings(enum_definition_name={self.enum_definition_name},related_mappings={self.related_mappings},)"
        
    
        
    


class EnumDefinitionNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'enum_definition_narrow_mappings'
    
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"enum_definition_narrow_mappings(enum_definition_name={self.enum_definition_name},narrow_mappings={self.narrow_mappings},)"
        
    
        
    


class EnumDefinitionBroadMappings(Base):
    """
    
    """
    __tablename__ = 'enum_definition_broad_mappings'
    
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"enum_definition_broad_mappings(enum_definition_name={self.enum_definition_name},broad_mappings={self.broad_mappings},)"
        
    
        
    


class EnumDefinitionTodos(Base):
    """
    
    """
    __tablename__ = 'enum_definition_todos'
    
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"enum_definition_todos(enum_definition_name={self.enum_definition_name},todos={self.todos},)"
        
    
        
    


class EnumDefinitionNotes(Base):
    """
    
    """
    __tablename__ = 'enum_definition_notes'
    
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"enum_definition_notes(enum_definition_name={self.enum_definition_name},notes={self.notes},)"
        
    
        
    


class EnumDefinitionComments(Base):
    """
    
    """
    __tablename__ = 'enum_definition_comments'
    
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"enum_definition_comments(enum_definition_name={self.enum_definition_name},comments={self.comments},)"
        
    
        
    


class EnumDefinitionInSubset(Base):
    """
    
    """
    __tablename__ = 'enum_definition_in_subset'
    
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    in_subset = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"enum_definition_in_subset(enum_definition_name={self.enum_definition_name},in_subset={self.in_subset},)"
        
    
        
    


class EnumDefinitionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'enum_definition_see_also'
    
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"enum_definition_see_also(enum_definition_name={self.enum_definition_name},see_also={self.see_also},)"
        
    
        
    


class AnonymousExpressionTodos(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_todos'
    
    anonymous_expression_id = Column(Text(), ForeignKey('anonymous_expression.id'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_expression_todos(anonymous_expression_id={self.anonymous_expression_id},todos={self.todos},)"
        
    
        
    


class AnonymousExpressionNotes(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_notes'
    
    anonymous_expression_id = Column(Text(), ForeignKey('anonymous_expression.id'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_expression_notes(anonymous_expression_id={self.anonymous_expression_id},notes={self.notes},)"
        
    
        
    


class AnonymousExpressionComments(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_comments'
    
    anonymous_expression_id = Column(Text(), ForeignKey('anonymous_expression.id'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_expression_comments(anonymous_expression_id={self.anonymous_expression_id},comments={self.comments},)"
        
    
        
    


class AnonymousExpressionInSubset(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_in_subset'
    
    anonymous_expression_id = Column(Text(), ForeignKey('anonymous_expression.id'), primary_key=True)
    in_subset = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_expression_in_subset(anonymous_expression_id={self.anonymous_expression_id},in_subset={self.in_subset},)"
        
    
        
    


class AnonymousExpressionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_see_also'
    
    anonymous_expression_id = Column(Text(), ForeignKey('anonymous_expression.id'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_expression_see_also(anonymous_expression_id={self.anonymous_expression_id},see_also={self.see_also},)"
        
    
        
    


class SlotExpressionEqualsStringIn(Base):
    """
    
    """
    __tablename__ = 'slot_expression_equals_string_in'
    
    slot_expression_id = Column(Text(), ForeignKey('slot_expression.id'), primary_key=True)
    equals_string_in = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_expression_equals_string_in(slot_expression_id={self.slot_expression_id},equals_string_in={self.equals_string_in},)"
        
    
        
    


class SlotExpressionNoneOf(Base):
    """
    
    """
    __tablename__ = 'slot_expression_none_of'
    
    slot_expression_id = Column(Text(), ForeignKey('slot_expression.id'), primary_key=True)
    none_of_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_expression_none_of(slot_expression_id={self.slot_expression_id},none_of_id={self.none_of_id},)"
        
    
        
    


class SlotExpressionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'slot_expression_exactly_one_of'
    
    slot_expression_id = Column(Text(), ForeignKey('slot_expression.id'), primary_key=True)
    exactly_one_of_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_expression_exactly_one_of(slot_expression_id={self.slot_expression_id},exactly_one_of_id={self.exactly_one_of_id},)"
        
    
        
    


class SlotExpressionAnyOf(Base):
    """
    
    """
    __tablename__ = 'slot_expression_any_of'
    
    slot_expression_id = Column(Text(), ForeignKey('slot_expression.id'), primary_key=True)
    any_of_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_expression_any_of(slot_expression_id={self.slot_expression_id},any_of_id={self.any_of_id},)"
        
    
        
    


class SlotExpressionAllOf(Base):
    """
    
    """
    __tablename__ = 'slot_expression_all_of'
    
    slot_expression_id = Column(Text(), ForeignKey('slot_expression.id'), primary_key=True)
    all_of_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_expression_all_of(slot_expression_id={self.slot_expression_id},all_of_id={self.all_of_id},)"
        
    
        
    


class AnonymousSlotExpressionEqualsStringIn(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_equals_string_in'
    
    anonymous_slot_expression_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    equals_string_in = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_slot_expression_equals_string_in(anonymous_slot_expression_id={self.anonymous_slot_expression_id},equals_string_in={self.equals_string_in},)"
        
    
        
    


class AnonymousSlotExpressionNoneOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_none_of'
    
    anonymous_slot_expression_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    none_of_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_slot_expression_none_of(anonymous_slot_expression_id={self.anonymous_slot_expression_id},none_of_id={self.none_of_id},)"
        
    
        
    


class AnonymousSlotExpressionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_exactly_one_of'
    
    anonymous_slot_expression_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    exactly_one_of_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_slot_expression_exactly_one_of(anonymous_slot_expression_id={self.anonymous_slot_expression_id},exactly_one_of_id={self.exactly_one_of_id},)"
        
    
        
    


class AnonymousSlotExpressionAnyOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_any_of'
    
    anonymous_slot_expression_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    any_of_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_slot_expression_any_of(anonymous_slot_expression_id={self.anonymous_slot_expression_id},any_of_id={self.any_of_id},)"
        
    
        
    


class AnonymousSlotExpressionAllOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_all_of'
    
    anonymous_slot_expression_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    all_of_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_slot_expression_all_of(anonymous_slot_expression_id={self.anonymous_slot_expression_id},all_of_id={self.all_of_id},)"
        
    
        
    


class AnonymousSlotExpressionTodos(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_todos'
    
    anonymous_slot_expression_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_slot_expression_todos(anonymous_slot_expression_id={self.anonymous_slot_expression_id},todos={self.todos},)"
        
    
        
    


class AnonymousSlotExpressionNotes(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_notes'
    
    anonymous_slot_expression_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_slot_expression_notes(anonymous_slot_expression_id={self.anonymous_slot_expression_id},notes={self.notes},)"
        
    
        
    


class AnonymousSlotExpressionComments(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_comments'
    
    anonymous_slot_expression_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_slot_expression_comments(anonymous_slot_expression_id={self.anonymous_slot_expression_id},comments={self.comments},)"
        
    
        
    


class AnonymousSlotExpressionInSubset(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_in_subset'
    
    anonymous_slot_expression_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    in_subset = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_slot_expression_in_subset(anonymous_slot_expression_id={self.anonymous_slot_expression_id},in_subset={self.in_subset},)"
        
    
        
    


class AnonymousSlotExpressionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_see_also'
    
    anonymous_slot_expression_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_slot_expression_see_also(anonymous_slot_expression_id={self.anonymous_slot_expression_id},see_also={self.see_also},)"
        
    
        
    


class SlotDefinitionDomainOf(Base):
    """
    
    """
    __tablename__ = 'slot_definition_domain_of'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    domain_of = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_domain_of(slot_definition_name={self.slot_definition_name},domain_of={self.domain_of},)"
        
    
        
    


class SlotDefinitionEqualsStringIn(Base):
    """
    
    """
    __tablename__ = 'slot_definition_equals_string_in'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    equals_string_in = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_equals_string_in(slot_definition_name={self.slot_definition_name},equals_string_in={self.equals_string_in},)"
        
    
        
    


class SlotDefinitionNoneOf(Base):
    """
    
    """
    __tablename__ = 'slot_definition_none_of'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    none_of_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_none_of(slot_definition_name={self.slot_definition_name},none_of_id={self.none_of_id},)"
        
    
        
    


class SlotDefinitionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'slot_definition_exactly_one_of'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    exactly_one_of_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_exactly_one_of(slot_definition_name={self.slot_definition_name},exactly_one_of_id={self.exactly_one_of_id},)"
        
    
        
    


class SlotDefinitionAnyOf(Base):
    """
    
    """
    __tablename__ = 'slot_definition_any_of'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    any_of_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_any_of(slot_definition_name={self.slot_definition_name},any_of_id={self.any_of_id},)"
        
    
        
    


class SlotDefinitionAllOf(Base):
    """
    
    """
    __tablename__ = 'slot_definition_all_of'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    all_of_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_all_of(slot_definition_name={self.slot_definition_name},all_of_id={self.all_of_id},)"
        
    
        
    


class SlotDefinitionMixins(Base):
    """
    
    """
    __tablename__ = 'slot_definition_mixins'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    mixins = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_mixins(slot_definition_name={self.slot_definition_name},mixins={self.mixins},)"
        
    
        
    


class SlotDefinitionApplyTo(Base):
    """
    
    """
    __tablename__ = 'slot_definition_apply_to'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    apply_to = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_apply_to(slot_definition_name={self.slot_definition_name},apply_to={self.apply_to},)"
        
    
        
    


class SlotDefinitionValuesFrom(Base):
    """
    
    """
    __tablename__ = 'slot_definition_values_from'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    values_from = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_values_from(slot_definition_name={self.slot_definition_name},values_from={self.values_from},)"
        
    
        
    


class SlotDefinitionIdPrefixes(Base):
    """
    
    """
    __tablename__ = 'slot_definition_id_prefixes'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    id_prefixes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_id_prefixes(slot_definition_name={self.slot_definition_name},id_prefixes={self.id_prefixes},)"
        
    
        
    


class SlotDefinitionAliases(Base):
    """
    
    """
    __tablename__ = 'slot_definition_aliases'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_aliases(slot_definition_name={self.slot_definition_name},aliases={self.aliases},)"
        
    
        
    


class SlotDefinitionMappings(Base):
    """
    
    """
    __tablename__ = 'slot_definition_mappings'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_mappings(slot_definition_name={self.slot_definition_name},mappings={self.mappings},)"
        
    
        
    


class SlotDefinitionExactMappings(Base):
    """
    
    """
    __tablename__ = 'slot_definition_exact_mappings'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_exact_mappings(slot_definition_name={self.slot_definition_name},exact_mappings={self.exact_mappings},)"
        
    
        
    


class SlotDefinitionCloseMappings(Base):
    """
    
    """
    __tablename__ = 'slot_definition_close_mappings'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_close_mappings(slot_definition_name={self.slot_definition_name},close_mappings={self.close_mappings},)"
        
    
        
    


class SlotDefinitionRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'slot_definition_related_mappings'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_related_mappings(slot_definition_name={self.slot_definition_name},related_mappings={self.related_mappings},)"
        
    
        
    


class SlotDefinitionNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'slot_definition_narrow_mappings'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_narrow_mappings(slot_definition_name={self.slot_definition_name},narrow_mappings={self.narrow_mappings},)"
        
    
        
    


class SlotDefinitionBroadMappings(Base):
    """
    
    """
    __tablename__ = 'slot_definition_broad_mappings'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_broad_mappings(slot_definition_name={self.slot_definition_name},broad_mappings={self.broad_mappings},)"
        
    
        
    


class SlotDefinitionTodos(Base):
    """
    
    """
    __tablename__ = 'slot_definition_todos'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_todos(slot_definition_name={self.slot_definition_name},todos={self.todos},)"
        
    
        
    


class SlotDefinitionNotes(Base):
    """
    
    """
    __tablename__ = 'slot_definition_notes'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_notes(slot_definition_name={self.slot_definition_name},notes={self.notes},)"
        
    
        
    


class SlotDefinitionComments(Base):
    """
    
    """
    __tablename__ = 'slot_definition_comments'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_comments(slot_definition_name={self.slot_definition_name},comments={self.comments},)"
        
    
        
    


class SlotDefinitionInSubset(Base):
    """
    
    """
    __tablename__ = 'slot_definition_in_subset'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    in_subset = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_in_subset(slot_definition_name={self.slot_definition_name},in_subset={self.in_subset},)"
        
    
        
    


class SlotDefinitionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'slot_definition_see_also'
    
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"slot_definition_see_also(slot_definition_name={self.slot_definition_name},see_also={self.see_also},)"
        
    
        
    


class ClassExpressionAnyOf(Base):
    """
    
    """
    __tablename__ = 'class_expression_any_of'
    
    class_expression_id = Column(Text(), ForeignKey('class_expression.id'), primary_key=True)
    any_of_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"class_expression_any_of(class_expression_id={self.class_expression_id},any_of_id={self.any_of_id},)"
        
    
        
    


class ClassExpressionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'class_expression_exactly_one_of'
    
    class_expression_id = Column(Text(), ForeignKey('class_expression.id'), primary_key=True)
    exactly_one_of_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"class_expression_exactly_one_of(class_expression_id={self.class_expression_id},exactly_one_of_id={self.exactly_one_of_id},)"
        
    
        
    


class ClassExpressionNoneOf(Base):
    """
    
    """
    __tablename__ = 'class_expression_none_of'
    
    class_expression_id = Column(Text(), ForeignKey('class_expression.id'), primary_key=True)
    none_of_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"class_expression_none_of(class_expression_id={self.class_expression_id},none_of_id={self.none_of_id},)"
        
    
        
    


class ClassExpressionAllOf(Base):
    """
    
    """
    __tablename__ = 'class_expression_all_of'
    
    class_expression_id = Column(Text(), ForeignKey('class_expression.id'), primary_key=True)
    all_of_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"class_expression_all_of(class_expression_id={self.class_expression_id},all_of_id={self.all_of_id},)"
        
    
        
    


class AnonymousClassExpressionAnyOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_any_of'
    
    anonymous_class_expression_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    any_of_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_class_expression_any_of(anonymous_class_expression_id={self.anonymous_class_expression_id},any_of_id={self.any_of_id},)"
        
    
        
    


class AnonymousClassExpressionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_exactly_one_of'
    
    anonymous_class_expression_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    exactly_one_of_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_class_expression_exactly_one_of(anonymous_class_expression_id={self.anonymous_class_expression_id},exactly_one_of_id={self.exactly_one_of_id},)"
        
    
        
    


class AnonymousClassExpressionNoneOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_none_of'
    
    anonymous_class_expression_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    none_of_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_class_expression_none_of(anonymous_class_expression_id={self.anonymous_class_expression_id},none_of_id={self.none_of_id},)"
        
    
        
    


class AnonymousClassExpressionAllOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_all_of'
    
    anonymous_class_expression_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    all_of_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_class_expression_all_of(anonymous_class_expression_id={self.anonymous_class_expression_id},all_of_id={self.all_of_id},)"
        
    
        
    


class AnonymousClassExpressionTodos(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_todos'
    
    anonymous_class_expression_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_class_expression_todos(anonymous_class_expression_id={self.anonymous_class_expression_id},todos={self.todos},)"
        
    
        
    


class AnonymousClassExpressionNotes(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_notes'
    
    anonymous_class_expression_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_class_expression_notes(anonymous_class_expression_id={self.anonymous_class_expression_id},notes={self.notes},)"
        
    
        
    


class AnonymousClassExpressionComments(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_comments'
    
    anonymous_class_expression_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_class_expression_comments(anonymous_class_expression_id={self.anonymous_class_expression_id},comments={self.comments},)"
        
    
        
    


class AnonymousClassExpressionInSubset(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_in_subset'
    
    anonymous_class_expression_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    in_subset = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_class_expression_in_subset(anonymous_class_expression_id={self.anonymous_class_expression_id},in_subset={self.in_subset},)"
        
    
        
    


class AnonymousClassExpressionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_see_also'
    
    anonymous_class_expression_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"anonymous_class_expression_see_also(anonymous_class_expression_id={self.anonymous_class_expression_id},see_also={self.see_also},)"
        
    
        
    


class ClassDefinitionSlots(Base):
    """
    
    """
    __tablename__ = 'class_definition_slots'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    slots = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_slots(class_definition_name={self.class_definition_name},slots={self.slots},)"
        
    
        
    


class ClassDefinitionUnionOf(Base):
    """
    
    """
    __tablename__ = 'class_definition_union_of'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    union_of = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_union_of(class_definition_name={self.class_definition_name},union_of={self.union_of},)"
        
    
        
    


class ClassDefinitionDefiningSlots(Base):
    """
    
    """
    __tablename__ = 'class_definition_defining_slots'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    defining_slots = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_defining_slots(class_definition_name={self.class_definition_name},defining_slots={self.defining_slots},)"
        
    
        
    


class ClassDefinitionAnyOf(Base):
    """
    
    """
    __tablename__ = 'class_definition_any_of'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    any_of_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_any_of(class_definition_name={self.class_definition_name},any_of_id={self.any_of_id},)"
        
    
        
    


class ClassDefinitionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'class_definition_exactly_one_of'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    exactly_one_of_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_exactly_one_of(class_definition_name={self.class_definition_name},exactly_one_of_id={self.exactly_one_of_id},)"
        
    
        
    


class ClassDefinitionNoneOf(Base):
    """
    
    """
    __tablename__ = 'class_definition_none_of'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    none_of_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_none_of(class_definition_name={self.class_definition_name},none_of_id={self.none_of_id},)"
        
    
        
    


class ClassDefinitionAllOf(Base):
    """
    
    """
    __tablename__ = 'class_definition_all_of'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    all_of_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_all_of(class_definition_name={self.class_definition_name},all_of_id={self.all_of_id},)"
        
    
        
    


class ClassDefinitionMixins(Base):
    """
    
    """
    __tablename__ = 'class_definition_mixins'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    mixins = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_mixins(class_definition_name={self.class_definition_name},mixins={self.mixins},)"
        
    
        
    


class ClassDefinitionApplyTo(Base):
    """
    
    """
    __tablename__ = 'class_definition_apply_to'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    apply_to = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_apply_to(class_definition_name={self.class_definition_name},apply_to={self.apply_to},)"
        
    
        
    


class ClassDefinitionValuesFrom(Base):
    """
    
    """
    __tablename__ = 'class_definition_values_from'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    values_from = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_values_from(class_definition_name={self.class_definition_name},values_from={self.values_from},)"
        
    
        
    


class ClassDefinitionIdPrefixes(Base):
    """
    
    """
    __tablename__ = 'class_definition_id_prefixes'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    id_prefixes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_id_prefixes(class_definition_name={self.class_definition_name},id_prefixes={self.id_prefixes},)"
        
    
        
    


class ClassDefinitionAliases(Base):
    """
    
    """
    __tablename__ = 'class_definition_aliases'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_aliases(class_definition_name={self.class_definition_name},aliases={self.aliases},)"
        
    
        
    


class ClassDefinitionMappings(Base):
    """
    
    """
    __tablename__ = 'class_definition_mappings'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_mappings(class_definition_name={self.class_definition_name},mappings={self.mappings},)"
        
    
        
    


class ClassDefinitionExactMappings(Base):
    """
    
    """
    __tablename__ = 'class_definition_exact_mappings'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_exact_mappings(class_definition_name={self.class_definition_name},exact_mappings={self.exact_mappings},)"
        
    
        
    


class ClassDefinitionCloseMappings(Base):
    """
    
    """
    __tablename__ = 'class_definition_close_mappings'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_close_mappings(class_definition_name={self.class_definition_name},close_mappings={self.close_mappings},)"
        
    
        
    


class ClassDefinitionRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'class_definition_related_mappings'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_related_mappings(class_definition_name={self.class_definition_name},related_mappings={self.related_mappings},)"
        
    
        
    


class ClassDefinitionNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'class_definition_narrow_mappings'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_narrow_mappings(class_definition_name={self.class_definition_name},narrow_mappings={self.narrow_mappings},)"
        
    
        
    


class ClassDefinitionBroadMappings(Base):
    """
    
    """
    __tablename__ = 'class_definition_broad_mappings'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_broad_mappings(class_definition_name={self.class_definition_name},broad_mappings={self.broad_mappings},)"
        
    
        
    


class ClassDefinitionTodos(Base):
    """
    
    """
    __tablename__ = 'class_definition_todos'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_todos(class_definition_name={self.class_definition_name},todos={self.todos},)"
        
    
        
    


class ClassDefinitionNotes(Base):
    """
    
    """
    __tablename__ = 'class_definition_notes'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_notes(class_definition_name={self.class_definition_name},notes={self.notes},)"
        
    
        
    


class ClassDefinitionComments(Base):
    """
    
    """
    __tablename__ = 'class_definition_comments'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_comments(class_definition_name={self.class_definition_name},comments={self.comments},)"
        
    
        
    


class ClassDefinitionInSubset(Base):
    """
    
    """
    __tablename__ = 'class_definition_in_subset'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    in_subset = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_in_subset(class_definition_name={self.class_definition_name},in_subset={self.in_subset},)"
        
    
        
    


class ClassDefinitionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'class_definition_see_also'
    
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_definition_see_also(class_definition_name={self.class_definition_name},see_also={self.see_also},)"
        
    
        
    


class ClassRuleTodos(Base):
    """
    
    """
    __tablename__ = 'class_rule_todos'
    
    class_rule_id = Column(Text(), ForeignKey('class_rule.id'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_rule_todos(class_rule_id={self.class_rule_id},todos={self.todos},)"
        
    
        
    


class ClassRuleNotes(Base):
    """
    
    """
    __tablename__ = 'class_rule_notes'
    
    class_rule_id = Column(Text(), ForeignKey('class_rule.id'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_rule_notes(class_rule_id={self.class_rule_id},notes={self.notes},)"
        
    
        
    


class ClassRuleComments(Base):
    """
    
    """
    __tablename__ = 'class_rule_comments'
    
    class_rule_id = Column(Text(), ForeignKey('class_rule.id'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_rule_comments(class_rule_id={self.class_rule_id},comments={self.comments},)"
        
    
        
    


class ClassRuleInSubset(Base):
    """
    
    """
    __tablename__ = 'class_rule_in_subset'
    
    class_rule_id = Column(Text(), ForeignKey('class_rule.id'), primary_key=True)
    in_subset = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"class_rule_in_subset(class_rule_id={self.class_rule_id},in_subset={self.in_subset},)"
        
    
        
    


class ClassRuleSeeAlso(Base):
    """
    
    """
    __tablename__ = 'class_rule_see_also'
    
    class_rule_id = Column(Text(), ForeignKey('class_rule.id'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"class_rule_see_also(class_rule_id={self.class_rule_id},see_also={self.see_also},)"
        
    
        
    


class PermissibleValueTodos(Base):
    """
    
    """
    __tablename__ = 'permissible_value_todos'
    
    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"permissible_value_todos(permissible_value_text={self.permissible_value_text},todos={self.todos},)"
        
    
        
    


class PermissibleValueNotes(Base):
    """
    
    """
    __tablename__ = 'permissible_value_notes'
    
    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"permissible_value_notes(permissible_value_text={self.permissible_value_text},notes={self.notes},)"
        
    
        
    


class PermissibleValueComments(Base):
    """
    
    """
    __tablename__ = 'permissible_value_comments'
    
    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"permissible_value_comments(permissible_value_text={self.permissible_value_text},comments={self.comments},)"
        
    
        
    


class PermissibleValueInSubset(Base):
    """
    
    """
    __tablename__ = 'permissible_value_in_subset'
    
    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    in_subset = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"permissible_value_in_subset(permissible_value_text={self.permissible_value_text},in_subset={self.in_subset},)"
        
    
        
    


class PermissibleValueSeeAlso(Base):
    """
    
    """
    __tablename__ = 'permissible_value_see_also'
    
    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"permissible_value_see_also(permissible_value_text={self.permissible_value_text},see_also={self.see_also},)"
        
    
        
    


class UniqueKeyUniqueKeySlots(Base):
    """
    
    """
    __tablename__ = 'unique_key_unique_key_slots'
    
    unique_key_id = Column(Text(), ForeignKey('unique_key.id'), primary_key=True)
    unique_key_slots = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"unique_key_unique_key_slots(unique_key_id={self.unique_key_id},unique_key_slots={self.unique_key_slots},)"
        
    
        
    


class UniqueKeyTodos(Base):
    """
    
    """
    __tablename__ = 'unique_key_todos'
    
    unique_key_id = Column(Text(), ForeignKey('unique_key.id'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"unique_key_todos(unique_key_id={self.unique_key_id},todos={self.todos},)"
        
    
        
    


class UniqueKeyNotes(Base):
    """
    
    """
    __tablename__ = 'unique_key_notes'
    
    unique_key_id = Column(Text(), ForeignKey('unique_key.id'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"unique_key_notes(unique_key_id={self.unique_key_id},notes={self.notes},)"
        
    
        
    


class UniqueKeyComments(Base):
    """
    
    """
    __tablename__ = 'unique_key_comments'
    
    unique_key_id = Column(Text(), ForeignKey('unique_key.id'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"unique_key_comments(unique_key_id={self.unique_key_id},comments={self.comments},)"
        
    
        
    


class UniqueKeyInSubset(Base):
    """
    
    """
    __tablename__ = 'unique_key_in_subset'
    
    unique_key_id = Column(Text(), ForeignKey('unique_key.id'), primary_key=True)
    in_subset = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    
    
    def __repr__(self):
        return f"unique_key_in_subset(unique_key_id={self.unique_key_id},in_subset={self.in_subset},)"
        
    
        
    


class UniqueKeySeeAlso(Base):
    """
    
    """
    __tablename__ = 'unique_key_see_also'
    
    unique_key_id = Column(Text(), ForeignKey('unique_key.id'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    
    
    def __repr__(self):
        return f"unique_key_see_also(unique_key_id={self.unique_key_id},see_also={self.see_also},)"
        
    
        
    


class SchemaDefinition(Element):
    """
    a collection of subset, type, slot and class definitions
    """
    __tablename__ = 'schema_definition'
    
    id = Column(Text(), primary_key=True)
    version = Column(Text())
    license = Column(Text())
    default_prefix = Column(Text())
    default_range = Column(Text(), ForeignKey('type_definition.name'))
    metamodel_version = Column(Text())
    source_file = Column(Text())
    source_file_date = Column(DateTime())
    source_file_size = Column(Integer())
    generation_date = Column(DateTime())
    name = Column(Text())
    definition_uri = Column(Text())
    conforms_to = Column(Text())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    
    
    imports_rel = relationship( "SchemaDefinitionImports" )
    imports = association_proxy("imports_rel", "imports",
                                  creator=lambda x_: SchemaDefinitionImports(imports=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='schema_definition', source_slot='prefixes', mapping_type=None, target_class='prefix', target_slot='schema_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    prefixes = relationship( "Prefix", foreign_keys="[prefix.schema_definition_name]")
    
    
    emit_prefixes_rel = relationship( "SchemaDefinitionEmitPrefixes" )
    emit_prefixes = association_proxy("emit_prefixes_rel", "emit_prefixes",
                                  creator=lambda x_: SchemaDefinitionEmitPrefixes(emit_prefixes=x_))
    
    
    default_curi_maps_rel = relationship( "SchemaDefinitionDefaultCuriMaps" )
    default_curi_maps = association_proxy("default_curi_maps_rel", "default_curi_maps",
                                  creator=lambda x_: SchemaDefinitionDefaultCuriMaps(default_curi_maps=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='schema_definition', source_slot='subsets', mapping_type=None, target_class='subset_definition', target_slot='schema_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    subsets = relationship( "SubsetDefinition", foreign_keys="[subset_definition.schema_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='schema_definition', source_slot='types', mapping_type=None, target_class='type_definition', target_slot='schema_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    types = relationship( "TypeDefinition", foreign_keys="[type_definition.schema_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='schema_definition', source_slot='enums', mapping_type=None, target_class='enum_definition', target_slot='schema_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    enums = relationship( "EnumDefinition", foreign_keys="[enum_definition.schema_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='schema_definition', source_slot='slots', mapping_type=None, target_class='slot_definition', target_slot='schema_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    slots = relationship( "SlotDefinition", foreign_keys="[slot_definition.schema_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='schema_definition', source_slot='classes', mapping_type=None, target_class='class_definition', target_slot='schema_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    classes = relationship( "ClassDefinition", foreign_keys="[class_definition.schema_definition_name]")
    
    
    id_prefixes_rel = relationship( "SchemaDefinitionIdPrefixes" )
    id_prefixes = association_proxy("id_prefixes_rel", "id_prefixes",
                                  creator=lambda x_: SchemaDefinitionIdPrefixes(id_prefixes=x_))
    
    
    aliases_rel = relationship( "SchemaDefinitionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: SchemaDefinitionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='schema_definition', source_slot='local_names', mapping_type=None, target_class='local_name', target_slot='schema_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    local_names = relationship( "LocalName", foreign_keys="[local_name.schema_definition_name]")
    
    
    mappings_rel = relationship( "SchemaDefinitionMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: SchemaDefinitionMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "SchemaDefinitionExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: SchemaDefinitionExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "SchemaDefinitionCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: SchemaDefinitionCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "SchemaDefinitionRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: SchemaDefinitionRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "SchemaDefinitionNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: SchemaDefinitionNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "SchemaDefinitionBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: SchemaDefinitionBroadMappings(broad_mappings=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='schema_definition', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='schema_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.schema_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='schema_definition', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='schema_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.schema_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='schema_definition', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='schema_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.schema_definition_name]")
    
    
    todos_rel = relationship( "SchemaDefinitionTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: SchemaDefinitionTodos(todos=x_))
    
    
    notes_rel = relationship( "SchemaDefinitionNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: SchemaDefinitionNotes(notes=x_))
    
    
    comments_rel = relationship( "SchemaDefinitionComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: SchemaDefinitionComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='schema_definition', source_slot='examples', mapping_type=None, target_class='example', target_slot='schema_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.schema_definition_name]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="schema_definition_in_subset")
    
    
    see_also_rel = relationship( "SchemaDefinitionSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: SchemaDefinitionSeeAlso(see_also=x_))
    
    
    def __repr__(self):
        return f"schema_definition(id={self.id},version={self.version},license={self.license},default_prefix={self.default_prefix},default_range={self.default_range},metamodel_version={self.metamodel_version},source_file={self.source_file},source_file_date={self.source_file_date},source_file_size={self.source_file_size},generation_date={self.generation_date},name={self.name},definition_uri={self.definition_uri},conforms_to={self.conforms_to},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class TypeExpression(Expression):
    """
    
    """
    __tablename__ = 'type_expression'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    pattern = Column(Text())
    equals_string = Column(Text())
    equals_number = Column(Integer())
    
    
    equals_string_in_rel = relationship( "TypeExpressionEqualsStringIn" )
    equals_string_in = association_proxy("equals_string_in_rel", "equals_string_in",
                                  creator=lambda x_: TypeExpressionEqualsStringIn(equals_string_in=x_))
    
    
    # ManyToMany
    none_of = relationship( "AnonymousTypeExpression", secondary="type_expression_none_of")
    
    
    # ManyToMany
    exactly_one_of = relationship( "AnonymousTypeExpression", secondary="type_expression_exactly_one_of")
    
    
    # ManyToMany
    any_of = relationship( "AnonymousTypeExpression", secondary="type_expression_any_of")
    
    
    # ManyToMany
    all_of = relationship( "AnonymousTypeExpression", secondary="type_expression_all_of")
    
    
    def __repr__(self):
        return f"type_expression(id={self.id},pattern={self.pattern},equals_string={self.equals_string},equals_number={self.equals_number},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class TypeDefinition(Element):
    """
    A data type definition.
    """
    __tablename__ = 'type_definition'
    
    typeof = Column(Text(), ForeignKey('type_definition.name'))
    base = Column(Text())
    uri = Column(Text())
    repr = Column(Text())
    pattern = Column(Text())
    equals_string = Column(Text())
    equals_number = Column(Integer())
    name = Column(Text(), primary_key=True)
    definition_uri = Column(Text())
    conforms_to = Column(Text())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'))
    
    
    equals_string_in_rel = relationship( "TypeDefinitionEqualsStringIn" )
    equals_string_in = association_proxy("equals_string_in_rel", "equals_string_in",
                                  creator=lambda x_: TypeDefinitionEqualsStringIn(equals_string_in=x_))
    
    
    # ManyToMany
    none_of = relationship( "AnonymousTypeExpression", secondary="type_definition_none_of")
    
    
    # ManyToMany
    exactly_one_of = relationship( "AnonymousTypeExpression", secondary="type_definition_exactly_one_of")
    
    
    # ManyToMany
    any_of = relationship( "AnonymousTypeExpression", secondary="type_definition_any_of")
    
    
    # ManyToMany
    all_of = relationship( "AnonymousTypeExpression", secondary="type_definition_all_of")
    
    
    id_prefixes_rel = relationship( "TypeDefinitionIdPrefixes" )
    id_prefixes = association_proxy("id_prefixes_rel", "id_prefixes",
                                  creator=lambda x_: TypeDefinitionIdPrefixes(id_prefixes=x_))
    
    
    aliases_rel = relationship( "TypeDefinitionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: TypeDefinitionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='type_definition', source_slot='local_names', mapping_type=None, target_class='local_name', target_slot='type_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    local_names = relationship( "LocalName", foreign_keys="[local_name.type_definition_name]")
    
    
    mappings_rel = relationship( "TypeDefinitionMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: TypeDefinitionMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "TypeDefinitionExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: TypeDefinitionExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "TypeDefinitionCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: TypeDefinitionCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "TypeDefinitionRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: TypeDefinitionRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "TypeDefinitionNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: TypeDefinitionNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "TypeDefinitionBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: TypeDefinitionBroadMappings(broad_mappings=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='type_definition', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='type_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.type_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='type_definition', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='type_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.type_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='type_definition', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='type_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.type_definition_name]")
    
    
    todos_rel = relationship( "TypeDefinitionTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: TypeDefinitionTodos(todos=x_))
    
    
    notes_rel = relationship( "TypeDefinitionNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: TypeDefinitionNotes(notes=x_))
    
    
    comments_rel = relationship( "TypeDefinitionComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: TypeDefinitionComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='type_definition', source_slot='examples', mapping_type=None, target_class='example', target_slot='type_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.type_definition_name]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="type_definition_in_subset")
    
    
    see_also_rel = relationship( "TypeDefinitionSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: TypeDefinitionSeeAlso(see_also=x_))
    
    
    def __repr__(self):
        return f"type_definition(typeof={self.typeof},base={self.base},uri={self.uri},repr={self.repr},pattern={self.pattern},equals_string={self.equals_string},equals_number={self.equals_number},name={self.name},definition_uri={self.definition_uri},conforms_to={self.conforms_to},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},schema_definition_name={self.schema_definition_name},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class SubsetDefinition(Element):
    """
    the name and description of a subset
    """
    __tablename__ = 'subset_definition'
    
    name = Column(Text(), primary_key=True)
    definition_uri = Column(Text())
    conforms_to = Column(Text())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'))
    
    
    id_prefixes_rel = relationship( "SubsetDefinitionIdPrefixes" )
    id_prefixes = association_proxy("id_prefixes_rel", "id_prefixes",
                                  creator=lambda x_: SubsetDefinitionIdPrefixes(id_prefixes=x_))
    
    
    aliases_rel = relationship( "SubsetDefinitionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: SubsetDefinitionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='subset_definition', source_slot='local_names', mapping_type=None, target_class='local_name', target_slot='subset_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    local_names = relationship( "LocalName", foreign_keys="[local_name.subset_definition_name]")
    
    
    mappings_rel = relationship( "SubsetDefinitionMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: SubsetDefinitionMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "SubsetDefinitionExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: SubsetDefinitionExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "SubsetDefinitionCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: SubsetDefinitionCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "SubsetDefinitionRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: SubsetDefinitionRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "SubsetDefinitionNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: SubsetDefinitionNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "SubsetDefinitionBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: SubsetDefinitionBroadMappings(broad_mappings=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='subset_definition', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='subset_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.subset_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='subset_definition', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='subset_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.subset_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='subset_definition', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='subset_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.subset_definition_name]")
    
    
    todos_rel = relationship( "SubsetDefinitionTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: SubsetDefinitionTodos(todos=x_))
    
    
    notes_rel = relationship( "SubsetDefinitionNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: SubsetDefinitionNotes(notes=x_))
    
    
    comments_rel = relationship( "SubsetDefinitionComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: SubsetDefinitionComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='subset_definition', source_slot='examples', mapping_type=None, target_class='example', target_slot='subset_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.subset_definition_name]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="subset_definition_in_subset")
    
    
    see_also_rel = relationship( "SubsetDefinitionSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: SubsetDefinitionSeeAlso(see_also=x_))
    
    
    def __repr__(self):
        return f"subset_definition(name={self.name},definition_uri={self.definition_uri},conforms_to={self.conforms_to},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},schema_definition_name={self.schema_definition_name},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class Definition(Element):
    """
    base class for definitions
    """
    __tablename__ = 'definition'
    
    is_a = Column(Text(), ForeignKey('definition.name'))
    abstract = Column(Boolean())
    mixin = Column(Boolean())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    string_serialization = Column(Text())
    name = Column(Text(), primary_key=True)
    definition_uri = Column(Text())
    conforms_to = Column(Text())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    
    
    # ManyToMany
    mixins = relationship( "Definition", secondary="definition_mixins")
    
    
    # ManyToMany
    apply_to = relationship( "Definition", secondary="definition_apply_to")
    
    
    values_from_rel = relationship( "DefinitionValuesFrom" )
    values_from = association_proxy("values_from_rel", "values_from",
                                  creator=lambda x_: DefinitionValuesFrom(values_from=x_))
    
    
    id_prefixes_rel = relationship( "DefinitionIdPrefixes" )
    id_prefixes = association_proxy("id_prefixes_rel", "id_prefixes",
                                  creator=lambda x_: DefinitionIdPrefixes(id_prefixes=x_))
    
    
    aliases_rel = relationship( "DefinitionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: DefinitionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='definition', source_slot='local_names', mapping_type=None, target_class='local_name', target_slot='definition_name', join_class=None, uses_join_table=None, multivalued=False)
    local_names = relationship( "LocalName", foreign_keys="[local_name.definition_name]")
    
    
    mappings_rel = relationship( "DefinitionMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: DefinitionMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "DefinitionExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: DefinitionExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "DefinitionCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: DefinitionCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "DefinitionRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: DefinitionRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "DefinitionNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: DefinitionNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "DefinitionBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: DefinitionBroadMappings(broad_mappings=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='definition', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='definition_name', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='definition', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='definition_name', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='definition', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='definition_name', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.definition_name]")
    
    
    todos_rel = relationship( "DefinitionTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: DefinitionTodos(todos=x_))
    
    
    notes_rel = relationship( "DefinitionNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: DefinitionNotes(notes=x_))
    
    
    comments_rel = relationship( "DefinitionComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: DefinitionComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='definition', source_slot='examples', mapping_type=None, target_class='example', target_slot='definition_name', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.definition_name]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="definition_in_subset")
    
    
    see_also_rel = relationship( "DefinitionSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: DefinitionSeeAlso(see_also=x_))
    
    
    def __repr__(self):
        return f"definition(is_a={self.is_a},abstract={self.abstract},mixin={self.mixin},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},string_serialization={self.string_serialization},name={self.name},definition_uri={self.definition_uri},conforms_to={self.conforms_to},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class EnumDefinition(Element):
    """
    List of values that constrain the range of a slot
    """
    __tablename__ = 'enum_definition'
    
    code_set = Column(Text())
    code_set_tag = Column(Text())
    code_set_version = Column(Text())
    pv_formula = Column(Enum('CODE', 'CURIE', 'URI', 'FHIR_CODING', name='pv_formula_options'))
    name = Column(Text(), primary_key=True)
    definition_uri = Column(Text())
    conforms_to = Column(Text())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'))
    
    
    # One-To-Many: OneToAnyMapping(source_class='enum_definition', source_slot='permissible_values', mapping_type=None, target_class='permissible_value', target_slot='enum_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    permissible_values = relationship( "PermissibleValue", foreign_keys="[permissible_value.enum_definition_name]")
    
    
    id_prefixes_rel = relationship( "EnumDefinitionIdPrefixes" )
    id_prefixes = association_proxy("id_prefixes_rel", "id_prefixes",
                                  creator=lambda x_: EnumDefinitionIdPrefixes(id_prefixes=x_))
    
    
    aliases_rel = relationship( "EnumDefinitionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: EnumDefinitionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='enum_definition', source_slot='local_names', mapping_type=None, target_class='local_name', target_slot='enum_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    local_names = relationship( "LocalName", foreign_keys="[local_name.enum_definition_name]")
    
    
    mappings_rel = relationship( "EnumDefinitionMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: EnumDefinitionMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "EnumDefinitionExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: EnumDefinitionExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "EnumDefinitionCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: EnumDefinitionCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "EnumDefinitionRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: EnumDefinitionRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "EnumDefinitionNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: EnumDefinitionNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "EnumDefinitionBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: EnumDefinitionBroadMappings(broad_mappings=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='enum_definition', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='enum_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.enum_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='enum_definition', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='enum_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.enum_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='enum_definition', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='enum_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.enum_definition_name]")
    
    
    todos_rel = relationship( "EnumDefinitionTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: EnumDefinitionTodos(todos=x_))
    
    
    notes_rel = relationship( "EnumDefinitionNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: EnumDefinitionNotes(notes=x_))
    
    
    comments_rel = relationship( "EnumDefinitionComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: EnumDefinitionComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='enum_definition', source_slot='examples', mapping_type=None, target_class='example', target_slot='enum_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.enum_definition_name]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="enum_definition_in_subset")
    
    
    see_also_rel = relationship( "EnumDefinitionSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: EnumDefinitionSeeAlso(see_also=x_))
    
    
    def __repr__(self):
        return f"enum_definition(code_set={self.code_set},code_set_tag={self.code_set_tag},code_set_version={self.code_set_version},pv_formula={self.pv_formula},name={self.name},definition_uri={self.definition_uri},conforms_to={self.conforms_to},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},schema_definition_name={self.schema_definition_name},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class SlotExpression(Expression):
    """
    an expression that constrains the range of values a slot can take
    """
    __tablename__ = 'slot_expression'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    range = Column(Text(), ForeignKey('element.name'))
    required = Column(Boolean())
    recommended = Column(Boolean())
    minimum_value = Column(Integer())
    maximum_value = Column(Integer())
    pattern = Column(Text())
    equals_string = Column(Text())
    equals_number = Column(Integer())
    equals_expression = Column(Text())
    minimum_cardinality = Column(Integer())
    maximum_cardinality = Column(Integer())
    range_expression_id = Column(Text(), ForeignKey('anonymous_class_expression.id'))
    range_expression = relationship("AnonymousClassExpression", uselist=False)
    has_member_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'))
    has_member = relationship("AnonymousSlotExpression", uselist=False)
    
    
    equals_string_in_rel = relationship( "SlotExpressionEqualsStringIn" )
    equals_string_in = association_proxy("equals_string_in_rel", "equals_string_in",
                                  creator=lambda x_: SlotExpressionEqualsStringIn(equals_string_in=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='slot_expression', source_slot='all_members', mapping_type=None, target_class='slot_definition', target_slot='slot_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    all_members = relationship( "SlotDefinition", foreign_keys="[slot_definition.slot_expression_id]")
    
    
    # ManyToMany
    none_of = relationship( "AnonymousSlotExpression", secondary="slot_expression_none_of")
    
    
    # ManyToMany
    exactly_one_of = relationship( "AnonymousSlotExpression", secondary="slot_expression_exactly_one_of")
    
    
    # ManyToMany
    any_of = relationship( "AnonymousSlotExpression", secondary="slot_expression_any_of")
    
    
    # ManyToMany
    all_of = relationship( "AnonymousSlotExpression", secondary="slot_expression_all_of")
    
    
    def __repr__(self):
        return f"slot_expression(id={self.id},range={self.range},required={self.required},recommended={self.recommended},minimum_value={self.minimum_value},maximum_value={self.maximum_value},pattern={self.pattern},equals_string={self.equals_string},equals_number={self.equals_number},equals_expression={self.equals_expression},minimum_cardinality={self.minimum_cardinality},maximum_cardinality={self.maximum_cardinality},range_expression_id={self.range_expression_id},has_member_id={self.has_member_id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class AnonymousSlotExpression(AnonymousExpression):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    range = Column(Text(), ForeignKey('element.name'))
    required = Column(Boolean())
    recommended = Column(Boolean())
    minimum_value = Column(Integer())
    maximum_value = Column(Integer())
    pattern = Column(Text())
    equals_string = Column(Text())
    equals_number = Column(Integer())
    equals_expression = Column(Text())
    minimum_cardinality = Column(Integer())
    maximum_cardinality = Column(Integer())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    range_expression_id = Column(Text(), ForeignKey('anonymous_class_expression.id'))
    range_expression = relationship("AnonymousClassExpression", uselist=False)
    has_member_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'))
    has_member = relationship("AnonymousSlotExpression", uselist=False)
    
    
    equals_string_in_rel = relationship( "AnonymousSlotExpressionEqualsStringIn" )
    equals_string_in = association_proxy("equals_string_in_rel", "equals_string_in",
                                  creator=lambda x_: AnonymousSlotExpressionEqualsStringIn(equals_string_in=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_slot_expression', source_slot='all_members', mapping_type=None, target_class='slot_definition', target_slot='anonymous_slot_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    all_members = relationship( "SlotDefinition", foreign_keys="[slot_definition.anonymous_slot_expression_id]")
    
    
    # ManyToMany
    none_of = relationship( "AnonymousSlotExpression", secondary="anonymous_slot_expression_none_of")
    
    
    # ManyToMany
    exactly_one_of = relationship( "AnonymousSlotExpression", secondary="anonymous_slot_expression_exactly_one_of")
    
    
    # ManyToMany
    any_of = relationship( "AnonymousSlotExpression", secondary="anonymous_slot_expression_any_of")
    
    
    # ManyToMany
    all_of = relationship( "AnonymousSlotExpression", secondary="anonymous_slot_expression_all_of")
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_slot_expression', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='anonymous_slot_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.anonymous_slot_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_slot_expression', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='anonymous_slot_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.anonymous_slot_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_slot_expression', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='anonymous_slot_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.anonymous_slot_expression_id]")
    
    
    todos_rel = relationship( "AnonymousSlotExpressionTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: AnonymousSlotExpressionTodos(todos=x_))
    
    
    notes_rel = relationship( "AnonymousSlotExpressionNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: AnonymousSlotExpressionNotes(notes=x_))
    
    
    comments_rel = relationship( "AnonymousSlotExpressionComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: AnonymousSlotExpressionComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_slot_expression', source_slot='examples', mapping_type=None, target_class='example', target_slot='anonymous_slot_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.anonymous_slot_expression_id]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="anonymous_slot_expression_in_subset")
    
    
    see_also_rel = relationship( "AnonymousSlotExpressionSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: AnonymousSlotExpressionSeeAlso(see_also=x_))
    
    
    def __repr__(self):
        return f"anonymous_slot_expression(id={self.id},range={self.range},required={self.required},recommended={self.recommended},minimum_value={self.minimum_value},maximum_value={self.maximum_value},pattern={self.pattern},equals_string={self.equals_string},equals_number={self.equals_number},equals_expression={self.equals_expression},minimum_cardinality={self.minimum_cardinality},maximum_cardinality={self.maximum_cardinality},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},range_expression_id={self.range_expression_id},has_member_id={self.has_member_id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class AnonymousClassExpression(AnonymousExpression):
    """
    
    """
    __tablename__ = 'anonymous_class_expression'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    is_a = Column(Text(), ForeignKey('definition.name'))
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'))
    
    
    # ManyToMany
    any_of = relationship( "AnonymousClassExpression", secondary="anonymous_class_expression_any_of")
    
    
    # ManyToMany
    exactly_one_of = relationship( "AnonymousClassExpression", secondary="anonymous_class_expression_exactly_one_of")
    
    
    # ManyToMany
    none_of = relationship( "AnonymousClassExpression", secondary="anonymous_class_expression_none_of")
    
    
    # ManyToMany
    all_of = relationship( "AnonymousClassExpression", secondary="anonymous_class_expression_all_of")
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_class_expression', source_slot='slot_conditions', mapping_type=None, target_class='slot_definition', target_slot='anonymous_class_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    slot_conditions = relationship( "SlotDefinition", foreign_keys="[slot_definition.anonymous_class_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_class_expression', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='anonymous_class_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.anonymous_class_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_class_expression', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='anonymous_class_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.anonymous_class_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_class_expression', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='anonymous_class_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.anonymous_class_expression_id]")
    
    
    todos_rel = relationship( "AnonymousClassExpressionTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: AnonymousClassExpressionTodos(todos=x_))
    
    
    notes_rel = relationship( "AnonymousClassExpressionNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: AnonymousClassExpressionNotes(notes=x_))
    
    
    comments_rel = relationship( "AnonymousClassExpressionComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: AnonymousClassExpressionComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_class_expression', source_slot='examples', mapping_type=None, target_class='example', target_slot='anonymous_class_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.anonymous_class_expression_id]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="anonymous_class_expression_in_subset")
    
    
    see_also_rel = relationship( "AnonymousClassExpressionSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: AnonymousClassExpressionSeeAlso(see_also=x_))
    
    
    def __repr__(self):
        return f"anonymous_class_expression(id={self.id},is_a={self.is_a},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},class_definition_name={self.class_definition_name},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class ClassRule(ClassLevelRule):
    """
    A rule that applies to instances of a class
    """
    __tablename__ = 'class_rule'
    
    id = Column(Integer(), primary_key=True, autoincrement=True )
    bidirectional = Column(Boolean())
    open_world = Column(Boolean())
    precedence = Column(Integer())
    deactivated = Column(Boolean())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'))
    preconditions_id = Column(Text(), ForeignKey('anonymous_class_expression.id'))
    preconditions = relationship("AnonymousClassExpression", uselist=False)
    postconditions_id = Column(Text(), ForeignKey('anonymous_class_expression.id'))
    postconditions = relationship("AnonymousClassExpression", uselist=False)
    elseconditions_id = Column(Text(), ForeignKey('anonymous_class_expression.id'))
    elseconditions = relationship("AnonymousClassExpression", uselist=False)
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_rule', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='class_rule_id', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.class_rule_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_rule', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='class_rule_id', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.class_rule_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_rule', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='class_rule_id', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.class_rule_id]")
    
    
    todos_rel = relationship( "ClassRuleTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: ClassRuleTodos(todos=x_))
    
    
    notes_rel = relationship( "ClassRuleNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: ClassRuleNotes(notes=x_))
    
    
    comments_rel = relationship( "ClassRuleComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: ClassRuleComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_rule', source_slot='examples', mapping_type=None, target_class='example', target_slot='class_rule_id', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.class_rule_id]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="class_rule_in_subset")
    
    
    see_also_rel = relationship( "ClassRuleSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: ClassRuleSeeAlso(see_also=x_))
    
    
    def __repr__(self):
        return f"class_rule(id={self.id},bidirectional={self.bidirectional},open_world={self.open_world},precedence={self.precedence},deactivated={self.deactivated},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},class_definition_name={self.class_definition_name},preconditions_id={self.preconditions_id},postconditions_id={self.postconditions_id},elseconditions_id={self.elseconditions_id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class Annotation(Extension):
    """
    a tag/value pair with the semantics of OWL Annotation
    """
    __tablename__ = 'annotation'
    
    tag = Column(Text(), primary_key=True)
    value = Column(Text(), primary_key=True)
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    anonymous_expression_id = Column(Text(), ForeignKey('anonymous_expression.id'), primary_key=True)
    anonymous_slot_expression_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    anonymous_class_expression_id = Column(Text(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    class_rule_id = Column(Text(), ForeignKey('class_rule.id'), primary_key=True)
    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    unique_key_id = Column(Text(), ForeignKey('unique_key.id'), primary_key=True)
    annotatable_id = Column(Text(), ForeignKey('annotatable.id'), primary_key=True)
    annotation_tag = Column(Text(), ForeignKey('annotation.tag'), primary_key=True)
    
    
    # One-To-Many: OneToAnyMapping(source_class='annotation', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='annotation_tag', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.annotation_tag]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='annotation', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='annotation_tag', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.annotation_tag]")
    
    
    def __repr__(self):
        return f"annotation(tag={self.tag},value={self.value},element_name={self.element_name},schema_definition_name={self.schema_definition_name},type_definition_name={self.type_definition_name},subset_definition_name={self.subset_definition_name},definition_name={self.definition_name},enum_definition_name={self.enum_definition_name},anonymous_expression_id={self.anonymous_expression_id},anonymous_slot_expression_id={self.anonymous_slot_expression_id},slot_definition_name={self.slot_definition_name},anonymous_class_expression_id={self.anonymous_class_expression_id},class_definition_name={self.class_definition_name},class_rule_id={self.class_rule_id},permissible_value_text={self.permissible_value_text},unique_key_id={self.unique_key_id},annotatable_id={self.annotatable_id},annotation_tag={self.annotation_tag},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class SlotDefinition(Definition):
    """
    the definition of a property or a slot
    """
    __tablename__ = 'slot_definition'
    
    singular_name = Column(Text())
    domain = Column(Text(), ForeignKey('class_definition.name'))
    slot_uri = Column(Text())
    multivalued = Column(Boolean())
    inherited = Column(Boolean())
    readonly = Column(Text())
    ifabsent = Column(Text())
    inlined = Column(Boolean())
    inlined_as_list = Column(Boolean())
    key = Column(Boolean())
    identifier = Column(Boolean())
    designates_type = Column(Boolean())
    alias = Column(Text())
    owner = Column(Text(), ForeignKey('definition.name'))
    subproperty_of = Column(Text(), ForeignKey('slot_definition.name'))
    symmetric = Column(Boolean())
    inverse = Column(Text(), ForeignKey('slot_definition.name'))
    is_class_field = Column(Boolean())
    role = Column(Text())
    is_usage_slot = Column(Boolean())
    usage_slot_name = Column(Text())
    range = Column(Text(), ForeignKey('element.name'))
    required = Column(Boolean())
    recommended = Column(Boolean())
    minimum_value = Column(Integer())
    maximum_value = Column(Integer())
    pattern = Column(Text())
    equals_string = Column(Text())
    equals_number = Column(Integer())
    equals_expression = Column(Text())
    minimum_cardinality = Column(Integer())
    maximum_cardinality = Column(Integer())
    is_a = Column(Text(), ForeignKey('slot_definition.name'))
    abstract = Column(Boolean())
    mixin = Column(Boolean())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    string_serialization = Column(Text())
    name = Column(Text(), primary_key=True)
    definition_uri = Column(Text())
    conforms_to = Column(Text())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'))
    slot_expression_id = Column(Text(), ForeignKey('slot_expression.id'))
    anonymous_slot_expression_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'))
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'))
    class_expression_id = Column(Text(), ForeignKey('class_expression.id'))
    anonymous_class_expression_id = Column(Text(), ForeignKey('anonymous_class_expression.id'))
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'))
    range_expression_id = Column(Text(), ForeignKey('anonymous_class_expression.id'))
    range_expression = relationship("AnonymousClassExpression", uselist=False)
    has_member_id = Column(Text(), ForeignKey('anonymous_slot_expression.id'))
    has_member = relationship("AnonymousSlotExpression", uselist=False)
    
    
    # ManyToMany
    domain_of = relationship( "ClassDefinition", secondary="slot_definition_domain_of")
    
    
    equals_string_in_rel = relationship( "SlotDefinitionEqualsStringIn" )
    equals_string_in = association_proxy("equals_string_in_rel", "equals_string_in",
                                  creator=lambda x_: SlotDefinitionEqualsStringIn(equals_string_in=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='slot_definition', source_slot='all_members', mapping_type=None, target_class='slot_definition', target_slot='slot_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    all_members = relationship( "SlotDefinition", foreign_keys="[slot_definition.slot_definition_name]")
    
    
    # ManyToMany
    none_of = relationship( "AnonymousSlotExpression", secondary="slot_definition_none_of")
    
    
    # ManyToMany
    exactly_one_of = relationship( "AnonymousSlotExpression", secondary="slot_definition_exactly_one_of")
    
    
    # ManyToMany
    any_of = relationship( "AnonymousSlotExpression", secondary="slot_definition_any_of")
    
    
    # ManyToMany
    all_of = relationship( "AnonymousSlotExpression", secondary="slot_definition_all_of")
    
    
    # ManyToMany
    mixins = relationship( "SlotDefinition", secondary="slot_definition_mixins")
    
    
    # ManyToMany
    apply_to = relationship( "SlotDefinition", secondary="slot_definition_apply_to")
    
    
    values_from_rel = relationship( "SlotDefinitionValuesFrom" )
    values_from = association_proxy("values_from_rel", "values_from",
                                  creator=lambda x_: SlotDefinitionValuesFrom(values_from=x_))
    
    
    id_prefixes_rel = relationship( "SlotDefinitionIdPrefixes" )
    id_prefixes = association_proxy("id_prefixes_rel", "id_prefixes",
                                  creator=lambda x_: SlotDefinitionIdPrefixes(id_prefixes=x_))
    
    
    aliases_rel = relationship( "SlotDefinitionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: SlotDefinitionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='slot_definition', source_slot='local_names', mapping_type=None, target_class='local_name', target_slot='slot_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    local_names = relationship( "LocalName", foreign_keys="[local_name.slot_definition_name]")
    
    
    mappings_rel = relationship( "SlotDefinitionMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: SlotDefinitionMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "SlotDefinitionExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: SlotDefinitionExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "SlotDefinitionCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: SlotDefinitionCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "SlotDefinitionRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: SlotDefinitionRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "SlotDefinitionNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: SlotDefinitionNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "SlotDefinitionBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: SlotDefinitionBroadMappings(broad_mappings=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='slot_definition', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='slot_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.slot_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='slot_definition', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='slot_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.slot_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='slot_definition', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='slot_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.slot_definition_name]")
    
    
    todos_rel = relationship( "SlotDefinitionTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: SlotDefinitionTodos(todos=x_))
    
    
    notes_rel = relationship( "SlotDefinitionNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: SlotDefinitionNotes(notes=x_))
    
    
    comments_rel = relationship( "SlotDefinitionComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: SlotDefinitionComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='slot_definition', source_slot='examples', mapping_type=None, target_class='example', target_slot='slot_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.slot_definition_name]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="slot_definition_in_subset")
    
    
    see_also_rel = relationship( "SlotDefinitionSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: SlotDefinitionSeeAlso(see_also=x_))
    
    
    def __repr__(self):
        return f"slot_definition(singular_name={self.singular_name},domain={self.domain},slot_uri={self.slot_uri},multivalued={self.multivalued},inherited={self.inherited},readonly={self.readonly},ifabsent={self.ifabsent},inlined={self.inlined},inlined_as_list={self.inlined_as_list},key={self.key},identifier={self.identifier},designates_type={self.designates_type},alias={self.alias},owner={self.owner},subproperty_of={self.subproperty_of},symmetric={self.symmetric},inverse={self.inverse},is_class_field={self.is_class_field},role={self.role},is_usage_slot={self.is_usage_slot},usage_slot_name={self.usage_slot_name},range={self.range},required={self.required},recommended={self.recommended},minimum_value={self.minimum_value},maximum_value={self.maximum_value},pattern={self.pattern},equals_string={self.equals_string},equals_number={self.equals_number},equals_expression={self.equals_expression},minimum_cardinality={self.minimum_cardinality},maximum_cardinality={self.maximum_cardinality},is_a={self.is_a},abstract={self.abstract},mixin={self.mixin},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},string_serialization={self.string_serialization},name={self.name},definition_uri={self.definition_uri},conforms_to={self.conforms_to},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},schema_definition_name={self.schema_definition_name},slot_expression_id={self.slot_expression_id},anonymous_slot_expression_id={self.anonymous_slot_expression_id},slot_definition_name={self.slot_definition_name},class_expression_id={self.class_expression_id},anonymous_class_expression_id={self.anonymous_class_expression_id},class_definition_name={self.class_definition_name},range_expression_id={self.range_expression_id},has_member_id={self.has_member_id},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class ClassDefinition(Definition):
    """
    the definition of a class or interface
    """
    __tablename__ = 'class_definition'
    
    class_uri = Column(Text())
    subclass_of = Column(Text())
    tree_root = Column(Boolean())
    is_a = Column(Text(), ForeignKey('class_definition.name'))
    abstract = Column(Boolean())
    mixin = Column(Boolean())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    string_serialization = Column(Text())
    name = Column(Text(), primary_key=True)
    definition_uri = Column(Text())
    conforms_to = Column(Text())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'))
    
    
    # ManyToMany
    slots = relationship( "SlotDefinition", secondary="class_definition_slots")
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_definition', source_slot='slot_usage', mapping_type=None, target_class='slot_definition', target_slot='class_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    slot_usage = relationship( "SlotDefinition", foreign_keys="[slot_definition.class_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_definition', source_slot='attributes', mapping_type=None, target_class='slot_definition', target_slot='class_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    attributes = relationship( "SlotDefinition", foreign_keys="[slot_definition.class_definition_name]")
    
    
    # ManyToMany
    union_of = relationship( "ClassDefinition", secondary="class_definition_union_of")
    
    
    # ManyToMany
    defining_slots = relationship( "SlotDefinition", secondary="class_definition_defining_slots")
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_definition', source_slot='unique_keys', mapping_type=None, target_class='unique_key', target_slot='class_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    unique_keys = relationship( "UniqueKey", foreign_keys="[unique_key.class_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_definition', source_slot='rules', mapping_type=None, target_class='class_rule', target_slot='class_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    rules = relationship( "ClassRule", foreign_keys="[class_rule.class_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_definition', source_slot='classification_rules', mapping_type=None, target_class='anonymous_class_expression', target_slot='class_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    classification_rules = relationship( "AnonymousClassExpression", foreign_keys="[anonymous_class_expression.class_definition_name]")
    
    
    # ManyToMany
    any_of = relationship( "AnonymousClassExpression", secondary="class_definition_any_of")
    
    
    # ManyToMany
    exactly_one_of = relationship( "AnonymousClassExpression", secondary="class_definition_exactly_one_of")
    
    
    # ManyToMany
    none_of = relationship( "AnonymousClassExpression", secondary="class_definition_none_of")
    
    
    # ManyToMany
    all_of = relationship( "AnonymousClassExpression", secondary="class_definition_all_of")
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_definition', source_slot='slot_conditions', mapping_type=None, target_class='slot_definition', target_slot='class_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    slot_conditions = relationship( "SlotDefinition", foreign_keys="[slot_definition.class_definition_name]")
    
    
    # ManyToMany
    mixins = relationship( "ClassDefinition", secondary="class_definition_mixins")
    
    
    # ManyToMany
    apply_to = relationship( "ClassDefinition", secondary="class_definition_apply_to")
    
    
    values_from_rel = relationship( "ClassDefinitionValuesFrom" )
    values_from = association_proxy("values_from_rel", "values_from",
                                  creator=lambda x_: ClassDefinitionValuesFrom(values_from=x_))
    
    
    id_prefixes_rel = relationship( "ClassDefinitionIdPrefixes" )
    id_prefixes = association_proxy("id_prefixes_rel", "id_prefixes",
                                  creator=lambda x_: ClassDefinitionIdPrefixes(id_prefixes=x_))
    
    
    aliases_rel = relationship( "ClassDefinitionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: ClassDefinitionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_definition', source_slot='local_names', mapping_type=None, target_class='local_name', target_slot='class_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    local_names = relationship( "LocalName", foreign_keys="[local_name.class_definition_name]")
    
    
    mappings_rel = relationship( "ClassDefinitionMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: ClassDefinitionMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "ClassDefinitionExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: ClassDefinitionExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "ClassDefinitionCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: ClassDefinitionCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "ClassDefinitionRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: ClassDefinitionRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "ClassDefinitionNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: ClassDefinitionNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "ClassDefinitionBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: ClassDefinitionBroadMappings(broad_mappings=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_definition', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='class_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.class_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_definition', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='class_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.class_definition_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_definition', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='class_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.class_definition_name]")
    
    
    todos_rel = relationship( "ClassDefinitionTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: ClassDefinitionTodos(todos=x_))
    
    
    notes_rel = relationship( "ClassDefinitionNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: ClassDefinitionNotes(notes=x_))
    
    
    comments_rel = relationship( "ClassDefinitionComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: ClassDefinitionComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_definition', source_slot='examples', mapping_type=None, target_class='example', target_slot='class_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.class_definition_name]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="class_definition_in_subset")
    
    
    see_also_rel = relationship( "ClassDefinitionSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: ClassDefinitionSeeAlso(see_also=x_))
    
    
    def __repr__(self):
        return f"class_definition(class_uri={self.class_uri},subclass_of={self.subclass_of},tree_root={self.tree_root},is_a={self.is_a},abstract={self.abstract},mixin={self.mixin},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},string_serialization={self.string_serialization},name={self.name},definition_uri={self.definition_uri},conforms_to={self.conforms_to},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},schema_definition_name={self.schema_definition_name},)"
        
    
        
    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    

