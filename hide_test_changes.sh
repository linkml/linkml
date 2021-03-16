#!/bin/bash
# Make all of the test output files invisible to git
git update-index --assume-unchanged `git status -s | grep tests | grep \/output\/ | sed 's/.* tests\//tests\//' | xargs`