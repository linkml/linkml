user:term_expansion(t(P/A),
                    [
                     (   :- multifile P/A),
                     (   :- discontiguous P/A)
                    ]).



t(rdf/3).

t(class/1).
t(slot/1).
t(is_mixin/1).

t(required/1).
t(required_in/2).

t(multivalued/1).
t(multivalued_in/2).

t(slotrange/1).
t(range/2).
t(range_in/3).
t(domain/2).
t(domain_in/3).

t(class_slot/2).
t(range_in/3).
t(multivalued_in/2).
t(has_uri/2).
t(is_a/2).
t(mixin/2).
t(defining_slots/2).

% meta-preds for testing
t(expected/1).
t(not_expected/1).
