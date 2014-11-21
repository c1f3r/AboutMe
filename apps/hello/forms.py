from django import forms

from models import AboutUser
from widgets import DatePickerWidget


class EditInfoForm(forms.ModelForm):
    class Meta:
        model = AboutUser
        exclude = ['username']

    birth_date = forms.DateField(widget=DatePickerWidget(params="dateFormat: 'dd.mm.yy', "
                                                                "changeYear: true, defaultDate: '-37y', "
                                                                "yearRange: 'c-15:c+15'",
                                                         attrs={'class': 'datepicker'}))

