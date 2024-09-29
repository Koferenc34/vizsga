from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

class UploadFileForm(forms.Form):
    fajl = forms.FileField(required=False)
    rows = forms.IntegerField()
    cols = forms.IntegerField()

class Upload2(forms.Form):
    file = forms.FileField()
    rows = forms.IntegerField()
    cols = forms.IntegerField()