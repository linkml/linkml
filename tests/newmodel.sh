#!/bin/bash
cp input/meta.yaml ../meta.yaml
cp input/includes/* ../includes
pushd output
# Update everything in the root
cp context.jsonld ../../
cp meta.jsonld ../../
cp meta.owl ../../
cp meta.shex ../../
cp meta.shexj ../../
cp meta.ttl ../../
cp includes/* ../../includes

# Update the documentation
rm -rf ../../docs/*
cp -r docs/* ../../docs
# Update the python image of the model itself
cp meta.py ../../linkml/meta.py
popd
