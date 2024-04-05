
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()
metadata = Base.metadata


class Anything(Base):
    """
    
    """
    __tablename__ = 'Anything'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    

    def __repr__(self):
        return f"Anything(id={self.id},)"



    


class CommonMetadata(Base):
    """
    Generic metadata shared across definitions
    """
    __tablename__ = 'common_metadata'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
    
    
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
    
    
    aliases_rel = relationship( "CommonMetadataAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: CommonMetadataAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='common_metadata', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='common_metadata_id', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.common_metadata_id]")
    
    
    mappings_rel = relationship( "CommonMetadataMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: CommonMetadataMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "CommonMetadataExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: CommonMetadataExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "CommonMetadataCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: CommonMetadataCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "CommonMetadataRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: CommonMetadataRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "CommonMetadataNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: CommonMetadataNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "CommonMetadataBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: CommonMetadataBroadMappings(broad_mappings=x_))
    
    
    contributors_rel = relationship( "CommonMetadataContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: CommonMetadataContributors(contributors=x_))
    
    
    categories_rel = relationship( "CommonMetadataCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: CommonMetadataCategory(category=x_))
    
    
    keywords_rel = relationship( "CommonMetadataKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: CommonMetadataKeyword(keyword=x_))
    

    def __repr__(self):
        return f"common_metadata(id={self.id},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},)"



    


class Element(Base):
    """
    A named element in the model
    """
    __tablename__ = 'element'

    name = Column(Text(), primary_key=True, nullable=False )
    id_prefixes_are_closed = Column(Boolean())
    definition_uri = Column(Text())
    conforms_to = Column(Text())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
    
    
    id_prefixes_rel = relationship( "ElementIdPrefixes" )
    id_prefixes = association_proxy("id_prefixes_rel", "id_prefixes",
                                  creator=lambda x_: ElementIdPrefixes(id_prefixes=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='element', source_slot='local_names', mapping_type=None, target_class='local_name', target_slot='element_name', join_class=None, uses_join_table=None, multivalued=False)
    local_names = relationship( "LocalName", foreign_keys="[local_name.element_name]")
    
    
    implements_rel = relationship( "ElementImplements" )
    implements = association_proxy("implements_rel", "implements",
                                  creator=lambda x_: ElementImplements(implements=x_))
    
    
    instantiates_rel = relationship( "ElementInstantiates" )
    instantiates = association_proxy("instantiates_rel", "instantiates",
                                  creator=lambda x_: ElementInstantiates(instantiates=x_))
    
    
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
    
    
    aliases_rel = relationship( "ElementAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: ElementAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='element', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='element_name', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.element_name]")
    
    
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
    
    
    contributors_rel = relationship( "ElementContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: ElementContributors(contributors=x_))
    
    
    categories_rel = relationship( "ElementCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: ElementCategory(category=x_))
    
    
    keywords_rel = relationship( "ElementKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: ElementKeyword(keyword=x_))
    

    def __repr__(self):
        return f"element(name={self.name},id_prefixes_are_closed={self.id_prefixes_are_closed},definition_uri={self.definition_uri},conforms_to={self.conforms_to},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},)"



    


class AnonymousTypeExpression(Base):
    """
    A type expression that is not a top-level named type definition. Used for nesting.
    """
    __tablename__ = 'anonymous_type_expression'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    pattern = Column(Text())
    implicit_prefix = Column(Text())
    equals_string = Column(Text())
    equals_number = Column(Integer())
    structured_pattern_id = Column(Integer(), ForeignKey('pattern_expression.id'))
    structured_pattern = relationship("PatternExpression", uselist=False, foreign_keys=[structured_pattern_id])
    unit_id = Column(Integer(), ForeignKey('UnitOfMeasure.id'))
    unit = relationship("UnitOfMeasure", uselist=False, foreign_keys=[unit_id])
    minimum_value_id = Column(Integer(), ForeignKey('Anything.id'))
    minimum_value = relationship("Anything", uselist=False, foreign_keys=[minimum_value_id])
    maximum_value_id = Column(Integer(), ForeignKey('Anything.id'))
    maximum_value = relationship("Anything", uselist=False, foreign_keys=[maximum_value_id])
    
    
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
        return f"anonymous_type_expression(id={self.id},pattern={self.pattern},implicit_prefix={self.implicit_prefix},equals_string={self.equals_string},equals_number={self.equals_number},structured_pattern_id={self.structured_pattern_id},unit_id={self.unit_id},minimum_value_id={self.minimum_value_id},maximum_value_id={self.maximum_value_id},)"



    


class AnonymousEnumExpression(Base):
    """
    An enum_expression that is not named
    """
    __tablename__ = 'anonymous_enum_expression'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    code_set = Column(Text())
    code_set_tag = Column(Text())
    code_set_version = Column(Text())
    pv_formula = Column(Enum('CODE', 'CURIE', 'URI', 'FHIR_CODING', 'LABEL', name='pv_formula_options'))
    reachable_from_id = Column(Integer(), ForeignKey('reachability_query.id'))
    reachable_from = relationship("ReachabilityQuery", uselist=False, foreign_keys=[reachable_from_id])
    matches_id = Column(Integer(), ForeignKey('match_query.id'))
    matches = relationship("MatchQuery", uselist=False, foreign_keys=[matches_id])
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_enum_expression', source_slot='permissible_values', mapping_type=None, target_class='permissible_value', target_slot='anonymous_enum_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    permissible_values = relationship( "PermissibleValue", foreign_keys="[permissible_value.anonymous_enum_expression_id]")
    
    
    # ManyToMany
    include = relationship( "AnonymousEnumExpression", secondary="anonymous_enum_expression_include")
    
    
    # ManyToMany
    minus = relationship( "AnonymousEnumExpression", secondary="anonymous_enum_expression_minus")
    
    
    # ManyToMany
    inherits = relationship( "EnumDefinition", secondary="anonymous_enum_expression_inherits")
    
    
    concepts_rel = relationship( "AnonymousEnumExpressionConcepts" )
    concepts = association_proxy("concepts_rel", "concepts",
                                  creator=lambda x_: AnonymousEnumExpressionConcepts(concepts=x_))
    

    def __repr__(self):
        return f"anonymous_enum_expression(id={self.id},code_set={self.code_set},code_set_tag={self.code_set_tag},code_set_version={self.code_set_version},pv_formula={self.pv_formula},reachable_from_id={self.reachable_from_id},matches_id={self.matches_id},)"



    


class MatchQuery(Base):
    """
    A query that is used on an enum expression to dynamically obtain a set of permissivle values via a query that  matches on properties of the external concepts.
    """
    __tablename__ = 'match_query'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    identifier_pattern = Column(Text())
    source_ontology = Column(Text())
    

    def __repr__(self):
        return f"match_query(id={self.id},identifier_pattern={self.identifier_pattern},source_ontology={self.source_ontology},)"



    


class ReachabilityQuery(Base):
    """
    A query that is used on an enum expression to dynamically obtain a set of permissible values via walking from a  set of source nodes to a set of descendants or ancestors over a set of relationship types.
    """
    __tablename__ = 'reachability_query'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    source_ontology = Column(Text())
    is_direct = Column(Boolean())
    include_self = Column(Boolean())
    traverse_up = Column(Boolean())
    
    
    source_nodes_rel = relationship( "ReachabilityQuerySourceNodes" )
    source_nodes = association_proxy("source_nodes_rel", "source_nodes",
                                  creator=lambda x_: ReachabilityQuerySourceNodes(source_nodes=x_))
    
    
    relationship_types_rel = relationship( "ReachabilityQueryRelationshipTypes" )
    relationship_types = association_proxy("relationship_types_rel", "relationship_types",
                                  creator=lambda x_: ReachabilityQueryRelationshipTypes(relationship_types=x_))
    

    def __repr__(self):
        return f"reachability_query(id={self.id},source_ontology={self.source_ontology},is_direct={self.is_direct},include_self={self.include_self},traverse_up={self.traverse_up},)"



    


class StructuredAlias(Base):
    """
    object that contains meta data about a synonym or alias including where it came from (source) and its scope (narrow, broad, etc.)
    """
    __tablename__ = 'structured_alias'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    literal_form = Column(Text(), nullable=False )
    predicate = Column(Enum('EXACT_SYNONYM', 'RELATED_SYNONYM', 'BROAD_SYNONYM', 'NARROW_SYNONYM', name='alias_predicate_enum'))
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'))
    element_name = Column(Text(), ForeignKey('element.name'))
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'))
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'))
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'))
    definition_name = Column(Text(), ForeignKey('definition.name'))
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'))
    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'))
    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'))
    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'))
    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'))
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'))
    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'))
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'))
    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'))
    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'))
    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'))
    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'))
    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'))
    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'))
    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'))
    
    
    categories_rel = relationship( "StructuredAliasCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: StructuredAliasCategory(category=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='structured_alias', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='structured_alias_id', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.structured_alias_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='structured_alias', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='structured_alias_id', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.structured_alias_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='structured_alias', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='structured_alias_id', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.structured_alias_id]")
    
    
    todos_rel = relationship( "StructuredAliasTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: StructuredAliasTodos(todos=x_))
    
    
    notes_rel = relationship( "StructuredAliasNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: StructuredAliasNotes(notes=x_))
    
    
    comments_rel = relationship( "StructuredAliasComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: StructuredAliasComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='structured_alias', source_slot='examples', mapping_type=None, target_class='example', target_slot='structured_alias_id', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.structured_alias_id]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="structured_alias_in_subset")
    
    
    see_also_rel = relationship( "StructuredAliasSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: StructuredAliasSeeAlso(see_also=x_))
    
    
    aliases_rel = relationship( "StructuredAliasAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: StructuredAliasAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='structured_alias', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='structured_alias_id', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.structured_alias_id]")
    
    
    mappings_rel = relationship( "StructuredAliasMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: StructuredAliasMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "StructuredAliasExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: StructuredAliasExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "StructuredAliasCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: StructuredAliasCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "StructuredAliasRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: StructuredAliasRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "StructuredAliasNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: StructuredAliasNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "StructuredAliasBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: StructuredAliasBroadMappings(broad_mappings=x_))
    
    
    contributors_rel = relationship( "StructuredAliasContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: StructuredAliasContributors(contributors=x_))
    
    
    keywords_rel = relationship( "StructuredAliasKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: StructuredAliasKeyword(keyword=x_))
    

    def __repr__(self):
        return f"structured_alias(id={self.id},literal_form={self.literal_form},predicate={self.predicate},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},common_metadata_id={self.common_metadata_id},element_name={self.element_name},schema_definition_name={self.schema_definition_name},type_definition_name={self.type_definition_name},subset_definition_name={self.subset_definition_name},definition_name={self.definition_name},enum_definition_name={self.enum_definition_name},structured_alias_id={self.structured_alias_id},anonymous_expression_id={self.anonymous_expression_id},path_expression_id={self.path_expression_id},anonymous_slot_expression_id={self.anonymous_slot_expression_id},slot_definition_name={self.slot_definition_name},anonymous_class_expression_id={self.anonymous_class_expression_id},class_definition_name={self.class_definition_name},class_rule_id={self.class_rule_id},array_expression_id={self.array_expression_id},dimension_expression_id={self.dimension_expression_id},pattern_expression_id={self.pattern_expression_id},import_expression_id={self.import_expression_id},permissible_value_text={self.permissible_value_text},unique_key_unique_key_name={self.unique_key_unique_key_name},)"



    


class Expression(Base):
    """
    general mixin for any class that can represent some form of expression
    """
    __tablename__ = 'expression'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    

    def __repr__(self):
        return f"expression(id={self.id},)"



    


class AnonymousExpression(Base):
    """
    An abstract parent class for any nested expression
    """
    __tablename__ = 'anonymous_expression'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
    
    
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
    
    
    aliases_rel = relationship( "AnonymousExpressionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: AnonymousExpressionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_expression', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='anonymous_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.anonymous_expression_id]")
    
    
    mappings_rel = relationship( "AnonymousExpressionMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: AnonymousExpressionMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "AnonymousExpressionExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: AnonymousExpressionExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "AnonymousExpressionCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: AnonymousExpressionCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "AnonymousExpressionRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: AnonymousExpressionRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "AnonymousExpressionNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: AnonymousExpressionNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "AnonymousExpressionBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: AnonymousExpressionBroadMappings(broad_mappings=x_))
    
    
    contributors_rel = relationship( "AnonymousExpressionContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: AnonymousExpressionContributors(contributors=x_))
    
    
    categories_rel = relationship( "AnonymousExpressionCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: AnonymousExpressionCategory(category=x_))
    
    
    keywords_rel = relationship( "AnonymousExpressionKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: AnonymousExpressionKeyword(keyword=x_))
    

    def __repr__(self):
        return f"anonymous_expression(id={self.id},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},)"



    


class PathExpression(Base):
    """
    An expression that describes an abstract path from an object to another through a sequence of slot lookups
    """
    __tablename__ = 'path_expression'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    reversed = Column(Boolean())
    traverse = Column(Text(), ForeignKey('slot_definition.name'))
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
    followed_by_id = Column(Integer(), ForeignKey('path_expression.id'))
    followed_by = relationship("PathExpression", uselist=False, foreign_keys=[followed_by_id])
    range_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'))
    range_expression = relationship("AnonymousClassExpression", uselist=False, foreign_keys=[range_expression_id])
    
    
    # ManyToMany
    none_of = relationship( "PathExpression", secondary="path_expression_none_of")
    
    
    # ManyToMany
    any_of = relationship( "PathExpression", secondary="path_expression_any_of")
    
    
    # ManyToMany
    all_of = relationship( "PathExpression", secondary="path_expression_all_of")
    
    
    # ManyToMany
    exactly_one_of = relationship( "PathExpression", secondary="path_expression_exactly_one_of")
    
    
    # One-To-Many: OneToAnyMapping(source_class='path_expression', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='path_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.path_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='path_expression', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='path_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.path_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='path_expression', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='path_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.path_expression_id]")
    
    
    todos_rel = relationship( "PathExpressionTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: PathExpressionTodos(todos=x_))
    
    
    notes_rel = relationship( "PathExpressionNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: PathExpressionNotes(notes=x_))
    
    
    comments_rel = relationship( "PathExpressionComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: PathExpressionComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='path_expression', source_slot='examples', mapping_type=None, target_class='example', target_slot='path_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.path_expression_id]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="path_expression_in_subset")
    
    
    see_also_rel = relationship( "PathExpressionSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: PathExpressionSeeAlso(see_also=x_))
    
    
    aliases_rel = relationship( "PathExpressionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: PathExpressionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='path_expression', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='path_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.path_expression_id]")
    
    
    mappings_rel = relationship( "PathExpressionMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: PathExpressionMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "PathExpressionExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: PathExpressionExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "PathExpressionCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: PathExpressionCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "PathExpressionRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: PathExpressionRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "PathExpressionNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: PathExpressionNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "PathExpressionBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: PathExpressionBroadMappings(broad_mappings=x_))
    
    
    contributors_rel = relationship( "PathExpressionContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: PathExpressionContributors(contributors=x_))
    
    
    categories_rel = relationship( "PathExpressionCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: PathExpressionCategory(category=x_))
    
    
    keywords_rel = relationship( "PathExpressionKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: PathExpressionKeyword(keyword=x_))
    

    def __repr__(self):
        return f"path_expression(id={self.id},reversed={self.reversed},traverse={self.traverse},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},followed_by_id={self.followed_by_id},range_expression_id={self.range_expression_id},)"



    


class ClassExpression(Base):
    """
    A boolean expression that can be used to dynamically determine membership of a class
    """
    __tablename__ = 'class_expression'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    
    
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

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    

    def __repr__(self):
        return f"class_level_rule(id={self.id},)"



    


class ArrayExpression(Base):
    """
    defines the dimensions of an array
    """
    __tablename__ = 'array_expression'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    exact_number_dimensions = Column(Integer())
    minimum_number_dimensions = Column(Integer())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
    maximum_number_dimensions_id = Column(Integer(), ForeignKey('Anything.id'))
    maximum_number_dimensions = relationship("Anything", uselist=False, foreign_keys=[maximum_number_dimensions_id])
    
    
    # ManyToMany
    dimensions = relationship( "DimensionExpression", secondary="array_expression_dimensions")
    
    
    # One-To-Many: OneToAnyMapping(source_class='array_expression', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='array_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.array_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='array_expression', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='array_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.array_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='array_expression', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='array_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.array_expression_id]")
    
    
    todos_rel = relationship( "ArrayExpressionTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: ArrayExpressionTodos(todos=x_))
    
    
    notes_rel = relationship( "ArrayExpressionNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: ArrayExpressionNotes(notes=x_))
    
    
    comments_rel = relationship( "ArrayExpressionComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: ArrayExpressionComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='array_expression', source_slot='examples', mapping_type=None, target_class='example', target_slot='array_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.array_expression_id]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="array_expression_in_subset")
    
    
    see_also_rel = relationship( "ArrayExpressionSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: ArrayExpressionSeeAlso(see_also=x_))
    
    
    aliases_rel = relationship( "ArrayExpressionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: ArrayExpressionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='array_expression', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='array_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.array_expression_id]")
    
    
    mappings_rel = relationship( "ArrayExpressionMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: ArrayExpressionMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "ArrayExpressionExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: ArrayExpressionExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "ArrayExpressionCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: ArrayExpressionCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "ArrayExpressionRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: ArrayExpressionRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "ArrayExpressionNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: ArrayExpressionNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "ArrayExpressionBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: ArrayExpressionBroadMappings(broad_mappings=x_))
    
    
    contributors_rel = relationship( "ArrayExpressionContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: ArrayExpressionContributors(contributors=x_))
    
    
    categories_rel = relationship( "ArrayExpressionCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: ArrayExpressionCategory(category=x_))
    
    
    keywords_rel = relationship( "ArrayExpressionKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: ArrayExpressionKeyword(keyword=x_))
    

    def __repr__(self):
        return f"array_expression(id={self.id},exact_number_dimensions={self.exact_number_dimensions},minimum_number_dimensions={self.minimum_number_dimensions},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},maximum_number_dimensions_id={self.maximum_number_dimensions_id},)"



    


class DimensionExpression(Base):
    """
    defines one of the dimensions of an array
    """
    __tablename__ = 'dimension_expression'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    alias = Column(Text())
    maximum_cardinality = Column(Integer())
    minimum_cardinality = Column(Integer())
    exact_cardinality = Column(Integer())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
    
    
    # One-To-Many: OneToAnyMapping(source_class='dimension_expression', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='dimension_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.dimension_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='dimension_expression', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='dimension_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.dimension_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='dimension_expression', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='dimension_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.dimension_expression_id]")
    
    
    todos_rel = relationship( "DimensionExpressionTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: DimensionExpressionTodos(todos=x_))
    
    
    notes_rel = relationship( "DimensionExpressionNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: DimensionExpressionNotes(notes=x_))
    
    
    comments_rel = relationship( "DimensionExpressionComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: DimensionExpressionComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='dimension_expression', source_slot='examples', mapping_type=None, target_class='example', target_slot='dimension_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.dimension_expression_id]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="dimension_expression_in_subset")
    
    
    see_also_rel = relationship( "DimensionExpressionSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: DimensionExpressionSeeAlso(see_also=x_))
    
    
    aliases_rel = relationship( "DimensionExpressionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: DimensionExpressionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='dimension_expression', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='dimension_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.dimension_expression_id]")
    
    
    mappings_rel = relationship( "DimensionExpressionMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: DimensionExpressionMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "DimensionExpressionExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: DimensionExpressionExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "DimensionExpressionCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: DimensionExpressionCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "DimensionExpressionRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: DimensionExpressionRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "DimensionExpressionNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: DimensionExpressionNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "DimensionExpressionBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: DimensionExpressionBroadMappings(broad_mappings=x_))
    
    
    contributors_rel = relationship( "DimensionExpressionContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: DimensionExpressionContributors(contributors=x_))
    
    
    categories_rel = relationship( "DimensionExpressionCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: DimensionExpressionCategory(category=x_))
    
    
    keywords_rel = relationship( "DimensionExpressionKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: DimensionExpressionKeyword(keyword=x_))
    

    def __repr__(self):
        return f"dimension_expression(id={self.id},alias={self.alias},maximum_cardinality={self.maximum_cardinality},minimum_cardinality={self.minimum_cardinality},exact_cardinality={self.exact_cardinality},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},)"



    


class PatternExpression(Base):
    """
    a regular expression pattern used to evaluate conformance of a string
    """
    __tablename__ = 'pattern_expression'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    syntax = Column(Text())
    interpolated = Column(Boolean())
    partial_match = Column(Boolean())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
    
    
    # One-To-Many: OneToAnyMapping(source_class='pattern_expression', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='pattern_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.pattern_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='pattern_expression', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='pattern_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.pattern_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='pattern_expression', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='pattern_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.pattern_expression_id]")
    
    
    todos_rel = relationship( "PatternExpressionTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: PatternExpressionTodos(todos=x_))
    
    
    notes_rel = relationship( "PatternExpressionNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: PatternExpressionNotes(notes=x_))
    
    
    comments_rel = relationship( "PatternExpressionComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: PatternExpressionComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='pattern_expression', source_slot='examples', mapping_type=None, target_class='example', target_slot='pattern_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.pattern_expression_id]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="pattern_expression_in_subset")
    
    
    see_also_rel = relationship( "PatternExpressionSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: PatternExpressionSeeAlso(see_also=x_))
    
    
    aliases_rel = relationship( "PatternExpressionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: PatternExpressionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='pattern_expression', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='pattern_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.pattern_expression_id]")
    
    
    mappings_rel = relationship( "PatternExpressionMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: PatternExpressionMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "PatternExpressionExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: PatternExpressionExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "PatternExpressionCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: PatternExpressionCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "PatternExpressionRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: PatternExpressionRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "PatternExpressionNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: PatternExpressionNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "PatternExpressionBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: PatternExpressionBroadMappings(broad_mappings=x_))
    
    
    contributors_rel = relationship( "PatternExpressionContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: PatternExpressionContributors(contributors=x_))
    
    
    categories_rel = relationship( "PatternExpressionCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: PatternExpressionCategory(category=x_))
    
    
    keywords_rel = relationship( "PatternExpressionKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: PatternExpressionKeyword(keyword=x_))
    

    def __repr__(self):
        return f"pattern_expression(id={self.id},syntax={self.syntax},interpolated={self.interpolated},partial_match={self.partial_match},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},)"



    


class ImportExpression(Base):
    """
    an expression describing an import
    """
    __tablename__ = 'import_expression'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    import_from = Column(Text(), nullable=False )
    import_as = Column(Text())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
    
    
    # One-To-Many: OneToAnyMapping(source_class='import_expression', source_slot='import_map', mapping_type=None, target_class='setting', target_slot='import_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    import_map = relationship( "Setting", foreign_keys="[setting.import_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='import_expression', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='import_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.import_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='import_expression', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='import_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.import_expression_id]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='import_expression', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='import_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.import_expression_id]")
    
    
    todos_rel = relationship( "ImportExpressionTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: ImportExpressionTodos(todos=x_))
    
    
    notes_rel = relationship( "ImportExpressionNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: ImportExpressionNotes(notes=x_))
    
    
    comments_rel = relationship( "ImportExpressionComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: ImportExpressionComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='import_expression', source_slot='examples', mapping_type=None, target_class='example', target_slot='import_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.import_expression_id]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="import_expression_in_subset")
    
    
    see_also_rel = relationship( "ImportExpressionSeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: ImportExpressionSeeAlso(see_also=x_))
    
    
    aliases_rel = relationship( "ImportExpressionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: ImportExpressionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='import_expression', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='import_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.import_expression_id]")
    
    
    mappings_rel = relationship( "ImportExpressionMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: ImportExpressionMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "ImportExpressionExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: ImportExpressionExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "ImportExpressionCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: ImportExpressionCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "ImportExpressionRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: ImportExpressionRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "ImportExpressionNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: ImportExpressionNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "ImportExpressionBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: ImportExpressionBroadMappings(broad_mappings=x_))
    
    
    contributors_rel = relationship( "ImportExpressionContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: ImportExpressionContributors(contributors=x_))
    
    
    categories_rel = relationship( "ImportExpressionCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: ImportExpressionCategory(category=x_))
    
    
    keywords_rel = relationship( "ImportExpressionKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: ImportExpressionKeyword(keyword=x_))
    

    def __repr__(self):
        return f"import_expression(id={self.id},import_from={self.import_from},import_as={self.import_as},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},)"



    


class Setting(Base):
    """
    assignment of a key to a value
    """
    __tablename__ = 'setting'

    setting_key = Column(Text(), primary_key=True, nullable=False )
    setting_value = Column(Text(), primary_key=True, nullable=False )
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"setting(setting_key={self.setting_key},setting_value={self.setting_value},schema_definition_name={self.schema_definition_name},import_expression_id={self.import_expression_id},)"



    


class Prefix(Base):
    """
    prefix URI tuple
    """
    __tablename__ = 'prefix'

    prefix_prefix = Column(Text(), primary_key=True, nullable=False )
    prefix_reference = Column(Text(), primary_key=True, nullable=False )
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"prefix(prefix_prefix={self.prefix_prefix},prefix_reference={self.prefix_reference},schema_definition_name={self.schema_definition_name},)"



    


class LocalName(Base):
    """
    an attributed label
    """
    __tablename__ = 'local_name'

    local_name_source = Column(Text(), primary_key=True, nullable=False )
    local_name_value = Column(Text(), primary_key=True, nullable=False )
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

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    value = Column(Text())
    description = Column(Text())
    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'))
    element_name = Column(Text(), ForeignKey('element.name'))
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'))
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'))
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'))
    definition_name = Column(Text(), ForeignKey('definition.name'))
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'))
    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'))
    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'))
    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'))
    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'))
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'))
    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'))
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'))
    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'))
    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'))
    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'))
    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'))
    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'))
    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'))
    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'))
    object_id = Column(Integer(), ForeignKey('Anything.id'))
    object = relationship("Anything", uselist=False, foreign_keys=[object_id])
    

    def __repr__(self):
        return f"example(id={self.id},value={self.value},description={self.description},common_metadata_id={self.common_metadata_id},element_name={self.element_name},schema_definition_name={self.schema_definition_name},type_definition_name={self.type_definition_name},subset_definition_name={self.subset_definition_name},definition_name={self.definition_name},enum_definition_name={self.enum_definition_name},structured_alias_id={self.structured_alias_id},anonymous_expression_id={self.anonymous_expression_id},path_expression_id={self.path_expression_id},anonymous_slot_expression_id={self.anonymous_slot_expression_id},slot_definition_name={self.slot_definition_name},anonymous_class_expression_id={self.anonymous_class_expression_id},class_definition_name={self.class_definition_name},class_rule_id={self.class_rule_id},array_expression_id={self.array_expression_id},dimension_expression_id={self.dimension_expression_id},pattern_expression_id={self.pattern_expression_id},import_expression_id={self.import_expression_id},permissible_value_text={self.permissible_value_text},unique_key_unique_key_name={self.unique_key_unique_key_name},object_id={self.object_id},)"



    


class AltDescription(Base):
    """
    an attributed description
    """
    __tablename__ = 'alt_description'

    source = Column(Text(), primary_key=True, nullable=False )
    description = Column(Text(), primary_key=True, nullable=False )
    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'), primary_key=True)
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    

    def __repr__(self):
        return f"alt_description(source={self.source},description={self.description},common_metadata_id={self.common_metadata_id},element_name={self.element_name},schema_definition_name={self.schema_definition_name},type_definition_name={self.type_definition_name},subset_definition_name={self.subset_definition_name},definition_name={self.definition_name},enum_definition_name={self.enum_definition_name},structured_alias_id={self.structured_alias_id},anonymous_expression_id={self.anonymous_expression_id},path_expression_id={self.path_expression_id},anonymous_slot_expression_id={self.anonymous_slot_expression_id},slot_definition_name={self.slot_definition_name},anonymous_class_expression_id={self.anonymous_class_expression_id},class_definition_name={self.class_definition_name},class_rule_id={self.class_rule_id},array_expression_id={self.array_expression_id},dimension_expression_id={self.dimension_expression_id},pattern_expression_id={self.pattern_expression_id},import_expression_id={self.import_expression_id},permissible_value_text={self.permissible_value_text},unique_key_unique_key_name={self.unique_key_unique_key_name},)"



    


class PermissibleValue(Base):
    """
    a permissible value, accompanied by intended text and an optional mapping to a concept URI
    """
    __tablename__ = 'permissible_value'

    text = Column(Text(), primary_key=True, nullable=False )
    description = Column(Text())
    meaning = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
    enum_expression_id = Column(Integer(), ForeignKey('enum_expression.id'))
    anonymous_enum_expression_id = Column(Integer(), ForeignKey('anonymous_enum_expression.id'))
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'))
    unit_id = Column(Integer(), ForeignKey('UnitOfMeasure.id'))
    unit = relationship("UnitOfMeasure", uselist=False, foreign_keys=[unit_id])
    
    
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
    
    
    aliases_rel = relationship( "PermissibleValueAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: PermissibleValueAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='permissible_value', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='permissible_value_text', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.permissible_value_text]")
    
    
    mappings_rel = relationship( "PermissibleValueMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: PermissibleValueMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "PermissibleValueExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: PermissibleValueExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "PermissibleValueCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: PermissibleValueCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "PermissibleValueRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: PermissibleValueRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "PermissibleValueNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: PermissibleValueNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "PermissibleValueBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: PermissibleValueBroadMappings(broad_mappings=x_))
    
    
    contributors_rel = relationship( "PermissibleValueContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: PermissibleValueContributors(contributors=x_))
    
    
    categories_rel = relationship( "PermissibleValueCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: PermissibleValueCategory(category=x_))
    
    
    keywords_rel = relationship( "PermissibleValueKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: PermissibleValueKeyword(keyword=x_))
    

    def __repr__(self):
        return f"permissible_value(text={self.text},description={self.description},meaning={self.meaning},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},enum_expression_id={self.enum_expression_id},anonymous_enum_expression_id={self.anonymous_enum_expression_id},enum_definition_name={self.enum_definition_name},unit_id={self.unit_id},)"



    


class UniqueKey(Base):
    """
    a collection of slots whose values uniquely identify an instance of a class
    """
    __tablename__ = 'unique_key'

    unique_key_name = Column(Text(), primary_key=True, nullable=False )
    consider_nulls_inequal = Column(Boolean(), primary_key=True)
    description = Column(Text(), primary_key=True)
    title = Column(Text(), primary_key=True)
    deprecated = Column(Text(), primary_key=True)
    from_schema = Column(Text(), primary_key=True)
    imported_from = Column(Text(), primary_key=True)
    source = Column(Text(), primary_key=True)
    in_language = Column(Text(), primary_key=True)
    deprecated_element_has_exact_replacement = Column(Text(), primary_key=True)
    deprecated_element_has_possible_replacement = Column(Text(), primary_key=True)
    created_by = Column(Text(), primary_key=True)
    created_on = Column(DateTime(), primary_key=True)
    last_updated_on = Column(DateTime(), primary_key=True)
    modified_by = Column(Text(), primary_key=True)
    status = Column(Text(), primary_key=True)
    rank = Column(Integer(), primary_key=True)
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    
    
    # ManyToMany
    unique_key_slots = relationship( "SlotDefinition", secondary="unique_key_unique_key_slots")
    
    
    # One-To-Many: OneToAnyMapping(source_class='unique_key', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='unique_key_unique_key_name', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.unique_key_unique_key_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='unique_key', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='unique_key_unique_key_name', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.unique_key_unique_key_name]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='unique_key', source_slot='alt_descriptions', mapping_type=None, target_class='alt_description', target_slot='unique_key_unique_key_name', join_class=None, uses_join_table=None, multivalued=False)
    alt_descriptions = relationship( "AltDescription", foreign_keys="[alt_description.unique_key_unique_key_name]")
    
    
    todos_rel = relationship( "UniqueKeyTodos" )
    todos = association_proxy("todos_rel", "todos",
                                  creator=lambda x_: UniqueKeyTodos(todos=x_))
    
    
    notes_rel = relationship( "UniqueKeyNotes" )
    notes = association_proxy("notes_rel", "notes",
                                  creator=lambda x_: UniqueKeyNotes(notes=x_))
    
    
    comments_rel = relationship( "UniqueKeyComments" )
    comments = association_proxy("comments_rel", "comments",
                                  creator=lambda x_: UniqueKeyComments(comments=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='unique_key', source_slot='examples', mapping_type=None, target_class='example', target_slot='unique_key_unique_key_name', join_class=None, uses_join_table=None, multivalued=False)
    examples = relationship( "Example", foreign_keys="[example.unique_key_unique_key_name]")
    
    
    # ManyToMany
    in_subset = relationship( "SubsetDefinition", secondary="unique_key_in_subset")
    
    
    see_also_rel = relationship( "UniqueKeySeeAlso" )
    see_also = association_proxy("see_also_rel", "see_also",
                                  creator=lambda x_: UniqueKeySeeAlso(see_also=x_))
    
    
    aliases_rel = relationship( "UniqueKeyAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: UniqueKeyAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='unique_key', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='unique_key_unique_key_name', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.unique_key_unique_key_name]")
    
    
    mappings_rel = relationship( "UniqueKeyMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: UniqueKeyMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "UniqueKeyExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: UniqueKeyExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "UniqueKeyCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: UniqueKeyCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "UniqueKeyRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: UniqueKeyRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "UniqueKeyNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: UniqueKeyNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "UniqueKeyBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: UniqueKeyBroadMappings(broad_mappings=x_))
    
    
    contributors_rel = relationship( "UniqueKeyContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: UniqueKeyContributors(contributors=x_))
    
    
    categories_rel = relationship( "UniqueKeyCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: UniqueKeyCategory(category=x_))
    
    
    keywords_rel = relationship( "UniqueKeyKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: UniqueKeyKeyword(keyword=x_))
    

    def __repr__(self):
        return f"unique_key(unique_key_name={self.unique_key_name},consider_nulls_inequal={self.consider_nulls_inequal},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},class_definition_name={self.class_definition_name},)"



    


class AnyValue(Base):
    """
    
    """
    __tablename__ = 'AnyValue'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    

    def __repr__(self):
        return f"AnyValue(id={self.id},)"



    


class Extension(Base):
    """
    a tag/value pair used to add non-model information to an entry
    """
    __tablename__ = 'extension'

    tag = Column(Text(), primary_key=True, nullable=False )
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    extension_tag = Column(Text(), ForeignKey('extension.tag'), primary_key=True)
    extensible_id = Column(Integer(), ForeignKey('extensible.id'), primary_key=True)
    annotation_tag = Column(Text(), ForeignKey('annotation.tag'), primary_key=True)
    value_id = Column(Integer(), ForeignKey('AnyValue.id'), primary_key=True, nullable=False )
    value = relationship("AnyValue", uselist=False, foreign_keys=[value_id])
    
    
    # One-To-Many: OneToAnyMapping(source_class='extension', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='extension_tag', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.extension_tag]")
    

    def __repr__(self):
        return f"extension(tag={self.tag},element_name={self.element_name},schema_definition_name={self.schema_definition_name},type_definition_name={self.type_definition_name},subset_definition_name={self.subset_definition_name},definition_name={self.definition_name},enum_definition_name={self.enum_definition_name},structured_alias_id={self.structured_alias_id},anonymous_expression_id={self.anonymous_expression_id},path_expression_id={self.path_expression_id},anonymous_slot_expression_id={self.anonymous_slot_expression_id},slot_definition_name={self.slot_definition_name},anonymous_class_expression_id={self.anonymous_class_expression_id},class_definition_name={self.class_definition_name},class_rule_id={self.class_rule_id},array_expression_id={self.array_expression_id},dimension_expression_id={self.dimension_expression_id},pattern_expression_id={self.pattern_expression_id},import_expression_id={self.import_expression_id},permissible_value_text={self.permissible_value_text},unique_key_unique_key_name={self.unique_key_unique_key_name},extension_tag={self.extension_tag},extensible_id={self.extensible_id},annotation_tag={self.annotation_tag},value_id={self.value_id},)"



    


class Extensible(Base):
    """
    mixin for classes that support extension
    """
    __tablename__ = 'extensible'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    
    
    # One-To-Many: OneToAnyMapping(source_class='extensible', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='extensible_id', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.extensible_id]")
    

    def __repr__(self):
        return f"extensible(id={self.id},)"



    


class Annotatable(Base):
    """
    mixin for classes that support annotations
    """
    __tablename__ = 'annotatable'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    
    
    # One-To-Many: OneToAnyMapping(source_class='annotatable', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='annotatable_id', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.annotatable_id]")
    

    def __repr__(self):
        return f"annotatable(id={self.id},)"



    


class UnitOfMeasure(Base):
    """
    A unit of measure, or unit, is a particular quantity value that has been chosen as a scale for  measuring other quantities the same kind (more generally of equivalent dimension).
    """
    __tablename__ = 'UnitOfMeasure'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    symbol = Column(Text())
    abbreviation = Column(Text())
    descriptive_name = Column(Text())
    ucum_code = Column(Text())
    derivation = Column(Text())
    has_quantity_kind = Column(Text())
    iec61360code = Column(Text())
    
    
    exact_mappings_rel = relationship( "UnitOfMeasureExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: UnitOfMeasureExactMappings(exact_mappings=x_))
    

    def __repr__(self):
        return f"UnitOfMeasure(id={self.id},symbol={self.symbol},abbreviation={self.abbreviation},descriptive_name={self.descriptive_name},ucum_code={self.ucum_code},derivation={self.derivation},has_quantity_kind={self.has_quantity_kind},iec61360code={self.iec61360code},)"



    


class CommonMetadataTodos(Base):
    """
    
    """
    __tablename__ = 'common_metadata_todos'

    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"common_metadata_todos(common_metadata_id={self.common_metadata_id},todos={self.todos},)"



    


class CommonMetadataNotes(Base):
    """
    
    """
    __tablename__ = 'common_metadata_notes'

    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"common_metadata_notes(common_metadata_id={self.common_metadata_id},notes={self.notes},)"



    


class CommonMetadataComments(Base):
    """
    
    """
    __tablename__ = 'common_metadata_comments'

    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"common_metadata_comments(common_metadata_id={self.common_metadata_id},comments={self.comments},)"



    


class CommonMetadataInSubset(Base):
    """
    
    """
    __tablename__ = 'common_metadata_in_subset'

    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'), primary_key=True)
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"common_metadata_in_subset(common_metadata_id={self.common_metadata_id},in_subset_name={self.in_subset_name},)"



    


class CommonMetadataSeeAlso(Base):
    """
    
    """
    __tablename__ = 'common_metadata_see_also'

    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"common_metadata_see_also(common_metadata_id={self.common_metadata_id},see_also={self.see_also},)"



    


class CommonMetadataAliases(Base):
    """
    
    """
    __tablename__ = 'common_metadata_aliases'

    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"common_metadata_aliases(common_metadata_id={self.common_metadata_id},aliases={self.aliases},)"



    


class CommonMetadataMappings(Base):
    """
    
    """
    __tablename__ = 'common_metadata_mappings'

    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"common_metadata_mappings(common_metadata_id={self.common_metadata_id},mappings={self.mappings},)"



    


class CommonMetadataExactMappings(Base):
    """
    
    """
    __tablename__ = 'common_metadata_exact_mappings'

    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"common_metadata_exact_mappings(common_metadata_id={self.common_metadata_id},exact_mappings={self.exact_mappings},)"



    


class CommonMetadataCloseMappings(Base):
    """
    
    """
    __tablename__ = 'common_metadata_close_mappings'

    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"common_metadata_close_mappings(common_metadata_id={self.common_metadata_id},close_mappings={self.close_mappings},)"



    


class CommonMetadataRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'common_metadata_related_mappings'

    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"common_metadata_related_mappings(common_metadata_id={self.common_metadata_id},related_mappings={self.related_mappings},)"



    


class CommonMetadataNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'common_metadata_narrow_mappings'

    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"common_metadata_narrow_mappings(common_metadata_id={self.common_metadata_id},narrow_mappings={self.narrow_mappings},)"



    


class CommonMetadataBroadMappings(Base):
    """
    
    """
    __tablename__ = 'common_metadata_broad_mappings'

    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"common_metadata_broad_mappings(common_metadata_id={self.common_metadata_id},broad_mappings={self.broad_mappings},)"



    


class CommonMetadataContributors(Base):
    """
    
    """
    __tablename__ = 'common_metadata_contributors'

    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"common_metadata_contributors(common_metadata_id={self.common_metadata_id},contributors={self.contributors},)"



    


class CommonMetadataCategory(Base):
    """
    
    """
    __tablename__ = 'common_metadata_category'

    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"common_metadata_category(common_metadata_id={self.common_metadata_id},category={self.category},)"



    


class CommonMetadataKeyword(Base):
    """
    
    """
    __tablename__ = 'common_metadata_keyword'

    common_metadata_id = Column(Integer(), ForeignKey('common_metadata.id'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"common_metadata_keyword(common_metadata_id={self.common_metadata_id},keyword={self.keyword},)"



    


class ElementIdPrefixes(Base):
    """
    
    """
    __tablename__ = 'element_id_prefixes'

    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    id_prefixes = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"element_id_prefixes(element_name={self.element_name},id_prefixes={self.id_prefixes},)"



    


class ElementImplements(Base):
    """
    
    """
    __tablename__ = 'element_implements'

    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    implements = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"element_implements(element_name={self.element_name},implements={self.implements},)"



    


class ElementInstantiates(Base):
    """
    
    """
    __tablename__ = 'element_instantiates'

    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    instantiates = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"element_instantiates(element_name={self.element_name},instantiates={self.instantiates},)"



    


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
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"element_in_subset(element_name={self.element_name},in_subset_name={self.in_subset_name},)"



    


class ElementSeeAlso(Base):
    """
    
    """
    __tablename__ = 'element_see_also'

    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"element_see_also(element_name={self.element_name},see_also={self.see_also},)"



    


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



    


class ElementContributors(Base):
    """
    
    """
    __tablename__ = 'element_contributors'

    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"element_contributors(element_name={self.element_name},contributors={self.contributors},)"



    


class ElementCategory(Base):
    """
    
    """
    __tablename__ = 'element_category'

    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"element_category(element_name={self.element_name},category={self.category},)"



    


class ElementKeyword(Base):
    """
    
    """
    __tablename__ = 'element_keyword'

    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"element_keyword(element_name={self.element_name},keyword={self.keyword},)"



    


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



    


class SchemaDefinitionImplements(Base):
    """
    
    """
    __tablename__ = 'schema_definition_implements'

    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    implements = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"schema_definition_implements(schema_definition_name={self.schema_definition_name},implements={self.implements},)"



    


class SchemaDefinitionInstantiates(Base):
    """
    
    """
    __tablename__ = 'schema_definition_instantiates'

    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    instantiates = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"schema_definition_instantiates(schema_definition_name={self.schema_definition_name},instantiates={self.instantiates},)"



    


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
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"schema_definition_in_subset(schema_definition_name={self.schema_definition_name},in_subset_name={self.in_subset_name},)"



    


class SchemaDefinitionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'schema_definition_see_also'

    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"schema_definition_see_also(schema_definition_name={self.schema_definition_name},see_also={self.see_also},)"



    


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



    


class SchemaDefinitionContributors(Base):
    """
    
    """
    __tablename__ = 'schema_definition_contributors'

    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"schema_definition_contributors(schema_definition_name={self.schema_definition_name},contributors={self.contributors},)"



    


class SchemaDefinitionCategory(Base):
    """
    
    """
    __tablename__ = 'schema_definition_category'

    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"schema_definition_category(schema_definition_name={self.schema_definition_name},category={self.category},)"



    


class SchemaDefinitionKeyword(Base):
    """
    
    """
    __tablename__ = 'schema_definition_keyword'

    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"schema_definition_keyword(schema_definition_name={self.schema_definition_name},keyword={self.keyword},)"



    


class TypeExpressionEqualsStringIn(Base):
    """
    
    """
    __tablename__ = 'type_expression_equals_string_in'

    type_expression_id = Column(Integer(), ForeignKey('type_expression.id'), primary_key=True)
    equals_string_in = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"type_expression_equals_string_in(type_expression_id={self.type_expression_id},equals_string_in={self.equals_string_in},)"



    


class TypeExpressionNoneOf(Base):
    """
    
    """
    __tablename__ = 'type_expression_none_of'

    type_expression_id = Column(Integer(), ForeignKey('type_expression.id'), primary_key=True)
    none_of_id = Column(Integer(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"type_expression_none_of(type_expression_id={self.type_expression_id},none_of_id={self.none_of_id},)"



    


class TypeExpressionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'type_expression_exactly_one_of'

    type_expression_id = Column(Integer(), ForeignKey('type_expression.id'), primary_key=True)
    exactly_one_of_id = Column(Integer(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"type_expression_exactly_one_of(type_expression_id={self.type_expression_id},exactly_one_of_id={self.exactly_one_of_id},)"



    


class TypeExpressionAnyOf(Base):
    """
    
    """
    __tablename__ = 'type_expression_any_of'

    type_expression_id = Column(Integer(), ForeignKey('type_expression.id'), primary_key=True)
    any_of_id = Column(Integer(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"type_expression_any_of(type_expression_id={self.type_expression_id},any_of_id={self.any_of_id},)"



    


class TypeExpressionAllOf(Base):
    """
    
    """
    __tablename__ = 'type_expression_all_of'

    type_expression_id = Column(Integer(), ForeignKey('type_expression.id'), primary_key=True)
    all_of_id = Column(Integer(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"type_expression_all_of(type_expression_id={self.type_expression_id},all_of_id={self.all_of_id},)"



    


class AnonymousTypeExpressionEqualsStringIn(Base):
    """
    
    """
    __tablename__ = 'anonymous_type_expression_equals_string_in'

    anonymous_type_expression_id = Column(Integer(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    equals_string_in = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_type_expression_equals_string_in(anonymous_type_expression_id={self.anonymous_type_expression_id},equals_string_in={self.equals_string_in},)"



    


class AnonymousTypeExpressionNoneOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_type_expression_none_of'

    anonymous_type_expression_id = Column(Integer(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    none_of_id = Column(Integer(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_type_expression_none_of(anonymous_type_expression_id={self.anonymous_type_expression_id},none_of_id={self.none_of_id},)"



    


class AnonymousTypeExpressionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_type_expression_exactly_one_of'

    anonymous_type_expression_id = Column(Integer(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    exactly_one_of_id = Column(Integer(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_type_expression_exactly_one_of(anonymous_type_expression_id={self.anonymous_type_expression_id},exactly_one_of_id={self.exactly_one_of_id},)"



    


class AnonymousTypeExpressionAnyOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_type_expression_any_of'

    anonymous_type_expression_id = Column(Integer(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    any_of_id = Column(Integer(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_type_expression_any_of(anonymous_type_expression_id={self.anonymous_type_expression_id},any_of_id={self.any_of_id},)"



    


class AnonymousTypeExpressionAllOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_type_expression_all_of'

    anonymous_type_expression_id = Column(Integer(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    all_of_id = Column(Integer(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_type_expression_all_of(anonymous_type_expression_id={self.anonymous_type_expression_id},all_of_id={self.all_of_id},)"



    


class TypeDefinitionUnionOf(Base):
    """
    
    """
    __tablename__ = 'type_definition_union_of'

    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    union_of_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"type_definition_union_of(type_definition_name={self.type_definition_name},union_of_name={self.union_of_name},)"



    


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
    none_of_id = Column(Integer(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"type_definition_none_of(type_definition_name={self.type_definition_name},none_of_id={self.none_of_id},)"



    


class TypeDefinitionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'type_definition_exactly_one_of'

    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    exactly_one_of_id = Column(Integer(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"type_definition_exactly_one_of(type_definition_name={self.type_definition_name},exactly_one_of_id={self.exactly_one_of_id},)"



    


class TypeDefinitionAnyOf(Base):
    """
    
    """
    __tablename__ = 'type_definition_any_of'

    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    any_of_id = Column(Integer(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"type_definition_any_of(type_definition_name={self.type_definition_name},any_of_id={self.any_of_id},)"



    


class TypeDefinitionAllOf(Base):
    """
    
    """
    __tablename__ = 'type_definition_all_of'

    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    all_of_id = Column(Integer(), ForeignKey('anonymous_type_expression.id'), primary_key=True)
    

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



    


class TypeDefinitionImplements(Base):
    """
    
    """
    __tablename__ = 'type_definition_implements'

    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    implements = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"type_definition_implements(type_definition_name={self.type_definition_name},implements={self.implements},)"



    


class TypeDefinitionInstantiates(Base):
    """
    
    """
    __tablename__ = 'type_definition_instantiates'

    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    instantiates = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"type_definition_instantiates(type_definition_name={self.type_definition_name},instantiates={self.instantiates},)"



    


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
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"type_definition_in_subset(type_definition_name={self.type_definition_name},in_subset_name={self.in_subset_name},)"



    


class TypeDefinitionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'type_definition_see_also'

    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"type_definition_see_also(type_definition_name={self.type_definition_name},see_also={self.see_also},)"



    


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



    


class TypeDefinitionContributors(Base):
    """
    
    """
    __tablename__ = 'type_definition_contributors'

    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"type_definition_contributors(type_definition_name={self.type_definition_name},contributors={self.contributors},)"



    


class TypeDefinitionCategory(Base):
    """
    
    """
    __tablename__ = 'type_definition_category'

    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"type_definition_category(type_definition_name={self.type_definition_name},category={self.category},)"



    


class TypeDefinitionKeyword(Base):
    """
    
    """
    __tablename__ = 'type_definition_keyword'

    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"type_definition_keyword(type_definition_name={self.type_definition_name},keyword={self.keyword},)"



    


class SubsetDefinitionIdPrefixes(Base):
    """
    
    """
    __tablename__ = 'subset_definition_id_prefixes'

    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    id_prefixes = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"subset_definition_id_prefixes(subset_definition_name={self.subset_definition_name},id_prefixes={self.id_prefixes},)"



    


class SubsetDefinitionImplements(Base):
    """
    
    """
    __tablename__ = 'subset_definition_implements'

    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    implements = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"subset_definition_implements(subset_definition_name={self.subset_definition_name},implements={self.implements},)"



    


class SubsetDefinitionInstantiates(Base):
    """
    
    """
    __tablename__ = 'subset_definition_instantiates'

    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    instantiates = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"subset_definition_instantiates(subset_definition_name={self.subset_definition_name},instantiates={self.instantiates},)"



    


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
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"subset_definition_in_subset(subset_definition_name={self.subset_definition_name},in_subset_name={self.in_subset_name},)"



    


class SubsetDefinitionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'subset_definition_see_also'

    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"subset_definition_see_also(subset_definition_name={self.subset_definition_name},see_also={self.see_also},)"



    


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



    


class SubsetDefinitionContributors(Base):
    """
    
    """
    __tablename__ = 'subset_definition_contributors'

    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"subset_definition_contributors(subset_definition_name={self.subset_definition_name},contributors={self.contributors},)"



    


class SubsetDefinitionCategory(Base):
    """
    
    """
    __tablename__ = 'subset_definition_category'

    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"subset_definition_category(subset_definition_name={self.subset_definition_name},category={self.category},)"



    


class SubsetDefinitionKeyword(Base):
    """
    
    """
    __tablename__ = 'subset_definition_keyword'

    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"subset_definition_keyword(subset_definition_name={self.subset_definition_name},keyword={self.keyword},)"



    


class DefinitionMixins(Base):
    """
    
    """
    __tablename__ = 'definition_mixins'

    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    mixins_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"definition_mixins(definition_name={self.definition_name},mixins_name={self.mixins_name},)"



    


class DefinitionApplyTo(Base):
    """
    
    """
    __tablename__ = 'definition_apply_to'

    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    apply_to_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"definition_apply_to(definition_name={self.definition_name},apply_to_name={self.apply_to_name},)"



    


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



    


class DefinitionImplements(Base):
    """
    
    """
    __tablename__ = 'definition_implements'

    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    implements = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"definition_implements(definition_name={self.definition_name},implements={self.implements},)"



    


class DefinitionInstantiates(Base):
    """
    
    """
    __tablename__ = 'definition_instantiates'

    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    instantiates = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"definition_instantiates(definition_name={self.definition_name},instantiates={self.instantiates},)"



    


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
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"definition_in_subset(definition_name={self.definition_name},in_subset_name={self.in_subset_name},)"



    


class DefinitionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'definition_see_also'

    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"definition_see_also(definition_name={self.definition_name},see_also={self.see_also},)"



    


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



    


class DefinitionContributors(Base):
    """
    
    """
    __tablename__ = 'definition_contributors'

    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"definition_contributors(definition_name={self.definition_name},contributors={self.contributors},)"



    


class DefinitionCategory(Base):
    """
    
    """
    __tablename__ = 'definition_category'

    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"definition_category(definition_name={self.definition_name},category={self.category},)"



    


class DefinitionKeyword(Base):
    """
    
    """
    __tablename__ = 'definition_keyword'

    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"definition_keyword(definition_name={self.definition_name},keyword={self.keyword},)"



    


class EnumExpressionInclude(Base):
    """
    
    """
    __tablename__ = 'enum_expression_include'

    enum_expression_id = Column(Integer(), ForeignKey('enum_expression.id'), primary_key=True)
    include_id = Column(Integer(), ForeignKey('anonymous_enum_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"enum_expression_include(enum_expression_id={self.enum_expression_id},include_id={self.include_id},)"



    


class EnumExpressionMinus(Base):
    """
    
    """
    __tablename__ = 'enum_expression_minus'

    enum_expression_id = Column(Integer(), ForeignKey('enum_expression.id'), primary_key=True)
    minus_id = Column(Integer(), ForeignKey('anonymous_enum_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"enum_expression_minus(enum_expression_id={self.enum_expression_id},minus_id={self.minus_id},)"



    


class EnumExpressionInherits(Base):
    """
    
    """
    __tablename__ = 'enum_expression_inherits'

    enum_expression_id = Column(Integer(), ForeignKey('enum_expression.id'), primary_key=True)
    inherits_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"enum_expression_inherits(enum_expression_id={self.enum_expression_id},inherits_name={self.inherits_name},)"



    


class EnumExpressionConcepts(Base):
    """
    
    """
    __tablename__ = 'enum_expression_concepts'

    enum_expression_id = Column(Integer(), ForeignKey('enum_expression.id'), primary_key=True)
    concepts = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"enum_expression_concepts(enum_expression_id={self.enum_expression_id},concepts={self.concepts},)"



    


class AnonymousEnumExpressionInclude(Base):
    """
    
    """
    __tablename__ = 'anonymous_enum_expression_include'

    anonymous_enum_expression_id = Column(Integer(), ForeignKey('anonymous_enum_expression.id'), primary_key=True)
    include_id = Column(Integer(), ForeignKey('anonymous_enum_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_enum_expression_include(anonymous_enum_expression_id={self.anonymous_enum_expression_id},include_id={self.include_id},)"



    


class AnonymousEnumExpressionMinus(Base):
    """
    
    """
    __tablename__ = 'anonymous_enum_expression_minus'

    anonymous_enum_expression_id = Column(Integer(), ForeignKey('anonymous_enum_expression.id'), primary_key=True)
    minus_id = Column(Integer(), ForeignKey('anonymous_enum_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_enum_expression_minus(anonymous_enum_expression_id={self.anonymous_enum_expression_id},minus_id={self.minus_id},)"



    


class AnonymousEnumExpressionInherits(Base):
    """
    
    """
    __tablename__ = 'anonymous_enum_expression_inherits'

    anonymous_enum_expression_id = Column(Integer(), ForeignKey('anonymous_enum_expression.id'), primary_key=True)
    inherits_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_enum_expression_inherits(anonymous_enum_expression_id={self.anonymous_enum_expression_id},inherits_name={self.inherits_name},)"



    


class AnonymousEnumExpressionConcepts(Base):
    """
    
    """
    __tablename__ = 'anonymous_enum_expression_concepts'

    anonymous_enum_expression_id = Column(Integer(), ForeignKey('anonymous_enum_expression.id'), primary_key=True)
    concepts = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_enum_expression_concepts(anonymous_enum_expression_id={self.anonymous_enum_expression_id},concepts={self.concepts},)"



    


class EnumDefinitionInclude(Base):
    """
    
    """
    __tablename__ = 'enum_definition_include'

    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    include_id = Column(Integer(), ForeignKey('anonymous_enum_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"enum_definition_include(enum_definition_name={self.enum_definition_name},include_id={self.include_id},)"



    


class EnumDefinitionMinus(Base):
    """
    
    """
    __tablename__ = 'enum_definition_minus'

    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    minus_id = Column(Integer(), ForeignKey('anonymous_enum_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"enum_definition_minus(enum_definition_name={self.enum_definition_name},minus_id={self.minus_id},)"



    


class EnumDefinitionInherits(Base):
    """
    
    """
    __tablename__ = 'enum_definition_inherits'

    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    inherits_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"enum_definition_inherits(enum_definition_name={self.enum_definition_name},inherits_name={self.inherits_name},)"



    


class EnumDefinitionConcepts(Base):
    """
    
    """
    __tablename__ = 'enum_definition_concepts'

    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    concepts = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"enum_definition_concepts(enum_definition_name={self.enum_definition_name},concepts={self.concepts},)"



    


class EnumDefinitionMixins(Base):
    """
    
    """
    __tablename__ = 'enum_definition_mixins'

    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    mixins_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"enum_definition_mixins(enum_definition_name={self.enum_definition_name},mixins_name={self.mixins_name},)"



    


class EnumDefinitionApplyTo(Base):
    """
    
    """
    __tablename__ = 'enum_definition_apply_to'

    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    apply_to_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"enum_definition_apply_to(enum_definition_name={self.enum_definition_name},apply_to_name={self.apply_to_name},)"



    


class EnumDefinitionValuesFrom(Base):
    """
    
    """
    __tablename__ = 'enum_definition_values_from'

    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    values_from = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"enum_definition_values_from(enum_definition_name={self.enum_definition_name},values_from={self.values_from},)"



    


class EnumDefinitionIdPrefixes(Base):
    """
    
    """
    __tablename__ = 'enum_definition_id_prefixes'

    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    id_prefixes = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"enum_definition_id_prefixes(enum_definition_name={self.enum_definition_name},id_prefixes={self.id_prefixes},)"



    


class EnumDefinitionImplements(Base):
    """
    
    """
    __tablename__ = 'enum_definition_implements'

    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    implements = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"enum_definition_implements(enum_definition_name={self.enum_definition_name},implements={self.implements},)"



    


class EnumDefinitionInstantiates(Base):
    """
    
    """
    __tablename__ = 'enum_definition_instantiates'

    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    instantiates = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"enum_definition_instantiates(enum_definition_name={self.enum_definition_name},instantiates={self.instantiates},)"



    


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
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"enum_definition_in_subset(enum_definition_name={self.enum_definition_name},in_subset_name={self.in_subset_name},)"



    


class EnumDefinitionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'enum_definition_see_also'

    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"enum_definition_see_also(enum_definition_name={self.enum_definition_name},see_also={self.see_also},)"



    


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



    


class EnumDefinitionContributors(Base):
    """
    
    """
    __tablename__ = 'enum_definition_contributors'

    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"enum_definition_contributors(enum_definition_name={self.enum_definition_name},contributors={self.contributors},)"



    


class EnumDefinitionCategory(Base):
    """
    
    """
    __tablename__ = 'enum_definition_category'

    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"enum_definition_category(enum_definition_name={self.enum_definition_name},category={self.category},)"



    


class EnumDefinitionKeyword(Base):
    """
    
    """
    __tablename__ = 'enum_definition_keyword'

    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"enum_definition_keyword(enum_definition_name={self.enum_definition_name},keyword={self.keyword},)"



    


class ReachabilityQuerySourceNodes(Base):
    """
    
    """
    __tablename__ = 'reachability_query_source_nodes'

    reachability_query_id = Column(Integer(), ForeignKey('reachability_query.id'), primary_key=True)
    source_nodes = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"reachability_query_source_nodes(reachability_query_id={self.reachability_query_id},source_nodes={self.source_nodes},)"



    


class ReachabilityQueryRelationshipTypes(Base):
    """
    
    """
    __tablename__ = 'reachability_query_relationship_types'

    reachability_query_id = Column(Integer(), ForeignKey('reachability_query.id'), primary_key=True)
    relationship_types = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"reachability_query_relationship_types(reachability_query_id={self.reachability_query_id},relationship_types={self.relationship_types},)"



    


class StructuredAliasCategory(Base):
    """
    
    """
    __tablename__ = 'structured_alias_category'

    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"structured_alias_category(structured_alias_id={self.structured_alias_id},category={self.category},)"



    


class StructuredAliasTodos(Base):
    """
    
    """
    __tablename__ = 'structured_alias_todos'

    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"structured_alias_todos(structured_alias_id={self.structured_alias_id},todos={self.todos},)"



    


class StructuredAliasNotes(Base):
    """
    
    """
    __tablename__ = 'structured_alias_notes'

    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"structured_alias_notes(structured_alias_id={self.structured_alias_id},notes={self.notes},)"



    


class StructuredAliasComments(Base):
    """
    
    """
    __tablename__ = 'structured_alias_comments'

    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"structured_alias_comments(structured_alias_id={self.structured_alias_id},comments={self.comments},)"



    


class StructuredAliasInSubset(Base):
    """
    
    """
    __tablename__ = 'structured_alias_in_subset'

    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"structured_alias_in_subset(structured_alias_id={self.structured_alias_id},in_subset_name={self.in_subset_name},)"



    


class StructuredAliasSeeAlso(Base):
    """
    
    """
    __tablename__ = 'structured_alias_see_also'

    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"structured_alias_see_also(structured_alias_id={self.structured_alias_id},see_also={self.see_also},)"



    


class StructuredAliasAliases(Base):
    """
    
    """
    __tablename__ = 'structured_alias_aliases'

    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"structured_alias_aliases(structured_alias_id={self.structured_alias_id},aliases={self.aliases},)"



    


class StructuredAliasMappings(Base):
    """
    
    """
    __tablename__ = 'structured_alias_mappings'

    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"structured_alias_mappings(structured_alias_id={self.structured_alias_id},mappings={self.mappings},)"



    


class StructuredAliasExactMappings(Base):
    """
    
    """
    __tablename__ = 'structured_alias_exact_mappings'

    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"structured_alias_exact_mappings(structured_alias_id={self.structured_alias_id},exact_mappings={self.exact_mappings},)"



    


class StructuredAliasCloseMappings(Base):
    """
    
    """
    __tablename__ = 'structured_alias_close_mappings'

    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"structured_alias_close_mappings(structured_alias_id={self.structured_alias_id},close_mappings={self.close_mappings},)"



    


class StructuredAliasRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'structured_alias_related_mappings'

    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"structured_alias_related_mappings(structured_alias_id={self.structured_alias_id},related_mappings={self.related_mappings},)"



    


class StructuredAliasNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'structured_alias_narrow_mappings'

    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"structured_alias_narrow_mappings(structured_alias_id={self.structured_alias_id},narrow_mappings={self.narrow_mappings},)"



    


class StructuredAliasBroadMappings(Base):
    """
    
    """
    __tablename__ = 'structured_alias_broad_mappings'

    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"structured_alias_broad_mappings(structured_alias_id={self.structured_alias_id},broad_mappings={self.broad_mappings},)"



    


class StructuredAliasContributors(Base):
    """
    
    """
    __tablename__ = 'structured_alias_contributors'

    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"structured_alias_contributors(structured_alias_id={self.structured_alias_id},contributors={self.contributors},)"



    


class StructuredAliasKeyword(Base):
    """
    
    """
    __tablename__ = 'structured_alias_keyword'

    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"structured_alias_keyword(structured_alias_id={self.structured_alias_id},keyword={self.keyword},)"



    


class AnonymousExpressionTodos(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_todos'

    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_expression_todos(anonymous_expression_id={self.anonymous_expression_id},todos={self.todos},)"



    


class AnonymousExpressionNotes(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_notes'

    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_expression_notes(anonymous_expression_id={self.anonymous_expression_id},notes={self.notes},)"



    


class AnonymousExpressionComments(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_comments'

    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_expression_comments(anonymous_expression_id={self.anonymous_expression_id},comments={self.comments},)"



    


class AnonymousExpressionInSubset(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_in_subset'

    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_expression_in_subset(anonymous_expression_id={self.anonymous_expression_id},in_subset_name={self.in_subset_name},)"



    


class AnonymousExpressionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_see_also'

    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_expression_see_also(anonymous_expression_id={self.anonymous_expression_id},see_also={self.see_also},)"



    


class AnonymousExpressionAliases(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_aliases'

    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_expression_aliases(anonymous_expression_id={self.anonymous_expression_id},aliases={self.aliases},)"



    


class AnonymousExpressionMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_mappings'

    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_expression_mappings(anonymous_expression_id={self.anonymous_expression_id},mappings={self.mappings},)"



    


class AnonymousExpressionExactMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_exact_mappings'

    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_expression_exact_mappings(anonymous_expression_id={self.anonymous_expression_id},exact_mappings={self.exact_mappings},)"



    


class AnonymousExpressionCloseMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_close_mappings'

    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_expression_close_mappings(anonymous_expression_id={self.anonymous_expression_id},close_mappings={self.close_mappings},)"



    


class AnonymousExpressionRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_related_mappings'

    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_expression_related_mappings(anonymous_expression_id={self.anonymous_expression_id},related_mappings={self.related_mappings},)"



    


class AnonymousExpressionNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_narrow_mappings'

    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_expression_narrow_mappings(anonymous_expression_id={self.anonymous_expression_id},narrow_mappings={self.narrow_mappings},)"



    


class AnonymousExpressionBroadMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_broad_mappings'

    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_expression_broad_mappings(anonymous_expression_id={self.anonymous_expression_id},broad_mappings={self.broad_mappings},)"



    


class AnonymousExpressionContributors(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_contributors'

    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_expression_contributors(anonymous_expression_id={self.anonymous_expression_id},contributors={self.contributors},)"



    


class AnonymousExpressionCategory(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_category'

    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_expression_category(anonymous_expression_id={self.anonymous_expression_id},category={self.category},)"



    


class AnonymousExpressionKeyword(Base):
    """
    
    """
    __tablename__ = 'anonymous_expression_keyword'

    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_expression_keyword(anonymous_expression_id={self.anonymous_expression_id},keyword={self.keyword},)"



    


class PathExpressionNoneOf(Base):
    """
    
    """
    __tablename__ = 'path_expression_none_of'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    none_of_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_none_of(path_expression_id={self.path_expression_id},none_of_id={self.none_of_id},)"



    


class PathExpressionAnyOf(Base):
    """
    
    """
    __tablename__ = 'path_expression_any_of'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    any_of_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_any_of(path_expression_id={self.path_expression_id},any_of_id={self.any_of_id},)"



    


class PathExpressionAllOf(Base):
    """
    
    """
    __tablename__ = 'path_expression_all_of'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    all_of_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_all_of(path_expression_id={self.path_expression_id},all_of_id={self.all_of_id},)"



    


class PathExpressionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'path_expression_exactly_one_of'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    exactly_one_of_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_exactly_one_of(path_expression_id={self.path_expression_id},exactly_one_of_id={self.exactly_one_of_id},)"



    


class PathExpressionTodos(Base):
    """
    
    """
    __tablename__ = 'path_expression_todos'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_todos(path_expression_id={self.path_expression_id},todos={self.todos},)"



    


class PathExpressionNotes(Base):
    """
    
    """
    __tablename__ = 'path_expression_notes'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_notes(path_expression_id={self.path_expression_id},notes={self.notes},)"



    


class PathExpressionComments(Base):
    """
    
    """
    __tablename__ = 'path_expression_comments'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_comments(path_expression_id={self.path_expression_id},comments={self.comments},)"



    


class PathExpressionInSubset(Base):
    """
    
    """
    __tablename__ = 'path_expression_in_subset'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_in_subset(path_expression_id={self.path_expression_id},in_subset_name={self.in_subset_name},)"



    


class PathExpressionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'path_expression_see_also'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_see_also(path_expression_id={self.path_expression_id},see_also={self.see_also},)"



    


class PathExpressionAliases(Base):
    """
    
    """
    __tablename__ = 'path_expression_aliases'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_aliases(path_expression_id={self.path_expression_id},aliases={self.aliases},)"



    


class PathExpressionMappings(Base):
    """
    
    """
    __tablename__ = 'path_expression_mappings'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_mappings(path_expression_id={self.path_expression_id},mappings={self.mappings},)"



    


class PathExpressionExactMappings(Base):
    """
    
    """
    __tablename__ = 'path_expression_exact_mappings'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_exact_mappings(path_expression_id={self.path_expression_id},exact_mappings={self.exact_mappings},)"



    


class PathExpressionCloseMappings(Base):
    """
    
    """
    __tablename__ = 'path_expression_close_mappings'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_close_mappings(path_expression_id={self.path_expression_id},close_mappings={self.close_mappings},)"



    


class PathExpressionRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'path_expression_related_mappings'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_related_mappings(path_expression_id={self.path_expression_id},related_mappings={self.related_mappings},)"



    


class PathExpressionNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'path_expression_narrow_mappings'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_narrow_mappings(path_expression_id={self.path_expression_id},narrow_mappings={self.narrow_mappings},)"



    


class PathExpressionBroadMappings(Base):
    """
    
    """
    __tablename__ = 'path_expression_broad_mappings'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_broad_mappings(path_expression_id={self.path_expression_id},broad_mappings={self.broad_mappings},)"



    


class PathExpressionContributors(Base):
    """
    
    """
    __tablename__ = 'path_expression_contributors'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_contributors(path_expression_id={self.path_expression_id},contributors={self.contributors},)"



    


class PathExpressionCategory(Base):
    """
    
    """
    __tablename__ = 'path_expression_category'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_category(path_expression_id={self.path_expression_id},category={self.category},)"



    


class PathExpressionKeyword(Base):
    """
    
    """
    __tablename__ = 'path_expression_keyword'

    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"path_expression_keyword(path_expression_id={self.path_expression_id},keyword={self.keyword},)"



    


class SlotExpressionEqualsStringIn(Base):
    """
    
    """
    __tablename__ = 'slot_expression_equals_string_in'

    slot_expression_id = Column(Integer(), ForeignKey('slot_expression.id'), primary_key=True)
    equals_string_in = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"slot_expression_equals_string_in(slot_expression_id={self.slot_expression_id},equals_string_in={self.equals_string_in},)"



    


class SlotExpressionNoneOf(Base):
    """
    
    """
    __tablename__ = 'slot_expression_none_of'

    slot_expression_id = Column(Integer(), ForeignKey('slot_expression.id'), primary_key=True)
    none_of_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"slot_expression_none_of(slot_expression_id={self.slot_expression_id},none_of_id={self.none_of_id},)"



    


class SlotExpressionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'slot_expression_exactly_one_of'

    slot_expression_id = Column(Integer(), ForeignKey('slot_expression.id'), primary_key=True)
    exactly_one_of_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"slot_expression_exactly_one_of(slot_expression_id={self.slot_expression_id},exactly_one_of_id={self.exactly_one_of_id},)"



    


class SlotExpressionAnyOf(Base):
    """
    
    """
    __tablename__ = 'slot_expression_any_of'

    slot_expression_id = Column(Integer(), ForeignKey('slot_expression.id'), primary_key=True)
    any_of_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"slot_expression_any_of(slot_expression_id={self.slot_expression_id},any_of_id={self.any_of_id},)"



    


class SlotExpressionAllOf(Base):
    """
    
    """
    __tablename__ = 'slot_expression_all_of'

    slot_expression_id = Column(Integer(), ForeignKey('slot_expression.id'), primary_key=True)
    all_of_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"slot_expression_all_of(slot_expression_id={self.slot_expression_id},all_of_id={self.all_of_id},)"



    


class AnonymousSlotExpressionEqualsStringIn(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_equals_string_in'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    equals_string_in = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_equals_string_in(anonymous_slot_expression_id={self.anonymous_slot_expression_id},equals_string_in={self.equals_string_in},)"



    


class AnonymousSlotExpressionNoneOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_none_of'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    none_of_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_none_of(anonymous_slot_expression_id={self.anonymous_slot_expression_id},none_of_id={self.none_of_id},)"



    


class AnonymousSlotExpressionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_exactly_one_of'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    exactly_one_of_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_exactly_one_of(anonymous_slot_expression_id={self.anonymous_slot_expression_id},exactly_one_of_id={self.exactly_one_of_id},)"



    


class AnonymousSlotExpressionAnyOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_any_of'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    any_of_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_any_of(anonymous_slot_expression_id={self.anonymous_slot_expression_id},any_of_id={self.any_of_id},)"



    


class AnonymousSlotExpressionAllOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_all_of'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    all_of_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_all_of(anonymous_slot_expression_id={self.anonymous_slot_expression_id},all_of_id={self.all_of_id},)"



    


class AnonymousSlotExpressionTodos(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_todos'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_todos(anonymous_slot_expression_id={self.anonymous_slot_expression_id},todos={self.todos},)"



    


class AnonymousSlotExpressionNotes(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_notes'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_notes(anonymous_slot_expression_id={self.anonymous_slot_expression_id},notes={self.notes},)"



    


class AnonymousSlotExpressionComments(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_comments'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_comments(anonymous_slot_expression_id={self.anonymous_slot_expression_id},comments={self.comments},)"



    


class AnonymousSlotExpressionInSubset(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_in_subset'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_in_subset(anonymous_slot_expression_id={self.anonymous_slot_expression_id},in_subset_name={self.in_subset_name},)"



    


class AnonymousSlotExpressionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_see_also'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_see_also(anonymous_slot_expression_id={self.anonymous_slot_expression_id},see_also={self.see_also},)"



    


class AnonymousSlotExpressionAliases(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_aliases'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_aliases(anonymous_slot_expression_id={self.anonymous_slot_expression_id},aliases={self.aliases},)"



    


class AnonymousSlotExpressionMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_mappings'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_mappings(anonymous_slot_expression_id={self.anonymous_slot_expression_id},mappings={self.mappings},)"



    


class AnonymousSlotExpressionExactMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_exact_mappings'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_exact_mappings(anonymous_slot_expression_id={self.anonymous_slot_expression_id},exact_mappings={self.exact_mappings},)"



    


class AnonymousSlotExpressionCloseMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_close_mappings'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_close_mappings(anonymous_slot_expression_id={self.anonymous_slot_expression_id},close_mappings={self.close_mappings},)"



    


class AnonymousSlotExpressionRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_related_mappings'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_related_mappings(anonymous_slot_expression_id={self.anonymous_slot_expression_id},related_mappings={self.related_mappings},)"



    


class AnonymousSlotExpressionNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_narrow_mappings'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_narrow_mappings(anonymous_slot_expression_id={self.anonymous_slot_expression_id},narrow_mappings={self.narrow_mappings},)"



    


class AnonymousSlotExpressionBroadMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_broad_mappings'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_broad_mappings(anonymous_slot_expression_id={self.anonymous_slot_expression_id},broad_mappings={self.broad_mappings},)"



    


class AnonymousSlotExpressionContributors(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_contributors'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_contributors(anonymous_slot_expression_id={self.anonymous_slot_expression_id},contributors={self.contributors},)"



    


class AnonymousSlotExpressionCategory(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_category'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_category(anonymous_slot_expression_id={self.anonymous_slot_expression_id},category={self.category},)"



    


class AnonymousSlotExpressionKeyword(Base):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression_keyword'

    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_slot_expression_keyword(anonymous_slot_expression_id={self.anonymous_slot_expression_id},keyword={self.keyword},)"



    


class SlotDefinitionDomainOf(Base):
    """
    
    """
    __tablename__ = 'slot_definition_domain_of'

    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    domain_of_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"slot_definition_domain_of(slot_definition_name={self.slot_definition_name},domain_of_name={self.domain_of_name},)"



    


class SlotDefinitionDisjointWith(Base):
    """
    
    """
    __tablename__ = 'slot_definition_disjoint_with'

    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    disjoint_with_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"slot_definition_disjoint_with(slot_definition_name={self.slot_definition_name},disjoint_with_name={self.disjoint_with_name},)"



    


class SlotDefinitionUnionOf(Base):
    """
    
    """
    __tablename__ = 'slot_definition_union_of'

    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    union_of_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"slot_definition_union_of(slot_definition_name={self.slot_definition_name},union_of_name={self.union_of_name},)"



    


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
    none_of_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"slot_definition_none_of(slot_definition_name={self.slot_definition_name},none_of_id={self.none_of_id},)"



    


class SlotDefinitionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'slot_definition_exactly_one_of'

    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    exactly_one_of_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"slot_definition_exactly_one_of(slot_definition_name={self.slot_definition_name},exactly_one_of_id={self.exactly_one_of_id},)"



    


class SlotDefinitionAnyOf(Base):
    """
    
    """
    __tablename__ = 'slot_definition_any_of'

    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    any_of_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"slot_definition_any_of(slot_definition_name={self.slot_definition_name},any_of_id={self.any_of_id},)"



    


class SlotDefinitionAllOf(Base):
    """
    
    """
    __tablename__ = 'slot_definition_all_of'

    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    all_of_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"slot_definition_all_of(slot_definition_name={self.slot_definition_name},all_of_id={self.all_of_id},)"



    


class SlotDefinitionMixins(Base):
    """
    
    """
    __tablename__ = 'slot_definition_mixins'

    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    mixins_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"slot_definition_mixins(slot_definition_name={self.slot_definition_name},mixins_name={self.mixins_name},)"



    


class SlotDefinitionApplyTo(Base):
    """
    
    """
    __tablename__ = 'slot_definition_apply_to'

    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    apply_to_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"slot_definition_apply_to(slot_definition_name={self.slot_definition_name},apply_to_name={self.apply_to_name},)"



    


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



    


class SlotDefinitionImplements(Base):
    """
    
    """
    __tablename__ = 'slot_definition_implements'

    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    implements = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"slot_definition_implements(slot_definition_name={self.slot_definition_name},implements={self.implements},)"



    


class SlotDefinitionInstantiates(Base):
    """
    
    """
    __tablename__ = 'slot_definition_instantiates'

    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    instantiates = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"slot_definition_instantiates(slot_definition_name={self.slot_definition_name},instantiates={self.instantiates},)"



    


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
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"slot_definition_in_subset(slot_definition_name={self.slot_definition_name},in_subset_name={self.in_subset_name},)"



    


class SlotDefinitionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'slot_definition_see_also'

    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"slot_definition_see_also(slot_definition_name={self.slot_definition_name},see_also={self.see_also},)"



    


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



    


class SlotDefinitionContributors(Base):
    """
    
    """
    __tablename__ = 'slot_definition_contributors'

    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"slot_definition_contributors(slot_definition_name={self.slot_definition_name},contributors={self.contributors},)"



    


class SlotDefinitionCategory(Base):
    """
    
    """
    __tablename__ = 'slot_definition_category'

    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"slot_definition_category(slot_definition_name={self.slot_definition_name},category={self.category},)"



    


class SlotDefinitionKeyword(Base):
    """
    
    """
    __tablename__ = 'slot_definition_keyword'

    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"slot_definition_keyword(slot_definition_name={self.slot_definition_name},keyword={self.keyword},)"



    


class ClassExpressionAnyOf(Base):
    """
    
    """
    __tablename__ = 'class_expression_any_of'

    class_expression_id = Column(Integer(), ForeignKey('class_expression.id'), primary_key=True)
    any_of_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"class_expression_any_of(class_expression_id={self.class_expression_id},any_of_id={self.any_of_id},)"



    


class ClassExpressionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'class_expression_exactly_one_of'

    class_expression_id = Column(Integer(), ForeignKey('class_expression.id'), primary_key=True)
    exactly_one_of_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"class_expression_exactly_one_of(class_expression_id={self.class_expression_id},exactly_one_of_id={self.exactly_one_of_id},)"



    


class ClassExpressionNoneOf(Base):
    """
    
    """
    __tablename__ = 'class_expression_none_of'

    class_expression_id = Column(Integer(), ForeignKey('class_expression.id'), primary_key=True)
    none_of_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"class_expression_none_of(class_expression_id={self.class_expression_id},none_of_id={self.none_of_id},)"



    


class ClassExpressionAllOf(Base):
    """
    
    """
    __tablename__ = 'class_expression_all_of'

    class_expression_id = Column(Integer(), ForeignKey('class_expression.id'), primary_key=True)
    all_of_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"class_expression_all_of(class_expression_id={self.class_expression_id},all_of_id={self.all_of_id},)"



    


class AnonymousClassExpressionAnyOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_any_of'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    any_of_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_any_of(anonymous_class_expression_id={self.anonymous_class_expression_id},any_of_id={self.any_of_id},)"



    


class AnonymousClassExpressionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_exactly_one_of'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    exactly_one_of_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_exactly_one_of(anonymous_class_expression_id={self.anonymous_class_expression_id},exactly_one_of_id={self.exactly_one_of_id},)"



    


class AnonymousClassExpressionNoneOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_none_of'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    none_of_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_none_of(anonymous_class_expression_id={self.anonymous_class_expression_id},none_of_id={self.none_of_id},)"



    


class AnonymousClassExpressionAllOf(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_all_of'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    all_of_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_all_of(anonymous_class_expression_id={self.anonymous_class_expression_id},all_of_id={self.all_of_id},)"



    


class AnonymousClassExpressionTodos(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_todos'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_todos(anonymous_class_expression_id={self.anonymous_class_expression_id},todos={self.todos},)"



    


class AnonymousClassExpressionNotes(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_notes'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_notes(anonymous_class_expression_id={self.anonymous_class_expression_id},notes={self.notes},)"



    


class AnonymousClassExpressionComments(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_comments'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_comments(anonymous_class_expression_id={self.anonymous_class_expression_id},comments={self.comments},)"



    


class AnonymousClassExpressionInSubset(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_in_subset'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_in_subset(anonymous_class_expression_id={self.anonymous_class_expression_id},in_subset_name={self.in_subset_name},)"



    


class AnonymousClassExpressionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_see_also'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_see_also(anonymous_class_expression_id={self.anonymous_class_expression_id},see_also={self.see_also},)"



    


class AnonymousClassExpressionAliases(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_aliases'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_aliases(anonymous_class_expression_id={self.anonymous_class_expression_id},aliases={self.aliases},)"



    


class AnonymousClassExpressionMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_mappings'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_mappings(anonymous_class_expression_id={self.anonymous_class_expression_id},mappings={self.mappings},)"



    


class AnonymousClassExpressionExactMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_exact_mappings'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_exact_mappings(anonymous_class_expression_id={self.anonymous_class_expression_id},exact_mappings={self.exact_mappings},)"



    


class AnonymousClassExpressionCloseMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_close_mappings'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_close_mappings(anonymous_class_expression_id={self.anonymous_class_expression_id},close_mappings={self.close_mappings},)"



    


class AnonymousClassExpressionRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_related_mappings'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_related_mappings(anonymous_class_expression_id={self.anonymous_class_expression_id},related_mappings={self.related_mappings},)"



    


class AnonymousClassExpressionNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_narrow_mappings'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_narrow_mappings(anonymous_class_expression_id={self.anonymous_class_expression_id},narrow_mappings={self.narrow_mappings},)"



    


class AnonymousClassExpressionBroadMappings(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_broad_mappings'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_broad_mappings(anonymous_class_expression_id={self.anonymous_class_expression_id},broad_mappings={self.broad_mappings},)"



    


class AnonymousClassExpressionContributors(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_contributors'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_contributors(anonymous_class_expression_id={self.anonymous_class_expression_id},contributors={self.contributors},)"



    


class AnonymousClassExpressionCategory(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_category'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_category(anonymous_class_expression_id={self.anonymous_class_expression_id},category={self.category},)"



    


class AnonymousClassExpressionKeyword(Base):
    """
    
    """
    __tablename__ = 'anonymous_class_expression_keyword'

    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"anonymous_class_expression_keyword(anonymous_class_expression_id={self.anonymous_class_expression_id},keyword={self.keyword},)"



    


class ClassDefinitionSlots(Base):
    """
    
    """
    __tablename__ = 'class_definition_slots'

    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    slots_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"class_definition_slots(class_definition_name={self.class_definition_name},slots_name={self.slots_name},)"



    


class ClassDefinitionUnionOf(Base):
    """
    
    """
    __tablename__ = 'class_definition_union_of'

    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    union_of_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"class_definition_union_of(class_definition_name={self.class_definition_name},union_of_name={self.union_of_name},)"



    


class ClassDefinitionDefiningSlots(Base):
    """
    
    """
    __tablename__ = 'class_definition_defining_slots'

    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    defining_slots_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"class_definition_defining_slots(class_definition_name={self.class_definition_name},defining_slots_name={self.defining_slots_name},)"



    


class ClassDefinitionDisjointWith(Base):
    """
    
    """
    __tablename__ = 'class_definition_disjoint_with'

    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    disjoint_with_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"class_definition_disjoint_with(class_definition_name={self.class_definition_name},disjoint_with_name={self.disjoint_with_name},)"



    


class ClassDefinitionAnyOf(Base):
    """
    
    """
    __tablename__ = 'class_definition_any_of'

    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    any_of_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"class_definition_any_of(class_definition_name={self.class_definition_name},any_of_id={self.any_of_id},)"



    


class ClassDefinitionExactlyOneOf(Base):
    """
    
    """
    __tablename__ = 'class_definition_exactly_one_of'

    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    exactly_one_of_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"class_definition_exactly_one_of(class_definition_name={self.class_definition_name},exactly_one_of_id={self.exactly_one_of_id},)"



    


class ClassDefinitionNoneOf(Base):
    """
    
    """
    __tablename__ = 'class_definition_none_of'

    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    none_of_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"class_definition_none_of(class_definition_name={self.class_definition_name},none_of_id={self.none_of_id},)"



    


class ClassDefinitionAllOf(Base):
    """
    
    """
    __tablename__ = 'class_definition_all_of'

    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    all_of_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"class_definition_all_of(class_definition_name={self.class_definition_name},all_of_id={self.all_of_id},)"



    


class ClassDefinitionMixins(Base):
    """
    
    """
    __tablename__ = 'class_definition_mixins'

    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    mixins_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"class_definition_mixins(class_definition_name={self.class_definition_name},mixins_name={self.mixins_name},)"



    


class ClassDefinitionApplyTo(Base):
    """
    
    """
    __tablename__ = 'class_definition_apply_to'

    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    apply_to_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"class_definition_apply_to(class_definition_name={self.class_definition_name},apply_to_name={self.apply_to_name},)"



    


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



    


class ClassDefinitionImplements(Base):
    """
    
    """
    __tablename__ = 'class_definition_implements'

    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    implements = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_definition_implements(class_definition_name={self.class_definition_name},implements={self.implements},)"



    


class ClassDefinitionInstantiates(Base):
    """
    
    """
    __tablename__ = 'class_definition_instantiates'

    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    instantiates = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_definition_instantiates(class_definition_name={self.class_definition_name},instantiates={self.instantiates},)"



    


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
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"class_definition_in_subset(class_definition_name={self.class_definition_name},in_subset_name={self.in_subset_name},)"



    


class ClassDefinitionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'class_definition_see_also'

    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_definition_see_also(class_definition_name={self.class_definition_name},see_also={self.see_also},)"



    


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



    


class ClassDefinitionContributors(Base):
    """
    
    """
    __tablename__ = 'class_definition_contributors'

    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_definition_contributors(class_definition_name={self.class_definition_name},contributors={self.contributors},)"



    


class ClassDefinitionCategory(Base):
    """
    
    """
    __tablename__ = 'class_definition_category'

    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_definition_category(class_definition_name={self.class_definition_name},category={self.category},)"



    


class ClassDefinitionKeyword(Base):
    """
    
    """
    __tablename__ = 'class_definition_keyword'

    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_definition_keyword(class_definition_name={self.class_definition_name},keyword={self.keyword},)"



    


class ClassRuleTodos(Base):
    """
    
    """
    __tablename__ = 'class_rule_todos'

    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_rule_todos(class_rule_id={self.class_rule_id},todos={self.todos},)"



    


class ClassRuleNotes(Base):
    """
    
    """
    __tablename__ = 'class_rule_notes'

    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_rule_notes(class_rule_id={self.class_rule_id},notes={self.notes},)"



    


class ClassRuleComments(Base):
    """
    
    """
    __tablename__ = 'class_rule_comments'

    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_rule_comments(class_rule_id={self.class_rule_id},comments={self.comments},)"



    


class ClassRuleInSubset(Base):
    """
    
    """
    __tablename__ = 'class_rule_in_subset'

    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"class_rule_in_subset(class_rule_id={self.class_rule_id},in_subset_name={self.in_subset_name},)"



    


class ClassRuleSeeAlso(Base):
    """
    
    """
    __tablename__ = 'class_rule_see_also'

    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_rule_see_also(class_rule_id={self.class_rule_id},see_also={self.see_also},)"



    


class ClassRuleAliases(Base):
    """
    
    """
    __tablename__ = 'class_rule_aliases'

    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_rule_aliases(class_rule_id={self.class_rule_id},aliases={self.aliases},)"



    


class ClassRuleMappings(Base):
    """
    
    """
    __tablename__ = 'class_rule_mappings'

    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_rule_mappings(class_rule_id={self.class_rule_id},mappings={self.mappings},)"



    


class ClassRuleExactMappings(Base):
    """
    
    """
    __tablename__ = 'class_rule_exact_mappings'

    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_rule_exact_mappings(class_rule_id={self.class_rule_id},exact_mappings={self.exact_mappings},)"



    


class ClassRuleCloseMappings(Base):
    """
    
    """
    __tablename__ = 'class_rule_close_mappings'

    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_rule_close_mappings(class_rule_id={self.class_rule_id},close_mappings={self.close_mappings},)"



    


class ClassRuleRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'class_rule_related_mappings'

    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_rule_related_mappings(class_rule_id={self.class_rule_id},related_mappings={self.related_mappings},)"



    


class ClassRuleNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'class_rule_narrow_mappings'

    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_rule_narrow_mappings(class_rule_id={self.class_rule_id},narrow_mappings={self.narrow_mappings},)"



    


class ClassRuleBroadMappings(Base):
    """
    
    """
    __tablename__ = 'class_rule_broad_mappings'

    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_rule_broad_mappings(class_rule_id={self.class_rule_id},broad_mappings={self.broad_mappings},)"



    


class ClassRuleContributors(Base):
    """
    
    """
    __tablename__ = 'class_rule_contributors'

    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_rule_contributors(class_rule_id={self.class_rule_id},contributors={self.contributors},)"



    


class ClassRuleCategory(Base):
    """
    
    """
    __tablename__ = 'class_rule_category'

    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_rule_category(class_rule_id={self.class_rule_id},category={self.category},)"



    


class ClassRuleKeyword(Base):
    """
    
    """
    __tablename__ = 'class_rule_keyword'

    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"class_rule_keyword(class_rule_id={self.class_rule_id},keyword={self.keyword},)"



    


class ArrayExpressionDimensions(Base):
    """
    
    """
    __tablename__ = 'array_expression_dimensions'

    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    dimensions_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    

    def __repr__(self):
        return f"array_expression_dimensions(array_expression_id={self.array_expression_id},dimensions_id={self.dimensions_id},)"



    


class ArrayExpressionTodos(Base):
    """
    
    """
    __tablename__ = 'array_expression_todos'

    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"array_expression_todos(array_expression_id={self.array_expression_id},todos={self.todos},)"



    


class ArrayExpressionNotes(Base):
    """
    
    """
    __tablename__ = 'array_expression_notes'

    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"array_expression_notes(array_expression_id={self.array_expression_id},notes={self.notes},)"



    


class ArrayExpressionComments(Base):
    """
    
    """
    __tablename__ = 'array_expression_comments'

    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"array_expression_comments(array_expression_id={self.array_expression_id},comments={self.comments},)"



    


class ArrayExpressionInSubset(Base):
    """
    
    """
    __tablename__ = 'array_expression_in_subset'

    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"array_expression_in_subset(array_expression_id={self.array_expression_id},in_subset_name={self.in_subset_name},)"



    


class ArrayExpressionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'array_expression_see_also'

    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"array_expression_see_also(array_expression_id={self.array_expression_id},see_also={self.see_also},)"



    


class ArrayExpressionAliases(Base):
    """
    
    """
    __tablename__ = 'array_expression_aliases'

    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"array_expression_aliases(array_expression_id={self.array_expression_id},aliases={self.aliases},)"



    


class ArrayExpressionMappings(Base):
    """
    
    """
    __tablename__ = 'array_expression_mappings'

    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"array_expression_mappings(array_expression_id={self.array_expression_id},mappings={self.mappings},)"



    


class ArrayExpressionExactMappings(Base):
    """
    
    """
    __tablename__ = 'array_expression_exact_mappings'

    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"array_expression_exact_mappings(array_expression_id={self.array_expression_id},exact_mappings={self.exact_mappings},)"



    


class ArrayExpressionCloseMappings(Base):
    """
    
    """
    __tablename__ = 'array_expression_close_mappings'

    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"array_expression_close_mappings(array_expression_id={self.array_expression_id},close_mappings={self.close_mappings},)"



    


class ArrayExpressionRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'array_expression_related_mappings'

    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"array_expression_related_mappings(array_expression_id={self.array_expression_id},related_mappings={self.related_mappings},)"



    


class ArrayExpressionNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'array_expression_narrow_mappings'

    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"array_expression_narrow_mappings(array_expression_id={self.array_expression_id},narrow_mappings={self.narrow_mappings},)"



    


class ArrayExpressionBroadMappings(Base):
    """
    
    """
    __tablename__ = 'array_expression_broad_mappings'

    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"array_expression_broad_mappings(array_expression_id={self.array_expression_id},broad_mappings={self.broad_mappings},)"



    


class ArrayExpressionContributors(Base):
    """
    
    """
    __tablename__ = 'array_expression_contributors'

    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"array_expression_contributors(array_expression_id={self.array_expression_id},contributors={self.contributors},)"



    


class ArrayExpressionCategory(Base):
    """
    
    """
    __tablename__ = 'array_expression_category'

    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"array_expression_category(array_expression_id={self.array_expression_id},category={self.category},)"



    


class ArrayExpressionKeyword(Base):
    """
    
    """
    __tablename__ = 'array_expression_keyword'

    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"array_expression_keyword(array_expression_id={self.array_expression_id},keyword={self.keyword},)"



    


class DimensionExpressionTodos(Base):
    """
    
    """
    __tablename__ = 'dimension_expression_todos'

    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"dimension_expression_todos(dimension_expression_id={self.dimension_expression_id},todos={self.todos},)"



    


class DimensionExpressionNotes(Base):
    """
    
    """
    __tablename__ = 'dimension_expression_notes'

    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"dimension_expression_notes(dimension_expression_id={self.dimension_expression_id},notes={self.notes},)"



    


class DimensionExpressionComments(Base):
    """
    
    """
    __tablename__ = 'dimension_expression_comments'

    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"dimension_expression_comments(dimension_expression_id={self.dimension_expression_id},comments={self.comments},)"



    


class DimensionExpressionInSubset(Base):
    """
    
    """
    __tablename__ = 'dimension_expression_in_subset'

    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"dimension_expression_in_subset(dimension_expression_id={self.dimension_expression_id},in_subset_name={self.in_subset_name},)"



    


class DimensionExpressionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'dimension_expression_see_also'

    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"dimension_expression_see_also(dimension_expression_id={self.dimension_expression_id},see_also={self.see_also},)"



    


class DimensionExpressionAliases(Base):
    """
    
    """
    __tablename__ = 'dimension_expression_aliases'

    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"dimension_expression_aliases(dimension_expression_id={self.dimension_expression_id},aliases={self.aliases},)"



    


class DimensionExpressionMappings(Base):
    """
    
    """
    __tablename__ = 'dimension_expression_mappings'

    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"dimension_expression_mappings(dimension_expression_id={self.dimension_expression_id},mappings={self.mappings},)"



    


class DimensionExpressionExactMappings(Base):
    """
    
    """
    __tablename__ = 'dimension_expression_exact_mappings'

    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"dimension_expression_exact_mappings(dimension_expression_id={self.dimension_expression_id},exact_mappings={self.exact_mappings},)"



    


class DimensionExpressionCloseMappings(Base):
    """
    
    """
    __tablename__ = 'dimension_expression_close_mappings'

    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"dimension_expression_close_mappings(dimension_expression_id={self.dimension_expression_id},close_mappings={self.close_mappings},)"



    


class DimensionExpressionRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'dimension_expression_related_mappings'

    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"dimension_expression_related_mappings(dimension_expression_id={self.dimension_expression_id},related_mappings={self.related_mappings},)"



    


class DimensionExpressionNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'dimension_expression_narrow_mappings'

    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"dimension_expression_narrow_mappings(dimension_expression_id={self.dimension_expression_id},narrow_mappings={self.narrow_mappings},)"



    


class DimensionExpressionBroadMappings(Base):
    """
    
    """
    __tablename__ = 'dimension_expression_broad_mappings'

    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"dimension_expression_broad_mappings(dimension_expression_id={self.dimension_expression_id},broad_mappings={self.broad_mappings},)"



    


class DimensionExpressionContributors(Base):
    """
    
    """
    __tablename__ = 'dimension_expression_contributors'

    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"dimension_expression_contributors(dimension_expression_id={self.dimension_expression_id},contributors={self.contributors},)"



    


class DimensionExpressionCategory(Base):
    """
    
    """
    __tablename__ = 'dimension_expression_category'

    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"dimension_expression_category(dimension_expression_id={self.dimension_expression_id},category={self.category},)"



    


class DimensionExpressionKeyword(Base):
    """
    
    """
    __tablename__ = 'dimension_expression_keyword'

    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"dimension_expression_keyword(dimension_expression_id={self.dimension_expression_id},keyword={self.keyword},)"



    


class PatternExpressionTodos(Base):
    """
    
    """
    __tablename__ = 'pattern_expression_todos'

    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"pattern_expression_todos(pattern_expression_id={self.pattern_expression_id},todos={self.todos},)"



    


class PatternExpressionNotes(Base):
    """
    
    """
    __tablename__ = 'pattern_expression_notes'

    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"pattern_expression_notes(pattern_expression_id={self.pattern_expression_id},notes={self.notes},)"



    


class PatternExpressionComments(Base):
    """
    
    """
    __tablename__ = 'pattern_expression_comments'

    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"pattern_expression_comments(pattern_expression_id={self.pattern_expression_id},comments={self.comments},)"



    


class PatternExpressionInSubset(Base):
    """
    
    """
    __tablename__ = 'pattern_expression_in_subset'

    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"pattern_expression_in_subset(pattern_expression_id={self.pattern_expression_id},in_subset_name={self.in_subset_name},)"



    


class PatternExpressionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'pattern_expression_see_also'

    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"pattern_expression_see_also(pattern_expression_id={self.pattern_expression_id},see_also={self.see_also},)"



    


class PatternExpressionAliases(Base):
    """
    
    """
    __tablename__ = 'pattern_expression_aliases'

    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"pattern_expression_aliases(pattern_expression_id={self.pattern_expression_id},aliases={self.aliases},)"



    


class PatternExpressionMappings(Base):
    """
    
    """
    __tablename__ = 'pattern_expression_mappings'

    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"pattern_expression_mappings(pattern_expression_id={self.pattern_expression_id},mappings={self.mappings},)"



    


class PatternExpressionExactMappings(Base):
    """
    
    """
    __tablename__ = 'pattern_expression_exact_mappings'

    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"pattern_expression_exact_mappings(pattern_expression_id={self.pattern_expression_id},exact_mappings={self.exact_mappings},)"



    


class PatternExpressionCloseMappings(Base):
    """
    
    """
    __tablename__ = 'pattern_expression_close_mappings'

    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"pattern_expression_close_mappings(pattern_expression_id={self.pattern_expression_id},close_mappings={self.close_mappings},)"



    


class PatternExpressionRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'pattern_expression_related_mappings'

    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"pattern_expression_related_mappings(pattern_expression_id={self.pattern_expression_id},related_mappings={self.related_mappings},)"



    


class PatternExpressionNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'pattern_expression_narrow_mappings'

    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"pattern_expression_narrow_mappings(pattern_expression_id={self.pattern_expression_id},narrow_mappings={self.narrow_mappings},)"



    


class PatternExpressionBroadMappings(Base):
    """
    
    """
    __tablename__ = 'pattern_expression_broad_mappings'

    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"pattern_expression_broad_mappings(pattern_expression_id={self.pattern_expression_id},broad_mappings={self.broad_mappings},)"



    


class PatternExpressionContributors(Base):
    """
    
    """
    __tablename__ = 'pattern_expression_contributors'

    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"pattern_expression_contributors(pattern_expression_id={self.pattern_expression_id},contributors={self.contributors},)"



    


class PatternExpressionCategory(Base):
    """
    
    """
    __tablename__ = 'pattern_expression_category'

    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"pattern_expression_category(pattern_expression_id={self.pattern_expression_id},category={self.category},)"



    


class PatternExpressionKeyword(Base):
    """
    
    """
    __tablename__ = 'pattern_expression_keyword'

    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"pattern_expression_keyword(pattern_expression_id={self.pattern_expression_id},keyword={self.keyword},)"



    


class ImportExpressionTodos(Base):
    """
    
    """
    __tablename__ = 'import_expression_todos'

    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"import_expression_todos(import_expression_id={self.import_expression_id},todos={self.todos},)"



    


class ImportExpressionNotes(Base):
    """
    
    """
    __tablename__ = 'import_expression_notes'

    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"import_expression_notes(import_expression_id={self.import_expression_id},notes={self.notes},)"



    


class ImportExpressionComments(Base):
    """
    
    """
    __tablename__ = 'import_expression_comments'

    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"import_expression_comments(import_expression_id={self.import_expression_id},comments={self.comments},)"



    


class ImportExpressionInSubset(Base):
    """
    
    """
    __tablename__ = 'import_expression_in_subset'

    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"import_expression_in_subset(import_expression_id={self.import_expression_id},in_subset_name={self.in_subset_name},)"



    


class ImportExpressionSeeAlso(Base):
    """
    
    """
    __tablename__ = 'import_expression_see_also'

    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"import_expression_see_also(import_expression_id={self.import_expression_id},see_also={self.see_also},)"



    


class ImportExpressionAliases(Base):
    """
    
    """
    __tablename__ = 'import_expression_aliases'

    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"import_expression_aliases(import_expression_id={self.import_expression_id},aliases={self.aliases},)"



    


class ImportExpressionMappings(Base):
    """
    
    """
    __tablename__ = 'import_expression_mappings'

    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"import_expression_mappings(import_expression_id={self.import_expression_id},mappings={self.mappings},)"



    


class ImportExpressionExactMappings(Base):
    """
    
    """
    __tablename__ = 'import_expression_exact_mappings'

    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"import_expression_exact_mappings(import_expression_id={self.import_expression_id},exact_mappings={self.exact_mappings},)"



    


class ImportExpressionCloseMappings(Base):
    """
    
    """
    __tablename__ = 'import_expression_close_mappings'

    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"import_expression_close_mappings(import_expression_id={self.import_expression_id},close_mappings={self.close_mappings},)"



    


class ImportExpressionRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'import_expression_related_mappings'

    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"import_expression_related_mappings(import_expression_id={self.import_expression_id},related_mappings={self.related_mappings},)"



    


class ImportExpressionNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'import_expression_narrow_mappings'

    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"import_expression_narrow_mappings(import_expression_id={self.import_expression_id},narrow_mappings={self.narrow_mappings},)"



    


class ImportExpressionBroadMappings(Base):
    """
    
    """
    __tablename__ = 'import_expression_broad_mappings'

    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"import_expression_broad_mappings(import_expression_id={self.import_expression_id},broad_mappings={self.broad_mappings},)"



    


class ImportExpressionContributors(Base):
    """
    
    """
    __tablename__ = 'import_expression_contributors'

    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"import_expression_contributors(import_expression_id={self.import_expression_id},contributors={self.contributors},)"



    


class ImportExpressionCategory(Base):
    """
    
    """
    __tablename__ = 'import_expression_category'

    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"import_expression_category(import_expression_id={self.import_expression_id},category={self.category},)"



    


class ImportExpressionKeyword(Base):
    """
    
    """
    __tablename__ = 'import_expression_keyword'

    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"import_expression_keyword(import_expression_id={self.import_expression_id},keyword={self.keyword},)"



    


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
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"permissible_value_in_subset(permissible_value_text={self.permissible_value_text},in_subset_name={self.in_subset_name},)"



    


class PermissibleValueSeeAlso(Base):
    """
    
    """
    __tablename__ = 'permissible_value_see_also'

    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"permissible_value_see_also(permissible_value_text={self.permissible_value_text},see_also={self.see_also},)"



    


class PermissibleValueAliases(Base):
    """
    
    """
    __tablename__ = 'permissible_value_aliases'

    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"permissible_value_aliases(permissible_value_text={self.permissible_value_text},aliases={self.aliases},)"



    


class PermissibleValueMappings(Base):
    """
    
    """
    __tablename__ = 'permissible_value_mappings'

    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"permissible_value_mappings(permissible_value_text={self.permissible_value_text},mappings={self.mappings},)"



    


class PermissibleValueExactMappings(Base):
    """
    
    """
    __tablename__ = 'permissible_value_exact_mappings'

    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"permissible_value_exact_mappings(permissible_value_text={self.permissible_value_text},exact_mappings={self.exact_mappings},)"



    


class PermissibleValueCloseMappings(Base):
    """
    
    """
    __tablename__ = 'permissible_value_close_mappings'

    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"permissible_value_close_mappings(permissible_value_text={self.permissible_value_text},close_mappings={self.close_mappings},)"



    


class PermissibleValueRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'permissible_value_related_mappings'

    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"permissible_value_related_mappings(permissible_value_text={self.permissible_value_text},related_mappings={self.related_mappings},)"



    


class PermissibleValueNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'permissible_value_narrow_mappings'

    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"permissible_value_narrow_mappings(permissible_value_text={self.permissible_value_text},narrow_mappings={self.narrow_mappings},)"



    


class PermissibleValueBroadMappings(Base):
    """
    
    """
    __tablename__ = 'permissible_value_broad_mappings'

    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"permissible_value_broad_mappings(permissible_value_text={self.permissible_value_text},broad_mappings={self.broad_mappings},)"



    


class PermissibleValueContributors(Base):
    """
    
    """
    __tablename__ = 'permissible_value_contributors'

    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"permissible_value_contributors(permissible_value_text={self.permissible_value_text},contributors={self.contributors},)"



    


class PermissibleValueCategory(Base):
    """
    
    """
    __tablename__ = 'permissible_value_category'

    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"permissible_value_category(permissible_value_text={self.permissible_value_text},category={self.category},)"



    


class PermissibleValueKeyword(Base):
    """
    
    """
    __tablename__ = 'permissible_value_keyword'

    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"permissible_value_keyword(permissible_value_text={self.permissible_value_text},keyword={self.keyword},)"



    


class UniqueKeyUniqueKeySlots(Base):
    """
    
    """
    __tablename__ = 'unique_key_unique_key_slots'

    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    unique_key_slots_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True, nullable=False )
    

    def __repr__(self):
        return f"unique_key_unique_key_slots(unique_key_unique_key_name={self.unique_key_unique_key_name},unique_key_slots_name={self.unique_key_slots_name},)"



    


class UniqueKeyTodos(Base):
    """
    
    """
    __tablename__ = 'unique_key_todos'

    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    todos = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"unique_key_todos(unique_key_unique_key_name={self.unique_key_unique_key_name},todos={self.todos},)"



    


class UniqueKeyNotes(Base):
    """
    
    """
    __tablename__ = 'unique_key_notes'

    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    notes = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"unique_key_notes(unique_key_unique_key_name={self.unique_key_unique_key_name},notes={self.notes},)"



    


class UniqueKeyComments(Base):
    """
    
    """
    __tablename__ = 'unique_key_comments'

    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    comments = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"unique_key_comments(unique_key_unique_key_name={self.unique_key_unique_key_name},comments={self.comments},)"



    


class UniqueKeyInSubset(Base):
    """
    
    """
    __tablename__ = 'unique_key_in_subset'

    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    in_subset_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    

    def __repr__(self):
        return f"unique_key_in_subset(unique_key_unique_key_name={self.unique_key_unique_key_name},in_subset_name={self.in_subset_name},)"



    


class UniqueKeySeeAlso(Base):
    """
    
    """
    __tablename__ = 'unique_key_see_also'

    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    see_also = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"unique_key_see_also(unique_key_unique_key_name={self.unique_key_unique_key_name},see_also={self.see_also},)"



    


class UniqueKeyAliases(Base):
    """
    
    """
    __tablename__ = 'unique_key_aliases'

    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    aliases = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"unique_key_aliases(unique_key_unique_key_name={self.unique_key_unique_key_name},aliases={self.aliases},)"



    


class UniqueKeyMappings(Base):
    """
    
    """
    __tablename__ = 'unique_key_mappings'

    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"unique_key_mappings(unique_key_unique_key_name={self.unique_key_unique_key_name},mappings={self.mappings},)"



    


class UniqueKeyExactMappings(Base):
    """
    
    """
    __tablename__ = 'unique_key_exact_mappings'

    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"unique_key_exact_mappings(unique_key_unique_key_name={self.unique_key_unique_key_name},exact_mappings={self.exact_mappings},)"



    


class UniqueKeyCloseMappings(Base):
    """
    
    """
    __tablename__ = 'unique_key_close_mappings'

    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    close_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"unique_key_close_mappings(unique_key_unique_key_name={self.unique_key_unique_key_name},close_mappings={self.close_mappings},)"



    


class UniqueKeyRelatedMappings(Base):
    """
    
    """
    __tablename__ = 'unique_key_related_mappings'

    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    related_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"unique_key_related_mappings(unique_key_unique_key_name={self.unique_key_unique_key_name},related_mappings={self.related_mappings},)"



    


class UniqueKeyNarrowMappings(Base):
    """
    
    """
    __tablename__ = 'unique_key_narrow_mappings'

    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    narrow_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"unique_key_narrow_mappings(unique_key_unique_key_name={self.unique_key_unique_key_name},narrow_mappings={self.narrow_mappings},)"



    


class UniqueKeyBroadMappings(Base):
    """
    
    """
    __tablename__ = 'unique_key_broad_mappings'

    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    broad_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"unique_key_broad_mappings(unique_key_unique_key_name={self.unique_key_unique_key_name},broad_mappings={self.broad_mappings},)"



    


class UniqueKeyContributors(Base):
    """
    
    """
    __tablename__ = 'unique_key_contributors'

    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    contributors = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"unique_key_contributors(unique_key_unique_key_name={self.unique_key_unique_key_name},contributors={self.contributors},)"



    


class UniqueKeyCategory(Base):
    """
    
    """
    __tablename__ = 'unique_key_category'

    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    category = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"unique_key_category(unique_key_unique_key_name={self.unique_key_unique_key_name},category={self.category},)"



    


class UniqueKeyKeyword(Base):
    """
    
    """
    __tablename__ = 'unique_key_keyword'

    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    keyword = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"unique_key_keyword(unique_key_unique_key_name={self.unique_key_unique_key_name},keyword={self.keyword},)"



    


class UnitOfMeasureExactMappings(Base):
    """
    
    """
    __tablename__ = 'UnitOfMeasure_exact_mappings'

    UnitOfMeasure_id = Column(Integer(), ForeignKey('UnitOfMeasure.id'), primary_key=True)
    exact_mappings = Column(Text(), primary_key=True)
    

    def __repr__(self):
        return f"UnitOfMeasure_exact_mappings(UnitOfMeasure_id={self.UnitOfMeasure_id},exact_mappings={self.exact_mappings},)"



    


class SchemaDefinition(Element):
    """
    A collection of definitions that make up a schema or a data model.
    """
    __tablename__ = 'schema_definition'

    id = Column(Text(), nullable=False )
    version = Column(Text())
    license = Column(Text())
    default_prefix = Column(Text())
    default_range = Column(Text(), ForeignKey('type_definition.name'))
    metamodel_version = Column(Text())
    source_file = Column(Text())
    source_file_date = Column(DateTime())
    source_file_size = Column(Integer())
    generation_date = Column(DateTime())
    slot_names_unique = Column(Boolean())
    name = Column(Text(), primary_key=True, nullable=False )
    id_prefixes_are_closed = Column(Boolean())
    definition_uri = Column(Text())
    conforms_to = Column(Text())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
    
    
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
    
    
    # One-To-Many: OneToAnyMapping(source_class='schema_definition', source_slot='settings', mapping_type=None, target_class='setting', target_slot='schema_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    settings = relationship( "Setting", foreign_keys="[setting.schema_definition_name]")
    
    
    id_prefixes_rel = relationship( "SchemaDefinitionIdPrefixes" )
    id_prefixes = association_proxy("id_prefixes_rel", "id_prefixes",
                                  creator=lambda x_: SchemaDefinitionIdPrefixes(id_prefixes=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='schema_definition', source_slot='local_names', mapping_type=None, target_class='local_name', target_slot='schema_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    local_names = relationship( "LocalName", foreign_keys="[local_name.schema_definition_name]")
    
    
    implements_rel = relationship( "SchemaDefinitionImplements" )
    implements = association_proxy("implements_rel", "implements",
                                  creator=lambda x_: SchemaDefinitionImplements(implements=x_))
    
    
    instantiates_rel = relationship( "SchemaDefinitionInstantiates" )
    instantiates = association_proxy("instantiates_rel", "instantiates",
                                  creator=lambda x_: SchemaDefinitionInstantiates(instantiates=x_))
    
    
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
    
    
    aliases_rel = relationship( "SchemaDefinitionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: SchemaDefinitionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='schema_definition', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='schema_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.schema_definition_name]")
    
    
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
    
    
    contributors_rel = relationship( "SchemaDefinitionContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: SchemaDefinitionContributors(contributors=x_))
    
    
    categories_rel = relationship( "SchemaDefinitionCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: SchemaDefinitionCategory(category=x_))
    
    
    keywords_rel = relationship( "SchemaDefinitionKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: SchemaDefinitionKeyword(keyword=x_))
    

    def __repr__(self):
        return f"schema_definition(id={self.id},version={self.version},license={self.license},default_prefix={self.default_prefix},default_range={self.default_range},metamodel_version={self.metamodel_version},source_file={self.source_file},source_file_date={self.source_file_date},source_file_size={self.source_file_size},generation_date={self.generation_date},slot_names_unique={self.slot_names_unique},name={self.name},id_prefixes_are_closed={self.id_prefixes_are_closed},definition_uri={self.definition_uri},conforms_to={self.conforms_to},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},)"



    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class TypeExpression(Expression):
    """
    An abstract class grouping named types and anonymous type expressions
    """
    __tablename__ = 'type_expression'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    pattern = Column(Text())
    implicit_prefix = Column(Text())
    equals_string = Column(Text())
    equals_number = Column(Integer())
    structured_pattern_id = Column(Integer(), ForeignKey('pattern_expression.id'))
    structured_pattern = relationship("PatternExpression", uselist=False, foreign_keys=[structured_pattern_id])
    unit_id = Column(Integer(), ForeignKey('UnitOfMeasure.id'))
    unit = relationship("UnitOfMeasure", uselist=False, foreign_keys=[unit_id])
    minimum_value_id = Column(Integer(), ForeignKey('Anything.id'))
    minimum_value = relationship("Anything", uselist=False, foreign_keys=[minimum_value_id])
    maximum_value_id = Column(Integer(), ForeignKey('Anything.id'))
    maximum_value = relationship("Anything", uselist=False, foreign_keys=[maximum_value_id])
    
    
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
        return f"type_expression(id={self.id},pattern={self.pattern},implicit_prefix={self.implicit_prefix},equals_string={self.equals_string},equals_number={self.equals_number},structured_pattern_id={self.structured_pattern_id},unit_id={self.unit_id},minimum_value_id={self.minimum_value_id},maximum_value_id={self.maximum_value_id},)"



    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class TypeDefinition(Element):
    """
    an element that whose instances are atomic scalar values that can be mapped to primitive types
    """
    __tablename__ = 'type_definition'

    typeof = Column(Text(), ForeignKey('type_definition.name'))
    base = Column(Text())
    uri = Column(Text())
    repr = Column(Text())
    pattern = Column(Text())
    implicit_prefix = Column(Text())
    equals_string = Column(Text())
    equals_number = Column(Integer())
    name = Column(Text(), primary_key=True, nullable=False )
    id_prefixes_are_closed = Column(Boolean())
    definition_uri = Column(Text())
    conforms_to = Column(Text())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'))
    structured_pattern_id = Column(Integer(), ForeignKey('pattern_expression.id'))
    structured_pattern = relationship("PatternExpression", uselist=False, foreign_keys=[structured_pattern_id])
    unit_id = Column(Integer(), ForeignKey('UnitOfMeasure.id'))
    unit = relationship("UnitOfMeasure", uselist=False, foreign_keys=[unit_id])
    minimum_value_id = Column(Integer(), ForeignKey('Anything.id'))
    minimum_value = relationship("Anything", uselist=False, foreign_keys=[minimum_value_id])
    maximum_value_id = Column(Integer(), ForeignKey('Anything.id'))
    maximum_value = relationship("Anything", uselist=False, foreign_keys=[maximum_value_id])
    
    
    # ManyToMany
    union_of = relationship( "TypeDefinition", secondary="type_definition_union_of")
    
    
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
    
    
    # One-To-Many: OneToAnyMapping(source_class='type_definition', source_slot='local_names', mapping_type=None, target_class='local_name', target_slot='type_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    local_names = relationship( "LocalName", foreign_keys="[local_name.type_definition_name]")
    
    
    implements_rel = relationship( "TypeDefinitionImplements" )
    implements = association_proxy("implements_rel", "implements",
                                  creator=lambda x_: TypeDefinitionImplements(implements=x_))
    
    
    instantiates_rel = relationship( "TypeDefinitionInstantiates" )
    instantiates = association_proxy("instantiates_rel", "instantiates",
                                  creator=lambda x_: TypeDefinitionInstantiates(instantiates=x_))
    
    
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
    
    
    aliases_rel = relationship( "TypeDefinitionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: TypeDefinitionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='type_definition', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='type_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.type_definition_name]")
    
    
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
    
    
    contributors_rel = relationship( "TypeDefinitionContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: TypeDefinitionContributors(contributors=x_))
    
    
    categories_rel = relationship( "TypeDefinitionCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: TypeDefinitionCategory(category=x_))
    
    
    keywords_rel = relationship( "TypeDefinitionKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: TypeDefinitionKeyword(keyword=x_))
    

    def __repr__(self):
        return f"type_definition(typeof={self.typeof},base={self.base},uri={self.uri},repr={self.repr},pattern={self.pattern},implicit_prefix={self.implicit_prefix},equals_string={self.equals_string},equals_number={self.equals_number},name={self.name},id_prefixes_are_closed={self.id_prefixes_are_closed},definition_uri={self.definition_uri},conforms_to={self.conforms_to},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},schema_definition_name={self.schema_definition_name},structured_pattern_id={self.structured_pattern_id},unit_id={self.unit_id},minimum_value_id={self.minimum_value_id},maximum_value_id={self.maximum_value_id},)"



    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class SubsetDefinition(Element):
    """
    an element that can be used to group other metamodel elements
    """
    __tablename__ = 'subset_definition'

    name = Column(Text(), primary_key=True, nullable=False )
    id_prefixes_are_closed = Column(Boolean())
    definition_uri = Column(Text())
    conforms_to = Column(Text())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'))
    
    
    id_prefixes_rel = relationship( "SubsetDefinitionIdPrefixes" )
    id_prefixes = association_proxy("id_prefixes_rel", "id_prefixes",
                                  creator=lambda x_: SubsetDefinitionIdPrefixes(id_prefixes=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='subset_definition', source_slot='local_names', mapping_type=None, target_class='local_name', target_slot='subset_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    local_names = relationship( "LocalName", foreign_keys="[local_name.subset_definition_name]")
    
    
    implements_rel = relationship( "SubsetDefinitionImplements" )
    implements = association_proxy("implements_rel", "implements",
                                  creator=lambda x_: SubsetDefinitionImplements(implements=x_))
    
    
    instantiates_rel = relationship( "SubsetDefinitionInstantiates" )
    instantiates = association_proxy("instantiates_rel", "instantiates",
                                  creator=lambda x_: SubsetDefinitionInstantiates(instantiates=x_))
    
    
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
    
    
    aliases_rel = relationship( "SubsetDefinitionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: SubsetDefinitionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='subset_definition', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='subset_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.subset_definition_name]")
    
    
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
    
    
    contributors_rel = relationship( "SubsetDefinitionContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: SubsetDefinitionContributors(contributors=x_))
    
    
    categories_rel = relationship( "SubsetDefinitionCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: SubsetDefinitionCategory(category=x_))
    
    
    keywords_rel = relationship( "SubsetDefinitionKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: SubsetDefinitionKeyword(keyword=x_))
    

    def __repr__(self):
        return f"subset_definition(name={self.name},id_prefixes_are_closed={self.id_prefixes_are_closed},definition_uri={self.definition_uri},conforms_to={self.conforms_to},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},schema_definition_name={self.schema_definition_name},)"



    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class Definition(Element):
    """
    abstract base class for core metaclasses
    """
    __tablename__ = 'definition'

    is_a = Column(Text(), ForeignKey('definition.name'))
    abstract = Column(Boolean())
    mixin = Column(Boolean())
    string_serialization = Column(Text())
    name = Column(Text(), primary_key=True, nullable=False )
    id_prefixes_are_closed = Column(Boolean())
    definition_uri = Column(Text())
    conforms_to = Column(Text())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
    
    
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
    
    
    # One-To-Many: OneToAnyMapping(source_class='definition', source_slot='local_names', mapping_type=None, target_class='local_name', target_slot='definition_name', join_class=None, uses_join_table=None, multivalued=False)
    local_names = relationship( "LocalName", foreign_keys="[local_name.definition_name]")
    
    
    implements_rel = relationship( "DefinitionImplements" )
    implements = association_proxy("implements_rel", "implements",
                                  creator=lambda x_: DefinitionImplements(implements=x_))
    
    
    instantiates_rel = relationship( "DefinitionInstantiates" )
    instantiates = association_proxy("instantiates_rel", "instantiates",
                                  creator=lambda x_: DefinitionInstantiates(instantiates=x_))
    
    
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
    
    
    aliases_rel = relationship( "DefinitionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: DefinitionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='definition', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='definition_name', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.definition_name]")
    
    
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
    
    
    contributors_rel = relationship( "DefinitionContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: DefinitionContributors(contributors=x_))
    
    
    categories_rel = relationship( "DefinitionCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: DefinitionCategory(category=x_))
    
    
    keywords_rel = relationship( "DefinitionKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: DefinitionKeyword(keyword=x_))
    

    def __repr__(self):
        return f"definition(is_a={self.is_a},abstract={self.abstract},mixin={self.mixin},string_serialization={self.string_serialization},name={self.name},id_prefixes_are_closed={self.id_prefixes_are_closed},definition_uri={self.definition_uri},conforms_to={self.conforms_to},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},)"



    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class EnumExpression(Expression):
    """
    An expression that constrains the range of a slot
    """
    __tablename__ = 'enum_expression'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    code_set = Column(Text())
    code_set_tag = Column(Text())
    code_set_version = Column(Text())
    pv_formula = Column(Enum('CODE', 'CURIE', 'URI', 'FHIR_CODING', 'LABEL', name='pv_formula_options'))
    reachable_from_id = Column(Integer(), ForeignKey('reachability_query.id'))
    reachable_from = relationship("ReachabilityQuery", uselist=False, foreign_keys=[reachable_from_id])
    matches_id = Column(Integer(), ForeignKey('match_query.id'))
    matches = relationship("MatchQuery", uselist=False, foreign_keys=[matches_id])
    
    
    # One-To-Many: OneToAnyMapping(source_class='enum_expression', source_slot='permissible_values', mapping_type=None, target_class='permissible_value', target_slot='enum_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    permissible_values = relationship( "PermissibleValue", foreign_keys="[permissible_value.enum_expression_id]")
    
    
    # ManyToMany
    include = relationship( "AnonymousEnumExpression", secondary="enum_expression_include")
    
    
    # ManyToMany
    minus = relationship( "AnonymousEnumExpression", secondary="enum_expression_minus")
    
    
    # ManyToMany
    inherits = relationship( "EnumDefinition", secondary="enum_expression_inherits")
    
    
    concepts_rel = relationship( "EnumExpressionConcepts" )
    concepts = association_proxy("concepts_rel", "concepts",
                                  creator=lambda x_: EnumExpressionConcepts(concepts=x_))
    

    def __repr__(self):
        return f"enum_expression(id={self.id},code_set={self.code_set},code_set_tag={self.code_set_tag},code_set_version={self.code_set_version},pv_formula={self.pv_formula},reachable_from_id={self.reachable_from_id},matches_id={self.matches_id},)"



    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class SlotExpression(Expression):
    """
    an expression that constrains the range of values a slot can take
    """
    __tablename__ = 'slot_expression'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    range = Column(Text(), ForeignKey('element.name'))
    required = Column(Boolean())
    recommended = Column(Boolean())
    inlined = Column(Boolean())
    inlined_as_list = Column(Boolean())
    pattern = Column(Text())
    implicit_prefix = Column(Text())
    value_presence = Column(Enum('UNCOMMITTED', 'PRESENT', 'ABSENT', name='presence_enum'))
    equals_string = Column(Text())
    equals_number = Column(Integer())
    equals_expression = Column(Text())
    exact_cardinality = Column(Integer())
    minimum_cardinality = Column(Integer())
    maximum_cardinality = Column(Integer())
    range_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'))
    range_expression = relationship("AnonymousClassExpression", uselist=False, foreign_keys=[range_expression_id])
    enum_range_id = Column(Integer(), ForeignKey('enum_expression.id'))
    enum_range = relationship("EnumExpression", uselist=False, foreign_keys=[enum_range_id])
    minimum_value_id = Column(Integer(), ForeignKey('Anything.id'))
    minimum_value = relationship("Anything", uselist=False, foreign_keys=[minimum_value_id])
    maximum_value_id = Column(Integer(), ForeignKey('Anything.id'))
    maximum_value = relationship("Anything", uselist=False, foreign_keys=[maximum_value_id])
    structured_pattern_id = Column(Integer(), ForeignKey('pattern_expression.id'))
    structured_pattern = relationship("PatternExpression", uselist=False, foreign_keys=[structured_pattern_id])
    unit_id = Column(Integer(), ForeignKey('UnitOfMeasure.id'))
    unit = relationship("UnitOfMeasure", uselist=False, foreign_keys=[unit_id])
    has_member_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'))
    has_member = relationship("AnonymousSlotExpression", uselist=False, foreign_keys=[has_member_id])
    all_members_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'))
    all_members = relationship("AnonymousSlotExpression", uselist=False, foreign_keys=[all_members_id])
    
    
    equals_string_in_rel = relationship( "SlotExpressionEqualsStringIn" )
    equals_string_in = association_proxy("equals_string_in_rel", "equals_string_in",
                                  creator=lambda x_: SlotExpressionEqualsStringIn(equals_string_in=x_))
    
    
    # ManyToMany
    none_of = relationship( "AnonymousSlotExpression", secondary="slot_expression_none_of")
    
    
    # ManyToMany
    exactly_one_of = relationship( "AnonymousSlotExpression", secondary="slot_expression_exactly_one_of")
    
    
    # ManyToMany
    any_of = relationship( "AnonymousSlotExpression", secondary="slot_expression_any_of")
    
    
    # ManyToMany
    all_of = relationship( "AnonymousSlotExpression", secondary="slot_expression_all_of")
    

    def __repr__(self):
        return f"slot_expression(id={self.id},range={self.range},required={self.required},recommended={self.recommended},inlined={self.inlined},inlined_as_list={self.inlined_as_list},pattern={self.pattern},implicit_prefix={self.implicit_prefix},value_presence={self.value_presence},equals_string={self.equals_string},equals_number={self.equals_number},equals_expression={self.equals_expression},exact_cardinality={self.exact_cardinality},minimum_cardinality={self.minimum_cardinality},maximum_cardinality={self.maximum_cardinality},range_expression_id={self.range_expression_id},enum_range_id={self.enum_range_id},minimum_value_id={self.minimum_value_id},maximum_value_id={self.maximum_value_id},structured_pattern_id={self.structured_pattern_id},unit_id={self.unit_id},has_member_id={self.has_member_id},all_members_id={self.all_members_id},)"



    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class AnonymousSlotExpression(AnonymousExpression):
    """
    
    """
    __tablename__ = 'anonymous_slot_expression'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    range = Column(Text(), ForeignKey('element.name'))
    required = Column(Boolean())
    recommended = Column(Boolean())
    inlined = Column(Boolean())
    inlined_as_list = Column(Boolean())
    pattern = Column(Text())
    implicit_prefix = Column(Text())
    value_presence = Column(Enum('UNCOMMITTED', 'PRESENT', 'ABSENT', name='presence_enum'))
    equals_string = Column(Text())
    equals_number = Column(Integer())
    equals_expression = Column(Text())
    exact_cardinality = Column(Integer())
    minimum_cardinality = Column(Integer())
    maximum_cardinality = Column(Integer())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
    range_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'))
    range_expression = relationship("AnonymousClassExpression", uselist=False, foreign_keys=[range_expression_id])
    enum_range_id = Column(Integer(), ForeignKey('enum_expression.id'))
    enum_range = relationship("EnumExpression", uselist=False, foreign_keys=[enum_range_id])
    minimum_value_id = Column(Integer(), ForeignKey('Anything.id'))
    minimum_value = relationship("Anything", uselist=False, foreign_keys=[minimum_value_id])
    maximum_value_id = Column(Integer(), ForeignKey('Anything.id'))
    maximum_value = relationship("Anything", uselist=False, foreign_keys=[maximum_value_id])
    structured_pattern_id = Column(Integer(), ForeignKey('pattern_expression.id'))
    structured_pattern = relationship("PatternExpression", uselist=False, foreign_keys=[structured_pattern_id])
    unit_id = Column(Integer(), ForeignKey('UnitOfMeasure.id'))
    unit = relationship("UnitOfMeasure", uselist=False, foreign_keys=[unit_id])
    has_member_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'))
    has_member = relationship("AnonymousSlotExpression", uselist=False, foreign_keys=[has_member_id])
    all_members_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'))
    all_members = relationship("AnonymousSlotExpression", uselist=False, foreign_keys=[all_members_id])
    
    
    equals_string_in_rel = relationship( "AnonymousSlotExpressionEqualsStringIn" )
    equals_string_in = association_proxy("equals_string_in_rel", "equals_string_in",
                                  creator=lambda x_: AnonymousSlotExpressionEqualsStringIn(equals_string_in=x_))
    
    
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
    
    
    aliases_rel = relationship( "AnonymousSlotExpressionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: AnonymousSlotExpressionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_slot_expression', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='anonymous_slot_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.anonymous_slot_expression_id]")
    
    
    mappings_rel = relationship( "AnonymousSlotExpressionMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: AnonymousSlotExpressionMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "AnonymousSlotExpressionExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: AnonymousSlotExpressionExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "AnonymousSlotExpressionCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: AnonymousSlotExpressionCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "AnonymousSlotExpressionRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: AnonymousSlotExpressionRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "AnonymousSlotExpressionNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: AnonymousSlotExpressionNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "AnonymousSlotExpressionBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: AnonymousSlotExpressionBroadMappings(broad_mappings=x_))
    
    
    contributors_rel = relationship( "AnonymousSlotExpressionContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: AnonymousSlotExpressionContributors(contributors=x_))
    
    
    categories_rel = relationship( "AnonymousSlotExpressionCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: AnonymousSlotExpressionCategory(category=x_))
    
    
    keywords_rel = relationship( "AnonymousSlotExpressionKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: AnonymousSlotExpressionKeyword(keyword=x_))
    

    def __repr__(self):
        return f"anonymous_slot_expression(id={self.id},range={self.range},required={self.required},recommended={self.recommended},inlined={self.inlined},inlined_as_list={self.inlined_as_list},pattern={self.pattern},implicit_prefix={self.implicit_prefix},value_presence={self.value_presence},equals_string={self.equals_string},equals_number={self.equals_number},equals_expression={self.equals_expression},exact_cardinality={self.exact_cardinality},minimum_cardinality={self.minimum_cardinality},maximum_cardinality={self.maximum_cardinality},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},range_expression_id={self.range_expression_id},enum_range_id={self.enum_range_id},minimum_value_id={self.minimum_value_id},maximum_value_id={self.maximum_value_id},structured_pattern_id={self.structured_pattern_id},unit_id={self.unit_id},has_member_id={self.has_member_id},all_members_id={self.all_members_id},)"



    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class AnonymousClassExpression(AnonymousExpression):
    """
    
    """
    __tablename__ = 'anonymous_class_expression'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    is_a = Column(Text(), ForeignKey('definition.name'))
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
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
    
    
    aliases_rel = relationship( "AnonymousClassExpressionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: AnonymousClassExpressionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='anonymous_class_expression', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='anonymous_class_expression_id', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.anonymous_class_expression_id]")
    
    
    mappings_rel = relationship( "AnonymousClassExpressionMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: AnonymousClassExpressionMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "AnonymousClassExpressionExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: AnonymousClassExpressionExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "AnonymousClassExpressionCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: AnonymousClassExpressionCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "AnonymousClassExpressionRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: AnonymousClassExpressionRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "AnonymousClassExpressionNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: AnonymousClassExpressionNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "AnonymousClassExpressionBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: AnonymousClassExpressionBroadMappings(broad_mappings=x_))
    
    
    contributors_rel = relationship( "AnonymousClassExpressionContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: AnonymousClassExpressionContributors(contributors=x_))
    
    
    categories_rel = relationship( "AnonymousClassExpressionCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: AnonymousClassExpressionCategory(category=x_))
    
    
    keywords_rel = relationship( "AnonymousClassExpressionKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: AnonymousClassExpressionKeyword(keyword=x_))
    

    def __repr__(self):
        return f"anonymous_class_expression(id={self.id},is_a={self.is_a},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},class_definition_name={self.class_definition_name},)"



    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class ClassRule(ClassLevelRule):
    """
    A rule that applies to instances of a class
    """
    __tablename__ = 'class_rule'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    bidirectional = Column(Boolean())
    open_world = Column(Boolean())
    rank = Column(Integer())
    deactivated = Column(Boolean())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'))
    preconditions_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'))
    preconditions = relationship("AnonymousClassExpression", uselist=False, foreign_keys=[preconditions_id])
    postconditions_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'))
    postconditions = relationship("AnonymousClassExpression", uselist=False, foreign_keys=[postconditions_id])
    elseconditions_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'))
    elseconditions = relationship("AnonymousClassExpression", uselist=False, foreign_keys=[elseconditions_id])
    
    
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
    
    
    aliases_rel = relationship( "ClassRuleAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: ClassRuleAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_rule', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='class_rule_id', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.class_rule_id]")
    
    
    mappings_rel = relationship( "ClassRuleMappings" )
    mappings = association_proxy("mappings_rel", "mappings",
                                  creator=lambda x_: ClassRuleMappings(mappings=x_))
    
    
    exact_mappings_rel = relationship( "ClassRuleExactMappings" )
    exact_mappings = association_proxy("exact_mappings_rel", "exact_mappings",
                                  creator=lambda x_: ClassRuleExactMappings(exact_mappings=x_))
    
    
    close_mappings_rel = relationship( "ClassRuleCloseMappings" )
    close_mappings = association_proxy("close_mappings_rel", "close_mappings",
                                  creator=lambda x_: ClassRuleCloseMappings(close_mappings=x_))
    
    
    related_mappings_rel = relationship( "ClassRuleRelatedMappings" )
    related_mappings = association_proxy("related_mappings_rel", "related_mappings",
                                  creator=lambda x_: ClassRuleRelatedMappings(related_mappings=x_))
    
    
    narrow_mappings_rel = relationship( "ClassRuleNarrowMappings" )
    narrow_mappings = association_proxy("narrow_mappings_rel", "narrow_mappings",
                                  creator=lambda x_: ClassRuleNarrowMappings(narrow_mappings=x_))
    
    
    broad_mappings_rel = relationship( "ClassRuleBroadMappings" )
    broad_mappings = association_proxy("broad_mappings_rel", "broad_mappings",
                                  creator=lambda x_: ClassRuleBroadMappings(broad_mappings=x_))
    
    
    contributors_rel = relationship( "ClassRuleContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: ClassRuleContributors(contributors=x_))
    
    
    categories_rel = relationship( "ClassRuleCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: ClassRuleCategory(category=x_))
    
    
    keywords_rel = relationship( "ClassRuleKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: ClassRuleKeyword(keyword=x_))
    

    def __repr__(self):
        return f"class_rule(id={self.id},bidirectional={self.bidirectional},open_world={self.open_world},rank={self.rank},deactivated={self.deactivated},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},class_definition_name={self.class_definition_name},preconditions_id={self.preconditions_id},postconditions_id={self.postconditions_id},elseconditions_id={self.elseconditions_id},)"



    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class Annotation(Extension):
    """
    a tag/value pair with the semantics of OWL Annotation
    """
    __tablename__ = 'annotation'

    tag = Column(Text(), primary_key=True, nullable=False )
    element_name = Column(Text(), ForeignKey('element.name'), primary_key=True)
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'), primary_key=True)
    type_definition_name = Column(Text(), ForeignKey('type_definition.name'), primary_key=True)
    subset_definition_name = Column(Text(), ForeignKey('subset_definition.name'), primary_key=True)
    definition_name = Column(Text(), ForeignKey('definition.name'), primary_key=True)
    enum_definition_name = Column(Text(), ForeignKey('enum_definition.name'), primary_key=True)
    structured_alias_id = Column(Integer(), ForeignKey('structured_alias.id'), primary_key=True)
    anonymous_expression_id = Column(Integer(), ForeignKey('anonymous_expression.id'), primary_key=True)
    path_expression_id = Column(Integer(), ForeignKey('path_expression.id'), primary_key=True)
    anonymous_slot_expression_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'), primary_key=True)
    slot_definition_name = Column(Text(), ForeignKey('slot_definition.name'), primary_key=True)
    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'), primary_key=True)
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'), primary_key=True)
    class_rule_id = Column(Integer(), ForeignKey('class_rule.id'), primary_key=True)
    array_expression_id = Column(Integer(), ForeignKey('array_expression.id'), primary_key=True)
    dimension_expression_id = Column(Integer(), ForeignKey('dimension_expression.id'), primary_key=True)
    pattern_expression_id = Column(Integer(), ForeignKey('pattern_expression.id'), primary_key=True)
    import_expression_id = Column(Integer(), ForeignKey('import_expression.id'), primary_key=True)
    permissible_value_text = Column(Text(), ForeignKey('permissible_value.text'), primary_key=True)
    unique_key_unique_key_name = Column(Text(), ForeignKey('unique_key.unique_key_name'), primary_key=True)
    annotatable_id = Column(Integer(), ForeignKey('annotatable.id'), primary_key=True)
    annotation_tag = Column(Text(), ForeignKey('annotation.tag'), primary_key=True)
    value_id = Column(Integer(), ForeignKey('AnyValue.id'), primary_key=True, nullable=False )
    value = relationship("AnyValue", uselist=False, foreign_keys=[value_id])
    
    
    # One-To-Many: OneToAnyMapping(source_class='annotation', source_slot='annotations', mapping_type=None, target_class='annotation', target_slot='annotation_tag', join_class=None, uses_join_table=None, multivalued=False)
    annotations = relationship( "Annotation", foreign_keys="[annotation.annotation_tag]")
    
    
    # One-To-Many: OneToAnyMapping(source_class='annotation', source_slot='extensions', mapping_type=None, target_class='extension', target_slot='annotation_tag', join_class=None, uses_join_table=None, multivalued=False)
    extensions = relationship( "Extension", foreign_keys="[extension.annotation_tag]")
    

    def __repr__(self):
        return f"annotation(tag={self.tag},element_name={self.element_name},schema_definition_name={self.schema_definition_name},type_definition_name={self.type_definition_name},subset_definition_name={self.subset_definition_name},definition_name={self.definition_name},enum_definition_name={self.enum_definition_name},structured_alias_id={self.structured_alias_id},anonymous_expression_id={self.anonymous_expression_id},path_expression_id={self.path_expression_id},anonymous_slot_expression_id={self.anonymous_slot_expression_id},slot_definition_name={self.slot_definition_name},anonymous_class_expression_id={self.anonymous_class_expression_id},class_definition_name={self.class_definition_name},class_rule_id={self.class_rule_id},array_expression_id={self.array_expression_id},dimension_expression_id={self.dimension_expression_id},pattern_expression_id={self.pattern_expression_id},import_expression_id={self.import_expression_id},permissible_value_text={self.permissible_value_text},unique_key_unique_key_name={self.unique_key_unique_key_name},annotatable_id={self.annotatable_id},annotation_tag={self.annotation_tag},value_id={self.value_id},)"



    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class EnumDefinition(Definition):
    """
    an element whose instances must be drawn from a specified set of permissible values
    """
    __tablename__ = 'enum_definition'

    enum_uri = Column(Text())
    code_set = Column(Text())
    code_set_tag = Column(Text())
    code_set_version = Column(Text())
    pv_formula = Column(Enum('CODE', 'CURIE', 'URI', 'FHIR_CODING', 'LABEL', name='pv_formula_options'))
    is_a = Column(Text(), ForeignKey('definition.name'))
    abstract = Column(Boolean())
    mixin = Column(Boolean())
    string_serialization = Column(Text())
    name = Column(Text(), primary_key=True, nullable=False )
    id_prefixes_are_closed = Column(Boolean())
    definition_uri = Column(Text())
    conforms_to = Column(Text())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'))
    reachable_from_id = Column(Integer(), ForeignKey('reachability_query.id'))
    reachable_from = relationship("ReachabilityQuery", uselist=False, foreign_keys=[reachable_from_id])
    matches_id = Column(Integer(), ForeignKey('match_query.id'))
    matches = relationship("MatchQuery", uselist=False, foreign_keys=[matches_id])
    
    
    # One-To-Many: OneToAnyMapping(source_class='enum_definition', source_slot='permissible_values', mapping_type=None, target_class='permissible_value', target_slot='enum_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    permissible_values = relationship( "PermissibleValue", foreign_keys="[permissible_value.enum_definition_name]")
    
    
    # ManyToMany
    include = relationship( "AnonymousEnumExpression", secondary="enum_definition_include")
    
    
    # ManyToMany
    minus = relationship( "AnonymousEnumExpression", secondary="enum_definition_minus")
    
    
    # ManyToMany
    inherits = relationship( "EnumDefinition", secondary="enum_definition_inherits")
    
    
    concepts_rel = relationship( "EnumDefinitionConcepts" )
    concepts = association_proxy("concepts_rel", "concepts",
                                  creator=lambda x_: EnumDefinitionConcepts(concepts=x_))
    
    
    # ManyToMany
    mixins = relationship( "Definition", secondary="enum_definition_mixins")
    
    
    # ManyToMany
    apply_to = relationship( "Definition", secondary="enum_definition_apply_to")
    
    
    values_from_rel = relationship( "EnumDefinitionValuesFrom" )
    values_from = association_proxy("values_from_rel", "values_from",
                                  creator=lambda x_: EnumDefinitionValuesFrom(values_from=x_))
    
    
    id_prefixes_rel = relationship( "EnumDefinitionIdPrefixes" )
    id_prefixes = association_proxy("id_prefixes_rel", "id_prefixes",
                                  creator=lambda x_: EnumDefinitionIdPrefixes(id_prefixes=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='enum_definition', source_slot='local_names', mapping_type=None, target_class='local_name', target_slot='enum_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    local_names = relationship( "LocalName", foreign_keys="[local_name.enum_definition_name]")
    
    
    implements_rel = relationship( "EnumDefinitionImplements" )
    implements = association_proxy("implements_rel", "implements",
                                  creator=lambda x_: EnumDefinitionImplements(implements=x_))
    
    
    instantiates_rel = relationship( "EnumDefinitionInstantiates" )
    instantiates = association_proxy("instantiates_rel", "instantiates",
                                  creator=lambda x_: EnumDefinitionInstantiates(instantiates=x_))
    
    
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
    
    
    aliases_rel = relationship( "EnumDefinitionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: EnumDefinitionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='enum_definition', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='enum_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.enum_definition_name]")
    
    
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
    
    
    contributors_rel = relationship( "EnumDefinitionContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: EnumDefinitionContributors(contributors=x_))
    
    
    categories_rel = relationship( "EnumDefinitionCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: EnumDefinitionCategory(category=x_))
    
    
    keywords_rel = relationship( "EnumDefinitionKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: EnumDefinitionKeyword(keyword=x_))
    

    def __repr__(self):
        return f"enum_definition(enum_uri={self.enum_uri},code_set={self.code_set},code_set_tag={self.code_set_tag},code_set_version={self.code_set_version},pv_formula={self.pv_formula},is_a={self.is_a},abstract={self.abstract},mixin={self.mixin},string_serialization={self.string_serialization},name={self.name},id_prefixes_are_closed={self.id_prefixes_are_closed},definition_uri={self.definition_uri},conforms_to={self.conforms_to},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},schema_definition_name={self.schema_definition_name},reachable_from_id={self.reachable_from_id},matches_id={self.matches_id},)"



    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class SlotDefinition(Definition):
    """
    an element that describes how instances are related to other instances
    """
    __tablename__ = 'slot_definition'

    singular_name = Column(Text())
    domain = Column(Text(), ForeignKey('class_definition.name'))
    slot_uri = Column(Text())
    multivalued = Column(Boolean())
    inherited = Column(Boolean())
    readonly = Column(Text())
    ifabsent = Column(Text())
    list_elements_unique = Column(Boolean())
    list_elements_ordered = Column(Boolean())
    shared = Column(Boolean())
    key = Column(Boolean())
    identifier = Column(Boolean())
    designates_type = Column(Boolean())
    alias = Column(Text())
    owner = Column(Text(), ForeignKey('definition.name'))
    subproperty_of = Column(Text(), ForeignKey('slot_definition.name'))
    symmetric = Column(Boolean())
    reflexive = Column(Boolean())
    locally_reflexive = Column(Boolean())
    irreflexive = Column(Boolean())
    asymmetric = Column(Boolean())
    transitive = Column(Boolean())
    inverse = Column(Text(), ForeignKey('slot_definition.name'))
    is_class_field = Column(Boolean())
    transitive_form_of = Column(Text(), ForeignKey('slot_definition.name'))
    reflexive_transitive_form_of = Column(Text(), ForeignKey('slot_definition.name'))
    role = Column(Text())
    is_usage_slot = Column(Boolean())
    usage_slot_name = Column(Text())
    relational_role = Column(Enum('SUBJECT', 'OBJECT', 'PREDICATE', 'NODE', 'OTHER_ROLE', name='relational_role_enum'))
    slot_group = Column(Text(), ForeignKey('slot_definition.name'))
    is_grouping_slot = Column(Boolean())
    children_are_mutually_disjoint = Column(Boolean())
    range = Column(Text(), ForeignKey('element.name'))
    required = Column(Boolean())
    recommended = Column(Boolean())
    inlined = Column(Boolean())
    inlined_as_list = Column(Boolean())
    pattern = Column(Text())
    implicit_prefix = Column(Text())
    value_presence = Column(Enum('UNCOMMITTED', 'PRESENT', 'ABSENT', name='presence_enum'))
    equals_string = Column(Text())
    equals_number = Column(Integer())
    equals_expression = Column(Text())
    exact_cardinality = Column(Integer())
    minimum_cardinality = Column(Integer())
    maximum_cardinality = Column(Integer())
    is_a = Column(Text(), ForeignKey('slot_definition.name'))
    abstract = Column(Boolean())
    mixin = Column(Boolean())
    string_serialization = Column(Text())
    name = Column(Text(), primary_key=True, nullable=False )
    id_prefixes_are_closed = Column(Boolean())
    definition_uri = Column(Text())
    conforms_to = Column(Text())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
    schema_definition_name = Column(Text(), ForeignKey('schema_definition.name'))
    class_expression_id = Column(Integer(), ForeignKey('class_expression.id'))
    anonymous_class_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'))
    class_definition_name = Column(Text(), ForeignKey('class_definition.name'))
    array_id = Column(Integer(), ForeignKey('array_expression.id'))
    array = relationship("ArrayExpression", uselist=False, foreign_keys=[array_id])
    path_rule_id = Column(Integer(), ForeignKey('path_expression.id'))
    path_rule = relationship("PathExpression", uselist=False, foreign_keys=[path_rule_id])
    range_expression_id = Column(Integer(), ForeignKey('anonymous_class_expression.id'))
    range_expression = relationship("AnonymousClassExpression", uselist=False, foreign_keys=[range_expression_id])
    enum_range_id = Column(Integer(), ForeignKey('enum_expression.id'))
    enum_range = relationship("EnumExpression", uselist=False, foreign_keys=[enum_range_id])
    minimum_value_id = Column(Integer(), ForeignKey('Anything.id'))
    minimum_value = relationship("Anything", uselist=False, foreign_keys=[minimum_value_id])
    maximum_value_id = Column(Integer(), ForeignKey('Anything.id'))
    maximum_value = relationship("Anything", uselist=False, foreign_keys=[maximum_value_id])
    structured_pattern_id = Column(Integer(), ForeignKey('pattern_expression.id'))
    structured_pattern = relationship("PatternExpression", uselist=False, foreign_keys=[structured_pattern_id])
    unit_id = Column(Integer(), ForeignKey('UnitOfMeasure.id'))
    unit = relationship("UnitOfMeasure", uselist=False, foreign_keys=[unit_id])
    has_member_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'))
    has_member = relationship("AnonymousSlotExpression", uselist=False, foreign_keys=[has_member_id])
    all_members_id = Column(Integer(), ForeignKey('anonymous_slot_expression.id'))
    all_members = relationship("AnonymousSlotExpression", uselist=False, foreign_keys=[all_members_id])
    
    
    # ManyToMany
    domain_of = relationship( "ClassDefinition", secondary="slot_definition_domain_of")
    
    
    # ManyToMany
    disjoint_with = relationship( "SlotDefinition", secondary="slot_definition_disjoint_with")
    
    
    # ManyToMany
    union_of = relationship( "SlotDefinition", secondary="slot_definition_union_of")
    
    
    equals_string_in_rel = relationship( "SlotDefinitionEqualsStringIn" )
    equals_string_in = association_proxy("equals_string_in_rel", "equals_string_in",
                                  creator=lambda x_: SlotDefinitionEqualsStringIn(equals_string_in=x_))
    
    
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
    
    
    # One-To-Many: OneToAnyMapping(source_class='slot_definition', source_slot='local_names', mapping_type=None, target_class='local_name', target_slot='slot_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    local_names = relationship( "LocalName", foreign_keys="[local_name.slot_definition_name]")
    
    
    implements_rel = relationship( "SlotDefinitionImplements" )
    implements = association_proxy("implements_rel", "implements",
                                  creator=lambda x_: SlotDefinitionImplements(implements=x_))
    
    
    instantiates_rel = relationship( "SlotDefinitionInstantiates" )
    instantiates = association_proxy("instantiates_rel", "instantiates",
                                  creator=lambda x_: SlotDefinitionInstantiates(instantiates=x_))
    
    
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
    
    
    aliases_rel = relationship( "SlotDefinitionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: SlotDefinitionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='slot_definition', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='slot_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.slot_definition_name]")
    
    
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
    
    
    contributors_rel = relationship( "SlotDefinitionContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: SlotDefinitionContributors(contributors=x_))
    
    
    categories_rel = relationship( "SlotDefinitionCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: SlotDefinitionCategory(category=x_))
    
    
    keywords_rel = relationship( "SlotDefinitionKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: SlotDefinitionKeyword(keyword=x_))
    

    def __repr__(self):
        return f"slot_definition(singular_name={self.singular_name},domain={self.domain},slot_uri={self.slot_uri},multivalued={self.multivalued},inherited={self.inherited},readonly={self.readonly},ifabsent={self.ifabsent},list_elements_unique={self.list_elements_unique},list_elements_ordered={self.list_elements_ordered},shared={self.shared},key={self.key},identifier={self.identifier},designates_type={self.designates_type},alias={self.alias},owner={self.owner},subproperty_of={self.subproperty_of},symmetric={self.symmetric},reflexive={self.reflexive},locally_reflexive={self.locally_reflexive},irreflexive={self.irreflexive},asymmetric={self.asymmetric},transitive={self.transitive},inverse={self.inverse},is_class_field={self.is_class_field},transitive_form_of={self.transitive_form_of},reflexive_transitive_form_of={self.reflexive_transitive_form_of},role={self.role},is_usage_slot={self.is_usage_slot},usage_slot_name={self.usage_slot_name},relational_role={self.relational_role},slot_group={self.slot_group},is_grouping_slot={self.is_grouping_slot},children_are_mutually_disjoint={self.children_are_mutually_disjoint},range={self.range},required={self.required},recommended={self.recommended},inlined={self.inlined},inlined_as_list={self.inlined_as_list},pattern={self.pattern},implicit_prefix={self.implicit_prefix},value_presence={self.value_presence},equals_string={self.equals_string},equals_number={self.equals_number},equals_expression={self.equals_expression},exact_cardinality={self.exact_cardinality},minimum_cardinality={self.minimum_cardinality},maximum_cardinality={self.maximum_cardinality},is_a={self.is_a},abstract={self.abstract},mixin={self.mixin},string_serialization={self.string_serialization},name={self.name},id_prefixes_are_closed={self.id_prefixes_are_closed},definition_uri={self.definition_uri},conforms_to={self.conforms_to},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},schema_definition_name={self.schema_definition_name},class_expression_id={self.class_expression_id},anonymous_class_expression_id={self.anonymous_class_expression_id},class_definition_name={self.class_definition_name},array_id={self.array_id},path_rule_id={self.path_rule_id},range_expression_id={self.range_expression_id},enum_range_id={self.enum_range_id},minimum_value_id={self.minimum_value_id},maximum_value_id={self.maximum_value_id},structured_pattern_id={self.structured_pattern_id},unit_id={self.unit_id},has_member_id={self.has_member_id},all_members_id={self.all_members_id},)"



    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    


class ClassDefinition(Definition):
    """
    an element whose instances are complex objects that may have slot-value assignments
    """
    __tablename__ = 'class_definition'

    class_uri = Column(Text())
    subclass_of = Column(Text())
    tree_root = Column(Boolean())
    slot_names_unique = Column(Boolean())
    represents_relationship = Column(Boolean())
    children_are_mutually_disjoint = Column(Boolean())
    is_a = Column(Text(), ForeignKey('class_definition.name'))
    abstract = Column(Boolean())
    mixin = Column(Boolean())
    string_serialization = Column(Text())
    name = Column(Text(), primary_key=True, nullable=False )
    id_prefixes_are_closed = Column(Boolean())
    definition_uri = Column(Text())
    conforms_to = Column(Text())
    description = Column(Text())
    title = Column(Text())
    deprecated = Column(Text())
    from_schema = Column(Text())
    imported_from = Column(Text())
    source = Column(Text())
    in_language = Column(Text())
    deprecated_element_has_exact_replacement = Column(Text())
    deprecated_element_has_possible_replacement = Column(Text())
    created_by = Column(Text())
    created_on = Column(DateTime())
    last_updated_on = Column(DateTime())
    modified_by = Column(Text())
    status = Column(Text())
    rank = Column(Integer())
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
    disjoint_with = relationship( "ClassDefinition", secondary="class_definition_disjoint_with")
    
    
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
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_definition', source_slot='local_names', mapping_type=None, target_class='local_name', target_slot='class_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    local_names = relationship( "LocalName", foreign_keys="[local_name.class_definition_name]")
    
    
    implements_rel = relationship( "ClassDefinitionImplements" )
    implements = association_proxy("implements_rel", "implements",
                                  creator=lambda x_: ClassDefinitionImplements(implements=x_))
    
    
    instantiates_rel = relationship( "ClassDefinitionInstantiates" )
    instantiates = association_proxy("instantiates_rel", "instantiates",
                                  creator=lambda x_: ClassDefinitionInstantiates(instantiates=x_))
    
    
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
    
    
    aliases_rel = relationship( "ClassDefinitionAliases" )
    aliases = association_proxy("aliases_rel", "aliases",
                                  creator=lambda x_: ClassDefinitionAliases(aliases=x_))
    
    
    # One-To-Many: OneToAnyMapping(source_class='class_definition', source_slot='structured_aliases', mapping_type=None, target_class='structured_alias', target_slot='class_definition_name', join_class=None, uses_join_table=None, multivalued=False)
    structured_aliases = relationship( "StructuredAlias", foreign_keys="[structured_alias.class_definition_name]")
    
    
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
    
    
    contributors_rel = relationship( "ClassDefinitionContributors" )
    contributors = association_proxy("contributors_rel", "contributors",
                                  creator=lambda x_: ClassDefinitionContributors(contributors=x_))
    
    
    categories_rel = relationship( "ClassDefinitionCategory" )
    categories = association_proxy("categories_rel", "category",
                                  creator=lambda x_: ClassDefinitionCategory(category=x_))
    
    
    keywords_rel = relationship( "ClassDefinitionKeyword" )
    keywords = association_proxy("keywords_rel", "keyword",
                                  creator=lambda x_: ClassDefinitionKeyword(keyword=x_))
    

    def __repr__(self):
        return f"class_definition(class_uri={self.class_uri},subclass_of={self.subclass_of},tree_root={self.tree_root},slot_names_unique={self.slot_names_unique},represents_relationship={self.represents_relationship},children_are_mutually_disjoint={self.children_are_mutually_disjoint},is_a={self.is_a},abstract={self.abstract},mixin={self.mixin},string_serialization={self.string_serialization},name={self.name},id_prefixes_are_closed={self.id_prefixes_are_closed},definition_uri={self.definition_uri},conforms_to={self.conforms_to},description={self.description},title={self.title},deprecated={self.deprecated},from_schema={self.from_schema},imported_from={self.imported_from},source={self.source},in_language={self.in_language},deprecated_element_has_exact_replacement={self.deprecated_element_has_exact_replacement},deprecated_element_has_possible_replacement={self.deprecated_element_has_possible_replacement},created_by={self.created_by},created_on={self.created_on},last_updated_on={self.last_updated_on},modified_by={self.modified_by},status={self.status},rank={self.rank},schema_definition_name={self.schema_definition_name},)"



    
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    

