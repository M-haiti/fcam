from django.contrib.contenttypes.models import ContentType
from django.forms.widgets import Widget
import programa
from django.contrib import admin
from programa.models import Contacto
from . import models
#Generic Foreign Key
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from django import forms


# Register your models here.
class ContactoInline(GenericTabularInline):
    model = models.Contacto
    extra = 0
    min_num = 1
    max_num = 10

# Register your models here.
class DistribucionIngresoApoyoEstrategicoInline(GenericTabularInline):
    model = models.DistribucionIngresoApoyoEstrategico
    extra = 1
    min_num = 1
    max_num = 10

# Register your models here.
class DistribucionIngresoICInline(GenericTabularInline):
    model = models.DistribucionIngresoIC
    extra = 1
    min_num = 1
    max_num = 10

# Register your models here.
class DistribucionIngresoProgramaInline(GenericTabularInline):
    model = models.DistribucionIngresoPrograma
    extra = 1
    min_num = 1
    max_num = 10


@admin.register(models.Donante)
class DonanteAdmin(admin.ModelAdmin):
    list_display = ['codigo']
    ordering = ['codigo']
    inlines = [ContactoInline]

@admin.register(models.DistribucionIngresoPrograma)
class DistribucionIngresoProgramaAdmin(admin.ModelAdmin):
   #list_display = ['monto','programa','content_type', 'object_id', 'content_object', 'ingreso']
    ordering = ['pk']

@admin.register(models.Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    list_display = ['codigo']
    ordering = ['codigo']
    inlines = [DistribucionIngresoApoyoEstrategicoInline, DistribucionIngresoICInline, DistribucionIngresoProgramaInline]

class DesembolsoAdminForm(forms.ModelForm):
    class Meta:
        model = models.Desembolso
        widgets = {
            'fecha_desembolso': forms.SelectDateWidget,
        }
        fields = '__all__'

@admin.register(models.Desembolso)
class DesembolsoAdmin(admin.ModelAdmin):
    form = DesembolsoAdminForm
    list_display = ['codigo']
    ordering = ['codigo']
