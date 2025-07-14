import pytest

from linkml_runtime.utils.metamodelcore import URI


def test_issue_1355_invalid_url_message() -> None:
    """Check that quotes are used when referencing invalid urls to improve troubleshooting UX.

    See https://github.com/linkml/linkml/issues/1355, improve invalid URL message
    """
    #  note the trailing blank
    url = "https://ceur-ws.org/Vol-2931/ICBO_2019_paper_20.pdf "
    with pytest.raises(ValueError, match="'https://ceur-ws.org/Vol-2931/ICBO_2019_paper_20.pdf ': is not a valid URI"):
        URI(url)
