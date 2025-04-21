import json
import os
from typing import Optional, Union


def flatten_dict(ctxt: str, base: str, seen: Optional[list[str]] = None) -> dict:

    def map_context(ctxt_ent: Union[str, dict, list], seen: list[str]) -> Union[dict, list]:
        if isinstance(ctxt_ent, str):
            ent_dict = flatten_dict(ctxt_ent, base, seen)
            return ent_dict['@context'] if '@context' in ent_dict else ent_dict
        elif isinstance(ctxt_ent, list):
            return [map_context(clent, seen) for clent in ctxt_ent]
        else:
            return map_dict(ctxt_ent, seen)

    def map_dict(inp: dict, seen: list[str]) -> dict:
        rval = dict()
        for k, v in inp.items():
            if k == '@context':
                v = map_context(v, seen)
            elif k == '@import':
                v = {}
            elif isinstance(v, dict):
                v = map_dict(v, seen)
            if v:
                rval[k] = v
        return rval

    if seen is None:
        seen = []
    elif ctxt in seen:
        return {}
    seen.append(ctxt)
    with open(os.path.join(base, ctxt)) as f:
        rval = map_dict(json.load(f), seen)
    seen.pop()
    return rval


def flatten(ctxt: str, base: str) -> str:
    print('_'*10 + f' Flattening {os.path.join(base, ctxt)}')
    return json.dumps(flatten_dict(ctxt, base), indent=2)


# ctxt_file = flatten('Package.context.jsonld', LD_11_DIR)
# with open(os.path.join(LD_11_DIR, 'termci_schema_inlined.context.jsonld'), 'w') as outf:
#     outf.write(ctxt_file)
