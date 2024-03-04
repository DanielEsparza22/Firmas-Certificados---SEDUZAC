from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
# from .forms import CustomPasswordChangeForm

# Create your views here.
def cerrar_sesion(request):
    logout(request)

    return redirect('Login')

def logear(request):
   if(request.method == "POST"):
      form = AuthenticationForm(request,data = request.POST)
      if(form.is_valid()):
         nombre_usuario = form.cleaned_data.get("username")
         password_usuario = form.cleaned_data.get("password")

         usuario = authenticate(username = nombre_usuario, password = password_usuario)
         if(usuario is not None):
            login(request, usuario)
            return redirect('Inicio')
         else:
            messages.error(request,"Usuario no valido")
      else:
         messages.error(request,"Información incorrecta")

   form = AuthenticationForm()
   return render(request,"login/login.html",{"form":form})
