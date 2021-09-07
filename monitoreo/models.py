from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from programa.models  import Coparte

ANO = (
        ('2021','2021'),
        ('2022','2022'),
        ('2023','2023'),
        ('2024','2024'),
        ('2025','2025')
)
# Create your models here.
class Monitoreo(models.Model):
    codigo = models.CharField('Código',max_length=255, null=True)
    coparte = models.ForeignKey(Coparte, on_delete=SET_NULL, null=True)
    ano = models.CharField('Año', max_length=4, choices=ANO, null=True)

class AutoevaluacionCoparte(models.Model):
    codigo = models.CharField('Código',max_length=255, null=True)
    coparte = models.ForeignKey(Coparte, on_delete=SET_NULL, null=True)
    ano = models.CharField('Año', max_length=4, choices=ANO, null=True)