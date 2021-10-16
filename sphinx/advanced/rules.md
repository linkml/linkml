# Rules

## Conditional rules

From https://json-schema.org/understanding-json-schema/reference/conditionals.html

```
classes:

  Address:
    attributes:
      street_address:
      country:
        range: CountryEnum
      postal_code:
    rules:
      - preconditions:
          slot_conditions:
            country:
              equals_string_value: United States of America
        postconditions:
          slot_conditions:
            postal_code:
              pattern: "[0-9]{5}(-[0-9]{4})?" 
        elseconditions:
          slot_conditions:
            postal_code:
              pattern: "[A-Z][0-9][A-Z] [0-9][A-Z][0-9]" 
```

## Boolean expressions

TODO: SO/GFF example?

## Classification rules

```
classes:

  Sample:
    ...
  GenomicsSample:
    classification_rules:
      - genus: Sample
        preconditions:
          slot_conditions:
            analyte:
              equals_string_value: DNA
```
