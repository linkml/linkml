import dataclasses
#
# The dataclass library builds a rigid `__init__` function that doesn't allow any unrecognized named parameters
#
# The purpose of this extension is to enhance the library to allow additional keyword arguments to passed in
# and then on to the __post_init__ function that can deal with them accordingly

# Beware that there is no promise that signature of the create function will remain consistent

def _create_fn(name, args, body, *, globals=None, locals=None,
               return_type=MISSING):
    # Note that we mutate locals when exec() is called.  Caller
    # beware!  The only callers are internal to this module, so no
    # worries about external callers.
    if locals is None:
        locals = {}
    if 'BUILTINS' not in locals:
        locals['BUILTINS'] = builtins
    return_annotation = ''
    if return_type is not MISSING:
        locals['_return_type'] = return_type
        return_annotation = '->_return_type'
    args = ','.join(args)
    body = '\n'.join(f'  {b}' for b in body)

    # Compute the text of the entire function.
    txt = f' def {name}({args}){return_annotation}:\n{body}'

    local_vars = ', '.join(locals.keys())
    txt = f"def __create_fn__({local_vars}):\n{txt}\n return {name}"
    ns = {}
    exec(txt, globals, ns)
    return ns['__create_fn__'](**locals)


loc_fn = _create_fn()


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
