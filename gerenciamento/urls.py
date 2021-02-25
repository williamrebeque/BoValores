from django.urls import path, include
from . import views

urlpatterns = [
	path('', include('django.contrib.auth.urls')),

	path('home/', views.home, name='home'),
	path('ativo/', views.AtivoCreate.as_view(), name='ativo'),
	path('ativo/<int:pk>/', views.AtivoUpdate.as_view(), name='ativo-update'),
	path('ativo/<int:pk>/delete/', views.AtivoDelete.as_view(), name='ativo-delete'),
]