# Import Maps
The Biolink Modeling Language includes the ability to import one or more model files. Syntax:
```yaml
prefixes:
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types
  - includes/mappings
  -   ...
```

Under the normal mode of operation, the above statements would import:
1) https://w3id.org/linkml/types.yaml
2) _\<yaml file location\>_/includes/mappings.yaml

Often, however, we may want to temporarily alter the location of the imported files for testing purposes.  As an example,
we may have added a new type to `types.yaml` and need to test it locally before it is commited.   Similarly, we may have
copied the base yaml file but do not want to copy th accompanying files as well.

Import Map files are used to address this problem.  An import map consists of a collection of JSON key/value pairs, where
the key matches an line in the `imports` section and the value supplies an alternative.

Example:
```json
{
  "linkml:types": "includes/types",
  "includes/types": "includes/types",
  "types": "includes/types",
  "includes/mappings": "mappings"
}
```
In the above example, `linkml:types`, `includes/types` and `types` all reference `types.yaml` from the `includes` directory
_relative to the location of the import map file itself_. Similarly, references to `includes/mappings` would reference `mappings.yaml'
 _in the same directory as the import map file_. If, for example, the following resided on `https://myserver.org/biolink/linkml.yaml`:
```yaml
prefixes:
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types
  - includes/mappings
  -   ...
```
In the absence of an import mapping, the includes would be resolved to:
* `https://w3id.org/linkml/types.yaml`  
and
* `https://myserver.org/biolink/includes/mappings.yaml`

If, however, the import mapping file defined previously (`~/some/local/directorymodel_map.json`) is passed to a linkml language parser:
```bash
> pwd
  ~/some/local/directory
> gen-owl https://myserver.org/biolink/linkml.yaml --importmap model_map.json
```

The imports would, instead, come from:
* `~/some/local/directory/includes/types.yaml`  
and
* `~/some/local/directory/mappings.yaml`

## Usage in the testing framework
We maintain two mapping files in the testing framework:
[tests/input/empty_import_map.md]()
and
[tests/input/local_import_map.md]()

Which of these maps 

## Notes
1) Mapping keys are literal.  As an example, the imports entry in
    ```yaml
    prefixes:
      p1: https://my.org/includes/
      p2: https://my.org/includes/
    
    imports:
      - p1:types
    ```
    Will not match _either_ of the entries below.  

    ```json
    {
      "p2:types": "local/types",
      "https://my.org/includes/mappings": "includes/mappings"
    }
    ```
2) Mappings apply to both the base file AND its imports.  Given:
    
base.yaml
```yaml
imports:
  - linkml:types
  - includes/localtypes
```
    
includes/localtypes.yaml
```yaml
imports:
  - linkml:types
```
   
The following mapping file:

```json
{
  "linkml:types": "local/types"
}
```
will apply to both the `linkml:types` import in base.yaml and localtypes.yaml

Note also that, if you have something of the form:

base.yaml

```yaml
imports:
  - includes/types
  - includes/localtypes
```
    
includes/localtypes.yaml

```yaml
imports:
  - types
```

You will need two mapping entries to catch both slots:
```json
{
  "includes/types": "local/types",
  "types": "local/types"
}
```
