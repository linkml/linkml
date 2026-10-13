"""BCP 47 language tag validation shared across generators.

Centralises the syntactic validator and resolution policy used by
:mod:`linkml.generators.owlgen` and :mod:`linkml.generators.shaclgen`
for the ``--default-language`` feature.

The validator implements *well-formedness* in the sense of
RFC 5646 §2.2.9 (Classes of Conformance): conformance to the ABNF
grammar in §2.1. It does **not** check IANA registry validity --
that would require external data and is out of scope for a code
generator. RDF 1.1 §3.3 also requires only well-formedness for
``rdf:langString`` literals.

References
----------
- RFC 5646 -- Tags for Identifying Languages (BCP 47): https://www.rfc-editor.org/rfc/rfc5646
- RFC 5646 §2.1 (Syntax / ABNF): https://www.rfc-editor.org/rfc/rfc5646#section-2.1
- RFC 5646 §2.2.9 (Classes of Conformance): https://www.rfc-editor.org/rfc/rfc5646#section-2.2.9
- RDF 1.1 Concepts §3.3 (Literals): https://www.w3.org/TR/rdf11-concepts/#section-Graph-Literal
"""

from __future__ import annotations

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

# RFC 5646 §2.1 ABNF -- full grammar (langtag | privateuse | grandfathered).
# Each top-level alternative maps 1:1 to an ABNF production:
#   langtag       = language ["-" script] ["-" region] *("-" variant)
#                   *("-" extension) ["-" privateuse]
#   privateuse    = "x" 1*("-" (1*8alphanum))
#   grandfathered = irregular | regular  (closed list from §2.2.8)
BCP47_RE: re.Pattern[str] = re.compile(
    r"^(?:"
    # langtag
    r"(?:(?:[A-Za-z]{2,3}(?:-[A-Za-z]{3}){0,3})|[A-Za-z]{4}|[A-Za-z]{5,8})"
    r"(?:-[A-Za-z]{4})?"
    r"(?:-(?:[A-Za-z]{2}|\d{3}))?"
    r"(?:-(?:[A-Za-z\d]{5,8}|\d[A-Za-z\d]{3}))*"
    r"(?:-[0-9A-WY-Za-wy-z](?:-[A-Za-z\d]{2,8})+)*"
    r"(?:-x(?:-[A-Za-z\d]{1,8})+)?"
    # privateuse
    r"|x(?:-[A-Za-z\d]{1,8})+"
    # grandfathered (irregular)
    r"|en-GB-oed|i-ami|i-bnn|i-default|i-enochian|i-hak|i-klingon"
    r"|i-lux|i-mingo|i-navajo|i-pwn|i-tao|i-tay|i-tsu"
    r"|sgn-BE-FR|sgn-BE-NL|sgn-CH-DE"
    # grandfathered (regular)
    r"|art-lojban|cel-gaulish|no-bok|no-nyn|zh-guoyu"
    r"|zh-hakka|zh-min|zh-min-nan|zh-xiang"
    r")$",
    re.ASCII,
)


def is_well_formed_bcp47(tag: str) -> bool:
    """Return ``True`` if *tag* is well-formed per RFC 5646 §2.2.9.

    Well-formedness is conformance to the ABNF grammar in RFC 5646 §2.1;
    it does not imply IANA registry validity (RFC 5646 §2.2.9).
    """
    return bool(BCP47_RE.match(tag))


class LanguageTagResolver:
    """Resolve and validate BCP 47 language tags for code generators.

    The resolver implements the two-level policy used by both ``gen-owl``
    and ``gen-shacl``:

    1. ``element.in_language`` (per-element override) takes precedence
    2. fall back to the generator-level default

    Validation happens at most once per distinct malformed tag:

    - the generator-level default is validated **once** at construction;
    - per-element ``in_language`` values are validated the first time
      each distinct tag is observed and remembered in :attr:`_warned`.

    This avoids the original implementation's "hundreds of warnings per
    run" failure mode while still surfacing every distinct problem tag.
    """

    __slots__ = ("default", "_warned")

    def __init__(self, default: str | None) -> None:
        self.default: str | None = (default or "").strip() or None
        if self.default is not None and not is_well_formed_bcp47(self.default):
            logger.warning(
                "default language tag %r is not a well-formed BCP 47 tag (RFC 5646 §2.2.9)",
                self.default,
            )
        self._warned: set[str] = set()

    def resolve(self, element: Any = None) -> str | None:
        """Return the resolved BCP 47 tag for *element*, or ``None``.

        Resolution order is per-element first, generator default second.
        Empty or whitespace-only ``in_language`` values are ignored
        (the default is consulted instead).
        """
        if element is not None:
            element_lang = getattr(element, "in_language", None)
            if element_lang and element_lang.strip():
                tag = element_lang.strip()
                if not is_well_formed_bcp47(tag) and tag not in self._warned:
                    logger.warning(
                        "in_language value %r is not a well-formed BCP 47 tag (RFC 5646 §2.2.9)",
                        tag,
                    )
                    self._warned.add(tag)
                return tag
        return self.default
