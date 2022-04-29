import dataclasses
#
# The dataclass library builds a rigid `__init__` function that doesn't allow any unrecognized named parameters
#
# The purpose of this extension is to enhance the library to allow additional keyword arguments to passed in
# and then on to the __post_init__ function that can deal with them accordingly

# Beware that there is no promise that signature of the create function will remain consistent
loc_fn = dataclasses._create_fn


def dc_create_fn(name, args, body, *_posargs, **_kwargs):
    # If overriding the initializer and using a post init
    if name == '__init__' and dataclasses._POST_INIT_NAME in body[-1]:
        # Then insert the kwargs into the both the call and the post init
        pi_parms = body[-1].rsplit(')', 1)[0]
        body[-1] = pi_parms + ('' if pi_parms[-1] == '(' else ',') + ' **_kwargs)'
        return loc_fn(name, list(args) + ["**_kwargs"], body, *_posargs, **_kwargs)
    else:
        return loc_fn(name, args, body, *_posargs, **_kwargs)


dataclasses._create_fn = dc_create_fn

# The following line is here solely to be backwards compatible.
dataclasses_init_fn_with_kwargs = dataclasses._init_fn

# The following line can be used to make certain that the import of the new create function doesn't get
# discarded as being potentially unused
DC_CREATE_FN = True
