
# Class: small molecule


A small molecule entity is a molecular entity characterized by availability in small-molecule databases of SMILES, InChI, IUPAC, or other unambiguous representation of its precise chemical structure; for convenience of representation, any valid chemical representation is included, even if it is not strictly molecular (e.g., sodium ion).

URI: [biolink:SmallMolecule](https://w3id.org/biolink/vocab/SmallMolecule)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[MolecularEntity]^-[SmallMolecule&#124;id:string;is_metabolite(i):boolean%20%3F;available_from(i):DrugAvailabilityEnum%20*;max_tolerated_dose(i):string%20%3F;is_toxic(i):boolean%20%3F;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[MolecularEntity],[ChemicalRole],[ChemicalEntity],[Attribute])](https://yuml.me/diagram/nofunky;dir:TB/class/[MolecularEntity]^-[SmallMolecule&#124;id:string;is_metabolite(i):boolean%20%3F;available_from(i):DrugAvailabilityEnum%20*;max_tolerated_dose(i):string%20%3F;is_toxic(i):boolean%20%3F;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[MolecularEntity],[ChemicalRole],[ChemicalEntity],[Attribute])

## Identifier prefixes

 * PUBCHEM.COMPOUND
 * CHEMBL.COMPOUND
 * UNII
 * CHEBI
 * DRUGBANK
 * MESH
 * CAS
 * DrugCentral
 * GTOPDB
 * HMDB
 * KEGG.COMPOUND
 * ChemBank
 * PUBCHEM.SUBSTANCE
 * SIDER.DRUG
 * INCHI
 * INCHIKEY
 * KEGG.GLYCAN
 * KEGG.DRUG
 * KEGG.DGROUP
 * KEGG.ENVIRON
 * BIGG.METABOLITE
 * UMLS
 * foodb.compound

## Parents

 *  is_a: [MolecularEntity](MolecularEntity.md) - A molecular entity is a chemical entity composed of individual or covalently bonded atoms.

## Referenced by Class


## Attributes


### Own

 * [small molecule➞id](small_molecule_id.md)  <sub>1..1</sub>
     * Description: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * Range: [String](types/String.md)
     * Example: CHEBI:29101 sodium ion
     * in subsets: (translator_minimal)

### Inherited from molecular entity:

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
 * [trade name](trade_name.md)  <sub>0..1</sub>
     * Range: [ChemicalEntity](ChemicalEntity.md)
 * [available from](available_from.md)  <sub>0..\*</sub>
     * Range: [DrugAvailabilityEnum](DrugAvailabilityEnum.md)
 * [max tolerated dose](max_tolerated_dose.md)  <sub>0..1</sub>
     * Description: The highest dose of a drug or treatment that does not cause unacceptable side effects. The maximum tolerated dose is determined in clinical trials by testing increasing doses on different groups of people until the highest dose with acceptable side effects is found. Also called MTD.
     * Range: [String](types/String.md)
 * [is toxic](is_toxic.md)  <sub>0..1</sub>
     * Range: [Boolean](types/Boolean.md)
 * [has chemical role](has_chemical_role.md)  <sub>0..\*</sub>
     * Description: A role is particular behaviour which a chemical entity may exhibit.
     * Range: [ChemicalRole](ChemicalRole.md)
 * [is metabolite](is_metabolite.md)  <sub>0..1</sub>
     * Description: indicates whether a molecular entity is a metabolite
     * Range: [Boolean](types/Boolean.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | chemical substance |
| **In Subsets:** | | model_organism_database |
|  | | translator_minimal |
| **Narrow Mappings:** | | STY:T196 |
|  | | CHEBI:59999 |
|  | | bioschemas:ChemicalSubstance |
|  | | STY:T123 |
|  | | STY:T131 |
|  | | STY:T125 |
|  | | STY:T197 |
|  | | STY:T109 |
|  | | STY:T118 |
|  | | STY:T111 |
|  | | STY:T119 |
|  | | STY:T124 |
|  | | STY:T115 |
|  | | STY:T110 |
|  | | STY:T127 |

