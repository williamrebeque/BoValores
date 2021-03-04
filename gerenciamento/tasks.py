import requests, datetime
from django.contrib.auth.models import User
from .models import Ativo, AtivoHistorico
from django.core.mail import send_mail

# py3 -m smtpd -n -c DebuggingServer localhost:1025

def busca_ativos():
	print("\n\nLOG - " + str(datetime.datetime.now()) )
	ativos = Ativo.objects.all()
	for ativo in ativos:
		response = requests.get('https://api.hgbrasil.com/finance/stock_price?key=10eb2b46&symbol=' + ativo.cod_b3).json()
		print(response)

		usuario = User.objects.get(id=ativo.usuario.id)

		if 'error' not in response['results'][ativo.cod_b3]:
			valor = response['results'][ativo.cod_b3]['price']
			hist = AtivoHistorico()
			hist.ativo_id = ativo
			hist.data = datetime.datetime.now()
			hist.valor = valor
			hist.save()
			print("atualizou historico", ativo.cod_b3)

			if valor >= ativo.lim_sup:
				send_mail(
					'Alerta BoValores - Venda',
					'Valor do ativo ' + ativo.cod_b3 + ' atingiu R$ ' + str(valor) + '! É a hora de VENDER!',
					'informativo@bovalores.com',
					[usuario.email],
					fail_silently=False,
				)
				print("email venda")
			elif valor <= ativo.lim_inf:
				send_mail(
					'Alerta BoValores - Compra',
					'Valor do ativo ' + ativo.cod_b3 + ' atingiu R$ ' + str(valor) + '! É a hora de COMPRAR!',
					'informativo@bovalores.com',
					[usuario.email],
					fail_silently=False,
				)
				print("email compra")

		print(" --------- ")
		print("")