
class(c).
class(c1).
class(c2).
is_a(c1,c).
is_a(c2,c).

slot(p).
slot(p1).
slot(p2).

% trivial case
rdf(ok1,p1,j).
slot(p1).
domain(p1,c).
rdf(ok1,rdf:type,c).
class_slot(c,p1).
expected(domain_induced_instance_of(ok1,c)).
expected(class_slot(c,p1)).
expected(instance_of(ok1,c)).
expected(subrelation_of(p1,p1)).
not_expected( invalid(ok1) ).

% ok to use a more specific class
rdf(ok2,p2,j).
slot(p2).
domain(p2,c).
rdf(ok2,rdf:type,c1).
class_slot(c,p2).
expected(instance_of(ok2,c)).
not_expected( invalid(ok2) ).

% not ok to use sib
rdf(bad3,p3,j).
slot(p3).
class_slot(c2,p3).
domain(p3,c1).
rdf(bad3,rdf:type,c2).
expected(instance_of(bad3,c)).
expected(instance_of(bad3,c2)).
expected(invalid(bad3)).

% not ok to use if no class_slot declared
rdf(bad4,p4,j).
slot(p4).
class_slot(c1,p4).
domain(p4,c).
rdf(bad4,rdf:type,c).
expected(instance_of(bad4,c)).
not_expected(instance_of(bad4,c1)).
expected(invalid(bad4)).

not_expected(incoherent).


