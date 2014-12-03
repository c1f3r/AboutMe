from StringIO import StringIO
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase
import sys

from models import HttpRequestLog, AboutUser, Event


class IndexTest(TestCase):
    """
    Class for testing if index page and own template tag works well
    """
    fixtures = [u'initial_data.json']

    def test_index_page_exists(self):
        """
        Tests if index page exists
        """
        response = self.client.get(reverse(u'index'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_contains_first_name(self):
        """
        Tests if index page contains first name
        """
        response = self.client.get(reverse(u'index'))
        self.assertContains(response, u'Artem')

    def test_index_shows_correct_user(self):
        """
        Tests if index page shows my bio if there are more than one AboutUser instance
        """
        AboutUser.objects.create(username=u'petryk', first_name=u'Petryk', last_name=u'Pyato4kin',
                                 birth_date='2000-01-01',
                                 bio='I was born with the wrong sign in the wrong house\nWith the wrong ascendancy',
                                 email='p.pyato4kin@example.com', jabber='p.pyato4kin@42cc.co', skype='p.pyato4kin',
                                 other_contacts='')
        response = self.client.get(reverse('index'))
        self.assertContains(response, u'Artem')
        self.assertNotContains(response, u'Petryk')

    def test_edit_link_tag(self):
        """
        Tests if link to admin page for edition info works (own template tag edit_link works correct)
        """
        self.client.login(username=u'admin', password=u'admin')
        response = self.client.get(reverse(u'index'))
        self.assertContains(response, '/admin/hello/aboutuser/1/">(admin)</a>')


class TestHttpRequests(TestCase):
    """
    Class for testing if Latest 10 HttpRequests page and own middleware works well
    """
    def test_requests_page_exists(self):
        """
        Tests if page containing 10 latest requests exists
        """
        response = self.client.get(reverse(u'requests'))
        self.assertEqual(response.status_code, 200)

    def test_requests_middleware_works(self):
        """
        Tests if middleware adds instance of HttpRequest when request was made
        """
        http_requests = HttpRequestLog.objects.all()
        self.assertFalse(http_requests)
        self.client.get(reverse(u'index'))
        http_requests = HttpRequestLog.objects.all()
        self.assertEqual(http_requests.count(), 1)

    def test_only_ten_first_requests_are_displayed(self):
        """
        Tests if only 10 first are displayed. Rewritten when added django-tables2 due to last (13) ticket
        """
        for i in range(10):
            self.client.get(reverse(u'index'))
            self.client.get(reverse(u'admin:index'))
        requests = HttpRequestLog.objects.all()
        response = self.client.get(reverse(u'requests'))
        self.assertEqual(requests.count(), 21)
        self.assertContains(response, '<tr', 11)  # checks if 10 requests displayed
        latest_ten_requests = HttpRequestLog.objects.order_by(u'date_time')[:10]
        for i in xrange(10):
            self.assertContains(response, latest_ten_requests[i].id)
            self.assertContains(response, latest_ten_requests[i].path)
            self.assertContains(response, latest_ten_requests[i].host)


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


class TestEditInfoPage(TestCase):
    """
    Class for testing page for editing info
    """
    def test_only_authorized_access(self):
        """
        Tests if only authorized user is allowed to edit info AboutUser
        """
        response = self.client.get(reverse(u'edit_info'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username=u'admin', password=u'admin')
        response = self.client.get(reverse(u'edit_info'))
        self.assertEqual(response.status_code, 200)

    def test_only_correct_info_allowed(self):
        """
        Tests if edition page allows only correct info
        """
        self.client.login(username=u'admin', password=u'admin')
        response = self.client.post(reverse(u'edit_info'), {'birth_date': 'today'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['birth_date'].errors, [u'Enter a valid date.'])


class TestManagementCommand(TestCase):
    """
    Class for testing own "list_models" management command
    """
    fixtures = [u'initial_data.json']

    def test_list_models_command(self):
        """
        Tests if correct info about models is displayed in both stdout and stderror
        """
        err = out = StringIO()
        sys.stdout = out
        sys.stderr = err
        call_command(u"list_models")
        # call_command(u"list_models", stdout=out, stderr=err)  # this didnt work, wonder why
        self.assertIn("Model AboutUser has 1 object", out.getvalue())
        self.assertIn("Model AboutUser has 1 object", out.getvalue())
        self.assertIn("Model HttpRequestLog has 0 objects", out.getvalue())
        self.assertIn("error: Model AboutUser has 1 object", err.getvalue())
        self.assertIn("error: Model HttpRequestLog has 0 objects", err.getvalue())
        self.client.get(reverse(u'index'))
        call_command(u"list_models")
        self.assertIn("Model AboutUser has 1 object", out.getvalue())
        self.assertIn("Model HttpRequestLog has 1 object", out.getvalue())
        self.assertIn("error: Model AboutUser has 1 object", err.getvalue())
        self.assertIn("error: Model HttpRequestLog has 1 object", err.getvalue())


class EventTest(TestCase):
    """
    Class for testing how signal works
    """
    fixtures = ['initial_data.json']

    def test_create_signal(self):
        """
        Tests if signal for creation of AboutUser instance works
        """
        Event.objects.all().delete()
        about_me = AboutUser.objects.get(username=u"cifer")
        self.assertEqual(about_me.first_name, u'Artem')
        self.assertEqual(Event.objects.all().count(), 0)
        AboutUser.objects.create(username=u'petryk', first_name=u'Petryk', last_name=u'Pyato4kin',
                                 birth_date='2000-01-01',
                                 bio='I was born with the wrong sign in the wrong house\nWith the wrong ascendancy',
                                 email='p.pyato4kin@example.com', jabber='p.pyato4kin@42cc.co', skype='p.pyato4kin',
                                 other_contacts='')
        self.assertEqual(AboutUser.objects.all().count(), 2)
        self.assertEqual(Event.objects.get(pk=1).action, 'create')

    def test_update_signal(self):
        """
        Tests if signal for update of AboutUser instance works
        """
        Event.objects.all().delete()
        about_me = AboutUser.objects.get(pk=1)
        about_me.username = u'root'
        about_me.save()
        self.assertEqual(about_me.username, u'root')
        self.assertEqual(Event.objects.get(pk=1).action, 'update')

    def test_delete_signal(self):
        """
        Tests if signal for deleting of AboutUser instance works
        """
        Event.objects.all().delete()
        AboutUser.objects.all().delete()
        self.assertEqual(Event.objects.get(pk=1).action, 'delete')


class TestPriority(TestCase):
    """
    Class for testing priority of HttpRequests
    """
    def test_priority(self):
        """
        Tests if modifying and displaying of HttpRequest with "priority" field works
        """
        self.client.get(reverse(u'index'))
        self.assertEqual(HttpRequestLog.objects.all().count(), 1)
        response = self.client.get(reverse(u'requests'))
        self.assertContains(response, 'Priority')
        http_request = HttpRequestLog.objects.get(pk=1)
        http_request.priority = 3
        http_request.save()
        self.client.get(reverse(u'requests'))
        self.assertEqual(HttpRequestLog.objects.get(pk=1).priority, 3)
        self.assertEqual(HttpRequestLog.objects.get(pk=2).priority, 1)