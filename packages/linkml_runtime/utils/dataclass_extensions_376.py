import sys
import dataclasses
import warnings

# Block unsupported Python versions
if sys.version_info >= (3, 13):
    raise RuntimeError(
        "The LinkML dataclass_extensions_376 patch is no longer compatible with Python 3.13 or newer.\n\n"
        "Python 3.13 removed internal support for `_create_fn`, which this patch depends on.\n\n"
        "To resolve this:\n"
        "  • Upgrade your LinkML schema and code to use LinkML >= 1.9.0, which no longer uses this patch\n"
        "  • Or migrate to Pydantic models for dataclass behavior\n\n"
    )

# Warn that this extension is deprecated
warnings.warn(
    "The LinkML dataclass extension patch is deprecated and will be removed in a future release.\n"
    "Consider upgrading to LinkML >= 1.9.0 or switching Python class generation to Pydantic.",
    DeprecationWarning,
    stacklevel=2,
)

# Conditionally patch only if _create_fn exists
if hasattr(dataclasses, "_create_fn"):
    loc_fn = dataclasses._create_fn

    def dc_create_fn(name, args, body, *_posargs, **_kwargs):
        if name == '__init__' and dataclasses._POST_INIT_NAME in body[-1]:
            pi_parms = body[-1].rsplit(')', 1)[0]
            body[-1] = pi_parms + ('' if pi_parms[-1] == '(' else ',') + ' **_kwargs)'
            return loc_fn(name, list(args) + ["**_kwargs"], body, *_posargs, **_kwargs)
        else:
            return loc_fn(name, args, body, *_posargs, **_kwargs)

    dataclasses._create_fn = dc_create_fn
    dataclasses_init_fn_with_kwargs = dataclasses._init_fn

    warnings.warn(
        "LinkML dataclass patch successfully applied.",
        UserWarning,
        stacklevel=2,
    )
else:
    raise RuntimeError(
        "The LinkML dataclass_extensions_376 patch could not be applied: `dataclasses._create_fn` is missing.\n\n"
        "This likely indicates a nonstandard or altered Python environment, or partial compatibility with this patch.\n\n"
        "To proceed:\n"
        "  • Use a supported Python version where `_create_fn` is present (Python < 3.13)\n"
        "  • Or upgrade to LinkML >= 1.9.0 to remove reliance on this patch\n"
        "  • Or migrate to Pydantic models\n\n"
    )

# Used to signal that this patch was imported/applied
DC_CREATE_FN = True