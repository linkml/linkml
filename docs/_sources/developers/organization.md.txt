# Organization

See [github.com/linkml](https://github.com/linkml)

* linkml-model
    - self-describing linkml datamodel
    - note that you should not use the python classes - use linkml_runtime.linkml_model
* linkml-runtime
    - code needed by linkml python object models
    - utility code such as schemaview
    - includes metamodel (linkml_runtime.linkml_model)
* linkml-runtime-api
  - extension to runtime to provide:
     - a change/patch API over data
     - a query API over data
* linkml
    - generators
    - datautils
* linkml-model-enrichment
    - tools for bootstrapping schemas
* linkml-model-template
  - Project template for new LinkML datamodels
