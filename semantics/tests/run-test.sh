#!/bin/sh
swipl  -l linkml.pro -g "['tests/std_header.pro'],['$1'],forall((expected(X),writeln(expected(X))), call(X)),writeln(success),halt" &&\
swipl  -l linkml.pro -g "['tests/std_header.pro'],['$1'],forall((not_expected(X),writeln(not_expected(X))), \\+call(X)),writeln(success),halt"

