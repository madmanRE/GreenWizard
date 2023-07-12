from django import forms
from .models import *


class SearchForm(forms.Form):
    query = forms.CharField()