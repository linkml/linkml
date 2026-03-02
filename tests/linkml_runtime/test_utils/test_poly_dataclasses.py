from linkml_runtime.linkml_model.meta import LINKML, Element


def test_class_for_uri():
    """Test various class lookup options for polymorphic dataclasses"""
    e = Element

    # Test class URI lookup
    cls = e._class_for_uri(LINKML.ClassDefinition)
    assert cls.__name__ == "ClassDefinition"

    # Test model URI lookup
    cls = e._class_for_uri(LINKML.TypeDefinition, use_model_uri=True)
    assert cls.__name__ == "TypeDefinition"

    # Test class curie lookup (note there isn't any model curie)
    cls = e._class_for_curie("linkml:TypeDefinition")
    assert cls.__name__ == "TypeDefinition"

    # Test self lookup works
    cls = e._class_for_uri(LINKML.Element)
    assert cls.__name__ == "Element"

    # Test graceful failure for missing classes
    cls = e._class_for_uri("linkml:Missing")
    assert cls is None
