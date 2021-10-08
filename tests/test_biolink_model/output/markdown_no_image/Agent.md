
# Class: agent


person, group, organization or project that provides a piece of information (i.e. a knowledge association)

URI: [biolink:Agent](https://w3id.org/biolink/vocab/Agent)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[NamedThing],[InformationContentEntity],[ContributorAssociation],[Attribute],[Association],[ContributorAssociation]-%20object%201..1>[Agent&#124;affiliation:uriorcurie%20*;address:string%20%3F;id:string;name:label_type%20%3F;iri(i):iri_type%20%3F;type(i):string%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[Entity]-%20provided%20by%200..*>[Agent],[AdministrativeEntity]^-[Agent],[Entity],[AdministrativeEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[NamedThing],[InformationContentEntity],[ContributorAssociation],[Attribute],[Association],[ContributorAssociation]-%20object%201..1>[Agent&#124;affiliation:uriorcurie%20*;address:string%20%3F;id:string;name:label_type%20%3F;iri(i):iri_type%20%3F;type(i):string%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[Entity]-%20provided%20by%200..*>[Agent],[AdministrativeEntity]^-[Agent],[Entity],[AdministrativeEntity])

## Identifier prefixes

 * isbn
 * ORCID
 * ScopusID
 * ResearchID
 * GSID
 * isni

## Parents

 *  is_a: [AdministrativeEntity](AdministrativeEntity.md)

## Referenced by Class

 *  **[Publication](Publication.md)** *[author](author.md)*  <sub>0..\*</sub>  **[Agent](Agent.md)**
 *  **[InformationContentEntity](InformationContentEntity.md)** *[contributor](contributor.md)*  <sub>0..\*</sub>  **[Agent](Agent.md)**
 *  **[ContributorAssociation](ContributorAssociation.md)** *[contributor association➞object](contributor_association_object.md)*  <sub>1..1</sub>  **[Agent](Agent.md)**
 *  **[Publication](Publication.md)** *[editor](editor.md)*  <sub>0..\*</sub>  **[Agent](Agent.md)**
 *  **[Association](Association.md)** *[provided by](provided_by.md)*  <sub>0..\*</sub>  **[Agent](Agent.md)**
 *  **[InformationContentEntity](InformationContentEntity.md)** *[provider](provider.md)*  <sub>0..\*</sub>  **[Agent](Agent.md)**
 *  **[Publication](Publication.md)** *[publisher](publisher.md)*  <sub>0..\*</sub>  **[Agent](Agent.md)**

## Attributes


### Own

 * [affiliation](affiliation.md)  <sub>0..\*</sub>
     * Description: a professional relationship between one provider (often a person) within another provider (often an organization). Target provider identity should be specified by a CURIE. Providers may have multiple affiliations.
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [address](address.md)  <sub>0..1</sub>
     * Description: the particulars of the place where someone or an organization is situated.  For now, this slot is a simple text "blob" containing all relevant details of the given location for fitness of purpose. For the moment, this "address" can include other contact details such as email and phone number(?).
     * Range: [String](types/String.md)
 * [agent➞id](agent_id.md)  <sub>1..1</sub>
     * Description: Different classes of agents have distinct preferred identifiers. For publishers, use the ISBN publisher code. See https://grp.isbn-international.org/ for publisher code lookups. For editors, authors and  individual providers, use the individual's ORCID if available; Otherwise, a ScopusID, ResearchID or Google Scholar ID ('GSID') may be used if the author ORCID is unknown. Institutional agents could be identified by an International Standard Name Identifier ('ISNI') code.
     * Range: [String](types/String.md)
     * in subsets: (translator_minimal)
 * [agent➞name](agent_name.md)  <sub>0..1</sub>
     * Description: it is recommended that an author's 'name' property be formatted as "surname, firstname initial."
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal,samples)

### Inherited from administrative entity:

 * [iri](iri.md)  <sub>0..1</sub>
     * Description: An IRI for an entity. This is determined by the id using expansion rules.
     * Range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal,samples)
 * [type](type.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Description: a human-readable description of an entity
     * Range: [NarrativeText](types/NarrativeText.md)
     * in subsets: (translator_minimal)
 * [source](source.md)  <sub>0..1</sub>
     * Description: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
 * [provided by](provided_by.md)  <sub>0..\*</sub>
     * Description: connects an association to the agent (person, organization or group) that provided it
     * Range: [Agent](Agent.md)
 * [has attribute](has_attribute.md)  <sub>0..\*</sub>
     * Description: connects any entity to an attribute
     * Range: [Attribute](Attribute.md)
     * in subsets: (samples)
 * [named thing➞category](named_thing_category.md)  <sub>1..\*</sub>
     * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * In a neo4j database this MAY correspond to the neo4j label tag.
 * In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}
     * Range: [NamedThing](NamedThing.md)
     * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | group |
| **Exact Mappings:** | | prov:Agent |
|  | | dct:Agent |
| **Narrow Mappings:** | | UMLSSG:ORGA |
|  | | UMLSSC:T092 |
|  | | UMLSST:orgt |
|  | | UMLSSC:T093 |
|  | | UMLSST:hcro |
|  | | UMLSSC:T094 |
|  | | UMLSST:pros |
|  | | UMLSSC:T095 |
|  | | UMLSST:shro |
|  | | UMLSSC:T096 |
|  | | UMLSST:grup |
|  | | UMLSSC:T097 |
|  | | UMLSST:prog |

