#!/bin/bash
# Make all of the test output changes visible to git
git update-index --no-assume-unchanged  `find tests -type f | grep \/output\/ | xargs`