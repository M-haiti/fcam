from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

#Signals & send mail imports
from django.core.mail import send_mail
from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

#Generic Foreign Key
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

#User = get_user_model()

#file upload extension validators
def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')
    
PROGRAMAS = (
    ('AFP','AfroPoderosas'),
    ('DMJ','Derechos de las Mujeres y Justicia Ambiental'),
    ('DLM','Derechos Laborales de las Mujeres'),
    ('DSR','Derechos Sexuales y Reproductivos'),
    ('LDS','Liderando desde el Sur'),
    ('MDC','Mujeres con Discapacidad'),
    ('MMJ','Mujeres jóvenes'),
    ('MMM','Mujeres Migrantes'),
    ('PEG','Programa Especial Guatemala'),
    ('NIN','Ninguno'),
)
PAISES = ( 
    ('GTM', 'Guatemala'),
    ('PAN', 'Panamá'),
    ('SLV', 'El Salvador'),
    ('HND', 'Honduras'),
    ('BLZ', 'Belize'),
    ('NIC', 'Nicaragua'),
    ('CRI', 'Costa Rica'),
    ('OTR', 'Otro')
)
TIPOIC = ( 
    ('SCA','Socias en Centroamérica'),
    ('FCA','Socias fuera de Centroamérica'),
    ('RFM','Redes y fondos de mujeres'),
    ('RRC','Respuesta Rápida en Centroamérica'),
    ('RRF','Respuesta Rápida fuera de Centroamérica'),
    ('OTR','Otros'),
)
PARTICIPAIC = ( 
    ('IC1','INICIATIVA-3'),
    ('IC2','GAGGA'),
    ('IC3','IMDEFENSORAS'),
)
ANO = (
    ('2021','2021'),
    ('2022','2022'),
    ('2023','2023'),
    ('2024','2024'),
    ('2025','2025')
)
# Create your models here.
class BaseOrg(models.Model):
    ESTATUS = ( 
        ('ACT', 'Activo'),
        ('TER', 'Terminado')
    )
    pais = models.CharField('País',max_length=3, choices=PAISES)
    codigo_org = models.CharField('Código de organización', max_length=25, unique=True)
    nombre_org = models.CharField('Nombre de organización', max_length=255, null=True, blank=True)
    estatus_org = models.CharField('Estatus', max_length=3, choices=ESTATUS, default='ACT')
    supervisora = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    sello_fecha_creacion = models.DateTimeField('Sello fecha de creación', auto_now_add=True, null=True)
    sello_fecha_actualizacion = models.DateTimeField('Sello fecha de actualización', auto_now=True, null=True)
    fecha_completado = models.DateField('Fecha inicial en que se completó la ficha', null=True, blank=True)
    municipio = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=255, blank=True)
    direccion = models.TextField('Dirección', max_length=255, blank=True)
    telefono = models.CharField('Teléfono', max_length=60, blank=True)
    correo = models.EmailField('Correo electrónico', blank=True)
    sitio_web = models.URLField(null=True, blank=True)
    fecha_grupo = models.DateField('Fecha de conformación del grupo u organización', null=True, blank=True)
    
    def __str__(self):
        return self.codigo_org

    class Meta:
        abstract=True


class BaseOrgExt(models.Model):
   personeria = models.BooleanField('Cuenta con personería jurídica', null=True, blank=True)
   fecha_personeria = models.DateField('Fecha de obtención de personería jurídica', null=True, blank=True)
   informacion_bancaria = models.TextField('Información bancaria', null=True, blank=True)

   class Meta:
       abstract=True

class Coparte(BaseOrg, BaseOrgExt):
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True, related_name='reponsable')
    #Generic relation to reverse relate contactos with foreign
    contacto = GenericRelation('Contacto' ,content_type_field='content_type', object_id_field='object_id', related_query_name='copartecontacto', blank=True)

    class Meta:
        verbose_name_plural = "1. Copartes"

class BaseProp(models.Model):
    ESTATUSPROP = (
         ('ENR','En revisión'),
         ('APR','Aprobado'),
         ('VCM','Ver Comentarios'),
    )
    codigo_prop = models.CharField('Código', max_length=25, null=True)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True, related_name='%(class)s_reponsable_propu')
    supervisora = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True, related_name='%(class)s_supervisora_propu')
    estatus_prop = models.CharField('Estatus', max_length=3, choices=ESTATUSPROP, default='ACT')
    sello_fecha_creacion = models.DateTimeField('Sello fecha de creación', auto_now_add=True, null=True)
    sello_fecha_actualizacion = models.DateTimeField('Sello fecha de actualización', auto_now=True, null=True)
    nombre_prop =  models.CharField('Nombre de la propuesta', max_length=255, null=True, blank=True)
    fecha_entrega = models.DateField('Fecha de entrega de la propuesta', null=True, blank=True)
    codigo_org = models.ForeignKey(Coparte, on_delete=models.SET_NULL, null=True)
    ano = models.CharField('Año', max_length=4, choices=ANO, null=True, blank=True)

    def __str__(self):
        return self.codigo_prop

    class Meta:
        abstract=True

class Propuesta(BaseProp):
    DURACION = (
         ('12M','12 Meses'),
         ('18M','18 Meses'),
         ('24M','24 Meses'),
         ('36M','36 Meses'),
    )
    FONDOSASIGNADOS = (
        ('SOP','Soporte general'),
        ('APG','Apoyo para proyectos')
    )
    duracion_prop = models.CharField('Duración de la propuesta', max_length=3, choices=DURACION, null=True) 
    pais = models.CharField('País', max_length=3, choices=PAISES, blank=True)
    fondos_prop = models.CharField('Fondos asignados a la propuestas', max_length=3, choices=FONDOSASIGNADOS, null=True)
    fecha_aprobacion = models.DateField('Fecha de aprobación', null=True, blank=True)
    programa = models.CharField('Programa', max_length=3, choices=PROGRAMAS, null=True)
    presupuesto_aprobado_super_USD = models.DecimalField('Presupuesto aprobado por Supervisora FCAM (USD)', max_digits=8, decimal_places=2, default=0)
    presupuesto_aprobado_super_EUR = models.DecimalField('Presupuesto aprobado por Supervisora FCAM (EUR)', max_digits=8, decimal_places=2, default=0)
    presupuesto_aprobado_finan_USD = models.DecimalField('Presupuesto aprobado por Gestión Financiera (USD)', max_digits=8, decimal_places=2, default=0)
    presupuesto_aprobado_finan_EUR = models.DecimalField('Presupuesto aprobado por Gestión Financiera (EUR)', max_digits=8, decimal_places=2, default=0)
    tipo_de_cambio_EUR_USD = models.DecimalField('Tipo de cambio (EUR -> USD)', max_digits=8, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = "2. Propuestas"

class BaseInf(models.Model):
    propuesta_vinculada = models.ForeignKey(Propuesta, on_delete=models.SET_NULL, null=True)
    fecha_periodo_init = models.DateField('Fecha de inicio', null=True, blank=True)
    fecha_periodo_finit = models.DateField('Fecha de finalización', null=True, blank=True)
    reporte_financiero = models.FileField('Reporte Financiero (PDF)', validators=[validate_file_extension], upload_to='%Y/reportesfinancieros',null=True, blank=True)
    informe_finan_aprobado_supervisora = models.BooleanField('Informe financiero aprobado por oficial de programa', null=True)
    informe_finan_aprobado_gestion = models.BooleanField('Informe financiero aprobado por oficial de gestión financiera', null=True)
    estado_bancario = models.FileField('Estado bancario (PDF)', validators=[validate_file_extension], upload_to='%Y/estadosbancarios',null=True, blank=True)
    fotografias = models.FileField('Fotografías', validators=[validate_file_extension], upload_to='%Y/fotografias',null=True, blank=True)

    def __str__(self):
        return self.codigo_org

    class Meta:
        abstract=True

class InformeIntermedio(BaseProp, BaseInf):
    PLAZO = (
         ('6M','6 Meses'),
         ('12M','12 Meses'),
         ('18M','18 Meses'),
         ('30M','30 Meses'),
    )
    plazo = models.CharField('Plazo del informe intermedio', max_length=3, choices= PLAZO, null=True) 

    class Meta:
        verbose_name_plural = '3. Informes intermedios'

class InformeFinal(BaseProp, BaseInf):
    PLAZO = (
         ('12M','12 Meses'),
         ('24M','24 Meses'),
         ('36M','36 Meses'),
    )
    plazo = models.CharField('Plazo del informe final', max_length=3, choices= PLAZO, null=True) 
    informe_intermedio_anterior = models.ForeignKey(InformeIntermedio, on_delete=models.SET_NULL, null=True)
    presupuesto_aprobado_super_USD = models.DecimalField('Presupuesto aprobado por Supervisora FCAM (USD)', max_digits=8, decimal_places=2, default=0)
    presupuesto_aprobado_super_EUR = models.DecimalField('Presupuesto aprobado por Supervisora FCAM (EUR)', max_digits=8, decimal_places=2, default=0)
    tipo_de_cambio_EUR_USD = models.DecimalField('Tipo de cambio (EUR -> USD)', max_digits=8, decimal_places=2, default=0)
    monto_total_ejecutado = models.DecimalField('Monto total ejecutado', max_digits=8, decimal_places=2, default=0)
    
    class Meta:
        verbose_name_plural = '4. Informes finales'

class ApoyoEstrategico(BaseOrg):
    TIPODONATIVO = ( 
        ('FRE','Fondos de Respuesta a Emergencias'),
        ('AEP','Apoyos Estratégicos Puntuales'),
    )
    FRE = (
        ('PDD','Protección a defensoras de derechos humanos'),
        ('APE','Apoyo de emergencia a organizaciones, redes y articulaciones'),
        ('RDN','Respuesta ante desastres naturales'),
        ('CLD','Cambios legislativos que afectan derechos de las mujeres'),
    )
    AEP = (
        ('BEV','Becas para eventos'),
        ('PEP','Proyectos estratégicos puntuales'),
        ('AOC','Apoyo a organizaciones en crisis financiera'),
        ('DOP','Donativos patrocinados'),
    )
    TIPOORG = (
        ('BEV','Grupo o colectivo de base'),
        ('PEP','Organizaciones grandes'),
        ('AOC','INGO/ONG internacional'),
        ('DOP','Grupos intermedios'),
        ('BEV','Redes'),
        ('PEP','Fondos'),
        ('AOC','Defensora de derechos humanos'),
    )
    tipo_donativo = models.CharField('Tipo de donativo', max_length=3, choices=TIPODONATIVO, null=True, blank=True) 
    fondo_resp_emer = models.CharField('Fondos de Respuesta a Emergencias', max_length=3, choices=FRE, null=True, blank=True) 
    apoyos_estra_punt = models.CharField('Apoyos Estratégicos Puntuales', max_length=3, choices=AEP, null=True, blank=True) 
    tipo_org = models.CharField('Tipo de organización', max_length=3, choices=TIPOORG, null=True, blank=True) 
    ano_donativo = models.CharField('Año del donativo', max_length=4, choices=ANO, null=True, blank=True) 
    monto_entregado_USD = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    monto_entregado_EUR = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tipo_de_cambio_EUR_USD = models.DecimalField('Tipo de cambio (EUR -> USD)', max_digits=8, decimal_places=2, default=0)
    programa = models.CharField('Programa', max_length=3, choices=PROGRAMAS, null=True)

    class Meta:
        verbose_name='8. Apoyo Estratégico'
        verbose_name_plural = '8. Apoyos estratégicos'

class IniciativaConjunta(BaseOrg, BaseOrgExt):
    tipo_ic = models.CharField('Tipo de iniciaptiva conjunta', max_length=3, choices=TIPOIC, null=True)
    participa_ic = models.CharField('Iniciativa conjunta en la que participa', max_length=3, choices=PARTICIPAIC, blank=True, null=True)
    programa = models.CharField('Programa', max_length=3, choices=PROGRAMAS, blank=True, null=True)

    def __str__(self):
        return self.codigo_org

    class Meta:
        verbose_name='Iniciativa conjunta'
        verbose_name_plural = '5. Iniciativas conjuntas'    

class PropuestaIC(models.Model):
    codigo_prop_ic = models.CharField('Código de la propuesta IC', max_length=7, null=True)
    ic_vinculada = models.ForeignKey(IniciativaConjunta, on_delete=SET_NULL, null=True, verbose_name='Iniciativa conjunta vinculada')
    ano = models.CharField('Año', max_length=4, choices=ANO, null=True)
    sello_fecha_creacion = models.DateTimeField('Sello fecha de creación', auto_now_add=True, null=True)
    sello_fecha_actualizacion = models.DateTimeField('Sello fecha de actualización', auto_now=True, null=True)

    class Meta:
        verbose_name = 'Propuesta iniciativa conjunta'
        verbose_name_plural = '6. Propuestas iniciativas conjuntas'
    
    def __str__(self):
        return self.codigo_prop_ic

class InformeIC(models.Model):
    codigo_inf_ic = models.CharField('Informe de IC', max_length=25, null=True)
    prop_ic_vincula = models.ForeignKey(PropuestaIC, on_delete=SET_NULL, null=True)
    ic_vinculada = models.ForeignKey(IniciativaConjunta, on_delete=SET_NULL, null=True)
    ano = models.CharField('Año', max_length=4, choices=ANO, null=True)
    sello_fecha_creacion = models.DateTimeField('Sello fecha de creación', auto_now_add=True, null=True)
    sello_fecha_actualizacion = models.DateTimeField('Sello fecha de actualización', auto_now=True, null=True)

    class Meta:
        verbose_name = 'Informe iniciativa conjunta'
        verbose_name_plural = '7. Informes iniciativas conjuntas'

    def __str__(self):
        return self.codigo_inf_ic

class Contacto(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    correo = models.EmailField(blank=True)
    telefono = models.CharField(max_length=60, blank=True)
    cargo = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(default=1)
    vinculado_a = GenericForeignKey()

    def __str__(self):
        return self.nombre

class Grupoactor(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Actor o grupo'
        verbose_name_plural = "Actores o grupos" 
           

class Comment(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL , models.SET_NULL, blank=True, null=True)
    cuerpo= models.TextField('Comentario', null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(default=1)
    vinculado_a = GenericForeignKey()
    
    class Meta:
        ordering = ['fecha']

    def __str__(self):
        return 'Comment {} by {}'.format(self.cuerpo, self.usuario)

'''@receiver(post_save, sender=Coparte)
def send_new_officer_notification_email(sender, instance, created, **kwargs):
    # if a new officer is created, compose and send the email
   
    sendaddress = instance.supervisora.email if instance.supervisora.email else ''
    sendaddress2 = instance.responsable.email if instance.responsable.email else ''

    codigo_org = instance.codigo_org if instance.codigo_org else 'Error en el código'   
    
    subject = 'Se ha actualizado la ficha de coparte: {0}'.format(codigo_org)
    message = 'Se ha actualizado la ficha de coparte'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [sendaddress, sendaddress2]
    send_mail( subject, message, email_from, recipient_list )'''  