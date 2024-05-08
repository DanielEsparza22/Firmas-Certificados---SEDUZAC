from django.shortcuts import render
from .forms import CURPForm
from django.contrib.auth.decorators import login_required

@login_required
def certificaciones_parciales(request):
    if(request.method == "POST"):
        form_curp = CURPForm(request.POST)
        if(form_curp.is_valid()):
            curp = form_curp.cleaned_data['curp']
            print(curp.upper())
    else:
        form_curp = CURPForm()
    return render(request, 'cert_parc.html',{'form':form_curp})
    

