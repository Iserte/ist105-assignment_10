from django import forms

CONTINENT_CHOICES = [
    ("Africa", "Africa"),
    ("Americas", "Americas"),
    ("Asia", "Asia"),
    ("Europe", "Europe"),
    ("Oceania", "Oceania"),
]

class ContinentForm(forms.Form):
    continent = forms.ChoiceField(
        choices=CONTINENT_CHOICES,
        label="Choose a continent",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    count = forms.IntegerField(
        label="Number of random countries",
        min_value=1, max_value=10, initial=5,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )