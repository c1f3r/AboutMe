from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class AboutUser(models.Model):
    '''
        model in which data about me is stored
    '''
    username = models.CharField(u'Username', max_length=20, blank=False)
    first_name = models.CharField(u'First Name', max_length=50, blank=False)
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

class Event(models.Model):
    time = models.DateTimeField('Date/Time', auto_now=True)
    action = models.CharField('Action', max_length=20)
    model = models.CharField('Model', max_length=50)

    class Meta:
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