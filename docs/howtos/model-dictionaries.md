# How to model dictionaries with arbitrary keys

Many data formats use JSON/YAML objects as dictionaries — that is, mappings
where the keys are not fixed by the schema but come from the data itself.
For example, a set of translations might look like:

```yaml
translations:
  hand: manus
  foot: pes
```

At first glance this seems hard to express in LinkML, which is class-and-slot
oriented.  In practice LinkML handles this well through its *inlined dictionary*
feature.  This guide walks through three approaches, from the most constrained
(and most useful) to the most open-ended.

## Solution 1: SimpleDict — string-to-string maps

A **SimpleDict** is the right choice when each entry maps a string key to a
single atomic value.  It is the most compact serialization LinkML offers.

### Schema

```yaml
id: https://example.org/translations
name: translations_example
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/translations/

default_range: string
default_prefix: ex

imports:
  - linkml:types

classes:
  TextRecord:
    description: A piece of text with translations.
    attributes:
      id:
        identifier: true
      original_text:
      translations:
        description: >-
          A set of translations, keyed by language code.
        range: Translation
        multivalued: true
        inlined: true

  Translation:
    description: A single translation entry.
    attributes:
      language:
        identifier: true
        description: Language code (e.g. "la", "es").
      translated_text:
        required: true
        description: The translated string.
```

### Data (SimpleDict form)

Because `Translation` has an identifier slot (`language`) and exactly one
other attribute (`translated_text`), LinkML automatically recognises this as
a **SimpleDict**.  The data can therefore be written as plain key-value pairs:

```yaml
- id: WORD_001
  original_text: hand
  translations:
    la: manus
    es: mano
- id: WORD_002
  original_text: foot
  translations:
    la: pes
    es: pie
```

### How it works

LinkML collapses the inlined dictionary when the range class satisfies all
of the following:

1. It has a slot marked `identifier: true` (or `key: true`).
2. It has **exactly one** other non-key slot — this becomes the "value" of
   the dictionary entry.

When both conditions hold, the serialization uses the identifier as the
dictionary key and the remaining slot value as the dictionary value,
producing the compact `key: value` form shown above.

If the class has more than two slots, you can still opt in to SimpleDict by
marking the intended value slot with the `simple_dict_value` annotation:

```yaml
  Translation:
    attributes:
      language:
        identifier: true
      translated_text:
        required: true
        annotations:
          simple_dict_value: true
      notes:
        description: Optional notes about this translation.
```

Alternatively, if exactly one non-key slot is `required`, LinkML will use
that slot as the SimpleDict value automatically.

### Expanded form

The same data can always be written in the fully expanded dictionary form:

```yaml
translations:
  la:
    translated_text: manus
  es:
    translated_text: mano
```

Or as a list:

```yaml
translations:
  - language: la
    translated_text: manus
  - language: es
    translated_text: mano
```

LinkML parsers normalise between these forms automatically.

### Real-world example

LinkML's own metamodel uses this pattern for `prefixes`.  The
[Prefix](https://w3id.org/linkml/Prefix) class has an identifier
(`prefix_prefix`) and one value (`prefix_reference`), so schemas can write:

```yaml
prefixes:
  linkml: https://w3id.org/linkml/
  dcterms: http://purl.org/dc/terms/
```

instead of the more verbose expanded form.

## Solution 2: CompactDict — string-to-object maps

When each entry needs **multiple fields** beyond the key, the SimpleDict
shorthand no longer applies.  Instead, LinkML serializes the collection as a
**CompactDict** — the key is still the identifier, but the value is an object
containing the remaining slots.

### Schema

```yaml
classes:
  Lexicon:
    attributes:
      id:
        identifier: true
      entries:
        range: LexiconEntry
        multivalued: true
        inlined: true

  LexiconEntry:
    description: A dictionary entry with multiple translation fields.
    attributes:
      term:
        identifier: true
      target_language:
        required: true
      translation:
        required: true
      part_of_speech:
```

### Data (CompactDict form)

```yaml
id: LEX_001
entries:
  hand:
    target_language: la
    translation: manus
    part_of_speech: noun
  foot:
    target_language: la
    translation: pes
    part_of_speech: noun
```

Note that the `term` field does not appear inside each object — it is
promoted to the dictionary key.  LinkML handles adding it back during
parsing.

### Expanded form

The same data in list form:

```yaml
entries:
  - term: hand
    target_language: la
    translation: manus
    part_of_speech: noun
  - term: foot
    target_language: la
    translation: pes
    part_of_speech: noun
```

## Solution 3: `linkml:Any` — fully open-ended

If the set of keys **and** the structure of values are both completely
unknown at schema-design time, you can fall back to `linkml:Any`.  This is
the least constrained option and should be used sparingly, because it
bypasses all type checking for the annotated slot.

### Schema

```yaml
classes:
  Any:
    class_uri: linkml:Any

  Record:
    attributes:
      id:
        identifier: true
      metadata:
        range: Any
        description: Arbitrary key-value metadata.
```

### Data

```yaml
- id: REC_001
  metadata:
    hand: manus
    foot: pes
    count: 42
    nested:
      a: 1
      b: 2
```

Because `metadata` accepts any structure, there is no validation of keys or
values.  Prefer Solution 1 or 2 whenever the shape of the data is even
partially known.

## Which approach should I use?

| Scenario | Approach | Serialization |
|---|---|---|
| Key → single atomic value | **SimpleDict** (Solution 1) | `key: value` |
| Key → object with multiple fields | **CompactDict** (Solution 2) | `key: {field: value, ...}` |
| Completely unknown structure | **`linkml:Any`** (Solution 3) | Anything goes |
| Ordered collection, no dict keys needed | `inlined_as_list: true` | `[{id: k, ...}, ...]` |

As a rule of thumb, start with Solution 1 or 2 — they give you the compact
dictionary syntax you want while retaining full schema-level validation.
Reserve `linkml:Any` for truly open-ended extension points.

## Further reading

- [Inlining objects](../schemas/inlining.md) — full reference on `inlined`,
  `inlined_as_list`, and dictionary forms.
- [Advanced features](../schemas/advanced.md) — details on `linkml:Any` and
  other experimental features.
