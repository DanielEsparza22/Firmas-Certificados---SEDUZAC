from django.shortcuts import render
from .forms import LetraFoliadorForm, AutoridadEducativaForm
from .models import FolioLetra, FolioSequence, AutoridadEducativa
from .utils import reiniciar_secuencia_folio
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def error_403(request, exception):
    return render(request, '403.html', status=403)

def is_admin(user):
    return user.is_superuser

@login_required
def reiniciar_foliador(request):
    if(not is_admin(request.user)):
        raise PermissionDenied
    mensaje = None
    letra_form = LetraFoliadorForm(request.POST or None)
    if(request.method == 'POST'):
        if(letra_form.is_valid()):
            letra_foliador = letra_form.cleaned_data['letra_foliador'].upper()
            FolioLetra.objects.all().delete()
            FolioLetra.objects.create(letra=letra_foliador)
            reiniciar_secuencia_folio()
            mensaje = f'Foliador restablecido: Letra nueva: {letra_foliador}, Secuencia restablecida a 1'

    return render(request,"reiniciar_foliador.html",{'letra_form':letra_form, 'mensaje':mensaje})

@login_required
def actualizar_autoridad_educativa(request):
    if(not is_admin(request.user)):
        raise PermissionDenied
    mensaje = None
    if(request.method == 'POST'):
        autoridad_form = AutoridadEducativaForm(request.POST)
        if(autoridad_form.is_valid()):
            autoridad = autoridad_form.cleaned_data['nombre_autoridad'].upper()
            certificado_autoridad = autoridad_form.cleaned_data['certificado_autoridad']
            AutoridadEducativa.objects.all().delete()
            AutoridadEducativa.objects.create(nombre_autoridad=autoridad, certificado_autoridad=certificado_autoridad)
            mensaje = f'Autoridad educativa actualizada correctamente'
    else:
        autoridad_form = AutoridadEducativaForm()

    return render(request, "autoridad_educativa.html",{'autoridad_form':autoridad_form,'mensaje':mensaje})
