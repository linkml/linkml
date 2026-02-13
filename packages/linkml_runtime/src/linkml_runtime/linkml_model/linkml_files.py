import os
from collections import namedtuple
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
    """LinkML package source name"""
    META = auto()
    TYPES = auto()
    MAPPINGS = auto()
    ANNOTATIONS = auto()
    EXTENSIONS = auto()


class Format(_AutoName):
    """LinkML package formats"""
    EXCEL = auto()
    GRAPHQL = auto()
    JSON = auto()
    JSONLD = auto()
    JSON_SCHEMA = auto()
    NATIVE_JSONLD = auto()
    NATIVE_RDF = auto()
    NATIVE_SHEXC = auto()
    NATIVE_SHEXJ = auto()
    OWL = auto()
    PREFIXMAP = auto()
    PROTOBUF = auto()
    PYTHON = auto()
    RDF = auto()
    SHACL = auto()
    SHEXC = auto()
    SHEXJ = auto()
    SQLDDL = auto()
    SQLSCHEMA = auto()
    YAML = auto()


_PathInfo = namedtuple("_PathInfo", ["path", "extension"])


class _Path:
    """LinkML Relative paths — maps each Format to its directory and file extension."""
    EXCEL = _PathInfo("excel", "xlsx")
    GRAPHQL = _PathInfo("graphql", "graphql")
    JSON = _PathInfo("json", "json")
    JSONLD = _PathInfo("jsonld", "context.jsonld")
    JSON_SCHEMA = _PathInfo("jsonschema", "schema.json")
    NATIVE_JSONLD = _PathInfo("jsonld", "model.context.jsonld")
    NATIVE_RDF = _PathInfo("rdf", "model.ttl")
    NATIVE_SHEXC = _PathInfo("shex", "shex")
    NATIVE_SHEXJ = _PathInfo("shex", "shexj")
    OWL = _PathInfo("owl", "owl.ttl")
    PREFIXMAP = _PathInfo("prefixmap", "yaml")
    PROTOBUF = _PathInfo("protobuf", "proto")
    PYTHON = _PathInfo("", "py")
    RDF = _PathInfo("rdf", "ttl")
    SHACL = _PathInfo("shacl", "shacl.ttl")
    SHEXC = _PathInfo("shex", "shex")
    SHEXJ = _PathInfo("shex", "shexj")
    SQLDDL = _PathInfo("sqlddl", "sql")
    SQLSCHEMA = _PathInfo("sqlschema", "sql")
    YAML = _PathInfo("model/schema", "yaml")

    @classmethod
    def items(cls):
        return {k: v for k, v in cls.__dict__.items() if isinstance(v, _PathInfo)}

    @classmethod
    def get(cls, item):
        if isinstance(item, Format):
            item = item.name
        return getattr(cls, item)


META_ONLY = (
    Format.EXCEL,
    Format.GRAPHQL,
    Format.OWL,
    Format.PREFIXMAP,
    Format.PROTOBUF,
    Format.SHACL,
    Format.SQLDDL,
    Format.SQLSCHEMA,
)


class ReleaseTag(_AutoName):
    """Release tags
    LATEST - the absolute latest in the supplied branch
    CURRENT - the latest _released_ version in the supplied branch"""
    LATEST = auto()
    CURRENT = auto()


def _build_path(source: Source, fmt: Format) -> str:
    """Create the relative path for source and fmt."""
    info = _Path.get(fmt.name)
    filename = f"{source.value}.{info.extension}"
    if info.path:
        return f"{info.path}/{filename}"
    return filename


def _build_loc(base: str, source: Source, fmt: Format) -> str:
    return f"{base}{_build_path(source, fmt)}".replace('blob/', '')


def URL_FOR(source: Source, fmt: Format) -> str:
    """Return the URL to retrieve source in format."""
    info = _Path.get(fmt.name)
    return f"{LINKML_URL_BASE}{source.value}.{info.extension}"


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
        tags = do_request(f"{GITHUB_API_BASE}tags?per_page=100")
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


class ModelFile:
    class ModelLoc:
        def __init__(self, model: Source, fmt: Format) -> str:
            self._model = model
            self._format = fmt
            self._path_info = _Path.get(fmt.name)

        def __str__(self):
            return f"{self._model.value}.{self._path_info.extension}"

        def __repr__(self):
            return str(self)

        @property
        def url(self) -> str:
            return URL_FOR(self._model, self._format)

        @property
        def file(self) -> str:
            return LOCAL_PATH_FOR(self._model, self._format)

        def github_loc(self, tag: Optional[str] = None, branch: Optional[str] = None, release: ReleaseTag = None) -> str:
            if not tag and not branch and not release:
                return GITHUB_IO_PATH_FOR(self._model, self._format)
            if tag:
                return GITHUB_PATH_FOR(self._model, self._format, tag, branch or "main")
            else:
                return GITHUB_PATH_FOR(self._model, self._format, release or ReleaseTag.CURRENT, branch or "main")

    def __init__(self, model: Source) -> None:
        self._model = model

    def __str__(self):
        return self._model.value

    def __repr__(self):
        return str(self)

    @property
    def graphql(self) -> ModelLoc:
        return ModelFile.ModelLoc(self._model, Format.GRAPHQL)

    @property
    def json(self) -> ModelLoc:
        return ModelFile.ModelLoc(self._model, Format.JSON)

    @property
    def jsonld(self) -> ModelLoc:
        return ModelFile.ModelLoc(self._model, Format.JSONLD)

    @property
    def jsonschema(self) -> ModelLoc:
        return ModelFile.ModelLoc(self._model, Format.JSON_SCHEMA)

    @property
    def model_jsonld(self) -> ModelLoc:
        return ModelFile.ModelLoc(self._model, Format.NATIVE_JSONLD)

    @property
    def model_rdf(self) -> ModelLoc:
        return ModelFile.ModelLoc(self._model, Format.NATIVE_RDF)

    @property
    def model_shexc(self) -> ModelLoc:
        return ModelFile.ModelLoc(self._model, Format.NATIVE_SHEXC)

    @property
    def model_shexj(self) -> ModelLoc:
        return ModelFile.ModelLoc(self._model, Format.NATIVE_SHEXJ)

    @property
    def owl(self) -> ModelLoc:
        return ModelFile.ModelLoc(self._model, Format.OWL)

    @property
    def python(self) -> ModelLoc:
        return ModelFile.ModelLoc(self._model, Format.PYTHON)

    @property
    def rdf(self) -> ModelLoc:
        return ModelFile.ModelLoc(self._model, Format.RDF)

    @property
    def shexc(self) -> ModelLoc:
        return ModelFile.ModelLoc(self._model, Format.SHEXC)

    @property
    def shexj(self) -> ModelLoc:
        return ModelFile.ModelLoc(self._model, Format.SHEXJ)

    @property
    def yaml(self) -> ModelLoc:
        return ModelFile.ModelLoc(self._model, Format.YAML)


meta = ModelFile(Source.META)
types = ModelFile(Source.TYPES)
annotations = ModelFile(Source.ANNOTATIONS)
extensions = ModelFile(Source.EXTENSIONS)
mappings = ModelFile(Source.MAPPINGS)
