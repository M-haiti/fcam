from django.shortcuts import render
from .models import  Desembolso, Ingreso, DistribucionIngresoApoyoEstrategico, DistribucionIngresoIC, DistribucionIngresoPrograma

def countdesembolsos(request, ano):
    conteo = Desembolso.objects.filter(fecha_desembolso__year=ano).count()
    return render(request,'countdesembolsos.html', {'conteo':conteo})

def countingresos(request, donante_fuente):
    conteo = Ingreso.objects.filter(donante_fuente=donante_fuente).count()
    return render(request,'countingresos.html',{'conteo':conteo})

def displaydesembolsosprop(request,propuesta):
    desembolsos = Desembolso.objects.filter(propuesta=propuesta)
    return render(request, 'displaydesembolsosprop.html',{'desembolsos':desembolsos})

def displaydesembolsosae(request,apoyoestrategico):
    desembolsos = Desembolso.objects.filter(apoyo_estrategico=apoyoestrategico)
    return render(request, 'displaydesembolsosae.html',{'desembolsos':desembolsos})

def displaydesembolsosic(request,iniciativaconjunta):
    desembolsos = Desembolso.objects.filter(iniciativa_conjunta=iniciativaconjunta)
    return render(request, 'displaydesembolsosic.html',{'desembolsos':desembolsos})

def displayingreso(request, id):
    ingreso = Ingreso.objects.get(id=id)
    desembolsosCops = Desembolso.objects.filter(ingreso_vinculado=id, tipo_org='COP')
    desembolsosApes = Desembolso.objects.filter(ingreso_vinculado=id, tipo_org='APE')
    desembolsosIcjs = Desembolso.objects.filter(ingreso_vinculado=id, tipo_org='ICJ')
    distprogramas = DistribucionIngresoPrograma.objects.filter(content_type=12, object_id=id)
    distics = DistribucionIngresoIC.objects.filter(content_type=12, object_id=id)
    distaes = DistribucionIngresoApoyoEstrategico.objects.filter(content_type=12, object_id=id)
    return render(request, 'displayingreso.html',{'ingreso':ingreso, 'desembolsosCops':desembolsosCops,'desembolsosApes':desembolsosApes,'desembolsosIcjs':desembolsosIcjs, 'distprogramas': distprogramas, 'distics':distics, 'distaes':distaes})
    #, 'desembolsos':desembolsos, 'distprogramas': distprogramas})
