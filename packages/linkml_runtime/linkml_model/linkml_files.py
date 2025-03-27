from pathlib import Path
from enum import Enum, auto
from typing import Optional, Union, NamedTuple
from urllib.parse import urljoin
from dataclasses import dataclass

import requests
from rdflib import Namespace

LINKML_URL_BASE = "https://w3id.org/linkml/"
LINKML_NAMESPACE = Namespace(LINKML_URL_BASE)
GITHUB_IO_BASE = "https://linkml.github.io/linkml-model/"
GITHUB_BASE = "https://raw.githubusercontent.com/linkml/linkml-model/"
LOCAL_BASE = Path(__file__).parent.resolve()
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


class Format(_AutoName):
    """ LinkML package formats """
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

@dataclass
class FormatPath:
    path: str
    extension: str

    def model_path(self, model:str) -> Path:
        return (Path(self.path) / model).with_suffix(self.extension)

class _Path:
    """ LinkML Relative paths"""
    EXCEL = FormatPath("excel","xlsx" )
    GRAPHQL = FormatPath("graphql","graphql" )
    JSON = FormatPath("json","json" )
    JSONLD = FormatPath("jsonld","context.jsonld" )
    JSON_SCHEMA = FormatPath("jsonschema", "schema.json" )
    NATIVE_JSONLD = FormatPath("jsonld", "context.jsonld" )
    NATIVE_RDF = FormatPath("rdf","ttl" )
    NATIVE_SHEXC = FormatPath("shex","shex" )
    NATIVE_SHEXJ = FormatPath("shex","shexj" )
    OWL = FormatPath("owl","owl.ttl" )
    PREFIXMAP = FormatPath('prefixmap','yaml' )
    PROTOBUF = FormatPath("protobuf","proto" )
    PYTHON = FormatPath("","py" )
    RDF = FormatPath("rdf","ttl" )
    SHACL = FormatPath("shacl","shacl.ttl" )
    SHEXC = FormatPath("shex","shex" )
    SHEXJ = FormatPath("shex","shexj" )
    SQLDDL = FormatPath("sqlddl","sql" )
    SQLSCHEMA = FormatPath("sqlschema","sql" )
    YAML = FormatPath((Path("model") / "schema").as_posix(),"yaml" )

    @classmethod
    def items(cls) -> dict[str, FormatPath]:
        return {k:v for k,v in cls.__dict__.items() if not k.startswith('_')}

    @classmethod
    def get(cls, item:Union[str,Format]) -> FormatPath:
        if isinstance(item, Format):
            item = item.name.upper()
        return getattr(cls, item)

    def __class_getitem__(cls, item:str) -> FormatPath:
        return getattr(cls, item)


META_ONLY = (
    Format.EXCEL,
    Format.GRAPHQL,
    Format.OWL,
    Format.PREFIXMAP,
    Format.PROTOBUF,
    Format.SHACL,
    Format.SQLDDL,
    Format.SQLSCHEMA
)


class ReleaseTag(_AutoName):
    """ Release tags
    LATEST - the absolute latest in the supplied branch
    CURRENT - the latest _released_ version in the supplied branch """
    LATEST = auto()
    CURRENT = auto()


class PathParts(NamedTuple):
    format: str
    file: str


def _build_path(source: Source, fmt: Format) -> PathParts:
    """
    Create the parts for a relative path for source and fmt.
    Combined elsewhere into a complete path, since OS paths and URLs differ.
    """
    fmt_path: FormatPath = _Path.get(fmt.name)
    return PathParts(fmt_path.path, f"{source.value}.{fmt_path.extension}")


def _build_loc(base: str, source: Source, fmt: Format) -> str:
    """A github location"""
    # urls are always forward slash separated, so hardcoding is appropriate here
    path = '/'.join(_build_path(source, fmt))
    return urljoin(base, path).replace('blob/', '')


def URL_FOR(source: Source, fmt: Format) -> str:
    """ Return the URL to retrieve source in format """
    fmt_path: FormatPath = _Path.get(fmt.name)
    return f"{LINKML_URL_BASE}{source.value}.{fmt_path.extension}"


def LOCAL_PATH_FOR(source: Source, fmt: Format) -> str:
    return str(LOCAL_BASE.joinpath(*_build_path(source, fmt)))


def GITHUB_IO_PATH_FOR(source: Source, fmt: Format, version="latest") -> str:
    path = '/'.join([version, 'linkml_model', *_build_path(source, fmt)])
    return urljoin(GITHUB_IO_BASE, path)


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
        path = '/'.join([branch, 'linkml_model', *_build_path(source, fmt)])
        return urljoin(GITHUB_BASE, path)

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
            self._fmt_path = _Path.get(fmt.name)

        def __str__(self):
            return f"{self._model.value}.{self._fmt_path.extension}"

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
