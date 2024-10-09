from typing import Union

from linkml_runtime.utils.schemaview import SchemaView, CLASS_NAME

CLASS_NAME_OR_LIST = Union[CLASS_NAME, list[CLASS_NAME]]

def roll_up(sv: SchemaView, classes: CLASS_NAME_OR_LIST = None, mixins=True, is_a=True, delete=True) -> None:
    """
    rolls slots up to a set of ancestor classes

    :param sv: view over source schema
    :param classes: all slots will be rolled up to these classes
    :param mixins: include mixins (default is True)
    :param is_a: include is_a parents (default is True)
    :return:
    """
    if classes is None:
        classes = sv.class_roots()
    if not isinstance(classes, list):
        classes = [classes]
    dels = set()
    for cn in classes:
        c = sv.get_class(cn)
        slots = []
        for d in sv.class_descendants(cn, reflexive=False, mixins=mixins, is_a=is_a):
            for sn in sv.class_slots(d):
                s = sv.induced_slot(sn, class_name=d)
                if sn not in c.slots:
                    c.slots.append(sn)
                # if slot was declared as an attribute it may not be in the set of slots
                if sn not in sv.schema.slots:
                    # TODO: determine behavior for merging
                    sv.add_slot(s)
            if delete:
                dels.add(d)
    for d in dels:
        sv.delete_class(d)
    sv.set_modified()

def roll_down(sv: SchemaView, classes: list[CLASS_NAME] = None, mixins=True, is_a=True, delete=True) -> None:
    """
    rolls down to a set of descendant classes

    :param sv:
    :param classes:
    :param mixins: include mixins (default is True)
    :param is_a: include is_a parents (default is True)
    :return:
    """
    if classes is None:
        classes = sv.class_leaves()
    dels = set()
    for cn in classes:
        c = sv.get_class(cn)
        slots = []
        for d in sv.class_ancestors(cn, reflexive=False, mixins=mixins, is_a=is_a):
            for sn in sv.class_slots(d):
                s = sv.induced_slot(sn, class_name=d)
                if sn not in c.slots:
                    c.slots.append(sn)
                # if slot was declared as an attribute it may not be in the set of slots
                if sn not in sv.schema.slots:
                    # TODO: determine behavior for merging
                    sv.add_slot(s)
            if delete:
                dels.add(d)
        # when we roll down with deletion, parent classes disappear,
        # cascading
        if delete and False:
            if mixins:
                c.mixins = []
            if is_a and c.is_a is not None:
                del c.is_a
    for d in dels:
        d_cls = sv.get_class(d)
        sv.delete_class(d)
    sv.set_modified()



