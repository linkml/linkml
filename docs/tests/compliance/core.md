# Core Compliance

````{jinja} compliance
{% set module = 'core' %}
```{eval-rst}
.. currentmodule:: tests.test_compliance.test_{{module}}_compliance
```

{% for test_name, schemas in compliance.modules['core'].items() %}
```{eval-rst}
.. autofunction:: {{ test_name }}

``` 

{% for schema_name, rows in schemas.items() %}

{{ schema_name }}

```{list-table}
:header-rows: 1

* 
{%- for key in rows[0].keys() %}
  - {{ key }} 
{%- endfor %}
{% for row in rows -%}
* 
{%- for item in row.values() %}
  - {{ item }}
{%- endfor %}
{% endfor -%}
```

{% endfor %}
{% endfor %}
````