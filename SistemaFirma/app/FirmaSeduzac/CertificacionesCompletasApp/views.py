from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def certificaciones_completas(request):
    return render(request,'cert_compl.html')
