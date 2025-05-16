import logging
import re
import unicodedata
from enum import Enum


class NamingProfiles(str, Enum):
    # GraphQL naming profile ensures compatibility with the GraphQL specification
    # WRT names: https://spec.graphql.org/October2021/#Name
    graphql = "graphql"


class NameCompatibility:
    """Make a name compatible to the given profile"""

    # heading double underscores and digit reserved to names starting with a digit
    re_reserved_heading_digit = re.compile("^__[0-9]")
    # valid name between double underscores is reserved for unicode name transformations
    re_reserved_unicode_name_transformation = re.compile("__[0-9a-zA-Z][0-9a-zA-Z_]*__")
    # something like '__U_xxxx_' is reserved for unicode code transformations
    re_reserved_unicode_code_transformation = re.compile("__U_[0-9a-eA-E]{4}_")
    # strings starting with a digit
    re_heading_digit = re.compile("^[0-9]")
    # character that is neither alphanumeric nor underscore
    re_no_alphanum_underscore = re.compile("[^0-9a-zA-Z_]")

    def __init__(self, profile: NamingProfiles, do_not_fix: bool = False):
        """Specify the naming policy on instantiation"""
        self.profile = profile
        self.do_not_fix = do_not_fix

    def _no_heading_digits(self, input: str) -> str:
        """Ensure name does not start with a heading digit"""
        output = input
        if self.re_heading_digit.match(input):
            if self.do_not_fix:
                raise ValueError(f"Name '{input}' starts with digit (illegal GraphQL) and will not be fixed!")
            else:
                logging.warning(
                    f"Name '{input}' starts with digit (illegal GraphQL), "
                    + f"it has been prefixed with '__', resulting in {output}"
                )
            output = f"__{input}"
        return output

    def _transform_char(self, char: str) -> str:
        """Transform unsupported characters"""
        if len(char) != 1:
            raise Exception(f"Single character expected, but got '{char}'!!")
        # replace whitespaces with underscores
        # the transformation cannot be inverted, but is a well-established
        # and expected transformation
        if char == " ":
            return "_"
        # try to use names for ASCII characters
        if ord(char) < 128:
            try:
                # unicodedata.lookup should be able to invert the transformation
                return f"__{unicodedata.name(char).replace(' ', '_').replace('-', '_')}__"
            except ValueError:
                pass
        # fallback to code-transformation if none of the previous has worked
        return f"__U_{ord(char):04X}_"

    def _only_alphanum_underscore(self, input: str) -> str:
        """Ensure name does not contain any unsupported characters"""
        output = input
        # with re.split and re.findall we get in the same order and separated in two arrays
        # the substrings between special characters and the special characters
        no_alphanum_underscore_match = self.re_no_alphanum_underscore.findall(input)
        if no_alphanum_underscore_match:
            if self.do_not_fix:
                raise ValueError(f"Name '{input}' contains a character illegal in GraphQL and will not be fixed!")
            else:
                logging.warning(
                    f"Name '{input}' contains a character illegal in GraphQL, "
                    + f"the resulting encoded name is {output}"
                )
            to_keep = self.re_no_alphanum_underscore.split(input)
            # first comes first substring to keep
            output = to_keep[0]
            # each char replacement is followed by the next substring to keep
            for offset in range(0, len(to_keep) - 1):
                output = output + self._transform_char(no_alphanum_underscore_match[offset])
                output = output + to_keep[offset + 1]
        return output

    def _graphql_compatibility(self, input: str) -> str:
        """Ensure name compatibility with GraphQL name policies"""
        # as of now, some (hopefully) very rare patterns are reserved to mark transformations
        if self.re_reserved_heading_digit.match(input):
            raise NotImplementedError("Names starting with a double underscore followed by a digit are not supported!!")
        if self.re_reserved_unicode_name_transformation.match(input):
            raise NotImplementedError("Names containing valid names between double underscores are not supported!!")
        if self.re_reserved_unicode_code_transformation.match(input):
            raise NotImplementedError("Names containing strings like '__U_xxxx_' are not supported!!")
        # apply transformation
        output = input
        output = self._no_heading_digits(output)
        output = self._only_alphanum_underscore(output)
        return output

    def compatible(self, input: str) -> str:
        """Make given name compatible with the given naming policy."""
        if self.profile == "graphql":
            return self._graphql_compatibility(input)
