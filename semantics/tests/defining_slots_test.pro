
class(gene).
class(pc_gene).
class(g2g).
class(a).
is_a(g2g,a).
is_a(pc_gene,gene).
defining_slots(g2g, [o]).
class_slot_range(g2g, s, gene).
class_slot_range(g2g, o, gene).

slot(r).
slot(s).
slot(o).
slot(interacts_with).

rdf(g1, rdf:type, pc_gene).
rdf(g2, rdf:type, pc_gene).
rdf(g2g_inst1, rdf:type, a).
rdf(g2g_inst1, r, interacts_with).
rdf(g2g_inst1, s, g1).
rdf(g2g_inst1, o, g2).

% TODO
expected(instance_of(g1,gene)).
expected(instance_of(g2,gene)).
expected(instance_of(g2g_inst1,a)).
expected(direct_fact(g2g_inst1,s,g1)).
expected(class_slot_range(g2g,s,gene)).
expected(class_slot_range(g2g,o,gene)).
expected(definition_induced_instance_of(g2g_inst1, g2g)).

not_expected(incoherent).
