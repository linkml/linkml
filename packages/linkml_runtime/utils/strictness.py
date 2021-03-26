

class BOOL:
    """  Boolean container -- supports global boolean variables """
    def __init__(self, v: bool) -> None:
        self.v = v

    def __bool__(self):
        return self.v

    def __str__(self):
        return str(self.v)


GLOBAL_STRICT = BOOL(True)


def strict() -> bool:
    """ Switch to global strict mode """
    rval = GLOBAL_STRICT.v
    GLOBAL_STRICT.v = True
    return rval


def lax() -> bool:
    """ Switch to global lax mode """
    rval = GLOBAL_STRICT.v
    GLOBAL_STRICT.v = False
    return rval


def is_strict() -> bool:
    """ Return the global strictness setting """
    return bool(GLOBAL_STRICT)
