from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import Http404, HttpResponseRedirect

from gerenciamento.models import Ativo, AtivoHistorico
from django.contrib.auth.models import User
from .forms import AtivoCreateForm, AtivoUpdateForm, UserForm

# Create your views here.

def login(request):
	return render(request, 'login.html')

@login_required
def home(request):

	ativos = Ativo.objects.filter(usuario_id=request.user)

	cont = 0
	for ativo in ativos:

		ultimo_hist = AtivoHistorico.objects.filter(ativo_id=ativo.id).order_by('-data')[:1]
		if ultimo_hist:
			ativos[cont].ultimo_hist = ultimo_hist[0].valor

		cont = cont + 1
	
	context = {
		'ativos': ativos
	}

	return render(request, 'home.html', context=context)

class AtivoCreate(LoginRequiredMixin, CreateView):
	model = Ativo
	form_class = AtivoCreateForm
	success_url = '/bovalores/home/'

	def form_valid(self, form):
		form.instance.usuario = self.request.user
		return super().form_valid(form)

class AtivoUpdate(LoginRequiredMixin, UpdateView):
	model = Ativo
	form_class = AtivoUpdateForm
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

@login_required
def ativo_historico(request, pk):
	ativo = Ativo.objects.filter(pk=pk, usuario_id=request.user)[0]
	historico = AtivoHistorico.objects.filter(ativo_id=ativo.id).order_by('-data')[:100]

	context = {
		'ativo': ativo, 
		'historico': historico
	}

	return render(request, 'historico.html', context=context)


class UsuarioUpdate(LoginRequiredMixin, UpdateView):
	model = User
	form_class = UserForm
	success_url = '/bovalores/home/'

	def get_object(self, *args, **kwargs):
		usuario = super(UsuarioUpdate, self).get_object(*args, **kwargs)
		if not usuario == self.request.user:
			raise Http404
		return usuario
