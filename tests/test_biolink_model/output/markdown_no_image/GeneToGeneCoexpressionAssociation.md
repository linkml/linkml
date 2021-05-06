
# Class: GeneToGeneCoexpressionAssociation


Indicates that two genes are co-expressed, generally under the same conditions.

URI: [biolink:GeneToGeneCoexpressionAssociation](https://w3id.org/biolink/vocab/GeneToGeneCoexpressionAssociation)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[OntologyClass],[LifeStage],[GeneToGeneCoexpressionAssociation&#124;predicate:predicate_type;relation(i):uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]uses%20-.->[GeneExpressionMixin],[GeneToGeneAssociation]^-[GeneToGeneCoexpressionAssociation],[GeneToGeneAssociation],[GeneOrGeneProduct],[GeneExpressionMixin],[DiseaseOrPhenotypicFeature],[Attribute],[AnatomicalEntity],[Agent])

## Parents

 *  is_a: [GeneToGeneAssociation](GeneToGeneAssociation.md) - abstract parent class for different kinds of gene-gene or gene product to gene product relationships. Includes homology and interaction.

## Uses Mixins

 *  mixin: [GeneExpressionMixin](GeneExpressionMixin.md) - Observed gene expression intensity, context (site, stage) and associated phenotypic status within which the expression occurs.

## Referenced by class


## Attributes


### Own

 * [gene to gene coexpression association➞predicate](gene_to_gene_coexpression_association_predicate.md)  <sub>REQ</sub>
     * range: [PredicateType](types/PredicateType.md)

### Inherited from gene to gene association:

 * [association➞category](association_category.md)  <sub>0..*</sub>
     * range: [CategoryType](types/CategoryType.md)
 * [association➞type](association_type.md)  <sub>OPT</sub>
     * Description: rdf:type of biolink:Association should be fixed at rdf:Statement
     * range: [String](types/String.md)
 * [description](description.md)  <sub>OPT</sub>
     * Description: a human-readable description of an entity
     * range: [NarrativeText](types/NarrativeText.md)
     * in subsets: (translator_minimal)
 * [gene to gene association➞object](gene_to_gene_association_object.md)  <sub>REQ</sub>
     * Description: the object gene in the association. If the relation is symmetric, subject vs object is arbitrary. We allow a gene product to stand as a proxy for the gene or vice versa.
     * range: [GeneOrGeneProduct](GeneOrGeneProduct.md)
 * [gene to gene association➞subject](gene_to_gene_association_subject.md)  <sub>REQ</sub>
     * Description: the subject gene in the association. If the relation is symmetric, subject vs object is arbitrary. We allow a gene product to stand as a proxy for the gene or vice versa.
     * range: [GeneOrGeneProduct](GeneOrGeneProduct.md)
 * [has attribute](has_attribute.md)  <sub>0..*</sub>
     * Description: connects any entity to an attribute
     * range: [Attribute](Attribute.md)
     * in subsets: (samples)
 * [id](id.md)  <sub>REQ</sub>
     * Description: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * range: [String](types/String.md)
     * in subsets: (translator_minimal)
 * [iri](iri.md)  <sub>OPT</sub>
     * Description: An IRI for an entity. This is determined by the id using expansion rules.
     * range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal,samples)
 * [name](name.md)  <sub>OPT</sub>
     * Description: A human-readable name for an attribute or entity.
     * range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal,samples)
 * [negated](negated.md)  <sub>OPT</sub>
     * Description: if set to true, then the association is negated i.e. is not true
     * range: [Boolean](types/Boolean.md)
 * [provided by](provided_by.md)  <sub>0..*</sub>
     * Description: connects an association to the agent (person, organization or group) that provided it
     * range: [Agent](Agent.md)
 * [publications](publications.md)  <sub>0..*</sub>
     * Description: connects an association to publications supporting the association
     * range: [Publication](Publication.md)
 * [qualifiers](qualifiers.md)  <sub>0..*</sub>
     * Description: connects an association to qualifiers that modify or qualify the meaning of that association
     * range: [OntologyClass](OntologyClass.md)
 * [relation](relation.md)  <sub>REQ</sub>
     * Description: The relation which describes an association between a subject and an object in a more granular manner. Usually this is a term from Relation Ontology, but it can be any edge CURIE.
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [source](source.md)  <sub>OPT</sub>
     * Description: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
     * range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)

### Mixed in from gene expression mixin:

 * [expression site](expression_site.md)  <sub>OPT</sub>
     * Description: location in which gene or protein expression takes place. May be cell, tissue, or organ.
     * range: [AnatomicalEntity](AnatomicalEntity.md)
     * Example: UBERON:0002037 cerebellum

### Mixed in from gene expression mixin:

 * [gene expression mixin➞quantifier qualifier](gene_expression_mixin_quantifier_qualifier.md)  <sub>OPT</sub>
     * Description: Optional quantitative value indicating degree of expression.
     * range: [OntologyClass](OntologyClass.md)

### Mixed in from gene expression mixin:

 * [phenotypic state](phenotypic_state.md)  <sub>OPT</sub>
     * Description: in experiments (e.g. gene expression) assaying diseased or unhealthy tissue, the phenotypic state can be put here, e.g. MONDO ID. For healthy tissues, use XXX.
     * range: [DiseaseOrPhenotypicFeature](DiseaseOrPhenotypicFeature.md)

### Mixed in from gene expression mixin:

 * [stage qualifier](stage_qualifier.md)  <sub>OPT</sub>
     * Description: stage during which gene or protein expression of takes place.
     * range: [LifeStage](LifeStage.md)
     * Example: UBERON:0000069 larval stage
