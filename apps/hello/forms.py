from django.forms import ModelForm

from apps.hello.models import AboutUser


class EditInfoForm(ModelForm):
    class Meta:
        model = AboutUser
        exclude = ['username']