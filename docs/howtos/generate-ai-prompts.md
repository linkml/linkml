# How to Generate AI prompts

## Introduction Preamble

Generative AI exemplified by ChatGPT is a powerful but unreliable technology that can help with many different
kinds of tasks:

 - Document summarization
 - Extracting from text into databases
 - Natural language interfaces to databases

The underlying technology is instruction-tuned Large Language Models (LLMs), powerful tools that have
very general question-answer abilities, yet are prone to hallucinations.
Additionally, LLMs can generate text that is understandable
by a human, but getting them to produce structured data according a defined schema can be challenging.

In June 2023, OpenAI announced the ability to
[describe function calls](https://platform.openai.com/docs/guides/gpt/function-calling)
in OpenAI API requests. This is compatible with using LinkML to describe your data, and it is possible
to auto-generate prompts using LinkML.

## Objective

The idea here is to go from free text narrative or semi-structured text such as:

```
PERSONRECORD: 1234

Izumi is a professor at the University of Tokyo, where she has been employed since 2017.
She is 56 years old.
She has a brother called Toshiro.
```

into JSON, YAML, or RDF conforming to a schema, such as the example
[PersonSchema](https://github.com/linkml/linkml/tree/main/examples/PersonSchema)
from the [LinkML tutorial](https://linkml.io/linkml/intro/tutorial01.html)

For example, the intended target object may be expressed in JSON as:

```json
{
  "id": "1234",
  "name": "Izumi",
  "description": "Izumi is a professor at the University of Tokyo.",
  "age_in_years": 56,
  "has_familial_relationships": [
    {
      "related_to": "Toshiro",
      "type": "SIBLING_OF"
    }
  ],
  "has_employment_history": [
    {
      "employed_at": "University of Tokyo",
      "start_date": "2017-01-01"
    }
  ]
}
```

This how-to is aimed at a typical LinkML developer. We'll briefly address why LinkML is a good
framework for this kind of task at the end, but if you are coming here as a newbie, you may
want to check out [Why LinkML?](https://linkml.io/linkml/faq/why-linkml.html) in the FAQ.

## Generating prompts from LinkML schemas

The OpenAI function system uses OpenAPI specifications, which are essentially JSON-Schema.
You could use the [JSON Schema Generator](https://linkml.io/linkml/generators/json-schema.html) to generate
the expected payload from a function, but this tutorial walks through the process of using Pydantic
generated from LinkML schemas.

### Step 1: Generate Pydantic models from LinkML

We will use the standard personinfo schema

```sh
gen-pydantic examples/PersonSchema/personinfo.yaml > personinfo.py
```

We can dynamically introspect what the generated models look like as JSON-schema

```python
>>> from personinfo import Person
>>> import json
>>> print(Person.schema_json(indent=2))
```

```json
{
  "title": "Person",
  "description": "A person (alive, dead, undead, or fictional).",
  "type": "object",
  "properties": {
    "id": {
      "title": "Id",
      "type": "string"
    },
    "name": {
      "title": "Name",
      "type": "string"
    },
    "has_familial_relationships": {
      "title": "Has Familial Relationships",
      "type": "array",
      "items": {
        "$ref": "#/definitions/FamilialRelationship"
      }
    }
  }
}
```

### Step 2: Generate a prompt from the Pydantic model

For this step you will need an OpenAI API key. You can get one from [OpenAI](https://openai.com/)



```python
from personinfo import Person
import json
import openai

functions = [
    {
        "name": "extract_data",
        "description":  "A person",
        "parameters": Person.schema(),
    },
]
text = """
PERSONRECORD: 1234

Izumi is a professor at the University of Tokyo, where she has been employed since 2017.
She is 56 years old.
She has a brother called Toshiro.
"""
messages = [
    {"role": "system",
     "content": "You are a helpful assistant that extracts summaries from text as JSON for a database."},
    {"role": "user",
     "content": 'Extract a summary from the following text: ' + text},
]
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613", functions=functions, messages=messages)
r = response.choices[0]['message']['function_call']['arguments']
print(json.dumps(json.loads(r), indent=2))
```

Note that LLM output is non-deterministic, so the JSON may look different each time.

When I ran this right now, I got:


```json
{
  "id": "1234",
  "name": "Izumi",
  "description": "Izumi is a professor at the University of Tokyo.",
  "age_in_years": 56,
  "has_familial_relationships": [
    {
      "related_to": "Toshiro",
      "type": "SIBLING_OF"
    }
  ]
}
```

Note it didn't seem to extract the employment portion, despite this being part of the model.
But on other runs it does include this.

Welcome to the world of LLMs!

### Step 3: Generating a python object

As the last step you can do:

```python
person = Person(**json.loads(r))
```

Note you can also use standard LinkML tools to generate YAML, RDF, TSV, store in a SQL database, etc

### Step 4: Troubleshooting

Often the last step will fail because the generated JSON sometimes does not strictly conform to the schema.

For example, sometimes the LLM is overly eager to fill in all slots, and rather than null/empty it may
fill these in with empty strings:

```json
  "has_familial_relationships": [
    {
      "started_at_time": "",
      "ended_at_time": "",
      "related_to": "Toshiro",
      "type": "SIBLING_OF"
    }
```

Pydantic will rightfully complain about this:

```python
has_familial_relationships -> 0 -> started_at_time
  invalid date format (type=value_error.date)
has_familial_relationships -> 0 -> ended_at_time
  invalid date format (type=value_error.date)
```

Because in our schema we have defined these as `date` types.

You may also notice if your schema is quite nested or uses opaque foreign keys,
the extracted JSON may be somewhat "flatter", or will do things like place
human-readable strings where there should be identifiers.

There are a number of possible solutions to this:

- Retry the query until the LLM gives something conformant (may be costly!)
- Tune the prompt and instruct the LLM not to use empty strings
- Relax the schema to allow empty strings
- Post-process the JSON to remove empty strings
- Hope for further fine-tuning of the LLMs
- Use a more advanced framework like SPIRES (see below)
- Provide *in context* examples

### Providing in-context examples

LLMs often work better with in-context examples ("few shot learning").

Where should we get these examples from? If you are following LinkML modeling best practices,
then you will have a set of examples in your model. You can use these to augment the prompt.

You could even get fancy and connect to a whole database of examples, indexed using embeddings,
and select the most relevant examples to the text to be extracted. We would recommend a framework
like [LangChain](https://github.com/hwchase17/langchain) or LlamaIndex for this.

This is outside the scope of the core LinkML framework and we leave it to you to decide
how best to proceed for your use case. In future this may be incorporated into the OntoGPT
library (see below).

See [this issue](https://github.com/linkml/linkml/issues/1499) for further discussion.

## Further exploration: Text extraction with OntoGPT and SPIRES

OntoGPT is a framework for combining LLMs with ontologies. It includes an implementation
of the SPIRES algorithm for extracting structured data from text, using LinkML schemas. The approach
taken differs from the above in two ways:

1. SPIRES allows for grounding of identified entities and concepts using ontology-lookup (via OAK), and [dynamic value sets](https://linkml.io/linkml/schemas/enums.html#dynamic-enums)
2. Rather than try and extract JSON in a single pass, SPIRES takes a multi-pass approach recursing down the schema

SPIRES predated OpenAI function calls and we are still exploring the relative strengths and benefits of both approaches.

SPIRES also makes use of optional additional annotations in the schema to augment the instructions provided to the LLM.
Some of these may be separated out into their own standard in future.

For more on SPIRES, see:

Structured prompt interrogation and recursive extraction of semantics (SPIRES):
A method for populating knowledge bases using zero-shot learning. (2023)
Caufield, J.H. et al
[doi.org/10.48550/arXiv.2304.02711](
https://doi.org/10.48550/arXiv.2304.02711)

## Other use cases

Extracting text is not the only use case for using LLMs with LinkML.

Another example is combining GPT with a trusted database to increase its reliability. If the
external database is described using LinkML, then we can build systems following patterns like
[ReAct](https://til.simonwillison.net/llms/python-react-pattern) or using [LangChain](https://github.com/hwchase17/langchain)
that combine the LLM with database lookups.

Check back later for examples of this!

## Questions

### Why use LinkML for this?

If you are not already a LinkML developer, you may be wondering why you should use LinkML for this,
rather than do this directly with Pydantic. And for many purposes, doing this directly from Pydantic
is a great solution! For some general reasons to use LinkML see [Why LinkML?](https://linkml.io/linkml/faq/why-linkml.html)
in the FAQ. And bear in mind LinkML is designed to be an optional layer *on top* of frameworks like
Pydantic, rather than a replacement for them.

Some specific reasons to use LinkML for this particular use case:

- Many schemas are already available in LinkML, decoupled from any programmatic python details
- LinkML is a polyglot framework, and is not tied to either Python or JSON.
- You can modify the above example easily to produce RDF
- LinkML allows for specification of additional semantics, some of which may be useful to help guide the LLM

### Can I use LLMs to help generate schemas?

Yes! LinkML is self-describing so the above methodology should be possible to generate a schema
from semi-structured or textual sources, simply by using the metamodel as the schema!
We haven't done many experiments yet, but if successful we may incorporate into [schema-automator](https://linkml.io/schema-automator/).

And of course, many LinkML developers have already discovered that GitHub copilot (and similar
tools like tabnine) work surprisingly well as an autocomplete assistant when editing schemas in
an IDE.

### Aren't LLMs unreliable?

As a LinkML developer you likely care about precise modeling, and accurate representation of knowledge and data.
LLMs may seem anathema to you! They are unreliable! They hallucinate! They give a different answer from
one run to the next!

Additionally, there are aspects of current LLMs that go against certain parts of the Open Science ethos of LinkML.
The examples in this tutorial require subscription access to use proprietary models, with inscrutable training
data. On top of that there are environmental costs in training them and running them.

If this *isn't* your reaction, then we encourage reading the Stochastic Parrots: https://dl.acm.org/doi/10.1145/3442188.3445922
paper which goes into these issues in more detail.

If it *is* your reaction, then rest assured that LLMs will not be a part of the core LinkML framework (although
they may be used in ancillary parts like schema-automator). But we do
intend to make it easier for people who are interested in combining LLMs with well-defined, reliable, trusted data.
Although everyone is still figuring out the strengths and benefits of this technology, there are reasons to
believe that LLMs *when combined with curator oversight and trusted data* can be a useful tool in the data
landscape.
