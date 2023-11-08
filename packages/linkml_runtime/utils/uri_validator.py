# Copyright Siemens 2023
# SPDX-License-Identifier: CC0-1.0

import re

"""
Regular-expression-based URI and CURIE validation functions

These regex are directly derived from the official sources mentioned in each
section.

They should be processed with re.VERBOSE.

Python named regular expression groups are being used to better understand the
URI/CURIE parsing.
"""


# -----------------------------------------------------------------------------
#
### BASICS

# Define DIGIT according RFC2234 section 3.4:
# https://datatracker.ietf.org/doc/html/rfc2234/#section-3.4
DIGIT = r"[0-9]"

# Define ALPHA according RFC2234 section 6.1:
# https://datatracker.ietf.org/doc/html/rfc2234/#section-6.1
ALPHA = r"[A-Za-z]"

# Define HEXDIG according RFC2234 section 6.1:
# https://datatracker.ietf.org/doc/html/rfc2234/#section-6.1
HEXDIG = r"[0-9A-Fa-f]"

#   pct-encoded   = "%" HEXDIG HEXDIG
pct_encoded = rf"% {HEXDIG} {HEXDIG}"

#   unreserved    = ALPHA / DIGIT / "-" / "." / "_" / "~"
unreserved = rf"(?: {ALPHA} | {DIGIT} | \- | \. | _ | ~ )"

#   gen-delims    = ":" / "/" / "?" / "#" / "[" / "]" / "@"
gen_delims = r"(?: : | / | \? | \# | \[ | \] | @ )"

#   sub-delims    = "!" / "$" / "&" / "'" / "("
sub_delims = r"(?: ! | \$ | & | ' | \( | \) | \* | \+ | , | ; | = )"

#   pchar         = unreserved / pct-encoded / sub-delims / ":" / "@"
pchar = rf"(?: {unreserved} | {pct_encoded} | {sub_delims} | : | @ )"

#   reserved      = gen-delims / sub-delims
reserved = rf"(?: {gen_delims} | {sub_delims} )"


### required for Authority

#   dec-octet     = DIGIT                 ; 0-9
#                 / %x31-39 DIGIT         ; 10-99
#                 / "1" 2DIGIT            ; 100-199
#                 / "2" %x30-34 DIGIT     ; 200-249
#                 / "25" %x30-35          ; 250-255
dec_octet = rf"""(?: {DIGIT} |
                    [1-9] {DIGIT} |
                    1 {DIGIT}{{2}} |
                    2 [0-4] {DIGIT} |
                    25 [0-5]
                )
"""

#  IPv4address   = dec-octet "." dec-octet "." dec-octet "." dec-octet
IPv4address = rf"{dec_octet} \. {dec_octet} \. {dec_octet} \. {dec_octet}"

#  h16           = 1*4HEXDIG
h16 = rf"(?: {HEXDIG} ){{1,4}}"

#  ls32          = ( h16 ":" h16 ) / IPv4address
ls32 = rf"(?: (?: {h16} : {h16} ) | {IPv4address} )"

#   IPv6address   =                            6( h16 ":" ) ls32
#                 /                       "::" 5( h16 ":" ) ls32
#                 / [               h16 ] "::" 4( h16 ":" ) ls32
#                 / [ *1( h16 ":" ) h16 ] "::" 3( h16 ":" ) ls32
#                 / [ *2( h16 ":" ) h16 ] "::" 2( h16 ":" ) ls32
#                 / [ *3( h16 ":" ) h16 ] "::"    h16 ":"   ls32
#                 / [ *4( h16 ":" ) h16 ] "::"              ls32
#                 / [ *5( h16 ":" ) h16 ] "::"              h16
#                 / [ *6( h16 ":" ) h16 ] "::"
IPv6address = rf"""(?:                              (?: {h16} : ){{6}} {ls32} |
                                                 :: (?: {h16} : ){{5}} {ls32} |
                                    (?: {h16} )? :: (?: {h16} : ){{4}} {ls32} |
               (?: (?: {h16} : )        {h16} )? :: (?: {h16} : ){{3}} {ls32} |
               (?: (?: {h16} : ){{1,2}} {h16} )? :: (?: {h16} : ){{2}} {ls32} |
               (?: (?: {h16} : ){{1,3}} {h16} )? ::     {h16} :        {ls32} |
               (?: (?: {h16} : ){{1,4}} {h16} )? ::                    {ls32} |
               (?: (?: {h16} : ){{1,5}} {h16} )? ::                    {h16}  |
               (?: (?: {h16} : ){{1,6}} {h16} )? ::
              )
"""

#   IPvFuture     = "v" 1*HEXDIG "." 1*( unreserved / sub-delims / ":" )
IPvFuture = rf"v {HEXDIG}+ \. (?: {unreserved} | {sub_delims} | : )+"

#   IP-literal    = "[" ( IPv6address / IPvFuture  ) "]"
IP_literal = rf"\[ (?: {IPv6address} | {IPvFuture} ) \]"

#   reg-name      = *( unreserved / pct-encoded / sub-delims )
reg_name = rf"(?: {unreserved} | {pct_encoded} | {sub_delims} )*"


### required for Path

#   segment       = *pchar
segment = rf"{pchar}*"

#   segment-nz    = 1*pchar
segment_nz = rf"{pchar}+"

#   segment-nz-nc = 1*( unreserved / pct-encoded / sub-delims / "@" )
segment_nz_nc = rf"(?: {unreserved} | {pct_encoded} | {sub_delims} | @ )+"

# -----------------------------------------------------------------------------
#
# Define SCHEME according RFC3986 section 3.1:
# https://datatracker.ietf.org/doc/html/rfc3986/#section-3.1
#

#   scheme        = ALPHA *( ALPHA / DIGIT / "+" / "-" / "." )
scheme = rf"(?P<scheme> {ALPHA} (?: {ALPHA} | {DIGIT} | \+ | \- | \. )* )"


# -----------------------------------------------------------------------------
#
# Define AUTHORITY according RFC3986 section 3.2:

# Define USER INFORMATION according RFC3986 section 3.2.1:
# https://datatracker.ietf.org/doc/html/rfc3986/#section-3.2.1

#   userinfo      = *( unreserved / pct-encoded / sub-delims / ":" )
userinfo = rf"""(?P<userinfo>
                    (?: {unreserved} | {pct_encoded} | {sub_delims} | : )*
                )
"""

# Define HOST according RFC3986 section 3.2.2:
# https://datatracker.ietf.org/doc/html/rfc3986/#section-3.2.2

#   host          = IP-literal / IPv4address / reg-name
host = rf"(?P<host> {IP_literal} | {IPv4address} | {reg_name} )"

# Define PORT according RFC3986 section 3.2.3:
# https://datatracker.ietf.org/doc/html/rfc3986/#section-3.2.3

#   port          = *DIGIT
port = rf"(?P<port> ( {DIGIT} )* )"

# Define AUTHORITY according RFC3986 section 3.2:
# https://datatracker.ietf.org/doc/html/rfc3986/#section-3.2
#

#   authority     = [ userinfo "@" ] host [ ":" port ]
#authority = rf"""(?: (?P<userinfo> {userinfo} ) @)?
authority = rf"""(?P<authority>
                    (?: {userinfo} @)?
                    {host}
                    (?: : {port} )?
                )
"""


# -----------------------------------------------------------------------------
#
# Define different PATHs according RFC3986 section 3.3:
# https://datatracker.ietf.org/doc/html/rfc3986/#section-3.3
#

#   path-abempty  = *( "/" segment )
path_abempty = rf"( / {segment} )*"

#   path-absolute = "/" [ segment-nz *( "/" segment ) ]
path_absolute = rf"( / (?: {segment_nz} (?: / {segment} )* )? )"

#   path-noscheme = segment-nz-nc *( "/" segment )
path_noscheme = rf"( {segment_nz_nc} (?: / {segment} )* )"

#   path-rootless = segment-nz *( "/" segment )
path_rootless = rf"( {segment_nz} (?: / {segment} )* )"

#   path-empty    = 0<pchar>
path_empty = r""

#   path          = path-abempty    ; begins with "/" or is empty
#                 / path-absolute   ; begins with "/" but not "//"
#                 / path-noscheme   ; begins with a non-colon segment
#                 / path-rootless   ; begins with a segment
#                 / path-empty      ; zero characters
path = rf"""(?:
               {path_abempty} |
               {path_absolute} |
               {path_noscheme} |
               {path_rootless} |
               {path_empty}
            )
"""


# -----------------------------------------------------------------------------
#
# Define QUERY according RFC3986 section 3.4:
# https://datatracker.ietf.org/doc/html/rfc3986/#section-3.4
#

#   query         = *( pchar / "/" / "?" )
query = rf"(?P<query> (?: {pchar} | / | \? )* )"


# -----------------------------------------------------------------------------
#
# Define FRAGMENT according RFC3986 section 3.5:
# https://datatracker.ietf.org/doc/html/rfc3986/#section-3.5
#

#   fragment      = *( pchar / "/" / "?" )
fragment = rf"(?P<fragment> (?: {pchar} | / | \? )* )"


# -----------------------------------------------------------------------------
#
# Define URI and HIERARCHICAL PATH according RFC3986 section 3:
# https://datatracker.ietf.org/doc/html/rfc3986/#section-3
#

#   hier-part     = "//" authority path-abempty
#                 / path-absolute
#                 / path-rootless
#                 / path-empty
hier_part = rf"""(?P<hier_part>
                    (?: // {authority} {path_abempty} ) |
                    {path_absolute} |
                    {path_rootless} |
                    {path_empty}
                )
"""


#   URI           = scheme ":" hier-part [ "?" query ] [ "#" fragment ]
URI = rf"""(?P<uri>
                {scheme} : {hier_part} (?: \? {query} )? (?: \# {fragment} )?
            )
"""


# -----------------------------------------------------------------------------
#
# Define RELATIVE REFERENCE according RFC3986 section 4.2:
# https://datatracker.ietf.org/doc/html/rfc3986/#section-4.2
#

#   relative-part = "//" authority path-abempty
#                 / path-absolute
#                 / path-noscheme
#                 / path-empty
#   relative-ref  = relative-part [ "?" query ] [ "#" fragment ]
relative_ref = rf"""(?P<relative_ref>
                        (?:
                            (?: //
                                {authority}
                                (?P<path_abempty> {path_abempty} )
                            ) |
                            (?P<path_absolute> {path_absolute} ) |
                            (?P<path_noscheme> {path_noscheme} ) |
                            (?P<path_empty> {path_empty} )
                         )
                         (?: \? {query} )?
                         (?: \# {fragment} )?
                     )
"""

# -----------------------------------------------------------------------------
#
# Define ABSOLUTE URI according RFC3986 section 4.3:
# https://datatracker.ietf.org/doc/html/rfc3986/#section-4.3
#

#   absolute-URI  = scheme ":" hier-part [ "?" query ]
absolute_URI = rf"(?P<absolute_URI> {scheme} : {hier_part} (?: \? {query} )? )"


# -----------------------------------------------------------------------------
#
# Define CURIE according W3C CURIE Syntax 1.0
# https://www.w3.org/TR/curie/#s_syntax
#

# NCNameChar	::=	Letter | Digit | '.' | '-' | '_' | CombiningChar | Extender
# !! IMPORTANT NOTE !!
# As of now this module doesn't support NCNameChar IRI, but
# relative-refs as defined in URI,
# NCNameChar	::=	Letter | Digit | '.' | '-' | '_'
NCNameChar = rf"(?: {ALPHA} | {DIGIT} | \. | \- | _ )"

# prefix      :=   NCName
# NCName  :=   (Letter | '_') (NCNameChar)*
prefix = rf"(?: {ALPHA} | _ ) (?: {NCNameChar} )*"

# reference   :=   irelative-ref (as defined in IRI)
# !! IMPORTANT NOTE !!
# As of now this module don't support irelative-refs as defined in IRI, but
# relative-refs as defined in URI
# curie       :=   [ [ prefix ] ':' ] reference
# reference   :=   relative-ref (as defined in URI)
CURIE = rf"""(?P<CURIE>
                (?: (?P<prefix> {prefix} )? : )?
                {relative_ref}
             )
"""

# safe_curie  :=   '[' curie ']'
safe_CURIE = rf"""(?P<safe_CURIE>
                        \[ {CURIE} \]
                  )
"""


# -----------------------------------------------------------------------------
#
### Compile the regular expressions for better performance

uri_validator = re.compile(f"^{URI}$", re.VERBOSE)

#uri_ref_validator = re.compile(f"^{URI_reference}$", re.VERBOSE)

uri_relative_ref_validator = re.compile(f"^{relative_ref}$", re.VERBOSE)

abs_uri_validator = re.compile(f"^{absolute_URI}$", re.VERBOSE)

curie_validator = re.compile(f"^{CURIE}$", re.VERBOSE)

safe_curie_validator = re.compile(f"^{safe_CURIE}$", re.VERBOSE)

# -----------------------------------------------------------------------------
#
### FUNCTIONS


def validate_uri(input):
    return uri_validator.match(input)


def validate_uri_reference(input):
    # -----------------------------------------------------------------------------
    #
    # Define URI REFERENCE according RFC3986 section 4.1:
    # https://datatracker.ietf.org/doc/html/rfc3986/#section-4.1
    #

    #   URI-reference = URI / relative-ref
    return uri_validator.match(input) or uri_relative_ref_validator.match(input)


def validate_curie(input):
    return curie_validator.match(input)

