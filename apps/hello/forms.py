from django import forms

from models import AboutUser
from widgets import DatePickerWidget
# from ajax_upload.widgets import AjaxClearableFileInput


class EditInfoForm(forms.ModelForm):
    class Meta:
        model = AboutUser
        exclude = ['username']

    birth_date = forms.DateField(widget=DatePickerWidget(params="dateFormat: 'yy-mm-dd', changeYear: true, "
                                                                "changeMonth: true, defaultDate: '-28y', "
                                                                "yearRange: 'c-80:c+28'",
                                                         attrs={'class': 'datepicker',
                                                                'autocomplete': 'off'}))
