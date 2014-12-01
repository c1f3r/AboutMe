from django.core.urlresolvers import reverse
from django.test import TestCase

from models import HttpRequestLog, AboutUser, Event


class IndexTest(TestCase):
    fixtures = [u'initial_data.json']

    def test_index_page_exists(self):
        response = self.client.get(reverse(u'index'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_contains_first_name(self):
        response = self.client.get(reverse(u'index'))
        self.assertContains(response, u'Artem')

    def test_index_shows_correct_user(self):
        AboutUser.objects.create(username=u'petryk', first_name=u'Petryk', last_name=u'Pyato4kin',
                                 birth_date='2000-01-01',
                                 bio='I was born with the wrong sign in the wrong house\nWith the wrong ascendancy',
                                 email='p.pyato4kin@example.com', jabber='p.pyato4kin@42cc.co', skype='p.pyato4kin',
                                 other_contacts='')
        response = self.client.get(reverse('index'))
        self.assertContains(response, u'Artem')
        self.assertNotContains(response, u'Petryk')

    def test_edit_link_tag(self):
        self.client.login(username=u'admin', password=u'admin')
        response = self.client.get(reverse(u'index'))
        self.assertContains(response, '<a href="/admin/hello/aboutuser/1/">(admin)</a>')


class TestHttpRequests(TestCase):
    def test_requests_page_exists(self):
        response = self.client.get(reverse(u'requests'))
        self.assertEqual(response.status_code, 200)

    def test_requests_page_contains_header(self):
        response = self.client.get(reverse(u'requests'))
        self.assertContains(response, u'h1')

    def test_requests_middleware_works(self):
        http_requests = HttpRequestLog.objects.all()
        self.assertFalse(http_requests)
        self.client.get(reverse(u'index'))
        http_requests = HttpRequestLog.objects.all()
        self.assertEqual(http_requests.count(), 1)

    def test_only_ten_latest_requests_are_displayed(self):
        for i in range(10):
            self.client.get(reverse(u'index'))
            self.client.get(reverse(u'admin:index'))
        requests = HttpRequestLog.objects.all()
        response = self.client.get(reverse(u'requests'))
        self.assertEqual(requests.count(), 21)
        # self.assertEqual(response.context[u'requests'].count(), 10)
        self.assertContains(response, '<tr', 11)  # checks if 10 requests displayed
        latest_ten_requests = HttpRequestLog.objects.order_by(u'-date_time')[:10]
        for i in xrange(10):
            self.assertContains(response, latest_ten_requests[i].id)
            self.assertContains(response, latest_ten_requests[i].path)
            self.assertContains(response, latest_ten_requests[i].host)
            # self.assertEqual(latest_ten_requests[i].date_time, response.context[u'requests'][i].date_time)


class TestSettingsContextProcessor(TestCase):
    def test_settings_context_processor(self):
        response = self.client.get(reverse(u'index'))
        self.assertTrue(response.context[u'settings'])
        response = self.client.get(reverse(u'requests'))
        self.assertTrue(response.context[u'settings'])


class TestEditInfoPage(TestCase):
    def test_only_authorized_access(self):
        response = self.client.get(reverse(u'edit_info'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username=u'admin', password=u'admin')
        response = self.client.get(reverse(u'edit_info'))
        self.assertEqual(response.status_code, 200)

    def test_only_correct_info_allowed(self):
        self.client.login(username=u'admin', password=u'admin')
        response = self.client.post(reverse(u'edit_info'), {'birth_date': 'today'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['birth_date'].errors, [u'Enter a valid date.'])


class EventTest(TestCase):
    fixtures = ['initial_data.json']

    def test_create_signal(self):
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
        Event.objects.all().delete()
        about_me = AboutUser.objects.get(pk=1)
        about_me.username = u'root'
        about_me.save()
        self.assertEqual(about_me.username, u'root')
        self.assertEqual(Event.objects.get(pk=1).action, 'update')

    def test_delete_signal(self):
        Event.objects.all().delete()
        AboutUser.objects.all().delete()
        self.assertEqual(Event.objects.get(pk=1).action, 'delete')




class TestPriority(TestCase):

    def test_priority(self):
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