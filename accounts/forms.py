from django import forms
from .models import Account
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter password',
        
    }))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Repeat password'
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phonenumber', 'password', 'username']


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Your Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email'
        self.fields['phonenumber'].widget.attrs['placeholder'] = 'Enter Your Phonenumber'
        self.fields['username'].widget.attrs['placeholder'] = 'Choose a username'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password != repeat_password:
            raise forms.ValidationError('Passwords do not match')


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Account.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Account.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken. Please choose a different one.')
        return username




