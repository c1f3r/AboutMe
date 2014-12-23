from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import TestCase
from apps.hello.models import AboutUser, HttpRequestLog, Event


class TestAboutUser(TestCase):

    fixtures = [u'initial_data.json']


    def test_about_user_string_representation(self):
        new_user = AboutUser.objects.create(username="petryk",
                                            first_name="Petryk",
                                            last_name="Pyatochkin"
                                            )
        self.assertEqual(u"Petryk Pyatochkin", unicode(new_user))

    def test_about_user_username_is_unique(self):
        with self.assertRaises(ValidationError):
            new_user = AboutUser(username="cifer", first_name="Petryk")
            new_user.full_clean()


class TestHttpRequestLog(TestCase):

    def test_http_request_log_string_representation(self):
        self.client.get(reverse(u'admin:index'))
        self.assertRegexpMatches(
            unicode(HttpRequestLog.objects.first()),
            r'testserver.+admin')

    def test_http_request_log_default_priority_equals_1(self):
        self.client.get(reverse(u'admin:index'))
        self.assertEqual(1, HttpRequestLog.objects.first().priority)

    def test_http_request_log_priority_can_be_changed(self):
        self.client.get(reverse(u'admin:index'))
        http_req_log = HttpRequestLog.objects.first()
        http_req_log.priority = 4
        http_req_log.save()
        self.assertEqual(4, HttpRequestLog.objects.first().priority)


class TestEvent(TestCase):

    fixtures = [u'initial_data.json']

    def test_event_string_representation(self):
        self.client.get(reverse(u"admin:index"))
        self.assertEqual(unicode(Event.objects.first()),
                         HttpRequestLog.__name__)

    def test_event_signals_follow_about_user_creating(self):
        events_count = Event.objects.count()
        AboutUser.objects.create(username=u"petryk", first_name=u"Petryk")
        self.assertEqual(Event.objects.count(), events_count + 1)
        self.assertEqual(Event.objects.first().action, u'create')

    def test_event_signals_follow_about_user_updating(self):
        events_count = Event.objects.count()
        new_user = AboutUser.objects.get(username=u"cifer")
        new_user.first_name = u"Petryk"
        new_user.save()
        self.assertEqual(Event.objects.count(), events_count + 1)
        self.assertEqual(Event.objects.first().action, u'update')

    def test_event_signals_follow_about_user_deleting(self):
        events_count = Event.objects.count()
        AboutUser.objects.get(username=u"cifer").delete()
        self.assertEqual(Event.objects.count(), events_count + 1)
        self.assertEqual(Event.objects.first().action, u'delete')
        
    def test_event_signals_follow_http_request_log_creating(self):
        events_count = Event.objects.count()
        self.client.get(reverse(u"admin:index"))
        self.assertEqual(Event.objects.count(), events_count + 1)
        self.assertEqual(Event.objects.first().action, u'create')

    def test_event_signals_follow_http_request_log_updating(self):
        events_count = Event.objects.count()
        self.client.get(reverse(u"admin:index"))
        http_req_log = HttpRequestLog.objects.first()
        http_req_log.priority = 4
        http_req_log.save()
        self.assertEqual(Event.objects.count(), events_count + 2)
        self.assertEqual(Event.objects.first().action, u'update')

    def test_event_signals_follow_http_request_log_deleting(self):
        events_count = Event.objects.count()
        self.client.get(reverse(u"admin:index"))
        HttpRequestLog.objects.first().delete()
        self.assertEqual(Event.objects.count(), events_count + 2)
        self.assertEqual(Event.objects.first().action, u'delete')

    def test_event_signals_do_not_follow_events_instances_creating(self):
        events_count = Event.objects.count()
        Event.objects.create()
        self.assertEqual(Event.objects.count(), events_count + 1)

    def test_event_signals_do_not_follow_events_instances_updating(self):
        self.client.get(reverse(u"admin:index"))
        events_count = Event.objects.count()
        event = Event.objects.first()
        event.action = u'update'
        event.save()
        self.assertEqual(Event.objects.count(), events_count)

    def test_event_signals_do_not_follow_events_instances_deleting(self):
        self.client.get(reverse(u"admin:index"))
        Event.objects.all().delete()
        self.assertEqual(Event.objects.count(), 0)
