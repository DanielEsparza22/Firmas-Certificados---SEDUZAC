from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import LoginForm
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .forms import UserForm
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages

def error_403(request, exception):
    return render(request, '403.html', status=403)

def is_admin(user):
    return user.is_superuser

class LoginView(LoginView):
    template_name = 'login/login.html'
    form_class = LoginForm

class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')
    success_message = "%(username)s se registró de manera exitosa"

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error con el registro. Por favor, revisa los campos.")
        return super().form_invalid(form)

    # @method_decorator(user_passes_test(is_admin, login_url=None))
    def dispatch(self, *args, **kwargs):
        if(not is_admin(self.request.user)):
            raise PermissionDenied
        return super().dispatch(*args, **kwargs)