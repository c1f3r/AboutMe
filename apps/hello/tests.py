from django.core.urlresolvers import reverse
from django.test import TestCase

# Create your tests here.


class IndexTest(TestCase):
    fixtures = [u'initial_data.json']

    def test_index_page_exists(self):
        response = self.client.get(reverse(u'index'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_contains_first_name(self):
        response = self.client.get(reverse(u'index'))
        self.assertContains(response, u'Artem')


class TestHttpRequests(TestCase):
    def test_requests_page_exists(self):
        response = self.client.get(reverse(u'requests'))
        self.assertEqual(response.status_code, 200)

    def test_Requests_page_contains_header(self):
        response = self.client.get(reverse(u'requests'))
        self.assertContains(response, u'h1')