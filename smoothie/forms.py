from django import forms
import requests
from smoothie.models import Smoothie


class SearchForm(forms.Form):
    query = forms.CharField()

    def submit(self):
        query = self.cleaned_data['query']
        url = 'https://api.nal.usda.gov/fdc/v1/foods/search'
        params = {
            'api_key': 'elhyRfYJ42dSR6zWHJXgOeU9zudQ7wfawa1hYFP8',
            'query': query,
            'pageSize': 10,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()['foods']


class SmoothieForm(forms.ModelForm):
    class Meta:
        model = Smoothie
        fields = ['name']
