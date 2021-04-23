# w3id.org rewrite rules
We use [w3id.org](https://github.com/perma-id/w3id.org) identifiers throughout the model. The current mappings are as
follows:

| FROM | TO | Purpose | Example |
| :----------------------------------:  | :------------------------------------: | ------- | ------- |
| http://w3id.org/linkml/ | http://linkml.github.io/linkml/ | | |
| meta[.sfx] | src/meta.[sfx] | Access to LinkML metamodel w/ connet | http
| includes/types[.sfx] | includes/types[.sfx] | Language types (and other includes) (.sfx set by conneg if not already specified -- .ttl, .yaml, .owl, .shex, ...) | http://w3id.org/linkml/includes/types --> http://linkml.github.io/linkml/includes/types.yaml (Accept: text/yaml) |
| | | | http://w3id.org/linkml/includes/types --> http://linkml.github.io/linkml/includes/types (Accept: text/html) |
| type/[TYPE][.sfx]  | types/[TYPE] | Access to metamodel type definitions w/ conneg | http://w3id.org/linkml/type/Bool --> http://linkml.github.io/linkml-model/docs/types/Bool |
| meta[.sfx] | meta[.sfx] | Access to linkml meta models w/ conneg | http://w3id.org/linkml/meta --> http://linkml.github.io/linkml/meta.yaml (Accept: application/yaml) |
| | | |  http://w3id.org/linkml/meta.owl --> http://linkml.github.io/linkml/meta.owl (*What SHOULD we use for conneg for OWL/TTL?*) |
| meta/[X][.sfx] | docs/[X][.sfx] | Access to metamodel class and slot definitions w/ conneg | http://w3id.org/linkml/meta/Definition --> http://linkml.github.io/linkml-model/docs/Definition.jsonld (Accept: application/json) |
| context.jsonld | context.jsonld | metamodel context.jsonld for converting json instances to RDF | http://w3id.org/linkml/context.jsonld --> http://linkml.github.io/linkml/context.jsonld |

## Testing the rewrite rules

1) Uncomment and change the followint lines in test_rewrite_rules.py:
```python
# DEFAULT_SERVER = "http://localhost:8091/"
# SKIP_REWRITE_RULES = False
```
2) Change the port if necessary -- note that this change has to be reflected in the instructions below
3) Run the unit tests

```bash
> cd httpd
> docker image build . -t w3id
> docker run --rm -d -p 8091:80 --name w3id -v `pwd`/linkml:/w3id/linkml w3id  
> cd ../../..
> pipenv install
> pipenv shell
(linkml) > cd tests/test_rewrite_rules
(linkml) > export SERVER="http://localhost:8091"
(linkml) > python test_rewrite_rules.py
ssss
----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK (skipped=6)
(linkml) > exit
> docker stop w3id
```

7. ** If necessary, make a pull request to w3id.org w/ changes **


