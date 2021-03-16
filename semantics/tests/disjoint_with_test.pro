
class(c1).
class(c2).
class(c).
class(d).

is_a(c1,c).
is_a(c2,c).
is_a(d,c1).
is_a(d,c2).

expected(subclass_of(d,c1)).
expected(subclass_of(d,c2)).
expected(class_disjoint_with(c1,c2)).
%expected(incoherent).
not_expected(inconsistent(_)).


