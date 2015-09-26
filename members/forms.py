from django import forms

class SubscribeForm(forms.Form):
    email = forms.CharField(label='Email', max_length=80)
