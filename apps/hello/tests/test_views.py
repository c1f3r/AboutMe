import json
from unittest import skip
from django.core.urlresolvers import reverse
from django.test import TestCase
from apps.hello.forms import EditInfoForm
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

    def test_index_page_contains_login_link_when_not_logged_in(self):
        response = self.client.get(reverse(u"index"))
        self.assertContains(response, 'id="login_link"')
        self.assertNotContains(response, 'id="logout_link"')
        self.assertNotContains(response, 'id="edit_info_link"')
        self.assertNotContains(response, 'id="admin_edit_link"')

    def test_index_page_contains_logout_link_when_logged_in(self):
        self.client.login(username=u'admin', password=u'admin')
        response = self.client.get(reverse(u"index"))
        self.assertNotContains(response, 'id="login_link"')
        self.assertContains(response, 'id="logout_link"')
        self.assertContains(response, 'id="edit_info_link"')
        self.assertContains(response, 'id="admin_edit_link"')

    def test_index_page_displays_edit_link_template_tag(self):
        self.client.login(username=u'admin', password=u'admin')
        response = self.client.get(reverse(u"index"))
        self.assertContains(response, u'/admin/hello/aboutuser/1/">(admin)')

    def test_index_page_contains_link_to_http_requests_page(self):
        response = self.client.get(reverse(u'index'))
        self.assertContains(response, u'id="requests_link')


class TestEditInfoPage(TestCase):

    def get_response(self):
        self.client.login(username=u'admin', password=u'admin')
        return self.client.get(reverse(u'edit_info'))

    def test_edit_info_page_redirects_to_login_page_if_user_not_authed(self):
        response = self.client.get(reverse(u"edit_info"))
        self.assertEqual(response.status_code, 302)
        expected_redirect = "accounts/login/?next=" + reverse(u'edit_info')
        self.assertRedirects(response, expected_redirect, 302, 302)

    def test_edit_info_page_uses_edit_info_template(self):
        self.assertTemplateUsed(self.get_response(), u'hello/edit_info.html')

    def test_edit_info_page_uses_edit_info_form(self):
        self.assertIsInstance(
            self.get_response().context['form'], EditInfoForm)

    def test_edit_info_page_redirects_to_itself_on_success(self):
        self.client.login(username=u'admin', password=u'admin')
        response = self.client.post(reverse(u'edit_info'), {'first_name': 'a'})
        self.assertRedirects(response, reverse(u'edit_info'))

    def test_edit_info_page_gives_errors_on_incorrect_input(self):
        self.client.login(username=u'admin', password=u'admin')
        # Check empty first_name validation
        response = self.client.post(reverse(u'edit_info'), {'first_name': ''})
        self.assertContains(response, "errorlist")
        # Check wrong date format validation
        response = self.client.post(reverse(u'edit_info'),
                                    {'first_name': 'a',
                                     'birth_date': '23.08.86'})
        self.assertContains(response, "errorlist")
        # Check wrong email format validation
        response = self.client.post(reverse(u'edit_info'),
                                    {'first_name': 'a',
                                     'email': 'email_without_at'})
        self.assertContains(response, "errorlist")

    def test_ajax_form_returns_OK_if_form_is_valid(self):
        self.client.login(username=u'admin', password=u'admin')
        response = self.client.post(reverse(u'edit_info'),
                                    {u'first_name': u'Petryk',
                                     u'birth_date': '2000-01-01',
                                     u'email': u'petryk@example.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_ajax_form_returns_400_and_shows_errors_if_form_is_invalid(self):
        self.client.login(username=u'admin', password=u'admin')
        response = self.client.post(reverse(u'edit_info'),
                                    {u'first_name': '',
                                     u'birth_date': '23.08.86',
                                     u'email': u'email_without_at'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 400)
        self.assertIn(u'first_name', response.content)
        self.assertIn(u'birth_date', response.content)
        self.assertIn(u'email', response.content)
