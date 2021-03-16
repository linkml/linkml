import json
from urllib.parse import urlparse, urljoin

from pyld.jsonld import requests_document_loader, JsonLdError


def pyld_document_loader(**kwargs):
    """
    Create a Requests or a file based document loader.

    Can be used to setup extra Requests args such as verify, cert, timeout,
    or others.

    :param kwargs: extra keyword args for Requests get() call.

    :return: the RemoteDocument loader function.
    """

    def loader(url, prev_url, options=None):
        """
        Retrieves JSON-LD from a URL, a file location or as text

        :param url: the URL to retrieve.
        :param prev_url: Dictionary to carry the previous URL referenced
        :param options: Additional options

        :return: the RemoteDocument.
        """
        if options is None:
            options = {}

        # Process text being passed in as the document
        if url.strip()[0] in '[{' or '\n' in url:
            return {
                'contentType': 'text/plain',
                'contextUrl': None,
                'documentUrl': None,
                'document': json.loads(url)
            }

        # process relative URL
        pieces = urlparse(url)
        if not any([pieces.scheme, pieces.netloc]):
            if prev_url['url']:
                url = urljoin(prev_url['url'], url)
                pieces = urlparse(url)
        else:
            prev_url['url'] = url

        # check for file access
        if pieces.scheme == 'file':
            try:
                with open(pieces.path) as f:
                    doc = f.read()
                return {
                    'contentType': 'text/plain',
                    'contextUrl': None,
                    'documentUrl': url,
                    'document': json.loads(doc)
                }
            except Exception as cause:
                raise JsonLdError(
                    f'Could not retrieve a JSON-LD document from {url}.',
                    'jsonld.LoadDocumentError', code='loading document failed',
                    cause=cause)
        else:
            return requests_document_loader(**kwargs)(url, options)

    prev_url_holder = {}
    return lambda url, options: loader(url, prev_url_holder, options)
