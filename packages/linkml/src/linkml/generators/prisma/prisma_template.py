"""
Jinja2 template for Prisma schema generation.

This template renders LinkML schemas as Prisma schema files (.prisma).
"""

prisma_template_str = """// Prisma schema generated from LinkML schema: {{ schema_name }}
{% if schema_id %}// @linkml:id {{ schema_id }}{% endif %}
{% if schema_description %}// {{ schema_description }}{% endif %}

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "{{ datasource_provider }}"
  url      = env("DATABASE_URL")
}
{% if enums %}

// Enums
{% for enum in enums %}
enum {{ enum.name }} {
  {%- for value in enum.values %}
  {{ value.name }}{% if value.description %}  // {{ value.description }}{% endif %}
  {%- endfor %}
}
{% endfor %}
{%- endif %}
{% if models %}

// Models
{% for model in models %}
{% if model.description %}// {{ model.description }}{% endif %}
{% if model.is_a %}// @linkml:is_a {{ model.is_a }}{% endif %}
{% if model.mixins %}// @linkml:mixins {{ model.mixins }}{% endif %}
{% if model.abstract %}// @linkml:abstract true{% endif %}
model {{ model.name }} {
  {%- for field in model.fields %}
  {%- set is_array = field.prisma_type.endswith('[]') %}
  {%- set field_type = field.prisma_type + ("?" if field.is_optional and not is_array else "") %}
  {%- set field_line = "%-20s"|format(field.name) ~ " " ~ "%-16s"|format(field_type) %}
  {%- if field.modifiers %}{% set field_line = field_line ~ field.modifiers %}{% endif %}
  {%- if field.linkml_metadata %}{% set field_line = field_line ~ "  // " ~ field.linkml_metadata %}{% endif %}
  {{ field_line }}
  {%- if field.is_relation and field.relation_fields %}
  {%- set fk_type = field.fk_type + ("?" if field.is_optional else "") %}
  {{ "%-20s"|format(field.fk_field_name) }} {{ "%-16s"|format(fk_type) }}
  {%- endif %}
  {%- endfor %}
  {%- if model.composite_key %}

  @@id([{{ model.composite_key }}])
  {%- endif %}
  {%- if model.unique_constraints %}
  {%- for constraint in model.unique_constraints %}
  @@unique([{{ constraint.fields }}]{% if constraint.name %}, name: "{{ constraint.name }}"{% endif %})
  {%- endfor %}
  {%- endif %}
}
{% endfor %}
{%- endif %}
"""
