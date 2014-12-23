from django import forms

from models import AboutUser
from widgets import DatePickerWidget
from django.utils.translation import ugettext_lazy as _


class EditInfoForm(forms.ModelForm):
    class Meta:
        model = AboutUser
        exclude = ['username']

    birth_date = forms.DateField(
        label=_(u"Birth date"),
        widget=DatePickerWidget(params="dateFormat: 'yy-mm-dd', "
                                       "changeYear: true, "
                                       "changeMonth: true, "
                                       "defaultDate: '-28y', "
                                       "yearRange: 'c-80:c+28'",
                                attrs={
                                    'class': 'datepicker',
                                    'autocomplete': 'off'
                                }
                                )
    )
