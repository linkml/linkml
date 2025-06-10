# Deprecating elements while maintaining PURLs and other URIs

By deprecating, rather than deleting, schema elements in a LinkML model, we ensure backward compatibility, extend user
trust, and provide a valuable historical record, aiding in the understanding of the model's evolution. Therefore,
'deleting' a schema element is instead, a two-step (and two-release) deprecation process.

## First release cycle:

- Add deprecation annotations to the element's definition

| Annotation                                                                                                                                                                                                                                                                           | Value                     |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------|
| One of: [deprecated_element_has_exact_replacement](https://linkml.io/linkml-model/latest/docs/deprecated_element_has_exact_replacement/) OR [deprecated_element_has_possible_replacement](https://linkml.io/linkml-model/latest/docs/deprecated_element_has_possible_replacement/) * | uriorcurie value required |
| [deprecated](https://linkml.io/linkml-model/latest/docs/deprecated/)                                                                                                                                                                                                                 | A string explaining the reason for deprecation along with a link to the corresponding issue. |
| [last_updated_on](https://linkml.io/linkml-model/latest/docs/last_updated_on/)                                                                                                                                                                                                       |                           |
| [modified_by](https://linkml.io/linkml-model/latest/docs/modified_by/)                                                                                                                                                                                                               | With an ORCID value       |
| Deprecation Date                                                                                                                                                                                                                                                                     | Conforms to iso8601/international dates (e.g., `# doi_awards deprecated on 2023-11-12` in a class's usage). |

\* note: If a replacement is not warranted, then using only the `deprecated` metadata tag with an explanation
string is acceptable.

## Second release cycle:

- Move the deprecated element to a "deprecated.yaml" schema file.  Doing this insures that the deprecated elements can
still be found in the documentation and via reference from stable unique identifiers (w3ids, PURLs), but do not appear in the
main schema file nor participate in the validation of data.
- Remove the element itself from the original schema YAML file (e.g. core.yaml, annotation.yaml, etc.).
- Remove any references to the deprecated element from the original schema YAML file. \*\*
- Do not include the "deprecation.yaml" in any imports in the main schema

\*\* note: For a deprecated class, references could be in the `is_a` or `mixin` elements of another class,
or in the `domain` or `range` elements of an existing slot. For deprecated slots, check all classes that
reference that slot, etc.

## Generating deprecated elements in online documentation

Modify any generators that need to continue producing deprecated elements (in general, this is likely to just be `gen-doc`
to use the '--include' flag to import the `deprecation.yaml` as an exception).

For example, this command in the Makefile generates documentation.  With the --include flag, `gen-doc` will create documentation
pages with the deprecated elements, which when deployed to their standard URL, will result in w3ids, PURLs or other
URIs continuing to exist despite the deprecated elements not being in the other serializations of the model (as the --include flag is
an opt-in parameter).

```bash
$(RUN) gen-doc -d $(DOCDIR) --template-directory $(SRC)/$(TEMPLATEDIR) --include src/schema/deprecated.yaml $(SOURCE_SCHEMA_PATH)
```
