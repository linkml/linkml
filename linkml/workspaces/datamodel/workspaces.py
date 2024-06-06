# Auto generated from workspaces.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-04-07T18:13:53
# Schema: workspace
#
# id: https://w3id.org/linkml/workspace
# description: A datamodel for Workspaces. A workspace is a local on-disk collection of projects managed by a
#              single user or agent
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional, Union

from jsonasobj2 import as_dict
from linkml_runtime.linkml_model.types import String
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.metamodelcore import Bool, XSDDateTime, empty_dict, empty_list
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str
from rdflib import URIRef

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
CSVW = CurieNamespace("csvw", "http://www.w3.org/ns/csvw#")
DCAT = CurieNamespace("dcat", "http://www.w3.org/ns/dcat#")
FORMATS = CurieNamespace("formats", "http://www.w3.org/ns/formats/")
FRICTIONLESS = CurieNamespace("frictionless", "https://specs.frictionlessdata.io/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
MEDIATYPES = CurieNamespace("mediatypes", "https://www.iana.org/assignments/media-types/")
OWL = CurieNamespace("owl", "http://www.w3.org/2002/07/owl#")
PAV = CurieNamespace("pav", "http://purl.org/pav/")
RDF = CurieNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = CurieNamespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
SCHEMA = CurieNamespace("schema", "http://schema.org/")
SH = CurieNamespace("sh", "https://w3id.org/shacl/")
SKOS = CurieNamespace("skos", "http://www.w3.org/2004/02/skos/core#")
VOID = CurieNamespace("void", "http://rdfs.org/ns/void#")
WORKSPACE = CurieNamespace("workspace", "https://w3id.org/linkml/workspace")
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = WORKSPACE


# Types
class FileSystemPath(String):
    """A local or absolute path on a file system"""

    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "FileSystemPath"
    type_model_uri = WORKSPACE.FileSystemPath


class ProjectName(String):
    """A project name MUST contain no whitespace and SHOULD only contains
    alphanumeric characters and hyphens (no underscores)"""

    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "ProjectName"
    type_model_uri = WORKSPACE.ProjectName


# Class references
class ProjectName(ProjectName):
    pass


class GoogleSheetsDocId(extended_str):
    pass


Any = Any


@dataclass
class Project(YAMLRoot):
    """
    A project consists of a single root schema
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = WORKSPACE.Project
    class_class_curie: ClassVar[str] = "workspace:Project"
    class_name: ClassVar[str] = "Project"
    class_model_uri: ClassVar[URIRef] = WORKSPACE.Project

    name: Union[str, ProjectName] = None
    uuid: Optional[str] = None
    github_organization: Optional[Union[dict, "GitHubAccount"]] = None
    creation_date: Optional[Union[str, XSDDateTime]] = None
    schema: Optional[Union[dict, Any]] = None
    description: Optional[str] = None
    source_schema_path: Optional[Union[str, FileSystemPath]] = None
    data_files: Optional[Union[Union[str, FileSystemPath], List[Union[str, FileSystemPath]]]] = empty_list()
    source_google_sheet_docs: Optional[
        Union[
            Dict[Union[str, GoogleSheetsDocId], Union[dict, "GoogleSheetsDoc"]],
            List[Union[dict, "GoogleSheetsDoc"]],
        ]
    ] = empty_dict()
    project_directory: Optional[Union[str, FileSystemPath]] = None
    external_project_path: Optional[Union[str, FileSystemPath]] = None
    last_saved: Optional[Union[str, XSDDateTime]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, ProjectName):
            self.name = ProjectName(self.name)

        if self.uuid is not None and not isinstance(self.uuid, str):
            self.uuid = str(self.uuid)

        if self.github_organization is not None and not isinstance(self.github_organization, GitHubAccount):
            self.github_organization = GitHubAccount(**as_dict(self.github_organization))

        if self.creation_date is not None and not isinstance(self.creation_date, XSDDateTime):
            self.creation_date = XSDDateTime(self.creation_date)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.source_schema_path is not None and not isinstance(self.source_schema_path, FileSystemPath):
            self.source_schema_path = FileSystemPath(self.source_schema_path)

        if not isinstance(self.data_files, list):
            self.data_files = [self.data_files] if self.data_files is not None else []
        self.data_files = [v if isinstance(v, FileSystemPath) else FileSystemPath(v) for v in self.data_files]

        self._normalize_inlined_as_dict(
            slot_name="source_google_sheet_docs",
            slot_type=GoogleSheetsDoc,
            key_name="id",
            keyed=True,
        )

        if self.project_directory is not None and not isinstance(self.project_directory, FileSystemPath):
            self.project_directory = FileSystemPath(self.project_directory)

        if self.external_project_path is not None and not isinstance(self.external_project_path, FileSystemPath):
            self.external_project_path = FileSystemPath(self.external_project_path)

        if self.last_saved is not None and not isinstance(self.last_saved, XSDDateTime):
            self.last_saved = XSDDateTime(self.last_saved)

        super().__post_init__(**kwargs)


@dataclass
class GoogleSheetsDoc(YAMLRoot):
    """
    A google sheets document can contain multiple individual sheets
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = WORKSPACE.GoogleSheetsDoc
    class_class_curie: ClassVar[str] = "workspace:GoogleSheetsDoc"
    class_name: ClassVar[str] = "GoogleSheetsDoc"
    class_model_uri: ClassVar[URIRef] = WORKSPACE.GoogleSheetsDoc

    id: Union[str, GoogleSheetsDocId] = None
    sheet_ids: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GoogleSheetsDocId):
            self.id = GoogleSheetsDocId(self.id)

        if not isinstance(self.sheet_ids, list):
            self.sheet_ids = [self.sheet_ids] if self.sheet_ids is not None else []
        self.sheet_ids = [v if isinstance(v, str) else str(v) for v in self.sheet_ids]

        super().__post_init__(**kwargs)


@dataclass
class GitHubAccount(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = WORKSPACE.GitHubAccount
    class_class_curie: ClassVar[str] = "workspace:GitHubAccount"
    class_name: ClassVar[str] = "GitHubAccount"
    class_model_uri: ClassVar[URIRef] = WORKSPACE.GitHubAccount

    username: Optional[str] = None
    password: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.username is not None and not isinstance(self.username, str):
            self.username = str(self.username)

        if self.password is not None and not isinstance(self.password, str):
            self.password = str(self.password)

        super().__post_init__(**kwargs)


@dataclass
class Workspace(YAMLRoot):
    """
    A workspace is a collection of projects managed locally on a file system
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = WORKSPACE.Workspace
    class_class_curie: ClassVar[str] = "workspace:Workspace"
    class_name: ClassVar[str] = "Workspace"
    class_model_uri: ClassVar[URIRef] = WORKSPACE.Workspace

    projects: Optional[
        Union[
            Dict[Union[str, ProjectName], Union[dict, Project]],
            List[Union[dict, Project]],
        ]
    ] = empty_dict()
    github_account: Optional[Union[dict, GitHubAccount]] = None
    projects_directory: Optional[Union[str, FileSystemPath]] = None
    autosync: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="projects", slot_type=Project, key_name="name", keyed=True)

        if self.github_account is not None and not isinstance(self.github_account, GitHubAccount):
            self.github_account = GitHubAccount(**as_dict(self.github_account))

        if self.projects_directory is not None and not isinstance(self.projects_directory, FileSystemPath):
            self.projects_directory = FileSystemPath(self.projects_directory)

        if self.autosync is not None and not isinstance(self.autosync, Bool):
            self.autosync = Bool(self.autosync)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass


slots.project__name = Slot(
    uri=WORKSPACE.name,
    name="project__name",
    curie=WORKSPACE.curie("name"),
    model_uri=WORKSPACE.project__name,
    domain=None,
    range=URIRef,
)

slots.project__uuid = Slot(
    uri=WORKSPACE.uuid,
    name="project__uuid",
    curie=WORKSPACE.curie("uuid"),
    model_uri=WORKSPACE.project__uuid,
    domain=None,
    range=Optional[str],
)

slots.project__github_organization = Slot(
    uri=WORKSPACE.github_organization,
    name="project__github_organization",
    curie=WORKSPACE.curie("github_organization"),
    model_uri=WORKSPACE.project__github_organization,
    domain=None,
    range=Optional[Union[dict, GitHubAccount]],
)

slots.project__creation_date = Slot(
    uri=WORKSPACE.creation_date,
    name="project__creation_date",
    curie=WORKSPACE.curie("creation_date"),
    model_uri=WORKSPACE.project__creation_date,
    domain=None,
    range=Optional[Union[str, XSDDateTime]],
)

slots.project__schema = Slot(
    uri=WORKSPACE.schema,
    name="project__schema",
    curie=WORKSPACE.curie("schema"),
    model_uri=WORKSPACE.project__schema,
    domain=None,
    range=Optional[Union[dict, Any]],
)

slots.project__description = Slot(
    uri=WORKSPACE.description,
    name="project__description",
    curie=WORKSPACE.curie("description"),
    model_uri=WORKSPACE.project__description,
    domain=None,
    range=Optional[str],
)

slots.project__source_schema_path = Slot(
    uri=WORKSPACE.source_schema_path,
    name="project__source_schema_path",
    curie=WORKSPACE.curie("source_schema_path"),
    model_uri=WORKSPACE.project__source_schema_path,
    domain=None,
    range=Optional[Union[str, FileSystemPath]],
)

slots.project__data_files = Slot(
    uri=WORKSPACE.data_files,
    name="project__data_files",
    curie=WORKSPACE.curie("data_files"),
    model_uri=WORKSPACE.project__data_files,
    domain=None,
    range=Optional[Union[Union[str, FileSystemPath], List[Union[str, FileSystemPath]]]],
)

slots.project__source_google_sheet_docs = Slot(
    uri=WORKSPACE.source_google_sheet_docs,
    name="project__source_google_sheet_docs",
    curie=WORKSPACE.curie("source_google_sheet_docs"),
    model_uri=WORKSPACE.project__source_google_sheet_docs,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, GoogleSheetsDocId], Union[dict, GoogleSheetsDoc]],
            List[Union[dict, GoogleSheetsDoc]],
        ]
    ],
)

slots.project__project_directory = Slot(
    uri=WORKSPACE.project_directory,
    name="project__project_directory",
    curie=WORKSPACE.curie("project_directory"),
    model_uri=WORKSPACE.project__project_directory,
    domain=None,
    range=Optional[Union[str, FileSystemPath]],
)

slots.project__external_project_path = Slot(
    uri=WORKSPACE.external_project_path,
    name="project__external_project_path",
    curie=WORKSPACE.curie("external_project_path"),
    model_uri=WORKSPACE.project__external_project_path,
    domain=None,
    range=Optional[Union[str, FileSystemPath]],
)

slots.project__last_saved = Slot(
    uri=WORKSPACE.last_saved,
    name="project__last_saved",
    curie=WORKSPACE.curie("last_saved"),
    model_uri=WORKSPACE.project__last_saved,
    domain=None,
    range=Optional[Union[str, XSDDateTime]],
)

slots.googleSheetsDoc__id = Slot(
    uri=WORKSPACE.id,
    name="googleSheetsDoc__id",
    curie=WORKSPACE.curie("id"),
    model_uri=WORKSPACE.googleSheetsDoc__id,
    domain=None,
    range=URIRef,
)

slots.googleSheetsDoc__sheet_ids = Slot(
    uri=WORKSPACE.sheet_ids,
    name="googleSheetsDoc__sheet_ids",
    curie=WORKSPACE.curie("sheet_ids"),
    model_uri=WORKSPACE.googleSheetsDoc__sheet_ids,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.gitHubAccount__username = Slot(
    uri=WORKSPACE.username,
    name="gitHubAccount__username",
    curie=WORKSPACE.curie("username"),
    model_uri=WORKSPACE.gitHubAccount__username,
    domain=None,
    range=Optional[str],
)

slots.gitHubAccount__password = Slot(
    uri=WORKSPACE.password,
    name="gitHubAccount__password",
    curie=WORKSPACE.curie("password"),
    model_uri=WORKSPACE.gitHubAccount__password,
    domain=None,
    range=Optional[str],
)

slots.workspace__projects = Slot(
    uri=WORKSPACE.projects,
    name="workspace__projects",
    curie=WORKSPACE.curie("projects"),
    model_uri=WORKSPACE.workspace__projects,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, ProjectName], Union[dict, Project]],
            List[Union[dict, Project]],
        ]
    ],
)

slots.workspace__github_account = Slot(
    uri=WORKSPACE.github_account,
    name="workspace__github_account",
    curie=WORKSPACE.curie("github_account"),
    model_uri=WORKSPACE.workspace__github_account,
    domain=None,
    range=Optional[Union[dict, GitHubAccount]],
)

slots.workspace__projects_directory = Slot(
    uri=WORKSPACE.projects_directory,
    name="workspace__projects_directory",
    curie=WORKSPACE.curie("projects_directory"),
    model_uri=WORKSPACE.workspace__projects_directory,
    domain=None,
    range=Optional[Union[str, FileSystemPath]],
)

slots.workspace__autosync = Slot(
    uri=WORKSPACE.autosync,
    name="workspace__autosync",
    curie=WORKSPACE.curie("autosync"),
    model_uri=WORKSPACE.workspace__autosync,
    domain=None,
    range=Optional[Union[bool, Bool]],
)
