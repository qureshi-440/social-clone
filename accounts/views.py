from django.shortcuts import render
from django.urls import reverse_lazy
from . import forms
from django.views.generic import CreateView

# Create your views here.

class signup(CreateView):
    form_class = forms.Createuser
    template_name = 'signup/register.html'
    success_url = reverse_lazy('accounts:login')