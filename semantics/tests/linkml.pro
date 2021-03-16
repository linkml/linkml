slot(actively_involved_in).
domain(actively_involved_in, named_thing).
range(actively_involved_in, occurrent).
has_uri(actively_involved_in, 'http://w3id.org/biolink/vocab/actively_involved_in').
multivalued(actively_involved_in).
slot(affects).
domain(affects, named_thing).
range(affects, named_thing).
has_uri(affects, 'http://w3id.org/biolink/vocab/affects').
multivalued(affects).
slot(affects_abundance_of).
domain(affects_abundance_of, molecular_entity).
range(affects_abundance_of, molecular_entity).
has_uri(affects_abundance_of, 'http://w3id.org/biolink/vocab/affects_abundance_of').
multivalued(affects_abundance_of).
slot(affects_activity_of).
domain(affects_activity_of, molecular_entity).
range(affects_activity_of, molecular_entity).
has_uri(affects_activity_of, 'http://w3id.org/biolink/vocab/affects_activity_of').
multivalued(affects_activity_of).
slot(affects_degradation_of).
domain(affects_degradation_of, molecular_entity).
range(affects_degradation_of, molecular_entity).
has_uri(affects_degradation_of, 'http://w3id.org/biolink/vocab/affects_degradation_of').
multivalued(affects_degradation_of).
slot(affects_expression_of).
domain(affects_expression_of, molecular_entity).
range(affects_expression_of, genomic_entity).
has_uri(affects_expression_of, 'http://w3id.org/biolink/vocab/affects_expression_of').
multivalued(affects_expression_of).
slot(affects_folding_of).
domain(affects_folding_of, molecular_entity).
range(affects_folding_of, molecular_entity).
has_uri(affects_folding_of, 'http://w3id.org/biolink/vocab/affects_folding_of').
multivalued(affects_folding_of).
slot(affects_localization_of).
domain(affects_localization_of, molecular_entity).
range(affects_localization_of, molecular_entity).
has_uri(affects_localization_of, 'http://w3id.org/biolink/vocab/affects_localization_of').
multivalued(affects_localization_of).
slot(affects_metabolic_processing_of).
domain(affects_metabolic_processing_of, molecular_entity).
range(affects_metabolic_processing_of, molecular_entity).
has_uri(affects_metabolic_processing_of, 'http://w3id.org/biolink/vocab/affects_metabolic_processing_of').
multivalued(affects_metabolic_processing_of).
slot(affects_molecular_modification_of).
domain(affects_molecular_modification_of, molecular_entity).
range(affects_molecular_modification_of, molecular_entity).
has_uri(affects_molecular_modification_of, 'http://w3id.org/biolink/vocab/affects_molecular_modification_of').
multivalued(affects_molecular_modification_of).
slot(affects_mutation_rate_of).
domain(affects_mutation_rate_of, molecular_entity).
range(affects_mutation_rate_of, genomic_entity).
has_uri(affects_mutation_rate_of, 'http://w3id.org/biolink/vocab/affects_mutation_rate_of').
multivalued(affects_mutation_rate_of).
slot(affects_response_to).
domain(affects_response_to, molecular_entity).
range(affects_response_to, molecular_entity).
has_uri(affects_response_to, 'http://w3id.org/biolink/vocab/affects_response_to').
multivalued(affects_response_to).
slot(affects_risk_for).
domain(affects_risk_for, named_thing).
range(affects_risk_for, named_thing).
has_uri(affects_risk_for, 'http://w3id.org/biolink/vocab/affects_risk_for').
multivalued(affects_risk_for).
slot(affects_secretion_of).
domain(affects_secretion_of, molecular_entity).
range(affects_secretion_of, molecular_entity).
has_uri(affects_secretion_of, 'http://w3id.org/biolink/vocab/affects_secretion_of').
multivalued(affects_secretion_of).
slot(affects_splicing_of).
domain(affects_splicing_of, molecular_entity).
range(affects_splicing_of, transcript).
has_uri(affects_splicing_of, 'http://w3id.org/biolink/vocab/affects_splicing_of').
multivalued(affects_splicing_of).
slot(affects_stability_of).
domain(affects_stability_of, molecular_entity).
range(affects_stability_of, molecular_entity).
has_uri(affects_stability_of, 'http://w3id.org/biolink/vocab/affects_stability_of').
multivalued(affects_stability_of).
slot(affects_synthesis_of).
domain(affects_synthesis_of, molecular_entity).
range(affects_synthesis_of, molecular_entity).
has_uri(affects_synthesis_of, 'http://w3id.org/biolink/vocab/affects_synthesis_of').
multivalued(affects_synthesis_of).
slot(affects_transport_of).
domain(affects_transport_of, molecular_entity).
range(affects_transport_of, molecular_entity).
has_uri(affects_transport_of, 'http://w3id.org/biolink/vocab/affects_transport_of').
multivalued(affects_transport_of).
slot(affects_uptake_of).
domain(affects_uptake_of, molecular_entity).
range(affects_uptake_of, molecular_entity).
has_uri(affects_uptake_of, 'http://w3id.org/biolink/vocab/affects_uptake_of').
multivalued(affects_uptake_of).
slot(aggregate_statistic).
domain(aggregate_statistic, named_thing).
range(aggregate_statistic, string).
has_uri(aggregate_statistic, 'http://w3id.org/biolink/vocab/aggregate_statistic').
slot(object).
domain(object, anatomical_entity_to_anatomical_entity_association).
range(object, anatomical_entity).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(subject).
domain(subject, anatomical_entity_to_anatomical_entity_association).
range(subject, anatomical_entity).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(object).
domain(object, anatomical_entity_to_anatomical_entity_ontogenic_association).
range(object, anatomical_entity).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(relation).
domain(relation, anatomical_entity_to_anatomical_entity_ontogenic_association).
range(relation, iri_type).
has_uri(relation, 'http://w3id.org/biolink/vocab/relation').
required(relation).
slot(subject).
domain(subject, anatomical_entity_to_anatomical_entity_ontogenic_association).
range(subject, anatomical_entity).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(object).
domain(object, anatomical_entity_to_anatomical_entity_part_of_association).
range(object, anatomical_entity).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(relation).
domain(relation, anatomical_entity_to_anatomical_entity_part_of_association).
range(relation, iri_type).
has_uri(relation, 'http://w3id.org/biolink/vocab/relation').
required(relation).
slot(subject).
domain(subject, anatomical_entity_to_anatomical_entity_part_of_association).
range(subject, anatomical_entity).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(association_slot).
domain(association_slot, association).
range(association_slot, string).
has_uri(association_slot, 'http://w3id.org/biolink/vocab/association_slot').
slot(association_type).
domain(association_type, association).
range(association_type, ontology_class).
has_uri(association_type, 'http://w3id.org/biolink/vocab/association_type').
slot(id).
domain(id, association).
range(id, identifier_type).
has_uri(id, 'http://w3id.org/biolink/vocab/id').
required(id).
slot(biomarker_for).
domain(biomarker_for, molecular_entity).
range(biomarker_for, disease_or_phenotypic_feature).
has_uri(biomarker_for, 'http://w3id.org/biolink/vocab/biomarker_for').
multivalued(biomarker_for).
slot(subject).
domain(subject, biosample_to_thing_association).
range(subject, biosample).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(capable_of).
domain(capable_of, named_thing).
range(capable_of, occurrent).
has_uri(capable_of, 'http://w3id.org/biolink/vocab/capable_of').
multivalued(capable_of).
slot(subject).
domain(subject, case_to_thing_association).
range(subject, case).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(category).
domain(category, named_thing).
range(category, iri_type).
has_uri(category, 'http://w3id.org/biolink/vocab/category').
multivalued(category).
slot(causes).
domain(causes, named_thing).
range(causes, named_thing).
has_uri(causes, 'http://w3id.org/biolink/vocab/causes').
multivalued(causes).
slot(subject).
domain(subject, cell_line_to_disease_or_phenotypic_feature_association).
range(subject, disease_or_phenotypic_feature).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(subject).
domain(subject, cell_line_to_thing_association).
range(subject, cell_line).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(object).
domain(object, chemical_to_disease_or_phenotypic_feature_association).
range(object, disease_or_phenotypic_feature).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(object).
domain(object, chemical_to_gene_association).
range(object, gene_or_gene_product).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(object).
domain(object, chemical_to_pathway_association).
range(object, pathway).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(subject).
domain(subject, chemical_to_thing_association).
range(subject, chemical_substance).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(clinical_modifier_qualifier).
domain(clinical_modifier_qualifier, association).
range(clinical_modifier_qualifier, clinical_modifier).
has_uri(clinical_modifier_qualifier, 'http://w3id.org/biolink/vocab/clinical_modifier_qualifier').
slot(coexists_with).
domain(coexists_with, named_thing).
range(coexists_with, named_thing).
has_uri(coexists_with, 'http://w3id.org/biolink/vocab/coexists_with').
multivalued(coexists_with).
slot(colocalizes_with).
domain(colocalizes_with, named_thing).
range(colocalizes_with, named_thing).
has_uri(colocalizes_with, 'http://w3id.org/biolink/vocab/colocalizes_with').
multivalued(colocalizes_with).
slot(contributes_to).
domain(contributes_to, named_thing).
range(contributes_to, named_thing).
has_uri(contributes_to, 'http://w3id.org/biolink/vocab/contributes_to').
multivalued(contributes_to).
slot(correlated_with).
domain(correlated_with, disease_or_phenotypic_feature).
range(correlated_with, molecular_entity).
has_uri(correlated_with, 'http://w3id.org/biolink/vocab/correlated_with').
multivalued(correlated_with).
slot(creation_date).
domain(creation_date, named_thing).
range(creation_date, date).
has_uri(creation_date, 'http://w3id.org/biolink/vocab/creation_date').
slot(decreases_abundance_of).
domain(decreases_abundance_of, molecular_entity).
range(decreases_abundance_of, molecular_entity).
has_uri(decreases_abundance_of, 'http://w3id.org/biolink/vocab/decreases_abundance_of').
multivalued(decreases_abundance_of).
slot(decreases_activity_of).
domain(decreases_activity_of, molecular_entity).
range(decreases_activity_of, molecular_entity).
has_uri(decreases_activity_of, 'http://w3id.org/biolink/vocab/decreases_activity_of').
multivalued(decreases_activity_of).
slot(decreases_degradation_of).
domain(decreases_degradation_of, molecular_entity).
range(decreases_degradation_of, molecular_entity).
has_uri(decreases_degradation_of, 'http://w3id.org/biolink/vocab/decreases_degradation_of').
multivalued(decreases_degradation_of).
slot(decreases_expression_of).
domain(decreases_expression_of, molecular_entity).
range(decreases_expression_of, genomic_entity).
has_uri(decreases_expression_of, 'http://w3id.org/biolink/vocab/decreases_expression_of').
multivalued(decreases_expression_of).
slot(decreases_folding_of).
domain(decreases_folding_of, molecular_entity).
range(decreases_folding_of, molecular_entity).
has_uri(decreases_folding_of, 'http://w3id.org/biolink/vocab/decreases_folding_of').
multivalued(decreases_folding_of).
slot(decreases_localization_of).
domain(decreases_localization_of, molecular_entity).
range(decreases_localization_of, molecular_entity).
has_uri(decreases_localization_of, 'http://w3id.org/biolink/vocab/decreases_localization_of').
multivalued(decreases_localization_of).
slot(decreases_metabolic_processing_of).
domain(decreases_metabolic_processing_of, molecular_entity).
range(decreases_metabolic_processing_of, molecular_entity).
has_uri(decreases_metabolic_processing_of, 'http://w3id.org/biolink/vocab/decreases_metabolic_processing_of').
multivalued(decreases_metabolic_processing_of).
slot(decreases_molecular_modification_of).
domain(decreases_molecular_modification_of, molecular_entity).
range(decreases_molecular_modification_of, molecular_entity).
has_uri(decreases_molecular_modification_of, 'http://w3id.org/biolink/vocab/decreases_molecular_modification_of').
multivalued(decreases_molecular_modification_of).
slot(decreases_mutation_rate_of).
domain(decreases_mutation_rate_of, molecular_entity).
range(decreases_mutation_rate_of, genomic_entity).
has_uri(decreases_mutation_rate_of, 'http://w3id.org/biolink/vocab/decreases_mutation_rate_of').
multivalued(decreases_mutation_rate_of).
slot(decreases_response_to).
domain(decreases_response_to, molecular_entity).
range(decreases_response_to, molecular_entity).
has_uri(decreases_response_to, 'http://w3id.org/biolink/vocab/decreases_response_to').
multivalued(decreases_response_to).
slot(decreases_secretion_of).
domain(decreases_secretion_of, molecular_entity).
range(decreases_secretion_of, molecular_entity).
has_uri(decreases_secretion_of, 'http://w3id.org/biolink/vocab/decreases_secretion_of').
multivalued(decreases_secretion_of).
slot(decreases_splicing_of).
domain(decreases_splicing_of, molecular_entity).
range(decreases_splicing_of, transcript).
has_uri(decreases_splicing_of, 'http://w3id.org/biolink/vocab/decreases_splicing_of').
multivalued(decreases_splicing_of).
slot(decreases_stability_of).
domain(decreases_stability_of, molecular_entity).
range(decreases_stability_of, molecular_entity).
has_uri(decreases_stability_of, 'http://w3id.org/biolink/vocab/decreases_stability_of').
multivalued(decreases_stability_of).
slot(decreases_synthesis_of).
domain(decreases_synthesis_of, molecular_entity).
range(decreases_synthesis_of, molecular_entity).
has_uri(decreases_synthesis_of, 'http://w3id.org/biolink/vocab/decreases_synthesis_of').
multivalued(decreases_synthesis_of).
slot(decreases_transport_of).
domain(decreases_transport_of, molecular_entity).
range(decreases_transport_of, molecular_entity).
has_uri(decreases_transport_of, 'http://w3id.org/biolink/vocab/decreases_transport_of').
multivalued(decreases_transport_of).
slot(decreases_uptake_of).
domain(decreases_uptake_of, molecular_entity).
range(decreases_uptake_of, molecular_entity).
has_uri(decreases_uptake_of, 'http://w3id.org/biolink/vocab/decreases_uptake_of').
multivalued(decreases_uptake_of).
slot(derives_from).
domain(derives_from, named_thing).
range(derives_from, named_thing).
has_uri(derives_from, 'http://w3id.org/biolink/vocab/derives_from').
multivalued(derives_from).
slot(derives_into).
domain(derives_into, named_thing).
range(derives_into, named_thing).
has_uri(derives_into, 'http://w3id.org/biolink/vocab/derives_into').
multivalued(derives_into).
slot(description).
domain(description, named_thing).
range(description, narrative_text).
has_uri(description, 'http://w3id.org/biolink/vocab/description').
slot(object).
domain(object, disease_or_phenotypic_feature_association_to_location_association).
range(object, anatomical_entity).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(subject).
domain(subject, disease_or_phenotypic_feature_association_to_thing_association).
range(subject, disease_or_phenotypic_feature).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(subject).
domain(subject, disease_to_thing_association).
range(subject, disease).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(disrupts).
domain(disrupts, named_thing).
range(disrupts, named_thing).
has_uri(disrupts, 'http://w3id.org/biolink/vocab/disrupts').
multivalued(disrupts).
slot(drug).
domain(drug, drug_exposure).
range(drug, chemical_substance).
has_uri(drug, 'http://w3id.org/biolink/vocab/drug').
multivalued(drug).
required(drug).
slot(edge_label).
domain(edge_label, association).
range(edge_label, label_type).
has_uri(edge_label, 'http://w3id.org/biolink/vocab/edge_label').
slot(end_interbase_coordinate).
domain(end_interbase_coordinate, genomic_sequence_localization).
range(end_interbase_coordinate, string).
has_uri(end_interbase_coordinate, 'http://w3id.org/biolink/vocab/end_interbase_coordinate').
slot(object).
domain(object, entity_to_disease_association).
range(object, disease).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(description).
domain(description, entity_to_phenotypic_feature_association).
range(description, narrative_text).
has_uri(description, 'http://w3id.org/biolink/vocab/description').
slot(object).
domain(object, entity_to_phenotypic_feature_association).
range(object, phenotypic_feature).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(subject).
domain(subject, environment_to_phenotypic_feature_association).
range(subject, environment).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(object).
domain(object, exon_to_transcript_relationship).
range(object, transcript).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(subject).
domain(subject, exon_to_transcript_relationship).
range(subject, exon).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(expressed_in).
domain(expressed_in, gene_or_gene_product).
range(expressed_in, anatomical_entity).
has_uri(expressed_in, 'http://w3id.org/biolink/vocab/expressed_in').
multivalued(expressed_in).
slot(expresses).
domain(expresses, anatomical_entity).
range(expresses, gene_or_gene_product).
has_uri(expresses, 'http://w3id.org/biolink/vocab/expresses').
multivalued(expresses).
slot(filler).
domain(filler, named_thing).
range(filler, named_thing).
has_uri(filler, 'http://w3id.org/biolink/vocab/filler').
slot(frequency_qualifier).
domain(frequency_qualifier, frequency_qualifier_mixin).
range(frequency_qualifier, frequency_value).
has_uri(frequency_qualifier, 'http://w3id.org/biolink/vocab/frequency_qualifier').
slot(full_name).
domain(full_name, named_thing).
range(full_name, label_type).
has_uri(full_name, 'http://w3id.org/biolink/vocab/full_name').
slot(object).
domain(object, functional_association).
range(object, gene_ontology_class).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(subject).
domain(subject, functional_association).
range(subject, macromolecular_machine).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(subject).
domain(subject, gene_as_a_model_of_disease_association).
range(subject, gene_or_gene_product).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(gene_associated_with_condition).
domain(gene_associated_with_condition, gene).
range(gene_associated_with_condition, disease_or_phenotypic_feature).
has_uri(gene_associated_with_condition, 'http://w3id.org/biolink/vocab/gene_associated_with_condition').
multivalued(gene_associated_with_condition).
slot(subject).
domain(subject, gene_has_variant_that_contributes_to_disease_association).
range(subject, gene_or_gene_product).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(object).
domain(object, gene_regulatory_relationship).
range(object, gene_or_gene_product).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(relation).
domain(relation, gene_regulatory_relationship).
range(relation, iri_type).
has_uri(relation, 'http://w3id.org/biolink/vocab/relation').
required(relation).
slot(subject).
domain(subject, gene_regulatory_relationship).
range(subject, gene_or_gene_product).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(subject).
domain(subject, gene_to_disease_association).
range(subject, gene_or_gene_product).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(object).
domain(object, gene_to_expression_site_association).
range(object, anatomical_entity).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(quantifier_qualifier).
domain(quantifier_qualifier, gene_to_expression_site_association).
range(quantifier_qualifier, ontology_class).
has_uri(quantifier_qualifier, 'http://w3id.org/biolink/vocab/quantifier_qualifier').
slot(relation).
domain(relation, gene_to_expression_site_association).
range(relation, iri_type).
has_uri(relation, 'http://w3id.org/biolink/vocab/relation').
required(relation).
slot(stage_qualifier).
domain(stage_qualifier, gene_to_expression_site_association).
range(stage_qualifier, life_stage).
has_uri(stage_qualifier, 'http://w3id.org/biolink/vocab/stage_qualifier').
slot(subject).
domain(subject, gene_to_expression_site_association).
range(subject, gene_or_gene_product).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(object).
domain(object, gene_to_gene_association).
range(object, gene_or_gene_product).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(subject).
domain(subject, gene_to_gene_association).
range(subject, gene_or_gene_product).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(relation).
domain(relation, gene_to_gene_homology_association).
range(relation, iri_type).
has_uri(relation, 'http://w3id.org/biolink/vocab/relation').
required(relation).
slot(object).
domain(object, gene_to_gene_product_relationship).
range(object, gene_product).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(relation).
domain(relation, gene_to_gene_product_relationship).
range(relation, iri_type).
has_uri(relation, 'http://w3id.org/biolink/vocab/relation').
required(relation).
slot(subject).
domain(subject, gene_to_gene_product_relationship).
range(subject, gene).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(object).
domain(object, gene_to_go_term_association).
range(object, gene_ontology_class).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(subject).
domain(subject, gene_to_go_term_association).
range(subject, molecular_entity).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(subject).
domain(subject, gene_to_phenotypic_feature_association).
range(subject, gene_or_gene_product).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(subject).
domain(subject, gene_to_thing_association).
range(subject, gene_or_gene_product).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(genetically_interacts_with).
domain(genetically_interacts_with, gene).
range(genetically_interacts_with, gene).
has_uri(genetically_interacts_with, 'http://w3id.org/biolink/vocab/genetically_interacts_with').
multivalued(genetically_interacts_with).
slot(genome_build).
domain(genome_build, genomic_sequence_localization).
range(genome_build, string).
has_uri(genome_build, 'http://w3id.org/biolink/vocab/genome_build').
slot(object).
domain(object, genomic_sequence_localization).
range(object, genomic_entity).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(subject).
domain(subject, genomic_sequence_localization).
range(subject, genomic_entity).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(object).
domain(object, genotype_to_gene_association).
range(object, gene).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(relation).
domain(relation, genotype_to_gene_association).
range(relation, iri_type).
has_uri(relation, 'http://w3id.org/biolink/vocab/relation').
required(relation).
slot(subject).
domain(subject, genotype_to_gene_association).
range(subject, genotype).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(object).
domain(object, genotype_to_genotype_part_association).
range(object, genotype).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(relation).
domain(relation, genotype_to_genotype_part_association).
range(relation, iri_type).
has_uri(relation, 'http://w3id.org/biolink/vocab/relation').
required(relation).
slot(subject).
domain(subject, genotype_to_genotype_part_association).
range(subject, genotype).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(relation).
domain(relation, genotype_to_phenotypic_feature_association).
range(relation, iri_type).
has_uri(relation, 'http://w3id.org/biolink/vocab/relation').
required(relation).
slot(subject).
domain(subject, genotype_to_phenotypic_feature_association).
range(subject, genotype).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(subject).
domain(subject, genotype_to_thing_association).
range(subject, genotype).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(object).
domain(object, genotype_to_variant_association).
range(object, sequence_variant).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(relation).
domain(relation, genotype_to_variant_association).
range(relation, iri_type).
has_uri(relation, 'http://w3id.org/biolink/vocab/relation').
required(relation).
slot(subject).
domain(subject, genotype_to_variant_association).
range(subject, genotype).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(has_biological_sequence).
domain(has_biological_sequence, genomic_entity).
range(has_biological_sequence, biological_sequence).
has_uri(has_biological_sequence, 'http://w3id.org/biolink/vocab/has_biological_sequence').
slot(has_biomarker).
domain(has_biomarker, disease_or_phenotypic_feature).
range(has_biomarker, molecular_entity).
has_uri(has_biomarker, 'http://w3id.org/biolink/vocab/has_biomarker').
multivalued(has_biomarker).
slot(has_chemical_formula).
domain(has_chemical_formula, named_thing).
range(has_chemical_formula, chemical_formula_value).
has_uri(has_chemical_formula, 'http://w3id.org/biolink/vocab/has_chemical_formula').
slot(has_confidence_level).
domain(has_confidence_level, association).
range(has_confidence_level, confidence_level).
has_uri(has_confidence_level, 'http://w3id.org/biolink/vocab/has_confidence_level').
slot(has_count).
domain(has_count, frequency_quantifier).
range(has_count, integer).
has_uri(has_count, 'http://w3id.org/biolink/vocab/has_count').
slot(has_evidence).
domain(has_evidence, association).
range(has_evidence, evidence_type).
has_uri(has_evidence, 'http://w3id.org/biolink/vocab/has_evidence').
slot(has_exposure_parts).
domain(has_exposure_parts, treatment).
range(has_exposure_parts, drug_exposure).
has_uri(has_exposure_parts, 'http://w3id.org/biolink/vocab/has_exposure_parts').
multivalued(has_exposure_parts).
required(has_exposure_parts).
slot(has_gene).
domain(has_gene, sequence_variant).
range(has_gene, gene).
has_uri(has_gene, 'http://w3id.org/biolink/vocab/has_gene').
slot(has_gene_product).
domain(has_gene_product, gene).
range(has_gene_product, gene_product).
has_uri(has_gene_product, 'http://w3id.org/biolink/vocab/has_gene_product').
multivalued(has_gene_product).
slot(has_input).
domain(has_input, occurrent).
range(has_input, named_thing).
has_uri(has_input, 'http://w3id.org/biolink/vocab/has_input').
multivalued(has_input).
slot(has_molecular_consequence).
domain(has_molecular_consequence, named_thing).
range(has_molecular_consequence, ontology_class).
has_uri(has_molecular_consequence, 'http://w3id.org/biolink/vocab/has_molecular_consequence').
multivalued(has_molecular_consequence).
slot(has_part).
domain(has_part, named_thing).
range(has_part, named_thing).
has_uri(has_part, 'http://w3id.org/biolink/vocab/has_part').
multivalued(has_part).
slot(has_participant).
domain(has_participant, occurrent).
range(has_participant, named_thing).
has_uri(has_participant, 'http://w3id.org/biolink/vocab/has_participant').
multivalued(has_participant).
slot(has_percentage).
domain(has_percentage, frequency_quantifier).
range(has_percentage, double).
has_uri(has_percentage, 'http://w3id.org/biolink/vocab/has_percentage').
slot(has_phenotype).
domain(has_phenotype, biological_entity).
range(has_phenotype, phenotypic_feature).
has_uri(has_phenotype, 'http://w3id.org/biolink/vocab/has_phenotype').
multivalued(has_phenotype).
slot(has_quotient).
domain(has_quotient, frequency_quantifier).
range(has_quotient, double).
has_uri(has_quotient, 'http://w3id.org/biolink/vocab/has_quotient').
slot(has_total).
domain(has_total, frequency_quantifier).
range(has_total, integer).
has_uri(has_total, 'http://w3id.org/biolink/vocab/has_total').
slot(has_zygosity).
domain(has_zygosity, genotype).
range(has_zygosity, zygosity).
has_uri(has_zygosity, 'http://w3id.org/biolink/vocab/has_zygosity').
slot(homologous_to).
domain(homologous_to, named_thing).
range(homologous_to, named_thing).
has_uri(homologous_to, 'http://w3id.org/biolink/vocab/homologous_to').
multivalued(homologous_to).
slot(id).
domain(id, named_thing).
range(id, identifier_type).
has_uri(id, 'http://w3id.org/biolink/vocab/id').
required(id).
slot(in_cell_population_with).
domain(in_cell_population_with, gene_or_gene_product).
range(in_cell_population_with, gene_or_gene_product).
has_uri(in_cell_population_with, 'http://w3id.org/biolink/vocab/in_cell_population_with').
multivalued(in_cell_population_with).
slot(in_complex_with).
domain(in_complex_with, gene_or_gene_product).
range(in_complex_with, gene_or_gene_product).
has_uri(in_complex_with, 'http://w3id.org/biolink/vocab/in_complex_with').
multivalued(in_complex_with).
slot(in_pathway_with).
domain(in_pathway_with, gene_or_gene_product).
range(in_pathway_with, gene_or_gene_product).
has_uri(in_pathway_with, 'http://w3id.org/biolink/vocab/in_pathway_with').
multivalued(in_pathway_with).
slot(in_taxon).
domain(in_taxon, thing_with_taxon).
range(in_taxon, organism_taxon).
has_uri(in_taxon, 'http://w3id.org/biolink/vocab/in_taxon').
multivalued(in_taxon).
slot(increases_abundance_of).
domain(increases_abundance_of, molecular_entity).
range(increases_abundance_of, molecular_entity).
has_uri(increases_abundance_of, 'http://w3id.org/biolink/vocab/increases_abundance_of').
multivalued(increases_abundance_of).
slot(increases_activity_of).
domain(increases_activity_of, molecular_entity).
range(increases_activity_of, molecular_entity).
has_uri(increases_activity_of, 'http://w3id.org/biolink/vocab/increases_activity_of').
multivalued(increases_activity_of).
slot(increases_degradation_of).
domain(increases_degradation_of, molecular_entity).
range(increases_degradation_of, molecular_entity).
has_uri(increases_degradation_of, 'http://w3id.org/biolink/vocab/increases_degradation_of').
multivalued(increases_degradation_of).
slot(increases_expression_of).
domain(increases_expression_of, molecular_entity).
range(increases_expression_of, genomic_entity).
has_uri(increases_expression_of, 'http://w3id.org/biolink/vocab/increases_expression_of').
multivalued(increases_expression_of).
slot(increases_folding_of).
domain(increases_folding_of, molecular_entity).
range(increases_folding_of, molecular_entity).
has_uri(increases_folding_of, 'http://w3id.org/biolink/vocab/increases_folding_of').
multivalued(increases_folding_of).
slot(increases_localization_of).
domain(increases_localization_of, molecular_entity).
range(increases_localization_of, molecular_entity).
has_uri(increases_localization_of, 'http://w3id.org/biolink/vocab/increases_localization_of').
multivalued(increases_localization_of).
slot(increases_metabolic_processing_of).
domain(increases_metabolic_processing_of, molecular_entity).
range(increases_metabolic_processing_of, molecular_entity).
has_uri(increases_metabolic_processing_of, 'http://w3id.org/biolink/vocab/increases_metabolic_processing_of').
multivalued(increases_metabolic_processing_of).
slot(increases_molecular_modification_of).
domain(increases_molecular_modification_of, molecular_entity).
range(increases_molecular_modification_of, molecular_entity).
has_uri(increases_molecular_modification_of, 'http://w3id.org/biolink/vocab/increases_molecular_modification_of').
multivalued(increases_molecular_modification_of).
slot(increases_mutation_rate_of).
domain(increases_mutation_rate_of, molecular_entity).
range(increases_mutation_rate_of, genomic_entity).
has_uri(increases_mutation_rate_of, 'http://w3id.org/biolink/vocab/increases_mutation_rate_of').
multivalued(increases_mutation_rate_of).
slot(increases_response_to).
domain(increases_response_to, molecular_entity).
range(increases_response_to, molecular_entity).
has_uri(increases_response_to, 'http://w3id.org/biolink/vocab/increases_response_to').
multivalued(increases_response_to).
slot(increases_secretion_of).
domain(increases_secretion_of, molecular_entity).
range(increases_secretion_of, molecular_entity).
has_uri(increases_secretion_of, 'http://w3id.org/biolink/vocab/increases_secretion_of').
multivalued(increases_secretion_of).
slot(increases_splicing_of).
domain(increases_splicing_of, molecular_entity).
range(increases_splicing_of, transcript).
has_uri(increases_splicing_of, 'http://w3id.org/biolink/vocab/increases_splicing_of').
multivalued(increases_splicing_of).
slot(increases_stability_of).
domain(increases_stability_of, molecular_entity).
range(increases_stability_of, molecular_entity).
has_uri(increases_stability_of, 'http://w3id.org/biolink/vocab/increases_stability_of').
multivalued(increases_stability_of).
slot(increases_synthesis_of).
domain(increases_synthesis_of, molecular_entity).
range(increases_synthesis_of, molecular_entity).
has_uri(increases_synthesis_of, 'http://w3id.org/biolink/vocab/increases_synthesis_of').
multivalued(increases_synthesis_of).
slot(increases_transport_of).
domain(increases_transport_of, molecular_entity).
range(increases_transport_of, molecular_entity).
has_uri(increases_transport_of, 'http://w3id.org/biolink/vocab/increases_transport_of').
multivalued(increases_transport_of).
slot(increases_uptake_of).
domain(increases_uptake_of, molecular_entity).
range(increases_uptake_of, molecular_entity).
has_uri(increases_uptake_of, 'http://w3id.org/biolink/vocab/increases_uptake_of').
multivalued(increases_uptake_of).
slot(interacting_molecules_category).
domain(interacting_molecules_category, pairwise_interaction_association).
range(interacting_molecules_category, ontology_class).
has_uri(interacting_molecules_category, 'http://w3id.org/biolink/vocab/interacting_molecules_category').
slot(interacts_with).
domain(interacts_with, named_thing).
range(interacts_with, named_thing).
has_uri(interacts_with, 'http://w3id.org/biolink/vocab/interacts_with').
multivalued(interacts_with).
slot(interbase_coordinate).
domain(interbase_coordinate, named_thing).
range(interbase_coordinate, string).
has_uri(interbase_coordinate, 'http://w3id.org/biolink/vocab/interbase_coordinate').
slot(iri).
domain(iri, named_thing).
range(iri, iri_type).
has_uri(iri, 'http://w3id.org/biolink/vocab/iri').
slot(latitude).
domain(latitude, geographic_location).
range(latitude, float).
has_uri(latitude, 'http://w3id.org/biolink/vocab/latitude').
slot(located_in).
domain(located_in, named_thing).
range(located_in, named_thing).
has_uri(located_in, 'http://w3id.org/biolink/vocab/located_in').
multivalued(located_in).
slot(location_of).
domain(location_of, named_thing).
range(location_of, named_thing).
has_uri(location_of, 'http://w3id.org/biolink/vocab/location_of').
multivalued(location_of).
slot(longitude).
domain(longitude, geographic_location).
range(longitude, float).
has_uri(longitude, 'http://w3id.org/biolink/vocab/longitude').
slot(object).
domain(object, macromolecular_machine_to_biological_process_association).
range(object, biological_process).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(object).
domain(object, macromolecular_machine_to_cellular_component_association).
range(object, cellular_component).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(object).
domain(object, macromolecular_machine_to_molecular_activity_association).
range(object, molecular_activity).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(name).
domain(name, macromolecular_machine).
range(name, symbol_type).
has_uri(name, 'http://w3id.org/biolink/vocab/name').
slot(manifestation_of).
domain(manifestation_of, named_thing).
range(manifestation_of, disease).
has_uri(manifestation_of, 'http://w3id.org/biolink/vocab/manifestation_of').
multivalued(manifestation_of).
slot(model_of).
domain(model_of, named_thing).
range(model_of, named_thing).
has_uri(model_of, 'http://w3id.org/biolink/vocab/model_of').
multivalued(model_of).
slot(relation).
domain(relation, model_to_disease_mixin).
range(relation, iri_type).
has_uri(relation, 'http://w3id.org/biolink/vocab/relation').
required(relation).
slot(subject).
domain(subject, model_to_disease_mixin).
range(subject, iri_type).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(molecularly_interacts_with).
domain(molecularly_interacts_with, molecular_entity).
range(molecularly_interacts_with, molecular_entity).
has_uri(molecularly_interacts_with, 'http://w3id.org/biolink/vocab/molecularly_interacts_with').
multivalued(molecularly_interacts_with).
slot(name).
domain(name, named_thing).
range(name, label_type).
has_uri(name, 'http://w3id.org/biolink/vocab/name').
slot(negated).
domain(negated, association).
range(negated, boolean).
has_uri(negated, 'http://w3id.org/biolink/vocab/negated').
slot(negatively_regulates).
domain(negatively_regulates, named_thing).
range(negatively_regulates, named_thing).
has_uri(negatively_regulates, 'http://w3id.org/biolink/vocab/negatively_regulates').
multivalued(negatively_regulates).
slot(negatively_regulates_entity_to_entity).
domain(negatively_regulates_entity_to_entity, molecular_entity).
range(negatively_regulates_entity_to_entity, molecular_entity).
mixin(negatively_regulates_entity_to_entity, negatively_regulates).
has_uri(negatively_regulates_entity_to_entity, 'http://w3id.org/biolink/vocab/negatively_regulates_entity_to_entity').
multivalued(negatively_regulates_entity_to_entity).
slot(negatively_regulates_process_to_process).
domain(negatively_regulates_process_to_process, occurrent).
range(negatively_regulates_process_to_process, occurrent).
mixin(negatively_regulates_process_to_process, negatively_regulates).
has_uri(negatively_regulates_process_to_process, 'http://w3id.org/biolink/vocab/negatively_regulates_process_to_process').
multivalued(negatively_regulates_process_to_process).
slot(node_property).
domain(node_property, named_thing).
range(node_property, string).
has_uri(node_property, 'http://w3id.org/biolink/vocab/node_property').
slot(object).
domain(object, association).
range(object, iri_type).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(occurs_in).
domain(occurs_in, named_thing).
range(occurs_in, named_thing).
has_uri(occurs_in, 'http://w3id.org/biolink/vocab/occurs_in').
multivalued(occurs_in).
slot(onset_qualifier).
domain(onset_qualifier, entity_to_feature_or_disease_qualifiers).
range(onset_qualifier, onset).
has_uri(onset_qualifier, 'http://w3id.org/biolink/vocab/onset_qualifier').
slot(orthologous_to).
domain(orthologous_to, named_thing).
range(orthologous_to, named_thing).
has_uri(orthologous_to, 'http://w3id.org/biolink/vocab/orthologous_to').
multivalued(orthologous_to).
slot(overlaps).
domain(overlaps, named_thing).
range(overlaps, named_thing).
has_uri(overlaps, 'http://w3id.org/biolink/vocab/overlaps').
multivalued(overlaps).
slot(relation).
domain(relation, pairwise_gene_to_gene_interaction).
range(relation, iri_type).
has_uri(relation, 'http://w3id.org/biolink/vocab/relation').
required(relation).
slot(id).
domain(id, pairwise_interaction_association).
range(id, identifier_type).
has_uri(id, 'http://w3id.org/biolink/vocab/id').
required(id).
slot(object).
domain(object, pairwise_interaction_association).
range(object, molecular_entity).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(relation).
domain(relation, pairwise_interaction_association).
range(relation, iri_type).
has_uri(relation, 'http://w3id.org/biolink/vocab/relation').
required(relation).
slot(subject).
domain(subject, pairwise_interaction_association).
range(subject, molecular_entity).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(paralogous_to).
domain(paralogous_to, named_thing).
range(paralogous_to, named_thing).
has_uri(paralogous_to, 'http://w3id.org/biolink/vocab/paralogous_to').
multivalued(paralogous_to).
slot(part_of).
domain(part_of, named_thing).
range(part_of, named_thing).
has_uri(part_of, 'http://w3id.org/biolink/vocab/part_of').
multivalued(part_of).
slot(participates_in).
domain(participates_in, named_thing).
range(participates_in, occurrent).
has_uri(participates_in, 'http://w3id.org/biolink/vocab/participates_in').
multivalued(participates_in).
slot(phase).
domain(phase, genomic_sequence_localization).
range(phase, string).
has_uri(phase, 'http://w3id.org/biolink/vocab/phase').
slot(physically_interacts_with).
domain(physically_interacts_with, named_thing).
range(physically_interacts_with, named_thing).
has_uri(physically_interacts_with, 'http://w3id.org/biolink/vocab/physically_interacts_with').
multivalued(physically_interacts_with).
slot(object).
domain(object, population_to_population_association).
range(object, population_of_individual_organisms).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(relation).
domain(relation, population_to_population_association).
range(relation, iri_type).
has_uri(relation, 'http://w3id.org/biolink/vocab/relation').
required(relation).
slot(subject).
domain(subject, population_to_population_association).
range(subject, population_of_individual_organisms).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(positively_regulates).
domain(positively_regulates, named_thing).
range(positively_regulates, named_thing).
has_uri(positively_regulates, 'http://w3id.org/biolink/vocab/positively_regulates').
multivalued(positively_regulates).
slot(positively_regulates_entity_to_entity).
domain(positively_regulates_entity_to_entity, molecular_entity).
range(positively_regulates_entity_to_entity, molecular_entity).
mixin(positively_regulates_entity_to_entity, positively_regulates).
has_uri(positively_regulates_entity_to_entity, 'http://w3id.org/biolink/vocab/positively_regulates_entity_to_entity').
multivalued(positively_regulates_entity_to_entity).
slot(positively_regulates_process_to_process).
domain(positively_regulates_process_to_process, occurrent).
range(positively_regulates_process_to_process, occurrent).
mixin(positively_regulates_process_to_process, positively_regulates).
has_uri(positively_regulates_process_to_process, 'http://w3id.org/biolink/vocab/positively_regulates_process_to_process').
multivalued(positively_regulates_process_to_process).
slot(precedes).
domain(precedes, occurrent).
range(precedes, occurrent).
has_uri(precedes, 'http://w3id.org/biolink/vocab/precedes').
multivalued(precedes).
slot(predisposes).
domain(predisposes, named_thing).
range(predisposes, named_thing).
has_uri(predisposes, 'http://w3id.org/biolink/vocab/predisposes').
multivalued(predisposes).
slot(prevents).
domain(prevents, named_thing).
range(prevents, named_thing).
has_uri(prevents, 'http://w3id.org/biolink/vocab/prevents').
multivalued(prevents).
slot(produces).
domain(produces, named_thing).
range(produces, named_thing).
has_uri(produces, 'http://w3id.org/biolink/vocab/produces').
multivalued(produces).
slot(provided_by).
domain(provided_by, association).
range(provided_by, provider).
has_uri(provided_by, 'http://w3id.org/biolink/vocab/provided_by').
slot(publications).
domain(publications, association).
range(publications, publication).
has_uri(publications, 'http://w3id.org/biolink/vocab/publications').
multivalued(publications).
slot(qualifiers).
domain(qualifiers, association).
range(qualifiers, ontology_class).
has_uri(qualifiers, 'http://w3id.org/biolink/vocab/qualifiers').
multivalued(qualifiers).
slot(quantifier_qualifier).
domain(quantifier_qualifier, gene_to_expression_site_association).
range(quantifier_qualifier, ontology_class).
has_uri(quantifier_qualifier, 'http://w3id.org/biolink/vocab/quantifier_qualifier').
slot(regulates).
domain(regulates, named_thing).
range(regulates, named_thing).
has_uri(regulates, 'http://w3id.org/biolink/vocab/regulates').
multivalued(regulates).
slot(regulates_entity_to_entity).
domain(regulates_entity_to_entity, molecular_entity).
range(regulates_entity_to_entity, molecular_entity).
has_uri(regulates_entity_to_entity, 'http://w3id.org/biolink/vocab/regulates_entity_to_entity').
multivalued(regulates_entity_to_entity).
slot(regulates_process_to_process).
domain(regulates_process_to_process, occurrent).
range(regulates_process_to_process, occurrent).
has_uri(regulates_process_to_process, 'http://w3id.org/biolink/vocab/regulates_process_to_process').
multivalued(regulates_process_to_process).
slot(related_to).
domain(related_to, named_thing).
range(related_to, named_thing).
has_uri(related_to, 'http://w3id.org/biolink/vocab/related_to').
multivalued(related_to).
slot(relation).
domain(relation, association).
range(relation, iri_type).
has_uri(relation, 'http://w3id.org/biolink/vocab/relation').
required(relation).
slot(same_as).
domain(same_as, named_thing).
range(same_as, named_thing).
has_uri(same_as, 'http://w3id.org/biolink/vocab/same_as').
multivalued(same_as).
slot(object).
domain(object, sequence_feature_relationship).
range(object, genomic_entity).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(subject).
domain(subject, sequence_feature_relationship).
range(subject, genomic_entity).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(object).
domain(object, sequence_variant_modulates_treatment_association).
range(object, treatment).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(subject).
domain(subject, sequence_variant_modulates_treatment_association).
range(subject, sequence_variant).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(sequence_variant_qualifier).
domain(sequence_variant_qualifier, gene_has_variant_that_contributes_to_disease_association).
range(sequence_variant_qualifier, sequence_variant).
has_uri(sequence_variant_qualifier, 'http://w3id.org/biolink/vocab/sequence_variant_qualifier').
slot(has_biological_sequence).
domain(has_biological_sequence, sequence_variant).
range(has_biological_sequence, biological_sequence).
has_uri(has_biological_sequence, 'http://w3id.org/biolink/vocab/has_biological_sequence').
slot(has_gene).
domain(has_gene, sequence_variant).
range(has_gene, gene).
has_uri(has_gene, 'http://w3id.org/biolink/vocab/has_gene').
multivalued(has_gene).
slot(id).
domain(id, sequence_variant).
range(id, identifier_type).
has_uri(id, 'http://w3id.org/biolink/vocab/id').
required(id).
slot(severity_qualifier).
domain(severity_qualifier, entity_to_feature_or_disease_qualifiers).
range(severity_qualifier, severity_value).
has_uri(severity_qualifier, 'http://w3id.org/biolink/vocab/severity_qualifier').
slot(sex_qualifier).
domain(sex_qualifier, entity_to_phenotypic_feature_association).
range(sex_qualifier, biological_sex).
has_uri(sex_qualifier, 'http://w3id.org/biolink/vocab/sex_qualifier').
slot(stage_qualifier).
domain(stage_qualifier, gene_to_expression_site_association).
range(stage_qualifier, life_stage).
has_uri(stage_qualifier, 'http://w3id.org/biolink/vocab/stage_qualifier').
slot(start_interbase_coordinate).
domain(start_interbase_coordinate, genomic_sequence_localization).
range(start_interbase_coordinate, string).
has_uri(start_interbase_coordinate, 'http://w3id.org/biolink/vocab/start_interbase_coordinate').
slot(subclass_of).
domain(subclass_of, ontology_class).
range(subclass_of, ontology_class).
has_uri(subclass_of, 'http://w3id.org/biolink/vocab/subclass_of').
multivalued(subclass_of).
slot(subject).
domain(subject, association).
range(subject, iri_type).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(synonym).
domain(synonym, named_thing).
range(synonym, label_type).
has_uri(synonym, 'http://w3id.org/biolink/vocab/synonym').
multivalued(synonym).
slot(systematic_synonym).
domain(systematic_synonym, named_thing).
range(systematic_synonym, label_type).
has_uri(systematic_synonym, 'http://w3id.org/biolink/vocab/systematic_synonym').
slot(object).
domain(object, thing_to_disease_or_phenotypic_feature_association).
range(object, disease_or_phenotypic_feature).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(timepoint).
domain(timepoint, geographic_location_at_time).
range(timepoint, time_type).
has_uri(timepoint, 'http://w3id.org/biolink/vocab/timepoint').
slot(object).
domain(object, transcript_to_gene_relationship).
range(object, gene).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(subject).
domain(subject, transcript_to_gene_relationship).
range(subject, transcript).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(treated_by).
domain(treated_by, disease_or_phenotypic_feature).
range(treated_by, named_thing).
has_uri(treated_by, 'http://w3id.org/biolink/vocab/treated_by').
multivalued(treated_by).
slot(treats).
domain(treats, treatment).
range(treats, disease_or_phenotypic_feature).
has_uri(treats, 'http://w3id.org/biolink/vocab/treats').
multivalued(treats).
required(treats).
slot(update_date).
domain(update_date, named_thing).
range(update_date, date).
has_uri(update_date, 'http://w3id.org/biolink/vocab/update_date').
slot(object).
domain(object, variant_to_disease_association).
range(object, iri_type).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(relation).
domain(relation, variant_to_disease_association).
range(relation, iri_type).
has_uri(relation, 'http://w3id.org/biolink/vocab/relation').
required(relation).
slot(subject).
domain(subject, variant_to_disease_association).
range(subject, iri_type).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(subject).
domain(subject, variant_to_phenotypic_feature_association).
range(subject, sequence_variant).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(has_count).
domain(has_count, variant_to_population_association).
range(has_count, integer).
has_uri(has_count, 'http://w3id.org/biolink/vocab/has_count').
slot(has_quotient).
domain(has_quotient, variant_to_population_association).
range(has_quotient, double).
has_uri(has_quotient, 'http://w3id.org/biolink/vocab/has_quotient').
slot(has_total).
domain(has_total, variant_to_population_association).
range(has_total, integer).
has_uri(has_total, 'http://w3id.org/biolink/vocab/has_total').
slot(object).
domain(object, variant_to_population_association).
range(object, population_of_individual_organisms).
has_uri(object, 'http://w3id.org/biolink/vocab/object').
required(object).
slot(subject).
domain(subject, variant_to_population_association).
range(subject, sequence_variant).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(subject).
domain(subject, variant_to_thing_association).
range(subject, sequence_variant).
has_uri(subject, 'http://w3id.org/biolink/vocab/subject').
required(subject).
slot(xenologous_to).
domain(xenologous_to, named_thing).
range(xenologous_to, named_thing).
has_uri(xenologous_to, 'http://w3id.org/biolink/vocab/xenologous_to').
multivalued(xenologous_to).
class(activity_and_behavior).
is_a(activity_and_behavior, occurrent).
has_uri(activity_and_behavior, 'http://w3id.org/biolink/vocab/ActivityAndBehavior').
class_slot(activity_and_behavior, id).
required(id).
slotrange(identifier_type).
required_in(id, activity_and_behavior).
range_in(id, identifier_type, activity_and_behavior).
class_slot(activity_and_behavior, name).
required(name).
slotrange(label_type).
range_in(name, label_type, activity_and_behavior).
class_slot(activity_and_behavior, category).
required(category).
slotrange(iri_type).
multivalued_in(category, activity_and_behavior).
range_in(category, iri_type, activity_and_behavior).
class_slot(activity_and_behavior, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, activity_and_behavior).
range_in(related_to, named_thing, activity_and_behavior).
class_slot(activity_and_behavior, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, activity_and_behavior).
range_in(interacts_with, named_thing, activity_and_behavior).
class_slot(activity_and_behavior, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, activity_and_behavior).
class_slot(activity_and_behavior, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, activity_and_behavior).
class_slot(activity_and_behavior, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, activity_and_behavior).
range_in(synonym, label_type, activity_and_behavior).
class_slot(activity_and_behavior, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, activity_and_behavior).
class_slot(activity_and_behavior, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, activity_and_behavior).
class_slot(activity_and_behavior, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, activity_and_behavior).
class_slot(activity_and_behavior, regulates_process_to_process).
required(regulates_process_to_process).
slotrange(occurrent).
multivalued_in(regulates_process_to_process, activity_and_behavior).
range_in(regulates_process_to_process, occurrent, activity_and_behavior).
class_slot(activity_and_behavior, has_participant).
required(has_participant).
slotrange(named_thing).
multivalued_in(has_participant, activity_and_behavior).
range_in(has_participant, named_thing, activity_and_behavior).
class_slot(activity_and_behavior, has_input).
required(has_input).
slotrange(named_thing).
multivalued_in(has_input, activity_and_behavior).
range_in(has_input, named_thing, activity_and_behavior).
class_slot(activity_and_behavior, precedes).
required(precedes).
slotrange(occurrent).
multivalued_in(precedes, activity_and_behavior).
range_in(precedes, occurrent, activity_and_behavior).
class(administrative_entity).
is_a(administrative_entity, named_thing).
has_uri(administrative_entity, 'http://w3id.org/biolink/vocab/AdministrativeEntity').
class_slot(administrative_entity, id).
required(id).
slotrange(identifier_type).
required_in(id, administrative_entity).
range_in(id, identifier_type, administrative_entity).
class_slot(administrative_entity, name).
required(name).
slotrange(label_type).
range_in(name, label_type, administrative_entity).
class_slot(administrative_entity, category).
required(category).
slotrange(iri_type).
multivalued_in(category, administrative_entity).
range_in(category, iri_type, administrative_entity).
class_slot(administrative_entity, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, administrative_entity).
range_in(related_to, named_thing, administrative_entity).
class_slot(administrative_entity, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, administrative_entity).
range_in(interacts_with, named_thing, administrative_entity).
class_slot(administrative_entity, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, administrative_entity).
class_slot(administrative_entity, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, administrative_entity).
class_slot(administrative_entity, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, administrative_entity).
range_in(synonym, label_type, administrative_entity).
class_slot(administrative_entity, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, administrative_entity).
class_slot(administrative_entity, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, administrative_entity).
class_slot(administrative_entity, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, administrative_entity).
class(anatomical_entity).
mixin(anatomical_entity, thing_with_taxon).
is_a(anatomical_entity, organismal_entity).
has_uri(anatomical_entity, 'http://w3id.org/biolink/vocab/AnatomicalEntity').
class_slot(anatomical_entity, id).
required(id).
slotrange(identifier_type).
required_in(id, anatomical_entity).
range_in(id, identifier_type, anatomical_entity).
class_slot(anatomical_entity, name).
required(name).
slotrange(label_type).
range_in(name, label_type, anatomical_entity).
class_slot(anatomical_entity, category).
required(category).
slotrange(iri_type).
multivalued_in(category, anatomical_entity).
range_in(category, iri_type, anatomical_entity).
class_slot(anatomical_entity, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, anatomical_entity).
range_in(related_to, named_thing, anatomical_entity).
class_slot(anatomical_entity, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, anatomical_entity).
range_in(interacts_with, named_thing, anatomical_entity).
class_slot(anatomical_entity, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, anatomical_entity).
class_slot(anatomical_entity, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, anatomical_entity).
class_slot(anatomical_entity, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, anatomical_entity).
range_in(synonym, label_type, anatomical_entity).
class_slot(anatomical_entity, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, anatomical_entity).
class_slot(anatomical_entity, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, anatomical_entity).
class_slot(anatomical_entity, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, anatomical_entity).
class_slot(anatomical_entity, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, anatomical_entity).
range_in(has_phenotype, phenotypic_feature, anatomical_entity).
class_slot(anatomical_entity, expresses).
required(expresses).
slotrange(gene_or_gene_product).
multivalued_in(expresses, anatomical_entity).
range_in(expresses, gene_or_gene_product, anatomical_entity).
class_slot(anatomical_entity, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, anatomical_entity).
range_in(in_taxon, organism_taxon, anatomical_entity).
class(anatomical_entity_to_anatomical_entity_association).
is_a(anatomical_entity_to_anatomical_entity_association, association).
defining_slots(association, [subject, object]).
has_uri(anatomical_entity_to_anatomical_entity_association, 'http://w3id.org/biolink/vocab/AnatomicalEntityToAnatomicalEntityAssociation').
class_slot(anatomical_entity_to_anatomical_entity_association, id).
required(id).
slotrange(identifier_type).
required_in(id, anatomical_entity_to_anatomical_entity_association).
range_in(id, identifier_type, anatomical_entity_to_anatomical_entity_association).
class_slot(anatomical_entity_to_anatomical_entity_association, subject).
required(subject).
slotrange(anatomical_entity).
required_in(subject, anatomical_entity_to_anatomical_entity_association).
range_in(subject, anatomical_entity, anatomical_entity_to_anatomical_entity_association).
class_slot(anatomical_entity_to_anatomical_entity_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, anatomical_entity_to_anatomical_entity_association).
range_in(relation, iri_type, anatomical_entity_to_anatomical_entity_association).
class_slot(anatomical_entity_to_anatomical_entity_association, object).
required(object).
slotrange(anatomical_entity).
required_in(object, anatomical_entity_to_anatomical_entity_association).
range_in(object, anatomical_entity, anatomical_entity_to_anatomical_entity_association).
class_slot(anatomical_entity_to_anatomical_entity_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, anatomical_entity_to_anatomical_entity_association).
class_slot(anatomical_entity_to_anatomical_entity_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, anatomical_entity_to_anatomical_entity_association).
class_slot(anatomical_entity_to_anatomical_entity_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, anatomical_entity_to_anatomical_entity_association).
range_in(qualifiers, ontology_class, anatomical_entity_to_anatomical_entity_association).
class_slot(anatomical_entity_to_anatomical_entity_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, anatomical_entity_to_anatomical_entity_association).
range_in(publications, publication, anatomical_entity_to_anatomical_entity_association).
class_slot(anatomical_entity_to_anatomical_entity_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, anatomical_entity_to_anatomical_entity_association).
class_slot(anatomical_entity_to_anatomical_entity_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, anatomical_entity_to_anatomical_entity_association).
class(anatomical_entity_to_anatomical_entity_ontogenic_association).
is_a(anatomical_entity_to_anatomical_entity_ontogenic_association, anatomical_entity_to_anatomical_entity_association).
defining_slots(anatomical_entity_to_anatomical_entity_association, [relation]).
has_uri(anatomical_entity_to_anatomical_entity_ontogenic_association, 'http://w3id.org/biolink/vocab/AnatomicalEntityToAnatomicalEntityOntogenicAssociation').
class_slot(anatomical_entity_to_anatomical_entity_ontogenic_association, id).
required(id).
slotrange(identifier_type).
required_in(id, anatomical_entity_to_anatomical_entity_ontogenic_association).
range_in(id, identifier_type, anatomical_entity_to_anatomical_entity_ontogenic_association).
class_slot(anatomical_entity_to_anatomical_entity_ontogenic_association, subject).
required(subject).
slotrange(anatomical_entity).
required_in(subject, anatomical_entity_to_anatomical_entity_ontogenic_association).
range_in(subject, anatomical_entity, anatomical_entity_to_anatomical_entity_ontogenic_association).
class_slot(anatomical_entity_to_anatomical_entity_ontogenic_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, anatomical_entity_to_anatomical_entity_ontogenic_association).
range_in(relation, iri_type, anatomical_entity_to_anatomical_entity_ontogenic_association).
class_slot(anatomical_entity_to_anatomical_entity_ontogenic_association, object).
required(object).
slotrange(anatomical_entity).
required_in(object, anatomical_entity_to_anatomical_entity_ontogenic_association).
range_in(object, anatomical_entity, anatomical_entity_to_anatomical_entity_ontogenic_association).
class_slot(anatomical_entity_to_anatomical_entity_ontogenic_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, anatomical_entity_to_anatomical_entity_ontogenic_association).
class_slot(anatomical_entity_to_anatomical_entity_ontogenic_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, anatomical_entity_to_anatomical_entity_ontogenic_association).
class_slot(anatomical_entity_to_anatomical_entity_ontogenic_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, anatomical_entity_to_anatomical_entity_ontogenic_association).
range_in(qualifiers, ontology_class, anatomical_entity_to_anatomical_entity_ontogenic_association).
class_slot(anatomical_entity_to_anatomical_entity_ontogenic_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, anatomical_entity_to_anatomical_entity_ontogenic_association).
range_in(publications, publication, anatomical_entity_to_anatomical_entity_ontogenic_association).
class_slot(anatomical_entity_to_anatomical_entity_ontogenic_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, anatomical_entity_to_anatomical_entity_ontogenic_association).
class_slot(anatomical_entity_to_anatomical_entity_ontogenic_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, anatomical_entity_to_anatomical_entity_ontogenic_association).
class(anatomical_entity_to_anatomical_entity_part_of_association).
is_a(anatomical_entity_to_anatomical_entity_part_of_association, anatomical_entity_to_anatomical_entity_association).
defining_slots(anatomical_entity_to_anatomical_entity_association, [relation]).
has_uri(anatomical_entity_to_anatomical_entity_part_of_association, 'http://w3id.org/biolink/vocab/AnatomicalEntityToAnatomicalEntityPartOfAssociation').
class_slot(anatomical_entity_to_anatomical_entity_part_of_association, id).
required(id).
slotrange(identifier_type).
required_in(id, anatomical_entity_to_anatomical_entity_part_of_association).
range_in(id, identifier_type, anatomical_entity_to_anatomical_entity_part_of_association).
class_slot(anatomical_entity_to_anatomical_entity_part_of_association, subject).
required(subject).
slotrange(anatomical_entity).
required_in(subject, anatomical_entity_to_anatomical_entity_part_of_association).
range_in(subject, anatomical_entity, anatomical_entity_to_anatomical_entity_part_of_association).
class_slot(anatomical_entity_to_anatomical_entity_part_of_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, anatomical_entity_to_anatomical_entity_part_of_association).
range_in(relation, iri_type, anatomical_entity_to_anatomical_entity_part_of_association).
class_slot(anatomical_entity_to_anatomical_entity_part_of_association, object).
required(object).
slotrange(anatomical_entity).
required_in(object, anatomical_entity_to_anatomical_entity_part_of_association).
range_in(object, anatomical_entity, anatomical_entity_to_anatomical_entity_part_of_association).
class_slot(anatomical_entity_to_anatomical_entity_part_of_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, anatomical_entity_to_anatomical_entity_part_of_association).
class_slot(anatomical_entity_to_anatomical_entity_part_of_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, anatomical_entity_to_anatomical_entity_part_of_association).
class_slot(anatomical_entity_to_anatomical_entity_part_of_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, anatomical_entity_to_anatomical_entity_part_of_association).
range_in(qualifiers, ontology_class, anatomical_entity_to_anatomical_entity_part_of_association).
class_slot(anatomical_entity_to_anatomical_entity_part_of_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, anatomical_entity_to_anatomical_entity_part_of_association).
range_in(publications, publication, anatomical_entity_to_anatomical_entity_part_of_association).
class_slot(anatomical_entity_to_anatomical_entity_part_of_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, anatomical_entity_to_anatomical_entity_part_of_association).
class_slot(anatomical_entity_to_anatomical_entity_part_of_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, anatomical_entity_to_anatomical_entity_part_of_association).
class(association).
has_uri(association, 'http://w3id.org/biolink/vocab/Association').
class_slot(association, id).
required(id).
slotrange(identifier_type).
required_in(id, association).
range_in(id, identifier_type, association).
class_slot(association, subject).
required(subject).
slotrange(iri_type).
required_in(subject, association).
range_in(subject, iri_type, association).
class_slot(association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, association).
range_in(relation, iri_type, association).
class_slot(association, object).
required(object).
slotrange(iri_type).
required_in(object, association).
range_in(object, iri_type, association).
class_slot(association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, association).
class_slot(association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, association).
class_slot(association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, association).
range_in(qualifiers, ontology_class, association).
class_slot(association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, association).
range_in(publications, publication, association).
class_slot(association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, association).
class_slot(association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, association).
class_slot(association, edge_label).
required(edge_label).
slotrange(label_type).
range_in(edge_label, label_type, association).
class_slot(association, has_confidence_level).
required(has_confidence_level).
slotrange(confidence_level).
range_in(has_confidence_level, confidence_level, association).
class_slot(association, has_evidence).
required(has_evidence).
slotrange(evidence_type).
range_in(has_evidence, evidence_type, association).
class_slot(association, clinical_modifier_qualifier).
required(clinical_modifier_qualifier).
slotrange(clinical_modifier).
range_in(clinical_modifier_qualifier, clinical_modifier, association).
class(attribute).
mixin(attribute, ontology_class).
has_uri(attribute, 'http://w3id.org/biolink/vocab/Attribute').
class_slot(attribute, id).
required(id).
slotrange(identifier_type).
required_in(id, attribute).
range_in(id, identifier_type, attribute).
class_slot(attribute, name).
required(name).
slotrange(label_type).
range_in(name, label_type, attribute).
class_slot(attribute, category).
required(category).
slotrange(iri_type).
multivalued_in(category, attribute).
range_in(category, iri_type, attribute).
class_slot(attribute, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, attribute).
range_in(related_to, named_thing, attribute).
class_slot(attribute, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, attribute).
range_in(interacts_with, named_thing, attribute).
class_slot(attribute, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, attribute).
class_slot(attribute, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, attribute).
class_slot(attribute, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, attribute).
range_in(synonym, label_type, attribute).
class_slot(attribute, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, attribute).
class_slot(attribute, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, attribute).
class_slot(attribute, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, attribute).
class_slot(attribute, subclass_of).
required(subclass_of).
slotrange(ontology_class).
multivalued_in(subclass_of, attribute).
range_in(subclass_of, ontology_class, attribute).
class(biological_entity).
is_a(biological_entity, named_thing).
has_uri(biological_entity, 'http://w3id.org/biolink/vocab/BiologicalEntity').
class_slot(biological_entity, id).
required(id).
slotrange(identifier_type).
required_in(id, biological_entity).
range_in(id, identifier_type, biological_entity).
class_slot(biological_entity, name).
required(name).
slotrange(label_type).
range_in(name, label_type, biological_entity).
class_slot(biological_entity, category).
required(category).
slotrange(iri_type).
multivalued_in(category, biological_entity).
range_in(category, iri_type, biological_entity).
class_slot(biological_entity, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, biological_entity).
range_in(related_to, named_thing, biological_entity).
class_slot(biological_entity, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, biological_entity).
range_in(interacts_with, named_thing, biological_entity).
class_slot(biological_entity, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, biological_entity).
class_slot(biological_entity, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, biological_entity).
class_slot(biological_entity, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, biological_entity).
range_in(synonym, label_type, biological_entity).
class_slot(biological_entity, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, biological_entity).
class_slot(biological_entity, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, biological_entity).
class_slot(biological_entity, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, biological_entity).
class_slot(biological_entity, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, biological_entity).
range_in(has_phenotype, phenotypic_feature, biological_entity).
class(biological_process).
mixin(biological_process, occurrent).
is_a(biological_process, biological_process_or_activity).
has_uri(biological_process, 'http://w3id.org/biolink/vocab/BiologicalProcess').
class_slot(biological_process, id).
required(id).
slotrange(identifier_type).
required_in(id, biological_process).
range_in(id, identifier_type, biological_process).
class_slot(biological_process, name).
required(name).
slotrange(label_type).
range_in(name, label_type, biological_process).
class_slot(biological_process, category).
required(category).
slotrange(iri_type).
multivalued_in(category, biological_process).
range_in(category, iri_type, biological_process).
class_slot(biological_process, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, biological_process).
range_in(related_to, named_thing, biological_process).
class_slot(biological_process, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, biological_process).
range_in(interacts_with, named_thing, biological_process).
class_slot(biological_process, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, biological_process).
class_slot(biological_process, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, biological_process).
class_slot(biological_process, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, biological_process).
range_in(synonym, label_type, biological_process).
class_slot(biological_process, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, biological_process).
class_slot(biological_process, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, biological_process).
class_slot(biological_process, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, biological_process).
class_slot(biological_process, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, biological_process).
range_in(has_phenotype, phenotypic_feature, biological_process).
class_slot(biological_process, regulates_process_to_process).
required(regulates_process_to_process).
slotrange(occurrent).
multivalued_in(regulates_process_to_process, biological_process).
range_in(regulates_process_to_process, occurrent, biological_process).
class_slot(biological_process, has_participant).
required(has_participant).
slotrange(named_thing).
multivalued_in(has_participant, biological_process).
range_in(has_participant, named_thing, biological_process).
class_slot(biological_process, has_input).
required(has_input).
slotrange(named_thing).
multivalued_in(has_input, biological_process).
range_in(has_input, named_thing, biological_process).
class_slot(biological_process, precedes).
required(precedes).
slotrange(occurrent).
multivalued_in(precedes, biological_process).
range_in(precedes, occurrent, biological_process).
class(biological_process_or_activity).
is_a(biological_process_or_activity, biological_entity).
has_uri(biological_process_or_activity, 'http://w3id.org/biolink/vocab/BiologicalProcessOrActivity').
class_slot(biological_process_or_activity, id).
required(id).
slotrange(identifier_type).
required_in(id, biological_process_or_activity).
range_in(id, identifier_type, biological_process_or_activity).
class_slot(biological_process_or_activity, name).
required(name).
slotrange(label_type).
range_in(name, label_type, biological_process_or_activity).
class_slot(biological_process_or_activity, category).
required(category).
slotrange(iri_type).
multivalued_in(category, biological_process_or_activity).
range_in(category, iri_type, biological_process_or_activity).
class_slot(biological_process_or_activity, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, biological_process_or_activity).
range_in(related_to, named_thing, biological_process_or_activity).
class_slot(biological_process_or_activity, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, biological_process_or_activity).
range_in(interacts_with, named_thing, biological_process_or_activity).
class_slot(biological_process_or_activity, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, biological_process_or_activity).
class_slot(biological_process_or_activity, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, biological_process_or_activity).
class_slot(biological_process_or_activity, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, biological_process_or_activity).
range_in(synonym, label_type, biological_process_or_activity).
class_slot(biological_process_or_activity, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, biological_process_or_activity).
class_slot(biological_process_or_activity, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, biological_process_or_activity).
class_slot(biological_process_or_activity, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, biological_process_or_activity).
class_slot(biological_process_or_activity, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, biological_process_or_activity).
range_in(has_phenotype, phenotypic_feature, biological_process_or_activity).
class(biological_sex).
is_a(biological_sex, attribute).
has_uri(biological_sex, 'http://w3id.org/biolink/vocab/BiologicalSex').
class_slot(biological_sex, id).
required(id).
slotrange(identifier_type).
required_in(id, biological_sex).
range_in(id, identifier_type, biological_sex).
class_slot(biological_sex, name).
required(name).
slotrange(label_type).
range_in(name, label_type, biological_sex).
class_slot(biological_sex, category).
required(category).
slotrange(iri_type).
multivalued_in(category, biological_sex).
range_in(category, iri_type, biological_sex).
class_slot(biological_sex, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, biological_sex).
range_in(related_to, named_thing, biological_sex).
class_slot(biological_sex, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, biological_sex).
range_in(interacts_with, named_thing, biological_sex).
class_slot(biological_sex, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, biological_sex).
class_slot(biological_sex, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, biological_sex).
class_slot(biological_sex, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, biological_sex).
range_in(synonym, label_type, biological_sex).
class_slot(biological_sex, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, biological_sex).
class_slot(biological_sex, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, biological_sex).
class_slot(biological_sex, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, biological_sex).
class_slot(biological_sex, subclass_of).
required(subclass_of).
slotrange(ontology_class).
multivalued_in(subclass_of, biological_sex).
range_in(subclass_of, ontology_class, biological_sex).
class(biosample).
mixin(biosample, thing_with_taxon).
is_a(biosample, organismal_entity).
has_uri(biosample, 'http://w3id.org/biolink/vocab/Biosample').
class_slot(biosample, id).
required(id).
slotrange(identifier_type).
required_in(id, biosample).
range_in(id, identifier_type, biosample).
class_slot(biosample, name).
required(name).
slotrange(label_type).
range_in(name, label_type, biosample).
class_slot(biosample, category).
required(category).
slotrange(iri_type).
multivalued_in(category, biosample).
range_in(category, iri_type, biosample).
class_slot(biosample, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, biosample).
range_in(related_to, named_thing, biosample).
class_slot(biosample, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, biosample).
range_in(interacts_with, named_thing, biosample).
class_slot(biosample, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, biosample).
class_slot(biosample, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, biosample).
class_slot(biosample, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, biosample).
range_in(synonym, label_type, biosample).
class_slot(biosample, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, biosample).
class_slot(biosample, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, biosample).
class_slot(biosample, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, biosample).
class_slot(biosample, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, biosample).
range_in(has_phenotype, phenotypic_feature, biosample).
class_slot(biosample, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, biosample).
range_in(in_taxon, organism_taxon, biosample).
class(biosample_to_disease_or_phenotypic_feature_association).
mixin(biosample_to_disease_or_phenotypic_feature_association, biosample_to_thing_association).
mixin(biosample_to_disease_or_phenotypic_feature_association, thing_to_disease_or_phenotypic_feature_association).
is_a(biosample_to_disease_or_phenotypic_feature_association, association).
defining_slots(association, [subject, object]).
has_uri(biosample_to_disease_or_phenotypic_feature_association, 'http://w3id.org/biolink/vocab/BiosampleToDiseaseOrPhenotypicFeatureAssociation').
class_slot(biosample_to_disease_or_phenotypic_feature_association, id).
required(id).
slotrange(identifier_type).
required_in(id, biosample_to_disease_or_phenotypic_feature_association).
range_in(id, identifier_type, biosample_to_disease_or_phenotypic_feature_association).
class_slot(biosample_to_disease_or_phenotypic_feature_association, subject).
required(subject).
slotrange(iri_type).
required_in(subject, biosample_to_disease_or_phenotypic_feature_association).
range_in(subject, iri_type, biosample_to_disease_or_phenotypic_feature_association).
class_slot(biosample_to_disease_or_phenotypic_feature_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, biosample_to_disease_or_phenotypic_feature_association).
range_in(relation, iri_type, biosample_to_disease_or_phenotypic_feature_association).
class_slot(biosample_to_disease_or_phenotypic_feature_association, object).
required(object).
slotrange(iri_type).
required_in(object, biosample_to_disease_or_phenotypic_feature_association).
range_in(object, iri_type, biosample_to_disease_or_phenotypic_feature_association).
class_slot(biosample_to_disease_or_phenotypic_feature_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, biosample_to_disease_or_phenotypic_feature_association).
class_slot(biosample_to_disease_or_phenotypic_feature_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, biosample_to_disease_or_phenotypic_feature_association).
class_slot(biosample_to_disease_or_phenotypic_feature_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, biosample_to_disease_or_phenotypic_feature_association).
range_in(qualifiers, ontology_class, biosample_to_disease_or_phenotypic_feature_association).
class_slot(biosample_to_disease_or_phenotypic_feature_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, biosample_to_disease_or_phenotypic_feature_association).
range_in(publications, publication, biosample_to_disease_or_phenotypic_feature_association).
class_slot(biosample_to_disease_or_phenotypic_feature_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, biosample_to_disease_or_phenotypic_feature_association).
class_slot(biosample_to_disease_or_phenotypic_feature_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, biosample_to_disease_or_phenotypic_feature_association).
class(biosample_to_thing_association).
is_a(biosample_to_thing_association, association).
defining_slots(association, [subject]).
has_uri(biosample_to_thing_association, 'http://w3id.org/biolink/vocab/BiosampleToThingAssociation').
class_slot(biosample_to_thing_association, id).
required(id).
slotrange(identifier_type).
required_in(id, biosample_to_thing_association).
range_in(id, identifier_type, biosample_to_thing_association).
class_slot(biosample_to_thing_association, subject).
required(subject).
slotrange(biosample).
required_in(subject, biosample_to_thing_association).
range_in(subject, biosample, biosample_to_thing_association).
class_slot(biosample_to_thing_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, biosample_to_thing_association).
range_in(relation, iri_type, biosample_to_thing_association).
class_slot(biosample_to_thing_association, object).
required(object).
slotrange(iri_type).
required_in(object, biosample_to_thing_association).
range_in(object, iri_type, biosample_to_thing_association).
class_slot(biosample_to_thing_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, biosample_to_thing_association).
class_slot(biosample_to_thing_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, biosample_to_thing_association).
class_slot(biosample_to_thing_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, biosample_to_thing_association).
range_in(qualifiers, ontology_class, biosample_to_thing_association).
class_slot(biosample_to_thing_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, biosample_to_thing_association).
range_in(publications, publication, biosample_to_thing_association).
class_slot(biosample_to_thing_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, biosample_to_thing_association).
class_slot(biosample_to_thing_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, biosample_to_thing_association).
class(carbohydrate).
is_a(carbohydrate, chemical_substance).
has_uri(carbohydrate, 'http://w3id.org/biolink/vocab/Carbohydrate').
class_slot(carbohydrate, id).
required(id).
slotrange(identifier_type).
required_in(id, carbohydrate).
range_in(id, identifier_type, carbohydrate).
class_slot(carbohydrate, name).
required(name).
slotrange(label_type).
range_in(name, label_type, carbohydrate).
class_slot(carbohydrate, category).
required(category).
slotrange(iri_type).
multivalued_in(category, carbohydrate).
range_in(category, iri_type, carbohydrate).
class_slot(carbohydrate, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, carbohydrate).
range_in(related_to, named_thing, carbohydrate).
class_slot(carbohydrate, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, carbohydrate).
range_in(interacts_with, named_thing, carbohydrate).
class_slot(carbohydrate, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, carbohydrate).
class_slot(carbohydrate, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, carbohydrate).
class_slot(carbohydrate, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, carbohydrate).
range_in(synonym, label_type, carbohydrate).
class_slot(carbohydrate, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, carbohydrate).
class_slot(carbohydrate, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, carbohydrate).
class_slot(carbohydrate, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, carbohydrate).
class_slot(carbohydrate, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, carbohydrate).
range_in(has_phenotype, phenotypic_feature, carbohydrate).
class_slot(carbohydrate, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, carbohydrate).
range_in(molecularly_interacts_with, molecular_entity, carbohydrate).
class_slot(carbohydrate, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, carbohydrate).
range_in(affects_abundance_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, carbohydrate).
range_in(increases_abundance_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, carbohydrate).
range_in(decreases_abundance_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, carbohydrate).
range_in(affects_activity_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, carbohydrate).
range_in(increases_activity_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, carbohydrate).
range_in(decreases_activity_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, carbohydrate).
range_in(affects_expression_of, genomic_entity, carbohydrate).
class_slot(carbohydrate, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, carbohydrate).
range_in(increases_expression_of, genomic_entity, carbohydrate).
class_slot(carbohydrate, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, carbohydrate).
range_in(decreases_expression_of, genomic_entity, carbohydrate).
class_slot(carbohydrate, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, carbohydrate).
range_in(affects_folding_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, carbohydrate).
range_in(increases_folding_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, carbohydrate).
range_in(decreases_folding_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, carbohydrate).
range_in(affects_localization_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, carbohydrate).
range_in(increases_localization_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, carbohydrate).
range_in(decreases_localization_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, carbohydrate).
range_in(affects_metabolic_processing_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, carbohydrate).
range_in(increases_metabolic_processing_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, carbohydrate).
range_in(decreases_metabolic_processing_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, carbohydrate).
range_in(affects_molecular_modification_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, carbohydrate).
range_in(increases_molecular_modification_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, carbohydrate).
range_in(decreases_molecular_modification_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, carbohydrate).
range_in(affects_synthesis_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, carbohydrate).
range_in(increases_synthesis_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, carbohydrate).
range_in(decreases_synthesis_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, carbohydrate).
range_in(affects_degradation_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, carbohydrate).
range_in(increases_degradation_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, carbohydrate).
range_in(decreases_degradation_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, carbohydrate).
range_in(affects_mutation_rate_of, genomic_entity, carbohydrate).
class_slot(carbohydrate, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, carbohydrate).
range_in(increases_mutation_rate_of, genomic_entity, carbohydrate).
class_slot(carbohydrate, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, carbohydrate).
range_in(decreases_mutation_rate_of, genomic_entity, carbohydrate).
class_slot(carbohydrate, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, carbohydrate).
range_in(affects_response_to, molecular_entity, carbohydrate).
class_slot(carbohydrate, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, carbohydrate).
range_in(increases_response_to, molecular_entity, carbohydrate).
class_slot(carbohydrate, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, carbohydrate).
range_in(decreases_response_to, molecular_entity, carbohydrate).
class_slot(carbohydrate, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, carbohydrate).
range_in(affects_splicing_of, transcript, carbohydrate).
class_slot(carbohydrate, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, carbohydrate).
range_in(increases_splicing_of, transcript, carbohydrate).
class_slot(carbohydrate, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, carbohydrate).
range_in(decreases_splicing_of, transcript, carbohydrate).
class_slot(carbohydrate, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, carbohydrate).
range_in(affects_stability_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, carbohydrate).
range_in(increases_stability_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, carbohydrate).
range_in(decreases_stability_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, carbohydrate).
range_in(affects_transport_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, carbohydrate).
range_in(increases_transport_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, carbohydrate).
range_in(decreases_transport_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, carbohydrate).
range_in(affects_secretion_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, carbohydrate).
range_in(increases_secretion_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, carbohydrate).
range_in(decreases_secretion_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, carbohydrate).
range_in(affects_uptake_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, carbohydrate).
range_in(increases_uptake_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, carbohydrate).
range_in(decreases_uptake_of, molecular_entity, carbohydrate).
class_slot(carbohydrate, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, carbohydrate).
range_in(regulates_entity_to_entity, molecular_entity, carbohydrate).
class_slot(carbohydrate, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, carbohydrate).
range_in(biomarker_for, disease_or_phenotypic_feature, carbohydrate).
class_slot(carbohydrate, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, carbohydrate).
range_in(in_taxon, organism_taxon, carbohydrate).
class(case).
is_a(case, individual_organism).
has_uri(case, 'http://w3id.org/biolink/vocab/Case').
class_slot(case, id).
required(id).
slotrange(identifier_type).
required_in(id, case).
range_in(id, identifier_type, case).
class_slot(case, name).
required(name).
slotrange(label_type).
range_in(name, label_type, case).
class_slot(case, category).
required(category).
slotrange(iri_type).
multivalued_in(category, case).
range_in(category, iri_type, case).
class_slot(case, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, case).
range_in(related_to, named_thing, case).
class_slot(case, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, case).
range_in(interacts_with, named_thing, case).
class_slot(case, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, case).
class_slot(case, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, case).
class_slot(case, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, case).
range_in(synonym, label_type, case).
class_slot(case, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, case).
class_slot(case, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, case).
class_slot(case, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, case).
class_slot(case, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, case).
range_in(has_phenotype, phenotypic_feature, case).
class_slot(case, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, case).
range_in(in_taxon, organism_taxon, case).
class(case_to_phenotypic_feature_association).
mixin(case_to_phenotypic_feature_association, entity_to_phenotypic_feature_association).
mixin(case_to_phenotypic_feature_association, case_to_thing_association).
is_a(case_to_phenotypic_feature_association, association).
defining_slots(association, [subject, object]).
has_uri(case_to_phenotypic_feature_association, 'http://w3id.org/biolink/vocab/CaseToPhenotypicFeatureAssociation').
class_slot(case_to_phenotypic_feature_association, id).
required(id).
slotrange(identifier_type).
required_in(id, case_to_phenotypic_feature_association).
range_in(id, identifier_type, case_to_phenotypic_feature_association).
class_slot(case_to_phenotypic_feature_association, subject).
required(subject).
slotrange(iri_type).
required_in(subject, case_to_phenotypic_feature_association).
range_in(subject, iri_type, case_to_phenotypic_feature_association).
class_slot(case_to_phenotypic_feature_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, case_to_phenotypic_feature_association).
range_in(relation, iri_type, case_to_phenotypic_feature_association).
class_slot(case_to_phenotypic_feature_association, object).
required(object).
slotrange(iri_type).
required_in(object, case_to_phenotypic_feature_association).
range_in(object, iri_type, case_to_phenotypic_feature_association).
class_slot(case_to_phenotypic_feature_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, case_to_phenotypic_feature_association).
class_slot(case_to_phenotypic_feature_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, case_to_phenotypic_feature_association).
class_slot(case_to_phenotypic_feature_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, case_to_phenotypic_feature_association).
range_in(qualifiers, ontology_class, case_to_phenotypic_feature_association).
class_slot(case_to_phenotypic_feature_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, case_to_phenotypic_feature_association).
range_in(publications, publication, case_to_phenotypic_feature_association).
class_slot(case_to_phenotypic_feature_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, case_to_phenotypic_feature_association).
class_slot(case_to_phenotypic_feature_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, case_to_phenotypic_feature_association).
class_slot(case_to_phenotypic_feature_association, sex_qualifier).
required(sex_qualifier).
slotrange(biological_sex).
range_in(sex_qualifier, biological_sex, case_to_phenotypic_feature_association).
class_slot(case_to_phenotypic_feature_association, frequency_qualifier).
required(frequency_qualifier).
slotrange(frequency_value).
range_in(frequency_qualifier, frequency_value, case_to_phenotypic_feature_association).
class_slot(case_to_phenotypic_feature_association, severity_qualifier).
required(severity_qualifier).
slotrange(severity_value).
range_in(severity_qualifier, severity_value, case_to_phenotypic_feature_association).
class_slot(case_to_phenotypic_feature_association, onset_qualifier).
required(onset_qualifier).
slotrange(onset).
range_in(onset_qualifier, onset, case_to_phenotypic_feature_association).
class(case_to_thing_association).
is_a(case_to_thing_association, association).
defining_slots(association, [subject]).
has_uri(case_to_thing_association, 'http://w3id.org/biolink/vocab/CaseToThingAssociation').
class_slot(case_to_thing_association, id).
required(id).
slotrange(identifier_type).
required_in(id, case_to_thing_association).
range_in(id, identifier_type, case_to_thing_association).
class_slot(case_to_thing_association, subject).
required(subject).
slotrange(case).
required_in(subject, case_to_thing_association).
range_in(subject, case, case_to_thing_association).
class_slot(case_to_thing_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, case_to_thing_association).
range_in(relation, iri_type, case_to_thing_association).
class_slot(case_to_thing_association, object).
required(object).
slotrange(iri_type).
required_in(object, case_to_thing_association).
range_in(object, iri_type, case_to_thing_association).
class_slot(case_to_thing_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, case_to_thing_association).
class_slot(case_to_thing_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, case_to_thing_association).
class_slot(case_to_thing_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, case_to_thing_association).
range_in(qualifiers, ontology_class, case_to_thing_association).
class_slot(case_to_thing_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, case_to_thing_association).
range_in(publications, publication, case_to_thing_association).
class_slot(case_to_thing_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, case_to_thing_association).
class_slot(case_to_thing_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, case_to_thing_association).
class(cell).
is_a(cell, anatomical_entity).
has_uri(cell, 'http://w3id.org/biolink/vocab/Cell').
class_slot(cell, id).
required(id).
slotrange(identifier_type).
required_in(id, cell).
range_in(id, identifier_type, cell).
class_slot(cell, name).
required(name).
slotrange(label_type).
range_in(name, label_type, cell).
class_slot(cell, category).
required(category).
slotrange(iri_type).
multivalued_in(category, cell).
range_in(category, iri_type, cell).
class_slot(cell, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, cell).
range_in(related_to, named_thing, cell).
class_slot(cell, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, cell).
range_in(interacts_with, named_thing, cell).
class_slot(cell, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, cell).
class_slot(cell, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, cell).
class_slot(cell, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, cell).
range_in(synonym, label_type, cell).
class_slot(cell, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, cell).
class_slot(cell, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, cell).
class_slot(cell, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, cell).
class_slot(cell, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, cell).
range_in(has_phenotype, phenotypic_feature, cell).
class_slot(cell, expresses).
required(expresses).
slotrange(gene_or_gene_product).
multivalued_in(expresses, cell).
range_in(expresses, gene_or_gene_product, cell).
class_slot(cell, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, cell).
range_in(in_taxon, organism_taxon, cell).
class(cell_line).
is_a(cell_line, biosample).
has_uri(cell_line, 'http://w3id.org/biolink/vocab/CellLine').
class_slot(cell_line, id).
required(id).
slotrange(identifier_type).
required_in(id, cell_line).
range_in(id, identifier_type, cell_line).
class_slot(cell_line, name).
required(name).
slotrange(label_type).
range_in(name, label_type, cell_line).
class_slot(cell_line, category).
required(category).
slotrange(iri_type).
multivalued_in(category, cell_line).
range_in(category, iri_type, cell_line).
class_slot(cell_line, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, cell_line).
range_in(related_to, named_thing, cell_line).
class_slot(cell_line, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, cell_line).
range_in(interacts_with, named_thing, cell_line).
class_slot(cell_line, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, cell_line).
class_slot(cell_line, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, cell_line).
class_slot(cell_line, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, cell_line).
range_in(synonym, label_type, cell_line).
class_slot(cell_line, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, cell_line).
class_slot(cell_line, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, cell_line).
class_slot(cell_line, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, cell_line).
class_slot(cell_line, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, cell_line).
range_in(has_phenotype, phenotypic_feature, cell_line).
class_slot(cell_line, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, cell_line).
range_in(in_taxon, organism_taxon, cell_line).
class(cell_line_to_disease_or_phenotypic_feature_association).
mixin(cell_line_to_disease_or_phenotypic_feature_association, cell_line_to_thing_association).
mixin(cell_line_to_disease_or_phenotypic_feature_association, thing_to_disease_or_phenotypic_feature_association).
is_a(cell_line_to_disease_or_phenotypic_feature_association, association).
has_uri(cell_line_to_disease_or_phenotypic_feature_association, 'http://w3id.org/biolink/vocab/CellLineToDiseaseOrPhenotypicFeatureAssociation').
class_slot(cell_line_to_disease_or_phenotypic_feature_association, id).
required(id).
slotrange(identifier_type).
required_in(id, cell_line_to_disease_or_phenotypic_feature_association).
range_in(id, identifier_type, cell_line_to_disease_or_phenotypic_feature_association).
class_slot(cell_line_to_disease_or_phenotypic_feature_association, subject).
required(subject).
slotrange(disease_or_phenotypic_feature).
required_in(subject, cell_line_to_disease_or_phenotypic_feature_association).
range_in(subject, disease_or_phenotypic_feature, cell_line_to_disease_or_phenotypic_feature_association).
class_slot(cell_line_to_disease_or_phenotypic_feature_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, cell_line_to_disease_or_phenotypic_feature_association).
range_in(relation, iri_type, cell_line_to_disease_or_phenotypic_feature_association).
class_slot(cell_line_to_disease_or_phenotypic_feature_association, object).
required(object).
slotrange(iri_type).
required_in(object, cell_line_to_disease_or_phenotypic_feature_association).
range_in(object, iri_type, cell_line_to_disease_or_phenotypic_feature_association).
class_slot(cell_line_to_disease_or_phenotypic_feature_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, cell_line_to_disease_or_phenotypic_feature_association).
class_slot(cell_line_to_disease_or_phenotypic_feature_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, cell_line_to_disease_or_phenotypic_feature_association).
class_slot(cell_line_to_disease_or_phenotypic_feature_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, cell_line_to_disease_or_phenotypic_feature_association).
range_in(qualifiers, ontology_class, cell_line_to_disease_or_phenotypic_feature_association).
class_slot(cell_line_to_disease_or_phenotypic_feature_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, cell_line_to_disease_or_phenotypic_feature_association).
range_in(publications, publication, cell_line_to_disease_or_phenotypic_feature_association).
class_slot(cell_line_to_disease_or_phenotypic_feature_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, cell_line_to_disease_or_phenotypic_feature_association).
class_slot(cell_line_to_disease_or_phenotypic_feature_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, cell_line_to_disease_or_phenotypic_feature_association).
class(cell_line_to_thing_association).
is_a(cell_line_to_thing_association, association).
defining_slots(association, [subject]).
has_uri(cell_line_to_thing_association, 'http://w3id.org/biolink/vocab/CellLineToThingAssociation').
class_slot(cell_line_to_thing_association, id).
required(id).
slotrange(identifier_type).
required_in(id, cell_line_to_thing_association).
range_in(id, identifier_type, cell_line_to_thing_association).
class_slot(cell_line_to_thing_association, subject).
required(subject).
slotrange(cell_line).
required_in(subject, cell_line_to_thing_association).
range_in(subject, cell_line, cell_line_to_thing_association).
class_slot(cell_line_to_thing_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, cell_line_to_thing_association).
range_in(relation, iri_type, cell_line_to_thing_association).
class_slot(cell_line_to_thing_association, object).
required(object).
slotrange(iri_type).
required_in(object, cell_line_to_thing_association).
range_in(object, iri_type, cell_line_to_thing_association).
class_slot(cell_line_to_thing_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, cell_line_to_thing_association).
class_slot(cell_line_to_thing_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, cell_line_to_thing_association).
class_slot(cell_line_to_thing_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, cell_line_to_thing_association).
range_in(qualifiers, ontology_class, cell_line_to_thing_association).
class_slot(cell_line_to_thing_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, cell_line_to_thing_association).
range_in(publications, publication, cell_line_to_thing_association).
class_slot(cell_line_to_thing_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, cell_line_to_thing_association).
class_slot(cell_line_to_thing_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, cell_line_to_thing_association).
class(cellular_component).
is_a(cellular_component, anatomical_entity).
has_uri(cellular_component, 'http://w3id.org/biolink/vocab/CellularComponent').
class_slot(cellular_component, id).
required(id).
slotrange(identifier_type).
required_in(id, cellular_component).
range_in(id, identifier_type, cellular_component).
class_slot(cellular_component, name).
required(name).
slotrange(label_type).
range_in(name, label_type, cellular_component).
class_slot(cellular_component, category).
required(category).
slotrange(iri_type).
multivalued_in(category, cellular_component).
range_in(category, iri_type, cellular_component).
class_slot(cellular_component, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, cellular_component).
range_in(related_to, named_thing, cellular_component).
class_slot(cellular_component, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, cellular_component).
range_in(interacts_with, named_thing, cellular_component).
class_slot(cellular_component, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, cellular_component).
class_slot(cellular_component, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, cellular_component).
class_slot(cellular_component, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, cellular_component).
range_in(synonym, label_type, cellular_component).
class_slot(cellular_component, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, cellular_component).
class_slot(cellular_component, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, cellular_component).
class_slot(cellular_component, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, cellular_component).
class_slot(cellular_component, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, cellular_component).
range_in(has_phenotype, phenotypic_feature, cellular_component).
class_slot(cellular_component, expresses).
required(expresses).
slotrange(gene_or_gene_product).
multivalued_in(expresses, cellular_component).
range_in(expresses, gene_or_gene_product, cellular_component).
class_slot(cellular_component, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, cellular_component).
range_in(in_taxon, organism_taxon, cellular_component).
class(chemical_substance).
is_a(chemical_substance, molecular_entity).
has_uri(chemical_substance, 'http://w3id.org/biolink/vocab/ChemicalSubstance').
class_slot(chemical_substance, id).
required(id).
slotrange(identifier_type).
required_in(id, chemical_substance).
range_in(id, identifier_type, chemical_substance).
class_slot(chemical_substance, name).
required(name).
slotrange(label_type).
range_in(name, label_type, chemical_substance).
class_slot(chemical_substance, category).
required(category).
slotrange(iri_type).
multivalued_in(category, chemical_substance).
range_in(category, iri_type, chemical_substance).
class_slot(chemical_substance, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, chemical_substance).
range_in(related_to, named_thing, chemical_substance).
class_slot(chemical_substance, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, chemical_substance).
range_in(interacts_with, named_thing, chemical_substance).
class_slot(chemical_substance, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, chemical_substance).
class_slot(chemical_substance, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, chemical_substance).
class_slot(chemical_substance, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, chemical_substance).
range_in(synonym, label_type, chemical_substance).
class_slot(chemical_substance, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, chemical_substance).
class_slot(chemical_substance, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, chemical_substance).
class_slot(chemical_substance, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, chemical_substance).
class_slot(chemical_substance, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, chemical_substance).
range_in(has_phenotype, phenotypic_feature, chemical_substance).
class_slot(chemical_substance, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, chemical_substance).
range_in(molecularly_interacts_with, molecular_entity, chemical_substance).
class_slot(chemical_substance, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, chemical_substance).
range_in(affects_abundance_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, chemical_substance).
range_in(increases_abundance_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, chemical_substance).
range_in(decreases_abundance_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, chemical_substance).
range_in(affects_activity_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, chemical_substance).
range_in(increases_activity_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, chemical_substance).
range_in(decreases_activity_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, chemical_substance).
range_in(affects_expression_of, genomic_entity, chemical_substance).
class_slot(chemical_substance, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, chemical_substance).
range_in(increases_expression_of, genomic_entity, chemical_substance).
class_slot(chemical_substance, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, chemical_substance).
range_in(decreases_expression_of, genomic_entity, chemical_substance).
class_slot(chemical_substance, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, chemical_substance).
range_in(affects_folding_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, chemical_substance).
range_in(increases_folding_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, chemical_substance).
range_in(decreases_folding_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, chemical_substance).
range_in(affects_localization_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, chemical_substance).
range_in(increases_localization_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, chemical_substance).
range_in(decreases_localization_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, chemical_substance).
range_in(affects_metabolic_processing_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, chemical_substance).
range_in(increases_metabolic_processing_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, chemical_substance).
range_in(decreases_metabolic_processing_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, chemical_substance).
range_in(affects_molecular_modification_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, chemical_substance).
range_in(increases_molecular_modification_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, chemical_substance).
range_in(decreases_molecular_modification_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, chemical_substance).
range_in(affects_synthesis_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, chemical_substance).
range_in(increases_synthesis_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, chemical_substance).
range_in(decreases_synthesis_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, chemical_substance).
range_in(affects_degradation_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, chemical_substance).
range_in(increases_degradation_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, chemical_substance).
range_in(decreases_degradation_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, chemical_substance).
range_in(affects_mutation_rate_of, genomic_entity, chemical_substance).
class_slot(chemical_substance, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, chemical_substance).
range_in(increases_mutation_rate_of, genomic_entity, chemical_substance).
class_slot(chemical_substance, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, chemical_substance).
range_in(decreases_mutation_rate_of, genomic_entity, chemical_substance).
class_slot(chemical_substance, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, chemical_substance).
range_in(affects_response_to, molecular_entity, chemical_substance).
class_slot(chemical_substance, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, chemical_substance).
range_in(increases_response_to, molecular_entity, chemical_substance).
class_slot(chemical_substance, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, chemical_substance).
range_in(decreases_response_to, molecular_entity, chemical_substance).
class_slot(chemical_substance, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, chemical_substance).
range_in(affects_splicing_of, transcript, chemical_substance).
class_slot(chemical_substance, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, chemical_substance).
range_in(increases_splicing_of, transcript, chemical_substance).
class_slot(chemical_substance, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, chemical_substance).
range_in(decreases_splicing_of, transcript, chemical_substance).
class_slot(chemical_substance, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, chemical_substance).
range_in(affects_stability_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, chemical_substance).
range_in(increases_stability_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, chemical_substance).
range_in(decreases_stability_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, chemical_substance).
range_in(affects_transport_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, chemical_substance).
range_in(increases_transport_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, chemical_substance).
range_in(decreases_transport_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, chemical_substance).
range_in(affects_secretion_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, chemical_substance).
range_in(increases_secretion_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, chemical_substance).
range_in(decreases_secretion_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, chemical_substance).
range_in(affects_uptake_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, chemical_substance).
range_in(increases_uptake_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, chemical_substance).
range_in(decreases_uptake_of, molecular_entity, chemical_substance).
class_slot(chemical_substance, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, chemical_substance).
range_in(regulates_entity_to_entity, molecular_entity, chemical_substance).
class_slot(chemical_substance, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, chemical_substance).
range_in(biomarker_for, disease_or_phenotypic_feature, chemical_substance).
class_slot(chemical_substance, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, chemical_substance).
range_in(in_taxon, organism_taxon, chemical_substance).
class(chemical_to_disease_or_phenotypic_feature_association).
mixin(chemical_to_disease_or_phenotypic_feature_association, chemical_to_thing_association).
mixin(chemical_to_disease_or_phenotypic_feature_association, thing_to_disease_or_phenotypic_feature_association).
is_a(chemical_to_disease_or_phenotypic_feature_association, association).
defining_slots(association, [subject, object]).
has_uri(chemical_to_disease_or_phenotypic_feature_association, 'http://w3id.org/biolink/vocab/ChemicalToDiseaseOrPhenotypicFeatureAssociation').
class_slot(chemical_to_disease_or_phenotypic_feature_association, id).
required(id).
slotrange(identifier_type).
required_in(id, chemical_to_disease_or_phenotypic_feature_association).
range_in(id, identifier_type, chemical_to_disease_or_phenotypic_feature_association).
class_slot(chemical_to_disease_or_phenotypic_feature_association, subject).
required(subject).
slotrange(iri_type).
required_in(subject, chemical_to_disease_or_phenotypic_feature_association).
range_in(subject, iri_type, chemical_to_disease_or_phenotypic_feature_association).
class_slot(chemical_to_disease_or_phenotypic_feature_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, chemical_to_disease_or_phenotypic_feature_association).
range_in(relation, iri_type, chemical_to_disease_or_phenotypic_feature_association).
class_slot(chemical_to_disease_or_phenotypic_feature_association, object).
required(object).
slotrange(disease_or_phenotypic_feature).
required_in(object, chemical_to_disease_or_phenotypic_feature_association).
range_in(object, disease_or_phenotypic_feature, chemical_to_disease_or_phenotypic_feature_association).
class_slot(chemical_to_disease_or_phenotypic_feature_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, chemical_to_disease_or_phenotypic_feature_association).
class_slot(chemical_to_disease_or_phenotypic_feature_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, chemical_to_disease_or_phenotypic_feature_association).
class_slot(chemical_to_disease_or_phenotypic_feature_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, chemical_to_disease_or_phenotypic_feature_association).
range_in(qualifiers, ontology_class, chemical_to_disease_or_phenotypic_feature_association).
class_slot(chemical_to_disease_or_phenotypic_feature_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, chemical_to_disease_or_phenotypic_feature_association).
range_in(publications, publication, chemical_to_disease_or_phenotypic_feature_association).
class_slot(chemical_to_disease_or_phenotypic_feature_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, chemical_to_disease_or_phenotypic_feature_association).
class_slot(chemical_to_disease_or_phenotypic_feature_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, chemical_to_disease_or_phenotypic_feature_association).
class(chemical_to_gene_association).
mixin(chemical_to_gene_association, chemical_to_thing_association).
is_a(chemical_to_gene_association, association).
defining_slots(association, [subject, object]).
has_uri(chemical_to_gene_association, 'http://w3id.org/biolink/vocab/ChemicalToGeneAssociation').
class_slot(chemical_to_gene_association, id).
required(id).
slotrange(identifier_type).
required_in(id, chemical_to_gene_association).
range_in(id, identifier_type, chemical_to_gene_association).
class_slot(chemical_to_gene_association, subject).
required(subject).
slotrange(iri_type).
required_in(subject, chemical_to_gene_association).
range_in(subject, iri_type, chemical_to_gene_association).
class_slot(chemical_to_gene_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, chemical_to_gene_association).
range_in(relation, iri_type, chemical_to_gene_association).
class_slot(chemical_to_gene_association, object).
required(object).
slotrange(gene_or_gene_product).
required_in(object, chemical_to_gene_association).
range_in(object, gene_or_gene_product, chemical_to_gene_association).
class_slot(chemical_to_gene_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, chemical_to_gene_association).
class_slot(chemical_to_gene_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, chemical_to_gene_association).
class_slot(chemical_to_gene_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, chemical_to_gene_association).
range_in(qualifiers, ontology_class, chemical_to_gene_association).
class_slot(chemical_to_gene_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, chemical_to_gene_association).
range_in(publications, publication, chemical_to_gene_association).
class_slot(chemical_to_gene_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, chemical_to_gene_association).
class_slot(chemical_to_gene_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, chemical_to_gene_association).
class(chemical_to_pathway_association).
mixin(chemical_to_pathway_association, chemical_to_thing_association).
is_a(chemical_to_pathway_association, association).
defining_slots(association, [subject, object]).
has_uri(chemical_to_pathway_association, 'http://w3id.org/biolink/vocab/ChemicalToPathwayAssociation').
class_slot(chemical_to_pathway_association, id).
required(id).
slotrange(identifier_type).
required_in(id, chemical_to_pathway_association).
range_in(id, identifier_type, chemical_to_pathway_association).
class_slot(chemical_to_pathway_association, subject).
required(subject).
slotrange(iri_type).
required_in(subject, chemical_to_pathway_association).
range_in(subject, iri_type, chemical_to_pathway_association).
class_slot(chemical_to_pathway_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, chemical_to_pathway_association).
range_in(relation, iri_type, chemical_to_pathway_association).
class_slot(chemical_to_pathway_association, object).
required(object).
slotrange(pathway).
required_in(object, chemical_to_pathway_association).
range_in(object, pathway, chemical_to_pathway_association).
class_slot(chemical_to_pathway_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, chemical_to_pathway_association).
class_slot(chemical_to_pathway_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, chemical_to_pathway_association).
class_slot(chemical_to_pathway_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, chemical_to_pathway_association).
range_in(qualifiers, ontology_class, chemical_to_pathway_association).
class_slot(chemical_to_pathway_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, chemical_to_pathway_association).
range_in(publications, publication, chemical_to_pathway_association).
class_slot(chemical_to_pathway_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, chemical_to_pathway_association).
class_slot(chemical_to_pathway_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, chemical_to_pathway_association).
class(chemical_to_thing_association).
is_a(chemical_to_thing_association, association).
defining_slots(association, [subject]).
has_uri(chemical_to_thing_association, 'http://w3id.org/biolink/vocab/ChemicalToThingAssociation').
class_slot(chemical_to_thing_association, id).
required(id).
slotrange(identifier_type).
required_in(id, chemical_to_thing_association).
range_in(id, identifier_type, chemical_to_thing_association).
class_slot(chemical_to_thing_association, subject).
required(subject).
slotrange(chemical_substance).
required_in(subject, chemical_to_thing_association).
range_in(subject, chemical_substance, chemical_to_thing_association).
class_slot(chemical_to_thing_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, chemical_to_thing_association).
range_in(relation, iri_type, chemical_to_thing_association).
class_slot(chemical_to_thing_association, object).
required(object).
slotrange(iri_type).
required_in(object, chemical_to_thing_association).
range_in(object, iri_type, chemical_to_thing_association).
class_slot(chemical_to_thing_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, chemical_to_thing_association).
class_slot(chemical_to_thing_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, chemical_to_thing_association).
class_slot(chemical_to_thing_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, chemical_to_thing_association).
range_in(qualifiers, ontology_class, chemical_to_thing_association).
class_slot(chemical_to_thing_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, chemical_to_thing_association).
range_in(publications, publication, chemical_to_thing_association).
class_slot(chemical_to_thing_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, chemical_to_thing_association).
class_slot(chemical_to_thing_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, chemical_to_thing_association).
class(clinical_entity).
is_a(clinical_entity, named_thing).
has_uri(clinical_entity, 'http://w3id.org/biolink/vocab/ClinicalEntity').
class_slot(clinical_entity, id).
required(id).
slotrange(identifier_type).
required_in(id, clinical_entity).
range_in(id, identifier_type, clinical_entity).
class_slot(clinical_entity, name).
required(name).
slotrange(label_type).
range_in(name, label_type, clinical_entity).
class_slot(clinical_entity, category).
required(category).
slotrange(iri_type).
multivalued_in(category, clinical_entity).
range_in(category, iri_type, clinical_entity).
class_slot(clinical_entity, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, clinical_entity).
range_in(related_to, named_thing, clinical_entity).
class_slot(clinical_entity, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, clinical_entity).
range_in(interacts_with, named_thing, clinical_entity).
class_slot(clinical_entity, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, clinical_entity).
class_slot(clinical_entity, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, clinical_entity).
class_slot(clinical_entity, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, clinical_entity).
range_in(synonym, label_type, clinical_entity).
class_slot(clinical_entity, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, clinical_entity).
class_slot(clinical_entity, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, clinical_entity).
class_slot(clinical_entity, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, clinical_entity).
class(clinical_intervention).
is_a(clinical_intervention, clinical_entity).
has_uri(clinical_intervention, 'http://w3id.org/biolink/vocab/ClinicalIntervention').
class_slot(clinical_intervention, id).
required(id).
slotrange(identifier_type).
required_in(id, clinical_intervention).
range_in(id, identifier_type, clinical_intervention).
class_slot(clinical_intervention, name).
required(name).
slotrange(label_type).
range_in(name, label_type, clinical_intervention).
class_slot(clinical_intervention, category).
required(category).
slotrange(iri_type).
multivalued_in(category, clinical_intervention).
range_in(category, iri_type, clinical_intervention).
class_slot(clinical_intervention, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, clinical_intervention).
range_in(related_to, named_thing, clinical_intervention).
class_slot(clinical_intervention, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, clinical_intervention).
range_in(interacts_with, named_thing, clinical_intervention).
class_slot(clinical_intervention, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, clinical_intervention).
class_slot(clinical_intervention, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, clinical_intervention).
class_slot(clinical_intervention, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, clinical_intervention).
range_in(synonym, label_type, clinical_intervention).
class_slot(clinical_intervention, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, clinical_intervention).
class_slot(clinical_intervention, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, clinical_intervention).
class_slot(clinical_intervention, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, clinical_intervention).
class(clinical_modifier).
is_a(clinical_modifier, attribute).
has_uri(clinical_modifier, 'http://w3id.org/biolink/vocab/ClinicalModifier').
class_slot(clinical_modifier, id).
required(id).
slotrange(identifier_type).
required_in(id, clinical_modifier).
range_in(id, identifier_type, clinical_modifier).
class_slot(clinical_modifier, name).
required(name).
slotrange(label_type).
range_in(name, label_type, clinical_modifier).
class_slot(clinical_modifier, category).
required(category).
slotrange(iri_type).
multivalued_in(category, clinical_modifier).
range_in(category, iri_type, clinical_modifier).
class_slot(clinical_modifier, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, clinical_modifier).
range_in(related_to, named_thing, clinical_modifier).
class_slot(clinical_modifier, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, clinical_modifier).
range_in(interacts_with, named_thing, clinical_modifier).
class_slot(clinical_modifier, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, clinical_modifier).
class_slot(clinical_modifier, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, clinical_modifier).
class_slot(clinical_modifier, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, clinical_modifier).
range_in(synonym, label_type, clinical_modifier).
class_slot(clinical_modifier, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, clinical_modifier).
class_slot(clinical_modifier, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, clinical_modifier).
class_slot(clinical_modifier, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, clinical_modifier).
class_slot(clinical_modifier, subclass_of).
required(subclass_of).
slotrange(ontology_class).
multivalued_in(subclass_of, clinical_modifier).
range_in(subclass_of, ontology_class, clinical_modifier).
class(clinical_trial).
is_a(clinical_trial, clinical_entity).
has_uri(clinical_trial, 'http://w3id.org/biolink/vocab/ClinicalTrial').
class_slot(clinical_trial, id).
required(id).
slotrange(identifier_type).
required_in(id, clinical_trial).
range_in(id, identifier_type, clinical_trial).
class_slot(clinical_trial, name).
required(name).
slotrange(label_type).
range_in(name, label_type, clinical_trial).
class_slot(clinical_trial, category).
required(category).
slotrange(iri_type).
multivalued_in(category, clinical_trial).
range_in(category, iri_type, clinical_trial).
class_slot(clinical_trial, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, clinical_trial).
range_in(related_to, named_thing, clinical_trial).
class_slot(clinical_trial, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, clinical_trial).
range_in(interacts_with, named_thing, clinical_trial).
class_slot(clinical_trial, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, clinical_trial).
class_slot(clinical_trial, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, clinical_trial).
class_slot(clinical_trial, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, clinical_trial).
range_in(synonym, label_type, clinical_trial).
class_slot(clinical_trial, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, clinical_trial).
class_slot(clinical_trial, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, clinical_trial).
class_slot(clinical_trial, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, clinical_trial).
class(coding_sequence).
is_a(coding_sequence, genomic_entity).
has_uri(coding_sequence, 'http://w3id.org/biolink/vocab/CodingSequence').
class_slot(coding_sequence, id).
required(id).
slotrange(identifier_type).
required_in(id, coding_sequence).
range_in(id, identifier_type, coding_sequence).
class_slot(coding_sequence, name).
required(name).
slotrange(label_type).
range_in(name, label_type, coding_sequence).
class_slot(coding_sequence, category).
required(category).
slotrange(iri_type).
multivalued_in(category, coding_sequence).
range_in(category, iri_type, coding_sequence).
class_slot(coding_sequence, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, coding_sequence).
range_in(related_to, named_thing, coding_sequence).
class_slot(coding_sequence, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, coding_sequence).
range_in(interacts_with, named_thing, coding_sequence).
class_slot(coding_sequence, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, coding_sequence).
class_slot(coding_sequence, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, coding_sequence).
class_slot(coding_sequence, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, coding_sequence).
range_in(synonym, label_type, coding_sequence).
class_slot(coding_sequence, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, coding_sequence).
class_slot(coding_sequence, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, coding_sequence).
class_slot(coding_sequence, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, coding_sequence).
class_slot(coding_sequence, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, coding_sequence).
range_in(has_phenotype, phenotypic_feature, coding_sequence).
class_slot(coding_sequence, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, coding_sequence).
range_in(molecularly_interacts_with, molecular_entity, coding_sequence).
class_slot(coding_sequence, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, coding_sequence).
range_in(affects_abundance_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, coding_sequence).
range_in(increases_abundance_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, coding_sequence).
range_in(decreases_abundance_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, coding_sequence).
range_in(affects_activity_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, coding_sequence).
range_in(increases_activity_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, coding_sequence).
range_in(decreases_activity_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, coding_sequence).
range_in(affects_expression_of, genomic_entity, coding_sequence).
class_slot(coding_sequence, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, coding_sequence).
range_in(increases_expression_of, genomic_entity, coding_sequence).
class_slot(coding_sequence, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, coding_sequence).
range_in(decreases_expression_of, genomic_entity, coding_sequence).
class_slot(coding_sequence, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, coding_sequence).
range_in(affects_folding_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, coding_sequence).
range_in(increases_folding_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, coding_sequence).
range_in(decreases_folding_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, coding_sequence).
range_in(affects_localization_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, coding_sequence).
range_in(increases_localization_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, coding_sequence).
range_in(decreases_localization_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, coding_sequence).
range_in(affects_metabolic_processing_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, coding_sequence).
range_in(increases_metabolic_processing_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, coding_sequence).
range_in(decreases_metabolic_processing_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, coding_sequence).
range_in(affects_molecular_modification_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, coding_sequence).
range_in(increases_molecular_modification_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, coding_sequence).
range_in(decreases_molecular_modification_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, coding_sequence).
range_in(affects_synthesis_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, coding_sequence).
range_in(increases_synthesis_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, coding_sequence).
range_in(decreases_synthesis_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, coding_sequence).
range_in(affects_degradation_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, coding_sequence).
range_in(increases_degradation_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, coding_sequence).
range_in(decreases_degradation_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, coding_sequence).
range_in(affects_mutation_rate_of, genomic_entity, coding_sequence).
class_slot(coding_sequence, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, coding_sequence).
range_in(increases_mutation_rate_of, genomic_entity, coding_sequence).
class_slot(coding_sequence, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, coding_sequence).
range_in(decreases_mutation_rate_of, genomic_entity, coding_sequence).
class_slot(coding_sequence, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, coding_sequence).
range_in(affects_response_to, molecular_entity, coding_sequence).
class_slot(coding_sequence, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, coding_sequence).
range_in(increases_response_to, molecular_entity, coding_sequence).
class_slot(coding_sequence, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, coding_sequence).
range_in(decreases_response_to, molecular_entity, coding_sequence).
class_slot(coding_sequence, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, coding_sequence).
range_in(affects_splicing_of, transcript, coding_sequence).
class_slot(coding_sequence, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, coding_sequence).
range_in(increases_splicing_of, transcript, coding_sequence).
class_slot(coding_sequence, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, coding_sequence).
range_in(decreases_splicing_of, transcript, coding_sequence).
class_slot(coding_sequence, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, coding_sequence).
range_in(affects_stability_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, coding_sequence).
range_in(increases_stability_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, coding_sequence).
range_in(decreases_stability_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, coding_sequence).
range_in(affects_transport_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, coding_sequence).
range_in(increases_transport_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, coding_sequence).
range_in(decreases_transport_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, coding_sequence).
range_in(affects_secretion_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, coding_sequence).
range_in(increases_secretion_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, coding_sequence).
range_in(decreases_secretion_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, coding_sequence).
range_in(affects_uptake_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, coding_sequence).
range_in(increases_uptake_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, coding_sequence).
range_in(decreases_uptake_of, molecular_entity, coding_sequence).
class_slot(coding_sequence, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, coding_sequence).
range_in(regulates_entity_to_entity, molecular_entity, coding_sequence).
class_slot(coding_sequence, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, coding_sequence).
range_in(biomarker_for, disease_or_phenotypic_feature, coding_sequence).
class_slot(coding_sequence, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, coding_sequence).
range_in(in_taxon, organism_taxon, coding_sequence).
class_slot(coding_sequence, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, coding_sequence).
class(confidence_level).
is_a(confidence_level, information_content_entity).
has_uri(confidence_level, 'http://w3id.org/biolink/vocab/ConfidenceLevel').
class_slot(confidence_level, id).
required(id).
slotrange(identifier_type).
required_in(id, confidence_level).
range_in(id, identifier_type, confidence_level).
class_slot(confidence_level, name).
required(name).
slotrange(label_type).
range_in(name, label_type, confidence_level).
class_slot(confidence_level, category).
required(category).
slotrange(iri_type).
multivalued_in(category, confidence_level).
range_in(category, iri_type, confidence_level).
class_slot(confidence_level, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, confidence_level).
range_in(related_to, named_thing, confidence_level).
class_slot(confidence_level, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, confidence_level).
range_in(interacts_with, named_thing, confidence_level).
class_slot(confidence_level, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, confidence_level).
class_slot(confidence_level, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, confidence_level).
class_slot(confidence_level, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, confidence_level).
range_in(synonym, label_type, confidence_level).
class_slot(confidence_level, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, confidence_level).
class_slot(confidence_level, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, confidence_level).
class_slot(confidence_level, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, confidence_level).
class(device).
is_a(device, named_thing).
has_uri(device, 'http://w3id.org/biolink/vocab/Device').
class_slot(device, id).
required(id).
slotrange(identifier_type).
required_in(id, device).
range_in(id, identifier_type, device).
class_slot(device, name).
required(name).
slotrange(label_type).
range_in(name, label_type, device).
class_slot(device, category).
required(category).
slotrange(iri_type).
multivalued_in(category, device).
range_in(category, iri_type, device).
class_slot(device, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, device).
range_in(related_to, named_thing, device).
class_slot(device, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, device).
range_in(interacts_with, named_thing, device).
class_slot(device, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, device).
class_slot(device, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, device).
class_slot(device, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, device).
range_in(synonym, label_type, device).
class_slot(device, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, device).
class_slot(device, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, device).
class_slot(device, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, device).
class(disease).
is_a(disease, disease_or_phenotypic_feature).
has_uri(disease, 'http://w3id.org/biolink/vocab/Disease').
class_slot(disease, id).
required(id).
slotrange(identifier_type).
required_in(id, disease).
range_in(id, identifier_type, disease).
class_slot(disease, name).
required(name).
slotrange(label_type).
range_in(name, label_type, disease).
class_slot(disease, category).
required(category).
slotrange(iri_type).
multivalued_in(category, disease).
range_in(category, iri_type, disease).
class_slot(disease, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, disease).
range_in(related_to, named_thing, disease).
class_slot(disease, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, disease).
range_in(interacts_with, named_thing, disease).
class_slot(disease, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, disease).
class_slot(disease, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, disease).
class_slot(disease, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, disease).
range_in(synonym, label_type, disease).
class_slot(disease, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, disease).
class_slot(disease, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, disease).
class_slot(disease, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, disease).
class_slot(disease, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, disease).
range_in(has_phenotype, phenotypic_feature, disease).
class_slot(disease, correlated_with).
required(correlated_with).
slotrange(molecular_entity).
multivalued_in(correlated_with, disease).
range_in(correlated_with, molecular_entity, disease).
class_slot(disease, has_biomarker).
required(has_biomarker).
slotrange(molecular_entity).
multivalued_in(has_biomarker, disease).
range_in(has_biomarker, molecular_entity, disease).
class_slot(disease, treated_by).
required(treated_by).
slotrange(named_thing).
multivalued_in(treated_by, disease).
range_in(treated_by, named_thing, disease).
class_slot(disease, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, disease).
range_in(in_taxon, organism_taxon, disease).
class(disease_or_phenotypic_feature).
mixin(disease_or_phenotypic_feature, thing_with_taxon).
is_a(disease_or_phenotypic_feature, biological_entity).
has_uri(disease_or_phenotypic_feature, 'http://w3id.org/biolink/vocab/DiseaseOrPhenotypicFeature').
class_slot(disease_or_phenotypic_feature, id).
required(id).
slotrange(identifier_type).
required_in(id, disease_or_phenotypic_feature).
range_in(id, identifier_type, disease_or_phenotypic_feature).
class_slot(disease_or_phenotypic_feature, name).
required(name).
slotrange(label_type).
range_in(name, label_type, disease_or_phenotypic_feature).
class_slot(disease_or_phenotypic_feature, category).
required(category).
slotrange(iri_type).
multivalued_in(category, disease_or_phenotypic_feature).
range_in(category, iri_type, disease_or_phenotypic_feature).
class_slot(disease_or_phenotypic_feature, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, disease_or_phenotypic_feature).
range_in(related_to, named_thing, disease_or_phenotypic_feature).
class_slot(disease_or_phenotypic_feature, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, disease_or_phenotypic_feature).
range_in(interacts_with, named_thing, disease_or_phenotypic_feature).
class_slot(disease_or_phenotypic_feature, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, disease_or_phenotypic_feature).
class_slot(disease_or_phenotypic_feature, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, disease_or_phenotypic_feature).
class_slot(disease_or_phenotypic_feature, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, disease_or_phenotypic_feature).
range_in(synonym, label_type, disease_or_phenotypic_feature).
class_slot(disease_or_phenotypic_feature, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, disease_or_phenotypic_feature).
class_slot(disease_or_phenotypic_feature, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, disease_or_phenotypic_feature).
class_slot(disease_or_phenotypic_feature, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, disease_or_phenotypic_feature).
class_slot(disease_or_phenotypic_feature, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, disease_or_phenotypic_feature).
range_in(has_phenotype, phenotypic_feature, disease_or_phenotypic_feature).
class_slot(disease_or_phenotypic_feature, correlated_with).
required(correlated_with).
slotrange(molecular_entity).
multivalued_in(correlated_with, disease_or_phenotypic_feature).
range_in(correlated_with, molecular_entity, disease_or_phenotypic_feature).
class_slot(disease_or_phenotypic_feature, has_biomarker).
required(has_biomarker).
slotrange(molecular_entity).
multivalued_in(has_biomarker, disease_or_phenotypic_feature).
range_in(has_biomarker, molecular_entity, disease_or_phenotypic_feature).
class_slot(disease_or_phenotypic_feature, treated_by).
required(treated_by).
slotrange(named_thing).
multivalued_in(treated_by, disease_or_phenotypic_feature).
range_in(treated_by, named_thing, disease_or_phenotypic_feature).
class_slot(disease_or_phenotypic_feature, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, disease_or_phenotypic_feature).
range_in(in_taxon, organism_taxon, disease_or_phenotypic_feature).
class(disease_or_phenotypic_feature_association_to_location_association).
is_a(disease_or_phenotypic_feature_association_to_location_association, disease_or_phenotypic_feature_association_to_thing_association).
has_uri(disease_or_phenotypic_feature_association_to_location_association, 'http://w3id.org/biolink/vocab/DiseaseOrPhenotypicFeatureAssociationToLocationAssociation').
class_slot(disease_or_phenotypic_feature_association_to_location_association, id).
required(id).
slotrange(identifier_type).
required_in(id, disease_or_phenotypic_feature_association_to_location_association).
range_in(id, identifier_type, disease_or_phenotypic_feature_association_to_location_association).
class_slot(disease_or_phenotypic_feature_association_to_location_association, subject).
required(subject).
slotrange(disease_or_phenotypic_feature).
required_in(subject, disease_or_phenotypic_feature_association_to_location_association).
range_in(subject, disease_or_phenotypic_feature, disease_or_phenotypic_feature_association_to_location_association).
class_slot(disease_or_phenotypic_feature_association_to_location_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, disease_or_phenotypic_feature_association_to_location_association).
range_in(relation, iri_type, disease_or_phenotypic_feature_association_to_location_association).
class_slot(disease_or_phenotypic_feature_association_to_location_association, object).
required(object).
slotrange(anatomical_entity).
required_in(object, disease_or_phenotypic_feature_association_to_location_association).
range_in(object, anatomical_entity, disease_or_phenotypic_feature_association_to_location_association).
class_slot(disease_or_phenotypic_feature_association_to_location_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, disease_or_phenotypic_feature_association_to_location_association).
class_slot(disease_or_phenotypic_feature_association_to_location_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, disease_or_phenotypic_feature_association_to_location_association).
class_slot(disease_or_phenotypic_feature_association_to_location_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, disease_or_phenotypic_feature_association_to_location_association).
range_in(qualifiers, ontology_class, disease_or_phenotypic_feature_association_to_location_association).
class_slot(disease_or_phenotypic_feature_association_to_location_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, disease_or_phenotypic_feature_association_to_location_association).
range_in(publications, publication, disease_or_phenotypic_feature_association_to_location_association).
class_slot(disease_or_phenotypic_feature_association_to_location_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, disease_or_phenotypic_feature_association_to_location_association).
class_slot(disease_or_phenotypic_feature_association_to_location_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, disease_or_phenotypic_feature_association_to_location_association).
class(disease_or_phenotypic_feature_association_to_thing_association).
is_a(disease_or_phenotypic_feature_association_to_thing_association, association).
defining_slots(association, [subject]).
has_uri(disease_or_phenotypic_feature_association_to_thing_association, 'http://w3id.org/biolink/vocab/DiseaseOrPhenotypicFeatureAssociationToThingAssociation').
class_slot(disease_or_phenotypic_feature_association_to_thing_association, id).
required(id).
slotrange(identifier_type).
required_in(id, disease_or_phenotypic_feature_association_to_thing_association).
range_in(id, identifier_type, disease_or_phenotypic_feature_association_to_thing_association).
class_slot(disease_or_phenotypic_feature_association_to_thing_association, subject).
required(subject).
slotrange(disease_or_phenotypic_feature).
required_in(subject, disease_or_phenotypic_feature_association_to_thing_association).
range_in(subject, disease_or_phenotypic_feature, disease_or_phenotypic_feature_association_to_thing_association).
class_slot(disease_or_phenotypic_feature_association_to_thing_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, disease_or_phenotypic_feature_association_to_thing_association).
range_in(relation, iri_type, disease_or_phenotypic_feature_association_to_thing_association).
class_slot(disease_or_phenotypic_feature_association_to_thing_association, object).
required(object).
slotrange(iri_type).
required_in(object, disease_or_phenotypic_feature_association_to_thing_association).
range_in(object, iri_type, disease_or_phenotypic_feature_association_to_thing_association).
class_slot(disease_or_phenotypic_feature_association_to_thing_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, disease_or_phenotypic_feature_association_to_thing_association).
class_slot(disease_or_phenotypic_feature_association_to_thing_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, disease_or_phenotypic_feature_association_to_thing_association).
class_slot(disease_or_phenotypic_feature_association_to_thing_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, disease_or_phenotypic_feature_association_to_thing_association).
range_in(qualifiers, ontology_class, disease_or_phenotypic_feature_association_to_thing_association).
class_slot(disease_or_phenotypic_feature_association_to_thing_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, disease_or_phenotypic_feature_association_to_thing_association).
range_in(publications, publication, disease_or_phenotypic_feature_association_to_thing_association).
class_slot(disease_or_phenotypic_feature_association_to_thing_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, disease_or_phenotypic_feature_association_to_thing_association).
class_slot(disease_or_phenotypic_feature_association_to_thing_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, disease_or_phenotypic_feature_association_to_thing_association).
class(disease_to_phenotypic_feature_association).
mixin(disease_to_phenotypic_feature_association, entity_to_phenotypic_feature_association).
mixin(disease_to_phenotypic_feature_association, disease_to_thing_association).
is_a(disease_to_phenotypic_feature_association, association).
defining_slots(association, [subject, object]).
has_uri(disease_to_phenotypic_feature_association, 'http://w3id.org/biolink/vocab/DiseaseToPhenotypicFeatureAssociation').
class_slot(disease_to_phenotypic_feature_association, id).
required(id).
slotrange(identifier_type).
required_in(id, disease_to_phenotypic_feature_association).
range_in(id, identifier_type, disease_to_phenotypic_feature_association).
class_slot(disease_to_phenotypic_feature_association, subject).
required(subject).
slotrange(iri_type).
required_in(subject, disease_to_phenotypic_feature_association).
range_in(subject, iri_type, disease_to_phenotypic_feature_association).
class_slot(disease_to_phenotypic_feature_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, disease_to_phenotypic_feature_association).
range_in(relation, iri_type, disease_to_phenotypic_feature_association).
class_slot(disease_to_phenotypic_feature_association, object).
required(object).
slotrange(iri_type).
required_in(object, disease_to_phenotypic_feature_association).
range_in(object, iri_type, disease_to_phenotypic_feature_association).
class_slot(disease_to_phenotypic_feature_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, disease_to_phenotypic_feature_association).
class_slot(disease_to_phenotypic_feature_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, disease_to_phenotypic_feature_association).
class_slot(disease_to_phenotypic_feature_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, disease_to_phenotypic_feature_association).
range_in(qualifiers, ontology_class, disease_to_phenotypic_feature_association).
class_slot(disease_to_phenotypic_feature_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, disease_to_phenotypic_feature_association).
range_in(publications, publication, disease_to_phenotypic_feature_association).
class_slot(disease_to_phenotypic_feature_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, disease_to_phenotypic_feature_association).
class_slot(disease_to_phenotypic_feature_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, disease_to_phenotypic_feature_association).
class_slot(disease_to_phenotypic_feature_association, sex_qualifier).
required(sex_qualifier).
slotrange(biological_sex).
range_in(sex_qualifier, biological_sex, disease_to_phenotypic_feature_association).
class_slot(disease_to_phenotypic_feature_association, frequency_qualifier).
required(frequency_qualifier).
slotrange(frequency_value).
range_in(frequency_qualifier, frequency_value, disease_to_phenotypic_feature_association).
class_slot(disease_to_phenotypic_feature_association, severity_qualifier).
required(severity_qualifier).
slotrange(severity_value).
range_in(severity_qualifier, severity_value, disease_to_phenotypic_feature_association).
class_slot(disease_to_phenotypic_feature_association, onset_qualifier).
required(onset_qualifier).
slotrange(onset).
range_in(onset_qualifier, onset, disease_to_phenotypic_feature_association).
class(disease_to_thing_association).
is_a(disease_to_thing_association, association).
defining_slots(association, [subject]).
has_uri(disease_to_thing_association, 'http://w3id.org/biolink/vocab/DiseaseToThingAssociation').
class_slot(disease_to_thing_association, id).
required(id).
slotrange(identifier_type).
required_in(id, disease_to_thing_association).
range_in(id, identifier_type, disease_to_thing_association).
class_slot(disease_to_thing_association, subject).
required(subject).
slotrange(disease).
required_in(subject, disease_to_thing_association).
range_in(subject, disease, disease_to_thing_association).
class_slot(disease_to_thing_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, disease_to_thing_association).
range_in(relation, iri_type, disease_to_thing_association).
class_slot(disease_to_thing_association, object).
required(object).
slotrange(iri_type).
required_in(object, disease_to_thing_association).
range_in(object, iri_type, disease_to_thing_association).
class_slot(disease_to_thing_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, disease_to_thing_association).
class_slot(disease_to_thing_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, disease_to_thing_association).
class_slot(disease_to_thing_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, disease_to_thing_association).
range_in(qualifiers, ontology_class, disease_to_thing_association).
class_slot(disease_to_thing_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, disease_to_thing_association).
range_in(publications, publication, disease_to_thing_association).
class_slot(disease_to_thing_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, disease_to_thing_association).
class_slot(disease_to_thing_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, disease_to_thing_association).
class(drug).
is_a(drug, chemical_substance).
has_uri(drug, 'http://w3id.org/biolink/vocab/Drug').
class_slot(drug, id).
required(id).
slotrange(identifier_type).
required_in(id, drug).
range_in(id, identifier_type, drug).
class_slot(drug, name).
required(name).
slotrange(label_type).
range_in(name, label_type, drug).
class_slot(drug, category).
required(category).
slotrange(iri_type).
multivalued_in(category, drug).
range_in(category, iri_type, drug).
class_slot(drug, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, drug).
range_in(related_to, named_thing, drug).
class_slot(drug, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, drug).
range_in(interacts_with, named_thing, drug).
class_slot(drug, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, drug).
class_slot(drug, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, drug).
class_slot(drug, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, drug).
range_in(synonym, label_type, drug).
class_slot(drug, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, drug).
class_slot(drug, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, drug).
class_slot(drug, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, drug).
class_slot(drug, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, drug).
range_in(has_phenotype, phenotypic_feature, drug).
class_slot(drug, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, drug).
range_in(molecularly_interacts_with, molecular_entity, drug).
class_slot(drug, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, drug).
range_in(affects_abundance_of, molecular_entity, drug).
class_slot(drug, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, drug).
range_in(increases_abundance_of, molecular_entity, drug).
class_slot(drug, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, drug).
range_in(decreases_abundance_of, molecular_entity, drug).
class_slot(drug, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, drug).
range_in(affects_activity_of, molecular_entity, drug).
class_slot(drug, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, drug).
range_in(increases_activity_of, molecular_entity, drug).
class_slot(drug, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, drug).
range_in(decreases_activity_of, molecular_entity, drug).
class_slot(drug, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, drug).
range_in(affects_expression_of, genomic_entity, drug).
class_slot(drug, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, drug).
range_in(increases_expression_of, genomic_entity, drug).
class_slot(drug, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, drug).
range_in(decreases_expression_of, genomic_entity, drug).
class_slot(drug, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, drug).
range_in(affects_folding_of, molecular_entity, drug).
class_slot(drug, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, drug).
range_in(increases_folding_of, molecular_entity, drug).
class_slot(drug, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, drug).
range_in(decreases_folding_of, molecular_entity, drug).
class_slot(drug, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, drug).
range_in(affects_localization_of, molecular_entity, drug).
class_slot(drug, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, drug).
range_in(increases_localization_of, molecular_entity, drug).
class_slot(drug, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, drug).
range_in(decreases_localization_of, molecular_entity, drug).
class_slot(drug, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, drug).
range_in(affects_metabolic_processing_of, molecular_entity, drug).
class_slot(drug, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, drug).
range_in(increases_metabolic_processing_of, molecular_entity, drug).
class_slot(drug, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, drug).
range_in(decreases_metabolic_processing_of, molecular_entity, drug).
class_slot(drug, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, drug).
range_in(affects_molecular_modification_of, molecular_entity, drug).
class_slot(drug, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, drug).
range_in(increases_molecular_modification_of, molecular_entity, drug).
class_slot(drug, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, drug).
range_in(decreases_molecular_modification_of, molecular_entity, drug).
class_slot(drug, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, drug).
range_in(affects_synthesis_of, molecular_entity, drug).
class_slot(drug, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, drug).
range_in(increases_synthesis_of, molecular_entity, drug).
class_slot(drug, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, drug).
range_in(decreases_synthesis_of, molecular_entity, drug).
class_slot(drug, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, drug).
range_in(affects_degradation_of, molecular_entity, drug).
class_slot(drug, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, drug).
range_in(increases_degradation_of, molecular_entity, drug).
class_slot(drug, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, drug).
range_in(decreases_degradation_of, molecular_entity, drug).
class_slot(drug, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, drug).
range_in(affects_mutation_rate_of, genomic_entity, drug).
class_slot(drug, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, drug).
range_in(increases_mutation_rate_of, genomic_entity, drug).
class_slot(drug, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, drug).
range_in(decreases_mutation_rate_of, genomic_entity, drug).
class_slot(drug, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, drug).
range_in(affects_response_to, molecular_entity, drug).
class_slot(drug, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, drug).
range_in(increases_response_to, molecular_entity, drug).
class_slot(drug, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, drug).
range_in(decreases_response_to, molecular_entity, drug).
class_slot(drug, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, drug).
range_in(affects_splicing_of, transcript, drug).
class_slot(drug, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, drug).
range_in(increases_splicing_of, transcript, drug).
class_slot(drug, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, drug).
range_in(decreases_splicing_of, transcript, drug).
class_slot(drug, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, drug).
range_in(affects_stability_of, molecular_entity, drug).
class_slot(drug, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, drug).
range_in(increases_stability_of, molecular_entity, drug).
class_slot(drug, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, drug).
range_in(decreases_stability_of, molecular_entity, drug).
class_slot(drug, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, drug).
range_in(affects_transport_of, molecular_entity, drug).
class_slot(drug, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, drug).
range_in(increases_transport_of, molecular_entity, drug).
class_slot(drug, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, drug).
range_in(decreases_transport_of, molecular_entity, drug).
class_slot(drug, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, drug).
range_in(affects_secretion_of, molecular_entity, drug).
class_slot(drug, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, drug).
range_in(increases_secretion_of, molecular_entity, drug).
class_slot(drug, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, drug).
range_in(decreases_secretion_of, molecular_entity, drug).
class_slot(drug, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, drug).
range_in(affects_uptake_of, molecular_entity, drug).
class_slot(drug, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, drug).
range_in(increases_uptake_of, molecular_entity, drug).
class_slot(drug, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, drug).
range_in(decreases_uptake_of, molecular_entity, drug).
class_slot(drug, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, drug).
range_in(regulates_entity_to_entity, molecular_entity, drug).
class_slot(drug, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, drug).
range_in(biomarker_for, disease_or_phenotypic_feature, drug).
class_slot(drug, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, drug).
range_in(in_taxon, organism_taxon, drug).
class(drug_exposure).
is_a(drug_exposure, environment).
has_uri(drug_exposure, 'http://w3id.org/biolink/vocab/DrugExposure').
class_slot(drug_exposure, id).
required(id).
slotrange(identifier_type).
required_in(id, drug_exposure).
range_in(id, identifier_type, drug_exposure).
class_slot(drug_exposure, name).
required(name).
slotrange(label_type).
range_in(name, label_type, drug_exposure).
class_slot(drug_exposure, category).
required(category).
slotrange(iri_type).
multivalued_in(category, drug_exposure).
range_in(category, iri_type, drug_exposure).
class_slot(drug_exposure, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, drug_exposure).
range_in(related_to, named_thing, drug_exposure).
class_slot(drug_exposure, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, drug_exposure).
range_in(interacts_with, named_thing, drug_exposure).
class_slot(drug_exposure, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, drug_exposure).
class_slot(drug_exposure, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, drug_exposure).
class_slot(drug_exposure, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, drug_exposure).
range_in(synonym, label_type, drug_exposure).
class_slot(drug_exposure, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, drug_exposure).
class_slot(drug_exposure, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, drug_exposure).
class_slot(drug_exposure, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, drug_exposure).
class_slot(drug_exposure, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, drug_exposure).
range_in(has_phenotype, phenotypic_feature, drug_exposure).
class_slot(drug_exposure, drug).
required(drug).
slotrange(chemical_substance).
multivalued_in(drug, drug_exposure).
required_in(drug, drug_exposure).
range_in(drug, chemical_substance, drug_exposure).
class(entity_to_disease_association).
is_a(entity_to_disease_association, entity_to_feature_or_disease_qualifiers).
defining_slots(entity_to_feature_or_disease_qualifiers, [object]).
has_uri(entity_to_disease_association, 'http://w3id.org/biolink/vocab/EntityToDiseaseAssociation').
class_slot(entity_to_disease_association, frequency_qualifier).
required(frequency_qualifier).
slotrange(frequency_value).
range_in(frequency_qualifier, frequency_value, entity_to_disease_association).
class_slot(entity_to_disease_association, severity_qualifier).
required(severity_qualifier).
slotrange(severity_value).
range_in(severity_qualifier, severity_value, entity_to_disease_association).
class_slot(entity_to_disease_association, onset_qualifier).
required(onset_qualifier).
slotrange(onset).
range_in(onset_qualifier, onset, entity_to_disease_association).
class_slot(entity_to_disease_association, object).
required(object).
slotrange(disease).
required_in(object, entity_to_disease_association).
range_in(object, disease, entity_to_disease_association).
class(entity_to_feature_or_disease_qualifiers).
is_a(entity_to_feature_or_disease_qualifiers, frequency_qualifier_mixin).
has_uri(entity_to_feature_or_disease_qualifiers, 'http://w3id.org/biolink/vocab/EntityToFeatureOrDiseaseQualifiers').
class_slot(entity_to_feature_or_disease_qualifiers, frequency_qualifier).
required(frequency_qualifier).
slotrange(frequency_value).
range_in(frequency_qualifier, frequency_value, entity_to_feature_or_disease_qualifiers).
class_slot(entity_to_feature_or_disease_qualifiers, severity_qualifier).
required(severity_qualifier).
slotrange(severity_value).
range_in(severity_qualifier, severity_value, entity_to_feature_or_disease_qualifiers).
class_slot(entity_to_feature_or_disease_qualifiers, onset_qualifier).
required(onset_qualifier).
slotrange(onset).
range_in(onset_qualifier, onset, entity_to_feature_or_disease_qualifiers).
class(entity_to_phenotypic_feature_association).
mixin(entity_to_phenotypic_feature_association, entity_to_feature_or_disease_qualifiers).
is_a(entity_to_phenotypic_feature_association, association).
defining_slots(association, [object]).
has_uri(entity_to_phenotypic_feature_association, 'http://w3id.org/biolink/vocab/EntityToPhenotypicFeatureAssociation').
class_slot(entity_to_phenotypic_feature_association, id).
required(id).
slotrange(identifier_type).
required_in(id, entity_to_phenotypic_feature_association).
range_in(id, identifier_type, entity_to_phenotypic_feature_association).
class_slot(entity_to_phenotypic_feature_association, subject).
required(subject).
slotrange(iri_type).
required_in(subject, entity_to_phenotypic_feature_association).
range_in(subject, iri_type, entity_to_phenotypic_feature_association).
class_slot(entity_to_phenotypic_feature_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, entity_to_phenotypic_feature_association).
range_in(relation, iri_type, entity_to_phenotypic_feature_association).
class_slot(entity_to_phenotypic_feature_association, object).
required(object).
slotrange(phenotypic_feature).
required_in(object, entity_to_phenotypic_feature_association).
range_in(object, phenotypic_feature, entity_to_phenotypic_feature_association).
class_slot(entity_to_phenotypic_feature_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, entity_to_phenotypic_feature_association).
class_slot(entity_to_phenotypic_feature_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, entity_to_phenotypic_feature_association).
class_slot(entity_to_phenotypic_feature_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, entity_to_phenotypic_feature_association).
range_in(qualifiers, ontology_class, entity_to_phenotypic_feature_association).
class_slot(entity_to_phenotypic_feature_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, entity_to_phenotypic_feature_association).
range_in(publications, publication, entity_to_phenotypic_feature_association).
class_slot(entity_to_phenotypic_feature_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, entity_to_phenotypic_feature_association).
class_slot(entity_to_phenotypic_feature_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, entity_to_phenotypic_feature_association).
class_slot(entity_to_phenotypic_feature_association, sex_qualifier).
required(sex_qualifier).
slotrange(biological_sex).
range_in(sex_qualifier, biological_sex, entity_to_phenotypic_feature_association).
class_slot(entity_to_phenotypic_feature_association, frequency_qualifier).
required(frequency_qualifier).
slotrange(frequency_value).
range_in(frequency_qualifier, frequency_value, entity_to_phenotypic_feature_association).
class_slot(entity_to_phenotypic_feature_association, severity_qualifier).
required(severity_qualifier).
slotrange(severity_value).
range_in(severity_qualifier, severity_value, entity_to_phenotypic_feature_association).
class_slot(entity_to_phenotypic_feature_association, onset_qualifier).
required(onset_qualifier).
slotrange(onset).
range_in(onset_qualifier, onset, entity_to_phenotypic_feature_association).
class_slot(entity_to_phenotypic_feature_association, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, entity_to_phenotypic_feature_association).
class(environment).
is_a(environment, biological_entity).
has_uri(environment, 'http://w3id.org/biolink/vocab/Environment').
class_slot(environment, id).
required(id).
slotrange(identifier_type).
required_in(id, environment).
range_in(id, identifier_type, environment).
class_slot(environment, name).
required(name).
slotrange(label_type).
range_in(name, label_type, environment).
class_slot(environment, category).
required(category).
slotrange(iri_type).
multivalued_in(category, environment).
range_in(category, iri_type, environment).
class_slot(environment, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, environment).
range_in(related_to, named_thing, environment).
class_slot(environment, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, environment).
range_in(interacts_with, named_thing, environment).
class_slot(environment, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, environment).
class_slot(environment, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, environment).
class_slot(environment, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, environment).
range_in(synonym, label_type, environment).
class_slot(environment, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, environment).
class_slot(environment, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, environment).
class_slot(environment, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, environment).
class_slot(environment, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, environment).
range_in(has_phenotype, phenotypic_feature, environment).
class(environment_to_phenotypic_feature_association).
mixin(environment_to_phenotypic_feature_association, entity_to_phenotypic_feature_association).
is_a(environment_to_phenotypic_feature_association, association).
defining_slots(association, [subject, object]).
has_uri(environment_to_phenotypic_feature_association, 'http://w3id.org/biolink/vocab/EnvironmentToPhenotypicFeatureAssociation').
class_slot(environment_to_phenotypic_feature_association, id).
required(id).
slotrange(identifier_type).
required_in(id, environment_to_phenotypic_feature_association).
range_in(id, identifier_type, environment_to_phenotypic_feature_association).
class_slot(environment_to_phenotypic_feature_association, subject).
required(subject).
slotrange(environment).
required_in(subject, environment_to_phenotypic_feature_association).
range_in(subject, environment, environment_to_phenotypic_feature_association).
class_slot(environment_to_phenotypic_feature_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, environment_to_phenotypic_feature_association).
range_in(relation, iri_type, environment_to_phenotypic_feature_association).
class_slot(environment_to_phenotypic_feature_association, object).
required(object).
slotrange(iri_type).
required_in(object, environment_to_phenotypic_feature_association).
range_in(object, iri_type, environment_to_phenotypic_feature_association).
class_slot(environment_to_phenotypic_feature_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, environment_to_phenotypic_feature_association).
class_slot(environment_to_phenotypic_feature_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, environment_to_phenotypic_feature_association).
class_slot(environment_to_phenotypic_feature_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, environment_to_phenotypic_feature_association).
range_in(qualifiers, ontology_class, environment_to_phenotypic_feature_association).
class_slot(environment_to_phenotypic_feature_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, environment_to_phenotypic_feature_association).
range_in(publications, publication, environment_to_phenotypic_feature_association).
class_slot(environment_to_phenotypic_feature_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, environment_to_phenotypic_feature_association).
class_slot(environment_to_phenotypic_feature_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, environment_to_phenotypic_feature_association).
class_slot(environment_to_phenotypic_feature_association, sex_qualifier).
required(sex_qualifier).
slotrange(biological_sex).
range_in(sex_qualifier, biological_sex, environment_to_phenotypic_feature_association).
class_slot(environment_to_phenotypic_feature_association, frequency_qualifier).
required(frequency_qualifier).
slotrange(frequency_value).
range_in(frequency_qualifier, frequency_value, environment_to_phenotypic_feature_association).
class_slot(environment_to_phenotypic_feature_association, severity_qualifier).
required(severity_qualifier).
slotrange(severity_value).
range_in(severity_qualifier, severity_value, environment_to_phenotypic_feature_association).
class_slot(environment_to_phenotypic_feature_association, onset_qualifier).
required(onset_qualifier).
slotrange(onset).
range_in(onset_qualifier, onset, environment_to_phenotypic_feature_association).
class(environmental_feature).
is_a(environmental_feature, planetary_entity).
has_uri(environmental_feature, 'http://w3id.org/biolink/vocab/EnvironmentalFeature').
class_slot(environmental_feature, id).
required(id).
slotrange(identifier_type).
required_in(id, environmental_feature).
range_in(id, identifier_type, environmental_feature).
class_slot(environmental_feature, name).
required(name).
slotrange(label_type).
range_in(name, label_type, environmental_feature).
class_slot(environmental_feature, category).
required(category).
slotrange(iri_type).
multivalued_in(category, environmental_feature).
range_in(category, iri_type, environmental_feature).
class_slot(environmental_feature, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, environmental_feature).
range_in(related_to, named_thing, environmental_feature).
class_slot(environmental_feature, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, environmental_feature).
range_in(interacts_with, named_thing, environmental_feature).
class_slot(environmental_feature, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, environmental_feature).
class_slot(environmental_feature, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, environmental_feature).
class_slot(environmental_feature, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, environmental_feature).
range_in(synonym, label_type, environmental_feature).
class_slot(environmental_feature, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, environmental_feature).
class_slot(environmental_feature, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, environmental_feature).
class_slot(environmental_feature, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, environmental_feature).
class(environmental_process).
mixin(environmental_process, occurrent).
is_a(environmental_process, planetary_entity).
has_uri(environmental_process, 'http://w3id.org/biolink/vocab/EnvironmentalProcess').
class_slot(environmental_process, id).
required(id).
slotrange(identifier_type).
required_in(id, environmental_process).
range_in(id, identifier_type, environmental_process).
class_slot(environmental_process, name).
required(name).
slotrange(label_type).
range_in(name, label_type, environmental_process).
class_slot(environmental_process, category).
required(category).
slotrange(iri_type).
multivalued_in(category, environmental_process).
range_in(category, iri_type, environmental_process).
class_slot(environmental_process, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, environmental_process).
range_in(related_to, named_thing, environmental_process).
class_slot(environmental_process, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, environmental_process).
range_in(interacts_with, named_thing, environmental_process).
class_slot(environmental_process, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, environmental_process).
class_slot(environmental_process, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, environmental_process).
class_slot(environmental_process, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, environmental_process).
range_in(synonym, label_type, environmental_process).
class_slot(environmental_process, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, environmental_process).
class_slot(environmental_process, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, environmental_process).
class_slot(environmental_process, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, environmental_process).
class_slot(environmental_process, regulates_process_to_process).
required(regulates_process_to_process).
slotrange(occurrent).
multivalued_in(regulates_process_to_process, environmental_process).
range_in(regulates_process_to_process, occurrent, environmental_process).
class_slot(environmental_process, has_participant).
required(has_participant).
slotrange(named_thing).
multivalued_in(has_participant, environmental_process).
range_in(has_participant, named_thing, environmental_process).
class_slot(environmental_process, has_input).
required(has_input).
slotrange(named_thing).
multivalued_in(has_input, environmental_process).
range_in(has_input, named_thing, environmental_process).
class_slot(environmental_process, precedes).
required(precedes).
slotrange(occurrent).
multivalued_in(precedes, environmental_process).
range_in(precedes, occurrent, environmental_process).
class(evidence_type).
is_a(evidence_type, information_content_entity).
has_uri(evidence_type, 'http://w3id.org/biolink/vocab/EvidenceType').
class_slot(evidence_type, id).
required(id).
slotrange(identifier_type).
required_in(id, evidence_type).
range_in(id, identifier_type, evidence_type).
class_slot(evidence_type, name).
required(name).
slotrange(label_type).
range_in(name, label_type, evidence_type).
class_slot(evidence_type, category).
required(category).
slotrange(iri_type).
multivalued_in(category, evidence_type).
range_in(category, iri_type, evidence_type).
class_slot(evidence_type, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, evidence_type).
range_in(related_to, named_thing, evidence_type).
class_slot(evidence_type, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, evidence_type).
range_in(interacts_with, named_thing, evidence_type).
class_slot(evidence_type, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, evidence_type).
class_slot(evidence_type, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, evidence_type).
class_slot(evidence_type, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, evidence_type).
range_in(synonym, label_type, evidence_type).
class_slot(evidence_type, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, evidence_type).
class_slot(evidence_type, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, evidence_type).
class_slot(evidence_type, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, evidence_type).
class(exon).
is_a(exon, genomic_entity).
has_uri(exon, 'http://w3id.org/biolink/vocab/Exon').
class_slot(exon, id).
required(id).
slotrange(identifier_type).
required_in(id, exon).
range_in(id, identifier_type, exon).
class_slot(exon, name).
required(name).
slotrange(label_type).
range_in(name, label_type, exon).
class_slot(exon, category).
required(category).
slotrange(iri_type).
multivalued_in(category, exon).
range_in(category, iri_type, exon).
class_slot(exon, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, exon).
range_in(related_to, named_thing, exon).
class_slot(exon, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, exon).
range_in(interacts_with, named_thing, exon).
class_slot(exon, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, exon).
class_slot(exon, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, exon).
class_slot(exon, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, exon).
range_in(synonym, label_type, exon).
class_slot(exon, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, exon).
class_slot(exon, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, exon).
class_slot(exon, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, exon).
class_slot(exon, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, exon).
range_in(has_phenotype, phenotypic_feature, exon).
class_slot(exon, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, exon).
range_in(molecularly_interacts_with, molecular_entity, exon).
class_slot(exon, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, exon).
range_in(affects_abundance_of, molecular_entity, exon).
class_slot(exon, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, exon).
range_in(increases_abundance_of, molecular_entity, exon).
class_slot(exon, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, exon).
range_in(decreases_abundance_of, molecular_entity, exon).
class_slot(exon, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, exon).
range_in(affects_activity_of, molecular_entity, exon).
class_slot(exon, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, exon).
range_in(increases_activity_of, molecular_entity, exon).
class_slot(exon, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, exon).
range_in(decreases_activity_of, molecular_entity, exon).
class_slot(exon, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, exon).
range_in(affects_expression_of, genomic_entity, exon).
class_slot(exon, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, exon).
range_in(increases_expression_of, genomic_entity, exon).
class_slot(exon, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, exon).
range_in(decreases_expression_of, genomic_entity, exon).
class_slot(exon, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, exon).
range_in(affects_folding_of, molecular_entity, exon).
class_slot(exon, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, exon).
range_in(increases_folding_of, molecular_entity, exon).
class_slot(exon, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, exon).
range_in(decreases_folding_of, molecular_entity, exon).
class_slot(exon, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, exon).
range_in(affects_localization_of, molecular_entity, exon).
class_slot(exon, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, exon).
range_in(increases_localization_of, molecular_entity, exon).
class_slot(exon, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, exon).
range_in(decreases_localization_of, molecular_entity, exon).
class_slot(exon, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, exon).
range_in(affects_metabolic_processing_of, molecular_entity, exon).
class_slot(exon, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, exon).
range_in(increases_metabolic_processing_of, molecular_entity, exon).
class_slot(exon, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, exon).
range_in(decreases_metabolic_processing_of, molecular_entity, exon).
class_slot(exon, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, exon).
range_in(affects_molecular_modification_of, molecular_entity, exon).
class_slot(exon, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, exon).
range_in(increases_molecular_modification_of, molecular_entity, exon).
class_slot(exon, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, exon).
range_in(decreases_molecular_modification_of, molecular_entity, exon).
class_slot(exon, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, exon).
range_in(affects_synthesis_of, molecular_entity, exon).
class_slot(exon, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, exon).
range_in(increases_synthesis_of, molecular_entity, exon).
class_slot(exon, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, exon).
range_in(decreases_synthesis_of, molecular_entity, exon).
class_slot(exon, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, exon).
range_in(affects_degradation_of, molecular_entity, exon).
class_slot(exon, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, exon).
range_in(increases_degradation_of, molecular_entity, exon).
class_slot(exon, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, exon).
range_in(decreases_degradation_of, molecular_entity, exon).
class_slot(exon, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, exon).
range_in(affects_mutation_rate_of, genomic_entity, exon).
class_slot(exon, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, exon).
range_in(increases_mutation_rate_of, genomic_entity, exon).
class_slot(exon, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, exon).
range_in(decreases_mutation_rate_of, genomic_entity, exon).
class_slot(exon, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, exon).
range_in(affects_response_to, molecular_entity, exon).
class_slot(exon, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, exon).
range_in(increases_response_to, molecular_entity, exon).
class_slot(exon, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, exon).
range_in(decreases_response_to, molecular_entity, exon).
class_slot(exon, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, exon).
range_in(affects_splicing_of, transcript, exon).
class_slot(exon, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, exon).
range_in(increases_splicing_of, transcript, exon).
class_slot(exon, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, exon).
range_in(decreases_splicing_of, transcript, exon).
class_slot(exon, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, exon).
range_in(affects_stability_of, molecular_entity, exon).
class_slot(exon, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, exon).
range_in(increases_stability_of, molecular_entity, exon).
class_slot(exon, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, exon).
range_in(decreases_stability_of, molecular_entity, exon).
class_slot(exon, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, exon).
range_in(affects_transport_of, molecular_entity, exon).
class_slot(exon, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, exon).
range_in(increases_transport_of, molecular_entity, exon).
class_slot(exon, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, exon).
range_in(decreases_transport_of, molecular_entity, exon).
class_slot(exon, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, exon).
range_in(affects_secretion_of, molecular_entity, exon).
class_slot(exon, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, exon).
range_in(increases_secretion_of, molecular_entity, exon).
class_slot(exon, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, exon).
range_in(decreases_secretion_of, molecular_entity, exon).
class_slot(exon, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, exon).
range_in(affects_uptake_of, molecular_entity, exon).
class_slot(exon, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, exon).
range_in(increases_uptake_of, molecular_entity, exon).
class_slot(exon, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, exon).
range_in(decreases_uptake_of, molecular_entity, exon).
class_slot(exon, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, exon).
range_in(regulates_entity_to_entity, molecular_entity, exon).
class_slot(exon, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, exon).
range_in(biomarker_for, disease_or_phenotypic_feature, exon).
class_slot(exon, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, exon).
range_in(in_taxon, organism_taxon, exon).
class_slot(exon, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, exon).
class(exon_to_transcript_relationship).
is_a(exon_to_transcript_relationship, sequence_feature_relationship).
defining_slots(sequence_feature_relationship, [subject, object]).
has_uri(exon_to_transcript_relationship, 'http://w3id.org/biolink/vocab/ExonToTranscriptRelationship').
class_slot(exon_to_transcript_relationship, id).
required(id).
slotrange(identifier_type).
required_in(id, exon_to_transcript_relationship).
range_in(id, identifier_type, exon_to_transcript_relationship).
class_slot(exon_to_transcript_relationship, subject).
required(subject).
slotrange(exon).
required_in(subject, exon_to_transcript_relationship).
range_in(subject, exon, exon_to_transcript_relationship).
class_slot(exon_to_transcript_relationship, relation).
required(relation).
slotrange(iri_type).
required_in(relation, exon_to_transcript_relationship).
range_in(relation, iri_type, exon_to_transcript_relationship).
class_slot(exon_to_transcript_relationship, object).
required(object).
slotrange(transcript).
required_in(object, exon_to_transcript_relationship).
range_in(object, transcript, exon_to_transcript_relationship).
class_slot(exon_to_transcript_relationship, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, exon_to_transcript_relationship).
class_slot(exon_to_transcript_relationship, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, exon_to_transcript_relationship).
class_slot(exon_to_transcript_relationship, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, exon_to_transcript_relationship).
range_in(qualifiers, ontology_class, exon_to_transcript_relationship).
class_slot(exon_to_transcript_relationship, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, exon_to_transcript_relationship).
range_in(publications, publication, exon_to_transcript_relationship).
class_slot(exon_to_transcript_relationship, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, exon_to_transcript_relationship).
class_slot(exon_to_transcript_relationship, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, exon_to_transcript_relationship).
class(frequency_qualifier_mixin).
has_uri(frequency_qualifier_mixin, 'http://w3id.org/biolink/vocab/FrequencyQualifierMixin').
class_slot(frequency_qualifier_mixin, frequency_qualifier).
required(frequency_qualifier).
slotrange(frequency_value).
range_in(frequency_qualifier, frequency_value, frequency_qualifier_mixin).
class(frequency_quantifier).
is_a(frequency_quantifier, relationship_quantifier).
has_uri(frequency_quantifier, 'http://w3id.org/biolink/vocab/FrequencyQuantifier').
class_slot(frequency_quantifier, has_count).
required(has_count).
slotrange(integer).
range_in(has_count, integer, frequency_quantifier).
class_slot(frequency_quantifier, has_total).
required(has_total).
slotrange(integer).
range_in(has_total, integer, frequency_quantifier).
class_slot(frequency_quantifier, has_quotient).
required(has_quotient).
slotrange(double).
range_in(has_quotient, double, frequency_quantifier).
class_slot(frequency_quantifier, has_percentage).
required(has_percentage).
slotrange(double).
range_in(has_percentage, double, frequency_quantifier).
class(frequency_value).
is_a(frequency_value, attribute).
has_uri(frequency_value, 'http://w3id.org/biolink/vocab/FrequencyValue').
class_slot(frequency_value, id).
required(id).
slotrange(identifier_type).
required_in(id, frequency_value).
range_in(id, identifier_type, frequency_value).
class_slot(frequency_value, name).
required(name).
slotrange(label_type).
range_in(name, label_type, frequency_value).
class_slot(frequency_value, category).
required(category).
slotrange(iri_type).
multivalued_in(category, frequency_value).
range_in(category, iri_type, frequency_value).
class_slot(frequency_value, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, frequency_value).
range_in(related_to, named_thing, frequency_value).
class_slot(frequency_value, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, frequency_value).
range_in(interacts_with, named_thing, frequency_value).
class_slot(frequency_value, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, frequency_value).
class_slot(frequency_value, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, frequency_value).
class_slot(frequency_value, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, frequency_value).
range_in(synonym, label_type, frequency_value).
class_slot(frequency_value, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, frequency_value).
class_slot(frequency_value, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, frequency_value).
class_slot(frequency_value, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, frequency_value).
class_slot(frequency_value, subclass_of).
required(subclass_of).
slotrange(ontology_class).
multivalued_in(subclass_of, frequency_value).
range_in(subclass_of, ontology_class, frequency_value).
class(functional_association).
is_a(functional_association, association).
has_uri(functional_association, 'http://w3id.org/biolink/vocab/FunctionalAssociation').
class_slot(functional_association, id).
required(id).
slotrange(identifier_type).
required_in(id, functional_association).
range_in(id, identifier_type, functional_association).
class_slot(functional_association, subject).
required(subject).
slotrange(macromolecular_machine).
required_in(subject, functional_association).
range_in(subject, macromolecular_machine, functional_association).
class_slot(functional_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, functional_association).
range_in(relation, iri_type, functional_association).
class_slot(functional_association, object).
required(object).
slotrange(gene_ontology_class).
required_in(object, functional_association).
range_in(object, gene_ontology_class, functional_association).
class_slot(functional_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, functional_association).
class_slot(functional_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, functional_association).
class_slot(functional_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, functional_association).
range_in(qualifiers, ontology_class, functional_association).
class_slot(functional_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, functional_association).
range_in(publications, publication, functional_association).
class_slot(functional_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, functional_association).
class_slot(functional_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, functional_association).
class(gene).
is_a(gene, gene_or_gene_product).
has_uri(gene, 'http://w3id.org/biolink/vocab/Gene').
class_slot(gene, id).
required(id).
slotrange(identifier_type).
required_in(id, gene).
range_in(id, identifier_type, gene).
class_slot(gene, name).
required(name).
slotrange(symbol_type).
range_in(name, symbol_type, gene).
class_slot(gene, category).
required(category).
slotrange(iri_type).
multivalued_in(category, gene).
range_in(category, iri_type, gene).
class_slot(gene, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, gene).
range_in(related_to, named_thing, gene).
class_slot(gene, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, gene).
range_in(interacts_with, named_thing, gene).
class_slot(gene, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, gene).
class_slot(gene, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, gene).
class_slot(gene, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, gene).
range_in(synonym, label_type, gene).
class_slot(gene, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, gene).
class_slot(gene, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, gene).
class_slot(gene, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, gene).
class_slot(gene, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, gene).
range_in(has_phenotype, phenotypic_feature, gene).
class_slot(gene, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, gene).
range_in(molecularly_interacts_with, molecular_entity, gene).
class_slot(gene, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, gene).
range_in(affects_abundance_of, molecular_entity, gene).
class_slot(gene, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, gene).
range_in(increases_abundance_of, molecular_entity, gene).
class_slot(gene, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, gene).
range_in(decreases_abundance_of, molecular_entity, gene).
class_slot(gene, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, gene).
range_in(affects_activity_of, molecular_entity, gene).
class_slot(gene, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, gene).
range_in(increases_activity_of, molecular_entity, gene).
class_slot(gene, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, gene).
range_in(decreases_activity_of, molecular_entity, gene).
class_slot(gene, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, gene).
range_in(affects_expression_of, genomic_entity, gene).
class_slot(gene, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, gene).
range_in(increases_expression_of, genomic_entity, gene).
class_slot(gene, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, gene).
range_in(decreases_expression_of, genomic_entity, gene).
class_slot(gene, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, gene).
range_in(affects_folding_of, molecular_entity, gene).
class_slot(gene, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, gene).
range_in(increases_folding_of, molecular_entity, gene).
class_slot(gene, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, gene).
range_in(decreases_folding_of, molecular_entity, gene).
class_slot(gene, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, gene).
range_in(affects_localization_of, molecular_entity, gene).
class_slot(gene, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, gene).
range_in(increases_localization_of, molecular_entity, gene).
class_slot(gene, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, gene).
range_in(decreases_localization_of, molecular_entity, gene).
class_slot(gene, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, gene).
range_in(affects_metabolic_processing_of, molecular_entity, gene).
class_slot(gene, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, gene).
range_in(increases_metabolic_processing_of, molecular_entity, gene).
class_slot(gene, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, gene).
range_in(decreases_metabolic_processing_of, molecular_entity, gene).
class_slot(gene, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, gene).
range_in(affects_molecular_modification_of, molecular_entity, gene).
class_slot(gene, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, gene).
range_in(increases_molecular_modification_of, molecular_entity, gene).
class_slot(gene, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, gene).
range_in(decreases_molecular_modification_of, molecular_entity, gene).
class_slot(gene, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, gene).
range_in(affects_synthesis_of, molecular_entity, gene).
class_slot(gene, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, gene).
range_in(increases_synthesis_of, molecular_entity, gene).
class_slot(gene, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, gene).
range_in(decreases_synthesis_of, molecular_entity, gene).
class_slot(gene, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, gene).
range_in(affects_degradation_of, molecular_entity, gene).
class_slot(gene, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, gene).
range_in(increases_degradation_of, molecular_entity, gene).
class_slot(gene, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, gene).
range_in(decreases_degradation_of, molecular_entity, gene).
class_slot(gene, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, gene).
range_in(affects_mutation_rate_of, genomic_entity, gene).
class_slot(gene, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, gene).
range_in(increases_mutation_rate_of, genomic_entity, gene).
class_slot(gene, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, gene).
range_in(decreases_mutation_rate_of, genomic_entity, gene).
class_slot(gene, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, gene).
range_in(affects_response_to, molecular_entity, gene).
class_slot(gene, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, gene).
range_in(increases_response_to, molecular_entity, gene).
class_slot(gene, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, gene).
range_in(decreases_response_to, molecular_entity, gene).
class_slot(gene, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, gene).
range_in(affects_splicing_of, transcript, gene).
class_slot(gene, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, gene).
range_in(increases_splicing_of, transcript, gene).
class_slot(gene, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, gene).
range_in(decreases_splicing_of, transcript, gene).
class_slot(gene, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, gene).
range_in(affects_stability_of, molecular_entity, gene).
class_slot(gene, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, gene).
range_in(increases_stability_of, molecular_entity, gene).
class_slot(gene, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, gene).
range_in(decreases_stability_of, molecular_entity, gene).
class_slot(gene, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, gene).
range_in(affects_transport_of, molecular_entity, gene).
class_slot(gene, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, gene).
range_in(increases_transport_of, molecular_entity, gene).
class_slot(gene, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, gene).
range_in(decreases_transport_of, molecular_entity, gene).
class_slot(gene, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, gene).
range_in(affects_secretion_of, molecular_entity, gene).
class_slot(gene, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, gene).
range_in(increases_secretion_of, molecular_entity, gene).
class_slot(gene, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, gene).
range_in(decreases_secretion_of, molecular_entity, gene).
class_slot(gene, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, gene).
range_in(affects_uptake_of, molecular_entity, gene).
class_slot(gene, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, gene).
range_in(increases_uptake_of, molecular_entity, gene).
class_slot(gene, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, gene).
range_in(decreases_uptake_of, molecular_entity, gene).
class_slot(gene, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, gene).
range_in(regulates_entity_to_entity, molecular_entity, gene).
class_slot(gene, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, gene).
range_in(biomarker_for, disease_or_phenotypic_feature, gene).
class_slot(gene, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, gene).
range_in(in_taxon, organism_taxon, gene).
class_slot(gene, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, gene).
class_slot(gene, in_pathway_with).
required(in_pathway_with).
slotrange(gene_or_gene_product).
multivalued_in(in_pathway_with, gene).
range_in(in_pathway_with, gene_or_gene_product, gene).
class_slot(gene, in_complex_with).
required(in_complex_with).
slotrange(gene_or_gene_product).
multivalued_in(in_complex_with, gene).
range_in(in_complex_with, gene_or_gene_product, gene).
class_slot(gene, in_cell_population_with).
required(in_cell_population_with).
slotrange(gene_or_gene_product).
multivalued_in(in_cell_population_with, gene).
range_in(in_cell_population_with, gene_or_gene_product, gene).
class_slot(gene, expressed_in).
required(expressed_in).
slotrange(anatomical_entity).
multivalued_in(expressed_in, gene).
range_in(expressed_in, anatomical_entity, gene).
class_slot(gene, genetically_interacts_with).
required(genetically_interacts_with).
slotrange(gene).
multivalued_in(genetically_interacts_with, gene).
range_in(genetically_interacts_with, gene, gene).
class_slot(gene, has_gene_product).
required(has_gene_product).
slotrange(gene_product).
multivalued_in(has_gene_product, gene).
range_in(has_gene_product, gene_product, gene).
class_slot(gene, gene_associated_with_condition).
required(gene_associated_with_condition).
slotrange(disease_or_phenotypic_feature).
multivalued_in(gene_associated_with_condition, gene).
range_in(gene_associated_with_condition, disease_or_phenotypic_feature, gene).
class(gene_as_a_model_of_disease_association).
mixin(gene_as_a_model_of_disease_association, model_to_disease_mixin).
mixin(gene_as_a_model_of_disease_association, entity_to_disease_association).
is_a(gene_as_a_model_of_disease_association, gene_to_disease_association).
defining_slots(gene_to_disease_association, [subject, object, relation]).
has_uri(gene_as_a_model_of_disease_association, 'http://w3id.org/biolink/vocab/GeneAsAModelOfDiseaseAssociation').
class_slot(gene_as_a_model_of_disease_association, id).
required(id).
slotrange(identifier_type).
required_in(id, gene_as_a_model_of_disease_association).
range_in(id, identifier_type, gene_as_a_model_of_disease_association).
class_slot(gene_as_a_model_of_disease_association, subject).
required(subject).
slotrange(gene_or_gene_product).
required_in(subject, gene_as_a_model_of_disease_association).
range_in(subject, gene_or_gene_product, gene_as_a_model_of_disease_association).
class_slot(gene_as_a_model_of_disease_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, gene_as_a_model_of_disease_association).
range_in(relation, iri_type, gene_as_a_model_of_disease_association).
class_slot(gene_as_a_model_of_disease_association, object).
required(object).
slotrange(iri_type).
required_in(object, gene_as_a_model_of_disease_association).
range_in(object, iri_type, gene_as_a_model_of_disease_association).
class_slot(gene_as_a_model_of_disease_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, gene_as_a_model_of_disease_association).
class_slot(gene_as_a_model_of_disease_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, gene_as_a_model_of_disease_association).
class_slot(gene_as_a_model_of_disease_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, gene_as_a_model_of_disease_association).
range_in(qualifiers, ontology_class, gene_as_a_model_of_disease_association).
class_slot(gene_as_a_model_of_disease_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, gene_as_a_model_of_disease_association).
range_in(publications, publication, gene_as_a_model_of_disease_association).
class_slot(gene_as_a_model_of_disease_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, gene_as_a_model_of_disease_association).
class_slot(gene_as_a_model_of_disease_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, gene_as_a_model_of_disease_association).
class_slot(gene_as_a_model_of_disease_association, frequency_qualifier).
required(frequency_qualifier).
slotrange(frequency_value).
range_in(frequency_qualifier, frequency_value, gene_as_a_model_of_disease_association).
class_slot(gene_as_a_model_of_disease_association, severity_qualifier).
required(severity_qualifier).
slotrange(severity_value).
range_in(severity_qualifier, severity_value, gene_as_a_model_of_disease_association).
class_slot(gene_as_a_model_of_disease_association, onset_qualifier).
required(onset_qualifier).
slotrange(onset).
range_in(onset_qualifier, onset, gene_as_a_model_of_disease_association).
class(gene_family).
mixin(gene_family, gene_grouping).
is_a(gene_family, molecular_entity).
has_uri(gene_family, 'http://w3id.org/biolink/vocab/GeneFamily').
class_slot(gene_family, id).
required(id).
slotrange(identifier_type).
required_in(id, gene_family).
range_in(id, identifier_type, gene_family).
class_slot(gene_family, name).
required(name).
slotrange(label_type).
range_in(name, label_type, gene_family).
class_slot(gene_family, category).
required(category).
slotrange(iri_type).
multivalued_in(category, gene_family).
range_in(category, iri_type, gene_family).
class_slot(gene_family, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, gene_family).
range_in(related_to, named_thing, gene_family).
class_slot(gene_family, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, gene_family).
range_in(interacts_with, named_thing, gene_family).
class_slot(gene_family, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, gene_family).
class_slot(gene_family, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, gene_family).
class_slot(gene_family, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, gene_family).
range_in(synonym, label_type, gene_family).
class_slot(gene_family, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, gene_family).
class_slot(gene_family, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, gene_family).
class_slot(gene_family, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, gene_family).
class_slot(gene_family, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, gene_family).
range_in(has_phenotype, phenotypic_feature, gene_family).
class_slot(gene_family, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, gene_family).
range_in(molecularly_interacts_with, molecular_entity, gene_family).
class_slot(gene_family, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, gene_family).
range_in(affects_abundance_of, molecular_entity, gene_family).
class_slot(gene_family, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, gene_family).
range_in(increases_abundance_of, molecular_entity, gene_family).
class_slot(gene_family, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, gene_family).
range_in(decreases_abundance_of, molecular_entity, gene_family).
class_slot(gene_family, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, gene_family).
range_in(affects_activity_of, molecular_entity, gene_family).
class_slot(gene_family, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, gene_family).
range_in(increases_activity_of, molecular_entity, gene_family).
class_slot(gene_family, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, gene_family).
range_in(decreases_activity_of, molecular_entity, gene_family).
class_slot(gene_family, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, gene_family).
range_in(affects_expression_of, genomic_entity, gene_family).
class_slot(gene_family, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, gene_family).
range_in(increases_expression_of, genomic_entity, gene_family).
class_slot(gene_family, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, gene_family).
range_in(decreases_expression_of, genomic_entity, gene_family).
class_slot(gene_family, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, gene_family).
range_in(affects_folding_of, molecular_entity, gene_family).
class_slot(gene_family, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, gene_family).
range_in(increases_folding_of, molecular_entity, gene_family).
class_slot(gene_family, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, gene_family).
range_in(decreases_folding_of, molecular_entity, gene_family).
class_slot(gene_family, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, gene_family).
range_in(affects_localization_of, molecular_entity, gene_family).
class_slot(gene_family, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, gene_family).
range_in(increases_localization_of, molecular_entity, gene_family).
class_slot(gene_family, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, gene_family).
range_in(decreases_localization_of, molecular_entity, gene_family).
class_slot(gene_family, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, gene_family).
range_in(affects_metabolic_processing_of, molecular_entity, gene_family).
class_slot(gene_family, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, gene_family).
range_in(increases_metabolic_processing_of, molecular_entity, gene_family).
class_slot(gene_family, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, gene_family).
range_in(decreases_metabolic_processing_of, molecular_entity, gene_family).
class_slot(gene_family, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, gene_family).
range_in(affects_molecular_modification_of, molecular_entity, gene_family).
class_slot(gene_family, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, gene_family).
range_in(increases_molecular_modification_of, molecular_entity, gene_family).
class_slot(gene_family, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, gene_family).
range_in(decreases_molecular_modification_of, molecular_entity, gene_family).
class_slot(gene_family, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, gene_family).
range_in(affects_synthesis_of, molecular_entity, gene_family).
class_slot(gene_family, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, gene_family).
range_in(increases_synthesis_of, molecular_entity, gene_family).
class_slot(gene_family, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, gene_family).
range_in(decreases_synthesis_of, molecular_entity, gene_family).
class_slot(gene_family, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, gene_family).
range_in(affects_degradation_of, molecular_entity, gene_family).
class_slot(gene_family, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, gene_family).
range_in(increases_degradation_of, molecular_entity, gene_family).
class_slot(gene_family, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, gene_family).
range_in(decreases_degradation_of, molecular_entity, gene_family).
class_slot(gene_family, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, gene_family).
range_in(affects_mutation_rate_of, genomic_entity, gene_family).
class_slot(gene_family, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, gene_family).
range_in(increases_mutation_rate_of, genomic_entity, gene_family).
class_slot(gene_family, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, gene_family).
range_in(decreases_mutation_rate_of, genomic_entity, gene_family).
class_slot(gene_family, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, gene_family).
range_in(affects_response_to, molecular_entity, gene_family).
class_slot(gene_family, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, gene_family).
range_in(increases_response_to, molecular_entity, gene_family).
class_slot(gene_family, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, gene_family).
range_in(decreases_response_to, molecular_entity, gene_family).
class_slot(gene_family, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, gene_family).
range_in(affects_splicing_of, transcript, gene_family).
class_slot(gene_family, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, gene_family).
range_in(increases_splicing_of, transcript, gene_family).
class_slot(gene_family, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, gene_family).
range_in(decreases_splicing_of, transcript, gene_family).
class_slot(gene_family, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, gene_family).
range_in(affects_stability_of, molecular_entity, gene_family).
class_slot(gene_family, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, gene_family).
range_in(increases_stability_of, molecular_entity, gene_family).
class_slot(gene_family, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, gene_family).
range_in(decreases_stability_of, molecular_entity, gene_family).
class_slot(gene_family, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, gene_family).
range_in(affects_transport_of, molecular_entity, gene_family).
class_slot(gene_family, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, gene_family).
range_in(increases_transport_of, molecular_entity, gene_family).
class_slot(gene_family, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, gene_family).
range_in(decreases_transport_of, molecular_entity, gene_family).
class_slot(gene_family, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, gene_family).
range_in(affects_secretion_of, molecular_entity, gene_family).
class_slot(gene_family, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, gene_family).
range_in(increases_secretion_of, molecular_entity, gene_family).
class_slot(gene_family, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, gene_family).
range_in(decreases_secretion_of, molecular_entity, gene_family).
class_slot(gene_family, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, gene_family).
range_in(affects_uptake_of, molecular_entity, gene_family).
class_slot(gene_family, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, gene_family).
range_in(increases_uptake_of, molecular_entity, gene_family).
class_slot(gene_family, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, gene_family).
range_in(decreases_uptake_of, molecular_entity, gene_family).
class_slot(gene_family, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, gene_family).
range_in(regulates_entity_to_entity, molecular_entity, gene_family).
class_slot(gene_family, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, gene_family).
range_in(biomarker_for, disease_or_phenotypic_feature, gene_family).
class_slot(gene_family, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, gene_family).
range_in(in_taxon, organism_taxon, gene_family).
class(gene_grouping).
has_uri(gene_grouping, 'http://w3id.org/biolink/vocab/GeneGrouping').
class(gene_has_variant_that_contributes_to_disease_association).
is_a(gene_has_variant_that_contributes_to_disease_association, gene_to_disease_association).
defining_slots(gene_to_disease_association, [subject, object, relation]).
has_uri(gene_has_variant_that_contributes_to_disease_association, 'http://w3id.org/biolink/vocab/GeneHasVariantThatContributesToDiseaseAssociation').
class_slot(gene_has_variant_that_contributes_to_disease_association, id).
required(id).
slotrange(identifier_type).
required_in(id, gene_has_variant_that_contributes_to_disease_association).
range_in(id, identifier_type, gene_has_variant_that_contributes_to_disease_association).
class_slot(gene_has_variant_that_contributes_to_disease_association, subject).
required(subject).
slotrange(gene_or_gene_product).
required_in(subject, gene_has_variant_that_contributes_to_disease_association).
range_in(subject, gene_or_gene_product, gene_has_variant_that_contributes_to_disease_association).
class_slot(gene_has_variant_that_contributes_to_disease_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, gene_has_variant_that_contributes_to_disease_association).
range_in(relation, iri_type, gene_has_variant_that_contributes_to_disease_association).
class_slot(gene_has_variant_that_contributes_to_disease_association, object).
required(object).
slotrange(iri_type).
required_in(object, gene_has_variant_that_contributes_to_disease_association).
range_in(object, iri_type, gene_has_variant_that_contributes_to_disease_association).
class_slot(gene_has_variant_that_contributes_to_disease_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, gene_has_variant_that_contributes_to_disease_association).
class_slot(gene_has_variant_that_contributes_to_disease_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, gene_has_variant_that_contributes_to_disease_association).
class_slot(gene_has_variant_that_contributes_to_disease_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, gene_has_variant_that_contributes_to_disease_association).
range_in(qualifiers, ontology_class, gene_has_variant_that_contributes_to_disease_association).
class_slot(gene_has_variant_that_contributes_to_disease_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, gene_has_variant_that_contributes_to_disease_association).
range_in(publications, publication, gene_has_variant_that_contributes_to_disease_association).
class_slot(gene_has_variant_that_contributes_to_disease_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, gene_has_variant_that_contributes_to_disease_association).
class_slot(gene_has_variant_that_contributes_to_disease_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, gene_has_variant_that_contributes_to_disease_association).
class_slot(gene_has_variant_that_contributes_to_disease_association, frequency_qualifier).
required(frequency_qualifier).
slotrange(frequency_value).
range_in(frequency_qualifier, frequency_value, gene_has_variant_that_contributes_to_disease_association).
class_slot(gene_has_variant_that_contributes_to_disease_association, severity_qualifier).
required(severity_qualifier).
slotrange(severity_value).
range_in(severity_qualifier, severity_value, gene_has_variant_that_contributes_to_disease_association).
class_slot(gene_has_variant_that_contributes_to_disease_association, onset_qualifier).
required(onset_qualifier).
slotrange(onset).
range_in(onset_qualifier, onset, gene_has_variant_that_contributes_to_disease_association).
class_slot(gene_has_variant_that_contributes_to_disease_association, sequence_variant_qualifier).
required(sequence_variant_qualifier).
slotrange(sequence_variant).
range_in(sequence_variant_qualifier, sequence_variant, gene_has_variant_that_contributes_to_disease_association).
class(gene_ontology_class).
is_a(gene_ontology_class, ontology_class).
has_uri(gene_ontology_class, 'http://w3id.org/biolink/vocab/GeneOntologyClass').
class_slot(gene_ontology_class, id).
required(id).
slotrange(identifier_type).
required_in(id, gene_ontology_class).
range_in(id, identifier_type, gene_ontology_class).
class_slot(gene_ontology_class, name).
required(name).
slotrange(label_type).
range_in(name, label_type, gene_ontology_class).
class_slot(gene_ontology_class, category).
required(category).
slotrange(iri_type).
multivalued_in(category, gene_ontology_class).
range_in(category, iri_type, gene_ontology_class).
class_slot(gene_ontology_class, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, gene_ontology_class).
range_in(related_to, named_thing, gene_ontology_class).
class_slot(gene_ontology_class, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, gene_ontology_class).
range_in(interacts_with, named_thing, gene_ontology_class).
class_slot(gene_ontology_class, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, gene_ontology_class).
class_slot(gene_ontology_class, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, gene_ontology_class).
class_slot(gene_ontology_class, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, gene_ontology_class).
range_in(synonym, label_type, gene_ontology_class).
class_slot(gene_ontology_class, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, gene_ontology_class).
class_slot(gene_ontology_class, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, gene_ontology_class).
class_slot(gene_ontology_class, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, gene_ontology_class).
class_slot(gene_ontology_class, subclass_of).
required(subclass_of).
slotrange(ontology_class).
multivalued_in(subclass_of, gene_ontology_class).
range_in(subclass_of, ontology_class, gene_ontology_class).
class(gene_or_gene_product).
is_a(gene_or_gene_product, macromolecular_machine).
has_uri(gene_or_gene_product, 'http://w3id.org/biolink/vocab/GeneOrGeneProduct').
class_slot(gene_or_gene_product, id).
required(id).
slotrange(identifier_type).
required_in(id, gene_or_gene_product).
range_in(id, identifier_type, gene_or_gene_product).
class_slot(gene_or_gene_product, name).
required(name).
slotrange(symbol_type).
range_in(name, symbol_type, gene_or_gene_product).
class_slot(gene_or_gene_product, category).
required(category).
slotrange(iri_type).
multivalued_in(category, gene_or_gene_product).
range_in(category, iri_type, gene_or_gene_product).
class_slot(gene_or_gene_product, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, gene_or_gene_product).
range_in(related_to, named_thing, gene_or_gene_product).
class_slot(gene_or_gene_product, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, gene_or_gene_product).
range_in(interacts_with, named_thing, gene_or_gene_product).
class_slot(gene_or_gene_product, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, gene_or_gene_product).
class_slot(gene_or_gene_product, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, gene_or_gene_product).
class_slot(gene_or_gene_product, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, gene_or_gene_product).
range_in(synonym, label_type, gene_or_gene_product).
class_slot(gene_or_gene_product, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, gene_or_gene_product).
class_slot(gene_or_gene_product, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, gene_or_gene_product).
class_slot(gene_or_gene_product, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, gene_or_gene_product).
class_slot(gene_or_gene_product, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, gene_or_gene_product).
range_in(has_phenotype, phenotypic_feature, gene_or_gene_product).
class_slot(gene_or_gene_product, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, gene_or_gene_product).
range_in(molecularly_interacts_with, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, gene_or_gene_product).
range_in(affects_abundance_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, gene_or_gene_product).
range_in(increases_abundance_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, gene_or_gene_product).
range_in(decreases_abundance_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, gene_or_gene_product).
range_in(affects_activity_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, gene_or_gene_product).
range_in(increases_activity_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, gene_or_gene_product).
range_in(decreases_activity_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, gene_or_gene_product).
range_in(affects_expression_of, genomic_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, gene_or_gene_product).
range_in(increases_expression_of, genomic_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, gene_or_gene_product).
range_in(decreases_expression_of, genomic_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, gene_or_gene_product).
range_in(affects_folding_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, gene_or_gene_product).
range_in(increases_folding_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, gene_or_gene_product).
range_in(decreases_folding_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, gene_or_gene_product).
range_in(affects_localization_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, gene_or_gene_product).
range_in(increases_localization_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, gene_or_gene_product).
range_in(decreases_localization_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, gene_or_gene_product).
range_in(affects_metabolic_processing_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, gene_or_gene_product).
range_in(increases_metabolic_processing_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, gene_or_gene_product).
range_in(decreases_metabolic_processing_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, gene_or_gene_product).
range_in(affects_molecular_modification_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, gene_or_gene_product).
range_in(increases_molecular_modification_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, gene_or_gene_product).
range_in(decreases_molecular_modification_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, gene_or_gene_product).
range_in(affects_synthesis_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, gene_or_gene_product).
range_in(increases_synthesis_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, gene_or_gene_product).
range_in(decreases_synthesis_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, gene_or_gene_product).
range_in(affects_degradation_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, gene_or_gene_product).
range_in(increases_degradation_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, gene_or_gene_product).
range_in(decreases_degradation_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, gene_or_gene_product).
range_in(affects_mutation_rate_of, genomic_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, gene_or_gene_product).
range_in(increases_mutation_rate_of, genomic_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, gene_or_gene_product).
range_in(decreases_mutation_rate_of, genomic_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, gene_or_gene_product).
range_in(affects_response_to, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, gene_or_gene_product).
range_in(increases_response_to, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, gene_or_gene_product).
range_in(decreases_response_to, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, gene_or_gene_product).
range_in(affects_splicing_of, transcript, gene_or_gene_product).
class_slot(gene_or_gene_product, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, gene_or_gene_product).
range_in(increases_splicing_of, transcript, gene_or_gene_product).
class_slot(gene_or_gene_product, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, gene_or_gene_product).
range_in(decreases_splicing_of, transcript, gene_or_gene_product).
class_slot(gene_or_gene_product, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, gene_or_gene_product).
range_in(affects_stability_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, gene_or_gene_product).
range_in(increases_stability_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, gene_or_gene_product).
range_in(decreases_stability_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, gene_or_gene_product).
range_in(affects_transport_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, gene_or_gene_product).
range_in(increases_transport_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, gene_or_gene_product).
range_in(decreases_transport_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, gene_or_gene_product).
range_in(affects_secretion_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, gene_or_gene_product).
range_in(increases_secretion_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, gene_or_gene_product).
range_in(decreases_secretion_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, gene_or_gene_product).
range_in(affects_uptake_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, gene_or_gene_product).
range_in(increases_uptake_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, gene_or_gene_product).
range_in(decreases_uptake_of, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, gene_or_gene_product).
range_in(regulates_entity_to_entity, molecular_entity, gene_or_gene_product).
class_slot(gene_or_gene_product, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, gene_or_gene_product).
range_in(biomarker_for, disease_or_phenotypic_feature, gene_or_gene_product).
class_slot(gene_or_gene_product, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, gene_or_gene_product).
range_in(in_taxon, organism_taxon, gene_or_gene_product).
class_slot(gene_or_gene_product, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, gene_or_gene_product).
class_slot(gene_or_gene_product, in_pathway_with).
required(in_pathway_with).
slotrange(gene_or_gene_product).
multivalued_in(in_pathway_with, gene_or_gene_product).
range_in(in_pathway_with, gene_or_gene_product, gene_or_gene_product).
class_slot(gene_or_gene_product, in_complex_with).
required(in_complex_with).
slotrange(gene_or_gene_product).
multivalued_in(in_complex_with, gene_or_gene_product).
range_in(in_complex_with, gene_or_gene_product, gene_or_gene_product).
class_slot(gene_or_gene_product, in_cell_population_with).
required(in_cell_population_with).
slotrange(gene_or_gene_product).
multivalued_in(in_cell_population_with, gene_or_gene_product).
range_in(in_cell_population_with, gene_or_gene_product, gene_or_gene_product).
class_slot(gene_or_gene_product, expressed_in).
required(expressed_in).
slotrange(anatomical_entity).
multivalued_in(expressed_in, gene_or_gene_product).
range_in(expressed_in, anatomical_entity, gene_or_gene_product).
class(gene_product).
is_a(gene_product, gene_or_gene_product).
has_uri(gene_product, 'http://w3id.org/biolink/vocab/GeneProduct').
class_slot(gene_product, id).
required(id).
slotrange(identifier_type).
required_in(id, gene_product).
range_in(id, identifier_type, gene_product).
class_slot(gene_product, name).
required(name).
slotrange(symbol_type).
range_in(name, symbol_type, gene_product).
class_slot(gene_product, category).
required(category).
slotrange(iri_type).
multivalued_in(category, gene_product).
range_in(category, iri_type, gene_product).
class_slot(gene_product, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, gene_product).
range_in(related_to, named_thing, gene_product).
class_slot(gene_product, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, gene_product).
range_in(interacts_with, named_thing, gene_product).
class_slot(gene_product, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, gene_product).
class_slot(gene_product, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, gene_product).
class_slot(gene_product, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, gene_product).
range_in(synonym, label_type, gene_product).
class_slot(gene_product, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, gene_product).
class_slot(gene_product, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, gene_product).
class_slot(gene_product, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, gene_product).
class_slot(gene_product, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, gene_product).
range_in(has_phenotype, phenotypic_feature, gene_product).
class_slot(gene_product, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, gene_product).
range_in(molecularly_interacts_with, molecular_entity, gene_product).
class_slot(gene_product, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, gene_product).
range_in(affects_abundance_of, molecular_entity, gene_product).
class_slot(gene_product, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, gene_product).
range_in(increases_abundance_of, molecular_entity, gene_product).
class_slot(gene_product, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, gene_product).
range_in(decreases_abundance_of, molecular_entity, gene_product).
class_slot(gene_product, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, gene_product).
range_in(affects_activity_of, molecular_entity, gene_product).
class_slot(gene_product, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, gene_product).
range_in(increases_activity_of, molecular_entity, gene_product).
class_slot(gene_product, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, gene_product).
range_in(decreases_activity_of, molecular_entity, gene_product).
class_slot(gene_product, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, gene_product).
range_in(affects_expression_of, genomic_entity, gene_product).
class_slot(gene_product, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, gene_product).
range_in(increases_expression_of, genomic_entity, gene_product).
class_slot(gene_product, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, gene_product).
range_in(decreases_expression_of, genomic_entity, gene_product).
class_slot(gene_product, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, gene_product).
range_in(affects_folding_of, molecular_entity, gene_product).
class_slot(gene_product, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, gene_product).
range_in(increases_folding_of, molecular_entity, gene_product).
class_slot(gene_product, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, gene_product).
range_in(decreases_folding_of, molecular_entity, gene_product).
class_slot(gene_product, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, gene_product).
range_in(affects_localization_of, molecular_entity, gene_product).
class_slot(gene_product, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, gene_product).
range_in(increases_localization_of, molecular_entity, gene_product).
class_slot(gene_product, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, gene_product).
range_in(decreases_localization_of, molecular_entity, gene_product).
class_slot(gene_product, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, gene_product).
range_in(affects_metabolic_processing_of, molecular_entity, gene_product).
class_slot(gene_product, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, gene_product).
range_in(increases_metabolic_processing_of, molecular_entity, gene_product).
class_slot(gene_product, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, gene_product).
range_in(decreases_metabolic_processing_of, molecular_entity, gene_product).
class_slot(gene_product, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, gene_product).
range_in(affects_molecular_modification_of, molecular_entity, gene_product).
class_slot(gene_product, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, gene_product).
range_in(increases_molecular_modification_of, molecular_entity, gene_product).
class_slot(gene_product, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, gene_product).
range_in(decreases_molecular_modification_of, molecular_entity, gene_product).
class_slot(gene_product, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, gene_product).
range_in(affects_synthesis_of, molecular_entity, gene_product).
class_slot(gene_product, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, gene_product).
range_in(increases_synthesis_of, molecular_entity, gene_product).
class_slot(gene_product, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, gene_product).
range_in(decreases_synthesis_of, molecular_entity, gene_product).
class_slot(gene_product, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, gene_product).
range_in(affects_degradation_of, molecular_entity, gene_product).
class_slot(gene_product, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, gene_product).
range_in(increases_degradation_of, molecular_entity, gene_product).
class_slot(gene_product, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, gene_product).
range_in(decreases_degradation_of, molecular_entity, gene_product).
class_slot(gene_product, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, gene_product).
range_in(affects_mutation_rate_of, genomic_entity, gene_product).
class_slot(gene_product, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, gene_product).
range_in(increases_mutation_rate_of, genomic_entity, gene_product).
class_slot(gene_product, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, gene_product).
range_in(decreases_mutation_rate_of, genomic_entity, gene_product).
class_slot(gene_product, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, gene_product).
range_in(affects_response_to, molecular_entity, gene_product).
class_slot(gene_product, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, gene_product).
range_in(increases_response_to, molecular_entity, gene_product).
class_slot(gene_product, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, gene_product).
range_in(decreases_response_to, molecular_entity, gene_product).
class_slot(gene_product, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, gene_product).
range_in(affects_splicing_of, transcript, gene_product).
class_slot(gene_product, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, gene_product).
range_in(increases_splicing_of, transcript, gene_product).
class_slot(gene_product, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, gene_product).
range_in(decreases_splicing_of, transcript, gene_product).
class_slot(gene_product, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, gene_product).
range_in(affects_stability_of, molecular_entity, gene_product).
class_slot(gene_product, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, gene_product).
range_in(increases_stability_of, molecular_entity, gene_product).
class_slot(gene_product, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, gene_product).
range_in(decreases_stability_of, molecular_entity, gene_product).
class_slot(gene_product, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, gene_product).
range_in(affects_transport_of, molecular_entity, gene_product).
class_slot(gene_product, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, gene_product).
range_in(increases_transport_of, molecular_entity, gene_product).
class_slot(gene_product, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, gene_product).
range_in(decreases_transport_of, molecular_entity, gene_product).
class_slot(gene_product, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, gene_product).
range_in(affects_secretion_of, molecular_entity, gene_product).
class_slot(gene_product, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, gene_product).
range_in(increases_secretion_of, molecular_entity, gene_product).
class_slot(gene_product, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, gene_product).
range_in(decreases_secretion_of, molecular_entity, gene_product).
class_slot(gene_product, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, gene_product).
range_in(affects_uptake_of, molecular_entity, gene_product).
class_slot(gene_product, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, gene_product).
range_in(increases_uptake_of, molecular_entity, gene_product).
class_slot(gene_product, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, gene_product).
range_in(decreases_uptake_of, molecular_entity, gene_product).
class_slot(gene_product, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, gene_product).
range_in(regulates_entity_to_entity, molecular_entity, gene_product).
class_slot(gene_product, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, gene_product).
range_in(biomarker_for, disease_or_phenotypic_feature, gene_product).
class_slot(gene_product, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, gene_product).
range_in(in_taxon, organism_taxon, gene_product).
class_slot(gene_product, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, gene_product).
class_slot(gene_product, in_pathway_with).
required(in_pathway_with).
slotrange(gene_or_gene_product).
multivalued_in(in_pathway_with, gene_product).
range_in(in_pathway_with, gene_or_gene_product, gene_product).
class_slot(gene_product, in_complex_with).
required(in_complex_with).
slotrange(gene_or_gene_product).
multivalued_in(in_complex_with, gene_product).
range_in(in_complex_with, gene_or_gene_product, gene_product).
class_slot(gene_product, in_cell_population_with).
required(in_cell_population_with).
slotrange(gene_or_gene_product).
multivalued_in(in_cell_population_with, gene_product).
range_in(in_cell_population_with, gene_or_gene_product, gene_product).
class_slot(gene_product, expressed_in).
required(expressed_in).
slotrange(anatomical_entity).
multivalued_in(expressed_in, gene_product).
range_in(expressed_in, anatomical_entity, gene_product).
class(gene_product_isoform).
is_a(gene_product_isoform, gene_product).
has_uri(gene_product_isoform, 'http://w3id.org/biolink/vocab/GeneProductIsoform').
class_slot(gene_product_isoform, id).
required(id).
slotrange(identifier_type).
required_in(id, gene_product_isoform).
range_in(id, identifier_type, gene_product_isoform).
class_slot(gene_product_isoform, name).
required(name).
slotrange(symbol_type).
range_in(name, symbol_type, gene_product_isoform).
class_slot(gene_product_isoform, category).
required(category).
slotrange(iri_type).
multivalued_in(category, gene_product_isoform).
range_in(category, iri_type, gene_product_isoform).
class_slot(gene_product_isoform, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, gene_product_isoform).
range_in(related_to, named_thing, gene_product_isoform).
class_slot(gene_product_isoform, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, gene_product_isoform).
range_in(interacts_with, named_thing, gene_product_isoform).
class_slot(gene_product_isoform, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, gene_product_isoform).
class_slot(gene_product_isoform, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, gene_product_isoform).
class_slot(gene_product_isoform, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, gene_product_isoform).
range_in(synonym, label_type, gene_product_isoform).
class_slot(gene_product_isoform, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, gene_product_isoform).
class_slot(gene_product_isoform, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, gene_product_isoform).
class_slot(gene_product_isoform, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, gene_product_isoform).
class_slot(gene_product_isoform, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, gene_product_isoform).
range_in(has_phenotype, phenotypic_feature, gene_product_isoform).
class_slot(gene_product_isoform, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, gene_product_isoform).
range_in(molecularly_interacts_with, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, gene_product_isoform).
range_in(affects_abundance_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, gene_product_isoform).
range_in(increases_abundance_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, gene_product_isoform).
range_in(decreases_abundance_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, gene_product_isoform).
range_in(affects_activity_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, gene_product_isoform).
range_in(increases_activity_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, gene_product_isoform).
range_in(decreases_activity_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, gene_product_isoform).
range_in(affects_expression_of, genomic_entity, gene_product_isoform).
class_slot(gene_product_isoform, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, gene_product_isoform).
range_in(increases_expression_of, genomic_entity, gene_product_isoform).
class_slot(gene_product_isoform, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, gene_product_isoform).
range_in(decreases_expression_of, genomic_entity, gene_product_isoform).
class_slot(gene_product_isoform, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, gene_product_isoform).
range_in(affects_folding_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, gene_product_isoform).
range_in(increases_folding_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, gene_product_isoform).
range_in(decreases_folding_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, gene_product_isoform).
range_in(affects_localization_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, gene_product_isoform).
range_in(increases_localization_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, gene_product_isoform).
range_in(decreases_localization_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, gene_product_isoform).
range_in(affects_metabolic_processing_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, gene_product_isoform).
range_in(increases_metabolic_processing_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, gene_product_isoform).
range_in(decreases_metabolic_processing_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, gene_product_isoform).
range_in(affects_molecular_modification_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, gene_product_isoform).
range_in(increases_molecular_modification_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, gene_product_isoform).
range_in(decreases_molecular_modification_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, gene_product_isoform).
range_in(affects_synthesis_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, gene_product_isoform).
range_in(increases_synthesis_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, gene_product_isoform).
range_in(decreases_synthesis_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, gene_product_isoform).
range_in(affects_degradation_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, gene_product_isoform).
range_in(increases_degradation_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, gene_product_isoform).
range_in(decreases_degradation_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, gene_product_isoform).
range_in(affects_mutation_rate_of, genomic_entity, gene_product_isoform).
class_slot(gene_product_isoform, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, gene_product_isoform).
range_in(increases_mutation_rate_of, genomic_entity, gene_product_isoform).
class_slot(gene_product_isoform, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, gene_product_isoform).
range_in(decreases_mutation_rate_of, genomic_entity, gene_product_isoform).
class_slot(gene_product_isoform, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, gene_product_isoform).
range_in(affects_response_to, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, gene_product_isoform).
range_in(increases_response_to, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, gene_product_isoform).
range_in(decreases_response_to, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, gene_product_isoform).
range_in(affects_splicing_of, transcript, gene_product_isoform).
class_slot(gene_product_isoform, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, gene_product_isoform).
range_in(increases_splicing_of, transcript, gene_product_isoform).
class_slot(gene_product_isoform, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, gene_product_isoform).
range_in(decreases_splicing_of, transcript, gene_product_isoform).
class_slot(gene_product_isoform, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, gene_product_isoform).
range_in(affects_stability_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, gene_product_isoform).
range_in(increases_stability_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, gene_product_isoform).
range_in(decreases_stability_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, gene_product_isoform).
range_in(affects_transport_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, gene_product_isoform).
range_in(increases_transport_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, gene_product_isoform).
range_in(decreases_transport_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, gene_product_isoform).
range_in(affects_secretion_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, gene_product_isoform).
range_in(increases_secretion_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, gene_product_isoform).
range_in(decreases_secretion_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, gene_product_isoform).
range_in(affects_uptake_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, gene_product_isoform).
range_in(increases_uptake_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, gene_product_isoform).
range_in(decreases_uptake_of, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, gene_product_isoform).
range_in(regulates_entity_to_entity, molecular_entity, gene_product_isoform).
class_slot(gene_product_isoform, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, gene_product_isoform).
range_in(biomarker_for, disease_or_phenotypic_feature, gene_product_isoform).
class_slot(gene_product_isoform, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, gene_product_isoform).
range_in(in_taxon, organism_taxon, gene_product_isoform).
class_slot(gene_product_isoform, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, gene_product_isoform).
class_slot(gene_product_isoform, in_pathway_with).
required(in_pathway_with).
slotrange(gene_or_gene_product).
multivalued_in(in_pathway_with, gene_product_isoform).
range_in(in_pathway_with, gene_or_gene_product, gene_product_isoform).
class_slot(gene_product_isoform, in_complex_with).
required(in_complex_with).
slotrange(gene_or_gene_product).
multivalued_in(in_complex_with, gene_product_isoform).
range_in(in_complex_with, gene_or_gene_product, gene_product_isoform).
class_slot(gene_product_isoform, in_cell_population_with).
required(in_cell_population_with).
slotrange(gene_or_gene_product).
multivalued_in(in_cell_population_with, gene_product_isoform).
range_in(in_cell_population_with, gene_or_gene_product, gene_product_isoform).
class_slot(gene_product_isoform, expressed_in).
required(expressed_in).
slotrange(anatomical_entity).
multivalued_in(expressed_in, gene_product_isoform).
range_in(expressed_in, anatomical_entity, gene_product_isoform).
class(gene_regulatory_relationship).
is_a(gene_regulatory_relationship, association).
has_uri(gene_regulatory_relationship, 'http://w3id.org/biolink/vocab/GeneRegulatoryRelationship').
class_slot(gene_regulatory_relationship, id).
required(id).
slotrange(identifier_type).
required_in(id, gene_regulatory_relationship).
range_in(id, identifier_type, gene_regulatory_relationship).
class_slot(gene_regulatory_relationship, subject).
required(subject).
slotrange(gene_or_gene_product).
required_in(subject, gene_regulatory_relationship).
range_in(subject, gene_or_gene_product, gene_regulatory_relationship).
class_slot(gene_regulatory_relationship, relation).
required(relation).
slotrange(iri_type).
required_in(relation, gene_regulatory_relationship).
range_in(relation, iri_type, gene_regulatory_relationship).
class_slot(gene_regulatory_relationship, object).
required(object).
slotrange(gene_or_gene_product).
required_in(object, gene_regulatory_relationship).
range_in(object, gene_or_gene_product, gene_regulatory_relationship).
class_slot(gene_regulatory_relationship, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, gene_regulatory_relationship).
class_slot(gene_regulatory_relationship, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, gene_regulatory_relationship).
class_slot(gene_regulatory_relationship, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, gene_regulatory_relationship).
range_in(qualifiers, ontology_class, gene_regulatory_relationship).
class_slot(gene_regulatory_relationship, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, gene_regulatory_relationship).
range_in(publications, publication, gene_regulatory_relationship).
class_slot(gene_regulatory_relationship, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, gene_regulatory_relationship).
class_slot(gene_regulatory_relationship, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, gene_regulatory_relationship).
class(gene_to_disease_association).
mixin(gene_to_disease_association, entity_to_disease_association).
mixin(gene_to_disease_association, gene_to_thing_association).
is_a(gene_to_disease_association, association).
defining_slots(association, [subject, object]).
has_uri(gene_to_disease_association, 'http://w3id.org/biolink/vocab/GeneToDiseaseAssociation').
class_slot(gene_to_disease_association, id).
required(id).
slotrange(identifier_type).
required_in(id, gene_to_disease_association).
range_in(id, identifier_type, gene_to_disease_association).
class_slot(gene_to_disease_association, subject).
required(subject).
slotrange(gene_or_gene_product).
required_in(subject, gene_to_disease_association).
range_in(subject, gene_or_gene_product, gene_to_disease_association).
class_slot(gene_to_disease_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, gene_to_disease_association).
range_in(relation, iri_type, gene_to_disease_association).
class_slot(gene_to_disease_association, object).
required(object).
slotrange(iri_type).
required_in(object, gene_to_disease_association).
range_in(object, iri_type, gene_to_disease_association).
class_slot(gene_to_disease_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, gene_to_disease_association).
class_slot(gene_to_disease_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, gene_to_disease_association).
class_slot(gene_to_disease_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, gene_to_disease_association).
range_in(qualifiers, ontology_class, gene_to_disease_association).
class_slot(gene_to_disease_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, gene_to_disease_association).
range_in(publications, publication, gene_to_disease_association).
class_slot(gene_to_disease_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, gene_to_disease_association).
class_slot(gene_to_disease_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, gene_to_disease_association).
class_slot(gene_to_disease_association, frequency_qualifier).
required(frequency_qualifier).
slotrange(frequency_value).
range_in(frequency_qualifier, frequency_value, gene_to_disease_association).
class_slot(gene_to_disease_association, severity_qualifier).
required(severity_qualifier).
slotrange(severity_value).
range_in(severity_qualifier, severity_value, gene_to_disease_association).
class_slot(gene_to_disease_association, onset_qualifier).
required(onset_qualifier).
slotrange(onset).
range_in(onset_qualifier, onset, gene_to_disease_association).
class(gene_to_expression_site_association).
is_a(gene_to_expression_site_association, association).
defining_slots(association, [subject, object, relation]).
has_uri(gene_to_expression_site_association, 'http://w3id.org/biolink/vocab/GeneToExpressionSiteAssociation').
class_slot(gene_to_expression_site_association, id).
required(id).
slotrange(identifier_type).
required_in(id, gene_to_expression_site_association).
range_in(id, identifier_type, gene_to_expression_site_association).
class_slot(gene_to_expression_site_association, subject).
required(subject).
slotrange(gene_or_gene_product).
required_in(subject, gene_to_expression_site_association).
range_in(subject, gene_or_gene_product, gene_to_expression_site_association).
class_slot(gene_to_expression_site_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, gene_to_expression_site_association).
range_in(relation, iri_type, gene_to_expression_site_association).
class_slot(gene_to_expression_site_association, object).
required(object).
slotrange(anatomical_entity).
required_in(object, gene_to_expression_site_association).
range_in(object, anatomical_entity, gene_to_expression_site_association).
class_slot(gene_to_expression_site_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, gene_to_expression_site_association).
class_slot(gene_to_expression_site_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, gene_to_expression_site_association).
class_slot(gene_to_expression_site_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, gene_to_expression_site_association).
range_in(qualifiers, ontology_class, gene_to_expression_site_association).
class_slot(gene_to_expression_site_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, gene_to_expression_site_association).
range_in(publications, publication, gene_to_expression_site_association).
class_slot(gene_to_expression_site_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, gene_to_expression_site_association).
class_slot(gene_to_expression_site_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, gene_to_expression_site_association).
class_slot(gene_to_expression_site_association, stage_qualifier).
required(stage_qualifier).
slotrange(life_stage).
range_in(stage_qualifier, life_stage, gene_to_expression_site_association).
class_slot(gene_to_expression_site_association, quantifier_qualifier).
required(quantifier_qualifier).
slotrange(ontology_class).
range_in(quantifier_qualifier, ontology_class, gene_to_expression_site_association).
class(gene_to_gene_association).
is_a(gene_to_gene_association, association).
defining_slots(association, [subject, object]).
has_uri(gene_to_gene_association, 'http://w3id.org/biolink/vocab/GeneToGeneAssociation').
class_slot(gene_to_gene_association, id).
required(id).
slotrange(identifier_type).
required_in(id, gene_to_gene_association).
range_in(id, identifier_type, gene_to_gene_association).
class_slot(gene_to_gene_association, subject).
required(subject).
slotrange(gene_or_gene_product).
required_in(subject, gene_to_gene_association).
range_in(subject, gene_or_gene_product, gene_to_gene_association).
class_slot(gene_to_gene_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, gene_to_gene_association).
range_in(relation, iri_type, gene_to_gene_association).
class_slot(gene_to_gene_association, object).
required(object).
slotrange(gene_or_gene_product).
required_in(object, gene_to_gene_association).
range_in(object, gene_or_gene_product, gene_to_gene_association).
class_slot(gene_to_gene_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, gene_to_gene_association).
class_slot(gene_to_gene_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, gene_to_gene_association).
class_slot(gene_to_gene_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, gene_to_gene_association).
range_in(qualifiers, ontology_class, gene_to_gene_association).
class_slot(gene_to_gene_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, gene_to_gene_association).
range_in(publications, publication, gene_to_gene_association).
class_slot(gene_to_gene_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, gene_to_gene_association).
class_slot(gene_to_gene_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, gene_to_gene_association).
class(gene_to_gene_homology_association).
is_a(gene_to_gene_homology_association, gene_to_gene_association).
defining_slots(gene_to_gene_association, [subject, object, relation]).
has_uri(gene_to_gene_homology_association, 'http://w3id.org/biolink/vocab/GeneToGeneHomologyAssociation').
class_slot(gene_to_gene_homology_association, id).
required(id).
slotrange(identifier_type).
required_in(id, gene_to_gene_homology_association).
range_in(id, identifier_type, gene_to_gene_homology_association).
class_slot(gene_to_gene_homology_association, subject).
required(subject).
slotrange(gene_or_gene_product).
required_in(subject, gene_to_gene_homology_association).
range_in(subject, gene_or_gene_product, gene_to_gene_homology_association).
class_slot(gene_to_gene_homology_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, gene_to_gene_homology_association).
range_in(relation, iri_type, gene_to_gene_homology_association).
class_slot(gene_to_gene_homology_association, object).
required(object).
slotrange(gene_or_gene_product).
required_in(object, gene_to_gene_homology_association).
range_in(object, gene_or_gene_product, gene_to_gene_homology_association).
class_slot(gene_to_gene_homology_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, gene_to_gene_homology_association).
class_slot(gene_to_gene_homology_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, gene_to_gene_homology_association).
class_slot(gene_to_gene_homology_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, gene_to_gene_homology_association).
range_in(qualifiers, ontology_class, gene_to_gene_homology_association).
class_slot(gene_to_gene_homology_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, gene_to_gene_homology_association).
range_in(publications, publication, gene_to_gene_homology_association).
class_slot(gene_to_gene_homology_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, gene_to_gene_homology_association).
class_slot(gene_to_gene_homology_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, gene_to_gene_homology_association).
class(gene_to_gene_product_relationship).
is_a(gene_to_gene_product_relationship, sequence_feature_relationship).
defining_slots(sequence_feature_relationship, [subject, object]).
has_uri(gene_to_gene_product_relationship, 'http://w3id.org/biolink/vocab/GeneToGeneProductRelationship').
class_slot(gene_to_gene_product_relationship, id).
required(id).
slotrange(identifier_type).
required_in(id, gene_to_gene_product_relationship).
range_in(id, identifier_type, gene_to_gene_product_relationship).
class_slot(gene_to_gene_product_relationship, subject).
required(subject).
slotrange(gene).
required_in(subject, gene_to_gene_product_relationship).
range_in(subject, gene, gene_to_gene_product_relationship).
class_slot(gene_to_gene_product_relationship, relation).
required(relation).
slotrange(iri_type).
required_in(relation, gene_to_gene_product_relationship).
range_in(relation, iri_type, gene_to_gene_product_relationship).
class_slot(gene_to_gene_product_relationship, object).
required(object).
slotrange(gene_product).
required_in(object, gene_to_gene_product_relationship).
range_in(object, gene_product, gene_to_gene_product_relationship).
class_slot(gene_to_gene_product_relationship, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, gene_to_gene_product_relationship).
class_slot(gene_to_gene_product_relationship, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, gene_to_gene_product_relationship).
class_slot(gene_to_gene_product_relationship, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, gene_to_gene_product_relationship).
range_in(qualifiers, ontology_class, gene_to_gene_product_relationship).
class_slot(gene_to_gene_product_relationship, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, gene_to_gene_product_relationship).
range_in(publications, publication, gene_to_gene_product_relationship).
class_slot(gene_to_gene_product_relationship, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, gene_to_gene_product_relationship).
class_slot(gene_to_gene_product_relationship, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, gene_to_gene_product_relationship).
class(gene_to_go_term_association).
is_a(gene_to_go_term_association, functional_association).
defining_slots(functional_association, [subject, object]).
has_uri(gene_to_go_term_association, 'http://w3id.org/biolink/vocab/GeneToGoTermAssociation').
class_slot(gene_to_go_term_association, id).
required(id).
slotrange(identifier_type).
required_in(id, gene_to_go_term_association).
range_in(id, identifier_type, gene_to_go_term_association).
class_slot(gene_to_go_term_association, subject).
required(subject).
slotrange(molecular_entity).
required_in(subject, gene_to_go_term_association).
range_in(subject, molecular_entity, gene_to_go_term_association).
class_slot(gene_to_go_term_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, gene_to_go_term_association).
range_in(relation, iri_type, gene_to_go_term_association).
class_slot(gene_to_go_term_association, object).
required(object).
slotrange(gene_ontology_class).
required_in(object, gene_to_go_term_association).
range_in(object, gene_ontology_class, gene_to_go_term_association).
class_slot(gene_to_go_term_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, gene_to_go_term_association).
class_slot(gene_to_go_term_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, gene_to_go_term_association).
class_slot(gene_to_go_term_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, gene_to_go_term_association).
range_in(qualifiers, ontology_class, gene_to_go_term_association).
class_slot(gene_to_go_term_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, gene_to_go_term_association).
range_in(publications, publication, gene_to_go_term_association).
class_slot(gene_to_go_term_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, gene_to_go_term_association).
class_slot(gene_to_go_term_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, gene_to_go_term_association).
class(gene_to_phenotypic_feature_association).
mixin(gene_to_phenotypic_feature_association, entity_to_phenotypic_feature_association).
mixin(gene_to_phenotypic_feature_association, gene_to_thing_association).
is_a(gene_to_phenotypic_feature_association, association).
defining_slots(association, [subject, object]).
has_uri(gene_to_phenotypic_feature_association, 'http://w3id.org/biolink/vocab/GeneToPhenotypicFeatureAssociation').
class_slot(gene_to_phenotypic_feature_association, id).
required(id).
slotrange(identifier_type).
required_in(id, gene_to_phenotypic_feature_association).
range_in(id, identifier_type, gene_to_phenotypic_feature_association).
class_slot(gene_to_phenotypic_feature_association, subject).
required(subject).
slotrange(gene_or_gene_product).
required_in(subject, gene_to_phenotypic_feature_association).
range_in(subject, gene_or_gene_product, gene_to_phenotypic_feature_association).
class_slot(gene_to_phenotypic_feature_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, gene_to_phenotypic_feature_association).
range_in(relation, iri_type, gene_to_phenotypic_feature_association).
class_slot(gene_to_phenotypic_feature_association, object).
required(object).
slotrange(iri_type).
required_in(object, gene_to_phenotypic_feature_association).
range_in(object, iri_type, gene_to_phenotypic_feature_association).
class_slot(gene_to_phenotypic_feature_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, gene_to_phenotypic_feature_association).
class_slot(gene_to_phenotypic_feature_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, gene_to_phenotypic_feature_association).
class_slot(gene_to_phenotypic_feature_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, gene_to_phenotypic_feature_association).
range_in(qualifiers, ontology_class, gene_to_phenotypic_feature_association).
class_slot(gene_to_phenotypic_feature_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, gene_to_phenotypic_feature_association).
range_in(publications, publication, gene_to_phenotypic_feature_association).
class_slot(gene_to_phenotypic_feature_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, gene_to_phenotypic_feature_association).
class_slot(gene_to_phenotypic_feature_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, gene_to_phenotypic_feature_association).
class_slot(gene_to_phenotypic_feature_association, sex_qualifier).
required(sex_qualifier).
slotrange(biological_sex).
range_in(sex_qualifier, biological_sex, gene_to_phenotypic_feature_association).
class_slot(gene_to_phenotypic_feature_association, frequency_qualifier).
required(frequency_qualifier).
slotrange(frequency_value).
range_in(frequency_qualifier, frequency_value, gene_to_phenotypic_feature_association).
class_slot(gene_to_phenotypic_feature_association, severity_qualifier).
required(severity_qualifier).
slotrange(severity_value).
range_in(severity_qualifier, severity_value, gene_to_phenotypic_feature_association).
class_slot(gene_to_phenotypic_feature_association, onset_qualifier).
required(onset_qualifier).
slotrange(onset).
range_in(onset_qualifier, onset, gene_to_phenotypic_feature_association).
class(gene_to_thing_association).
is_a(gene_to_thing_association, association).
defining_slots(association, [subject]).
has_uri(gene_to_thing_association, 'http://w3id.org/biolink/vocab/GeneToThingAssociation').
class_slot(gene_to_thing_association, id).
required(id).
slotrange(identifier_type).
required_in(id, gene_to_thing_association).
range_in(id, identifier_type, gene_to_thing_association).
class_slot(gene_to_thing_association, subject).
required(subject).
slotrange(gene_or_gene_product).
required_in(subject, gene_to_thing_association).
range_in(subject, gene_or_gene_product, gene_to_thing_association).
class_slot(gene_to_thing_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, gene_to_thing_association).
range_in(relation, iri_type, gene_to_thing_association).
class_slot(gene_to_thing_association, object).
required(object).
slotrange(iri_type).
required_in(object, gene_to_thing_association).
range_in(object, iri_type, gene_to_thing_association).
class_slot(gene_to_thing_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, gene_to_thing_association).
class_slot(gene_to_thing_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, gene_to_thing_association).
class_slot(gene_to_thing_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, gene_to_thing_association).
range_in(qualifiers, ontology_class, gene_to_thing_association).
class_slot(gene_to_thing_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, gene_to_thing_association).
range_in(publications, publication, gene_to_thing_association).
class_slot(gene_to_thing_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, gene_to_thing_association).
class_slot(gene_to_thing_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, gene_to_thing_association).
class(genome).
is_a(genome, genomic_entity).
has_uri(genome, 'http://w3id.org/biolink/vocab/Genome').
class_slot(genome, id).
required(id).
slotrange(identifier_type).
required_in(id, genome).
range_in(id, identifier_type, genome).
class_slot(genome, name).
required(name).
slotrange(label_type).
range_in(name, label_type, genome).
class_slot(genome, category).
required(category).
slotrange(iri_type).
multivalued_in(category, genome).
range_in(category, iri_type, genome).
class_slot(genome, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, genome).
range_in(related_to, named_thing, genome).
class_slot(genome, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, genome).
range_in(interacts_with, named_thing, genome).
class_slot(genome, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, genome).
class_slot(genome, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, genome).
class_slot(genome, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, genome).
range_in(synonym, label_type, genome).
class_slot(genome, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, genome).
class_slot(genome, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, genome).
class_slot(genome, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, genome).
class_slot(genome, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, genome).
range_in(has_phenotype, phenotypic_feature, genome).
class_slot(genome, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, genome).
range_in(molecularly_interacts_with, molecular_entity, genome).
class_slot(genome, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, genome).
range_in(affects_abundance_of, molecular_entity, genome).
class_slot(genome, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, genome).
range_in(increases_abundance_of, molecular_entity, genome).
class_slot(genome, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, genome).
range_in(decreases_abundance_of, molecular_entity, genome).
class_slot(genome, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, genome).
range_in(affects_activity_of, molecular_entity, genome).
class_slot(genome, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, genome).
range_in(increases_activity_of, molecular_entity, genome).
class_slot(genome, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, genome).
range_in(decreases_activity_of, molecular_entity, genome).
class_slot(genome, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, genome).
range_in(affects_expression_of, genomic_entity, genome).
class_slot(genome, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, genome).
range_in(increases_expression_of, genomic_entity, genome).
class_slot(genome, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, genome).
range_in(decreases_expression_of, genomic_entity, genome).
class_slot(genome, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, genome).
range_in(affects_folding_of, molecular_entity, genome).
class_slot(genome, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, genome).
range_in(increases_folding_of, molecular_entity, genome).
class_slot(genome, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, genome).
range_in(decreases_folding_of, molecular_entity, genome).
class_slot(genome, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, genome).
range_in(affects_localization_of, molecular_entity, genome).
class_slot(genome, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, genome).
range_in(increases_localization_of, molecular_entity, genome).
class_slot(genome, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, genome).
range_in(decreases_localization_of, molecular_entity, genome).
class_slot(genome, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, genome).
range_in(affects_metabolic_processing_of, molecular_entity, genome).
class_slot(genome, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, genome).
range_in(increases_metabolic_processing_of, molecular_entity, genome).
class_slot(genome, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, genome).
range_in(decreases_metabolic_processing_of, molecular_entity, genome).
class_slot(genome, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, genome).
range_in(affects_molecular_modification_of, molecular_entity, genome).
class_slot(genome, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, genome).
range_in(increases_molecular_modification_of, molecular_entity, genome).
class_slot(genome, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, genome).
range_in(decreases_molecular_modification_of, molecular_entity, genome).
class_slot(genome, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, genome).
range_in(affects_synthesis_of, molecular_entity, genome).
class_slot(genome, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, genome).
range_in(increases_synthesis_of, molecular_entity, genome).
class_slot(genome, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, genome).
range_in(decreases_synthesis_of, molecular_entity, genome).
class_slot(genome, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, genome).
range_in(affects_degradation_of, molecular_entity, genome).
class_slot(genome, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, genome).
range_in(increases_degradation_of, molecular_entity, genome).
class_slot(genome, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, genome).
range_in(decreases_degradation_of, molecular_entity, genome).
class_slot(genome, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, genome).
range_in(affects_mutation_rate_of, genomic_entity, genome).
class_slot(genome, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, genome).
range_in(increases_mutation_rate_of, genomic_entity, genome).
class_slot(genome, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, genome).
range_in(decreases_mutation_rate_of, genomic_entity, genome).
class_slot(genome, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, genome).
range_in(affects_response_to, molecular_entity, genome).
class_slot(genome, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, genome).
range_in(increases_response_to, molecular_entity, genome).
class_slot(genome, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, genome).
range_in(decreases_response_to, molecular_entity, genome).
class_slot(genome, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, genome).
range_in(affects_splicing_of, transcript, genome).
class_slot(genome, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, genome).
range_in(increases_splicing_of, transcript, genome).
class_slot(genome, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, genome).
range_in(decreases_splicing_of, transcript, genome).
class_slot(genome, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, genome).
range_in(affects_stability_of, molecular_entity, genome).
class_slot(genome, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, genome).
range_in(increases_stability_of, molecular_entity, genome).
class_slot(genome, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, genome).
range_in(decreases_stability_of, molecular_entity, genome).
class_slot(genome, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, genome).
range_in(affects_transport_of, molecular_entity, genome).
class_slot(genome, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, genome).
range_in(increases_transport_of, molecular_entity, genome).
class_slot(genome, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, genome).
range_in(decreases_transport_of, molecular_entity, genome).
class_slot(genome, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, genome).
range_in(affects_secretion_of, molecular_entity, genome).
class_slot(genome, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, genome).
range_in(increases_secretion_of, molecular_entity, genome).
class_slot(genome, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, genome).
range_in(decreases_secretion_of, molecular_entity, genome).
class_slot(genome, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, genome).
range_in(affects_uptake_of, molecular_entity, genome).
class_slot(genome, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, genome).
range_in(increases_uptake_of, molecular_entity, genome).
class_slot(genome, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, genome).
range_in(decreases_uptake_of, molecular_entity, genome).
class_slot(genome, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, genome).
range_in(regulates_entity_to_entity, molecular_entity, genome).
class_slot(genome, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, genome).
range_in(biomarker_for, disease_or_phenotypic_feature, genome).
class_slot(genome, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, genome).
range_in(in_taxon, organism_taxon, genome).
class_slot(genome, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, genome).
class(genomic_entity).
is_a(genomic_entity, molecular_entity).
has_uri(genomic_entity, 'http://w3id.org/biolink/vocab/GenomicEntity').
class_slot(genomic_entity, id).
required(id).
slotrange(identifier_type).
required_in(id, genomic_entity).
range_in(id, identifier_type, genomic_entity).
class_slot(genomic_entity, name).
required(name).
slotrange(label_type).
range_in(name, label_type, genomic_entity).
class_slot(genomic_entity, category).
required(category).
slotrange(iri_type).
multivalued_in(category, genomic_entity).
range_in(category, iri_type, genomic_entity).
class_slot(genomic_entity, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, genomic_entity).
range_in(related_to, named_thing, genomic_entity).
class_slot(genomic_entity, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, genomic_entity).
range_in(interacts_with, named_thing, genomic_entity).
class_slot(genomic_entity, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, genomic_entity).
class_slot(genomic_entity, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, genomic_entity).
class_slot(genomic_entity, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, genomic_entity).
range_in(synonym, label_type, genomic_entity).
class_slot(genomic_entity, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, genomic_entity).
class_slot(genomic_entity, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, genomic_entity).
class_slot(genomic_entity, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, genomic_entity).
class_slot(genomic_entity, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, genomic_entity).
range_in(has_phenotype, phenotypic_feature, genomic_entity).
class_slot(genomic_entity, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, genomic_entity).
range_in(molecularly_interacts_with, molecular_entity, genomic_entity).
class_slot(genomic_entity, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, genomic_entity).
range_in(affects_abundance_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, genomic_entity).
range_in(increases_abundance_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, genomic_entity).
range_in(decreases_abundance_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, genomic_entity).
range_in(affects_activity_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, genomic_entity).
range_in(increases_activity_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, genomic_entity).
range_in(decreases_activity_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, genomic_entity).
range_in(affects_expression_of, genomic_entity, genomic_entity).
class_slot(genomic_entity, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, genomic_entity).
range_in(increases_expression_of, genomic_entity, genomic_entity).
class_slot(genomic_entity, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, genomic_entity).
range_in(decreases_expression_of, genomic_entity, genomic_entity).
class_slot(genomic_entity, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, genomic_entity).
range_in(affects_folding_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, genomic_entity).
range_in(increases_folding_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, genomic_entity).
range_in(decreases_folding_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, genomic_entity).
range_in(affects_localization_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, genomic_entity).
range_in(increases_localization_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, genomic_entity).
range_in(decreases_localization_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, genomic_entity).
range_in(affects_metabolic_processing_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, genomic_entity).
range_in(increases_metabolic_processing_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, genomic_entity).
range_in(decreases_metabolic_processing_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, genomic_entity).
range_in(affects_molecular_modification_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, genomic_entity).
range_in(increases_molecular_modification_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, genomic_entity).
range_in(decreases_molecular_modification_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, genomic_entity).
range_in(affects_synthesis_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, genomic_entity).
range_in(increases_synthesis_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, genomic_entity).
range_in(decreases_synthesis_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, genomic_entity).
range_in(affects_degradation_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, genomic_entity).
range_in(increases_degradation_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, genomic_entity).
range_in(decreases_degradation_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, genomic_entity).
range_in(affects_mutation_rate_of, genomic_entity, genomic_entity).
class_slot(genomic_entity, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, genomic_entity).
range_in(increases_mutation_rate_of, genomic_entity, genomic_entity).
class_slot(genomic_entity, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, genomic_entity).
range_in(decreases_mutation_rate_of, genomic_entity, genomic_entity).
class_slot(genomic_entity, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, genomic_entity).
range_in(affects_response_to, molecular_entity, genomic_entity).
class_slot(genomic_entity, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, genomic_entity).
range_in(increases_response_to, molecular_entity, genomic_entity).
class_slot(genomic_entity, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, genomic_entity).
range_in(decreases_response_to, molecular_entity, genomic_entity).
class_slot(genomic_entity, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, genomic_entity).
range_in(affects_splicing_of, transcript, genomic_entity).
class_slot(genomic_entity, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, genomic_entity).
range_in(increases_splicing_of, transcript, genomic_entity).
class_slot(genomic_entity, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, genomic_entity).
range_in(decreases_splicing_of, transcript, genomic_entity).
class_slot(genomic_entity, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, genomic_entity).
range_in(affects_stability_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, genomic_entity).
range_in(increases_stability_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, genomic_entity).
range_in(decreases_stability_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, genomic_entity).
range_in(affects_transport_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, genomic_entity).
range_in(increases_transport_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, genomic_entity).
range_in(decreases_transport_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, genomic_entity).
range_in(affects_secretion_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, genomic_entity).
range_in(increases_secretion_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, genomic_entity).
range_in(decreases_secretion_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, genomic_entity).
range_in(affects_uptake_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, genomic_entity).
range_in(increases_uptake_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, genomic_entity).
range_in(decreases_uptake_of, molecular_entity, genomic_entity).
class_slot(genomic_entity, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, genomic_entity).
range_in(regulates_entity_to_entity, molecular_entity, genomic_entity).
class_slot(genomic_entity, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, genomic_entity).
range_in(biomarker_for, disease_or_phenotypic_feature, genomic_entity).
class_slot(genomic_entity, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, genomic_entity).
range_in(in_taxon, organism_taxon, genomic_entity).
class_slot(genomic_entity, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, genomic_entity).
class(genomic_sequence_localization).
is_a(genomic_sequence_localization, association).
has_uri(genomic_sequence_localization, 'http://w3id.org/biolink/vocab/GenomicSequenceLocalization').
class_slot(genomic_sequence_localization, id).
required(id).
slotrange(identifier_type).
required_in(id, genomic_sequence_localization).
range_in(id, identifier_type, genomic_sequence_localization).
class_slot(genomic_sequence_localization, subject).
required(subject).
slotrange(genomic_entity).
required_in(subject, genomic_sequence_localization).
range_in(subject, genomic_entity, genomic_sequence_localization).
class_slot(genomic_sequence_localization, relation).
required(relation).
slotrange(iri_type).
required_in(relation, genomic_sequence_localization).
range_in(relation, iri_type, genomic_sequence_localization).
class_slot(genomic_sequence_localization, object).
required(object).
slotrange(genomic_entity).
required_in(object, genomic_sequence_localization).
range_in(object, genomic_entity, genomic_sequence_localization).
class_slot(genomic_sequence_localization, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, genomic_sequence_localization).
class_slot(genomic_sequence_localization, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, genomic_sequence_localization).
class_slot(genomic_sequence_localization, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, genomic_sequence_localization).
range_in(qualifiers, ontology_class, genomic_sequence_localization).
class_slot(genomic_sequence_localization, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, genomic_sequence_localization).
range_in(publications, publication, genomic_sequence_localization).
class_slot(genomic_sequence_localization, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, genomic_sequence_localization).
class_slot(genomic_sequence_localization, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, genomic_sequence_localization).
class_slot(genomic_sequence_localization, start_interbase_coordinate).
required(start_interbase_coordinate).
slotrange(string).
range_in(start_interbase_coordinate, string, genomic_sequence_localization).
class_slot(genomic_sequence_localization, end_interbase_coordinate).
required(end_interbase_coordinate).
slotrange(string).
range_in(end_interbase_coordinate, string, genomic_sequence_localization).
class_slot(genomic_sequence_localization, genome_build).
required(genome_build).
slotrange(string).
range_in(genome_build, string, genomic_sequence_localization).
class_slot(genomic_sequence_localization, phase).
required(phase).
slotrange(string).
range_in(phase, string, genomic_sequence_localization).
class(genotype).
is_a(genotype, genomic_entity).
has_uri(genotype, 'http://w3id.org/biolink/vocab/Genotype').
class_slot(genotype, id).
required(id).
slotrange(identifier_type).
required_in(id, genotype).
range_in(id, identifier_type, genotype).
class_slot(genotype, name).
required(name).
slotrange(label_type).
range_in(name, label_type, genotype).
class_slot(genotype, category).
required(category).
slotrange(iri_type).
multivalued_in(category, genotype).
range_in(category, iri_type, genotype).
class_slot(genotype, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, genotype).
range_in(related_to, named_thing, genotype).
class_slot(genotype, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, genotype).
range_in(interacts_with, named_thing, genotype).
class_slot(genotype, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, genotype).
class_slot(genotype, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, genotype).
class_slot(genotype, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, genotype).
range_in(synonym, label_type, genotype).
class_slot(genotype, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, genotype).
class_slot(genotype, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, genotype).
class_slot(genotype, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, genotype).
class_slot(genotype, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, genotype).
range_in(has_phenotype, phenotypic_feature, genotype).
class_slot(genotype, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, genotype).
range_in(molecularly_interacts_with, molecular_entity, genotype).
class_slot(genotype, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, genotype).
range_in(affects_abundance_of, molecular_entity, genotype).
class_slot(genotype, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, genotype).
range_in(increases_abundance_of, molecular_entity, genotype).
class_slot(genotype, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, genotype).
range_in(decreases_abundance_of, molecular_entity, genotype).
class_slot(genotype, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, genotype).
range_in(affects_activity_of, molecular_entity, genotype).
class_slot(genotype, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, genotype).
range_in(increases_activity_of, molecular_entity, genotype).
class_slot(genotype, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, genotype).
range_in(decreases_activity_of, molecular_entity, genotype).
class_slot(genotype, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, genotype).
range_in(affects_expression_of, genomic_entity, genotype).
class_slot(genotype, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, genotype).
range_in(increases_expression_of, genomic_entity, genotype).
class_slot(genotype, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, genotype).
range_in(decreases_expression_of, genomic_entity, genotype).
class_slot(genotype, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, genotype).
range_in(affects_folding_of, molecular_entity, genotype).
class_slot(genotype, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, genotype).
range_in(increases_folding_of, molecular_entity, genotype).
class_slot(genotype, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, genotype).
range_in(decreases_folding_of, molecular_entity, genotype).
class_slot(genotype, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, genotype).
range_in(affects_localization_of, molecular_entity, genotype).
class_slot(genotype, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, genotype).
range_in(increases_localization_of, molecular_entity, genotype).
class_slot(genotype, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, genotype).
range_in(decreases_localization_of, molecular_entity, genotype).
class_slot(genotype, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, genotype).
range_in(affects_metabolic_processing_of, molecular_entity, genotype).
class_slot(genotype, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, genotype).
range_in(increases_metabolic_processing_of, molecular_entity, genotype).
class_slot(genotype, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, genotype).
range_in(decreases_metabolic_processing_of, molecular_entity, genotype).
class_slot(genotype, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, genotype).
range_in(affects_molecular_modification_of, molecular_entity, genotype).
class_slot(genotype, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, genotype).
range_in(increases_molecular_modification_of, molecular_entity, genotype).
class_slot(genotype, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, genotype).
range_in(decreases_molecular_modification_of, molecular_entity, genotype).
class_slot(genotype, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, genotype).
range_in(affects_synthesis_of, molecular_entity, genotype).
class_slot(genotype, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, genotype).
range_in(increases_synthesis_of, molecular_entity, genotype).
class_slot(genotype, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, genotype).
range_in(decreases_synthesis_of, molecular_entity, genotype).
class_slot(genotype, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, genotype).
range_in(affects_degradation_of, molecular_entity, genotype).
class_slot(genotype, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, genotype).
range_in(increases_degradation_of, molecular_entity, genotype).
class_slot(genotype, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, genotype).
range_in(decreases_degradation_of, molecular_entity, genotype).
class_slot(genotype, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, genotype).
range_in(affects_mutation_rate_of, genomic_entity, genotype).
class_slot(genotype, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, genotype).
range_in(increases_mutation_rate_of, genomic_entity, genotype).
class_slot(genotype, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, genotype).
range_in(decreases_mutation_rate_of, genomic_entity, genotype).
class_slot(genotype, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, genotype).
range_in(affects_response_to, molecular_entity, genotype).
class_slot(genotype, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, genotype).
range_in(increases_response_to, molecular_entity, genotype).
class_slot(genotype, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, genotype).
range_in(decreases_response_to, molecular_entity, genotype).
class_slot(genotype, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, genotype).
range_in(affects_splicing_of, transcript, genotype).
class_slot(genotype, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, genotype).
range_in(increases_splicing_of, transcript, genotype).
class_slot(genotype, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, genotype).
range_in(decreases_splicing_of, transcript, genotype).
class_slot(genotype, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, genotype).
range_in(affects_stability_of, molecular_entity, genotype).
class_slot(genotype, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, genotype).
range_in(increases_stability_of, molecular_entity, genotype).
class_slot(genotype, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, genotype).
range_in(decreases_stability_of, molecular_entity, genotype).
class_slot(genotype, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, genotype).
range_in(affects_transport_of, molecular_entity, genotype).
class_slot(genotype, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, genotype).
range_in(increases_transport_of, molecular_entity, genotype).
class_slot(genotype, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, genotype).
range_in(decreases_transport_of, molecular_entity, genotype).
class_slot(genotype, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, genotype).
range_in(affects_secretion_of, molecular_entity, genotype).
class_slot(genotype, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, genotype).
range_in(increases_secretion_of, molecular_entity, genotype).
class_slot(genotype, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, genotype).
range_in(decreases_secretion_of, molecular_entity, genotype).
class_slot(genotype, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, genotype).
range_in(affects_uptake_of, molecular_entity, genotype).
class_slot(genotype, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, genotype).
range_in(increases_uptake_of, molecular_entity, genotype).
class_slot(genotype, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, genotype).
range_in(decreases_uptake_of, molecular_entity, genotype).
class_slot(genotype, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, genotype).
range_in(regulates_entity_to_entity, molecular_entity, genotype).
class_slot(genotype, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, genotype).
range_in(biomarker_for, disease_or_phenotypic_feature, genotype).
class_slot(genotype, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, genotype).
range_in(in_taxon, organism_taxon, genotype).
class_slot(genotype, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, genotype).
class_slot(genotype, has_zygosity).
required(has_zygosity).
slotrange(zygosity).
range_in(has_zygosity, zygosity, genotype).
class(genotype_to_gene_association).
is_a(genotype_to_gene_association, association).
defining_slots(association, [subject, object]).
has_uri(genotype_to_gene_association, 'http://w3id.org/biolink/vocab/GenotypeToGeneAssociation').
class_slot(genotype_to_gene_association, id).
required(id).
slotrange(identifier_type).
required_in(id, genotype_to_gene_association).
range_in(id, identifier_type, genotype_to_gene_association).
class_slot(genotype_to_gene_association, subject).
required(subject).
slotrange(genotype).
required_in(subject, genotype_to_gene_association).
range_in(subject, genotype, genotype_to_gene_association).
class_slot(genotype_to_gene_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, genotype_to_gene_association).
range_in(relation, iri_type, genotype_to_gene_association).
class_slot(genotype_to_gene_association, object).
required(object).
slotrange(gene).
required_in(object, genotype_to_gene_association).
range_in(object, gene, genotype_to_gene_association).
class_slot(genotype_to_gene_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, genotype_to_gene_association).
class_slot(genotype_to_gene_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, genotype_to_gene_association).
class_slot(genotype_to_gene_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, genotype_to_gene_association).
range_in(qualifiers, ontology_class, genotype_to_gene_association).
class_slot(genotype_to_gene_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, genotype_to_gene_association).
range_in(publications, publication, genotype_to_gene_association).
class_slot(genotype_to_gene_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, genotype_to_gene_association).
class_slot(genotype_to_gene_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, genotype_to_gene_association).
class(genotype_to_genotype_part_association).
is_a(genotype_to_genotype_part_association, association).
defining_slots(association, [subject, object]).
has_uri(genotype_to_genotype_part_association, 'http://w3id.org/biolink/vocab/GenotypeToGenotypePartAssociation').
class_slot(genotype_to_genotype_part_association, id).
required(id).
slotrange(identifier_type).
required_in(id, genotype_to_genotype_part_association).
range_in(id, identifier_type, genotype_to_genotype_part_association).
class_slot(genotype_to_genotype_part_association, subject).
required(subject).
slotrange(genotype).
required_in(subject, genotype_to_genotype_part_association).
range_in(subject, genotype, genotype_to_genotype_part_association).
class_slot(genotype_to_genotype_part_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, genotype_to_genotype_part_association).
range_in(relation, iri_type, genotype_to_genotype_part_association).
class_slot(genotype_to_genotype_part_association, object).
required(object).
slotrange(genotype).
required_in(object, genotype_to_genotype_part_association).
range_in(object, genotype, genotype_to_genotype_part_association).
class_slot(genotype_to_genotype_part_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, genotype_to_genotype_part_association).
class_slot(genotype_to_genotype_part_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, genotype_to_genotype_part_association).
class_slot(genotype_to_genotype_part_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, genotype_to_genotype_part_association).
range_in(qualifiers, ontology_class, genotype_to_genotype_part_association).
class_slot(genotype_to_genotype_part_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, genotype_to_genotype_part_association).
range_in(publications, publication, genotype_to_genotype_part_association).
class_slot(genotype_to_genotype_part_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, genotype_to_genotype_part_association).
class_slot(genotype_to_genotype_part_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, genotype_to_genotype_part_association).
class(genotype_to_phenotypic_feature_association).
mixin(genotype_to_phenotypic_feature_association, entity_to_phenotypic_feature_association).
mixin(genotype_to_phenotypic_feature_association, genotype_to_thing_association).
is_a(genotype_to_phenotypic_feature_association, association).
defining_slots(association, [subject, object]).
has_uri(genotype_to_phenotypic_feature_association, 'http://w3id.org/biolink/vocab/GenotypeToPhenotypicFeatureAssociation').
class_slot(genotype_to_phenotypic_feature_association, id).
required(id).
slotrange(identifier_type).
required_in(id, genotype_to_phenotypic_feature_association).
range_in(id, identifier_type, genotype_to_phenotypic_feature_association).
class_slot(genotype_to_phenotypic_feature_association, subject).
required(subject).
slotrange(genotype).
required_in(subject, genotype_to_phenotypic_feature_association).
range_in(subject, genotype, genotype_to_phenotypic_feature_association).
class_slot(genotype_to_phenotypic_feature_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, genotype_to_phenotypic_feature_association).
range_in(relation, iri_type, genotype_to_phenotypic_feature_association).
class_slot(genotype_to_phenotypic_feature_association, object).
required(object).
slotrange(iri_type).
required_in(object, genotype_to_phenotypic_feature_association).
range_in(object, iri_type, genotype_to_phenotypic_feature_association).
class_slot(genotype_to_phenotypic_feature_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, genotype_to_phenotypic_feature_association).
class_slot(genotype_to_phenotypic_feature_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, genotype_to_phenotypic_feature_association).
class_slot(genotype_to_phenotypic_feature_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, genotype_to_phenotypic_feature_association).
range_in(qualifiers, ontology_class, genotype_to_phenotypic_feature_association).
class_slot(genotype_to_phenotypic_feature_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, genotype_to_phenotypic_feature_association).
range_in(publications, publication, genotype_to_phenotypic_feature_association).
class_slot(genotype_to_phenotypic_feature_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, genotype_to_phenotypic_feature_association).
class_slot(genotype_to_phenotypic_feature_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, genotype_to_phenotypic_feature_association).
class_slot(genotype_to_phenotypic_feature_association, sex_qualifier).
required(sex_qualifier).
slotrange(biological_sex).
range_in(sex_qualifier, biological_sex, genotype_to_phenotypic_feature_association).
class_slot(genotype_to_phenotypic_feature_association, frequency_qualifier).
required(frequency_qualifier).
slotrange(frequency_value).
range_in(frequency_qualifier, frequency_value, genotype_to_phenotypic_feature_association).
class_slot(genotype_to_phenotypic_feature_association, severity_qualifier).
required(severity_qualifier).
slotrange(severity_value).
range_in(severity_qualifier, severity_value, genotype_to_phenotypic_feature_association).
class_slot(genotype_to_phenotypic_feature_association, onset_qualifier).
required(onset_qualifier).
slotrange(onset).
range_in(onset_qualifier, onset, genotype_to_phenotypic_feature_association).
class(genotype_to_thing_association).
is_a(genotype_to_thing_association, association).
defining_slots(association, [subject]).
has_uri(genotype_to_thing_association, 'http://w3id.org/biolink/vocab/GenotypeToThingAssociation').
class_slot(genotype_to_thing_association, id).
required(id).
slotrange(identifier_type).
required_in(id, genotype_to_thing_association).
range_in(id, identifier_type, genotype_to_thing_association).
class_slot(genotype_to_thing_association, subject).
required(subject).
slotrange(genotype).
required_in(subject, genotype_to_thing_association).
range_in(subject, genotype, genotype_to_thing_association).
class_slot(genotype_to_thing_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, genotype_to_thing_association).
range_in(relation, iri_type, genotype_to_thing_association).
class_slot(genotype_to_thing_association, object).
required(object).
slotrange(iri_type).
required_in(object, genotype_to_thing_association).
range_in(object, iri_type, genotype_to_thing_association).
class_slot(genotype_to_thing_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, genotype_to_thing_association).
class_slot(genotype_to_thing_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, genotype_to_thing_association).
class_slot(genotype_to_thing_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, genotype_to_thing_association).
range_in(qualifiers, ontology_class, genotype_to_thing_association).
class_slot(genotype_to_thing_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, genotype_to_thing_association).
range_in(publications, publication, genotype_to_thing_association).
class_slot(genotype_to_thing_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, genotype_to_thing_association).
class_slot(genotype_to_thing_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, genotype_to_thing_association).
class(genotype_to_variant_association).
is_a(genotype_to_variant_association, association).
defining_slots(association, [subject, object]).
has_uri(genotype_to_variant_association, 'http://w3id.org/biolink/vocab/GenotypeToVariantAssociation').
class_slot(genotype_to_variant_association, id).
required(id).
slotrange(identifier_type).
required_in(id, genotype_to_variant_association).
range_in(id, identifier_type, genotype_to_variant_association).
class_slot(genotype_to_variant_association, subject).
required(subject).
slotrange(genotype).
required_in(subject, genotype_to_variant_association).
range_in(subject, genotype, genotype_to_variant_association).
class_slot(genotype_to_variant_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, genotype_to_variant_association).
range_in(relation, iri_type, genotype_to_variant_association).
class_slot(genotype_to_variant_association, object).
required(object).
slotrange(sequence_variant).
required_in(object, genotype_to_variant_association).
range_in(object, sequence_variant, genotype_to_variant_association).
class_slot(genotype_to_variant_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, genotype_to_variant_association).
class_slot(genotype_to_variant_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, genotype_to_variant_association).
class_slot(genotype_to_variant_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, genotype_to_variant_association).
range_in(qualifiers, ontology_class, genotype_to_variant_association).
class_slot(genotype_to_variant_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, genotype_to_variant_association).
range_in(publications, publication, genotype_to_variant_association).
class_slot(genotype_to_variant_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, genotype_to_variant_association).
class_slot(genotype_to_variant_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, genotype_to_variant_association).
class(genotypic_sex).
is_a(genotypic_sex, biological_sex).
has_uri(genotypic_sex, 'http://w3id.org/biolink/vocab/GenotypicSex').
class_slot(genotypic_sex, id).
required(id).
slotrange(identifier_type).
required_in(id, genotypic_sex).
range_in(id, identifier_type, genotypic_sex).
class_slot(genotypic_sex, name).
required(name).
slotrange(label_type).
range_in(name, label_type, genotypic_sex).
class_slot(genotypic_sex, category).
required(category).
slotrange(iri_type).
multivalued_in(category, genotypic_sex).
range_in(category, iri_type, genotypic_sex).
class_slot(genotypic_sex, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, genotypic_sex).
range_in(related_to, named_thing, genotypic_sex).
class_slot(genotypic_sex, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, genotypic_sex).
range_in(interacts_with, named_thing, genotypic_sex).
class_slot(genotypic_sex, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, genotypic_sex).
class_slot(genotypic_sex, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, genotypic_sex).
class_slot(genotypic_sex, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, genotypic_sex).
range_in(synonym, label_type, genotypic_sex).
class_slot(genotypic_sex, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, genotypic_sex).
class_slot(genotypic_sex, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, genotypic_sex).
class_slot(genotypic_sex, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, genotypic_sex).
class_slot(genotypic_sex, subclass_of).
required(subclass_of).
slotrange(ontology_class).
multivalued_in(subclass_of, genotypic_sex).
range_in(subclass_of, ontology_class, genotypic_sex).
class(geographic_location).
is_a(geographic_location, planetary_entity).
has_uri(geographic_location, 'http://w3id.org/biolink/vocab/GeographicLocation').
class_slot(geographic_location, id).
required(id).
slotrange(identifier_type).
required_in(id, geographic_location).
range_in(id, identifier_type, geographic_location).
class_slot(geographic_location, name).
required(name).
slotrange(label_type).
range_in(name, label_type, geographic_location).
class_slot(geographic_location, category).
required(category).
slotrange(iri_type).
multivalued_in(category, geographic_location).
range_in(category, iri_type, geographic_location).
class_slot(geographic_location, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, geographic_location).
range_in(related_to, named_thing, geographic_location).
class_slot(geographic_location, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, geographic_location).
range_in(interacts_with, named_thing, geographic_location).
class_slot(geographic_location, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, geographic_location).
class_slot(geographic_location, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, geographic_location).
class_slot(geographic_location, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, geographic_location).
range_in(synonym, label_type, geographic_location).
class_slot(geographic_location, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, geographic_location).
class_slot(geographic_location, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, geographic_location).
class_slot(geographic_location, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, geographic_location).
class_slot(geographic_location, latitude).
required(latitude).
slotrange(float).
range_in(latitude, float, geographic_location).
class_slot(geographic_location, longitude).
required(longitude).
slotrange(float).
range_in(longitude, float, geographic_location).
class(geographic_location_at_time).
is_a(geographic_location_at_time, geographic_location).
has_uri(geographic_location_at_time, 'http://w3id.org/biolink/vocab/GeographicLocationAtTime').
class_slot(geographic_location_at_time, id).
required(id).
slotrange(identifier_type).
required_in(id, geographic_location_at_time).
range_in(id, identifier_type, geographic_location_at_time).
class_slot(geographic_location_at_time, name).
required(name).
slotrange(label_type).
range_in(name, label_type, geographic_location_at_time).
class_slot(geographic_location_at_time, category).
required(category).
slotrange(iri_type).
multivalued_in(category, geographic_location_at_time).
range_in(category, iri_type, geographic_location_at_time).
class_slot(geographic_location_at_time, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, geographic_location_at_time).
range_in(related_to, named_thing, geographic_location_at_time).
class_slot(geographic_location_at_time, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, geographic_location_at_time).
range_in(interacts_with, named_thing, geographic_location_at_time).
class_slot(geographic_location_at_time, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, geographic_location_at_time).
class_slot(geographic_location_at_time, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, geographic_location_at_time).
class_slot(geographic_location_at_time, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, geographic_location_at_time).
range_in(synonym, label_type, geographic_location_at_time).
class_slot(geographic_location_at_time, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, geographic_location_at_time).
class_slot(geographic_location_at_time, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, geographic_location_at_time).
class_slot(geographic_location_at_time, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, geographic_location_at_time).
class_slot(geographic_location_at_time, latitude).
required(latitude).
slotrange(float).
range_in(latitude, float, geographic_location_at_time).
class_slot(geographic_location_at_time, longitude).
required(longitude).
slotrange(float).
range_in(longitude, float, geographic_location_at_time).
class_slot(geographic_location_at_time, timepoint).
required(timepoint).
slotrange(time_type).
range_in(timepoint, time_type, geographic_location_at_time).
class(gross_anatomical_structure).
is_a(gross_anatomical_structure, anatomical_entity).
has_uri(gross_anatomical_structure, 'http://w3id.org/biolink/vocab/GrossAnatomicalStructure').
class_slot(gross_anatomical_structure, id).
required(id).
slotrange(identifier_type).
required_in(id, gross_anatomical_structure).
range_in(id, identifier_type, gross_anatomical_structure).
class_slot(gross_anatomical_structure, name).
required(name).
slotrange(label_type).
range_in(name, label_type, gross_anatomical_structure).
class_slot(gross_anatomical_structure, category).
required(category).
slotrange(iri_type).
multivalued_in(category, gross_anatomical_structure).
range_in(category, iri_type, gross_anatomical_structure).
class_slot(gross_anatomical_structure, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, gross_anatomical_structure).
range_in(related_to, named_thing, gross_anatomical_structure).
class_slot(gross_anatomical_structure, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, gross_anatomical_structure).
range_in(interacts_with, named_thing, gross_anatomical_structure).
class_slot(gross_anatomical_structure, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, gross_anatomical_structure).
class_slot(gross_anatomical_structure, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, gross_anatomical_structure).
class_slot(gross_anatomical_structure, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, gross_anatomical_structure).
range_in(synonym, label_type, gross_anatomical_structure).
class_slot(gross_anatomical_structure, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, gross_anatomical_structure).
class_slot(gross_anatomical_structure, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, gross_anatomical_structure).
class_slot(gross_anatomical_structure, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, gross_anatomical_structure).
class_slot(gross_anatomical_structure, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, gross_anatomical_structure).
range_in(has_phenotype, phenotypic_feature, gross_anatomical_structure).
class_slot(gross_anatomical_structure, expresses).
required(expresses).
slotrange(gene_or_gene_product).
multivalued_in(expresses, gross_anatomical_structure).
range_in(expresses, gene_or_gene_product, gross_anatomical_structure).
class_slot(gross_anatomical_structure, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, gross_anatomical_structure).
range_in(in_taxon, organism_taxon, gross_anatomical_structure).
class(haplotype).
is_a(haplotype, genomic_entity).
has_uri(haplotype, 'http://w3id.org/biolink/vocab/Haplotype').
class_slot(haplotype, id).
required(id).
slotrange(identifier_type).
required_in(id, haplotype).
range_in(id, identifier_type, haplotype).
class_slot(haplotype, name).
required(name).
slotrange(label_type).
range_in(name, label_type, haplotype).
class_slot(haplotype, category).
required(category).
slotrange(iri_type).
multivalued_in(category, haplotype).
range_in(category, iri_type, haplotype).
class_slot(haplotype, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, haplotype).
range_in(related_to, named_thing, haplotype).
class_slot(haplotype, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, haplotype).
range_in(interacts_with, named_thing, haplotype).
class_slot(haplotype, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, haplotype).
class_slot(haplotype, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, haplotype).
class_slot(haplotype, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, haplotype).
range_in(synonym, label_type, haplotype).
class_slot(haplotype, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, haplotype).
class_slot(haplotype, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, haplotype).
class_slot(haplotype, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, haplotype).
class_slot(haplotype, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, haplotype).
range_in(has_phenotype, phenotypic_feature, haplotype).
class_slot(haplotype, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, haplotype).
range_in(molecularly_interacts_with, molecular_entity, haplotype).
class_slot(haplotype, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, haplotype).
range_in(affects_abundance_of, molecular_entity, haplotype).
class_slot(haplotype, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, haplotype).
range_in(increases_abundance_of, molecular_entity, haplotype).
class_slot(haplotype, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, haplotype).
range_in(decreases_abundance_of, molecular_entity, haplotype).
class_slot(haplotype, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, haplotype).
range_in(affects_activity_of, molecular_entity, haplotype).
class_slot(haplotype, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, haplotype).
range_in(increases_activity_of, molecular_entity, haplotype).
class_slot(haplotype, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, haplotype).
range_in(decreases_activity_of, molecular_entity, haplotype).
class_slot(haplotype, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, haplotype).
range_in(affects_expression_of, genomic_entity, haplotype).
class_slot(haplotype, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, haplotype).
range_in(increases_expression_of, genomic_entity, haplotype).
class_slot(haplotype, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, haplotype).
range_in(decreases_expression_of, genomic_entity, haplotype).
class_slot(haplotype, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, haplotype).
range_in(affects_folding_of, molecular_entity, haplotype).
class_slot(haplotype, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, haplotype).
range_in(increases_folding_of, molecular_entity, haplotype).
class_slot(haplotype, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, haplotype).
range_in(decreases_folding_of, molecular_entity, haplotype).
class_slot(haplotype, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, haplotype).
range_in(affects_localization_of, molecular_entity, haplotype).
class_slot(haplotype, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, haplotype).
range_in(increases_localization_of, molecular_entity, haplotype).
class_slot(haplotype, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, haplotype).
range_in(decreases_localization_of, molecular_entity, haplotype).
class_slot(haplotype, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, haplotype).
range_in(affects_metabolic_processing_of, molecular_entity, haplotype).
class_slot(haplotype, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, haplotype).
range_in(increases_metabolic_processing_of, molecular_entity, haplotype).
class_slot(haplotype, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, haplotype).
range_in(decreases_metabolic_processing_of, molecular_entity, haplotype).
class_slot(haplotype, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, haplotype).
range_in(affects_molecular_modification_of, molecular_entity, haplotype).
class_slot(haplotype, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, haplotype).
range_in(increases_molecular_modification_of, molecular_entity, haplotype).
class_slot(haplotype, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, haplotype).
range_in(decreases_molecular_modification_of, molecular_entity, haplotype).
class_slot(haplotype, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, haplotype).
range_in(affects_synthesis_of, molecular_entity, haplotype).
class_slot(haplotype, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, haplotype).
range_in(increases_synthesis_of, molecular_entity, haplotype).
class_slot(haplotype, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, haplotype).
range_in(decreases_synthesis_of, molecular_entity, haplotype).
class_slot(haplotype, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, haplotype).
range_in(affects_degradation_of, molecular_entity, haplotype).
class_slot(haplotype, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, haplotype).
range_in(increases_degradation_of, molecular_entity, haplotype).
class_slot(haplotype, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, haplotype).
range_in(decreases_degradation_of, molecular_entity, haplotype).
class_slot(haplotype, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, haplotype).
range_in(affects_mutation_rate_of, genomic_entity, haplotype).
class_slot(haplotype, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, haplotype).
range_in(increases_mutation_rate_of, genomic_entity, haplotype).
class_slot(haplotype, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, haplotype).
range_in(decreases_mutation_rate_of, genomic_entity, haplotype).
class_slot(haplotype, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, haplotype).
range_in(affects_response_to, molecular_entity, haplotype).
class_slot(haplotype, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, haplotype).
range_in(increases_response_to, molecular_entity, haplotype).
class_slot(haplotype, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, haplotype).
range_in(decreases_response_to, molecular_entity, haplotype).
class_slot(haplotype, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, haplotype).
range_in(affects_splicing_of, transcript, haplotype).
class_slot(haplotype, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, haplotype).
range_in(increases_splicing_of, transcript, haplotype).
class_slot(haplotype, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, haplotype).
range_in(decreases_splicing_of, transcript, haplotype).
class_slot(haplotype, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, haplotype).
range_in(affects_stability_of, molecular_entity, haplotype).
class_slot(haplotype, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, haplotype).
range_in(increases_stability_of, molecular_entity, haplotype).
class_slot(haplotype, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, haplotype).
range_in(decreases_stability_of, molecular_entity, haplotype).
class_slot(haplotype, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, haplotype).
range_in(affects_transport_of, molecular_entity, haplotype).
class_slot(haplotype, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, haplotype).
range_in(increases_transport_of, molecular_entity, haplotype).
class_slot(haplotype, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, haplotype).
range_in(decreases_transport_of, molecular_entity, haplotype).
class_slot(haplotype, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, haplotype).
range_in(affects_secretion_of, molecular_entity, haplotype).
class_slot(haplotype, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, haplotype).
range_in(increases_secretion_of, molecular_entity, haplotype).
class_slot(haplotype, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, haplotype).
range_in(decreases_secretion_of, molecular_entity, haplotype).
class_slot(haplotype, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, haplotype).
range_in(affects_uptake_of, molecular_entity, haplotype).
class_slot(haplotype, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, haplotype).
range_in(increases_uptake_of, molecular_entity, haplotype).
class_slot(haplotype, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, haplotype).
range_in(decreases_uptake_of, molecular_entity, haplotype).
class_slot(haplotype, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, haplotype).
range_in(regulates_entity_to_entity, molecular_entity, haplotype).
class_slot(haplotype, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, haplotype).
range_in(biomarker_for, disease_or_phenotypic_feature, haplotype).
class_slot(haplotype, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, haplotype).
range_in(in_taxon, organism_taxon, haplotype).
class_slot(haplotype, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, haplotype).
class(individual_organism).
mixin(individual_organism, thing_with_taxon).
is_a(individual_organism, organismal_entity).
has_uri(individual_organism, 'http://w3id.org/biolink/vocab/IndividualOrganism').
class_slot(individual_organism, id).
required(id).
slotrange(identifier_type).
required_in(id, individual_organism).
range_in(id, identifier_type, individual_organism).
class_slot(individual_organism, name).
required(name).
slotrange(label_type).
range_in(name, label_type, individual_organism).
class_slot(individual_organism, category).
required(category).
slotrange(iri_type).
multivalued_in(category, individual_organism).
range_in(category, iri_type, individual_organism).
class_slot(individual_organism, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, individual_organism).
range_in(related_to, named_thing, individual_organism).
class_slot(individual_organism, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, individual_organism).
range_in(interacts_with, named_thing, individual_organism).
class_slot(individual_organism, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, individual_organism).
class_slot(individual_organism, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, individual_organism).
class_slot(individual_organism, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, individual_organism).
range_in(synonym, label_type, individual_organism).
class_slot(individual_organism, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, individual_organism).
class_slot(individual_organism, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, individual_organism).
class_slot(individual_organism, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, individual_organism).
class_slot(individual_organism, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, individual_organism).
range_in(has_phenotype, phenotypic_feature, individual_organism).
class_slot(individual_organism, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, individual_organism).
range_in(in_taxon, organism_taxon, individual_organism).
class(information_content_entity).
is_a(information_content_entity, named_thing).
has_uri(information_content_entity, 'http://w3id.org/biolink/vocab/InformationContentEntity').
class_slot(information_content_entity, id).
required(id).
slotrange(identifier_type).
required_in(id, information_content_entity).
range_in(id, identifier_type, information_content_entity).
class_slot(information_content_entity, name).
required(name).
slotrange(label_type).
range_in(name, label_type, information_content_entity).
class_slot(information_content_entity, category).
required(category).
slotrange(iri_type).
multivalued_in(category, information_content_entity).
range_in(category, iri_type, information_content_entity).
class_slot(information_content_entity, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, information_content_entity).
range_in(related_to, named_thing, information_content_entity).
class_slot(information_content_entity, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, information_content_entity).
range_in(interacts_with, named_thing, information_content_entity).
class_slot(information_content_entity, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, information_content_entity).
class_slot(information_content_entity, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, information_content_entity).
class_slot(information_content_entity, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, information_content_entity).
range_in(synonym, label_type, information_content_entity).
class_slot(information_content_entity, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, information_content_entity).
class_slot(information_content_entity, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, information_content_entity).
class_slot(information_content_entity, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, information_content_entity).
class(life_stage).
mixin(life_stage, thing_with_taxon).
is_a(life_stage, organismal_entity).
has_uri(life_stage, 'http://w3id.org/biolink/vocab/LifeStage').
class_slot(life_stage, id).
required(id).
slotrange(identifier_type).
required_in(id, life_stage).
range_in(id, identifier_type, life_stage).
class_slot(life_stage, name).
required(name).
slotrange(label_type).
range_in(name, label_type, life_stage).
class_slot(life_stage, category).
required(category).
slotrange(iri_type).
multivalued_in(category, life_stage).
range_in(category, iri_type, life_stage).
class_slot(life_stage, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, life_stage).
range_in(related_to, named_thing, life_stage).
class_slot(life_stage, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, life_stage).
range_in(interacts_with, named_thing, life_stage).
class_slot(life_stage, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, life_stage).
class_slot(life_stage, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, life_stage).
class_slot(life_stage, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, life_stage).
range_in(synonym, label_type, life_stage).
class_slot(life_stage, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, life_stage).
class_slot(life_stage, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, life_stage).
class_slot(life_stage, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, life_stage).
class_slot(life_stage, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, life_stage).
range_in(has_phenotype, phenotypic_feature, life_stage).
class_slot(life_stage, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, life_stage).
range_in(in_taxon, organism_taxon, life_stage).
class(macromolecular_complex).
is_a(macromolecular_complex, macromolecular_machine).
has_uri(macromolecular_complex, 'http://w3id.org/biolink/vocab/MacromolecularComplex').
class_slot(macromolecular_complex, id).
required(id).
slotrange(identifier_type).
required_in(id, macromolecular_complex).
range_in(id, identifier_type, macromolecular_complex).
class_slot(macromolecular_complex, name).
required(name).
slotrange(symbol_type).
range_in(name, symbol_type, macromolecular_complex).
class_slot(macromolecular_complex, category).
required(category).
slotrange(iri_type).
multivalued_in(category, macromolecular_complex).
range_in(category, iri_type, macromolecular_complex).
class_slot(macromolecular_complex, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, macromolecular_complex).
range_in(related_to, named_thing, macromolecular_complex).
class_slot(macromolecular_complex, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, macromolecular_complex).
range_in(interacts_with, named_thing, macromolecular_complex).
class_slot(macromolecular_complex, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, macromolecular_complex).
class_slot(macromolecular_complex, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, macromolecular_complex).
class_slot(macromolecular_complex, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, macromolecular_complex).
range_in(synonym, label_type, macromolecular_complex).
class_slot(macromolecular_complex, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, macromolecular_complex).
class_slot(macromolecular_complex, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, macromolecular_complex).
class_slot(macromolecular_complex, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, macromolecular_complex).
class_slot(macromolecular_complex, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, macromolecular_complex).
range_in(has_phenotype, phenotypic_feature, macromolecular_complex).
class_slot(macromolecular_complex, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, macromolecular_complex).
range_in(molecularly_interacts_with, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, macromolecular_complex).
range_in(affects_abundance_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, macromolecular_complex).
range_in(increases_abundance_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, macromolecular_complex).
range_in(decreases_abundance_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, macromolecular_complex).
range_in(affects_activity_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, macromolecular_complex).
range_in(increases_activity_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, macromolecular_complex).
range_in(decreases_activity_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, macromolecular_complex).
range_in(affects_expression_of, genomic_entity, macromolecular_complex).
class_slot(macromolecular_complex, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, macromolecular_complex).
range_in(increases_expression_of, genomic_entity, macromolecular_complex).
class_slot(macromolecular_complex, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, macromolecular_complex).
range_in(decreases_expression_of, genomic_entity, macromolecular_complex).
class_slot(macromolecular_complex, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, macromolecular_complex).
range_in(affects_folding_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, macromolecular_complex).
range_in(increases_folding_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, macromolecular_complex).
range_in(decreases_folding_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, macromolecular_complex).
range_in(affects_localization_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, macromolecular_complex).
range_in(increases_localization_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, macromolecular_complex).
range_in(decreases_localization_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, macromolecular_complex).
range_in(affects_metabolic_processing_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, macromolecular_complex).
range_in(increases_metabolic_processing_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, macromolecular_complex).
range_in(decreases_metabolic_processing_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, macromolecular_complex).
range_in(affects_molecular_modification_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, macromolecular_complex).
range_in(increases_molecular_modification_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, macromolecular_complex).
range_in(decreases_molecular_modification_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, macromolecular_complex).
range_in(affects_synthesis_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, macromolecular_complex).
range_in(increases_synthesis_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, macromolecular_complex).
range_in(decreases_synthesis_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, macromolecular_complex).
range_in(affects_degradation_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, macromolecular_complex).
range_in(increases_degradation_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, macromolecular_complex).
range_in(decreases_degradation_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, macromolecular_complex).
range_in(affects_mutation_rate_of, genomic_entity, macromolecular_complex).
class_slot(macromolecular_complex, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, macromolecular_complex).
range_in(increases_mutation_rate_of, genomic_entity, macromolecular_complex).
class_slot(macromolecular_complex, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, macromolecular_complex).
range_in(decreases_mutation_rate_of, genomic_entity, macromolecular_complex).
class_slot(macromolecular_complex, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, macromolecular_complex).
range_in(affects_response_to, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, macromolecular_complex).
range_in(increases_response_to, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, macromolecular_complex).
range_in(decreases_response_to, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, macromolecular_complex).
range_in(affects_splicing_of, transcript, macromolecular_complex).
class_slot(macromolecular_complex, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, macromolecular_complex).
range_in(increases_splicing_of, transcript, macromolecular_complex).
class_slot(macromolecular_complex, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, macromolecular_complex).
range_in(decreases_splicing_of, transcript, macromolecular_complex).
class_slot(macromolecular_complex, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, macromolecular_complex).
range_in(affects_stability_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, macromolecular_complex).
range_in(increases_stability_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, macromolecular_complex).
range_in(decreases_stability_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, macromolecular_complex).
range_in(affects_transport_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, macromolecular_complex).
range_in(increases_transport_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, macromolecular_complex).
range_in(decreases_transport_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, macromolecular_complex).
range_in(affects_secretion_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, macromolecular_complex).
range_in(increases_secretion_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, macromolecular_complex).
range_in(decreases_secretion_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, macromolecular_complex).
range_in(affects_uptake_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, macromolecular_complex).
range_in(increases_uptake_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, macromolecular_complex).
range_in(decreases_uptake_of, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, macromolecular_complex).
range_in(regulates_entity_to_entity, molecular_entity, macromolecular_complex).
class_slot(macromolecular_complex, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, macromolecular_complex).
range_in(biomarker_for, disease_or_phenotypic_feature, macromolecular_complex).
class_slot(macromolecular_complex, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, macromolecular_complex).
range_in(in_taxon, organism_taxon, macromolecular_complex).
class_slot(macromolecular_complex, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, macromolecular_complex).
class(macromolecular_machine).
is_a(macromolecular_machine, genomic_entity).
has_uri(macromolecular_machine, 'http://w3id.org/biolink/vocab/MacromolecularMachine').
class_slot(macromolecular_machine, id).
required(id).
slotrange(identifier_type).
required_in(id, macromolecular_machine).
range_in(id, identifier_type, macromolecular_machine).
class_slot(macromolecular_machine, name).
required(name).
slotrange(symbol_type).
range_in(name, symbol_type, macromolecular_machine).
class_slot(macromolecular_machine, category).
required(category).
slotrange(iri_type).
multivalued_in(category, macromolecular_machine).
range_in(category, iri_type, macromolecular_machine).
class_slot(macromolecular_machine, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, macromolecular_machine).
range_in(related_to, named_thing, macromolecular_machine).
class_slot(macromolecular_machine, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, macromolecular_machine).
range_in(interacts_with, named_thing, macromolecular_machine).
class_slot(macromolecular_machine, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, macromolecular_machine).
class_slot(macromolecular_machine, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, macromolecular_machine).
class_slot(macromolecular_machine, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, macromolecular_machine).
range_in(synonym, label_type, macromolecular_machine).
class_slot(macromolecular_machine, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, macromolecular_machine).
class_slot(macromolecular_machine, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, macromolecular_machine).
class_slot(macromolecular_machine, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, macromolecular_machine).
class_slot(macromolecular_machine, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, macromolecular_machine).
range_in(has_phenotype, phenotypic_feature, macromolecular_machine).
class_slot(macromolecular_machine, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, macromolecular_machine).
range_in(molecularly_interacts_with, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, macromolecular_machine).
range_in(affects_abundance_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, macromolecular_machine).
range_in(increases_abundance_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, macromolecular_machine).
range_in(decreases_abundance_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, macromolecular_machine).
range_in(affects_activity_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, macromolecular_machine).
range_in(increases_activity_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, macromolecular_machine).
range_in(decreases_activity_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, macromolecular_machine).
range_in(affects_expression_of, genomic_entity, macromolecular_machine).
class_slot(macromolecular_machine, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, macromolecular_machine).
range_in(increases_expression_of, genomic_entity, macromolecular_machine).
class_slot(macromolecular_machine, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, macromolecular_machine).
range_in(decreases_expression_of, genomic_entity, macromolecular_machine).
class_slot(macromolecular_machine, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, macromolecular_machine).
range_in(affects_folding_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, macromolecular_machine).
range_in(increases_folding_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, macromolecular_machine).
range_in(decreases_folding_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, macromolecular_machine).
range_in(affects_localization_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, macromolecular_machine).
range_in(increases_localization_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, macromolecular_machine).
range_in(decreases_localization_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, macromolecular_machine).
range_in(affects_metabolic_processing_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, macromolecular_machine).
range_in(increases_metabolic_processing_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, macromolecular_machine).
range_in(decreases_metabolic_processing_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, macromolecular_machine).
range_in(affects_molecular_modification_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, macromolecular_machine).
range_in(increases_molecular_modification_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, macromolecular_machine).
range_in(decreases_molecular_modification_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, macromolecular_machine).
range_in(affects_synthesis_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, macromolecular_machine).
range_in(increases_synthesis_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, macromolecular_machine).
range_in(decreases_synthesis_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, macromolecular_machine).
range_in(affects_degradation_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, macromolecular_machine).
range_in(increases_degradation_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, macromolecular_machine).
range_in(decreases_degradation_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, macromolecular_machine).
range_in(affects_mutation_rate_of, genomic_entity, macromolecular_machine).
class_slot(macromolecular_machine, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, macromolecular_machine).
range_in(increases_mutation_rate_of, genomic_entity, macromolecular_machine).
class_slot(macromolecular_machine, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, macromolecular_machine).
range_in(decreases_mutation_rate_of, genomic_entity, macromolecular_machine).
class_slot(macromolecular_machine, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, macromolecular_machine).
range_in(affects_response_to, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, macromolecular_machine).
range_in(increases_response_to, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, macromolecular_machine).
range_in(decreases_response_to, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, macromolecular_machine).
range_in(affects_splicing_of, transcript, macromolecular_machine).
class_slot(macromolecular_machine, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, macromolecular_machine).
range_in(increases_splicing_of, transcript, macromolecular_machine).
class_slot(macromolecular_machine, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, macromolecular_machine).
range_in(decreases_splicing_of, transcript, macromolecular_machine).
class_slot(macromolecular_machine, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, macromolecular_machine).
range_in(affects_stability_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, macromolecular_machine).
range_in(increases_stability_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, macromolecular_machine).
range_in(decreases_stability_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, macromolecular_machine).
range_in(affects_transport_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, macromolecular_machine).
range_in(increases_transport_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, macromolecular_machine).
range_in(decreases_transport_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, macromolecular_machine).
range_in(affects_secretion_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, macromolecular_machine).
range_in(increases_secretion_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, macromolecular_machine).
range_in(decreases_secretion_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, macromolecular_machine).
range_in(affects_uptake_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, macromolecular_machine).
range_in(increases_uptake_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, macromolecular_machine).
range_in(decreases_uptake_of, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, macromolecular_machine).
range_in(regulates_entity_to_entity, molecular_entity, macromolecular_machine).
class_slot(macromolecular_machine, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, macromolecular_machine).
range_in(biomarker_for, disease_or_phenotypic_feature, macromolecular_machine).
class_slot(macromolecular_machine, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, macromolecular_machine).
range_in(in_taxon, organism_taxon, macromolecular_machine).
class_slot(macromolecular_machine, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, macromolecular_machine).
class(macromolecular_machine_to_biological_process_association).
is_a(macromolecular_machine_to_biological_process_association, functional_association).
has_uri(macromolecular_machine_to_biological_process_association, 'http://w3id.org/biolink/vocab/MacromolecularMachineToBiologicalProcessAssociation').
class_slot(macromolecular_machine_to_biological_process_association, id).
required(id).
slotrange(identifier_type).
required_in(id, macromolecular_machine_to_biological_process_association).
range_in(id, identifier_type, macromolecular_machine_to_biological_process_association).
class_slot(macromolecular_machine_to_biological_process_association, subject).
required(subject).
slotrange(macromolecular_machine).
required_in(subject, macromolecular_machine_to_biological_process_association).
range_in(subject, macromolecular_machine, macromolecular_machine_to_biological_process_association).
class_slot(macromolecular_machine_to_biological_process_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, macromolecular_machine_to_biological_process_association).
range_in(relation, iri_type, macromolecular_machine_to_biological_process_association).
class_slot(macromolecular_machine_to_biological_process_association, object).
required(object).
slotrange(biological_process).
required_in(object, macromolecular_machine_to_biological_process_association).
range_in(object, biological_process, macromolecular_machine_to_biological_process_association).
class_slot(macromolecular_machine_to_biological_process_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, macromolecular_machine_to_biological_process_association).
class_slot(macromolecular_machine_to_biological_process_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, macromolecular_machine_to_biological_process_association).
class_slot(macromolecular_machine_to_biological_process_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, macromolecular_machine_to_biological_process_association).
range_in(qualifiers, ontology_class, macromolecular_machine_to_biological_process_association).
class_slot(macromolecular_machine_to_biological_process_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, macromolecular_machine_to_biological_process_association).
range_in(publications, publication, macromolecular_machine_to_biological_process_association).
class_slot(macromolecular_machine_to_biological_process_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, macromolecular_machine_to_biological_process_association).
class_slot(macromolecular_machine_to_biological_process_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, macromolecular_machine_to_biological_process_association).
class(macromolecular_machine_to_cellular_component_association).
is_a(macromolecular_machine_to_cellular_component_association, functional_association).
has_uri(macromolecular_machine_to_cellular_component_association, 'http://w3id.org/biolink/vocab/MacromolecularMachineToCellularComponentAssociation').
class_slot(macromolecular_machine_to_cellular_component_association, id).
required(id).
slotrange(identifier_type).
required_in(id, macromolecular_machine_to_cellular_component_association).
range_in(id, identifier_type, macromolecular_machine_to_cellular_component_association).
class_slot(macromolecular_machine_to_cellular_component_association, subject).
required(subject).
slotrange(macromolecular_machine).
required_in(subject, macromolecular_machine_to_cellular_component_association).
range_in(subject, macromolecular_machine, macromolecular_machine_to_cellular_component_association).
class_slot(macromolecular_machine_to_cellular_component_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, macromolecular_machine_to_cellular_component_association).
range_in(relation, iri_type, macromolecular_machine_to_cellular_component_association).
class_slot(macromolecular_machine_to_cellular_component_association, object).
required(object).
slotrange(cellular_component).
required_in(object, macromolecular_machine_to_cellular_component_association).
range_in(object, cellular_component, macromolecular_machine_to_cellular_component_association).
class_slot(macromolecular_machine_to_cellular_component_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, macromolecular_machine_to_cellular_component_association).
class_slot(macromolecular_machine_to_cellular_component_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, macromolecular_machine_to_cellular_component_association).
class_slot(macromolecular_machine_to_cellular_component_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, macromolecular_machine_to_cellular_component_association).
range_in(qualifiers, ontology_class, macromolecular_machine_to_cellular_component_association).
class_slot(macromolecular_machine_to_cellular_component_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, macromolecular_machine_to_cellular_component_association).
range_in(publications, publication, macromolecular_machine_to_cellular_component_association).
class_slot(macromolecular_machine_to_cellular_component_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, macromolecular_machine_to_cellular_component_association).
class_slot(macromolecular_machine_to_cellular_component_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, macromolecular_machine_to_cellular_component_association).
class(macromolecular_machine_to_molecular_activity_association).
is_a(macromolecular_machine_to_molecular_activity_association, functional_association).
has_uri(macromolecular_machine_to_molecular_activity_association, 'http://w3id.org/biolink/vocab/MacromolecularMachineToMolecularActivityAssociation').
class_slot(macromolecular_machine_to_molecular_activity_association, id).
required(id).
slotrange(identifier_type).
required_in(id, macromolecular_machine_to_molecular_activity_association).
range_in(id, identifier_type, macromolecular_machine_to_molecular_activity_association).
class_slot(macromolecular_machine_to_molecular_activity_association, subject).
required(subject).
slotrange(macromolecular_machine).
required_in(subject, macromolecular_machine_to_molecular_activity_association).
range_in(subject, macromolecular_machine, macromolecular_machine_to_molecular_activity_association).
class_slot(macromolecular_machine_to_molecular_activity_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, macromolecular_machine_to_molecular_activity_association).
range_in(relation, iri_type, macromolecular_machine_to_molecular_activity_association).
class_slot(macromolecular_machine_to_molecular_activity_association, object).
required(object).
slotrange(molecular_activity).
required_in(object, macromolecular_machine_to_molecular_activity_association).
range_in(object, molecular_activity, macromolecular_machine_to_molecular_activity_association).
class_slot(macromolecular_machine_to_molecular_activity_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, macromolecular_machine_to_molecular_activity_association).
class_slot(macromolecular_machine_to_molecular_activity_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, macromolecular_machine_to_molecular_activity_association).
class_slot(macromolecular_machine_to_molecular_activity_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, macromolecular_machine_to_molecular_activity_association).
range_in(qualifiers, ontology_class, macromolecular_machine_to_molecular_activity_association).
class_slot(macromolecular_machine_to_molecular_activity_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, macromolecular_machine_to_molecular_activity_association).
range_in(publications, publication, macromolecular_machine_to_molecular_activity_association).
class_slot(macromolecular_machine_to_molecular_activity_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, macromolecular_machine_to_molecular_activity_association).
class_slot(macromolecular_machine_to_molecular_activity_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, macromolecular_machine_to_molecular_activity_association).
class(metabolite).
is_a(metabolite, chemical_substance).
has_uri(metabolite, 'http://w3id.org/biolink/vocab/Metabolite').
class_slot(metabolite, id).
required(id).
slotrange(identifier_type).
required_in(id, metabolite).
range_in(id, identifier_type, metabolite).
class_slot(metabolite, name).
required(name).
slotrange(label_type).
range_in(name, label_type, metabolite).
class_slot(metabolite, category).
required(category).
slotrange(iri_type).
multivalued_in(category, metabolite).
range_in(category, iri_type, metabolite).
class_slot(metabolite, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, metabolite).
range_in(related_to, named_thing, metabolite).
class_slot(metabolite, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, metabolite).
range_in(interacts_with, named_thing, metabolite).
class_slot(metabolite, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, metabolite).
class_slot(metabolite, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, metabolite).
class_slot(metabolite, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, metabolite).
range_in(synonym, label_type, metabolite).
class_slot(metabolite, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, metabolite).
class_slot(metabolite, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, metabolite).
class_slot(metabolite, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, metabolite).
class_slot(metabolite, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, metabolite).
range_in(has_phenotype, phenotypic_feature, metabolite).
class_slot(metabolite, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, metabolite).
range_in(molecularly_interacts_with, molecular_entity, metabolite).
class_slot(metabolite, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, metabolite).
range_in(affects_abundance_of, molecular_entity, metabolite).
class_slot(metabolite, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, metabolite).
range_in(increases_abundance_of, molecular_entity, metabolite).
class_slot(metabolite, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, metabolite).
range_in(decreases_abundance_of, molecular_entity, metabolite).
class_slot(metabolite, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, metabolite).
range_in(affects_activity_of, molecular_entity, metabolite).
class_slot(metabolite, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, metabolite).
range_in(increases_activity_of, molecular_entity, metabolite).
class_slot(metabolite, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, metabolite).
range_in(decreases_activity_of, molecular_entity, metabolite).
class_slot(metabolite, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, metabolite).
range_in(affects_expression_of, genomic_entity, metabolite).
class_slot(metabolite, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, metabolite).
range_in(increases_expression_of, genomic_entity, metabolite).
class_slot(metabolite, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, metabolite).
range_in(decreases_expression_of, genomic_entity, metabolite).
class_slot(metabolite, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, metabolite).
range_in(affects_folding_of, molecular_entity, metabolite).
class_slot(metabolite, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, metabolite).
range_in(increases_folding_of, molecular_entity, metabolite).
class_slot(metabolite, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, metabolite).
range_in(decreases_folding_of, molecular_entity, metabolite).
class_slot(metabolite, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, metabolite).
range_in(affects_localization_of, molecular_entity, metabolite).
class_slot(metabolite, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, metabolite).
range_in(increases_localization_of, molecular_entity, metabolite).
class_slot(metabolite, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, metabolite).
range_in(decreases_localization_of, molecular_entity, metabolite).
class_slot(metabolite, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, metabolite).
range_in(affects_metabolic_processing_of, molecular_entity, metabolite).
class_slot(metabolite, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, metabolite).
range_in(increases_metabolic_processing_of, molecular_entity, metabolite).
class_slot(metabolite, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, metabolite).
range_in(decreases_metabolic_processing_of, molecular_entity, metabolite).
class_slot(metabolite, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, metabolite).
range_in(affects_molecular_modification_of, molecular_entity, metabolite).
class_slot(metabolite, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, metabolite).
range_in(increases_molecular_modification_of, molecular_entity, metabolite).
class_slot(metabolite, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, metabolite).
range_in(decreases_molecular_modification_of, molecular_entity, metabolite).
class_slot(metabolite, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, metabolite).
range_in(affects_synthesis_of, molecular_entity, metabolite).
class_slot(metabolite, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, metabolite).
range_in(increases_synthesis_of, molecular_entity, metabolite).
class_slot(metabolite, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, metabolite).
range_in(decreases_synthesis_of, molecular_entity, metabolite).
class_slot(metabolite, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, metabolite).
range_in(affects_degradation_of, molecular_entity, metabolite).
class_slot(metabolite, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, metabolite).
range_in(increases_degradation_of, molecular_entity, metabolite).
class_slot(metabolite, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, metabolite).
range_in(decreases_degradation_of, molecular_entity, metabolite).
class_slot(metabolite, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, metabolite).
range_in(affects_mutation_rate_of, genomic_entity, metabolite).
class_slot(metabolite, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, metabolite).
range_in(increases_mutation_rate_of, genomic_entity, metabolite).
class_slot(metabolite, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, metabolite).
range_in(decreases_mutation_rate_of, genomic_entity, metabolite).
class_slot(metabolite, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, metabolite).
range_in(affects_response_to, molecular_entity, metabolite).
class_slot(metabolite, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, metabolite).
range_in(increases_response_to, molecular_entity, metabolite).
class_slot(metabolite, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, metabolite).
range_in(decreases_response_to, molecular_entity, metabolite).
class_slot(metabolite, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, metabolite).
range_in(affects_splicing_of, transcript, metabolite).
class_slot(metabolite, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, metabolite).
range_in(increases_splicing_of, transcript, metabolite).
class_slot(metabolite, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, metabolite).
range_in(decreases_splicing_of, transcript, metabolite).
class_slot(metabolite, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, metabolite).
range_in(affects_stability_of, molecular_entity, metabolite).
class_slot(metabolite, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, metabolite).
range_in(increases_stability_of, molecular_entity, metabolite).
class_slot(metabolite, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, metabolite).
range_in(decreases_stability_of, molecular_entity, metabolite).
class_slot(metabolite, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, metabolite).
range_in(affects_transport_of, molecular_entity, metabolite).
class_slot(metabolite, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, metabolite).
range_in(increases_transport_of, molecular_entity, metabolite).
class_slot(metabolite, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, metabolite).
range_in(decreases_transport_of, molecular_entity, metabolite).
class_slot(metabolite, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, metabolite).
range_in(affects_secretion_of, molecular_entity, metabolite).
class_slot(metabolite, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, metabolite).
range_in(increases_secretion_of, molecular_entity, metabolite).
class_slot(metabolite, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, metabolite).
range_in(decreases_secretion_of, molecular_entity, metabolite).
class_slot(metabolite, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, metabolite).
range_in(affects_uptake_of, molecular_entity, metabolite).
class_slot(metabolite, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, metabolite).
range_in(increases_uptake_of, molecular_entity, metabolite).
class_slot(metabolite, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, metabolite).
range_in(decreases_uptake_of, molecular_entity, metabolite).
class_slot(metabolite, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, metabolite).
range_in(regulates_entity_to_entity, molecular_entity, metabolite).
class_slot(metabolite, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, metabolite).
range_in(biomarker_for, disease_or_phenotypic_feature, metabolite).
class_slot(metabolite, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, metabolite).
range_in(in_taxon, organism_taxon, metabolite).
class(microRNA).
is_a(microRNA, noncoding_RNA_product).
has_uri(microRNA, 'http://w3id.org/biolink/vocab/MicroRNA').
class_slot(microRNA, id).
required(id).
slotrange(identifier_type).
required_in(id, microRNA).
range_in(id, identifier_type, microRNA).
class_slot(microRNA, name).
required(name).
slotrange(symbol_type).
range_in(name, symbol_type, microRNA).
class_slot(microRNA, category).
required(category).
slotrange(iri_type).
multivalued_in(category, microRNA).
range_in(category, iri_type, microRNA).
class_slot(microRNA, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, microRNA).
range_in(related_to, named_thing, microRNA).
class_slot(microRNA, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, microRNA).
range_in(interacts_with, named_thing, microRNA).
class_slot(microRNA, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, microRNA).
class_slot(microRNA, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, microRNA).
class_slot(microRNA, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, microRNA).
range_in(synonym, label_type, microRNA).
class_slot(microRNA, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, microRNA).
class_slot(microRNA, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, microRNA).
class_slot(microRNA, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, microRNA).
class_slot(microRNA, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, microRNA).
range_in(has_phenotype, phenotypic_feature, microRNA).
class_slot(microRNA, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, microRNA).
range_in(molecularly_interacts_with, molecular_entity, microRNA).
class_slot(microRNA, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, microRNA).
range_in(affects_abundance_of, molecular_entity, microRNA).
class_slot(microRNA, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, microRNA).
range_in(increases_abundance_of, molecular_entity, microRNA).
class_slot(microRNA, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, microRNA).
range_in(decreases_abundance_of, molecular_entity, microRNA).
class_slot(microRNA, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, microRNA).
range_in(affects_activity_of, molecular_entity, microRNA).
class_slot(microRNA, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, microRNA).
range_in(increases_activity_of, molecular_entity, microRNA).
class_slot(microRNA, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, microRNA).
range_in(decreases_activity_of, molecular_entity, microRNA).
class_slot(microRNA, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, microRNA).
range_in(affects_expression_of, genomic_entity, microRNA).
class_slot(microRNA, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, microRNA).
range_in(increases_expression_of, genomic_entity, microRNA).
class_slot(microRNA, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, microRNA).
range_in(decreases_expression_of, genomic_entity, microRNA).
class_slot(microRNA, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, microRNA).
range_in(affects_folding_of, molecular_entity, microRNA).
class_slot(microRNA, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, microRNA).
range_in(increases_folding_of, molecular_entity, microRNA).
class_slot(microRNA, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, microRNA).
range_in(decreases_folding_of, molecular_entity, microRNA).
class_slot(microRNA, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, microRNA).
range_in(affects_localization_of, molecular_entity, microRNA).
class_slot(microRNA, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, microRNA).
range_in(increases_localization_of, molecular_entity, microRNA).
class_slot(microRNA, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, microRNA).
range_in(decreases_localization_of, molecular_entity, microRNA).
class_slot(microRNA, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, microRNA).
range_in(affects_metabolic_processing_of, molecular_entity, microRNA).
class_slot(microRNA, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, microRNA).
range_in(increases_metabolic_processing_of, molecular_entity, microRNA).
class_slot(microRNA, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, microRNA).
range_in(decreases_metabolic_processing_of, molecular_entity, microRNA).
class_slot(microRNA, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, microRNA).
range_in(affects_molecular_modification_of, molecular_entity, microRNA).
class_slot(microRNA, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, microRNA).
range_in(increases_molecular_modification_of, molecular_entity, microRNA).
class_slot(microRNA, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, microRNA).
range_in(decreases_molecular_modification_of, molecular_entity, microRNA).
class_slot(microRNA, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, microRNA).
range_in(affects_synthesis_of, molecular_entity, microRNA).
class_slot(microRNA, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, microRNA).
range_in(increases_synthesis_of, molecular_entity, microRNA).
class_slot(microRNA, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, microRNA).
range_in(decreases_synthesis_of, molecular_entity, microRNA).
class_slot(microRNA, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, microRNA).
range_in(affects_degradation_of, molecular_entity, microRNA).
class_slot(microRNA, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, microRNA).
range_in(increases_degradation_of, molecular_entity, microRNA).
class_slot(microRNA, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, microRNA).
range_in(decreases_degradation_of, molecular_entity, microRNA).
class_slot(microRNA, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, microRNA).
range_in(affects_mutation_rate_of, genomic_entity, microRNA).
class_slot(microRNA, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, microRNA).
range_in(increases_mutation_rate_of, genomic_entity, microRNA).
class_slot(microRNA, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, microRNA).
range_in(decreases_mutation_rate_of, genomic_entity, microRNA).
class_slot(microRNA, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, microRNA).
range_in(affects_response_to, molecular_entity, microRNA).
class_slot(microRNA, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, microRNA).
range_in(increases_response_to, molecular_entity, microRNA).
class_slot(microRNA, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, microRNA).
range_in(decreases_response_to, molecular_entity, microRNA).
class_slot(microRNA, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, microRNA).
range_in(affects_splicing_of, transcript, microRNA).
class_slot(microRNA, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, microRNA).
range_in(increases_splicing_of, transcript, microRNA).
class_slot(microRNA, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, microRNA).
range_in(decreases_splicing_of, transcript, microRNA).
class_slot(microRNA, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, microRNA).
range_in(affects_stability_of, molecular_entity, microRNA).
class_slot(microRNA, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, microRNA).
range_in(increases_stability_of, molecular_entity, microRNA).
class_slot(microRNA, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, microRNA).
range_in(decreases_stability_of, molecular_entity, microRNA).
class_slot(microRNA, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, microRNA).
range_in(affects_transport_of, molecular_entity, microRNA).
class_slot(microRNA, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, microRNA).
range_in(increases_transport_of, molecular_entity, microRNA).
class_slot(microRNA, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, microRNA).
range_in(decreases_transport_of, molecular_entity, microRNA).
class_slot(microRNA, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, microRNA).
range_in(affects_secretion_of, molecular_entity, microRNA).
class_slot(microRNA, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, microRNA).
range_in(increases_secretion_of, molecular_entity, microRNA).
class_slot(microRNA, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, microRNA).
range_in(decreases_secretion_of, molecular_entity, microRNA).
class_slot(microRNA, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, microRNA).
range_in(affects_uptake_of, molecular_entity, microRNA).
class_slot(microRNA, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, microRNA).
range_in(increases_uptake_of, molecular_entity, microRNA).
class_slot(microRNA, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, microRNA).
range_in(decreases_uptake_of, molecular_entity, microRNA).
class_slot(microRNA, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, microRNA).
range_in(regulates_entity_to_entity, molecular_entity, microRNA).
class_slot(microRNA, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, microRNA).
range_in(biomarker_for, disease_or_phenotypic_feature, microRNA).
class_slot(microRNA, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, microRNA).
range_in(in_taxon, organism_taxon, microRNA).
class_slot(microRNA, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, microRNA).
class_slot(microRNA, in_pathway_with).
required(in_pathway_with).
slotrange(gene_or_gene_product).
multivalued_in(in_pathway_with, microRNA).
range_in(in_pathway_with, gene_or_gene_product, microRNA).
class_slot(microRNA, in_complex_with).
required(in_complex_with).
slotrange(gene_or_gene_product).
multivalued_in(in_complex_with, microRNA).
range_in(in_complex_with, gene_or_gene_product, microRNA).
class_slot(microRNA, in_cell_population_with).
required(in_cell_population_with).
slotrange(gene_or_gene_product).
multivalued_in(in_cell_population_with, microRNA).
range_in(in_cell_population_with, gene_or_gene_product, microRNA).
class_slot(microRNA, expressed_in).
required(expressed_in).
slotrange(anatomical_entity).
multivalued_in(expressed_in, microRNA).
range_in(expressed_in, anatomical_entity, microRNA).
class(model_to_disease_mixin).
has_uri(model_to_disease_mixin, 'http://w3id.org/biolink/vocab/ModelToDiseaseMixin').
class_slot(model_to_disease_mixin, subject).
required(subject).
slotrange(iri_type).
required_in(subject, model_to_disease_mixin).
range_in(subject, iri_type, model_to_disease_mixin).
class_slot(model_to_disease_mixin, relation).
required(relation).
slotrange(iri_type).
required_in(relation, model_to_disease_mixin).
range_in(relation, iri_type, model_to_disease_mixin).
class(molecular_activity).
mixin(molecular_activity, occurrent).
is_a(molecular_activity, biological_process_or_activity).
has_uri(molecular_activity, 'http://w3id.org/biolink/vocab/MolecularActivity').
class_slot(molecular_activity, id).
required(id).
slotrange(identifier_type).
required_in(id, molecular_activity).
range_in(id, identifier_type, molecular_activity).
class_slot(molecular_activity, name).
required(name).
slotrange(label_type).
range_in(name, label_type, molecular_activity).
class_slot(molecular_activity, category).
required(category).
slotrange(iri_type).
multivalued_in(category, molecular_activity).
range_in(category, iri_type, molecular_activity).
class_slot(molecular_activity, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, molecular_activity).
range_in(related_to, named_thing, molecular_activity).
class_slot(molecular_activity, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, molecular_activity).
range_in(interacts_with, named_thing, molecular_activity).
class_slot(molecular_activity, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, molecular_activity).
class_slot(molecular_activity, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, molecular_activity).
class_slot(molecular_activity, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, molecular_activity).
range_in(synonym, label_type, molecular_activity).
class_slot(molecular_activity, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, molecular_activity).
class_slot(molecular_activity, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, molecular_activity).
class_slot(molecular_activity, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, molecular_activity).
class_slot(molecular_activity, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, molecular_activity).
range_in(has_phenotype, phenotypic_feature, molecular_activity).
class_slot(molecular_activity, regulates_process_to_process).
required(regulates_process_to_process).
slotrange(occurrent).
multivalued_in(regulates_process_to_process, molecular_activity).
range_in(regulates_process_to_process, occurrent, molecular_activity).
class_slot(molecular_activity, has_participant).
required(has_participant).
slotrange(named_thing).
multivalued_in(has_participant, molecular_activity).
range_in(has_participant, named_thing, molecular_activity).
class_slot(molecular_activity, has_input).
required(has_input).
slotrange(named_thing).
multivalued_in(has_input, molecular_activity).
range_in(has_input, named_thing, molecular_activity).
class_slot(molecular_activity, precedes).
required(precedes).
slotrange(occurrent).
multivalued_in(precedes, molecular_activity).
range_in(precedes, occurrent, molecular_activity).
class(molecular_entity).
mixin(molecular_entity, thing_with_taxon).
is_a(molecular_entity, biological_entity).
has_uri(molecular_entity, 'http://w3id.org/biolink/vocab/MolecularEntity').
class_slot(molecular_entity, id).
required(id).
slotrange(identifier_type).
required_in(id, molecular_entity).
range_in(id, identifier_type, molecular_entity).
class_slot(molecular_entity, name).
required(name).
slotrange(label_type).
range_in(name, label_type, molecular_entity).
class_slot(molecular_entity, category).
required(category).
slotrange(iri_type).
multivalued_in(category, molecular_entity).
range_in(category, iri_type, molecular_entity).
class_slot(molecular_entity, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, molecular_entity).
range_in(related_to, named_thing, molecular_entity).
class_slot(molecular_entity, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, molecular_entity).
range_in(interacts_with, named_thing, molecular_entity).
class_slot(molecular_entity, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, molecular_entity).
class_slot(molecular_entity, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, molecular_entity).
class_slot(molecular_entity, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, molecular_entity).
range_in(synonym, label_type, molecular_entity).
class_slot(molecular_entity, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, molecular_entity).
class_slot(molecular_entity, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, molecular_entity).
class_slot(molecular_entity, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, molecular_entity).
class_slot(molecular_entity, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, molecular_entity).
range_in(has_phenotype, phenotypic_feature, molecular_entity).
class_slot(molecular_entity, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, molecular_entity).
range_in(molecularly_interacts_with, molecular_entity, molecular_entity).
class_slot(molecular_entity, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, molecular_entity).
range_in(affects_abundance_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, molecular_entity).
range_in(increases_abundance_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, molecular_entity).
range_in(decreases_abundance_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, molecular_entity).
range_in(affects_activity_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, molecular_entity).
range_in(increases_activity_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, molecular_entity).
range_in(decreases_activity_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, molecular_entity).
range_in(affects_expression_of, genomic_entity, molecular_entity).
class_slot(molecular_entity, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, molecular_entity).
range_in(increases_expression_of, genomic_entity, molecular_entity).
class_slot(molecular_entity, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, molecular_entity).
range_in(decreases_expression_of, genomic_entity, molecular_entity).
class_slot(molecular_entity, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, molecular_entity).
range_in(affects_folding_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, molecular_entity).
range_in(increases_folding_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, molecular_entity).
range_in(decreases_folding_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, molecular_entity).
range_in(affects_localization_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, molecular_entity).
range_in(increases_localization_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, molecular_entity).
range_in(decreases_localization_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, molecular_entity).
range_in(affects_metabolic_processing_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, molecular_entity).
range_in(increases_metabolic_processing_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, molecular_entity).
range_in(decreases_metabolic_processing_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, molecular_entity).
range_in(affects_molecular_modification_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, molecular_entity).
range_in(increases_molecular_modification_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, molecular_entity).
range_in(decreases_molecular_modification_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, molecular_entity).
range_in(affects_synthesis_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, molecular_entity).
range_in(increases_synthesis_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, molecular_entity).
range_in(decreases_synthesis_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, molecular_entity).
range_in(affects_degradation_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, molecular_entity).
range_in(increases_degradation_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, molecular_entity).
range_in(decreases_degradation_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, molecular_entity).
range_in(affects_mutation_rate_of, genomic_entity, molecular_entity).
class_slot(molecular_entity, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, molecular_entity).
range_in(increases_mutation_rate_of, genomic_entity, molecular_entity).
class_slot(molecular_entity, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, molecular_entity).
range_in(decreases_mutation_rate_of, genomic_entity, molecular_entity).
class_slot(molecular_entity, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, molecular_entity).
range_in(affects_response_to, molecular_entity, molecular_entity).
class_slot(molecular_entity, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, molecular_entity).
range_in(increases_response_to, molecular_entity, molecular_entity).
class_slot(molecular_entity, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, molecular_entity).
range_in(decreases_response_to, molecular_entity, molecular_entity).
class_slot(molecular_entity, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, molecular_entity).
range_in(affects_splicing_of, transcript, molecular_entity).
class_slot(molecular_entity, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, molecular_entity).
range_in(increases_splicing_of, transcript, molecular_entity).
class_slot(molecular_entity, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, molecular_entity).
range_in(decreases_splicing_of, transcript, molecular_entity).
class_slot(molecular_entity, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, molecular_entity).
range_in(affects_stability_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, molecular_entity).
range_in(increases_stability_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, molecular_entity).
range_in(decreases_stability_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, molecular_entity).
range_in(affects_transport_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, molecular_entity).
range_in(increases_transport_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, molecular_entity).
range_in(decreases_transport_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, molecular_entity).
range_in(affects_secretion_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, molecular_entity).
range_in(increases_secretion_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, molecular_entity).
range_in(decreases_secretion_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, molecular_entity).
range_in(affects_uptake_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, molecular_entity).
range_in(increases_uptake_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, molecular_entity).
range_in(decreases_uptake_of, molecular_entity, molecular_entity).
class_slot(molecular_entity, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, molecular_entity).
range_in(regulates_entity_to_entity, molecular_entity, molecular_entity).
class_slot(molecular_entity, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, molecular_entity).
range_in(biomarker_for, disease_or_phenotypic_feature, molecular_entity).
class_slot(molecular_entity, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, molecular_entity).
range_in(in_taxon, organism_taxon, molecular_entity).
class_slot(molecular_entity, positively_regulates_entity_to_entity).
required(positively_regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(positively_regulates_entity_to_entity, molecular_entity).
range_in(positively_regulates_entity_to_entity, molecular_entity, molecular_entity).
class_slot(molecular_entity, negatively_regulates_entity_to_entity).
required(negatively_regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(negatively_regulates_entity_to_entity, molecular_entity).
range_in(negatively_regulates_entity_to_entity, molecular_entity, molecular_entity).
class(named_thing).
has_uri(named_thing, 'http://w3id.org/biolink/vocab/NamedThing').
class_slot(named_thing, id).
required(id).
slotrange(identifier_type).
required_in(id, named_thing).
range_in(id, identifier_type, named_thing).
class_slot(named_thing, name).
required(name).
slotrange(label_type).
range_in(name, label_type, named_thing).
class_slot(named_thing, category).
required(category).
slotrange(iri_type).
multivalued_in(category, named_thing).
range_in(category, iri_type, named_thing).
class_slot(named_thing, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, named_thing).
range_in(related_to, named_thing, named_thing).
class_slot(named_thing, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, named_thing).
range_in(interacts_with, named_thing, named_thing).
class_slot(named_thing, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, named_thing).
class_slot(named_thing, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, named_thing).
class_slot(named_thing, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, named_thing).
range_in(synonym, label_type, named_thing).
class_slot(named_thing, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, named_thing).
class_slot(named_thing, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, named_thing).
class_slot(named_thing, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, named_thing).
class_slot(named_thing, physically_interacts_with).
required(physically_interacts_with).
slotrange(named_thing).
multivalued_in(physically_interacts_with, named_thing).
range_in(physically_interacts_with, named_thing, named_thing).
class_slot(named_thing, affects).
required(affects).
slotrange(named_thing).
multivalued_in(affects, named_thing).
range_in(affects, named_thing, named_thing).
class_slot(named_thing, regulates).
required(regulates).
slotrange(named_thing).
multivalued_in(regulates, named_thing).
range_in(regulates, named_thing, named_thing).
class_slot(named_thing, positively_regulates).
required(positively_regulates).
slotrange(named_thing).
multivalued_in(positively_regulates, named_thing).
range_in(positively_regulates, named_thing, named_thing).
class_slot(named_thing, negatively_regulates).
required(negatively_regulates).
slotrange(named_thing).
multivalued_in(negatively_regulates, named_thing).
range_in(negatively_regulates, named_thing, named_thing).
class_slot(named_thing, disrupts).
required(disrupts).
slotrange(named_thing).
multivalued_in(disrupts, named_thing).
range_in(disrupts, named_thing, named_thing).
class_slot(named_thing, homologous_to).
required(homologous_to).
slotrange(named_thing).
multivalued_in(homologous_to, named_thing).
range_in(homologous_to, named_thing, named_thing).
class_slot(named_thing, paralogous_to).
required(paralogous_to).
slotrange(named_thing).
multivalued_in(paralogous_to, named_thing).
range_in(paralogous_to, named_thing, named_thing).
class_slot(named_thing, orthologous_to).
required(orthologous_to).
slotrange(named_thing).
multivalued_in(orthologous_to, named_thing).
range_in(orthologous_to, named_thing, named_thing).
class_slot(named_thing, xenologous_to).
required(xenologous_to).
slotrange(named_thing).
multivalued_in(xenologous_to, named_thing).
range_in(xenologous_to, named_thing, named_thing).
class_slot(named_thing, coexists_with).
required(coexists_with).
slotrange(named_thing).
multivalued_in(coexists_with, named_thing).
range_in(coexists_with, named_thing, named_thing).
class_slot(named_thing, colocalizes_with).
required(colocalizes_with).
slotrange(named_thing).
multivalued_in(colocalizes_with, named_thing).
range_in(colocalizes_with, named_thing, named_thing).
class_slot(named_thing, affects_risk_for).
required(affects_risk_for).
slotrange(named_thing).
multivalued_in(affects_risk_for, named_thing).
range_in(affects_risk_for, named_thing, named_thing).
class_slot(named_thing, predisposes).
required(predisposes).
slotrange(named_thing).
multivalued_in(predisposes, named_thing).
range_in(predisposes, named_thing, named_thing).
class_slot(named_thing, contributes_to).
required(contributes_to).
slotrange(named_thing).
multivalued_in(contributes_to, named_thing).
range_in(contributes_to, named_thing, named_thing).
class_slot(named_thing, causes).
required(causes).
slotrange(named_thing).
multivalued_in(causes, named_thing).
range_in(causes, named_thing, named_thing).
class_slot(named_thing, prevents).
required(prevents).
slotrange(named_thing).
multivalued_in(prevents, named_thing).
range_in(prevents, named_thing, named_thing).
class_slot(named_thing, occurs_in).
required(occurs_in).
slotrange(named_thing).
multivalued_in(occurs_in, named_thing).
range_in(occurs_in, named_thing, named_thing).
class_slot(named_thing, located_in).
required(located_in).
slotrange(named_thing).
multivalued_in(located_in, named_thing).
range_in(located_in, named_thing, named_thing).
class_slot(named_thing, location_of).
required(location_of).
slotrange(named_thing).
multivalued_in(location_of, named_thing).
range_in(location_of, named_thing, named_thing).
class_slot(named_thing, model_of).
required(model_of).
slotrange(named_thing).
multivalued_in(model_of, named_thing).
range_in(model_of, named_thing, named_thing).
class_slot(named_thing, overlaps).
required(overlaps).
slotrange(named_thing).
multivalued_in(overlaps, named_thing).
range_in(overlaps, named_thing, named_thing).
class_slot(named_thing, has_part).
required(has_part).
slotrange(named_thing).
multivalued_in(has_part, named_thing).
range_in(has_part, named_thing, named_thing).
class_slot(named_thing, part_of).
required(part_of).
slotrange(named_thing).
multivalued_in(part_of, named_thing).
range_in(part_of, named_thing, named_thing).
class_slot(named_thing, participates_in).
required(participates_in).
slotrange(occurrent).
multivalued_in(participates_in, named_thing).
range_in(participates_in, occurrent, named_thing).
class_slot(named_thing, actively_involved_in).
required(actively_involved_in).
slotrange(occurrent).
multivalued_in(actively_involved_in, named_thing).
range_in(actively_involved_in, occurrent, named_thing).
class_slot(named_thing, capable_of).
required(capable_of).
slotrange(occurrent).
multivalued_in(capable_of, named_thing).
range_in(capable_of, occurrent, named_thing).
class_slot(named_thing, derives_into).
required(derives_into).
slotrange(named_thing).
multivalued_in(derives_into, named_thing).
range_in(derives_into, named_thing, named_thing).
class_slot(named_thing, derives_from).
required(derives_from).
slotrange(named_thing).
multivalued_in(derives_from, named_thing).
range_in(derives_from, named_thing, named_thing).
class_slot(named_thing, manifestation_of).
required(manifestation_of).
slotrange(disease).
multivalued_in(manifestation_of, named_thing).
range_in(manifestation_of, disease, named_thing).
class_slot(named_thing, produces).
required(produces).
slotrange(named_thing).
multivalued_in(produces, named_thing).
range_in(produces, named_thing, named_thing).
class_slot(named_thing, same_as).
required(same_as).
slotrange(named_thing).
multivalued_in(same_as, named_thing).
range_in(same_as, named_thing, named_thing).
class_slot(named_thing, creation_date).
required(creation_date).
slotrange(date).
range_in(creation_date, date, named_thing).
class_slot(named_thing, update_date).
required(update_date).
slotrange(date).
range_in(update_date, date, named_thing).
class_slot(named_thing, has_chemical_formula).
required(has_chemical_formula).
slotrange(chemical_formula_value).
range_in(has_chemical_formula, chemical_formula_value, named_thing).
class_slot(named_thing, aggregate_statistic).
required(aggregate_statistic).
slotrange(string).
range_in(aggregate_statistic, string, named_thing).
class_slot(named_thing, has_molecular_consequence).
required(has_molecular_consequence).
slotrange(ontology_class).
multivalued_in(has_molecular_consequence, named_thing).
range_in(has_molecular_consequence, ontology_class, named_thing).
class_slot(named_thing, filler).
required(filler).
slotrange(named_thing).
range_in(filler, named_thing, named_thing).
class_slot(named_thing, interbase_coordinate).
required(interbase_coordinate).
slotrange(string).
range_in(interbase_coordinate, string, named_thing).
class(noncoding_RNA_product).
is_a(noncoding_RNA_product, 'RNA_product').
has_uri(noncoding_RNA_product, 'http://w3id.org/biolink/vocab/NoncodingRNAProduct').
class_slot(noncoding_RNA_product, id).
required(id).
slotrange(identifier_type).
required_in(id, noncoding_RNA_product).
range_in(id, identifier_type, noncoding_RNA_product).
class_slot(noncoding_RNA_product, name).
required(name).
slotrange(symbol_type).
range_in(name, symbol_type, noncoding_RNA_product).
class_slot(noncoding_RNA_product, category).
required(category).
slotrange(iri_type).
multivalued_in(category, noncoding_RNA_product).
range_in(category, iri_type, noncoding_RNA_product).
class_slot(noncoding_RNA_product, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, noncoding_RNA_product).
range_in(related_to, named_thing, noncoding_RNA_product).
class_slot(noncoding_RNA_product, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, noncoding_RNA_product).
range_in(interacts_with, named_thing, noncoding_RNA_product).
class_slot(noncoding_RNA_product, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, noncoding_RNA_product).
class_slot(noncoding_RNA_product, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, noncoding_RNA_product).
class_slot(noncoding_RNA_product, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, noncoding_RNA_product).
range_in(synonym, label_type, noncoding_RNA_product).
class_slot(noncoding_RNA_product, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, noncoding_RNA_product).
class_slot(noncoding_RNA_product, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, noncoding_RNA_product).
class_slot(noncoding_RNA_product, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, noncoding_RNA_product).
class_slot(noncoding_RNA_product, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, noncoding_RNA_product).
range_in(has_phenotype, phenotypic_feature, noncoding_RNA_product).
class_slot(noncoding_RNA_product, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, noncoding_RNA_product).
range_in(molecularly_interacts_with, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, noncoding_RNA_product).
range_in(affects_abundance_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, noncoding_RNA_product).
range_in(increases_abundance_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, noncoding_RNA_product).
range_in(decreases_abundance_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, noncoding_RNA_product).
range_in(affects_activity_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, noncoding_RNA_product).
range_in(increases_activity_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, noncoding_RNA_product).
range_in(decreases_activity_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, noncoding_RNA_product).
range_in(affects_expression_of, genomic_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, noncoding_RNA_product).
range_in(increases_expression_of, genomic_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, noncoding_RNA_product).
range_in(decreases_expression_of, genomic_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, noncoding_RNA_product).
range_in(affects_folding_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, noncoding_RNA_product).
range_in(increases_folding_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, noncoding_RNA_product).
range_in(decreases_folding_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, noncoding_RNA_product).
range_in(affects_localization_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, noncoding_RNA_product).
range_in(increases_localization_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, noncoding_RNA_product).
range_in(decreases_localization_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, noncoding_RNA_product).
range_in(affects_metabolic_processing_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, noncoding_RNA_product).
range_in(increases_metabolic_processing_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, noncoding_RNA_product).
range_in(decreases_metabolic_processing_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, noncoding_RNA_product).
range_in(affects_molecular_modification_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, noncoding_RNA_product).
range_in(increases_molecular_modification_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, noncoding_RNA_product).
range_in(decreases_molecular_modification_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, noncoding_RNA_product).
range_in(affects_synthesis_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, noncoding_RNA_product).
range_in(increases_synthesis_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, noncoding_RNA_product).
range_in(decreases_synthesis_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, noncoding_RNA_product).
range_in(affects_degradation_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, noncoding_RNA_product).
range_in(increases_degradation_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, noncoding_RNA_product).
range_in(decreases_degradation_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, noncoding_RNA_product).
range_in(affects_mutation_rate_of, genomic_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, noncoding_RNA_product).
range_in(increases_mutation_rate_of, genomic_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, noncoding_RNA_product).
range_in(decreases_mutation_rate_of, genomic_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, noncoding_RNA_product).
range_in(affects_response_to, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, noncoding_RNA_product).
range_in(increases_response_to, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, noncoding_RNA_product).
range_in(decreases_response_to, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, noncoding_RNA_product).
range_in(affects_splicing_of, transcript, noncoding_RNA_product).
class_slot(noncoding_RNA_product, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, noncoding_RNA_product).
range_in(increases_splicing_of, transcript, noncoding_RNA_product).
class_slot(noncoding_RNA_product, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, noncoding_RNA_product).
range_in(decreases_splicing_of, transcript, noncoding_RNA_product).
class_slot(noncoding_RNA_product, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, noncoding_RNA_product).
range_in(affects_stability_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, noncoding_RNA_product).
range_in(increases_stability_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, noncoding_RNA_product).
range_in(decreases_stability_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, noncoding_RNA_product).
range_in(affects_transport_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, noncoding_RNA_product).
range_in(increases_transport_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, noncoding_RNA_product).
range_in(decreases_transport_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, noncoding_RNA_product).
range_in(affects_secretion_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, noncoding_RNA_product).
range_in(increases_secretion_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, noncoding_RNA_product).
range_in(decreases_secretion_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, noncoding_RNA_product).
range_in(affects_uptake_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, noncoding_RNA_product).
range_in(increases_uptake_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, noncoding_RNA_product).
range_in(decreases_uptake_of, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, noncoding_RNA_product).
range_in(regulates_entity_to_entity, molecular_entity, noncoding_RNA_product).
class_slot(noncoding_RNA_product, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, noncoding_RNA_product).
range_in(biomarker_for, disease_or_phenotypic_feature, noncoding_RNA_product).
class_slot(noncoding_RNA_product, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, noncoding_RNA_product).
range_in(in_taxon, organism_taxon, noncoding_RNA_product).
class_slot(noncoding_RNA_product, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, noncoding_RNA_product).
class_slot(noncoding_RNA_product, in_pathway_with).
required(in_pathway_with).
slotrange(gene_or_gene_product).
multivalued_in(in_pathway_with, noncoding_RNA_product).
range_in(in_pathway_with, gene_or_gene_product, noncoding_RNA_product).
class_slot(noncoding_RNA_product, in_complex_with).
required(in_complex_with).
slotrange(gene_or_gene_product).
multivalued_in(in_complex_with, noncoding_RNA_product).
range_in(in_complex_with, gene_or_gene_product, noncoding_RNA_product).
class_slot(noncoding_RNA_product, in_cell_population_with).
required(in_cell_population_with).
slotrange(gene_or_gene_product).
multivalued_in(in_cell_population_with, noncoding_RNA_product).
range_in(in_cell_population_with, gene_or_gene_product, noncoding_RNA_product).
class_slot(noncoding_RNA_product, expressed_in).
required(expressed_in).
slotrange(anatomical_entity).
multivalued_in(expressed_in, noncoding_RNA_product).
range_in(expressed_in, anatomical_entity, noncoding_RNA_product).
class(occurrent).
is_a(occurrent, named_thing).
has_uri(occurrent, 'http://w3id.org/biolink/vocab/Occurrent').
class_slot(occurrent, id).
required(id).
slotrange(identifier_type).
required_in(id, occurrent).
range_in(id, identifier_type, occurrent).
class_slot(occurrent, name).
required(name).
slotrange(label_type).
range_in(name, label_type, occurrent).
class_slot(occurrent, category).
required(category).
slotrange(iri_type).
multivalued_in(category, occurrent).
range_in(category, iri_type, occurrent).
class_slot(occurrent, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, occurrent).
range_in(related_to, named_thing, occurrent).
class_slot(occurrent, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, occurrent).
range_in(interacts_with, named_thing, occurrent).
class_slot(occurrent, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, occurrent).
class_slot(occurrent, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, occurrent).
class_slot(occurrent, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, occurrent).
range_in(synonym, label_type, occurrent).
class_slot(occurrent, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, occurrent).
class_slot(occurrent, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, occurrent).
class_slot(occurrent, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, occurrent).
class_slot(occurrent, regulates_process_to_process).
required(regulates_process_to_process).
slotrange(occurrent).
multivalued_in(regulates_process_to_process, occurrent).
range_in(regulates_process_to_process, occurrent, occurrent).
class_slot(occurrent, has_participant).
required(has_participant).
slotrange(named_thing).
multivalued_in(has_participant, occurrent).
range_in(has_participant, named_thing, occurrent).
class_slot(occurrent, has_input).
required(has_input).
slotrange(named_thing).
multivalued_in(has_input, occurrent).
range_in(has_input, named_thing, occurrent).
class_slot(occurrent, precedes).
required(precedes).
slotrange(occurrent).
multivalued_in(precedes, occurrent).
range_in(precedes, occurrent, occurrent).
class_slot(occurrent, positively_regulates_process_to_process).
required(positively_regulates_process_to_process).
slotrange(occurrent).
multivalued_in(positively_regulates_process_to_process, occurrent).
range_in(positively_regulates_process_to_process, occurrent, occurrent).
class_slot(occurrent, negatively_regulates_process_to_process).
required(negatively_regulates_process_to_process).
slotrange(occurrent).
multivalued_in(negatively_regulates_process_to_process, occurrent).
range_in(negatively_regulates_process_to_process, occurrent, occurrent).
class(onset).
is_a(onset, attribute).
has_uri(onset, 'http://w3id.org/biolink/vocab/Onset').
class_slot(onset, id).
required(id).
slotrange(identifier_type).
required_in(id, onset).
range_in(id, identifier_type, onset).
class_slot(onset, name).
required(name).
slotrange(label_type).
range_in(name, label_type, onset).
class_slot(onset, category).
required(category).
slotrange(iri_type).
multivalued_in(category, onset).
range_in(category, iri_type, onset).
class_slot(onset, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, onset).
range_in(related_to, named_thing, onset).
class_slot(onset, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, onset).
range_in(interacts_with, named_thing, onset).
class_slot(onset, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, onset).
class_slot(onset, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, onset).
class_slot(onset, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, onset).
range_in(synonym, label_type, onset).
class_slot(onset, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, onset).
class_slot(onset, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, onset).
class_slot(onset, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, onset).
class_slot(onset, subclass_of).
required(subclass_of).
slotrange(ontology_class).
multivalued_in(subclass_of, onset).
range_in(subclass_of, ontology_class, onset).
class(ontology_class).
is_a(ontology_class, named_thing).
has_uri(ontology_class, 'http://w3id.org/biolink/vocab/OntologyClass').
class_slot(ontology_class, id).
required(id).
slotrange(identifier_type).
required_in(id, ontology_class).
range_in(id, identifier_type, ontology_class).
class_slot(ontology_class, name).
required(name).
slotrange(label_type).
range_in(name, label_type, ontology_class).
class_slot(ontology_class, category).
required(category).
slotrange(iri_type).
multivalued_in(category, ontology_class).
range_in(category, iri_type, ontology_class).
class_slot(ontology_class, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, ontology_class).
range_in(related_to, named_thing, ontology_class).
class_slot(ontology_class, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, ontology_class).
range_in(interacts_with, named_thing, ontology_class).
class_slot(ontology_class, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, ontology_class).
class_slot(ontology_class, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, ontology_class).
class_slot(ontology_class, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, ontology_class).
range_in(synonym, label_type, ontology_class).
class_slot(ontology_class, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, ontology_class).
class_slot(ontology_class, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, ontology_class).
class_slot(ontology_class, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, ontology_class).
class_slot(ontology_class, subclass_of).
required(subclass_of).
slotrange(ontology_class).
multivalued_in(subclass_of, ontology_class).
range_in(subclass_of, ontology_class, ontology_class).
class(organism_taxon).
is_a(organism_taxon, ontology_class).
has_uri(organism_taxon, 'http://w3id.org/biolink/vocab/OrganismTaxon').
class_slot(organism_taxon, id).
required(id).
slotrange(identifier_type).
required_in(id, organism_taxon).
range_in(id, identifier_type, organism_taxon).
class_slot(organism_taxon, name).
required(name).
slotrange(label_type).
range_in(name, label_type, organism_taxon).
class_slot(organism_taxon, category).
required(category).
slotrange(iri_type).
multivalued_in(category, organism_taxon).
range_in(category, iri_type, organism_taxon).
class_slot(organism_taxon, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, organism_taxon).
range_in(related_to, named_thing, organism_taxon).
class_slot(organism_taxon, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, organism_taxon).
range_in(interacts_with, named_thing, organism_taxon).
class_slot(organism_taxon, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, organism_taxon).
class_slot(organism_taxon, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, organism_taxon).
class_slot(organism_taxon, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, organism_taxon).
range_in(synonym, label_type, organism_taxon).
class_slot(organism_taxon, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, organism_taxon).
class_slot(organism_taxon, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, organism_taxon).
class_slot(organism_taxon, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, organism_taxon).
class_slot(organism_taxon, subclass_of).
required(subclass_of).
slotrange(ontology_class).
multivalued_in(subclass_of, organism_taxon).
range_in(subclass_of, ontology_class, organism_taxon).
class(organismal_entity).
is_a(organismal_entity, biological_entity).
has_uri(organismal_entity, 'http://w3id.org/biolink/vocab/OrganismalEntity').
class_slot(organismal_entity, id).
required(id).
slotrange(identifier_type).
required_in(id, organismal_entity).
range_in(id, identifier_type, organismal_entity).
class_slot(organismal_entity, name).
required(name).
slotrange(label_type).
range_in(name, label_type, organismal_entity).
class_slot(organismal_entity, category).
required(category).
slotrange(iri_type).
multivalued_in(category, organismal_entity).
range_in(category, iri_type, organismal_entity).
class_slot(organismal_entity, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, organismal_entity).
range_in(related_to, named_thing, organismal_entity).
class_slot(organismal_entity, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, organismal_entity).
range_in(interacts_with, named_thing, organismal_entity).
class_slot(organismal_entity, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, organismal_entity).
class_slot(organismal_entity, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, organismal_entity).
class_slot(organismal_entity, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, organismal_entity).
range_in(synonym, label_type, organismal_entity).
class_slot(organismal_entity, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, organismal_entity).
class_slot(organismal_entity, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, organismal_entity).
class_slot(organismal_entity, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, organismal_entity).
class_slot(organismal_entity, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, organismal_entity).
range_in(has_phenotype, phenotypic_feature, organismal_entity).
class(pairwise_gene_to_gene_interaction).
mixin(pairwise_gene_to_gene_interaction, pairwise_interaction_association).
is_a(pairwise_gene_to_gene_interaction, gene_to_gene_association).
defining_slots(gene_to_gene_association, [subject, object, relation]).
has_uri(pairwise_gene_to_gene_interaction, 'http://w3id.org/biolink/vocab/PairwiseGeneToGeneInteraction').
class_slot(pairwise_gene_to_gene_interaction, id).
required(id).
slotrange(identifier_type).
required_in(id, pairwise_gene_to_gene_interaction).
range_in(id, identifier_type, pairwise_gene_to_gene_interaction).
class_slot(pairwise_gene_to_gene_interaction, subject).
required(subject).
slotrange(gene_or_gene_product).
required_in(subject, pairwise_gene_to_gene_interaction).
range_in(subject, gene_or_gene_product, pairwise_gene_to_gene_interaction).
class_slot(pairwise_gene_to_gene_interaction, relation).
required(relation).
slotrange(iri_type).
required_in(relation, pairwise_gene_to_gene_interaction).
range_in(relation, iri_type, pairwise_gene_to_gene_interaction).
class_slot(pairwise_gene_to_gene_interaction, object).
required(object).
slotrange(gene_or_gene_product).
required_in(object, pairwise_gene_to_gene_interaction).
range_in(object, gene_or_gene_product, pairwise_gene_to_gene_interaction).
class_slot(pairwise_gene_to_gene_interaction, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, pairwise_gene_to_gene_interaction).
class_slot(pairwise_gene_to_gene_interaction, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, pairwise_gene_to_gene_interaction).
class_slot(pairwise_gene_to_gene_interaction, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, pairwise_gene_to_gene_interaction).
range_in(qualifiers, ontology_class, pairwise_gene_to_gene_interaction).
class_slot(pairwise_gene_to_gene_interaction, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, pairwise_gene_to_gene_interaction).
range_in(publications, publication, pairwise_gene_to_gene_interaction).
class_slot(pairwise_gene_to_gene_interaction, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, pairwise_gene_to_gene_interaction).
class_slot(pairwise_gene_to_gene_interaction, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, pairwise_gene_to_gene_interaction).
class(pairwise_interaction_association).
is_a(pairwise_interaction_association, association).
defining_slots(association, [subject, object, relation]).
has_uri(pairwise_interaction_association, 'http://w3id.org/biolink/vocab/PairwiseInteractionAssociation').
class_slot(pairwise_interaction_association, id).
required(id).
slotrange(identifier_type).
required_in(id, pairwise_interaction_association).
range_in(id, identifier_type, pairwise_interaction_association).
class_slot(pairwise_interaction_association, subject).
required(subject).
slotrange(molecular_entity).
required_in(subject, pairwise_interaction_association).
range_in(subject, molecular_entity, pairwise_interaction_association).
class_slot(pairwise_interaction_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, pairwise_interaction_association).
range_in(relation, iri_type, pairwise_interaction_association).
class_slot(pairwise_interaction_association, object).
required(object).
slotrange(molecular_entity).
required_in(object, pairwise_interaction_association).
range_in(object, molecular_entity, pairwise_interaction_association).
class_slot(pairwise_interaction_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, pairwise_interaction_association).
class_slot(pairwise_interaction_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, pairwise_interaction_association).
class_slot(pairwise_interaction_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, pairwise_interaction_association).
range_in(qualifiers, ontology_class, pairwise_interaction_association).
class_slot(pairwise_interaction_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, pairwise_interaction_association).
range_in(publications, publication, pairwise_interaction_association).
class_slot(pairwise_interaction_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, pairwise_interaction_association).
class_slot(pairwise_interaction_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, pairwise_interaction_association).
class_slot(pairwise_interaction_association, interacting_molecules_category).
required(interacting_molecules_category).
slotrange(ontology_class).
range_in(interacting_molecules_category, ontology_class, pairwise_interaction_association).
class(pathognomonicity_quantifier).
is_a(pathognomonicity_quantifier, specificity_quantifier).
has_uri(pathognomonicity_quantifier, 'http://w3id.org/biolink/vocab/PathognomonicityQuantifier').
class(pathway).
is_a(pathway, biological_process).
has_uri(pathway, 'http://w3id.org/biolink/vocab/Pathway').
class_slot(pathway, id).
required(id).
slotrange(identifier_type).
required_in(id, pathway).
range_in(id, identifier_type, pathway).
class_slot(pathway, name).
required(name).
slotrange(label_type).
range_in(name, label_type, pathway).
class_slot(pathway, category).
required(category).
slotrange(iri_type).
multivalued_in(category, pathway).
range_in(category, iri_type, pathway).
class_slot(pathway, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, pathway).
range_in(related_to, named_thing, pathway).
class_slot(pathway, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, pathway).
range_in(interacts_with, named_thing, pathway).
class_slot(pathway, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, pathway).
class_slot(pathway, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, pathway).
class_slot(pathway, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, pathway).
range_in(synonym, label_type, pathway).
class_slot(pathway, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, pathway).
class_slot(pathway, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, pathway).
class_slot(pathway, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, pathway).
class_slot(pathway, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, pathway).
range_in(has_phenotype, phenotypic_feature, pathway).
class_slot(pathway, regulates_process_to_process).
required(regulates_process_to_process).
slotrange(occurrent).
multivalued_in(regulates_process_to_process, pathway).
range_in(regulates_process_to_process, occurrent, pathway).
class_slot(pathway, has_participant).
required(has_participant).
slotrange(named_thing).
multivalued_in(has_participant, pathway).
range_in(has_participant, named_thing, pathway).
class_slot(pathway, has_input).
required(has_input).
slotrange(named_thing).
multivalued_in(has_input, pathway).
range_in(has_input, named_thing, pathway).
class_slot(pathway, precedes).
required(precedes).
slotrange(occurrent).
multivalued_in(precedes, pathway).
range_in(precedes, occurrent, pathway).
class(phenomenon).
is_a(phenomenon, occurrent).
has_uri(phenomenon, 'http://w3id.org/biolink/vocab/Phenomenon').
class_slot(phenomenon, id).
required(id).
slotrange(identifier_type).
required_in(id, phenomenon).
range_in(id, identifier_type, phenomenon).
class_slot(phenomenon, name).
required(name).
slotrange(label_type).
range_in(name, label_type, phenomenon).
class_slot(phenomenon, category).
required(category).
slotrange(iri_type).
multivalued_in(category, phenomenon).
range_in(category, iri_type, phenomenon).
class_slot(phenomenon, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, phenomenon).
range_in(related_to, named_thing, phenomenon).
class_slot(phenomenon, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, phenomenon).
range_in(interacts_with, named_thing, phenomenon).
class_slot(phenomenon, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, phenomenon).
class_slot(phenomenon, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, phenomenon).
class_slot(phenomenon, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, phenomenon).
range_in(synonym, label_type, phenomenon).
class_slot(phenomenon, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, phenomenon).
class_slot(phenomenon, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, phenomenon).
class_slot(phenomenon, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, phenomenon).
class_slot(phenomenon, regulates_process_to_process).
required(regulates_process_to_process).
slotrange(occurrent).
multivalued_in(regulates_process_to_process, phenomenon).
range_in(regulates_process_to_process, occurrent, phenomenon).
class_slot(phenomenon, has_participant).
required(has_participant).
slotrange(named_thing).
multivalued_in(has_participant, phenomenon).
range_in(has_participant, named_thing, phenomenon).
class_slot(phenomenon, has_input).
required(has_input).
slotrange(named_thing).
multivalued_in(has_input, phenomenon).
range_in(has_input, named_thing, phenomenon).
class_slot(phenomenon, precedes).
required(precedes).
slotrange(occurrent).
multivalued_in(precedes, phenomenon).
range_in(precedes, occurrent, phenomenon).
class(phenotypic_feature).
is_a(phenotypic_feature, disease_or_phenotypic_feature).
has_uri(phenotypic_feature, 'http://w3id.org/biolink/vocab/PhenotypicFeature').
class_slot(phenotypic_feature, id).
required(id).
slotrange(identifier_type).
required_in(id, phenotypic_feature).
range_in(id, identifier_type, phenotypic_feature).
class_slot(phenotypic_feature, name).
required(name).
slotrange(label_type).
range_in(name, label_type, phenotypic_feature).
class_slot(phenotypic_feature, category).
required(category).
slotrange(iri_type).
multivalued_in(category, phenotypic_feature).
range_in(category, iri_type, phenotypic_feature).
class_slot(phenotypic_feature, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, phenotypic_feature).
range_in(related_to, named_thing, phenotypic_feature).
class_slot(phenotypic_feature, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, phenotypic_feature).
range_in(interacts_with, named_thing, phenotypic_feature).
class_slot(phenotypic_feature, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, phenotypic_feature).
class_slot(phenotypic_feature, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, phenotypic_feature).
class_slot(phenotypic_feature, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, phenotypic_feature).
range_in(synonym, label_type, phenotypic_feature).
class_slot(phenotypic_feature, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, phenotypic_feature).
class_slot(phenotypic_feature, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, phenotypic_feature).
class_slot(phenotypic_feature, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, phenotypic_feature).
class_slot(phenotypic_feature, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, phenotypic_feature).
range_in(has_phenotype, phenotypic_feature, phenotypic_feature).
class_slot(phenotypic_feature, correlated_with).
required(correlated_with).
slotrange(molecular_entity).
multivalued_in(correlated_with, phenotypic_feature).
range_in(correlated_with, molecular_entity, phenotypic_feature).
class_slot(phenotypic_feature, has_biomarker).
required(has_biomarker).
slotrange(molecular_entity).
multivalued_in(has_biomarker, phenotypic_feature).
range_in(has_biomarker, molecular_entity, phenotypic_feature).
class_slot(phenotypic_feature, treated_by).
required(treated_by).
slotrange(named_thing).
multivalued_in(treated_by, phenotypic_feature).
range_in(treated_by, named_thing, phenotypic_feature).
class_slot(phenotypic_feature, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, phenotypic_feature).
range_in(in_taxon, organism_taxon, phenotypic_feature).
class(phenotypic_sex).
is_a(phenotypic_sex, biological_sex).
has_uri(phenotypic_sex, 'http://w3id.org/biolink/vocab/PhenotypicSex').
class_slot(phenotypic_sex, id).
required(id).
slotrange(identifier_type).
required_in(id, phenotypic_sex).
range_in(id, identifier_type, phenotypic_sex).
class_slot(phenotypic_sex, name).
required(name).
slotrange(label_type).
range_in(name, label_type, phenotypic_sex).
class_slot(phenotypic_sex, category).
required(category).
slotrange(iri_type).
multivalued_in(category, phenotypic_sex).
range_in(category, iri_type, phenotypic_sex).
class_slot(phenotypic_sex, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, phenotypic_sex).
range_in(related_to, named_thing, phenotypic_sex).
class_slot(phenotypic_sex, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, phenotypic_sex).
range_in(interacts_with, named_thing, phenotypic_sex).
class_slot(phenotypic_sex, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, phenotypic_sex).
class_slot(phenotypic_sex, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, phenotypic_sex).
class_slot(phenotypic_sex, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, phenotypic_sex).
range_in(synonym, label_type, phenotypic_sex).
class_slot(phenotypic_sex, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, phenotypic_sex).
class_slot(phenotypic_sex, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, phenotypic_sex).
class_slot(phenotypic_sex, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, phenotypic_sex).
class_slot(phenotypic_sex, subclass_of).
required(subclass_of).
slotrange(ontology_class).
multivalued_in(subclass_of, phenotypic_sex).
range_in(subclass_of, ontology_class, phenotypic_sex).
class(physiological_process).
is_a(physiological_process, biological_process).
has_uri(physiological_process, 'http://w3id.org/biolink/vocab/PhysiologicalProcess').
class_slot(physiological_process, id).
required(id).
slotrange(identifier_type).
required_in(id, physiological_process).
range_in(id, identifier_type, physiological_process).
class_slot(physiological_process, name).
required(name).
slotrange(label_type).
range_in(name, label_type, physiological_process).
class_slot(physiological_process, category).
required(category).
slotrange(iri_type).
multivalued_in(category, physiological_process).
range_in(category, iri_type, physiological_process).
class_slot(physiological_process, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, physiological_process).
range_in(related_to, named_thing, physiological_process).
class_slot(physiological_process, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, physiological_process).
range_in(interacts_with, named_thing, physiological_process).
class_slot(physiological_process, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, physiological_process).
class_slot(physiological_process, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, physiological_process).
class_slot(physiological_process, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, physiological_process).
range_in(synonym, label_type, physiological_process).
class_slot(physiological_process, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, physiological_process).
class_slot(physiological_process, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, physiological_process).
class_slot(physiological_process, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, physiological_process).
class_slot(physiological_process, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, physiological_process).
range_in(has_phenotype, phenotypic_feature, physiological_process).
class_slot(physiological_process, regulates_process_to_process).
required(regulates_process_to_process).
slotrange(occurrent).
multivalued_in(regulates_process_to_process, physiological_process).
range_in(regulates_process_to_process, occurrent, physiological_process).
class_slot(physiological_process, has_participant).
required(has_participant).
slotrange(named_thing).
multivalued_in(has_participant, physiological_process).
range_in(has_participant, named_thing, physiological_process).
class_slot(physiological_process, has_input).
required(has_input).
slotrange(named_thing).
multivalued_in(has_input, physiological_process).
range_in(has_input, named_thing, physiological_process).
class_slot(physiological_process, precedes).
required(precedes).
slotrange(occurrent).
multivalued_in(precedes, physiological_process).
range_in(precedes, occurrent, physiological_process).
class(planetary_entity).
is_a(planetary_entity, named_thing).
has_uri(planetary_entity, 'http://w3id.org/biolink/vocab/PlanetaryEntity').
class_slot(planetary_entity, id).
required(id).
slotrange(identifier_type).
required_in(id, planetary_entity).
range_in(id, identifier_type, planetary_entity).
class_slot(planetary_entity, name).
required(name).
slotrange(label_type).
range_in(name, label_type, planetary_entity).
class_slot(planetary_entity, category).
required(category).
slotrange(iri_type).
multivalued_in(category, planetary_entity).
range_in(category, iri_type, planetary_entity).
class_slot(planetary_entity, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, planetary_entity).
range_in(related_to, named_thing, planetary_entity).
class_slot(planetary_entity, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, planetary_entity).
range_in(interacts_with, named_thing, planetary_entity).
class_slot(planetary_entity, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, planetary_entity).
class_slot(planetary_entity, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, planetary_entity).
class_slot(planetary_entity, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, planetary_entity).
range_in(synonym, label_type, planetary_entity).
class_slot(planetary_entity, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, planetary_entity).
class_slot(planetary_entity, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, planetary_entity).
class_slot(planetary_entity, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, planetary_entity).
class(population_of_individual_organisms).
mixin(population_of_individual_organisms, thing_with_taxon).
is_a(population_of_individual_organisms, organismal_entity).
has_uri(population_of_individual_organisms, 'http://w3id.org/biolink/vocab/PopulationOfIndividualOrganisms').
class_slot(population_of_individual_organisms, id).
required(id).
slotrange(identifier_type).
required_in(id, population_of_individual_organisms).
range_in(id, identifier_type, population_of_individual_organisms).
class_slot(population_of_individual_organisms, name).
required(name).
slotrange(label_type).
range_in(name, label_type, population_of_individual_organisms).
class_slot(population_of_individual_organisms, category).
required(category).
slotrange(iri_type).
multivalued_in(category, population_of_individual_organisms).
range_in(category, iri_type, population_of_individual_organisms).
class_slot(population_of_individual_organisms, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, population_of_individual_organisms).
range_in(related_to, named_thing, population_of_individual_organisms).
class_slot(population_of_individual_organisms, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, population_of_individual_organisms).
range_in(interacts_with, named_thing, population_of_individual_organisms).
class_slot(population_of_individual_organisms, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, population_of_individual_organisms).
class_slot(population_of_individual_organisms, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, population_of_individual_organisms).
class_slot(population_of_individual_organisms, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, population_of_individual_organisms).
range_in(synonym, label_type, population_of_individual_organisms).
class_slot(population_of_individual_organisms, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, population_of_individual_organisms).
class_slot(population_of_individual_organisms, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, population_of_individual_organisms).
class_slot(population_of_individual_organisms, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, population_of_individual_organisms).
class_slot(population_of_individual_organisms, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, population_of_individual_organisms).
range_in(has_phenotype, phenotypic_feature, population_of_individual_organisms).
class_slot(population_of_individual_organisms, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, population_of_individual_organisms).
range_in(in_taxon, organism_taxon, population_of_individual_organisms).
class(population_to_population_association).
is_a(population_to_population_association, association).
defining_slots(association, [subject, object]).
has_uri(population_to_population_association, 'http://w3id.org/biolink/vocab/PopulationToPopulationAssociation').
class_slot(population_to_population_association, id).
required(id).
slotrange(identifier_type).
required_in(id, population_to_population_association).
range_in(id, identifier_type, population_to_population_association).
class_slot(population_to_population_association, subject).
required(subject).
slotrange(population_of_individual_organisms).
required_in(subject, population_to_population_association).
range_in(subject, population_of_individual_organisms, population_to_population_association).
class_slot(population_to_population_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, population_to_population_association).
range_in(relation, iri_type, population_to_population_association).
class_slot(population_to_population_association, object).
required(object).
slotrange(population_of_individual_organisms).
required_in(object, population_to_population_association).
range_in(object, population_of_individual_organisms, population_to_population_association).
class_slot(population_to_population_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, population_to_population_association).
class_slot(population_to_population_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, population_to_population_association).
class_slot(population_to_population_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, population_to_population_association).
range_in(qualifiers, ontology_class, population_to_population_association).
class_slot(population_to_population_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, population_to_population_association).
range_in(publications, publication, population_to_population_association).
class_slot(population_to_population_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, population_to_population_association).
class_slot(population_to_population_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, population_to_population_association).
class(procedure).
is_a(procedure, occurrent).
has_uri(procedure, 'http://w3id.org/biolink/vocab/Procedure').
class_slot(procedure, id).
required(id).
slotrange(identifier_type).
required_in(id, procedure).
range_in(id, identifier_type, procedure).
class_slot(procedure, name).
required(name).
slotrange(label_type).
range_in(name, label_type, procedure).
class_slot(procedure, category).
required(category).
slotrange(iri_type).
multivalued_in(category, procedure).
range_in(category, iri_type, procedure).
class_slot(procedure, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, procedure).
range_in(related_to, named_thing, procedure).
class_slot(procedure, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, procedure).
range_in(interacts_with, named_thing, procedure).
class_slot(procedure, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, procedure).
class_slot(procedure, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, procedure).
class_slot(procedure, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, procedure).
range_in(synonym, label_type, procedure).
class_slot(procedure, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, procedure).
class_slot(procedure, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, procedure).
class_slot(procedure, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, procedure).
class_slot(procedure, regulates_process_to_process).
required(regulates_process_to_process).
slotrange(occurrent).
multivalued_in(regulates_process_to_process, procedure).
range_in(regulates_process_to_process, occurrent, procedure).
class_slot(procedure, has_participant).
required(has_participant).
slotrange(named_thing).
multivalued_in(has_participant, procedure).
range_in(has_participant, named_thing, procedure).
class_slot(procedure, has_input).
required(has_input).
slotrange(named_thing).
multivalued_in(has_input, procedure).
range_in(has_input, named_thing, procedure).
class_slot(procedure, precedes).
required(precedes).
slotrange(occurrent).
multivalued_in(precedes, procedure).
range_in(precedes, occurrent, procedure).
class(protein).
is_a(protein, gene_product).
has_uri(protein, 'http://w3id.org/biolink/vocab/Protein').
class_slot(protein, id).
required(id).
slotrange(identifier_type).
required_in(id, protein).
range_in(id, identifier_type, protein).
class_slot(protein, name).
required(name).
slotrange(symbol_type).
range_in(name, symbol_type, protein).
class_slot(protein, category).
required(category).
slotrange(iri_type).
multivalued_in(category, protein).
range_in(category, iri_type, protein).
class_slot(protein, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, protein).
range_in(related_to, named_thing, protein).
class_slot(protein, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, protein).
range_in(interacts_with, named_thing, protein).
class_slot(protein, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, protein).
class_slot(protein, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, protein).
class_slot(protein, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, protein).
range_in(synonym, label_type, protein).
class_slot(protein, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, protein).
class_slot(protein, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, protein).
class_slot(protein, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, protein).
class_slot(protein, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, protein).
range_in(has_phenotype, phenotypic_feature, protein).
class_slot(protein, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, protein).
range_in(molecularly_interacts_with, molecular_entity, protein).
class_slot(protein, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, protein).
range_in(affects_abundance_of, molecular_entity, protein).
class_slot(protein, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, protein).
range_in(increases_abundance_of, molecular_entity, protein).
class_slot(protein, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, protein).
range_in(decreases_abundance_of, molecular_entity, protein).
class_slot(protein, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, protein).
range_in(affects_activity_of, molecular_entity, protein).
class_slot(protein, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, protein).
range_in(increases_activity_of, molecular_entity, protein).
class_slot(protein, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, protein).
range_in(decreases_activity_of, molecular_entity, protein).
class_slot(protein, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, protein).
range_in(affects_expression_of, genomic_entity, protein).
class_slot(protein, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, protein).
range_in(increases_expression_of, genomic_entity, protein).
class_slot(protein, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, protein).
range_in(decreases_expression_of, genomic_entity, protein).
class_slot(protein, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, protein).
range_in(affects_folding_of, molecular_entity, protein).
class_slot(protein, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, protein).
range_in(increases_folding_of, molecular_entity, protein).
class_slot(protein, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, protein).
range_in(decreases_folding_of, molecular_entity, protein).
class_slot(protein, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, protein).
range_in(affects_localization_of, molecular_entity, protein).
class_slot(protein, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, protein).
range_in(increases_localization_of, molecular_entity, protein).
class_slot(protein, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, protein).
range_in(decreases_localization_of, molecular_entity, protein).
class_slot(protein, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, protein).
range_in(affects_metabolic_processing_of, molecular_entity, protein).
class_slot(protein, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, protein).
range_in(increases_metabolic_processing_of, molecular_entity, protein).
class_slot(protein, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, protein).
range_in(decreases_metabolic_processing_of, molecular_entity, protein).
class_slot(protein, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, protein).
range_in(affects_molecular_modification_of, molecular_entity, protein).
class_slot(protein, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, protein).
range_in(increases_molecular_modification_of, molecular_entity, protein).
class_slot(protein, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, protein).
range_in(decreases_molecular_modification_of, molecular_entity, protein).
class_slot(protein, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, protein).
range_in(affects_synthesis_of, molecular_entity, protein).
class_slot(protein, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, protein).
range_in(increases_synthesis_of, molecular_entity, protein).
class_slot(protein, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, protein).
range_in(decreases_synthesis_of, molecular_entity, protein).
class_slot(protein, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, protein).
range_in(affects_degradation_of, molecular_entity, protein).
class_slot(protein, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, protein).
range_in(increases_degradation_of, molecular_entity, protein).
class_slot(protein, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, protein).
range_in(decreases_degradation_of, molecular_entity, protein).
class_slot(protein, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, protein).
range_in(affects_mutation_rate_of, genomic_entity, protein).
class_slot(protein, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, protein).
range_in(increases_mutation_rate_of, genomic_entity, protein).
class_slot(protein, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, protein).
range_in(decreases_mutation_rate_of, genomic_entity, protein).
class_slot(protein, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, protein).
range_in(affects_response_to, molecular_entity, protein).
class_slot(protein, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, protein).
range_in(increases_response_to, molecular_entity, protein).
class_slot(protein, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, protein).
range_in(decreases_response_to, molecular_entity, protein).
class_slot(protein, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, protein).
range_in(affects_splicing_of, transcript, protein).
class_slot(protein, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, protein).
range_in(increases_splicing_of, transcript, protein).
class_slot(protein, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, protein).
range_in(decreases_splicing_of, transcript, protein).
class_slot(protein, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, protein).
range_in(affects_stability_of, molecular_entity, protein).
class_slot(protein, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, protein).
range_in(increases_stability_of, molecular_entity, protein).
class_slot(protein, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, protein).
range_in(decreases_stability_of, molecular_entity, protein).
class_slot(protein, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, protein).
range_in(affects_transport_of, molecular_entity, protein).
class_slot(protein, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, protein).
range_in(increases_transport_of, molecular_entity, protein).
class_slot(protein, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, protein).
range_in(decreases_transport_of, molecular_entity, protein).
class_slot(protein, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, protein).
range_in(affects_secretion_of, molecular_entity, protein).
class_slot(protein, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, protein).
range_in(increases_secretion_of, molecular_entity, protein).
class_slot(protein, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, protein).
range_in(decreases_secretion_of, molecular_entity, protein).
class_slot(protein, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, protein).
range_in(affects_uptake_of, molecular_entity, protein).
class_slot(protein, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, protein).
range_in(increases_uptake_of, molecular_entity, protein).
class_slot(protein, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, protein).
range_in(decreases_uptake_of, molecular_entity, protein).
class_slot(protein, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, protein).
range_in(regulates_entity_to_entity, molecular_entity, protein).
class_slot(protein, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, protein).
range_in(biomarker_for, disease_or_phenotypic_feature, protein).
class_slot(protein, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, protein).
range_in(in_taxon, organism_taxon, protein).
class_slot(protein, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, protein).
class_slot(protein, in_pathway_with).
required(in_pathway_with).
slotrange(gene_or_gene_product).
multivalued_in(in_pathway_with, protein).
range_in(in_pathway_with, gene_or_gene_product, protein).
class_slot(protein, in_complex_with).
required(in_complex_with).
slotrange(gene_or_gene_product).
multivalued_in(in_complex_with, protein).
range_in(in_complex_with, gene_or_gene_product, protein).
class_slot(protein, in_cell_population_with).
required(in_cell_population_with).
slotrange(gene_or_gene_product).
multivalued_in(in_cell_population_with, protein).
range_in(in_cell_population_with, gene_or_gene_product, protein).
class_slot(protein, expressed_in).
required(expressed_in).
slotrange(anatomical_entity).
multivalued_in(expressed_in, protein).
range_in(expressed_in, anatomical_entity, protein).
class(protein_isoform).
mixin(protein_isoform, gene_product_isoform).
is_a(protein_isoform, protein).
has_uri(protein_isoform, 'http://w3id.org/biolink/vocab/ProteinIsoform').
class_slot(protein_isoform, id).
required(id).
slotrange(identifier_type).
required_in(id, protein_isoform).
range_in(id, identifier_type, protein_isoform).
class_slot(protein_isoform, name).
required(name).
slotrange(symbol_type).
range_in(name, symbol_type, protein_isoform).
class_slot(protein_isoform, category).
required(category).
slotrange(iri_type).
multivalued_in(category, protein_isoform).
range_in(category, iri_type, protein_isoform).
class_slot(protein_isoform, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, protein_isoform).
range_in(related_to, named_thing, protein_isoform).
class_slot(protein_isoform, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, protein_isoform).
range_in(interacts_with, named_thing, protein_isoform).
class_slot(protein_isoform, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, protein_isoform).
class_slot(protein_isoform, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, protein_isoform).
class_slot(protein_isoform, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, protein_isoform).
range_in(synonym, label_type, protein_isoform).
class_slot(protein_isoform, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, protein_isoform).
class_slot(protein_isoform, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, protein_isoform).
class_slot(protein_isoform, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, protein_isoform).
class_slot(protein_isoform, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, protein_isoform).
range_in(has_phenotype, phenotypic_feature, protein_isoform).
class_slot(protein_isoform, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, protein_isoform).
range_in(molecularly_interacts_with, molecular_entity, protein_isoform).
class_slot(protein_isoform, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, protein_isoform).
range_in(affects_abundance_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, protein_isoform).
range_in(increases_abundance_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, protein_isoform).
range_in(decreases_abundance_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, protein_isoform).
range_in(affects_activity_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, protein_isoform).
range_in(increases_activity_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, protein_isoform).
range_in(decreases_activity_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, protein_isoform).
range_in(affects_expression_of, genomic_entity, protein_isoform).
class_slot(protein_isoform, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, protein_isoform).
range_in(increases_expression_of, genomic_entity, protein_isoform).
class_slot(protein_isoform, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, protein_isoform).
range_in(decreases_expression_of, genomic_entity, protein_isoform).
class_slot(protein_isoform, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, protein_isoform).
range_in(affects_folding_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, protein_isoform).
range_in(increases_folding_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, protein_isoform).
range_in(decreases_folding_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, protein_isoform).
range_in(affects_localization_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, protein_isoform).
range_in(increases_localization_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, protein_isoform).
range_in(decreases_localization_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, protein_isoform).
range_in(affects_metabolic_processing_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, protein_isoform).
range_in(increases_metabolic_processing_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, protein_isoform).
range_in(decreases_metabolic_processing_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, protein_isoform).
range_in(affects_molecular_modification_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, protein_isoform).
range_in(increases_molecular_modification_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, protein_isoform).
range_in(decreases_molecular_modification_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, protein_isoform).
range_in(affects_synthesis_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, protein_isoform).
range_in(increases_synthesis_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, protein_isoform).
range_in(decreases_synthesis_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, protein_isoform).
range_in(affects_degradation_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, protein_isoform).
range_in(increases_degradation_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, protein_isoform).
range_in(decreases_degradation_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, protein_isoform).
range_in(affects_mutation_rate_of, genomic_entity, protein_isoform).
class_slot(protein_isoform, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, protein_isoform).
range_in(increases_mutation_rate_of, genomic_entity, protein_isoform).
class_slot(protein_isoform, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, protein_isoform).
range_in(decreases_mutation_rate_of, genomic_entity, protein_isoform).
class_slot(protein_isoform, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, protein_isoform).
range_in(affects_response_to, molecular_entity, protein_isoform).
class_slot(protein_isoform, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, protein_isoform).
range_in(increases_response_to, molecular_entity, protein_isoform).
class_slot(protein_isoform, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, protein_isoform).
range_in(decreases_response_to, molecular_entity, protein_isoform).
class_slot(protein_isoform, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, protein_isoform).
range_in(affects_splicing_of, transcript, protein_isoform).
class_slot(protein_isoform, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, protein_isoform).
range_in(increases_splicing_of, transcript, protein_isoform).
class_slot(protein_isoform, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, protein_isoform).
range_in(decreases_splicing_of, transcript, protein_isoform).
class_slot(protein_isoform, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, protein_isoform).
range_in(affects_stability_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, protein_isoform).
range_in(increases_stability_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, protein_isoform).
range_in(decreases_stability_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, protein_isoform).
range_in(affects_transport_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, protein_isoform).
range_in(increases_transport_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, protein_isoform).
range_in(decreases_transport_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, protein_isoform).
range_in(affects_secretion_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, protein_isoform).
range_in(increases_secretion_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, protein_isoform).
range_in(decreases_secretion_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, protein_isoform).
range_in(affects_uptake_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, protein_isoform).
range_in(increases_uptake_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, protein_isoform).
range_in(decreases_uptake_of, molecular_entity, protein_isoform).
class_slot(protein_isoform, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, protein_isoform).
range_in(regulates_entity_to_entity, molecular_entity, protein_isoform).
class_slot(protein_isoform, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, protein_isoform).
range_in(biomarker_for, disease_or_phenotypic_feature, protein_isoform).
class_slot(protein_isoform, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, protein_isoform).
range_in(in_taxon, organism_taxon, protein_isoform).
class_slot(protein_isoform, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, protein_isoform).
class_slot(protein_isoform, in_pathway_with).
required(in_pathway_with).
slotrange(gene_or_gene_product).
multivalued_in(in_pathway_with, protein_isoform).
range_in(in_pathway_with, gene_or_gene_product, protein_isoform).
class_slot(protein_isoform, in_complex_with).
required(in_complex_with).
slotrange(gene_or_gene_product).
multivalued_in(in_complex_with, protein_isoform).
range_in(in_complex_with, gene_or_gene_product, protein_isoform).
class_slot(protein_isoform, in_cell_population_with).
required(in_cell_population_with).
slotrange(gene_or_gene_product).
multivalued_in(in_cell_population_with, protein_isoform).
range_in(in_cell_population_with, gene_or_gene_product, protein_isoform).
class_slot(protein_isoform, expressed_in).
required(expressed_in).
slotrange(anatomical_entity).
multivalued_in(expressed_in, protein_isoform).
range_in(expressed_in, anatomical_entity, protein_isoform).
class(provider).
is_a(provider, administrative_entity).
has_uri(provider, 'http://w3id.org/biolink/vocab/Provider').
class_slot(provider, id).
required(id).
slotrange(identifier_type).
required_in(id, provider).
range_in(id, identifier_type, provider).
class_slot(provider, name).
required(name).
slotrange(label_type).
range_in(name, label_type, provider).
class_slot(provider, category).
required(category).
slotrange(iri_type).
multivalued_in(category, provider).
range_in(category, iri_type, provider).
class_slot(provider, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, provider).
range_in(related_to, named_thing, provider).
class_slot(provider, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, provider).
range_in(interacts_with, named_thing, provider).
class_slot(provider, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, provider).
class_slot(provider, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, provider).
class_slot(provider, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, provider).
range_in(synonym, label_type, provider).
class_slot(provider, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, provider).
class_slot(provider, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, provider).
class_slot(provider, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, provider).
class(publication).
is_a(publication, information_content_entity).
has_uri(publication, 'http://w3id.org/biolink/vocab/Publication').
class_slot(publication, id).
required(id).
slotrange(identifier_type).
required_in(id, publication).
range_in(id, identifier_type, publication).
class_slot(publication, name).
required(name).
slotrange(label_type).
range_in(name, label_type, publication).
class_slot(publication, category).
required(category).
slotrange(iri_type).
multivalued_in(category, publication).
range_in(category, iri_type, publication).
class_slot(publication, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, publication).
range_in(related_to, named_thing, publication).
class_slot(publication, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, publication).
range_in(interacts_with, named_thing, publication).
class_slot(publication, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, publication).
class_slot(publication, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, publication).
class_slot(publication, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, publication).
range_in(synonym, label_type, publication).
class_slot(publication, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, publication).
class_slot(publication, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, publication).
class_slot(publication, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, publication).
class(relationship_quantifier).
has_uri(relationship_quantifier, 'http://w3id.org/biolink/vocab/RelationshipQuantifier').
class(relationship_type).
is_a(relationship_type, ontology_class).
has_uri(relationship_type, 'http://w3id.org/biolink/vocab/RelationshipType').
class_slot(relationship_type, id).
required(id).
slotrange(identifier_type).
required_in(id, relationship_type).
range_in(id, identifier_type, relationship_type).
class_slot(relationship_type, name).
required(name).
slotrange(label_type).
range_in(name, label_type, relationship_type).
class_slot(relationship_type, category).
required(category).
slotrange(iri_type).
multivalued_in(category, relationship_type).
range_in(category, iri_type, relationship_type).
class_slot(relationship_type, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, relationship_type).
range_in(related_to, named_thing, relationship_type).
class_slot(relationship_type, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, relationship_type).
range_in(interacts_with, named_thing, relationship_type).
class_slot(relationship_type, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, relationship_type).
class_slot(relationship_type, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, relationship_type).
class_slot(relationship_type, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, relationship_type).
range_in(synonym, label_type, relationship_type).
class_slot(relationship_type, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, relationship_type).
class_slot(relationship_type, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, relationship_type).
class_slot(relationship_type, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, relationship_type).
class_slot(relationship_type, subclass_of).
required(subclass_of).
slotrange(ontology_class).
multivalued_in(subclass_of, relationship_type).
range_in(subclass_of, ontology_class, relationship_type).
class('RNA_product').
is_a('RNA_product', gene_product).
has_uri('RNA_product', 'http://w3id.org/biolink/vocab/RNAProduct').
class_slot('RNA_product', id).
required(id).
slotrange(identifier_type).
required_in(id, 'RNA_product').
range_in(id, identifier_type, 'RNA_product').
class_slot('RNA_product', name).
required(name).
slotrange(symbol_type).
range_in(name, symbol_type, 'RNA_product').
class_slot('RNA_product', category).
required(category).
slotrange(iri_type).
multivalued_in(category, 'RNA_product').
range_in(category, iri_type, 'RNA_product').
class_slot('RNA_product', related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, 'RNA_product').
range_in(related_to, named_thing, 'RNA_product').
class_slot('RNA_product', interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, 'RNA_product').
range_in(interacts_with, named_thing, 'RNA_product').
class_slot('RNA_product', node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, 'RNA_product').
class_slot('RNA_product', iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, 'RNA_product').
class_slot('RNA_product', synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, 'RNA_product').
range_in(synonym, label_type, 'RNA_product').
class_slot('RNA_product', full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, 'RNA_product').
class_slot('RNA_product', description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, 'RNA_product').
class_slot('RNA_product', systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, 'RNA_product').
class_slot('RNA_product', has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, 'RNA_product').
range_in(has_phenotype, phenotypic_feature, 'RNA_product').
class_slot('RNA_product', molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, 'RNA_product').
range_in(molecularly_interacts_with, molecular_entity, 'RNA_product').
class_slot('RNA_product', affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, 'RNA_product').
range_in(affects_abundance_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, 'RNA_product').
range_in(increases_abundance_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, 'RNA_product').
range_in(decreases_abundance_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, 'RNA_product').
range_in(affects_activity_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, 'RNA_product').
range_in(increases_activity_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, 'RNA_product').
range_in(decreases_activity_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, 'RNA_product').
range_in(affects_expression_of, genomic_entity, 'RNA_product').
class_slot('RNA_product', increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, 'RNA_product').
range_in(increases_expression_of, genomic_entity, 'RNA_product').
class_slot('RNA_product', decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, 'RNA_product').
range_in(decreases_expression_of, genomic_entity, 'RNA_product').
class_slot('RNA_product', affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, 'RNA_product').
range_in(affects_folding_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, 'RNA_product').
range_in(increases_folding_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, 'RNA_product').
range_in(decreases_folding_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, 'RNA_product').
range_in(affects_localization_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, 'RNA_product').
range_in(increases_localization_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, 'RNA_product').
range_in(decreases_localization_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, 'RNA_product').
range_in(affects_metabolic_processing_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, 'RNA_product').
range_in(increases_metabolic_processing_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, 'RNA_product').
range_in(decreases_metabolic_processing_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, 'RNA_product').
range_in(affects_molecular_modification_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, 'RNA_product').
range_in(increases_molecular_modification_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, 'RNA_product').
range_in(decreases_molecular_modification_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, 'RNA_product').
range_in(affects_synthesis_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, 'RNA_product').
range_in(increases_synthesis_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, 'RNA_product').
range_in(decreases_synthesis_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, 'RNA_product').
range_in(affects_degradation_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, 'RNA_product').
range_in(increases_degradation_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, 'RNA_product').
range_in(decreases_degradation_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, 'RNA_product').
range_in(affects_mutation_rate_of, genomic_entity, 'RNA_product').
class_slot('RNA_product', increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, 'RNA_product').
range_in(increases_mutation_rate_of, genomic_entity, 'RNA_product').
class_slot('RNA_product', decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, 'RNA_product').
range_in(decreases_mutation_rate_of, genomic_entity, 'RNA_product').
class_slot('RNA_product', affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, 'RNA_product').
range_in(affects_response_to, molecular_entity, 'RNA_product').
class_slot('RNA_product', increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, 'RNA_product').
range_in(increases_response_to, molecular_entity, 'RNA_product').
class_slot('RNA_product', decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, 'RNA_product').
range_in(decreases_response_to, molecular_entity, 'RNA_product').
class_slot('RNA_product', affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, 'RNA_product').
range_in(affects_splicing_of, transcript, 'RNA_product').
class_slot('RNA_product', increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, 'RNA_product').
range_in(increases_splicing_of, transcript, 'RNA_product').
class_slot('RNA_product', decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, 'RNA_product').
range_in(decreases_splicing_of, transcript, 'RNA_product').
class_slot('RNA_product', affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, 'RNA_product').
range_in(affects_stability_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, 'RNA_product').
range_in(increases_stability_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, 'RNA_product').
range_in(decreases_stability_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, 'RNA_product').
range_in(affects_transport_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, 'RNA_product').
range_in(increases_transport_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, 'RNA_product').
range_in(decreases_transport_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, 'RNA_product').
range_in(affects_secretion_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, 'RNA_product').
range_in(increases_secretion_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, 'RNA_product').
range_in(decreases_secretion_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, 'RNA_product').
range_in(affects_uptake_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, 'RNA_product').
range_in(increases_uptake_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, 'RNA_product').
range_in(decreases_uptake_of, molecular_entity, 'RNA_product').
class_slot('RNA_product', regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, 'RNA_product').
range_in(regulates_entity_to_entity, molecular_entity, 'RNA_product').
class_slot('RNA_product', biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, 'RNA_product').
range_in(biomarker_for, disease_or_phenotypic_feature, 'RNA_product').
class_slot('RNA_product', in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, 'RNA_product').
range_in(in_taxon, organism_taxon, 'RNA_product').
class_slot('RNA_product', has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, 'RNA_product').
class_slot('RNA_product', in_pathway_with).
required(in_pathway_with).
slotrange(gene_or_gene_product).
multivalued_in(in_pathway_with, 'RNA_product').
range_in(in_pathway_with, gene_or_gene_product, 'RNA_product').
class_slot('RNA_product', in_complex_with).
required(in_complex_with).
slotrange(gene_or_gene_product).
multivalued_in(in_complex_with, 'RNA_product').
range_in(in_complex_with, gene_or_gene_product, 'RNA_product').
class_slot('RNA_product', in_cell_population_with).
required(in_cell_population_with).
slotrange(gene_or_gene_product).
multivalued_in(in_cell_population_with, 'RNA_product').
range_in(in_cell_population_with, gene_or_gene_product, 'RNA_product').
class_slot('RNA_product', expressed_in).
required(expressed_in).
slotrange(anatomical_entity).
multivalued_in(expressed_in, 'RNA_product').
range_in(expressed_in, anatomical_entity, 'RNA_product').
class('RNA_product_isoform').
mixin('RNA_product_isoform', gene_product_isoform).
is_a('RNA_product_isoform', 'RNA_product').
has_uri('RNA_product_isoform', 'http://w3id.org/biolink/vocab/RNAProductIsoform').
class_slot('RNA_product_isoform', id).
required(id).
slotrange(identifier_type).
required_in(id, 'RNA_product_isoform').
range_in(id, identifier_type, 'RNA_product_isoform').
class_slot('RNA_product_isoform', name).
required(name).
slotrange(symbol_type).
range_in(name, symbol_type, 'RNA_product_isoform').
class_slot('RNA_product_isoform', category).
required(category).
slotrange(iri_type).
multivalued_in(category, 'RNA_product_isoform').
range_in(category, iri_type, 'RNA_product_isoform').
class_slot('RNA_product_isoform', related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, 'RNA_product_isoform').
range_in(related_to, named_thing, 'RNA_product_isoform').
class_slot('RNA_product_isoform', interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, 'RNA_product_isoform').
range_in(interacts_with, named_thing, 'RNA_product_isoform').
class_slot('RNA_product_isoform', node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, 'RNA_product_isoform').
class_slot('RNA_product_isoform', iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, 'RNA_product_isoform').
class_slot('RNA_product_isoform', synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, 'RNA_product_isoform').
range_in(synonym, label_type, 'RNA_product_isoform').
class_slot('RNA_product_isoform', full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, 'RNA_product_isoform').
class_slot('RNA_product_isoform', description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, 'RNA_product_isoform').
class_slot('RNA_product_isoform', systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, 'RNA_product_isoform').
class_slot('RNA_product_isoform', has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, 'RNA_product_isoform').
range_in(has_phenotype, phenotypic_feature, 'RNA_product_isoform').
class_slot('RNA_product_isoform', molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, 'RNA_product_isoform').
range_in(molecularly_interacts_with, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, 'RNA_product_isoform').
range_in(affects_abundance_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, 'RNA_product_isoform').
range_in(increases_abundance_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, 'RNA_product_isoform').
range_in(decreases_abundance_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, 'RNA_product_isoform').
range_in(affects_activity_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, 'RNA_product_isoform').
range_in(increases_activity_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, 'RNA_product_isoform').
range_in(decreases_activity_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, 'RNA_product_isoform').
range_in(affects_expression_of, genomic_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, 'RNA_product_isoform').
range_in(increases_expression_of, genomic_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, 'RNA_product_isoform').
range_in(decreases_expression_of, genomic_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, 'RNA_product_isoform').
range_in(affects_folding_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, 'RNA_product_isoform').
range_in(increases_folding_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, 'RNA_product_isoform').
range_in(decreases_folding_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, 'RNA_product_isoform').
range_in(affects_localization_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, 'RNA_product_isoform').
range_in(increases_localization_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, 'RNA_product_isoform').
range_in(decreases_localization_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, 'RNA_product_isoform').
range_in(affects_metabolic_processing_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, 'RNA_product_isoform').
range_in(increases_metabolic_processing_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, 'RNA_product_isoform').
range_in(decreases_metabolic_processing_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, 'RNA_product_isoform').
range_in(affects_molecular_modification_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, 'RNA_product_isoform').
range_in(increases_molecular_modification_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, 'RNA_product_isoform').
range_in(decreases_molecular_modification_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, 'RNA_product_isoform').
range_in(affects_synthesis_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, 'RNA_product_isoform').
range_in(increases_synthesis_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, 'RNA_product_isoform').
range_in(decreases_synthesis_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, 'RNA_product_isoform').
range_in(affects_degradation_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, 'RNA_product_isoform').
range_in(increases_degradation_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, 'RNA_product_isoform').
range_in(decreases_degradation_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, 'RNA_product_isoform').
range_in(affects_mutation_rate_of, genomic_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, 'RNA_product_isoform').
range_in(increases_mutation_rate_of, genomic_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, 'RNA_product_isoform').
range_in(decreases_mutation_rate_of, genomic_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, 'RNA_product_isoform').
range_in(affects_response_to, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, 'RNA_product_isoform').
range_in(increases_response_to, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, 'RNA_product_isoform').
range_in(decreases_response_to, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, 'RNA_product_isoform').
range_in(affects_splicing_of, transcript, 'RNA_product_isoform').
class_slot('RNA_product_isoform', increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, 'RNA_product_isoform').
range_in(increases_splicing_of, transcript, 'RNA_product_isoform').
class_slot('RNA_product_isoform', decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, 'RNA_product_isoform').
range_in(decreases_splicing_of, transcript, 'RNA_product_isoform').
class_slot('RNA_product_isoform', affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, 'RNA_product_isoform').
range_in(affects_stability_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, 'RNA_product_isoform').
range_in(increases_stability_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, 'RNA_product_isoform').
range_in(decreases_stability_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, 'RNA_product_isoform').
range_in(affects_transport_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, 'RNA_product_isoform').
range_in(increases_transport_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, 'RNA_product_isoform').
range_in(decreases_transport_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, 'RNA_product_isoform').
range_in(affects_secretion_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, 'RNA_product_isoform').
range_in(increases_secretion_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, 'RNA_product_isoform').
range_in(decreases_secretion_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, 'RNA_product_isoform').
range_in(affects_uptake_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, 'RNA_product_isoform').
range_in(increases_uptake_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, 'RNA_product_isoform').
range_in(decreases_uptake_of, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, 'RNA_product_isoform').
range_in(regulates_entity_to_entity, molecular_entity, 'RNA_product_isoform').
class_slot('RNA_product_isoform', biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, 'RNA_product_isoform').
range_in(biomarker_for, disease_or_phenotypic_feature, 'RNA_product_isoform').
class_slot('RNA_product_isoform', in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, 'RNA_product_isoform').
range_in(in_taxon, organism_taxon, 'RNA_product_isoform').
class_slot('RNA_product_isoform', has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, 'RNA_product_isoform').
class_slot('RNA_product_isoform', in_pathway_with).
required(in_pathway_with).
slotrange(gene_or_gene_product).
multivalued_in(in_pathway_with, 'RNA_product_isoform').
range_in(in_pathway_with, gene_or_gene_product, 'RNA_product_isoform').
class_slot('RNA_product_isoform', in_complex_with).
required(in_complex_with).
slotrange(gene_or_gene_product).
multivalued_in(in_complex_with, 'RNA_product_isoform').
range_in(in_complex_with, gene_or_gene_product, 'RNA_product_isoform').
class_slot('RNA_product_isoform', in_cell_population_with).
required(in_cell_population_with).
slotrange(gene_or_gene_product).
multivalued_in(in_cell_population_with, 'RNA_product_isoform').
range_in(in_cell_population_with, gene_or_gene_product, 'RNA_product_isoform').
class_slot('RNA_product_isoform', expressed_in).
required(expressed_in).
slotrange(anatomical_entity).
multivalued_in(expressed_in, 'RNA_product_isoform').
range_in(expressed_in, anatomical_entity, 'RNA_product_isoform').
class(sensitivity_quantifier).
is_a(sensitivity_quantifier, relationship_quantifier).
has_uri(sensitivity_quantifier, 'http://w3id.org/biolink/vocab/SensitivityQuantifier').
class(sequence_feature_relationship).
is_a(sequence_feature_relationship, association).
defining_slots(association, [subject, object]).
has_uri(sequence_feature_relationship, 'http://w3id.org/biolink/vocab/SequenceFeatureRelationship').
class_slot(sequence_feature_relationship, id).
required(id).
slotrange(identifier_type).
required_in(id, sequence_feature_relationship).
range_in(id, identifier_type, sequence_feature_relationship).
class_slot(sequence_feature_relationship, subject).
required(subject).
slotrange(genomic_entity).
required_in(subject, sequence_feature_relationship).
range_in(subject, genomic_entity, sequence_feature_relationship).
class_slot(sequence_feature_relationship, relation).
required(relation).
slotrange(iri_type).
required_in(relation, sequence_feature_relationship).
range_in(relation, iri_type, sequence_feature_relationship).
class_slot(sequence_feature_relationship, object).
required(object).
slotrange(genomic_entity).
required_in(object, sequence_feature_relationship).
range_in(object, genomic_entity, sequence_feature_relationship).
class_slot(sequence_feature_relationship, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, sequence_feature_relationship).
class_slot(sequence_feature_relationship, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, sequence_feature_relationship).
class_slot(sequence_feature_relationship, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, sequence_feature_relationship).
range_in(qualifiers, ontology_class, sequence_feature_relationship).
class_slot(sequence_feature_relationship, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, sequence_feature_relationship).
range_in(publications, publication, sequence_feature_relationship).
class_slot(sequence_feature_relationship, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, sequence_feature_relationship).
class_slot(sequence_feature_relationship, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, sequence_feature_relationship).
class(sequence_variant).
is_a(sequence_variant, genomic_entity).
has_uri(sequence_variant, 'http://w3id.org/biolink/vocab/SequenceVariant').
class_slot(sequence_variant, id).
required(id).
slotrange(identifier_type).
required_in(id, sequence_variant).
range_in(id, identifier_type, sequence_variant).
class_slot(sequence_variant, name).
required(name).
slotrange(label_type).
range_in(name, label_type, sequence_variant).
class_slot(sequence_variant, category).
required(category).
slotrange(iri_type).
multivalued_in(category, sequence_variant).
range_in(category, iri_type, sequence_variant).
class_slot(sequence_variant, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, sequence_variant).
range_in(related_to, named_thing, sequence_variant).
class_slot(sequence_variant, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, sequence_variant).
range_in(interacts_with, named_thing, sequence_variant).
class_slot(sequence_variant, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, sequence_variant).
class_slot(sequence_variant, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, sequence_variant).
class_slot(sequence_variant, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, sequence_variant).
range_in(synonym, label_type, sequence_variant).
class_slot(sequence_variant, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, sequence_variant).
class_slot(sequence_variant, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, sequence_variant).
class_slot(sequence_variant, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, sequence_variant).
class_slot(sequence_variant, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, sequence_variant).
range_in(has_phenotype, phenotypic_feature, sequence_variant).
class_slot(sequence_variant, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, sequence_variant).
range_in(molecularly_interacts_with, molecular_entity, sequence_variant).
class_slot(sequence_variant, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, sequence_variant).
range_in(affects_abundance_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, sequence_variant).
range_in(increases_abundance_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, sequence_variant).
range_in(decreases_abundance_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, sequence_variant).
range_in(affects_activity_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, sequence_variant).
range_in(increases_activity_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, sequence_variant).
range_in(decreases_activity_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, sequence_variant).
range_in(affects_expression_of, genomic_entity, sequence_variant).
class_slot(sequence_variant, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, sequence_variant).
range_in(increases_expression_of, genomic_entity, sequence_variant).
class_slot(sequence_variant, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, sequence_variant).
range_in(decreases_expression_of, genomic_entity, sequence_variant).
class_slot(sequence_variant, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, sequence_variant).
range_in(affects_folding_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, sequence_variant).
range_in(increases_folding_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, sequence_variant).
range_in(decreases_folding_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, sequence_variant).
range_in(affects_localization_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, sequence_variant).
range_in(increases_localization_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, sequence_variant).
range_in(decreases_localization_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, sequence_variant).
range_in(affects_metabolic_processing_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, sequence_variant).
range_in(increases_metabolic_processing_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, sequence_variant).
range_in(decreases_metabolic_processing_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, sequence_variant).
range_in(affects_molecular_modification_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, sequence_variant).
range_in(increases_molecular_modification_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, sequence_variant).
range_in(decreases_molecular_modification_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, sequence_variant).
range_in(affects_synthesis_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, sequence_variant).
range_in(increases_synthesis_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, sequence_variant).
range_in(decreases_synthesis_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, sequence_variant).
range_in(affects_degradation_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, sequence_variant).
range_in(increases_degradation_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, sequence_variant).
range_in(decreases_degradation_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, sequence_variant).
range_in(affects_mutation_rate_of, genomic_entity, sequence_variant).
class_slot(sequence_variant, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, sequence_variant).
range_in(increases_mutation_rate_of, genomic_entity, sequence_variant).
class_slot(sequence_variant, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, sequence_variant).
range_in(decreases_mutation_rate_of, genomic_entity, sequence_variant).
class_slot(sequence_variant, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, sequence_variant).
range_in(affects_response_to, molecular_entity, sequence_variant).
class_slot(sequence_variant, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, sequence_variant).
range_in(increases_response_to, molecular_entity, sequence_variant).
class_slot(sequence_variant, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, sequence_variant).
range_in(decreases_response_to, molecular_entity, sequence_variant).
class_slot(sequence_variant, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, sequence_variant).
range_in(affects_splicing_of, transcript, sequence_variant).
class_slot(sequence_variant, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, sequence_variant).
range_in(increases_splicing_of, transcript, sequence_variant).
class_slot(sequence_variant, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, sequence_variant).
range_in(decreases_splicing_of, transcript, sequence_variant).
class_slot(sequence_variant, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, sequence_variant).
range_in(affects_stability_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, sequence_variant).
range_in(increases_stability_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, sequence_variant).
range_in(decreases_stability_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, sequence_variant).
range_in(affects_transport_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, sequence_variant).
range_in(increases_transport_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, sequence_variant).
range_in(decreases_transport_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, sequence_variant).
range_in(affects_secretion_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, sequence_variant).
range_in(increases_secretion_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, sequence_variant).
range_in(decreases_secretion_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, sequence_variant).
range_in(affects_uptake_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, sequence_variant).
range_in(increases_uptake_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, sequence_variant).
range_in(decreases_uptake_of, molecular_entity, sequence_variant).
class_slot(sequence_variant, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, sequence_variant).
range_in(regulates_entity_to_entity, molecular_entity, sequence_variant).
class_slot(sequence_variant, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, sequence_variant).
range_in(biomarker_for, disease_or_phenotypic_feature, sequence_variant).
class_slot(sequence_variant, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, sequence_variant).
range_in(in_taxon, organism_taxon, sequence_variant).
class_slot(sequence_variant, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, sequence_variant).
class_slot(sequence_variant, has_gene).
required(has_gene).
slotrange(gene).
multivalued_in(has_gene, sequence_variant).
range_in(has_gene, gene, sequence_variant).
class(sequence_variant_modulates_treatment_association).
is_a(sequence_variant_modulates_treatment_association, association).
defining_slots(association, [subject, object]).
has_uri(sequence_variant_modulates_treatment_association, 'http://w3id.org/biolink/vocab/SequenceVariantModulatesTreatmentAssociation').
class_slot(sequence_variant_modulates_treatment_association, id).
required(id).
slotrange(identifier_type).
required_in(id, sequence_variant_modulates_treatment_association).
range_in(id, identifier_type, sequence_variant_modulates_treatment_association).
class_slot(sequence_variant_modulates_treatment_association, subject).
required(subject).
slotrange(sequence_variant).
required_in(subject, sequence_variant_modulates_treatment_association).
range_in(subject, sequence_variant, sequence_variant_modulates_treatment_association).
class_slot(sequence_variant_modulates_treatment_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, sequence_variant_modulates_treatment_association).
range_in(relation, iri_type, sequence_variant_modulates_treatment_association).
class_slot(sequence_variant_modulates_treatment_association, object).
required(object).
slotrange(treatment).
required_in(object, sequence_variant_modulates_treatment_association).
range_in(object, treatment, sequence_variant_modulates_treatment_association).
class_slot(sequence_variant_modulates_treatment_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, sequence_variant_modulates_treatment_association).
class_slot(sequence_variant_modulates_treatment_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, sequence_variant_modulates_treatment_association).
class_slot(sequence_variant_modulates_treatment_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, sequence_variant_modulates_treatment_association).
range_in(qualifiers, ontology_class, sequence_variant_modulates_treatment_association).
class_slot(sequence_variant_modulates_treatment_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, sequence_variant_modulates_treatment_association).
range_in(publications, publication, sequence_variant_modulates_treatment_association).
class_slot(sequence_variant_modulates_treatment_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, sequence_variant_modulates_treatment_association).
class_slot(sequence_variant_modulates_treatment_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, sequence_variant_modulates_treatment_association).
class(severity_value).
is_a(severity_value, attribute).
has_uri(severity_value, 'http://w3id.org/biolink/vocab/SeverityValue').
class_slot(severity_value, id).
required(id).
slotrange(identifier_type).
required_in(id, severity_value).
range_in(id, identifier_type, severity_value).
class_slot(severity_value, name).
required(name).
slotrange(label_type).
range_in(name, label_type, severity_value).
class_slot(severity_value, category).
required(category).
slotrange(iri_type).
multivalued_in(category, severity_value).
range_in(category, iri_type, severity_value).
class_slot(severity_value, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, severity_value).
range_in(related_to, named_thing, severity_value).
class_slot(severity_value, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, severity_value).
range_in(interacts_with, named_thing, severity_value).
class_slot(severity_value, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, severity_value).
class_slot(severity_value, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, severity_value).
class_slot(severity_value, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, severity_value).
range_in(synonym, label_type, severity_value).
class_slot(severity_value, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, severity_value).
class_slot(severity_value, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, severity_value).
class_slot(severity_value, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, severity_value).
class_slot(severity_value, subclass_of).
required(subclass_of).
slotrange(ontology_class).
multivalued_in(subclass_of, severity_value).
range_in(subclass_of, ontology_class, severity_value).
class(specificity_quantifier).
is_a(specificity_quantifier, relationship_quantifier).
has_uri(specificity_quantifier, 'http://w3id.org/biolink/vocab/SpecificityQuantifier').
class(thing_to_disease_or_phenotypic_feature_association).
is_a(thing_to_disease_or_phenotypic_feature_association, association).
defining_slots(association, [object]).
has_uri(thing_to_disease_or_phenotypic_feature_association, 'http://w3id.org/biolink/vocab/ThingToDiseaseOrPhenotypicFeatureAssociation').
class_slot(thing_to_disease_or_phenotypic_feature_association, id).
required(id).
slotrange(identifier_type).
required_in(id, thing_to_disease_or_phenotypic_feature_association).
range_in(id, identifier_type, thing_to_disease_or_phenotypic_feature_association).
class_slot(thing_to_disease_or_phenotypic_feature_association, subject).
required(subject).
slotrange(iri_type).
required_in(subject, thing_to_disease_or_phenotypic_feature_association).
range_in(subject, iri_type, thing_to_disease_or_phenotypic_feature_association).
class_slot(thing_to_disease_or_phenotypic_feature_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, thing_to_disease_or_phenotypic_feature_association).
range_in(relation, iri_type, thing_to_disease_or_phenotypic_feature_association).
class_slot(thing_to_disease_or_phenotypic_feature_association, object).
required(object).
slotrange(disease_or_phenotypic_feature).
required_in(object, thing_to_disease_or_phenotypic_feature_association).
range_in(object, disease_or_phenotypic_feature, thing_to_disease_or_phenotypic_feature_association).
class_slot(thing_to_disease_or_phenotypic_feature_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, thing_to_disease_or_phenotypic_feature_association).
class_slot(thing_to_disease_or_phenotypic_feature_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, thing_to_disease_or_phenotypic_feature_association).
class_slot(thing_to_disease_or_phenotypic_feature_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, thing_to_disease_or_phenotypic_feature_association).
range_in(qualifiers, ontology_class, thing_to_disease_or_phenotypic_feature_association).
class_slot(thing_to_disease_or_phenotypic_feature_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, thing_to_disease_or_phenotypic_feature_association).
range_in(publications, publication, thing_to_disease_or_phenotypic_feature_association).
class_slot(thing_to_disease_or_phenotypic_feature_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, thing_to_disease_or_phenotypic_feature_association).
class_slot(thing_to_disease_or_phenotypic_feature_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, thing_to_disease_or_phenotypic_feature_association).
class(thing_with_taxon).
has_uri(thing_with_taxon, 'http://w3id.org/biolink/vocab/ThingWithTaxon').
class_slot(thing_with_taxon, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, thing_with_taxon).
range_in(in_taxon, organism_taxon, thing_with_taxon).
class(transcript).
is_a(transcript, genomic_entity).
has_uri(transcript, 'http://w3id.org/biolink/vocab/Transcript').
class_slot(transcript, id).
required(id).
slotrange(identifier_type).
required_in(id, transcript).
range_in(id, identifier_type, transcript).
class_slot(transcript, name).
required(name).
slotrange(label_type).
range_in(name, label_type, transcript).
class_slot(transcript, category).
required(category).
slotrange(iri_type).
multivalued_in(category, transcript).
range_in(category, iri_type, transcript).
class_slot(transcript, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, transcript).
range_in(related_to, named_thing, transcript).
class_slot(transcript, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, transcript).
range_in(interacts_with, named_thing, transcript).
class_slot(transcript, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, transcript).
class_slot(transcript, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, transcript).
class_slot(transcript, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, transcript).
range_in(synonym, label_type, transcript).
class_slot(transcript, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, transcript).
class_slot(transcript, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, transcript).
class_slot(transcript, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, transcript).
class_slot(transcript, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, transcript).
range_in(has_phenotype, phenotypic_feature, transcript).
class_slot(transcript, molecularly_interacts_with).
required(molecularly_interacts_with).
slotrange(molecular_entity).
multivalued_in(molecularly_interacts_with, transcript).
range_in(molecularly_interacts_with, molecular_entity, transcript).
class_slot(transcript, affects_abundance_of).
required(affects_abundance_of).
slotrange(molecular_entity).
multivalued_in(affects_abundance_of, transcript).
range_in(affects_abundance_of, molecular_entity, transcript).
class_slot(transcript, increases_abundance_of).
required(increases_abundance_of).
slotrange(molecular_entity).
multivalued_in(increases_abundance_of, transcript).
range_in(increases_abundance_of, molecular_entity, transcript).
class_slot(transcript, decreases_abundance_of).
required(decreases_abundance_of).
slotrange(molecular_entity).
multivalued_in(decreases_abundance_of, transcript).
range_in(decreases_abundance_of, molecular_entity, transcript).
class_slot(transcript, affects_activity_of).
required(affects_activity_of).
slotrange(molecular_entity).
multivalued_in(affects_activity_of, transcript).
range_in(affects_activity_of, molecular_entity, transcript).
class_slot(transcript, increases_activity_of).
required(increases_activity_of).
slotrange(molecular_entity).
multivalued_in(increases_activity_of, transcript).
range_in(increases_activity_of, molecular_entity, transcript).
class_slot(transcript, decreases_activity_of).
required(decreases_activity_of).
slotrange(molecular_entity).
multivalued_in(decreases_activity_of, transcript).
range_in(decreases_activity_of, molecular_entity, transcript).
class_slot(transcript, affects_expression_of).
required(affects_expression_of).
slotrange(genomic_entity).
multivalued_in(affects_expression_of, transcript).
range_in(affects_expression_of, genomic_entity, transcript).
class_slot(transcript, increases_expression_of).
required(increases_expression_of).
slotrange(genomic_entity).
multivalued_in(increases_expression_of, transcript).
range_in(increases_expression_of, genomic_entity, transcript).
class_slot(transcript, decreases_expression_of).
required(decreases_expression_of).
slotrange(genomic_entity).
multivalued_in(decreases_expression_of, transcript).
range_in(decreases_expression_of, genomic_entity, transcript).
class_slot(transcript, affects_folding_of).
required(affects_folding_of).
slotrange(molecular_entity).
multivalued_in(affects_folding_of, transcript).
range_in(affects_folding_of, molecular_entity, transcript).
class_slot(transcript, increases_folding_of).
required(increases_folding_of).
slotrange(molecular_entity).
multivalued_in(increases_folding_of, transcript).
range_in(increases_folding_of, molecular_entity, transcript).
class_slot(transcript, decreases_folding_of).
required(decreases_folding_of).
slotrange(molecular_entity).
multivalued_in(decreases_folding_of, transcript).
range_in(decreases_folding_of, molecular_entity, transcript).
class_slot(transcript, affects_localization_of).
required(affects_localization_of).
slotrange(molecular_entity).
multivalued_in(affects_localization_of, transcript).
range_in(affects_localization_of, molecular_entity, transcript).
class_slot(transcript, increases_localization_of).
required(increases_localization_of).
slotrange(molecular_entity).
multivalued_in(increases_localization_of, transcript).
range_in(increases_localization_of, molecular_entity, transcript).
class_slot(transcript, decreases_localization_of).
required(decreases_localization_of).
slotrange(molecular_entity).
multivalued_in(decreases_localization_of, transcript).
range_in(decreases_localization_of, molecular_entity, transcript).
class_slot(transcript, affects_metabolic_processing_of).
required(affects_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(affects_metabolic_processing_of, transcript).
range_in(affects_metabolic_processing_of, molecular_entity, transcript).
class_slot(transcript, increases_metabolic_processing_of).
required(increases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(increases_metabolic_processing_of, transcript).
range_in(increases_metabolic_processing_of, molecular_entity, transcript).
class_slot(transcript, decreases_metabolic_processing_of).
required(decreases_metabolic_processing_of).
slotrange(molecular_entity).
multivalued_in(decreases_metabolic_processing_of, transcript).
range_in(decreases_metabolic_processing_of, molecular_entity, transcript).
class_slot(transcript, affects_molecular_modification_of).
required(affects_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(affects_molecular_modification_of, transcript).
range_in(affects_molecular_modification_of, molecular_entity, transcript).
class_slot(transcript, increases_molecular_modification_of).
required(increases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(increases_molecular_modification_of, transcript).
range_in(increases_molecular_modification_of, molecular_entity, transcript).
class_slot(transcript, decreases_molecular_modification_of).
required(decreases_molecular_modification_of).
slotrange(molecular_entity).
multivalued_in(decreases_molecular_modification_of, transcript).
range_in(decreases_molecular_modification_of, molecular_entity, transcript).
class_slot(transcript, affects_synthesis_of).
required(affects_synthesis_of).
slotrange(molecular_entity).
multivalued_in(affects_synthesis_of, transcript).
range_in(affects_synthesis_of, molecular_entity, transcript).
class_slot(transcript, increases_synthesis_of).
required(increases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(increases_synthesis_of, transcript).
range_in(increases_synthesis_of, molecular_entity, transcript).
class_slot(transcript, decreases_synthesis_of).
required(decreases_synthesis_of).
slotrange(molecular_entity).
multivalued_in(decreases_synthesis_of, transcript).
range_in(decreases_synthesis_of, molecular_entity, transcript).
class_slot(transcript, affects_degradation_of).
required(affects_degradation_of).
slotrange(molecular_entity).
multivalued_in(affects_degradation_of, transcript).
range_in(affects_degradation_of, molecular_entity, transcript).
class_slot(transcript, increases_degradation_of).
required(increases_degradation_of).
slotrange(molecular_entity).
multivalued_in(increases_degradation_of, transcript).
range_in(increases_degradation_of, molecular_entity, transcript).
class_slot(transcript, decreases_degradation_of).
required(decreases_degradation_of).
slotrange(molecular_entity).
multivalued_in(decreases_degradation_of, transcript).
range_in(decreases_degradation_of, molecular_entity, transcript).
class_slot(transcript, affects_mutation_rate_of).
required(affects_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(affects_mutation_rate_of, transcript).
range_in(affects_mutation_rate_of, genomic_entity, transcript).
class_slot(transcript, increases_mutation_rate_of).
required(increases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(increases_mutation_rate_of, transcript).
range_in(increases_mutation_rate_of, genomic_entity, transcript).
class_slot(transcript, decreases_mutation_rate_of).
required(decreases_mutation_rate_of).
slotrange(genomic_entity).
multivalued_in(decreases_mutation_rate_of, transcript).
range_in(decreases_mutation_rate_of, genomic_entity, transcript).
class_slot(transcript, affects_response_to).
required(affects_response_to).
slotrange(molecular_entity).
multivalued_in(affects_response_to, transcript).
range_in(affects_response_to, molecular_entity, transcript).
class_slot(transcript, increases_response_to).
required(increases_response_to).
slotrange(molecular_entity).
multivalued_in(increases_response_to, transcript).
range_in(increases_response_to, molecular_entity, transcript).
class_slot(transcript, decreases_response_to).
required(decreases_response_to).
slotrange(molecular_entity).
multivalued_in(decreases_response_to, transcript).
range_in(decreases_response_to, molecular_entity, transcript).
class_slot(transcript, affects_splicing_of).
required(affects_splicing_of).
slotrange(transcript).
multivalued_in(affects_splicing_of, transcript).
range_in(affects_splicing_of, transcript, transcript).
class_slot(transcript, increases_splicing_of).
required(increases_splicing_of).
slotrange(transcript).
multivalued_in(increases_splicing_of, transcript).
range_in(increases_splicing_of, transcript, transcript).
class_slot(transcript, decreases_splicing_of).
required(decreases_splicing_of).
slotrange(transcript).
multivalued_in(decreases_splicing_of, transcript).
range_in(decreases_splicing_of, transcript, transcript).
class_slot(transcript, affects_stability_of).
required(affects_stability_of).
slotrange(molecular_entity).
multivalued_in(affects_stability_of, transcript).
range_in(affects_stability_of, molecular_entity, transcript).
class_slot(transcript, increases_stability_of).
required(increases_stability_of).
slotrange(molecular_entity).
multivalued_in(increases_stability_of, transcript).
range_in(increases_stability_of, molecular_entity, transcript).
class_slot(transcript, decreases_stability_of).
required(decreases_stability_of).
slotrange(molecular_entity).
multivalued_in(decreases_stability_of, transcript).
range_in(decreases_stability_of, molecular_entity, transcript).
class_slot(transcript, affects_transport_of).
required(affects_transport_of).
slotrange(molecular_entity).
multivalued_in(affects_transport_of, transcript).
range_in(affects_transport_of, molecular_entity, transcript).
class_slot(transcript, increases_transport_of).
required(increases_transport_of).
slotrange(molecular_entity).
multivalued_in(increases_transport_of, transcript).
range_in(increases_transport_of, molecular_entity, transcript).
class_slot(transcript, decreases_transport_of).
required(decreases_transport_of).
slotrange(molecular_entity).
multivalued_in(decreases_transport_of, transcript).
range_in(decreases_transport_of, molecular_entity, transcript).
class_slot(transcript, affects_secretion_of).
required(affects_secretion_of).
slotrange(molecular_entity).
multivalued_in(affects_secretion_of, transcript).
range_in(affects_secretion_of, molecular_entity, transcript).
class_slot(transcript, increases_secretion_of).
required(increases_secretion_of).
slotrange(molecular_entity).
multivalued_in(increases_secretion_of, transcript).
range_in(increases_secretion_of, molecular_entity, transcript).
class_slot(transcript, decreases_secretion_of).
required(decreases_secretion_of).
slotrange(molecular_entity).
multivalued_in(decreases_secretion_of, transcript).
range_in(decreases_secretion_of, molecular_entity, transcript).
class_slot(transcript, affects_uptake_of).
required(affects_uptake_of).
slotrange(molecular_entity).
multivalued_in(affects_uptake_of, transcript).
range_in(affects_uptake_of, molecular_entity, transcript).
class_slot(transcript, increases_uptake_of).
required(increases_uptake_of).
slotrange(molecular_entity).
multivalued_in(increases_uptake_of, transcript).
range_in(increases_uptake_of, molecular_entity, transcript).
class_slot(transcript, decreases_uptake_of).
required(decreases_uptake_of).
slotrange(molecular_entity).
multivalued_in(decreases_uptake_of, transcript).
range_in(decreases_uptake_of, molecular_entity, transcript).
class_slot(transcript, regulates_entity_to_entity).
required(regulates_entity_to_entity).
slotrange(molecular_entity).
multivalued_in(regulates_entity_to_entity, transcript).
range_in(regulates_entity_to_entity, molecular_entity, transcript).
class_slot(transcript, biomarker_for).
required(biomarker_for).
slotrange(disease_or_phenotypic_feature).
multivalued_in(biomarker_for, transcript).
range_in(biomarker_for, disease_or_phenotypic_feature, transcript).
class_slot(transcript, in_taxon).
required(in_taxon).
slotrange(organism_taxon).
multivalued_in(in_taxon, transcript).
range_in(in_taxon, organism_taxon, transcript).
class_slot(transcript, has_biological_sequence).
required(has_biological_sequence).
slotrange(biological_sequence).
range_in(has_biological_sequence, biological_sequence, transcript).
class(transcript_to_gene_relationship).
is_a(transcript_to_gene_relationship, sequence_feature_relationship).
defining_slots(sequence_feature_relationship, [subject, object]).
has_uri(transcript_to_gene_relationship, 'http://w3id.org/biolink/vocab/TranscriptToGeneRelationship').
class_slot(transcript_to_gene_relationship, id).
required(id).
slotrange(identifier_type).
required_in(id, transcript_to_gene_relationship).
range_in(id, identifier_type, transcript_to_gene_relationship).
class_slot(transcript_to_gene_relationship, subject).
required(subject).
slotrange(transcript).
required_in(subject, transcript_to_gene_relationship).
range_in(subject, transcript, transcript_to_gene_relationship).
class_slot(transcript_to_gene_relationship, relation).
required(relation).
slotrange(iri_type).
required_in(relation, transcript_to_gene_relationship).
range_in(relation, iri_type, transcript_to_gene_relationship).
class_slot(transcript_to_gene_relationship, object).
required(object).
slotrange(gene).
required_in(object, transcript_to_gene_relationship).
range_in(object, gene, transcript_to_gene_relationship).
class_slot(transcript_to_gene_relationship, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, transcript_to_gene_relationship).
class_slot(transcript_to_gene_relationship, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, transcript_to_gene_relationship).
class_slot(transcript_to_gene_relationship, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, transcript_to_gene_relationship).
range_in(qualifiers, ontology_class, transcript_to_gene_relationship).
class_slot(transcript_to_gene_relationship, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, transcript_to_gene_relationship).
range_in(publications, publication, transcript_to_gene_relationship).
class_slot(transcript_to_gene_relationship, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, transcript_to_gene_relationship).
class_slot(transcript_to_gene_relationship, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, transcript_to_gene_relationship).
class(treatment).
is_a(treatment, environment).
has_uri(treatment, 'http://w3id.org/biolink/vocab/Treatment').
class_slot(treatment, id).
required(id).
slotrange(identifier_type).
required_in(id, treatment).
range_in(id, identifier_type, treatment).
class_slot(treatment, name).
required(name).
slotrange(label_type).
range_in(name, label_type, treatment).
class_slot(treatment, category).
required(category).
slotrange(iri_type).
multivalued_in(category, treatment).
range_in(category, iri_type, treatment).
class_slot(treatment, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, treatment).
range_in(related_to, named_thing, treatment).
class_slot(treatment, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, treatment).
range_in(interacts_with, named_thing, treatment).
class_slot(treatment, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, treatment).
class_slot(treatment, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, treatment).
class_slot(treatment, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, treatment).
range_in(synonym, label_type, treatment).
class_slot(treatment, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, treatment).
class_slot(treatment, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, treatment).
class_slot(treatment, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, treatment).
class_slot(treatment, has_phenotype).
required(has_phenotype).
slotrange(phenotypic_feature).
multivalued_in(has_phenotype, treatment).
range_in(has_phenotype, phenotypic_feature, treatment).
class_slot(treatment, treats).
required(treats).
slotrange(disease_or_phenotypic_feature).
multivalued_in(treats, treatment).
required_in(treats, treatment).
range_in(treats, disease_or_phenotypic_feature, treatment).
class_slot(treatment, has_exposure_parts).
required(has_exposure_parts).
slotrange(drug_exposure).
multivalued_in(has_exposure_parts, treatment).
required_in(has_exposure_parts, treatment).
range_in(has_exposure_parts, drug_exposure, treatment).
class(variant_to_disease_association).
mixin(variant_to_disease_association, variant_to_thing_association).
mixin(variant_to_disease_association, entity_to_disease_association).
is_a(variant_to_disease_association, association).
defining_slots(association, [subject, object]).
has_uri(variant_to_disease_association, 'http://w3id.org/biolink/vocab/VariantToDiseaseAssociation').
class_slot(variant_to_disease_association, id).
required(id).
slotrange(identifier_type).
required_in(id, variant_to_disease_association).
range_in(id, identifier_type, variant_to_disease_association).
class_slot(variant_to_disease_association, subject).
required(subject).
slotrange(iri_type).
required_in(subject, variant_to_disease_association).
range_in(subject, iri_type, variant_to_disease_association).
class_slot(variant_to_disease_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, variant_to_disease_association).
range_in(relation, iri_type, variant_to_disease_association).
class_slot(variant_to_disease_association, object).
required(object).
slotrange(iri_type).
required_in(object, variant_to_disease_association).
range_in(object, iri_type, variant_to_disease_association).
class_slot(variant_to_disease_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, variant_to_disease_association).
class_slot(variant_to_disease_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, variant_to_disease_association).
class_slot(variant_to_disease_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, variant_to_disease_association).
range_in(qualifiers, ontology_class, variant_to_disease_association).
class_slot(variant_to_disease_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, variant_to_disease_association).
range_in(publications, publication, variant_to_disease_association).
class_slot(variant_to_disease_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, variant_to_disease_association).
class_slot(variant_to_disease_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, variant_to_disease_association).
class_slot(variant_to_disease_association, frequency_qualifier).
required(frequency_qualifier).
slotrange(frequency_value).
range_in(frequency_qualifier, frequency_value, variant_to_disease_association).
class_slot(variant_to_disease_association, severity_qualifier).
required(severity_qualifier).
slotrange(severity_value).
range_in(severity_qualifier, severity_value, variant_to_disease_association).
class_slot(variant_to_disease_association, onset_qualifier).
required(onset_qualifier).
slotrange(onset).
range_in(onset_qualifier, onset, variant_to_disease_association).
class(variant_to_phenotypic_feature_association).
mixin(variant_to_phenotypic_feature_association, variant_to_thing_association).
mixin(variant_to_phenotypic_feature_association, entity_to_phenotypic_feature_association).
is_a(variant_to_phenotypic_feature_association, association).
defining_slots(association, [subject, object]).
has_uri(variant_to_phenotypic_feature_association, 'http://w3id.org/biolink/vocab/VariantToPhenotypicFeatureAssociation').
class_slot(variant_to_phenotypic_feature_association, id).
required(id).
slotrange(identifier_type).
required_in(id, variant_to_phenotypic_feature_association).
range_in(id, identifier_type, variant_to_phenotypic_feature_association).
class_slot(variant_to_phenotypic_feature_association, subject).
required(subject).
slotrange(sequence_variant).
required_in(subject, variant_to_phenotypic_feature_association).
range_in(subject, sequence_variant, variant_to_phenotypic_feature_association).
class_slot(variant_to_phenotypic_feature_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, variant_to_phenotypic_feature_association).
range_in(relation, iri_type, variant_to_phenotypic_feature_association).
class_slot(variant_to_phenotypic_feature_association, object).
required(object).
slotrange(iri_type).
required_in(object, variant_to_phenotypic_feature_association).
range_in(object, iri_type, variant_to_phenotypic_feature_association).
class_slot(variant_to_phenotypic_feature_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, variant_to_phenotypic_feature_association).
class_slot(variant_to_phenotypic_feature_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, variant_to_phenotypic_feature_association).
class_slot(variant_to_phenotypic_feature_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, variant_to_phenotypic_feature_association).
range_in(qualifiers, ontology_class, variant_to_phenotypic_feature_association).
class_slot(variant_to_phenotypic_feature_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, variant_to_phenotypic_feature_association).
range_in(publications, publication, variant_to_phenotypic_feature_association).
class_slot(variant_to_phenotypic_feature_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, variant_to_phenotypic_feature_association).
class_slot(variant_to_phenotypic_feature_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, variant_to_phenotypic_feature_association).
class_slot(variant_to_phenotypic_feature_association, sex_qualifier).
required(sex_qualifier).
slotrange(biological_sex).
range_in(sex_qualifier, biological_sex, variant_to_phenotypic_feature_association).
class_slot(variant_to_phenotypic_feature_association, frequency_qualifier).
required(frequency_qualifier).
slotrange(frequency_value).
range_in(frequency_qualifier, frequency_value, variant_to_phenotypic_feature_association).
class_slot(variant_to_phenotypic_feature_association, severity_qualifier).
required(severity_qualifier).
slotrange(severity_value).
range_in(severity_qualifier, severity_value, variant_to_phenotypic_feature_association).
class_slot(variant_to_phenotypic_feature_association, onset_qualifier).
required(onset_qualifier).
slotrange(onset).
range_in(onset_qualifier, onset, variant_to_phenotypic_feature_association).
class(variant_to_population_association).
mixin(variant_to_population_association, variant_to_thing_association).
mixin(variant_to_population_association, frequency_quantifier).
mixin(variant_to_population_association, frequency_qualifier_mixin).
is_a(variant_to_population_association, association).
defining_slots(association, [subject, object]).
has_uri(variant_to_population_association, 'http://w3id.org/biolink/vocab/VariantToPopulationAssociation').
class_slot(variant_to_population_association, id).
required(id).
slotrange(identifier_type).
required_in(id, variant_to_population_association).
range_in(id, identifier_type, variant_to_population_association).
class_slot(variant_to_population_association, subject).
required(subject).
slotrange(sequence_variant).
required_in(subject, variant_to_population_association).
range_in(subject, sequence_variant, variant_to_population_association).
class_slot(variant_to_population_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, variant_to_population_association).
range_in(relation, iri_type, variant_to_population_association).
class_slot(variant_to_population_association, object).
required(object).
slotrange(population_of_individual_organisms).
required_in(object, variant_to_population_association).
range_in(object, population_of_individual_organisms, variant_to_population_association).
class_slot(variant_to_population_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, variant_to_population_association).
class_slot(variant_to_population_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, variant_to_population_association).
class_slot(variant_to_population_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, variant_to_population_association).
range_in(qualifiers, ontology_class, variant_to_population_association).
class_slot(variant_to_population_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, variant_to_population_association).
range_in(publications, publication, variant_to_population_association).
class_slot(variant_to_population_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, variant_to_population_association).
class_slot(variant_to_population_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, variant_to_population_association).
class_slot(variant_to_population_association, has_count).
required(has_count).
slotrange(integer).
range_in(has_count, integer, variant_to_population_association).
class_slot(variant_to_population_association, has_total).
required(has_total).
slotrange(integer).
range_in(has_total, integer, variant_to_population_association).
class_slot(variant_to_population_association, has_quotient).
required(has_quotient).
slotrange(double).
range_in(has_quotient, double, variant_to_population_association).
class_slot(variant_to_population_association, has_percentage).
required(has_percentage).
slotrange(double).
range_in(has_percentage, double, variant_to_population_association).
class_slot(variant_to_population_association, frequency_qualifier).
required(frequency_qualifier).
slotrange(frequency_value).
range_in(frequency_qualifier, frequency_value, variant_to_population_association).
class(variant_to_thing_association).
is_a(variant_to_thing_association, association).
defining_slots(association, [subject]).
has_uri(variant_to_thing_association, 'http://w3id.org/biolink/vocab/VariantToThingAssociation').
class_slot(variant_to_thing_association, id).
required(id).
slotrange(identifier_type).
required_in(id, variant_to_thing_association).
range_in(id, identifier_type, variant_to_thing_association).
class_slot(variant_to_thing_association, subject).
required(subject).
slotrange(sequence_variant).
required_in(subject, variant_to_thing_association).
range_in(subject, sequence_variant, variant_to_thing_association).
class_slot(variant_to_thing_association, relation).
required(relation).
slotrange(iri_type).
required_in(relation, variant_to_thing_association).
range_in(relation, iri_type, variant_to_thing_association).
class_slot(variant_to_thing_association, object).
required(object).
slotrange(iri_type).
required_in(object, variant_to_thing_association).
range_in(object, iri_type, variant_to_thing_association).
class_slot(variant_to_thing_association, negated).
required(negated).
slotrange(boolean).
range_in(negated, boolean, variant_to_thing_association).
class_slot(variant_to_thing_association, association_type).
required(association_type).
slotrange(ontology_class).
range_in(association_type, ontology_class, variant_to_thing_association).
class_slot(variant_to_thing_association, qualifiers).
required(qualifiers).
slotrange(ontology_class).
multivalued_in(qualifiers, variant_to_thing_association).
range_in(qualifiers, ontology_class, variant_to_thing_association).
class_slot(variant_to_thing_association, publications).
required(publications).
slotrange(publication).
multivalued_in(publications, variant_to_thing_association).
range_in(publications, publication, variant_to_thing_association).
class_slot(variant_to_thing_association, provided_by).
required(provided_by).
slotrange(provider).
range_in(provided_by, provider, variant_to_thing_association).
class_slot(variant_to_thing_association, association_slot).
required(association_slot).
slotrange(string).
range_in(association_slot, string, variant_to_thing_association).
class(zygosity).
is_a(zygosity, attribute).
has_uri(zygosity, 'http://w3id.org/biolink/vocab/Zygosity').
class_slot(zygosity, id).
required(id).
slotrange(identifier_type).
required_in(id, zygosity).
range_in(id, identifier_type, zygosity).
class_slot(zygosity, name).
required(name).
slotrange(label_type).
range_in(name, label_type, zygosity).
class_slot(zygosity, category).
required(category).
slotrange(iri_type).
multivalued_in(category, zygosity).
range_in(category, iri_type, zygosity).
class_slot(zygosity, related_to).
required(related_to).
slotrange(named_thing).
multivalued_in(related_to, zygosity).
range_in(related_to, named_thing, zygosity).
class_slot(zygosity, interacts_with).
required(interacts_with).
slotrange(named_thing).
multivalued_in(interacts_with, zygosity).
range_in(interacts_with, named_thing, zygosity).
class_slot(zygosity, node_property).
required(node_property).
slotrange(string).
range_in(node_property, string, zygosity).
class_slot(zygosity, iri).
required(iri).
slotrange(iri_type).
range_in(iri, iri_type, zygosity).
class_slot(zygosity, synonym).
required(synonym).
slotrange(label_type).
multivalued_in(synonym, zygosity).
range_in(synonym, label_type, zygosity).
class_slot(zygosity, full_name).
required(full_name).
slotrange(label_type).
range_in(full_name, label_type, zygosity).
class_slot(zygosity, description).
required(description).
slotrange(narrative_text).
range_in(description, narrative_text, zygosity).
class_slot(zygosity, systematic_synonym).
required(systematic_synonym).
slotrange(label_type).
range_in(systematic_synonym, label_type, zygosity).
class_slot(zygosity, subclass_of).
required(subclass_of).
slotrange(ontology_class).
multivalued_in(subclass_of, zygosity).
range_in(subclass_of, ontology_class, zygosity).

