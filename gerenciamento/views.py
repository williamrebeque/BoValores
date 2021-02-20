from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from gerenciamento.models import Ativo, AtivoHistorico

# Create your views here.

def login(request):
	return render(request, 'login.html')

@login_required
def home(request):

	ativos = Ativo.objects.filter(usuario_id=request.user)

	cont = 0
	for ativo in ativos:
		ativos[cont].lim_sup = real_br_money_mask(ativo.lim_sup)
		ativos[cont].lim_inf = real_br_money_mask(ativo.lim_inf)

		ultimo_hist = AtivoHistorico.objects.filter(ativo_id=ativo.id).order_by('-data')[:1]
		if ultimo_hist:
			ativos[cont].ultimo_hist = real_br_money_mask(ultimo_hist[0].valor)

		cont = cont + 1
	
	context = {
		'ativos': ativos
	}

	return render(request, 'home.html', context=context)

@login_required
def ativo(request):
	return render(request, 'ativo.html')

def real_br_money_mask(my_value):
    a = '{:,.2f}'.format(float(my_value))
    b = a.replace(',','v')
    c = b.replace('.',',')
    return c.replace('v','.')