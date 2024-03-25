# Compliance Tests

## Summary
 
````{jinja} compliance
```{list-table}
:header-rows: 1
* 
{%- for key in compliance.summary[0].keys() %}
  - {{ key }} 
{%- endfor %}
{% for row in compliance.summary -%}
* 
{%- for item in row.values() %}
  - {{ item }}
{%- endfor %}
{% endfor -%}
```
````

```{toctree}
core
```