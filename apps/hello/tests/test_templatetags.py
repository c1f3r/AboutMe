# -*- coding:utf8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import translation

from apps.hello.models import HttpRequestLog
from apps.hello.templatetags import edit_link, verbose_names


class TestEditLinkTag(TestCase):
    def test_edit_link_tag_gives_correct_link_to_admin_site(self):
        self.client.get(reverse(u'index'))
        admin_link = edit_link.edit_link(HttpRequestLog.objects.first())
        self.assertIn(u'/admin/hello/httprequestlog/1/', admin_link)

    def test_verbose_names_tag_gives_correct_model_verbose_name(self):
        language = translation.get_language()
        self.client.get(reverse(u'index'))
        instance = HttpRequestLog.objects.first()
        verbose_name = verbose_names.get_verbose_field_name(instance, u'host')
        translation.activate(u'en')
        self.assertEqual(verbose_name, u'Host')
        translation.activate(u'uk')
        verbose_name = verbose_names.get_verbose_field_name(instance, u'host')
        self.assertEqual(verbose_name, u'Хост')
        translation.activate(language)