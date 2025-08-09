from abc import ABC, abstractmethod


class NameHandlerBase(ABC):
    """
    An abstract base class providing a template for classes that handle naming conventions in generated code.
    """

    def render_name(self, range) -> str:
        """Renders a name as a string."""
        if range in self.schemaview.all_classes():
            return self.render_class_name(range)
        elif range in self.schemaview.all_types():
            raise Exception("not implemented")
        elif range in self.schemaview.all_enums():
            return self.render_enum_name(range)
        else:
            raise ValueError(f"Unknown type: {type(range)}")

    @abstractmethod
    def render_enum_name(self, enum_name: str) -> str:
        """Renders an enum name as a string."""
        pass

    @abstractmethod
    def render_class_name(self, class_name: str) -> str:
        """Renders a class name as a string."""
        pass

    @abstractmethod
    def render_slot_name(self, slot_name: str) -> str:
        """Renders a slot name as a string."""
        pass
