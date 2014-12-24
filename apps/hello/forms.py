from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.hello.models import AboutUser
from apps.hello.widgets import DatePickerWidget


class EditInfoForm(forms.ModelForm):
    class Meta:
        model = AboutUser
        exclude = ['username']
    birth_date = forms.DateField(
        label=_(u"Birth date"),
        widget=DatePickerWidget(params="dateFormat: 'yy-mm-dd', "
                                       "changeYear: true, "
                                       "changeMonth: true, "
                                       "defaultDate: '1986-08-23', "
                                       "yearRange: 'c-80:c+28'",
                                attrs={
                                    'class': 'datepicker',
                                    'autocomplete': 'off'
                                }
                                ),
        required=False
    )
