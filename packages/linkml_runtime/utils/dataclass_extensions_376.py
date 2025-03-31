import sys
import dataclasses
import warnings

# Raise helpful error in unsupported Python versions
if sys.version_info >= (3, 13):
    raise RuntimeError(
        "The LinkML dataclass_extensions_376 is no longer compatible with Python 3.13 or newer.\n\n"
        "Python 3.13 removed _create_fn), which this extension relies on.\n\n"
        "To resolve this:\n"
        "  • Upgrade your LinkML schema and code to use LinkML >= 1.9.0, which no longer requires this patch\n"
        "  • Or migrate to Pydantic models for runtime dataclass behavior\n\n"
    )

# Emit deprecation warning in all other Python versions
warnings.warn(
    "The LinkML dataclass extension is deprecated and will be removed in a future release.\n"
    "Consider upgrading to LinkML >=1.9.0 or switching to Pydantic.",
    DeprecationWarning,
    stacklevel=2
)

# Patch _create_fn if it still exists
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
    DC_CREATE_FN = True

