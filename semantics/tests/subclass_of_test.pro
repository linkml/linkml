:- include('basic.pro').

expected(subclass_of(c,d)).
expected(subclass_of(c,c)).
expected(subclass_of(d,d)).
not_expected(subclass_of(d,c)).

not_expected(incoherent).
