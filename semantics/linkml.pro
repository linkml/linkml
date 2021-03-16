/*

  This document contains logical formulae specifying the semantics of
  the biolink modeling language (linkml). See the README.md file in
  this directory for more details.

  These rules are executable and can be used for validation, or
  inferring useful type information.

  Conventions:

   - we never use the same predicate name for an asserted (unit
   clause) predicate and inferred predicate. asserted predicates come
   only from conversion of the yaml (see tests/biolink.pro for an
   example). inferred predicates are never unit clauses, and are inferred only from the rules below.

   - `direct` indicates a non-transitive connection (may be inferred)

   - Predicates such as subclass_of/2 and subrelation_of/2 are inferred

*/

% ========================================
% model-level reasoning
% ========================================

% --
% rules for classes.
% --
% uses asserted predicates: class/1, is_a/2, mixin/2

% reflexive transitive case of subclass predicate
subclass_of(C,D) :- proper_subclass_of(C,D).
subclass_of(C,C) :- class(C).

% transitive form of direct subclass predicate
% ("proper" == excludes reflexive case)
proper_subclass_of(C,D) :- direct_subclass_of(C,D).
proper_subclass_of(C,D) :- direct_subclass_of(C,Z), proper_subclass_of(Z,D).

% a direct subclass_of link is inferred when we have two classes connected either by
% is_a/2 or mixin/2. These have identical semantics from the perspective of subclass_of
direct_subclass_of(C,D) :- is_a(C,D),class(C),class(D).
direct_subclass_of(C,D) :- mixin(C,D),class(C),class(D).

% is_a-siblings are assumed disjoint
% EXPERIMENTAL: THIS IS LIKELY TOO STRING AND SHOULD BE REPLACED BY EXPLICIT DISJOINTNESS
class_disjoint_with(C,D) :- is_a(C,Z),is_a(D,Z), C\=D, class(Z), \+ is_mixin(Z).

% --
% rules for relations/slots.
% --
% uses asserted predicates: slot/1, is_a/2, mixin/2

% reflexive transitive case of subrelation predicate
subrelation_of(C,D) :- proper_subrelation_of(C,D).
subrelation_of(C,C) :- slot(C).

% transitive form of direct subrelation predicate
% ("proper" == excludes reflexive case)
proper_subrelation_of(C,D) :- direct_subrelation_of(C,D).
proper_subrelation_of(C,D) :- direct_subrelation_of(C,Z), proper_subrelation_of(Z,D).

% a direct subrelation_of link is inferred when we have two relations connected either by
% is_a/2 or mixin/2. These have identical semantics from the perspective of subrelation_of
direct_subrelation_of(C,D) :- is_a(C,D),slot(C),slot(D).
direct_subrelation_of(C,D) :- mixin(C,D),slot(C),slot(D).

% --
% rules for domain/range constraints
% --
% uses asserted predicates: domain/2, range/2, as well as domain_in/3 and range_in/3

% infer whether R is allowed for domain D and range R
% domain and range propagates down subrelation hierarchy and up subclass hierarchy
% e.g. given `friend-of` has domain and range of `human`, we infer:
%  - `friend-of` implies subject and object are of inferred type `human` (trivial reflexive case)
%  - `very-good-friend-of` (a subrelation of friend-of) implies subject and object are of inferred type `organism`
implied_domain(R,D) :- domain(R1,D1), subrelation_of(R,R1), subclass_of(D1,D).
implied_range(R,D) :- range(R1,D1), subrelation_of(R,R1), subclass_of(D1,D).

% as above but contextualized by a class
implied_domain_in(R,D,C) :- implied_domain(R,D),class(C).
implied_domain_in(R,D,C) :- domain_in(R1,D1,C1),subrelation_of(R,R1), subclass_of(D1,D),subclass_of(C,C1).
implied_range_in(R,D,C) :- implied_range(R,D),class(C).
implied_range_in(R,D,C) :- range_in(R1,D1,C1),subrelation_of(R,R1), subclass_of(D1,D),subclass_of(C,C1).

% --
% rules for determining model-level incoherency
% --
unsatisfiable(C) :- subclass_of(C,A),subclass_of(C,B),class_disjoint_with(A,B).

incoherent :- unsatisfiable(_).
incoherent :- inconsistent(_).

% non-redundant form (i.e. subclasses of unsatisfiable classes are trivially unsatisfiable - exclude from this report)
nr_unsatisfiable(C) :- unsatisfiable(C), \+ ((unsatisfiable(Z),proper_subclass_of(C,Z))).


% ========================================
% instance-level reasoning
% ========================================


% bridge to URIs. For convenience we allow use of symbols instead of URIs, e.g. `biological_process`, these formally
% correspond to URIs suuch as http://w3id.org/biolink/vocab/BiologicalProcess
%
% uses asserted predicate: has_uri(ElementShortName, ElementURI) (from the yaml), and rdf/3 (instance data encoded as RDF)
direct_instance_of(I,C) :- rdf(I,rdf:type,Cx), has_uri(C,Cx).
direct_instance_of(I,C) :- rdf(I,rdf:type,C).

% inferred instance_of relation; propagates up subclass_of (recall subclass_of/2 is reflexive transitive form)
instance_of(I,C) :- direct_instance_of(I,C1), subclass_of(C1,C).

% mapping of RDF to facts.
direct_fact(I,P,J) :- rdf(I,Px,J), has_uri(P,Px), \+ rdf(I,rdf:type,J).
direct_fact(I,P,J) :- rdf(I,P,J), \+ rdf(I,rdf:type,J).

% data is inconsistent if any unsatisfiable classes are instantiated
inconsistent(I) :- instance_of(I,C),unsatisfiable(C).

% classification of instances can be induced by domain or range constraints.
% for example, if the domain and range of `friend-of` is `person`, and we have p1 friend-of p2,
% then p1 and and p2 is induced to be of type `person` (or a subclass of).
% note however, that this entailment is considered outside the object-oriented set of entailments,
% and unlike OWL open world semantics, domain/range is treated as a constraint, and if we
% get a new entailment from domain/range it is considered an error
domain_induced_instance_of(I,C) :- direct_fact(I,P,_), instance_of(I,C1),implied_domain_in(P,C,C1).
range_induced_instance_of(I,C) :- direct_fact(_,P,I), instance_of(I,C1),implied_range_in(P,C,C1).

% an instance is invalid if it is induced to instantiate a class C through domain or range constraints
% AND it is not inferred to be of that class via OO rules.
% thus if the domain/range of `friend-of` is `person`, and we have p1 friend-of p2, then
% both p1 and p2 must have been asserted to be of type `friend` (or one of its subclasses).
% note that this is different than OWL, as we treat domain/range as constraints.
invalid(I) :- domain_induced_instance_of(I,C),\+ instance_of(I,C).
invalid(I) :- range_induced_instance_of(I,C),\+ instance_of(I,C).

% an instance I is invalid if it tries to use (i.e. asserted a fact where I is subject) a disallowed slot.
% a slot must be explicitly declared for a class to be used (with OO inference)
invalid(I) :- direct_fact(I,P,_), \+ ((instance_of(I,IC), subrelation_of(P, PA), class_slot(IC, PA) )).

% cardinality of is_a is zero or one
invalid(C) :- is_a(C,P1),is_a(C,P2),P1\=P2.

% infer a more specific type relationship.
% note we do not do anything with this yet.
definition_induced_instance_of(I,C) :-
        defining_slots(C,Slots),is_a(C,Genus),instance_of(I,Genus),
        forall(member(Slot,Slots),
               (   (   class_slot_range(C,Slot,Range),
                       direct_fact(I,Slot,J),
                       instance_of(J,Range)))).


