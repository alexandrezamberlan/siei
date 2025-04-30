from __future__ import unicode_literals
from django.urls import path

from core.views import HomeRedirectView

from .views import (DadosMembroUpdateView,
                    EventoListView,  # InscricaoListView, InscricaoCreateView, InscricaoDeleteView,
                    HomeView, AboutView,
                    SubmissaoListView, SubmissaoCreateView, SubmissaoUpdateView, MinhaAvaliacaoListView,
                    SubmissaoDeleteView,
                    MinhaAvaliacaoResponsavelUpdateView, MinhaAvaliacaoSuplenteUpdateView,
                    MinhaAvaliacaoConvidadoUpdateView, AvaliacaoDetailView)

urlpatterns = [
   path('home', HomeView.as_view(), name='appmembro_home'), 
   # path('', HomeRedirectView.as_view(), name='home_redirect'),
   path('about', AboutView.as_view(), name='appmembro_about'),
   path('eventos/', EventoListView.as_view(), name='appmembro_evento_list'),

   path('meus-dados/', DadosMembroUpdateView.as_view(), name='appmembro_dados_update'),

   path('minhas-submissoes', SubmissaoListView.as_view(), name='appmembro_submissao_list'),
   path('minhas-submissoes/cad/', SubmissaoCreateView.as_view(), name='appmembro_submissao_create'),
   # path('minhas-submissoes/pendente/<slug:slug>/', SubmissaoPendenteUpdateView.as_view(), name='appmembro_submissao_pendente_update'),
   # path('minhas-submissoes/aprovado/<slug:slug>/', SubmissaoAprovadoUpdateView.as_view(), name='appmembro_submissao_aprovado_update'),
   path('minhas-submissoes/<slug:slug>/', SubmissaoUpdateView.as_view(), name='appmembro_submissao_update'),
   path('minhas-submissoes/<slug:slug>/delete/', SubmissaoDeleteView.as_view(), name='appmembro_submissao_delete'),
   path('minhas-submissoes/<slug:slug>/detail/', AvaliacaoDetailView.as_view(), name='appmembro_avaliacao_detail'),

   path('minhas-avaliacoes', MinhaAvaliacaoListView.as_view(), name='appmembro_minha_avaliacao_list'),

   path('minhas-avaliacoes/avaliacao/<slug:slug>/responsavel/', MinhaAvaliacaoResponsavelUpdateView.as_view(), name='appmembro_minha_avaliacao_responsavel'),
   path('minhas-avaliacoes/avaliacao/<slug:slug>/suplente/', MinhaAvaliacaoSuplenteUpdateView.as_view(), name='appmembro_minha_avaliacao_suplente'),
   path('minhas-avaliacoes-convidado/<slug:slug>/convidado/', MinhaAvaliacaoConvidadoUpdateView.as_view(), name='appmembro_minha_avaliacao_convidado'),
]
