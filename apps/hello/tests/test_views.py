from django.core.urlresolvers import reverse
from django.test import TestCase
from apps.hello.models import AboutUser


class TestIndexPage(TestCase):

    fixtures = [u'initial_data.json']

    def test_index_page_renders_index_template(self):
        response = self.client.get(reverse(u"index"))
        self.assertTemplateUsed(response, u'hello/index.html')

    def test_index_page_displays_info_about_me(self):
        about_me = AboutUser.objects.get(username=u"cifer")
        response = self.client.get(reverse(u"index"))
        self.assertContains(response, about_me.first_name)

    def test_index_page_does_not_display_info_about_others(self):
        new_user = AboutUser.objects.create(username="petryk",
                                            first_name="Petryk")
        response = self.client.get(reverse(u"index"))
        self.assertNotContains(response, new_user.first_name)
