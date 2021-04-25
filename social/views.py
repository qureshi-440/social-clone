from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

class home(TemplateView):
    template_name = 'home.html'

class login_redirect(TemplateView):
    template_name = 'test.html'

class logout_redirect(TemplateView):
    template_name = 'thanks.html'