# GitHub Organization

See [github.com/linkml](https://github.com/linkml)

* [linkml](https://github.com/linkml-model)
    - [generators](../generators/)
    - datautils
    - this documentation
* [linkml-model](https://github.com/linkml-model)
    - self-describing linkml datamodel
    - note that you should not use this module programmatically - use linkml_runtime.linkml_model
* [linkml-runtime](https://github.com/linkml-runtime)
    - code needed by linkml python object models
    - utility code such as [schemaview](manipulating-schemas)
    - includes metamodel (linkml_runtime.linkml_model)
* [linkml-runtime-api](https://github.com/linkml-runtime-api) **NEW**
  - extension to runtime to provide:
     - a change/patch API over data
     - a query API over data
* [linkml-model-enrichment](https://github.com/linkml-model-enrichment)
    - tools for bootstrapping schemas
       - from unstructured TSVs
       - from OWL ontologies
       - from JSON-Schema
    - tools for inferring enum ontology mappings using OLS and BioPortal
* [linkml-model-template](https://github.com/linkml-model-template)
  - Project template for new LinkML datamodels
  - **NOTE** this may be replaced by a cookiecutter system soon
