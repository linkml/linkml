import os

from rdflib import Namespace
from pathlib import Path

HTTP_TEST_PORT = 8000
HTTPS_TEST_PORT = 8443

TESTING_DIR = os.path.abspath(os.path.dirname(__file__))
INPUT_DIR = os.path.join(TESTING_DIR, 'input')
OUTPUT_DIR = os.path.join(TESTING_DIR, 'output')

LD_10_DIR = os.path.join(TESTING_DIR, 'jsonld_context/jsonld_10/')
LD_11_DIR = os.path.join(TESTING_DIR, 'jsonld_context/jsonld_11/')


GITHUB_DIR = 'https://raw.githubusercontent.com/HOT-Ecosystem/TermCI-model/main/'
GITHUB_INPUT_DIR = GITHUB_DIR + Path(os.path.relpath(INPUT_DIR, os.path.dirname(TESTING_DIR))).as_posix()
GITHUB_LD10_CONTEXT = GITHUB_DIR + Path(os.path.relpath(LD_10_DIR, os.path.dirname(TESTING_DIR))).as_posix() + '/'
GITHUB_LD11_CONTEXT = GITHUB_DIR + Path(os.path.relpath(LD_11_DIR, os.path.dirname(TESTING_DIR))).as_posix() + '/'

SCT = Namespace("http://snomed.info/id/")
OBO = Namespace("http://purl.obolibrary.org/obo/")
NCIT = Namespace("http://purl.obolibrary.org/obo/ncit#")
TERMCI = Namespace("https://hotecosystem.org/termci/")
SHACL = Namespace("http://www.w3.org/ns/shacl#")

CONTEXT_SVR = f"http://localhost:{HTTP_TEST_PORT}/"
CONTEXT_SSL_SVR = f'https://localhost:{HTTPS_TEST_PORT}/'

LD_10_SVR = CONTEXT_SVR + 'jsonld_10/'
LD_11_SVR = CONTEXT_SVR + 'jsonld_11/'
LD_10_SSL_SVR = CONTEXT_SSL_SVR + 'jsonld_10/'
LD_11_SSL_SVR = CONTEXT_SSL_SVR + 'jsonld_11/'

