from django.core.urlresolvers import reverse
from django.test import TestCase, Client

# Create your tests here.


class IndexTest(TestCase):
    fixtures = [u'initial_data.json']


    def setUp(self):
        self.client = Client()

    def test_index_page_exists(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_contains_first_name(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, u'Artem')