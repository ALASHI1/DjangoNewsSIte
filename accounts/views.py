from django.shortcuts import render
from allauth.account.views import SignupView
from accounts.forms import CustomSignupForm

class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = 'signup.html'
