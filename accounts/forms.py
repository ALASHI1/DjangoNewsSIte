from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import LoginForm, SignupForm
from accounts.models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username","email","first_name","last_name")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields =  ("username","email","first_name","last_name")
        

class CustomLoginForm(LoginForm):
    def login(self, *args, **kwargs):
        email = self.user_cache['email']
        user = CustomUser.objects.get(email=email)
        return super(CustomLoginForm, self).login(*args, **kwargs)
        
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    def save(self, request, commit=True):
        user = super(CustomSignupForm, self).save(request)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        user.set_password(password)
        user.save()
        return user