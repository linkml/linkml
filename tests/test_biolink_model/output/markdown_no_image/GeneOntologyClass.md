
# Class: gene ontology class


an ontology class that describes a functional aspect of a gene, gene prodoct or complex

URI: [biolink:GeneOntologyClass](https://w3id.org/biolink/vocab/GeneOntologyClass)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[OntologyClass],[GeneToGoTermAssociation],[FunctionalAssociation]++-%20object%201..1>[GeneOntologyClass],[GeneToGoTermAssociation]++-%20object%201..1>[GeneOntologyClass],[OntologyClass]^-[GeneOntologyClass],[FunctionalAssociation])](https://yuml.me/diagram/nofunky;dir:TB/class/[OntologyClass],[GeneToGoTermAssociation],[FunctionalAssociation]++-%20object%201..1>[GeneOntologyClass],[GeneToGoTermAssociation]++-%20object%201..1>[GeneOntologyClass],[OntologyClass]^-[GeneOntologyClass],[FunctionalAssociation])

## Parents

 *  is_a: [OntologyClass](OntologyClass.md) - a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.

## Referenced by Class

 *  **[FunctionalAssociation](FunctionalAssociation.md)** *[functional association➞object](functional_association_object.md)*  <sub>1..1</sub>  **[GeneOntologyClass](GeneOntologyClass.md)**
 *  **[GeneToGoTermAssociation](GeneToGoTermAssociation.md)** *[gene to go term association➞object](gene_to_go_term_association_object.md)*  <sub>1..1</sub>  **[GeneOntologyClass](GeneOntologyClass.md)**

## Attributes


## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | testing |

