from django import forms
from . import models

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.

class SimpleForm(forms.Form):
    entered_text = forms.CharField(max_length=100)