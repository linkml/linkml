import sys
import warnings
import dataclasses

warnings.warn(
    "The LinkML dataclass extension patch is deprecated and will be removed in a future release.\n"
    "If you're currently using Python < 3.13, where this patch still applies, you should:\n"
    "  • Upgrade your LinkML tooling to version >= 1.9.0 (which no longer needs this patch), OR\n"
    "  • Migrate to Pydantic models if you're using LinkML's generated classes at runtime.\n",
    DeprecationWarning,
    stacklevel=2
)

dataclasses_init_fn_with_kwargs = dataclasses._init_fn
DC_CREATE_FN = False