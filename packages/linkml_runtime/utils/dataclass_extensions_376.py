import sys
import warnings

warnings.warn(
    "The LinkML dataclass extension patch is deprecated and will be removed in a future release.\n"
    "If you're currently using Python < 3.13, where this patch still applies, you should:\n"
    "  • Upgrade your LinkML tooling to version >= 1.9.0 (which no longer needs this patch), OR\n"
    "  • Migrate to Pydantic models if you're using LinkML's generated classes at runtime.\n\n"
    "If you're currently using Python >= 3.13, this patch is ignored.",
    DeprecationWarning,
    stacklevel=2
)

# In Python < 3.13, still apply the dataclass extension patch
if sys.version_info < (3, 13):
    import dataclasses

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
    else:
        warnings.warn(
            "The LinkML dataclass patch could not be applied because `dataclasses._create_fn` is missing.\n"
            "This may indicate a nonstandard Python environment. "
            "Please upgrade to LinkML >= 1.9.0 or migrate to Pydantic.",
            RuntimeWarning,
            stacklevel=2,
        )
