from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse, Http404
#from django.db.models.aggregates import Count
from .models import  Coparte, Propuesta, InformeIntermedio, InformeFinal, ApoyoEstrategico, IniciativaConjunta, PropuestaIC, InformeIC

# Create your views here.
def home(request):
    return render(request, 'index.html')

def countcopartepais(request, pais):
    conteo =  Coparte.objects.filter(pais=pais).count()
    return render(request, 'countcopartepais.html', {'conteo':conteo})

def countpropuesta(request, id):
    conteo =  Propuesta.objects.filter(codigo_org__id=id).count()
    propuestas = Propuesta.objects.filter(codigo_org__id=id).order_by('codigo_org').reverse()
    return render(request, 'countpropuesta.html', {'propuestas':propuestas, 'conteo' : conteo})

def countinformeintermedio(request, id):
    conteo =  InformeIntermedio.objects.filter(propuesta_vinculada__id=id).count()
    informeIntermedios = InformeIntermedio.objects.filter(propuesta_vinculada__id=id)
    propuesta = Propuesta.objects.get(id=id)
    return render(request, 'countInformeIntermedio.html', {'informeIntermedios':informeIntermedios, 'conteo' : conteo, 'propuesta': propuesta})

def countinformefinal(request, id):
    conteo =  InformeFinal.objects.filter(propuesta_vinculada__id=id).count()
    informeFinal = InformeFinal.objects.filter(propuesta_vinculada__id=id)
    propuesta = Propuesta.objects.get(id=id)
    return render(request, 'countInformefinal.html', {'informeFinal':informeFinal, 'conteo' : conteo, 'propuesta': propuesta})

def countic(request):
    conteo =  IniciativaConjunta.objects.all().count()
    return render(request, 'countic.html', {'conteo':conteo})

def countpropic(request,id):
    conteo =  PropuestaIC.objects.filter(ic_vinculada=id).count()
    return render(request, 'countpropic.html', {'conteo':conteo})

def countinfic(request,id):
    conteo =  InformeIC.objects.filter(prop_ic_vincula=id).count()
    return render(request, 'countinfic.html', {'conteo':conteo})

def countae(request):
    conteo =  ApoyoEstrategico.objects.all().count()
    return render(request, 'countae.html', {'conteo':conteo})

def copartes(request):
    copartes = Coparte.objects.all()
    return render(request, 'copartes.html', {'copartes':copartes})

def coparte(request, coparte_id):
    template_name = 'coparte.html'
    return render(request, template_name)

