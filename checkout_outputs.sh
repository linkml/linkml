#!/bin/bash
# checkout (update) all of the outputs to revert to what is on github
git checkout  `find tests -name output | xargs`
