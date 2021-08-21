from typing import List

from linkml_runtime.utils.schemaview import SchemaView, CLASS_NAME

def roll_up(sv: SchemaView, classes: List[CLASS_NAME] = None) -> None:
    """
    rolls slots up to a set of ancestor classes
    :param sv:
    :param classes:
    :return:
    """
    if classes is None:
        classes = sv.class_roots()
    for cn in classes:
        c = sv.get_class(cn)
        slots = []
        for d in sv.class_descendants(cn, reflexive=False):
            for sn in sv.class_slots(d):
                s = sv.induced_slot(sn, class_name=d)
                if sn not in c.slots:
                    c.slots.append(sn)
                # if slot was declared as an attribute it may not be in the set of slots
                if sn not in sv.schema.slots:
                    # TODO: determine behavior for merging
                    sv.add_slot(s)
    sv.set_modified()

def roll_down(sv: SchemaView, classes: List[CLASS_NAME] = None) -> None:
    if classes is None:
        classes = sv.class_leaves()
    for cn in classes:
        c = sv.get_class(cn)
        slots = []
        for d in sv.class_ancestors(cn, reflexive=False):
            for sn in sv.class_slots(d):
                s = sv.induced_slot(sn, class_name=d)
                if sn not in c.slots:
                    c.slots.append(sn)
                # if slot was declared as an attribute it may not be in the set of slots
                if sn not in sv.schema.slots:
                    # TODO: determine behavior for merging
                    sv.add_slot(s)
    sv.set_modified()



