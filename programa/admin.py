from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.http import request
from . import models
from . import forms

#Generic Foreign Key
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline

#form validation
from django.core.exceptions import ValidationError
from django import forms

admin.site.site_header = 'Plataforma de Monitoreo y Evaluación del FCAM'

# Register your models here.
USERGROUP = [
    'Copartes',
    'Supervisoras',
    'Financieras',
    'Visitantes'
]

class ContactoInline(GenericTabularInline):
    model = models.Contacto
    extra = 2
    min_num = 1
    max_num = 10

class GrupoInline(GenericStackedInline):
    model = models.Grupoactor
    extra = 2
    min_num = 1
    max_num = 10

class CommentInline(GenericStackedInline):
    model = models.Comment
    min_num = 1
    extra = 1
    fields = ['cuerpo']

@admin.register(models.Contacto)
class ContactoAdmin(admin.ModelAdmin):    
    list_display = ['nombre','cargo','telefono','correo','vinculado_a']
    ordering = ['nombre']

    """
    #Sets created by field value on Save 
    def save_model(self, request, obj, form, change):
        # associating the current logged in user to the client_id
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

    #Sets model permission on the spot based on current loggedin user group,m username and created_by field comparisons
    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name=USERGROUP[0]).exists():
            if obj is not None and obj.created_by != request.user:
                return False
            return True

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name=USERGROUP[0]).exists():
            if obj is not None and obj.created_by != request.user:
                return False
            return True
       """     

    #Filters display list to user related nodes
    def get_queryset(self, request):
        if request.user.groups.filter(name=USERGROUP[0]).exists():
            #self.message_user(request,'Es Contacto.', messages.INFO)
              queryset = models.Contacto.objects.filter(copartecontacto__responsable=request.user.id)
        else:
              queryset = models.Contacto.objects.all()      
        return queryset        

    #Hides from admin main sidebar
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return False

@admin.register(models.Coparte)
class CoparteAdmin(admin.ModelAdmin):
    list_display = ['codigo_org','nombre_org','supervisora', 'responsable']
    ordering = ['codigo_org']
    inlines = [ContactoInline, CommentInline]
    search_fields = ['codigo_org', 'nombre_org']
    list_filter = ['pais', 'estatus_org']
   
    fieldsets = (
        ('Información del sistema', {
            'fields': ('codigo_org','pais','estatus_org','supervisora','responsable','fecha_completado','sello_fecha_creacion','sello_fecha_actualizacion')
        }),
        ('Información General de la organizacion', {
            'fields': ('nombre_org','fecha_grupo','personeria','fecha_personeria','informacion_bancaria','telefono','correo','sitio_web','municipio','ciudad','direccion'),
        }),
    )

    #Sets specific readonly fields according to user group
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            if request.user.is_superuser:
                readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[0]).exists():
                readonly_fields = ['pais','codigo_org','estatus_org','supervisora','fecha_completado','sello_fecha_creacion', 'sello_fecha_actualizacion','responsable']
            elif request.user.groups.filter(name=USERGROUP[1]).exists():
                readonly_fields = ['pais','codigo_org','sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[2]).exists():
                readonly_fields = ['pais','codigo_org','sello_fecha_creacion', 'sello_fecha_actualizacion']    
            elif request.user.groups.filter(name=USERGROUP[3]).exists():
                readonly_fields = ['pais','codigo_org','sello_fecha_creacion', 'sello_fecha_actualizacion']        
        else:        
            readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
        return list(set(readonly_fields))

    #Filters display list to user related nodes
    def get_queryset(self, request):
        if request.user.is_superuser:
            queryset = models.Coparte.objects.all()
        elif request.user.groups.filter(name=USERGROUP[0]).exists():
            #self.message_user(request,'Es Coparte.', messages.INFO)
            try:  
                queryset = models.Coparte.objects.filter(responsable=request.user.id)
            except:
                queryset = models.Coparte.objects.none()
        elif request.user.groups.filter(name=USERGROUP[1]).exists():
            #self.message_user(request,'Es Supervisora.', messages.INFO)
            try:
                queryset = models.Coparte.objects.filter(supervisora=request.user.id)
            except:
                queryset = models.Coparte.objects.none()
        elif request.user.groups.filter(name=USERGROUP[2]).exists():
            #self.message_user(request,'Es Gestion Finanieras.', messages.INFO)
            queryset = models.Coparte.objects.all() #Can only view as per permissions system
        elif request.user.groups.filter(name=USERGROUP[3]).exists():
            #self.message_user(request,'Es Gestion Finanieras.', messages.INFO)
            queryset = models.Coparte.objects.all() #Can only view as per            
        else:
              queryset = models.Coparte.objects.none()      
        return queryset

    #Filters User reference fields filter by groups. Eg: "responsable" user reference field only shows user group type responsable
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "responsable":
            kwargs["queryset"] = get_user_model().objects.filter(groups__name=USERGROUP[0])
        elif db_field.name == "supervisora":
            kwargs["queryset"] = get_user_model().objects.filter(groups__name=USERGROUP[1])
    
        return super().formfield_for_foreignkey(db_field, request, **kwargs)        

    #Sets created by field value to user performing save action, for inline model named Contacto
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, models.Comment): #Check if it is the correct type of inline
                if(not instance.usuario):
                    instance.usuario = request.user
                else:
                    instance.usuario = request.user            
                instance.save() 

@admin.register(models.Propuesta)
class PropuestaAdmin(admin.ModelAdmin):
    list_display = ['codigo_prop','nombre_prop','programa','codigo_org','duracion_prop', 'pais','supervisora', 'responsable']
    ordering = ['codigo_prop']
    inlines = [ContactoInline, GrupoInline, CommentInline]
    search_fields = ['codigo_org', 'codigo_prop','nombre_prop']
    list_filter = ['programa','pais', 'estatus_prop','ano']
    
    fieldsets = (
        ('Información del sistema', {
            'fields': ('codigo_prop','codigo_org','estatus_prop','programa', 'supervisora', 'responsable','sello_fecha_creacion','sello_fecha_actualizacion')
        }),
        ('Información General de la propuesta', {
            'fields': ('nombre_prop', 'pais', 'ano','fecha_entrega','fecha_aprobacion','duracion_prop'),
        }),
        ('Gestión Financiera', {
            'fields': ('presupuesto_aprobado_super_USD','presupuesto_aprobado_super_EUR','presupuesto_aprobado_finan_USD', 'presupuesto_aprobado_finan_EUR','tipo_de_cambio_EUR_USD'),
        })
    )

    #Filters display list to user related nodes
    def get_queryset(self, request):
        if request.user.is_superuser:
            queryset = models.Propuesta.objects.all()
        elif request.user.groups.filter(name=USERGROUP[0]).exists():
            #self.message_user(request,'Es Propuesta.', messages.INFO)
            try:  
                queryset = models.Propuesta.objects.filter(responsable=request.user.id)
            except:
                queryset = models.Propuesta.objects.none()
        elif request.user.groups.filter(name=USERGROUP[1]).exists():
            #self.message_user(request,'Es Supervisora.', messages.INFO)
            try:
                queryset = models.Propuesta.objects.filter(supervisora=request.user.id)
            except:
                queryset = models.Propuesta.objects.none()
        elif request.user.groups.filter(name=USERGROUP[2]).exists():
            #self.message_user(request,'Es Gestion Finanieras.', messages.INFO)
            queryset = models.Propuesta.objects.all() #Can only view as per permissions system
        elif request.user.groups.filter(name=USERGROUP[3]).exists():
            #self.message_user(request,'Es Gestion Finanieras.', messages.INFO)
            queryset = models.Propuesta.objects.all() #Can only view as per            
        else:
            queryset = models.Propuesta.objects.none()      
        return queryset

    #Sets specific readonly fields according to user group
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            if request.user.is_superuser:
                readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[0]).exists():
                readonly_fields = ['codigo_prop','codigo_org','responsable','supervisora','sello_fecha_creacion', 'sello_fecha_actualizacion','duracion_prop', 'pais','estatus_prop','codigo_org','presupuesto_aprobado_super_USD','presupuesto_aprobado_super_EUR','presupuesto_aprobado_finan_USD','presupuesto_aprobado_finan_EUR','tipo_de_cambio_EUR_USD']  
            elif request.user.groups.filter(name=USERGROUP[1]).exists():
                readonly_fields = ['codigo_prop','codigo_org','sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[2]).exists():
                readonly_fields = ['codigo_prop','codigo_org','estatus_prop', 'supervisora', 'responsable','sello_fecha_creacion','sello_fecha_actualizacion','nombre_prop','programa', 'pais', 'ano','fecha_entrega','fecha_aprobacion','duracion_prop'] 
            elif request.user.groups.filter(name=USERGROUP[3]).exists():
                readonly_fields = ['codigo_prop','sello_fecha_creacion', 'sello_fecha_actualizacion']        
        else:        
            readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
        return list(set(readonly_fields))
    


    #Filters User reference fields filter by groups. Eg: "responsable" user reference field only shows user group type responsable
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "responsable":
            kwargs["queryset"] = get_user_model().objects.filter(groups__name=USERGROUP[0])
        elif db_field.name == "supervisora":
            kwargs["queryset"] = get_user_model().objects.filter(groups__name=USERGROUP[1])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)    

@admin.register(models.InformeIntermedio)
class InformeIntermedioAdmin(admin.ModelAdmin):
    list_display = ['codigo_org','codigo_prop','propuesta_vinculada','get_prop','get_orgname','estatus_prop','informe_finan_aprobado_gestion']
    #add org name in list
    ordering = ['codigo_prop']
    inlines = [ContactoInline, GrupoInline]
    search_fields = ['codigo_prop','propuesta_vinculada','codigo_org']
    list_filter = ['ano'] 
    
    #get Propuesta vinculada nombre, to display inside list_diplay
    def get_prop(self, obj):
        return obj.propuesta_vinculada.nombre_prop
    get_prop.short_description = 'Nombre de propuesta'
    get_prop.admin_order_field = 'propuesta_vinculada__nombre_prop'

    #get Propuesta vinculada nombre, to display inside list_diplay
    def get_orgname(self, obj):
        return obj.codigo_org.nombre_org
    get_orgname.short_description = 'Nombre de organizacion'
    get_orgname.admin_order_field = 'codigo_org__nombre_org'
    
    #Filters User reference fields filter by groups. Eg: "responsable" user reference field only shows user group type responsable
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "responsable":
            kwargs["queryset"] = get_user_model().objects.filter(groups__name=USERGROUP[0])
        elif db_field.name == "supervisora":
            kwargs["queryset"] = get_user_model().objects.filter(groups__name=USERGROUP[1])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)    

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            if request.user.is_superuser:
                readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[0]).exists():
                readonly_fields = ['codigo_prop','propuesta_vinculada','plazo','codigo_org','estatus_prop', 'responsable', 'supervisora','sello_fecha_creacion', 'sello_fecha_actualizacion', 'informe_finan_aprobado_supervisora','informe_finan_aprobado_gestion']  
            elif request.user.groups.filter(name=USERGROUP[1]).exists():
                readonly_fields = ['codigo_prop','propuesta_vinculada','plazo','codigo_org','sello_fecha_creacion', 'sello_fecha_actualizacion','informe_finan_aprobado_gestion']
            elif request.user.groups.filter(name=USERGROUP[2]).exists():
                readonly_fields = ['codigo_prop','propuesta_vinculada','plazo','codigo_org','estatus_prop', 'responsable', 'supervisora','sello_fecha_creacion', 'sello_fecha_actualizacion','nombre_prop','fecha_periodo_init','fecha_periodo_finit','ano','fecha_entrega','fotografias','informe_finan_aprobado_supervisora'] 
            elif request.user.groups.filter(name=USERGROUP[3]).exists():
                readonly_fields = ['codigo_prop','sello_fecha_creacion', 'sello_fecha_actualizacion']        
        else:        
            readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
        return list(set(readonly_fields))

    fieldsets = (
        ('Información del sistema', {
            'fields': ('codigo_org','propuesta_vinculada','codigo_prop','plazo','estatus_prop', 'responsable', 'supervisora','sello_fecha_creacion', 'sello_fecha_actualizacion')
        }),
        ('Información General del informe intermedio', {
            'fields': ('nombre_prop','fecha_periodo_init','fecha_periodo_finit','ano','fecha_entrega','fotografias'),
        }),
        ('Gestión Financiera', {
            'fields': ('reporte_financiero','informe_finan_aprobado_supervisora','informe_finan_aprobado_gestion','estado_bancario'),
        })
    )
    
    #Filters display list to user related nodes
    def get_queryset(self, request):
        if request.user.is_superuser:
            queryset = models.InformeIntermedio.objects.all()
        elif request.user.groups.filter(name=USERGROUP[0]).exists():
            #self.message_user(request,'Es InformeIntermedio.', messages.INFO)
            try:  
                queryset = models.InformeIntermedio.objects.filter(responsable=request.user.id)
            except:
                queryset = models.InformeIntermedio.objects.none()
        elif request.user.groups.filter(name=USERGROUP[1]).exists():
            #self.message_user(request,'Es Supervisora.', messages.INFO)
            try:
                queryset = models.InformeIntermedio.objects.filter(supervisora=request.user.id)
            except:
                queryset = models.InformeIntermedio.objects.none()
        elif request.user.groups.filter(name=USERGROUP[2]).exists():
            #self.message_user(request,'Es Gestion Finanieras.', messages.INFO)
            queryset = models.InformeIntermedio.objects.all() #Can only view as per permissions system
        elif request.user.groups.filter(name=USERGROUP[3]).exists():
            #self.message_user(request,'Es Gestion Finanieras.', messages.INFO)
            queryset = models.InformeIntermedio.objects.all() #Can only view as per            
        else:
            queryset = models.InformeIntermedio.objects.none()      
        return queryset

@admin.register(models.InformeFinal)
class InformeFinalAdmin(admin.ModelAdmin):
    list_display = ['codigo_org','codigo_prop','propuesta_vinculada','get_prop','get_orgname','estatus_prop','informe_finan_aprobado_gestion']
    ordering = ['codigo_prop']
    inlines = [ContactoInline, GrupoInline]
    search_fields = ['codigo_prop','propuesta_vinculada','codigo_org']
    list_filter = ['ano'] 
    
    #get nombre de Propuesta vinculada, to display inside list_diplay
    def get_prop(self, obj):
        return obj.propuesta_vinculada.nombre_prop
    get_prop.short_description = 'Nombre de propuesta'
    get_prop.admin_order_field = 'propuesta_vinculada__nombre_prop'

    #get nombre Organizacion vinculada, to display inside list_diplay
    def get_orgname(self, obj):
        return obj.codigo_org.nombre_org
    get_orgname.short_description = 'Nombre de organizacion'
    get_orgname.admin_order_field = 'codigo_org__nombre_org'

    
    fieldsets = (
        ('Información del sistema', {
            'fields': ('codigo_prop','codigo_org','propuesta_vinculada','informe_intermedio_anterior','plazo','estatus_prop', 'responsable', 'supervisora','sello_fecha_creacion', 'sello_fecha_actualizacion')
        }),
        ('Información General de la propuesta', {
            'fields': ('nombre_prop','fecha_periodo_init','fecha_periodo_finit','ano','fecha_entrega','fotografias'),
        }),
        ('Gestión Financiera', {
            'fields': ('reporte_financiero','informe_finan_aprobado_supervisora','informe_finan_aprobado_gestion','estado_bancario','presupuesto_aprobado_super_USD','presupuesto_aprobado_super_EUR','tipo_de_cambio_EUR_USD','monto_total_ejecutado'),
        })
    )

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            if request.user.is_superuser:
                readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[0]).exists():
                readonly_fields = ['codigo_prop','propuesta_vinculada','plazo','codigo_org','informe_intermedio_anterior','estatus_prop', 'responsable', 'supervisora','sello_fecha_creacion', 'sello_fecha_actualizacion','reporte_financiero','informe_finan_aprobado_supervisora','informe_finan_aprobado_gestion','estado_bancario','presupuesto_aprobado_super_USD','presupuesto_aprobado_super_EUR','tipo_de_cambio_EUR_USD','monto_total_ejecutado']  
            elif request.user.groups.filter(name=USERGROUP[1]).exists():
                readonly_fields = ['codigo_org','propuesta_vinculada','codigo_prop','sello_fecha_creacion', 'sello_fecha_actualizacion','informe_finan_aprobado_gestion']
            elif request.user.groups.filter(name=USERGROUP[2]).exists():
                readonly_fields = ['codigo_prop','propuesta_vinculada','plazo','codigo_org','estatus_prop', 'responsable', 'supervisora','sello_fecha_creacion', 'sello_fecha_actualizacion','nombre_prop','fecha_periodo_init','fecha_periodo_finit','ano','fecha_entrega','fotografias','informe_finan_aprobado_supervisora'] 
            elif request.user.groups.filter(name=USERGROUP[3]).exists():
                readonly_fields = ['codigo_prop','sello_fecha_creacion', 'sello_fecha_actualizacion']        
        else:        
            readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
        return list(set(readonly_fields))

    #Filters display list to user related nodes
    def get_queryset(self, request):
        if request.user.is_superuser:
            queryset = models.InformeFinal.objects.all()
        elif request.user.groups.filter(name=USERGROUP[0]).exists():
            #self.message_user(request,'Es InformeFinal.', messages.INFO)
            try:  
                queryset = models.InformeFinal.objects.filter(responsable=request.user.id)
            except:
                queryset = models.InformeFinal.objects.none()
        elif request.user.groups.filter(name=USERGROUP[1]).exists():
            #self.message_user(request,'Es Supervisora.', messages.INFO)
            try:
                queryset = models.InformeFinal.objects.filter(supervisora=request.user.id)
            except:
                queryset = models.InformeFinal.objects.none()
        elif request.user.groups.filter(name=USERGROUP[2]).exists():
            #self.message_user(request,'Es Gestion Finanieras.', messages.INFO)
            queryset = models.InformeFinal.objects.all() #Can only view as per permissions system
        elif request.user.groups.filter(name=USERGROUP[3]).exists():
            #self.message_user(request,'Es Gestion Finanieras.', messages.INFO)
            queryset = models.InformeFinal.objects.all() #Can only view as per            
        else:
            queryset = models.InformeFinal.objects.none()      
        return queryset

    #Filters User reference fields filter by groups. Eg: "responsable" user reference field only shows user group type responsable
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "responsable":
            kwargs["queryset"] = get_user_model().objects.filter(groups__name=USERGROUP[0])
        elif db_field.name == "supervisora":
            kwargs["queryset"] = get_user_model().objects.filter(groups__name=USERGROUP[1])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)    

@admin.register(models.IniciativaConjunta)
class IniciativaConjuntaAdmin(admin.ModelAdmin):

    list_display = ['codigo_org','nombre_org','pais','supervisora']
    ordering = ['codigo_org']
    #inlines = [ContactoInline]
    
    fieldsets = (
        ('Información del sistema', {
            'fields': ('codigo_org','tipo_ic','pais','estatus_org','supervisora','fecha_completado','sello_fecha_creacion','sello_fecha_actualizacion')
        }),
        ('Información General de la organizacion', {
            'fields': ('nombre_org','fecha_grupo','personeria','fecha_personeria','informacion_bancaria','telefono','correo','sitio_web','municipio','ciudad','direccion'),
        }),
    )
    

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            if request.user.is_superuser:
                readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[0]).exists():
                readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[1]).exists():
                readonly_fields = ['codigo_org','tipo_ic','sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[2]).exists():
                readonly_fields = ['codigo_org','tipo_ic','pais','estatus_org','supervisora','fecha_completado','sello_fecha_creacion','sello_fecha_actualizacion','nombre_org','fecha_grupo','personeria','fecha_personeria','informacion_bancaria','telefono','correo','sitio_web','municipio','ciudad','direccion']
            elif request.user.groups.filter(name=USERGROUP[3]).exists():
                readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']        
        else:        
            readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
        return list(set(readonly_fields))


    def get_queryset(self, request):
        if request.user.is_superuser:
            queryset = models.IniciativaConjunta.objects.all()
        elif request.user.groups.filter(name=USERGROUP[0]).exists():
                queryset = models.IniciativaConjunta.objects.none()
        elif request.user.groups.filter(name=USERGROUP[1]).exists():
            #self.message_user(request,'Es Supervisora.', messages.INFO)
            try:
                queryset = models.IniciativaConjunta.objects.filter(supervisora=request.user.id)
            except:
                queryset = models.IniciativaConjunta.objects.none()
        elif request.user.groups.filter(name=USERGROUP[2]).exists():
            #self.message_user(request,'Es Supervisora.', messages.INFO)
            queryset = models.IniciativaConjunta.objects.all()
        elif request.user.groups.filter(name=USERGROUP[3]).exists():
            #self.message_user(request,'Es Supervisora.', messages.INFO)
            queryset = models.IniciativaConjunta.objects.all()
        else:
              queryset = models.IniciativaConjunta.objects.none()      
        return queryset
    #Filters User reference fields filter by groups. Eg: "responsable" user reference field only shows user group type responsable
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "supervisora":
            kwargs["queryset"] = get_user_model().objects.filter(groups__name=USERGROUP[1])
    
        return super().formfield_for_foreignkey(db_field, request, **kwargs)        

@admin.register(models.PropuestaIC)
class PropuestaICAdmin(admin.ModelAdmin):
    list_display = ['codigo_prop_ic','ic_vinculada','get_icname','ano']
    ordering = ['codigo_prop_ic']

    #get nombre Organizacion vinculada, to display inside list_diplay
    def get_icname(self, obj):
        return obj.ic_vinculada.nombre_org
    get_icname.short_description = 'Nombre de organización'
    get_icname.admin_order_field = 'ic_vinculada__nombre_org'
    
    fieldsets = (
        ('Información del sistema', {
            'fields': ('codigo_prop_ic','ic_vinculada','ano','sello_fecha_creacion', 'sello_fecha_actualizacion')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            if request.user.is_superuser:
                readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[0]).exists():
                readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[1]).exists():
                readonly_fields = ['codigo_prop_ic','ic_vinculada','sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[2]).exists():
                readonly_fields = ['codigo_prop_ic','ic_vinculada','sello_fecha_creacion', 'sello_fecha_actualizacion','ano']    
            elif request.user.groups.filter(name=USERGROUP[3]).exists():
                readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
        else:        
            readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
        return list(set(readonly_fields))
    
    def get_queryset(self, request):
        if request.user.is_superuser:
            queryset = models.PropuestaIC.objects.all()
        elif request.user.groups.filter(name=USERGROUP[0]).exists():
                queryset = models.PropuestaIC.objects.none()
        elif request.user.groups.filter(name=USERGROUP[1]).exists():
            try:
                queryset = models.PropuestaIC.objects.filter(ic_vinculada__supervisora=request.user.id)
            except:
                queryset = models.PropuestaIC.objects.none()
        elif request.user.groups.filter(name=USERGROUP[2]).exists():
            queryset = models.PropuestaIC.objects.all()
        elif request.user.groups.filter(name=USERGROUP[3]).exists():
            queryset = models.PropuestaIC.objects.all()    
        else:
              queryset = models.PropuestaIC.objects.none()      
        return queryset

@admin.register(models.InformeIC)
class InformeICAdmin(admin.ModelAdmin):
    list_display = ['codigo_inf_ic','prop_ic_vincula', 'ic_vinculada','get_icname',  'ano']
    ordering = ['codigo_inf_ic']
    
    #get nombre Organizacion vinculada, to display inside list_diplay
    def get_icname(self, obj):
        return obj.ic_vinculada.nombre_org
    get_icname.short_description = 'Nombre de organizacion'
    get_icname.admin_order_field = 'ic_vinculada__nombre_org'

    fieldsets = (
        ('Información del sistema', {
            'fields': ('codigo_inf_ic','ic_vinculada','prop_ic_vincula','ano','sello_fecha_creacion', 'sello_fecha_actualizacion')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            if request.user.is_superuser:
                readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[0]).exists():
                readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[1]).exists():
                readonly_fields = ['codigo_inf_ic','ic_vinculada','prop_ic_vincula','sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[2]).exists():
                readonly_fields = ['codigo_inf_ic','ic_vinculada','prop_ic_vincula','ano','sello_fecha_creacion', 'sello_fecha_actualizacion']    
            elif request.user.groups.filter(name=USERGROUP[3]).exists():
                readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
        else:        
            readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
        return list(set(readonly_fields))

    def get_queryset(self, request):
        if request.user.is_superuser:
            queryset = models.InformeIC.objects.all()
        elif request.user.groups.filter(name=USERGROUP[0]).exists():
                queryset = models.InformeIC.objects.none()
        elif request.user.groups.filter(name=USERGROUP[1]).exists():
            try:
                queryset = models.InformeIC.objects.filter(ic_vinculada__supervisora=request.user.id)
            except:
                queryset = models.InformeIC.objects.none()
        elif request.user.groups.filter(name=USERGROUP[2]).exists():
            queryset = models.InformeIC.objects.all()
        elif request.user.groups.filter(name=USERGROUP[3]).exists():
            queryset = models.InformeIC.objects.all()              
        else:
              queryset = models.InformeIC.objects.none()      
        return queryset

@admin.register(models.ApoyoEstrategico)
class ApoyoEstrategico(admin.ModelAdmin):
    list_display = ['codigo_org','nombre_org','programa','supervisora']
    ordering = ['codigo_org']
    search_fields = ['codigo_org', 'nombre_org']
    list_filter = ['pais', 'estatus_org']
    readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
      
    fieldsets = (
         ('Información del sistema', {
            'fields': ('codigo_org','programa','pais','estatus_org','supervisora','fecha_completado','sello_fecha_creacion','sello_fecha_actualizacion')
        }),
        ('Información General de la organizacion', {
            'fields': ('nombre_org','tipo_org','fecha_grupo','telefono','correo','sitio_web','municipio','ciudad','direccion'),
        }),
        ('Gestión Financiera', {
            'fields': ('tipo_donativo','fondo_resp_emer','apoyos_estra_punt','ano_donativo','monto_entregado_USD','monto_entregado_EUR','tipo_de_cambio_EUR_USD'),
        })
    )

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            if request.user.is_superuser:
                readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[0]).exists():
                readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[1]).exists():
                readonly_fields = ['codigo_org','programa','sello_fecha_creacion', 'sello_fecha_actualizacion']
            elif request.user.groups.filter(name=USERGROUP[2]).exists():
                readonly_fields = ['codigo_org','programa','pais','estatus_org','supervisora','fecha_completado','sello_fecha_creacion','sello_fecha_actualizacion','nombre_org','tipo_org','fecha_grupo','telefono','correo','sitio_web','municipio','ciudad','direccion']
            elif request.user.groups.filter(name=USERGROUP[3]).exists():
                readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
        else:        
            readonly_fields = ['sello_fecha_creacion', 'sello_fecha_actualizacion']
        return list(set(readonly_fields))

    def get_queryset(self, request):
        if request.user.is_superuser:
            queryset = models.ApoyoEstrategico.objects.all()
        elif request.user.groups.filter(name=USERGROUP[0]).exists():
                queryset = models.ApoyoEstrategico.objects.none()
        elif request.user.groups.filter(name=USERGROUP[1]).exists():
            try:
                queryset = models.ApoyoEstrategico.objects.filter(supervisora=request.user.id)
            except:
                queryset = models.ApoyoEstrategico.objects.none()
        elif request.user.groups.filter(name=USERGROUP[2]).exists():
            queryset = models.ApoyoEstrategico.objects.all() 
        elif request.user.groups.filter(name=USERGROUP[3]).exists():
            queryset = models.ApoyoEstrategico.objects.all()     
        else:
              queryset = models.ApoyoEstrategico.objects.none()      
        return queryset

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('fecha','usuario','cuerpo')
    search_fields = ('usuario','cuerpo')
    
    #Hides from admin main sidebar
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return False