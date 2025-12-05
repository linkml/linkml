"""Package for subclasses of SlotHandlerBase, etc. specific to Pandera schema generation"""

from .slot_handler_pandera import SlotHandlerPandera

__all__ = [
    "SlotHandlerPandera",
]
