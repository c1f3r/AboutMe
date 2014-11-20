from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.


class AboutUser(models.Model):
    '''
        model in which data about me is stored
    '''
    username = models.CharField(u'Username', max_length=20)
    first_name = models.CharField(u'First Name', max_length=50, blank=True)
    last_name = models.CharField(u'Last Name', max_length=50, blank=True)
    birth_date = models.DateField(u'Birth Date', blank=True, null=True)
    bio = models.TextField(u'Bio', blank=True)
    email = models.EmailField(u'Email', blank=True)
    jabber = models.CharField(u'Jabber', max_length=50, blank=True)
    skype = models.CharField(u'Skype', max_length=50, blank=True)
    other_contacts = models.TextField(u'Other Contacts', blank=True)
    avatar = models.ImageField(u'Avatar', upload_to='img', blank=True, null=True)

    def __unicode__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse(u'index')


class HttpRequestLog(models.Model):
    '''
        model which stores HttpRequest info
    '''
    host = models.CharField(u'Host', max_length=100)
    path = models.CharField(u'Full Path', max_length=255)
    date_time = models.DateTimeField(u'Date/Time of Request', auto_now_add=True)
    method = models.CharField(u'Method', max_length=4)  # len('POST') == 4
    user = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return u"{0}{1} at {2}".format(self.host, self.path, self.date_time)