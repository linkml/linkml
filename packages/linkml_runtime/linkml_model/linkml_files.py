import os
from enum import Enum, auto
from typing import Optional, Union

import requests
from rdflib import Namespace

LINKML_URL_BASE = "https://w3id.org/linkml/"
LINKML_NAMESPACE = Namespace(LINKML_URL_BASE)
GITHUB_IO_BASE = "https://linkml.github.io/linkml-model/"
GITHUB_BASE = "https://raw.githubusercontent.com/linkml/linkml-model/"
LOCAL_BASE = os.path.abspath(os.path.dirname(__file__))
GITHUB_API_BASE = "https://api.github.com/repos/linkml/linkml-model/"
GITHUB_RELEASES = GITHUB_BASE + "releases"
GITHUB_TAGS = GITHUB_BASE + "tags"




class _AutoName(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()


class Source(_AutoName):
    """ LinkML package source name """
    META = auto()
    TYPES = auto()
    MAPPINGS = auto()
    ANNOTATIONS = auto()
    EXTENSIONS = auto()


class Format(Enum):
    """ LinkML package formats """
    GRAPHQL = "graphql"
    HTML = ""
    JSON = "json"
    JSONLD = "context.jsonld"
    JSON_SCHEMA = "schema.json"
    NATIVE_JSONLD = "model.context.jsonld"
    NATIVE_RDF = "model.ttl"
    NATIVE_SHEXC = "model.shex"
    NATIVE_SHEXJ = "model.shexj"
    OWL = "owl.ttl"
    PYTHON = "py"
    RDF = "ttl"
    SHEXC = "shex"
    SHEXJ = "shexj"
    YAML = "yaml"


class _Path(Enum):
    """ LinkML Relative paths"""
    GRAPHQL = "graphql"
    HTML = "docs"
    JSON = "json"
    JSONLD = "jsonld"
    JSON_SCHEMA = "jsonschema"
    NATIVE_JSONLD = "jsonld"
    NATIVE_RDF = "ttl"
    NATIVE_SHEXC = "shex"
    NATIVE_SHEXJ = "shex"
    OWL = "owl"
    PYTHON = "linkml_model"
    RDF = "rdf"
    SHEXC = "shex"
    SHEXJ = "shex"
    YAML = "model/schema"


class ReleaseTag(_AutoName):
    """ Release tags
    LATEST - the absolute latest in the supplied branch
    CURRENT - the latest _released_ version in the supplied branch """
    LATEST = auto()
    CURRENT = auto()


def _build_path(source: Source, fmt: Format) -> str:
    """ Create the relative path for source and fmt """
    return f"{_Path[fmt.name].value}/{source.value}.{fmt.value}"


def _build_loc(base: str, source: Source, fmt: Format) -> str:
    return f"{base}{_build_path(source, fmt)}"


def URL_FOR(source: Source, fmt: Format) -> str:
    """ Return the URL to retrieve source in format """
    return f"{LINKML_URL_BASE}{source.value}.{fmt.value}"


def LOCAL_PATH_FOR(source: Source, fmt: Format) -> str:
    return os.path.join(LOCAL_BASE, _build_path(source, fmt))


def GITHUB_IO_PATH_FOR(source: Source, fmt: Format) -> str:
    return _build_loc(GITHUB_IO_BASE, source, fmt)


def GITHUB_PATH_FOR(source: Source,
                    fmt: Format,
                    release: Optional[Union[ReleaseTag, str]] = ReleaseTag.CURRENT,
                    branch: Optional[str] = "main") -> str:
    def do_request(url) -> object:
        resp = requests.get(url)
        if resp.ok:
            return resp.json()
        raise requests.HTTPError(f"{resp.status_code} - {resp.reason}: {url}")

    def tag_to_commit(tag: str) -> str:
        tags = do_request(f"{GITHUB_API_BASE}tags")
        for tagent in tags:
            if tagent['name'] == tag:
                return _build_loc(f"{GITHUB_BASE}blob/{tagent['commit']['sha']}/", source, fmt)
        raise ValueError(f"Tag: {tag} not found!")

    if release is not ReleaseTag.CURRENT and branch != "main":
        raise ValueError("Cannot specify both a release and a branch")

    # Return the absolute latest entry for branch
    if release is ReleaseTag.LATEST or (release is ReleaseTag.CURRENT and branch != "main"):
        return f"{GITHUB_BASE}{branch}/{_build_path(source, fmt)}"

    # Return the latest published version
    elif release is ReleaseTag.CURRENT:
        release = do_request(f"{GITHUB_API_BASE}releases/latest")
        return tag_to_commit(release['tag_name'])

    # Return a specific tag
    else:
        return tag_to_commit(release)


