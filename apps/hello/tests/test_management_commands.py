import sys
from StringIO import StringIO

from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase


class TestManagementCommand(TestCase):
    """
    Class for testing own "list_models" management command
    """
    fixtures = [u'initial_data.json']

    def test_list_models_command(self):
        """
        Tests if correct info about models is displayed
        in both stdout and stderror
        """
        err = out = StringIO()
        (sys_out, sys_err) = (sys.stdout, sys.stderr)
        (sys.stdout, sys.stderr) = (out, err)
        call_command(u"list_models")
        self.assertIn("Model AboutUser has 1 object", out.getvalue())
        self.assertIn("Model HttpRequestLog has 0 objects", out.getvalue())
        self.assertIn("error: Model AboutUser has 1 object", err.getvalue())
        self.assertIn("error: Model HttpRequestLog has 0 objects",
                      err.getvalue())
        self.client.get(reverse(u'index'))
        call_command(u"list_models")
        self.assertIn("Model AboutUser has 1 object", out.getvalue())
        self.assertIn("Model HttpRequestLog has 1 object", out.getvalue())
        self.assertIn("error: Model AboutUser has 1 object", err.getvalue())
        self.assertIn("error: Model HttpRequestLog has 1 object",
                      err.getvalue())
        (sys.stdout, sys.stderr) = (sys_out, sys_err)
