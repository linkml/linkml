'''
Created on 2023-03-24

@author: wf
'''
from unittest import TestCase
from linkml_runtime.utils.metamodelcore import URI

class Issue1355TestCase(TestCase):
    """
    https://github.com/linkml/linkml/issues/1355
    improve invalid URL message
    """
    
    def test_issue_1355_invalid_url_message(self):
        """
        check that quotes are used when referencing invalid urls so that
        the visiblity of the problem gets better
        """
        #  note the trailing blank 
        url="https://ceur-ws.org/Vol-2931/ICBO_2019_paper_20.pdf "
        try:
            _uri=URI(url)
        except ValueError as vex:
            msg=str(vex)
            # 'https://ceur-ws.org/Vol-2931/ICBO_2019_paper_20.pdf ': is not a valid URI
            self.assertTrue(".pdf '" in msg)
    
