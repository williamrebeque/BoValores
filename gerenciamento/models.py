from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.

class Ativo(models.Model):
	"""Model for Ativo"""
	
	usuario = models.ForeignKey(User, on_delete=models.RESTRICT, null=False)
	cod_b3 = models.CharField(max_length=6, verbose_name='Código B3')
	lim_sup = models.FloatField(verbose_name='Vender em')
	lim_inf = models.FloatField(verbose_name='Comprar em')

	def __str__(self):
		""" Representação em string do ativo """
		return self.cod_b3 

	def get_absolute_url(self):
		""" Url para acessar o ativo diretamente """
		return reverse('ativo-update', args=[str(self.id)])


class AtivoHistorico(models.Model):
	"""Model for AtivoHistorico"""
	
	ativo_id = models.ForeignKey('Ativo', on_delete=models.RESTRICT, null=False)
	valor = models.FloatField()
	data = models.DateTimeField()
	
