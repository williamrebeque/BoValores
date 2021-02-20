from django.urls import path, include
from . import views

urlpatterns = [
	path('', include('django.contrib.auth.urls')),

	path('home/', views.home, name='home'),
	path('ativo/', views.ativo, name='ativo'),
]