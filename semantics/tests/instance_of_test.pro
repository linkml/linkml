:- include('basic.pro').

rdf(i,rdf:type,d).

expected(instance_of(i,d)).
expected(instance_of(i,e)).
expected(instance_of(i,m1)).
expected(instance_of(i,m2)).
not_expected(instance_of(i,c)).
not_expected(instance_of(_,i)).
not_expected(instance_of(c,_)).

not_expected(incoherent).
