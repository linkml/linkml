
# Class: gene to expression site association


An association between a gene and a gene expression site, possibly qualified by stage/timing info.

URI: [biolink:GeneToExpressionSiteAssociation](https://w3id.org/biolink/vocab/GeneToExpressionSiteAssociation)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[OntologyClass],[LifeStage],[InformationResource],[AnatomicalEntity]<object%201..1-%20[GeneToExpressionSiteAssociation&#124;predicate:predicate_type;negated(i):boolean%20%3F;timepoint(i):time_type%20%3F;original_subject(i):string%20%3F;original_predicate(i):uriorcurie%20%3F;original_object(i):string%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[GeneOrGeneProduct]<subject%201..1-++[GeneToExpressionSiteAssociation],[OntologyClass]<quantifier%20qualifier%200..1-%20[GeneToExpressionSiteAssociation],[LifeStage]<stage%20qualifier%200..1-%20[GeneToExpressionSiteAssociation],[Association]^-[GeneToExpressionSiteAssociation],[GeneOrGeneProduct],[EvidenceType],[Attribute],[Association],[AnatomicalEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[OntologyClass],[LifeStage],[InformationResource],[AnatomicalEntity]<object%201..1-%20[GeneToExpressionSiteAssociation&#124;predicate:predicate_type;negated(i):boolean%20%3F;timepoint(i):time_type%20%3F;original_subject(i):string%20%3F;original_predicate(i):uriorcurie%20%3F;original_object(i):string%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[GeneOrGeneProduct]<subject%201..1-++[GeneToExpressionSiteAssociation],[OntologyClass]<quantifier%20qualifier%200..1-%20[GeneToExpressionSiteAssociation],[LifeStage]<stage%20qualifier%200..1-%20[GeneToExpressionSiteAssociation],[Association]^-[GeneToExpressionSiteAssociation],[GeneOrGeneProduct],[EvidenceType],[Attribute],[Association],[AnatomicalEntity])

## Parents

 *  is_a: [Association](Association.md) - A typed association between two entities, supported by evidence

## Referenced by Class


## Attributes


### Own

 * [gene to expression site association➞stage qualifier](gene_to_expression_site_association_stage_qualifier.md)  <sub>0..1</sub>
     * Description: stage at which the gene is expressed in the site
     * Range: [LifeStage](LifeStage.md)
     * Example: UBERON:0000069 larval stage
 * [gene to expression site association➞quantifier qualifier](gene_to_expression_site_association_quantifier_qualifier.md)  <sub>0..1</sub>
     * Description: can be used to indicate magnitude, or also ranking
     * Range: [OntologyClass](OntologyClass.md)
 * [gene to expression site association➞subject](gene_to_expression_site_association_subject.md)  <sub>1..1</sub>
     * Description: Gene or gene product positively within the specified anatomical entity (or subclass, i.e. cellular component) location.
     * Range: [GeneOrGeneProduct](GeneOrGeneProduct.md)
 * [gene to expression site association➞object](gene_to_expression_site_association_object.md)  <sub>1..1</sub>
     * Description: location in which the gene is expressed
     * Range: [AnatomicalEntity](AnatomicalEntity.md)
     * Example: UBERON:0002037 cerebellum
 * [gene to expression site association➞predicate](gene_to_expression_site_association_predicate.md)  <sub>1..1</sub>
     * Description: expression relationship
     * Range: [PredicateType](types/PredicateType.md)

### Inherited from association:

 * [id](id.md)  <sub>1..1</sub>
     * Description: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * Range: [String](types/String.md)
     * in subsets: (translator_minimal)
 * [iri](iri.md)  <sub>0..1</sub>
     * Description: An IRI for an entity. This is determined by the id using expansion rules.
     * Range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal,samples)
 * [name](name.md)  <sub>0..1</sub>
     * Description: A human-readable name for an attribute or entity.
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal,samples)
 * [description](description.md)  <sub>0..1</sub>
     * Description: a human-readable description of an entity
     * Range: [NarrativeText](types/NarrativeText.md)
     * in subsets: (translator_minimal)
 * [has attribute](has_attribute.md)  <sub>0..\*</sub>
     * Description: connects any entity to an attribute
     * Range: [Attribute](Attribute.md)
     * in subsets: (samples)
 * [negated](negated.md)  <sub>0..1</sub>
     * Description: if set to true, then the association is negated i.e. is not true
     * Range: [Boolean](types/Boolean.md)
 * [qualifiers](qualifiers.md)  <sub>0..\*</sub>
     * Description: connects an association to qualifiers that modify or qualify the meaning of that association
     * Range: [OntologyClass](OntologyClass.md)
 * [publications](publications.md)  <sub>0..\*</sub>
     * Description: One or more publications that report the statement expressed in an Association, or provide information used as  evidence supporting this statement.
     * Range: [Publication](Publication.md)
 * [has evidence](has_evidence.md)  <sub>0..\*</sub>
     * Description: connects an association to an instance of supporting evidence
     * Range: [EvidenceType](EvidenceType.md)
 * [knowledge source](knowledge_source.md)  <sub>0..1</sub>
     * Description: An Information Resource from which the knowledge expressed in an Association was retrieved, directly or indirectly. This can be any resource through which the knowledge passed on its way to its currently serialized form. In practice, implementers should use one of the more specific subtypes of this generic property.
     * Range: [InformationResource](InformationResource.md)
 * [primary knowledge source](primary_knowledge_source.md)  <sub>0..1</sub>
     * Description: The most upstream source of the knowledge expressed in an Association that an implementer can identify.  Performing a rigorous analysis of upstream data providers is expected; every effort is made to catalog the most upstream source of data in this property.  Only one data source should be declared primary in any association.  "aggregator knowledge source" can be used to caputre non-primary sources.
     * Range: [InformationResource](InformationResource.md)
 * [aggregator knowledge source](aggregator_knowledge_source.md)  <sub>0..\*</sub>
     * Description: An intermediate aggregator resource from which knowledge expressed in an Association was retrieved downstream of the original source, on its path to its current serialized form.
     * Range: [InformationResource](InformationResource.md)
 * [timepoint](timepoint.md)  <sub>0..1</sub>
     * Description: a point in time
     * Range: [TimeType](types/TimeType.md)
 * [original subject](original_subject.md)  <sub>0..1</sub>
     * Description: used to hold the original subject of a relation (or predicate) that an external knowledge source uses before transformation to match the biolink-model specification.
     * Range: [String](types/String.md)
 * [original predicate](original_predicate.md)  <sub>0..1</sub>
     * Description: used to hold the original relation/predicate that an external knowledge source uses before transformation to match the biolink-model specification.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [original object](original_object.md)  <sub>0..1</sub>
     * Description: used to hold the original object of a relation (or predicate) that an external knowledge source uses before transformation to match the biolink-model specification.
     * Range: [String](types/String.md)
 * [association➞type](association_type.md)  <sub>0..1</sub>
     * Description: rdf:type of biolink:Association should be fixed at rdf:Statement
     * Range: [String](types/String.md)
 * [association➞category](association_category.md)  <sub>0..\*</sub>
     * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * In a neo4j database this MAY correspond to the neo4j label tag.
 * In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}
     * Range: [CategoryType](types/CategoryType.md)
     * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **See also:** | | [https://github.com/monarch-initiative/ingest-artifacts/tree/master/sources/BGee](https://github.com/monarch-initiative/ingest-artifacts/tree/master/sources/BGee) |

