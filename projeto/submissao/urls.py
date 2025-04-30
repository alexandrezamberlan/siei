from django.urls import path

from .views import SubmissaoListView, SubmissaoCreateView, SubmissaoUpdateView, SubmissaoDeleteView
from .views import CoordenadorSubmissaoListView, CoordenadorSubmissaoCreateView, CoordenadorSubmissaoUpdateView,CoordenadorSubmissaoDeleteView


urlpatterns = [
	path('list/', SubmissaoListView.as_view(), name='submissao_list'),	
	path('cad/', SubmissaoCreateView.as_view(), name='submissao_create'),
	path('<slug:slug>/', SubmissaoUpdateView.as_view(), name='submissao_update'),
	path('<slug:slug>/delete/', SubmissaoDeleteView.as_view(), name='submissao_delete'), 
	
 	path('coordenador/list', CoordenadorSubmissaoListView.as_view(), name='submissao_coordenador_list'),
	path('coordenador/cad/', CoordenadorSubmissaoCreateView.as_view(), name='submissao_coordenador_create'),
	path('coordenador/<slug:slug>/', CoordenadorSubmissaoUpdateView.as_view(), name='submissao_coordenador_update'),
	path('coordenador/<slug:slug>/delete/', CoordenadorSubmissaoDeleteView.as_view(), name='submissao_coordenador_delete'),
]
 