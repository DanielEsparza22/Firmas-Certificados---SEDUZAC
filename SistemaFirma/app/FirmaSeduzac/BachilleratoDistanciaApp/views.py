from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def bachillerato_distancia(request):
    return render(request,'bac_dist.html')

