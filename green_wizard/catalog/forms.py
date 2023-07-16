from django import forms
from .models import *


class SearchForm(forms.Form):
    query = forms.CharField()


class FilterForm(forms.Form):
    min_price = forms.IntegerField(min_value=0, max_value=999999, required=False)
    max_price = forms.IntegerField(min_value=0, max_value=999999, required=False)
    age_limit = forms.IntegerField(min_value=0, max_value=99, required=False)
    amount_people = forms.ChoiceField(choices=[('1-2', '1-2'), ('2-4', '2-4'), ('1-5', '1-5'), ('3-6', '3-6')],
                                      required=False)
