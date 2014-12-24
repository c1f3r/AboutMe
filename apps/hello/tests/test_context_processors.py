from django.core.urlresolvers import reverse
from django.test import TestCase


class TestSettingsContextProcessor(TestCase):
    """
    Class for testing own "settings" context processor
    """

    def test_settings_context_processor(self):
        """
        Tests if context processor exists in index and HttpRequests pages
        """
        response = self.client.get(reverse(u'index'))
        self.assertTrue(response.context[u'settings'])
        response = self.client.get(reverse(u'requests'))
        self.assertTrue(response.context[u'settings'])
