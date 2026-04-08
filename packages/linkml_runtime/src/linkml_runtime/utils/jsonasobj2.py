"""Re-export jsonasobj2 symbols from linkml_runtime.

This shim centralises the jsonasobj2 dependency so that all linkml code
imports from ``linkml_runtime.utils.jsonasobj2`` instead of the external
package directly.  A future release may vendor or replace the underlying
implementation without requiring downstream import changes.
"""

from jsonasobj2 import (  # noqa: F401
    JsonObj,
    JsonObjTypes,
    as_dict,
    as_json,
    as_json_obj,
    is_dict,
    is_list,
    items,
    loads,
    values,
)
