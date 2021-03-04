import requests
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from .models import Ativo
from django.contrib.auth.models import User

class AtivoCreateForm(forms.ModelForm):
	def clean_cod_b3(self):
		ativo = self.cleaned_data['cod_b3'].upper()
		response = requests.get('https://api.hgbrasil.com/finance/stock_price?key=10eb2b46&symbol=' + ativo).json()
		print("response", response)
		if 'error' in response['results'][ativo]:
			raise ValidationError(
				mark_safe(_('Ativo indisponível para monitoramento, <a href="https://console.hgbrasil.com/documentation/finance/symbols" target="_blank">verifique a lista completa</a>'))
			)

		return ativo

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

class AtivoUpdateForm(forms.ModelForm):
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
		fields = ['lim_sup', 'lim_inf']

class UserForm(forms.ModelForm):
	def clean_email(self):
		email = self.cleaned_data['email']
		if email == "":
			raise ValidationError(_('Email não pode ficar em branco'))

		return email

	class Meta:
		model = User
		fields = ['email']