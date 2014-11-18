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

    def __unicode__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('index')