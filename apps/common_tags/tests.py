from django.test import TestCase
from django.utils import translation
from templatetags.strip_lang import strip_lang


class TestFilter(TestCase):
    def test_filter_strips_language_from_path(self):
        language = translation.get_language()
        self.assertEqual(
            u"/some-page", strip_lang(u"/{0}/some-page".format(language)))
        self.assertEqual(u"/some-page", strip_lang(u"/some-page"))
