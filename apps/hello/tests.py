from django.test import TestCase, Client

# Create your tests here.


class IndexTest(TestCase):
    def test_index_page(self):
        client = Client()
        response = client.get(u'/')
        self.assertEqual(response.status_code, 200)
