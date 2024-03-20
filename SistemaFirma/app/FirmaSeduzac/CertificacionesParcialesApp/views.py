from django.shortcuts import render

def certificaciones_parciales(request):
    return render(request,'cert_parc.html')
