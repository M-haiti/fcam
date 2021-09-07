from django.contrib.admin import widgets
from django.db import models
from django.db.models.deletion import SET_NULL
#para meter contactoinline en admin.py se debe importar Contacto en este 
from programa.models import ApoyoEstrategico, Contacto, Coparte, IniciativaConjunta, PARTICIPAIC, PROGRAMAS, TIPOIC, Propuesta

#Generic Foreign Key
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

#from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from django.contrib.admin.widgets import AdminDateWidget

# Create your models here.
class Base(models.Model):
    codigo = models.CharField(max_length=255, null=True, unique=True)

    class Meta:
        abstract: True
    
    def __str__(self):
        return self.codigo

class DistribucionIngresoPrograma(models.Model):
    monto = models.DecimalField('Monto', max_digits=8, decimal_places=2, default=0)
    programa = models.CharField('Programa', max_length=3, choices=PROGRAMAS, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey()
    ingreso = GenericRelation('Ingreso' ,content_type_field='content_type', object_id_field='object_id', related_query_name='ingresodistic', blank=True)
    #ingreso_vinculado = GenericRelation()
    ##ingreso_vinculado = GenericRelation('Ingreso' ,content_type_field='content_type', object_id_field='object_id', blank=True)


    class Meta:
        abstract: True

class DistribucionIngresoApoyoEstrategico(models.Model):
    monto = models.DecimalField('Monto', max_digits=8, decimal_places=2, default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey()
    
    class Meta:
        abstract: True

class DistribucionIngresoIC(models.Model):
    monto = models.DecimalField('Monto', max_digits=8, decimal_places=2, default=0)
    ic = models.CharField('Iniciativa conjunta', max_length=3, choices=TIPOIC, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey()
   
    class Meta:
        abstract: True

class Donante(Base):
    TIPO = (
        ('IDV','Donante individual'),
        ('IFM','Donante institucional - Fondo de mujeres'),
        ('IFP','Donante institucional - Fundación privada'),
        ('IIB','Donante institucional - Institución bilateral'),
        ('IIM','Donante institucional - Institución multilateral'),
        ('IOG','Donante institucional - ONG'),
        ('CEP','Donante corporativo - Empresa privada'),
        ('CGR','Donante corporativo - Gremio'),
        ('COT','Donante corporativo - Otro'),
    )
    ESTATUS = ( 
        ('ACT', 'Actual'),
        ('PAS', 'Pasado'),
        ('POT', 'Potencial'),
    )
    nombre = models.CharField(max_length=255, null=True)
    tipo = models.CharField(max_length=3, choices=TIPO, null=True)
    fecha_init_fcam = models.DateField('Fecha que empezó su relación con el FCAM', null=True, blank=True)
    estatus = models.CharField(max_length=3, choices=ESTATUS, null=True, blank=True)
    pais = models.CharField('País de origen', max_length=255, null=True, blank=True)
    direccion = models.TextField('Dirección', null=True, blank=True)
    sitio_web = models.URLField('Sitio web', null=True, blank=True)
    descripcion = models.TextField('Descripción', null=True, blank=True)
    comentarios = models.TextField('Comentarios', null=True, blank=True)


class Ingreso(Base):
    TIPO = (
        ('SPG','Soporte general'),
        ('PRO','Proyecto'),
        ('ICG',' Iniciativa Conjunta Soporte General'),
        ('ICP','Iniciativa Conjunta Proyecto'),
    )
    MECANISMO = (
        ('CAM','Campaña'),
        ('DES','Donación en especie'),
        ('PAT','Patrocinio fiscal'),
        ('DLR','Donación en línea regular'),
        ('DLP','Donación en línea puntual'),
        ('DEF','Donación en efectivo'),
        ('OTR','Otros')
    )
    donante_fuente = models.ForeignKey(Donante, on_delete=SET_NULL, null=True)
    nombre = models.CharField('Nombre del proyecto', max_length=255, null=True, blank=True)
    tipo =  models.CharField(max_length=3, choices=TIPO, null=True, blank=True)
    ic_apoya =  models.CharField(max_length=3, choices=PARTICIPAIC, null=True, blank=True)
    mecanismo =  models.CharField(max_length=3, choices=MECANISMO, null=True, blank=True)
    fecha_ingreso = models.DateField('Fecha del ingreso', null=True, blank=True)
    fecha_init = models.DateField('Fecha del inicio', null=True, blank=True)
    fecha_finit = models.DateField('Fecha de finalización', null=True, blank=True)
    monto_total_USD = models.DecimalField('Monto total USD', max_digits=8, decimal_places=2, default=0, blank=True)
    monto_total_EUR = models.DecimalField('Monto total USD', max_digits=8, decimal_places=2, default=0, blank=True)
    tipo_de_cambio_EUR_USD = models.DecimalField('Tipo de cambio (EUR -> USD)', max_digits=8, decimal_places=2, default=0, blank=True)
    monto_total_USD = models.DecimalField('Monto total para Propuestas', max_digits=8, decimal_places=2, default=0, blank=True)
    monto_total_USD = models.DecimalField('Monto total para Apoyos estratégicos', max_digits=8, decimal_places=2, default=0, blank=True)
    monto_total_USD = models.DecimalField('Monto total para Iniciativas conjuntas', max_digits=8, decimal_places=2, default=0, blank=True)

class Desembolso(Base):
    TIPOORG = (
        ('COP','Coparte'),
        ('APE','Apoyo estratégico'),
        ('ICJ','Iniciativa conjunta'),
    )
    ESTATUS = ( 
        ('REA', 'Realizado'),
        ('PEN', 'Pendiente'),
        ('ANU', 'Anulado'),
    )
    fecha_proyectada = models.DateField('Fecha proyectada de desembolso', null=True, blank=True)
    fecha_desembolso = models.DateField('Fecha de desembolso', null=True)
    tipo_org = models.CharField(max_length=3, choices=TIPOORG, null=True, blank=True)
    propuesta = models.ForeignKey(Propuesta, on_delete=SET_NULL, null=True, blank=True)
    apoyo_estrategico  = models.ForeignKey(ApoyoEstrategico, on_delete=SET_NULL, null=True, blank=True)
    iniciativa_conjunta = models.ForeignKey(IniciativaConjunta, on_delete=SET_NULL, null=True, blank=True)
    numero_desembolso = models.PositiveIntegerField(null=True, blank=True)
    total_desembolsos = models.PositiveIntegerField(null=True, blank=True)
    ingreso_vinculado = models.ForeignKey(Ingreso, on_delete=SET_NULL, null=True, blank=True)
    estatus = models.CharField(max_length=3, choices=ESTATUS, null=True, blank=True)
    monto_total_USD = models.DecimalField('Monto total USD', max_digits=8, decimal_places=2, default=0, blank=True)
    monto_total_EUR = models.DecimalField('Monto total EUR', max_digits=8, decimal_places=2, default=0, blank=True)
    tipo_de_cambio_EUR_USD = models.DecimalField('Tipo de cambio (EUR -> USD)', max_digits=8, decimal_places=2, default=0, blank=True)
    descripcion = models.TextField('Descripción', null=True, blank=True)
    numero_comprobante = models.CharField(max_length=255, null=True, blank=True)