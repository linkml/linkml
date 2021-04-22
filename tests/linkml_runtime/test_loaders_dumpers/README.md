# Description of this directory
This directory does a basic functional test of the different flavors of loaders and dumpers. The
layout is as follows:
* input - contains sample(s) of input in the different possible formats.
  * .json - plain old json representation of the input
  * .jsonld - RDF representation in JSONLD expanded format 
  * .ttl - RDF representation in Turtle format 
  * .yaml - YAML format. **Note:** YAML format is also used to test the dumpers -- see below
* jsonld_context - this contains a docker file to set up a JSON-LD context server.
* models - 
* output - contains sample(s) of dumper output in various formats.  


## Process
The `loader` tests 
