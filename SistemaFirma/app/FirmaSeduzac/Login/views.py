from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import LoginForm
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .forms import UserForm
from django.contrib.messages.views import SuccessMessageMixin

class LoginView(LoginView):
    template_name = 'login/login.html'
    form_class = LoginForm

class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')
    success_message = "%(username)s se registró de manera exitosa"