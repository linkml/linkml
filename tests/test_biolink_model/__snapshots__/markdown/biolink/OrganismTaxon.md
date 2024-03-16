
# Class: organism taxon


A classification of a set of organisms. Example instances: NCBITaxon:9606 (Homo sapiens), NCBITaxon:2 (Bacteria). Can also be used to represent strains or subspecies.

URI: [biolink:OrganismTaxon](https://w3id.org/biolink/vocab/OrganismTaxon)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[ThingWithTaxon],[TaxonomicRank],[TaxonToTaxonAssociation],[OrganismTaxonToOrganismTaxonSpecialization],[OrganismTaxonToOrganismTaxonInteraction],[OrganismTaxonToOrganismTaxonAssociation],[OrganismTaxonToEnvironmentAssociation],[OrganismTaxonToEntityAssociation],[TaxonomicRank]<has%20taxonomic%20rank%200..1-%20[OrganismTaxon&#124;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[ChemicalAffectsGeneAssociation]-%20species%20context%20qualifier%200..1>[OrganismTaxon],[ThingWithTaxon]-%20in%20taxon%200..*>[OrganismTaxon],[OrganismTaxonToEntityAssociation]-%20subject%201..1>[OrganismTaxon],[OrganismTaxonToEnvironmentAssociation]-%20subject%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonAssociation]-%20object%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonAssociation]-%20subject%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonInteraction]-%20object%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonInteraction]-%20subject%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonSpecialization]-%20object%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonSpecialization]-%20subject%201..1>[OrganismTaxon],[PredicateMapping]-%20species%20context%20qualifier%200..1>[OrganismTaxon],[TaxonToTaxonAssociation]-%20object%201..1>[OrganismTaxon],[TaxonToTaxonAssociation]-%20subject%201..1>[OrganismTaxon],[NamedThing]^-[OrganismTaxon],[PredicateMapping],[NamedThing],[ChemicalAffectsGeneAssociation],[Attribute],[Association])](https://yuml.me/diagram/nofunky;dir:TB/class/[ThingWithTaxon],[TaxonomicRank],[TaxonToTaxonAssociation],[OrganismTaxonToOrganismTaxonSpecialization],[OrganismTaxonToOrganismTaxonInteraction],[OrganismTaxonToOrganismTaxonAssociation],[OrganismTaxonToEnvironmentAssociation],[OrganismTaxonToEntityAssociation],[TaxonomicRank]<has%20taxonomic%20rank%200..1-%20[OrganismTaxon&#124;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[ChemicalAffectsGeneAssociation]-%20species%20context%20qualifier%200..1>[OrganismTaxon],[ThingWithTaxon]-%20in%20taxon%200..*>[OrganismTaxon],[OrganismTaxonToEntityAssociation]-%20subject%201..1>[OrganismTaxon],[OrganismTaxonToEnvironmentAssociation]-%20subject%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonAssociation]-%20object%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonAssociation]-%20subject%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonInteraction]-%20object%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonInteraction]-%20subject%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonSpecialization]-%20object%201..1>[OrganismTaxon],[OrganismTaxonToOrganismTaxonSpecialization]-%20subject%201..1>[OrganismTaxon],[PredicateMapping]-%20species%20context%20qualifier%200..1>[OrganismTaxon],[TaxonToTaxonAssociation]-%20object%201..1>[OrganismTaxon],[TaxonToTaxonAssociation]-%20subject%201..1>[OrganismTaxon],[NamedThing]^-[OrganismTaxon],[PredicateMapping],[NamedThing],[ChemicalAffectsGeneAssociation],[Attribute],[Association])

## Identifier prefixes

 * NCBITaxon
 * MESH
 * UMLS

## Parents

 *  is_a: [NamedThing](NamedThing.md) - a databased entity or concept/class

## Referenced by Class

 *  **[ChemicalAffectsGeneAssociation](ChemicalAffectsGeneAssociation.md)** *[chemical affects gene association➞species context qualifier](chemical_affects_gene_association_species_context_qualifier.md)*  <sub>0..1</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[ThingWithTaxon](ThingWithTaxon.md)** *[in taxon](in_taxon.md)*  <sub>0..\*</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[OrganismTaxonToEntityAssociation](OrganismTaxonToEntityAssociation.md)** *[organism taxon to entity association➞subject](organism_taxon_to_entity_association_subject.md)*  <sub>1..1</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[OrganismTaxonToEnvironmentAssociation](OrganismTaxonToEnvironmentAssociation.md)** *[organism taxon to environment association➞subject](organism_taxon_to_environment_association_subject.md)*  <sub>1..1</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[OrganismTaxonToOrganismTaxonAssociation](OrganismTaxonToOrganismTaxonAssociation.md)** *[organism taxon to organism taxon association➞object](organism_taxon_to_organism_taxon_association_object.md)*  <sub>1..1</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[OrganismTaxonToOrganismTaxonAssociation](OrganismTaxonToOrganismTaxonAssociation.md)** *[organism taxon to organism taxon association➞subject](organism_taxon_to_organism_taxon_association_subject.md)*  <sub>1..1</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[OrganismTaxonToOrganismTaxonInteraction](OrganismTaxonToOrganismTaxonInteraction.md)** *[organism taxon to organism taxon interaction➞object](organism_taxon_to_organism_taxon_interaction_object.md)*  <sub>1..1</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[OrganismTaxonToOrganismTaxonInteraction](OrganismTaxonToOrganismTaxonInteraction.md)** *[organism taxon to organism taxon interaction➞subject](organism_taxon_to_organism_taxon_interaction_subject.md)*  <sub>1..1</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[OrganismTaxonToOrganismTaxonSpecialization](OrganismTaxonToOrganismTaxonSpecialization.md)** *[organism taxon to organism taxon specialization➞object](organism_taxon_to_organism_taxon_specialization_object.md)*  <sub>1..1</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[OrganismTaxonToOrganismTaxonSpecialization](OrganismTaxonToOrganismTaxonSpecialization.md)** *[organism taxon to organism taxon specialization➞subject](organism_taxon_to_organism_taxon_specialization_subject.md)*  <sub>1..1</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[Association](Association.md)** *[species context qualifier](species_context_qualifier.md)*  <sub>0..1</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[TaxonToTaxonAssociation](TaxonToTaxonAssociation.md)** *[taxon to taxon association➞object](taxon_to_taxon_association_object.md)*  <sub>1..1</sub>  **[OrganismTaxon](OrganismTaxon.md)**
 *  **[TaxonToTaxonAssociation](TaxonToTaxonAssociation.md)** *[taxon to taxon association➞subject](taxon_to_taxon_association_subject.md)*  <sub>1..1</sub>  **[OrganismTaxon](OrganismTaxon.md)**

## Attributes


### Own

 * [organism taxon➞has taxonomic rank](organism_taxon_has_taxonomic_rank.md)  <sub>0..1</sub>
     * Range: [TaxonomicRank](TaxonomicRank.md)

### Inherited from named thing:

 * [id](id.md)  <sub>1..1</sub>
     * Description: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * Range: [String](types/String.md)
     * in subsets: (translator_minimal)
 * [iri](iri.md)  <sub>0..1</sub>
     * Description: An IRI for an entity. This is determined by the id using expansion rules.
     * Range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal,samples)
 * [type](type.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
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
 * [provided by](provided_by.md)  <sub>0..\*</sub>
     * Description: The value in this node property represents the knowledge provider that created or assembled the node and all of its attributes.  Used internally to represent how a particular node made its way into a knowledge provider or graph.
     * Range: [String](types/String.md)
 * [xref](xref.md)  <sub>0..\*</sub>
     * Description: Alternate CURIEs for a thing
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (translator_minimal)
 * [named thing➞category](named_thing_category.md)  <sub>1..\*</sub>
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
| **Aliases:** | | taxon |
|  | | taxonomic classification |
| **In Subsets:** | | model_organism_database |
| **Exact Mappings:** | | WIKIDATA:Q16521 |
|  | | STY:T001 |
|  | | bioschemas:Taxon |
| **Narrow Mappings:** | | dcid:BiologicalSpecies |

