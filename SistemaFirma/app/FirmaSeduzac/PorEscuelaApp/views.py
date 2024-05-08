from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def por_escuela(request):
    return render(request,'por_esc.html')

