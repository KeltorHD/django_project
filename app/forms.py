from django import forms
from .models import State, People
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

class DateInput(forms.DateInput):
    input_type='date'


class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ('date', 'people')
        labels = {
        	'people':_('Ученики'),
            'date':_('Дата')
        }
        widgets = {
            'date': DateInput()
        }
