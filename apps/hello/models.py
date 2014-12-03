from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext, ugettext_lazy as _


class AboutUser(models.Model):
    '''
    model in which data about me is stored
    '''
    username = models.CharField(_(u'Username'), max_length=20, blank=False)
    first_name = models.CharField(_(u'First Name'), max_length=50, blank=False)
    last_name = models.CharField(_(u'Last Name'), max_length=50, blank=True)
    birth_date = models.DateField(_(u'Birth Date'), blank=True, null=True)
    bio = models.TextField(_(u'Bio'), blank=True)
    email = models.EmailField(_(u'Email'), blank=True)
    jabber = models.CharField(_(u'Jabber'), max_length=50, blank=True)
    skype = models.CharField(_(u'Skype'), max_length=50, blank=True)
    other_contacts = models.TextField(_(u'Other Contacts'), blank=True)
    avatar = models.ImageField(_(u'Avatar'), upload_to='img', blank=True, null=True)

    def __unicode__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = _(u'About User')

    def meta(self):
        return self._meta


class HttpRequestLog(models.Model):
    '''
        model which stores HttpRequest info
    '''
    PRIORITY_CHOICES = [(i, i) for i in xrange(1, 6)]
    host = models.CharField(_(u'Host'), max_length=100)
    path = models.CharField(_(u'Full Path'), max_length=255)
    date_time = models.DateTimeField(_(u'Date/Time of Request'), auto_now_add=True)
    method = models.CharField(_(u'Method'), max_length=4)  # len('POST') == 4
    user = models.ForeignKey(User, blank=True, null=True)
    priority = models.IntegerField(_(u'Priority'), max_length=3, choices=PRIORITY_CHOICES, default=1)

    def __unicode__(self):
        return u"{0}{1} at {2}".format(self.host, self.path, self.date_time)

    class Meta:
        verbose_name = _(u'Http Request Log')


class Event(models.Model):
    time = models.DateTimeField(_(u'Date/Time'), auto_now=True)
    action = models.CharField(_(u'Action'), max_length=20)
    model = models.CharField(_(u'Model'), max_length=50)

    class Meta:
        verbose_name = _(u'Event')
        ordering = ['-time']

    def __unicode__(self):
        return self.model


@receiver(post_save)
def post_save_signal(sender, created, **kwargs):
    if created and sender.__name__ != 'Event':
        Event.objects.create(model=sender.__name__, action='create')
    elif not created and sender.__name__ != 'Event':
        Event.objects.create(model=sender.__name__, action='update')


@receiver(post_delete)
def post_delete_signal(sender, **kwargs):
    if sender.__name__ != 'Event':
        Event.objects.create(model=sender.__name__, action='delete')