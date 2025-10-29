from linkml_runtime.linkml_model.meta import PermissibleValue, PermissibleValueText


class EnumGeneratorMixin:
    def escape_permissible_value_text(self, pv_text):
        return pv_text.replace("'", "\\'").replace('"', '\\"')

    def extract_permissible_text(self, pv):
        if isinstance(pv, str) or isinstance(pv, PermissibleValueText):
            return self.escape_permissible_value_text(pv)
        elif isinstance(pv, PermissibleValue):
            return pv.text.code
        else:
            raise ValueError(f"Invalid permissible value in enum : {pv}")

    def get_enum_permissible_values(self, enum):
        return list(map(self.extract_permissible_text, enum.permissible_values or []))
