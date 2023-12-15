from django import forms

class SignUpForm(forms.Form):
    email = forms.EmailField(label="email")
    name = forms.CharField(label='name',required='True')
    password = forms.CharField(label="password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="password2", widget=forms.PasswordInput())

class LogInForm(forms.Form):
    email = forms.EmailField(label="email")
    password = forms.CharField(label="password", widget=forms.PasswordInput())
