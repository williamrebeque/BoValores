from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from gerenciamento.models import Ativo, AtivoHistorico
from gerenciamento.forms import AtivoAlterarForm

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

class AtivoCreate(LoginRequiredMixin, CreateView):
	model = Ativo 
	fields = ['cod_b3', 'lim_sup', 'lim_inf']
	success_url = '/bovalores/home/'

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.usuario = self.request.user
		self.object.save()

		return HttpResponseRedirect(self.get_success_url())

class AtivoUpdate(LoginRequiredMixin, UpdateView):
	model = Ativo
	fields = ['cod_b3', 'lim_sup', 'lim_inf']
	success_url = '/bovalores/home/'

	def get_object(self, *args, **kwargs):
		ativo = super(AtivoUpdate, self).get_object(*args, **kwargs)
		if not ativo.usuario == self.request.user:
			raise Http404
		return ativo

class AtivoDelete(LoginRequiredMixin, DeleteView):
	model = Ativo 
	success_url = '/bovalores/home/'

	def get_object(self, *args, **kwargs):
		ativo = super(AtivoDelete, self).get_object(*args, **kwargs)
		if not ativo.usuario == self.request.user:
			raise Http404
		return ativo

def real_br_money_mask(my_value):
	a = '{:,.2f}'.format(float(my_value))
	b = a.replace(',','v')
	c = b.replace('.',',')
	return c.replace('v','.')

def real_us_money_mask(my_value):
	a = str(my_value)
	b = a.replace(',', 'v')
	c = b.replace('.', '')
	return float(c.replace('v', '.'))
