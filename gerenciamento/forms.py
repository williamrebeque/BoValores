# from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Ativo
from django.contrib.auth.models import User

class AtivoForm(ModelForm):
	def clean_lim_sup(self):
		valor = self.cleaned_data['lim_sup']
		if (valor <= 0):
			raise ValidationError(_('Limite de venda deve ser maior que 0'))

		return valor 
	
	def clean_lim_inf(self):
		valor = self.cleaned_data['lim_inf']
		if (valor <= 0):
			raise ValidationError(_('Limite de compra deve ser maior que 0'))

		return valor

	class Meta:
		model = Ativo 
		fields = ['cod_b3', 'lim_sup', 'lim_inf']

class UserForm(ModelForm):
	def clean_email(self):
		email = self.cleaned_data['email']
		if email == "":
			raise ValidationError(_('Email não pode ficar em branco'))

		return email

	class Meta:
		model = User
		fields = ['email']