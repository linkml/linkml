#!/bin/bash
# Clear all of the temporary directories before a run.\
find . -name temp -exec rm -rf {}/* \;
