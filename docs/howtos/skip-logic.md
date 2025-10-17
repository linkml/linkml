# How to implement skip logic in LinkML

This guide will show you how to implement skip logic in your LinkML schemas. Skip logic, also known as conditional branching or survey routing, is a feature that allows you to control which questions are shown to a user based on their previous answers. This is a common requirement in systems like REDCap, CEDAR, and other questionnaire-based data collection systems.

## What is Skip Logic?

In a questionnaire, some questions may only be relevant if a specific answer was given to a previous question. For example, a question about the due date of a pregnancy is only relevant if the respondent has indicated that they are pregnant. Skip logic allows you to hide or show questions based on these conditions, creating a more dynamic and user-friendly experience.

## Modeling Questionnaires in LinkML

You can model a questionnaire in LinkML by defining a class for the questionnaire itself, and then adding slots for each question. For example:

```yaml
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
prefixes:
  linkml: https://w3id.org/linkml/
  personinfo: https://w3id.org/linkml/examples/personinfo/
default_prefix: personinfo

imports:
  - linkml:types

classes:
  Person:
    slots:
      - is_pregnant
      - due_date
      - has_children
      - number_of_children
```

In this schema, we have a `Person` class with four slots representing questions in a questionnaire.

## Implementing Skip Logic with LinkML Rules

LinkML's `rules` feature can be used to implement skip logic. Rules are composed of `preconditions` and `postconditions`. The `preconditions` define the conditions under which the rule applies, and the `postconditions` define the constraints that should be enforced when the preconditions are met.

### Pattern 1: Making a field inapplicable

In some cases, a question may not be applicable based on a previous answer. For example, if a person is not pregnant, the `due_date` question is not applicable. We can model this by making the `due_date` slot inapplicable if the `is_pregnant` slot is `false`.

```yaml
classes:
  Person:
    slots:
      - is_pregnant
      - due_date
      - has_children
      - number_of_children
    rules:
      - description: "If a person is not pregnant, the due date is not applicable."
        preconditions:
          slot_conditions:
            is_pregnant:
              equals_string: "no"
        postconditions:
          slot_conditions:
            due_date:
              inapplicable: true
```

With this rule, if a user enters "no" for `is_pregnant`, any value entered for `due_date` will be considered a validation error. The data validation engine would expect the `due_date` to be null or absent.

### Pattern 2: Making a field conditionally required

Another common pattern is to make a field required only if a certain condition is met. For example, the `due_date` should be required if the person is pregnant.

```yaml
classes:
  Person:
    slots:
      - is_pregnant
      - due_date
      - has_children
      - number_of_children
    rules:
      - description: "If a person is pregnant, the due date is required."
        preconditions:
          slot_conditions:
            is_pregnant:
              equals_string: "yes"
        postconditions:
          slot_conditions:
            due_date:
              required: true
```

In this case, if `is_pregnant` is "yes", the `due_date` slot must have a value.

### Combining Rules

You can combine these rules to create more complex logic. For example, we can combine the two rules above, and add similar logic for the `number_of_children` slot.

```yaml
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
prefixes:
  linkml: https://w3id.org/linkml/
  personinfo: https://w3id.org/linkml/examples/personinfo/
default_prefix: personinfo

imports:
  - linkml:types

enums:
  YesNoEnum:
    permissible_values:
      "yes":
      "no":

slots:
  is_pregnant:
    range: YesNoEnum
    description: "Are you pregnant?"
  due_date:
    range: date
    description: "What is your due date?"
  has_children:
    range: YesNoEnum
    description: "Do you have children?"
  number_of_children:
    range: integer
    description: "How many children do you have?"

classes:
  Person:
    slots:
      - is_pregnant
      - due_date
      - has_children
      - number_of_children
    rules:
      - description: "Due date is required if pregnant, otherwise it's inapplicable."
        preconditions:
          slot_conditions:
            is_pregnant:
              equals_enum:
                codeable_concept: "yes"
        postconditions:
          slot_conditions:
            due_date:
              required: true
      - preconditions:
          slot_conditions:
            is_pregnant:
              equals_enum:
                codeable_concept: "no"
        postconditions:
          slot_conditions:
            due_date:
              inapplicable: true

      - description: "Number of children is required if has_children is yes, otherwise it's inapplicable."
        preconditions:
          slot_conditions:
            has_children:
              equals_enum:
                codeable_concept: "yes"
        postconditions:
          slot_conditions:
            number_of_children:
              required: true
      - preconditions:
          slot_conditions:
            has_children:
              equals_enum:
                codeable_concept: "no"
        postconditions:
          slot_conditions:
            number_of_children:
              inapplicable: true
```

This complete example demonstrates how to use LinkML rules to implement skip logic in your schemas, ensuring that your data is valid and consistent. By using these patterns, you can create sophisticated and dynamic questionnaires that adapt to user input.
