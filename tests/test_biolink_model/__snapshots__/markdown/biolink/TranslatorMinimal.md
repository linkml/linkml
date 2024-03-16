
# Subset: translator_minimal


Minimum subset of translator work

URI: [biolink:translator_minimal](https://w3id.org/biolink/vocab/translator_minimal)


### Classes

 * [ChemicalEntity](ChemicalEntity.md) - A chemical entity is a physical entity that pertains to chemistry or biochemistry.
 * [ChemicalMixture](ChemicalMixture.md) - A chemical mixture is a chemical entity composed of two or more molecular entities.
 * [ComplexMolecularMixture](ComplexMolecularMixture.md) - A complex molecular mixture is a chemical mixture composed of two or more molecular entities with unknown concentration and stoichiometry.
 * [Gene](Gene.md) - A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A gene locus may include regulatory regions, transcribed regions and/or other functional sequence regions.
 * [InformationResource](InformationResource.md) - A database or knowledgebase and its supporting ecosystem of interfaces  and services that deliver content to consumers (e.g. web portals, APIs,  query endpoints, streaming services, data downloads, etc.). A single Information Resource by this definition may span many different datasets or databases, and include many access endpoints and user interfaces. Information Resources include project-specific resources such as a Translator Knowledge Provider, and community knowledgebases like ChemBL, OMIM, or DGIdb.
 * [MolecularEntity](MolecularEntity.md) - A molecular entity is a chemical entity composed of individual or covalently bonded atoms.
 * [MolecularMixture](MolecularMixture.md) - A molecular mixture is a chemical mixture composed of two or more molecular entities with known concentration and stoichiometry.
 * [NucleicAcidEntity](NucleicAcidEntity.md) - A nucleic acid entity is a molecular entity characterized by availability in gene databases of nucleotide-based sequence representations of its precise sequence; for convenience of representation, partial sequences of various kinds are included.
 * [SmallMolecule](SmallMolecule.md) - A small molecule entity is a molecular entity characterized by availability in small-molecule databases of SMILES, InChI, IUPAC, or other unambiguous representation of its precise chemical structure; for convenience of representation, any valid chemical representation is included, even if it is not strictly molecular (e.g., sodium ion).

### Mixins

 * [EpigenomicEntity](EpigenomicEntity.md)
 * [GenomicEntity](GenomicEntity.md)

### Slots

 * [actively involved in](actively_involved_in.md) - holds between a continuant and a process or function, where the continuant actively contributes to part or all of the process or function it realizes
 * [actively involves](actively_involves.md)
 * [affects](affects.md) - describes an entity that has a direct affect on the state or quality of another existing entity. Use of the 'affects' predicate implies that the affected entity already exists, unlike predicates such as 'affects risk for' and 'prevents, where the outcome is something that may or may not come to be.
 * [affects response to](affects_response_to.md)
 * [affects risk for](affects_risk_for.md) - holds between two entities where exposure to one entity alters the chance of developing the other
 * [agent➞id](agent_id.md) - Different classes of agents have distinct preferred identifiers. For publishers, use the ISBN publisher code. See https://grp.isbn-international.org/ for publisher code lookups. For editors, authors and  individual providers, use the individual's ORCID if available; Otherwise, a ScopusID, ResearchID or Google Scholar ID ('GSID') may be used if the author ORCID is unknown. Institutional agents could be identified by an International Standard Name Identifier ('ISNI') code.
 * [agent➞name](agent_name.md) - it is recommended that an author's 'name' property be formatted as "surname, firstname initial."
 * [association➞category](association_category.md)
 * [attribute➞name](attribute_name.md) - The human-readable 'attribute name' can be set to a string which reflects its context of interpretation, e.g. SEPIO evidence/provenance/confidence annotation or it can default to the name associated with the 'has attribute type' slot ontology term.
 * [biomarker for](biomarker_for.md) - holds between a measurable chemical entity and a disease or phenotypic feature, where the entity is used as an indicator of the presence or state of the disease or feature.
 * [book➞id](book_id.md) - Books should have industry-standard identifier such as from ISBN.
 * [broad match](broad_match.md) - a list of terms from different schemas or terminology systems that have a broader, more general meaning. Broader terms are typically shown as parents in a hierarchy or tree.
 * [capable of](capable_of.md) - holds between a physical entity and process or function, where the continuant alone has the ability to carry out the process or function.
 * [category](category.md) - Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * [caused by](caused_by.md) - holds between two entities where the occurrence, existence, or activity of one is caused by the occurrence or generation of the other
 * [causes](causes.md) - holds between two entities where the occurrence, existence, or activity of one causes the occurrence or generation of the other
 * [chemically similar to](chemically_similar_to.md) - holds between one small molecule entity and another that it approximates for purposes of scientific study, in virtue of its exhibiting similar features of the studied entity.
 * [close match](close_match.md) - a list of terms from different schemas or terminology systems that have a semantically similar but not strictly equivalent, broader, or narrower meaning. Such terms often describe the same general concept from different ontological perspectives (e.g. drug as a type of chemical entity versus drug as a type of role borne by a chemical entity).
 * [coexists with](coexists_with.md) - holds between two entities that are co-located in the same aggregate object, process, or spatio-temporal region
 * [colocalizes with](colocalizes_with.md) - holds between two entities that are observed to be located in the same place.
 * [composed primarily of](composed_primarily_of.md) - x composed_primarily_of_y if:more than half of the mass of x is made from parts of y.
 * [condition associated with gene](condition_associated_with_gene.md) - holds between a gene and a disease or phenotypic feature that may be influenced, contribute to, or be correlated with the gene or its alleles/products
 * [contributes to](contributes_to.md) - holds between two entities where the occurrence, existence, or activity of one causes or contributes to the occurrence or generation of the other
 * [contribution from](contribution_from.md)
 * [correlated with](correlated_with.md) - A relationship that holds between two concepts represented by variables for which a statistical dependence is  demonstrated using a correlation analysis method.
 * [decreases response to](decreases_response_to.md) - holds between two chemical entities where the action or effect of one decreases the susceptibility of a biological entity or system (e.g. an organism, cell, cellular component, macromolecular machine mixin, biological or pathological process) to the other
 * [derives from](derives_from.md) - holds between two distinct material entities, the new entity and the old entity, in which the new entity begins to exist when the old entity ceases to exist, and the new entity inherits the significant portion of the matter of the old entity
 * [derives into](derives_into.md) - holds between two distinct material entities, the old entity and the new entity, in which the new entity begins to exist when the old entity ceases to exist, and the new entity inherits the significant portion of the matter of the old entity
 * [description](description.md) - a human-readable description of an entity
 * [disrupts](disrupts.md) - describes a relationship where one entity degrades or interferes with the structure, function, or occurrence of another.
 * [enabled by](enabled_by.md) - holds between a process and a physical entity, where the physical entity executes the process
 * [enables](enables.md) - holds between a physical entity and a process, where the physical entity executes the process
 * [exact match](exact_match.md) - holds between two entities that have strictly equivalent meanings, with a high degree of confidence
 * [expressed in](expressed_in.md) - holds between a gene or gene product and an anatomical entity in which it is expressed
 * [expresses](expresses.md) - holds between an anatomical entity and gene or gene product that is expressed there
 * [food component of](food_component_of.md) - holds between a one or more chemical entities present in food, irrespective of nutritional value (i.e. could also be a contaminant or additive)
 * [gene associated with condition](gene_associated_with_condition.md) - holds between a gene and a disease or phenotypic feature that the gene or its alleles/products may influence, contribute to, or correlate with
 * [gene product of](gene_product_of.md) - definition x has gene product of y if and only if y is a gene (SO:0000704) that participates in some gene expression process (GO:0010467) where the output of thatf process is either y or something that is ribosomally translated from x
 * [genetically interacts with](genetically_interacts_with.md) - holds between two genes whose phenotypic effects are dependent on each other in some way - such that their combined phenotypic effects are the result of some interaction between the activity of their gene products. Examples include epistasis and synthetic lethality.
 * [has active ingredient](has_active_ingredient.md) - holds between a drug and a molecular entity in which the latter is a part of the former, and is a biologically active component
 * [has biomarker](has_biomarker.md) - holds between a disease or phenotypic feature and a measurable chemical entity that is used as an indicator of the presence or state of the disease or feature. # metabolite
 * [has excipient](has_excipient.md) - holds between a drug and a molecular entities in which the latter is a part of the former, and is a biologically inactive component
 * [has food component](has_food_component.md) - holds between food and one or more chemical entities composing it, irrespective of nutritional value (i.e. could also be a contaminant or additive)
 * [has gene product](has_gene_product.md) - holds between a gene and a transcribed and/or translated product generated from it
 * [has input](has_input.md) - holds between a process and a continuant, where the continuant is an input into the process
 * [has member](has_member.md) - Defines a mereological relation between a collection and an item.
 * [has metabolite](has_metabolite.md) - holds between two molecular entities in which the second one is derived from the first one as a product of metabolism
 * [has mode of inheritance](has_mode_of_inheritance.md) - Relates a disease or phenotypic feature to its observed genetic segregation and assumed associated underlying DNA manifestation (i.e. autosomal, sex or mitochondrial chromosome).
 * [has nutrient](has_nutrient.md) - one or more nutrients which are growth factors for a living organism
 * [has output](has_output.md) - holds between a process and a continuant, where the continuant is an output of the process
 * [has part](has_part.md) - holds between wholes and their parts (material entities or processes)
 * [has participant](has_participant.md) - holds between a process and a continuant, where the continuant is somehow involved in the process
 * [has phenotype](has_phenotype.md) - holds between a biological entity and a phenotype, where a phenotype is construed broadly as any kind of quality of an organism part, a collection of these qualities, or a change in quality or qualities (e.g. abnormally increased temperature). In SNOMEDCT, disorders with keyword 'characterized by' should translate into this predicate.
 * [has plasma membrane part](has_plasma_membrane_part.md) - Holds between a cell c and a protein complex or protein p if and only if that cell has as part a plasma_membrane[GO:0005886], and that plasma membrane has p as part.
 * [has predisposing factor](has_predisposing_factor.md)
 * [homologous to](homologous_to.md) - holds between two biological entities that have common evolutionary origin
 * [id](id.md) - A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
 * [in cell population with](in_cell_population_with.md) - holds between two genes or gene products that are expressed in the same cell type or population
 * [in complex with](in_complex_with.md) - holds between two genes or gene products that are part of (or code for products that are part of) in the same macromolecular complex
 * [in pathway with](in_pathway_with.md) - holds between two genes or gene products that are part of in the same biological pathway
 * [in taxon](in_taxon.md) - connects an entity to its taxonomic classification. Only certain kinds of entities can be taxonomically classified; see 'thing with taxon'
 * [increases response to](increases_response_to.md) - holds between two chemical entities where the action or effect of one increases the susceptibility of a biological entity or system (e.g. an organism, cell, cellular component, macromolecular machine mixin, biological or pathological process) to the other
 * [interacts with](interacts_with.md) - holds between any two entities that directly or indirectly interact with each other
 * [iri](iri.md) - An IRI for an entity. This is determined by the id using expansion rules.
 * [is active ingredient of](is_active_ingredient_of.md) - holds between a molecular entity and a drug, in which the former is a part of the latter, and is a biologically active component
 * [is exacerbated by](is_exacerbated_by.md)
 * [is excipient of](is_excipient_of.md) - holds between a molecular entity and a drug in which the former is a part of the latter, and is a biologically inactive component
 * [is input of](is_input_of.md)
 * [is metabolite of](is_metabolite_of.md) - holds between two molecular entities in which the first one is derived from the second one as a product of metabolism
 * [is output of](is_output_of.md)
 * [located in](located_in.md) - holds between a material entity and a material entity or site within which it is located (but of which it is not considered a part)
 * [location of](location_of.md) - holds between material entity or site and a material entity that is located within it (but not considered a part of it)
 * [macromolecular machine mixin➞name](macromolecular_machine_mixin_name.md) - genes are typically designated by a short symbol and a full name. We map the symbol to the default display name and use an additional slot for full name
 * [manifestation of](manifestation_of.md) - that part of a phenomenon which is directly observable or visibly expressed, or which gives evidence to the underlying process; used in SemMedDB for linking things like dysfunctions and processes to some disease or syndrome
 * [member of](member_of.md) - Defines a mereological relation between a item and a collection.
 * [model of](model_of.md) - holds between a thing and some other thing it approximates for purposes of scientific study, in virtue of its exhibiting similar features of the studied entity.
 * [molecular activity➞enabled by](molecular_activity_enabled_by.md) - The gene product, gene, or complex that catalyzes the reaction
 * [molecular activity➞has input](molecular_activity_has_input.md) - A chemical entity that is the input for the reaction
 * [molecular activity➞has output](molecular_activity_has_output.md) - A chemical entity that is the output for the reaction
 * [name](name.md) - A human-readable name for an attribute or entity.
 * [named thing➞category](named_thing_category.md)
 * [narrow match](narrow_match.md) - a list of terms from different schemas or terminology systems that have a narrower, more specific meaning. Narrower terms are typically shown as children in a hierarchy or tree.
 * [negatively correlated with](negatively_correlated_with.md) - A relationship that holds between two concepts represented by variables for which a statistical correlation  is demonstrated, wherein variable values move in opposite directions (i.e. increased in one or presence of  one correlates with a decrease or absence of the other).
 * [nutrient of](nutrient_of.md)
 * [occurs in](occurs_in.md) - holds between a process and a material entity or site within which the process occurs
 * [occurs together in literature with](occurs_together_in_literature_with.md) - holds between two entities where their co-occurrence is correlated by counts of publications in which both occur, using some threshold of occurrence as defined by the edge provider.
 * [orthologous to](orthologous_to.md) - a homology relationship between entities (typically genes) that diverged after a speciation event.
 * [overlaps](overlaps.md) - holds between entities that overlap in their extents (materials or processes)
 * [pairwise molecular interaction➞id](pairwise_molecular_interaction_id.md) - identifier for the interaction. This may come from an interaction database such as IMEX.
 * [paralogous to](paralogous_to.md) - a homology relationship that holds between entities (typically genes) that diverged after a duplication event.
 * [part of](part_of.md) - holds between parts and wholes (material entities or processes)
 * [participates in](participates_in.md) - holds between a continuant and a process, where the continuant is somehow involved in the process
 * [physically interacts with](physically_interacts_with.md) - holds between two entities that make physical contact as part of some interaction.  does not imply a causal relationship.
 * [positively correlated with](positively_correlated_with.md) - A relationship that holds between two concepts represented by variables for which a statistical correlation  is demonstrated, wherein variable values move together in the same direction (i.e. increased in one or  presence of one correlates with an increase or presence of the other).
 * [preceded by](preceded_by.md) - holds between two processes, where the other is completed before the one begins
 * [precedes](precedes.md) - holds between two processes, where one completes before the other begins
 * [predisposes](predisposes.md) - holds between two entities where exposure to one entity increases the chance of developing the other
 * [prevents](prevents.md) - holds between an entity whose application or use reduces the likelihood of a potential outcome. Typically used to associate a chemical entity, exposure, activity, or medical intervention that can prevent the onset a disease or phenotypic feature.
 * [produces](produces.md) - holds between a material entity and a product that is generated through the intentional actions or functioning of the material entity
 * [publication➞id](publication_id.md) - Different kinds of publication subtypes will have different preferred identifiers (curies when feasible). Precedence of identifiers for scientific articles is as follows: PMID if available; DOI if not; actual alternate CURIE otherwise. Enclosing publications (i.e. referenced by 'published in' node property) such as books and journals, should have industry-standard identifier such as from ISBN and ISSN.
 * [publication➞name](publication_name.md) - the 'title' of the publication is generally recorded in the 'name' property (inherited from NamedThing). The field name 'title' is now also tagged as an acceptable alias for the node property 'name' (just in case).
 * [response affected by](response_affected_by.md) - holds between two chemical entities where the susceptibility of a biological entity or system (e.g. an organism, cell, cellular component, macromolecular machine mixin, biological or pathological process) of one is affected by the action of the other.
 * [response decreased by](response_decreased_by.md)
 * [response increased by](response_increased_by.md)
 * [same as](same_as.md) - holds between two entities that are considered equivalent to each other
 * [sequence variant➞id](sequence_variant_id.md)
 * [serial➞id](serial_id.md) - Serials (journals) should have industry-standard identifier such as from ISSN.
 * [similar to](similar_to.md) - holds between an entity and some other entity with similar features.
 * [small molecule➞id](small_molecule_id.md)
 * [subclass of](subclass_of.md) - holds between two classes where the domain class is a specialization of the range class
 * [superclass of](superclass_of.md) - holds between two classes where the domain class is a super class of the range class
 * [synonym](synonym.md) - Alternate human-readable names for a thing
 * [treated by](treated_by.md) - holds between a disease or phenotypic feature and a therapeutic process or chemical entity that is used to treat the condition
 * [treats](treats.md) - holds between a therapeutic procedure or chemical entity and a disease or phenotypic feature that it is used to treat
 * [xenologous to](xenologous_to.md) - a homology relationship characterized by an interspecies (horizontal) transfer since the common ancestor.
 * [xref](xref.md) - Alternate CURIEs for a thing

### Types


### Enums

