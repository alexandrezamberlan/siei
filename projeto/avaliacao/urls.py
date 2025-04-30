from django.urls import path

from .views import AvaliacaoListView, AvaliacaoAndamentoListView, MinhaAvaliacaoListView, AvaliacaoMinhaCoordenacaoListView
from .views import AvaliacaoUpdateView, AvaliacaoDeleteView, AvaliacaoCreateView, AvaliacaoDetailView, AvaliacaoImpressaoListView
from .views import AvaliacaoMinhasAndamentoListView
from .views import MinhaAvaliacaoResponsavelUpdateView, MinhaAvaliacaoSuplenteUpdateView

urlpatterns = [
    path('<slug:slug>/avaliacao-parecer-liberado/', AvaliacaoDetailView.as_view(), name='avaliacao_parecer_detail'),
	path('list/', AvaliacaoListView.as_view(), name='avaliacao_list'),
 	path('avaliacao-minhas-andamento/', AvaliacaoMinhasAndamentoListView.as_view(), name='avaliacao_minhas_andamento_list'),
	path('avaliacao-andamento/', AvaliacaoAndamentoListView.as_view(), name='avaliacao_andamento_list'),
	
  	path('avaliacao-minha-coordenacao/', AvaliacaoMinhaCoordenacaoListView.as_view(), name='avaliacao_minha_coordenacao_list'),
	path('impressao/', AvaliacaoImpressaoListView.as_view(), name='impressao_avaliacao_list'),
 	path('minha-avaliacao/', MinhaAvaliacaoListView.as_view(), name='minha_avaliacao_list'),
	path('cad/', AvaliacaoCreateView.as_view(), name='avaliacao_create'),
	path('<slug:slug>/', AvaliacaoUpdateView.as_view(), name='avaliacao_update'),

	path('minhas-avaliacoes/avaliacao/<slug:slug>/responsavel/', MinhaAvaliacaoResponsavelUpdateView.as_view(),
		 name='minha_avaliacao_responsavel'),
	path('minhas-avaliacoes/avaliacao/<slug:slug>/suplente/', MinhaAvaliacaoSuplenteUpdateView.as_view(),
		 name='minha_avaliacao_suplente'),

	path('<slug:slug>/delete/', AvaliacaoDeleteView.as_view(), name='avaliacao_delete'),	
 	# path('<slug:slug>/pdf/', AvaliacaoPdfView.as_view(), name='avaliacao_pdf'),
]
