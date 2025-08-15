from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1' , 'password2' ,'first_name' ,'last_name' ,'email' )
        
        def __init__(self,*args, **kwargs):
            super(RegistrationForm, self).__init__(*args, **kwargs)
            
            self.fields['username'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['class'] = 'form-control'
            self.fields['first_name'].widget.attrs['class'] = 'form-control'
            self.fields['last_name'].widget.attrs['class'] = 'form-control'
            self.fields['email'].widget.attrs['class'] = 'form-control'
            
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))

class EditeRegisterForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_login = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_active = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    date_joined = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'type': 'hidden'}))
    
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','last_login','password','is_active','date_joined')


class ChangePasswordForm(PasswordChangeForm):
    old_password  = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control' , 'type': 'password'}))
    new_password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control' , 'type': 'password'}))
    new_password2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control' , 'type': 'password'}))
    
    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2')