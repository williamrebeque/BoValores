from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class AtivoAlterarForm(forms.Form):
	codigob3 = forms.CharField(
		label='Código B3',
		help_text='Digite o código da B3 para o ativo que deseja monitorar'
	)
	lim_superior = forms.FloatField(
		label='Limite Superior',
	)
	lim_inferior = forms.FloatField(
		label='Limite Inferior',
	)

	def clean_lim_superior(self):
		valor = self.cleaned_data['lim_superior']
		print("valor lim_superior cleaned", valor)

		valor = str(valor)
		valor = float(valor.replace(',', '.'))

		# valor = real_us_money_mask(valor)

		return valor 

	def clean_lim_inferior(self):
		valor = self.cleaned_data['lim_inferior']
		print("valor lim_inferior cleaned", valor)

		valor = str(valor)
		valor = float(valor.replace(',', '.'))

		# valor = real_us_money_mask(valor)

		return valor 

	def clean_codigob3(self):
		valor = self.cleaned_data['codigob3']

		return str(valor)