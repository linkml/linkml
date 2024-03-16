
# Enum: GeneOrGeneProductOrChemicalEntityAspectEnum




URI: [biolink:GeneOrGeneProductOrChemicalEntityAspectEnum](https://w3id.org/biolink/vocab/GeneOrGeneProductOrChemicalEntityAspectEnum)


## Other properties

|  |  |  |
| --- | --- | --- |

## Permissible Values

| Text | Description | Meaning | Other Information |
| :--- | :---: | :---: | ---: |
| activity_or_abundance | Used in cases where the specificity of the relationship can not be determined to be either activity  or abundance.  In general, a more specific value from this enumeration should be used. |  |  |
| abundance |  |  | {'is_a': 'activity_or_abundance'} |
| activity |  |  | {'is_a': 'activity_or_abundance'} |
| expression |  |  | {'is_a': 'abundance'} |
| synthesis |  |  | {'is_a': 'abundance'} |
| degradation |  |  | {'is_a': 'abundance'} |
| cleavage |  |  | {'is_a': 'degradation'} |
| hydrolysis |  |  | {'is_a': 'degradation'} |
| metabolic_processing |  |  |  |
| mutation_rate |  |  |  |
| stability |  |  |  |
| folding |  |  |  |
| localization |  |  |  |
| transport |  |  |  |
| secretion |  |  | {'is_a': 'transport'} |
| uptake |  |  | {'is_a': 'transport'} |
| molecular_modification |  |  |  |
| acetylation |  |  | {'is_a': 'molecular_modification'} |
| acylation |  |  | {'is_a': 'molecular_modification'} |
| alkylation |  |  | {'is_a': 'molecular_modification'} |
| amination |  |  | {'is_a': 'molecular_modification'} |
| carbamoylation |  |  | {'is_a': 'molecular_modification'} |
| ethylation |  |  | {'is_a': 'molecular_modification'} |
| glutathionylation |  |  | {'is_a': 'molecular_modification'} |
| glycation |  |  | {'is_a': 'molecular_modification'} |
| glycosylation |  |  | {'is_a': 'molecular_modification'} |
| glucuronidation |  |  | {'is_a': 'molecular_modification'} |
| n_linked_glycosylation |  |  | {'is_a': 'molecular_modification'} |
| o_linked_glycosylation |  |  | {'is_a': 'molecular_modification'} |
| hydroxylation |  |  | {'is_a': 'molecular_modification'} |
| lipidation |  |  | {'is_a': 'molecular_modification'} |
| farnesylation |  |  | {'is_a': 'molecular_modification'} |
| geranoylation |  |  | {'is_a': 'molecular_modification'} |
| myristoylation |  |  | {'is_a': 'molecular_modification'} |
| palmitoylation |  |  | {'is_a': 'molecular_modification'} |
| prenylation |  |  | {'is_a': 'molecular_modification'} |
| methylation |  |  | {'is_a': 'molecular_modification'} |
| nitrosation |  |  | {'is_a': 'molecular_modification'} |
| nucleotidylation |  |  | {'is_a': 'molecular_modification'} |
| phosphorylation |  |  | {'is_a': 'molecular_modification'} |
| ribosylation |  |  | {'is_a': 'molecular_modification'} |
| ADP-ribosylation |  |  | {'is_a': 'molecular_modification'} |
| sulfation |  |  | {'is_a': 'molecular_modification'} |
| sumoylation |  |  | {'is_a': 'molecular_modification'} |
| ubiquitination |  |  | {'is_a': 'molecular_modification'} |
| oxidation |  |  | {'is_a': 'molecular_modification'} |
| reduction |  |  | {'is_a': 'molecular_modification'} |
| carboxylation |  |  | {'is_a': 'molecular_modification'} |

