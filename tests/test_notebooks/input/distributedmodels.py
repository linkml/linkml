from logging import ERROR

model = """
# Every model must have a globally unique URI. This is the external name of the model
id: http://example.org/examples/distributeExample 

# Every model should also have a globally unique name (well, global within the context of the particular modeling environment)
name: dist1

# Descriptions are always useful, but not required
description: A toy extension to the base biolink model

# Versions are recommended but not required.  The version is copied into the output artifacts.  An error will be raised
# if two different versions of the same model are imported
version: 0.0.1

# A license is not required at this point -- should it be?
license: https://creativecommons.org/publicdomain/zero/1.0/
                                                         
# Prefixes can be assigned specifically.  We define two below:
#   biolink -- the prefix used by the biolink-model
#   dist1 -- the URI prefix used by this example.  Note that the dist1 prefix may or may not align with the model id
prefixes:
  biolink: https://w3id.org/biolink/vocab/
  linkml: https://w3id.org/linkml/
  dist: http://example.org/examples/dist1#

# Prefixes can also be pulled from a prefixcommons compliant site. The map below uses the definitions found in
#     https://github.com/prefixcommons/biocontext/blob/master/registry/semweb_context.yaml.
default_curi_maps:
  - semweb_context

# The default prefix is what is used in the subsets, types, slots, classes sections below if not otherwise supplied
default_prefix:  dist
default_range: string

# The list of prefixes to emit target files.  Note that all prefixes that are used elsewhere in the model are automatically
# emitted, with the exception of 
emit_prefixes:
    - skos
    - rdf
    - dist

# List of models to import.  Note that import specifications can (currently) be URI's, absolute (file://...file), curies
# (biolink:model), or relative (includes/myfile) file names.  Note, however, that this latter form is being deprecated.  
# The location of imported files can now be specified in an accompanying mapping file.  The imports below reference:
#   https://w3id.org/biolink/biolink-model    -- the biolink model
#   https://w3id.org/linkml/types  -- the biolink modeling language types definitions
imports: 
  - https://w3id.org/biolink/biolink-model
  - linkml:types

# Subsets that are defined in this model extension
subsets:
    experimental:
        # A subset should have a description
        description: model elements that have not yet been tested

# Types that are defined in this model extension
types:
  gene sequence:
    uri: dist:seq
    typeof: string
    description: A gene sequence
        
# Slots that are defined in this model extension
slots:
    gene has sequence:
        description: A gene pattern
        domain: gene
        range: gene sequence
        slot_uri: dist:hasSeq
        required: true

# Classes that are defined in this model extension
classes:
    # The class name.  For most generators, this will be transformed to CamelCase (MyGene)
    my gene:
        description: This is an example extension.  Doesn't do a lot
        is_a: gene
        slots:
            - gene has sequence
    
    
"""


from linkml.generators.pythongen import PythonGenerator

gen = PythonGenerator(model, log_level=ERROR)
print(gen.serialize())

