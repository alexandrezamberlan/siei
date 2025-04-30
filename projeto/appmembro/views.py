from __future__ import unicode_literals

from datetime import timedelta, datetime

from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView

from utils.decorators import LoginRequiredMixin, MembroRequiredMixin

from avaliacao.models import Avaliacao
from aviso.models import Aviso
from evento.models import Evento
from submissao.models import Submissao
from usuario.models import Usuario

from .forms import MinhaAvaliacaoResponsavelForm, MinhaAvaliacaoSuplenteForm, MinhaAvaliacaoConvidadoForm
from .forms import MembroCreateForm, BuscaSubmissaoForm, SubmissaoForm, BuscaMinhasAvaliacoesForm
from evento.forms import BuscaEventoForm
# from inscricao.forms import BuscaInscricaoForm


class HomeView(LoginRequiredMixin, MembroRequiredMixin, TemplateView):
    template_name = 'appmembro/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avisos'] = Aviso.ativos.filter(destinatario__in=[self.request.user.tipo, 'TODOS'])[0:2]
        return context

class AboutView(LoginRequiredMixin, MembroRequiredMixin, TemplateView):
    template_name = 'appmembro/about.html'
    

class DadosMembroUpdateView(LoginRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'appmembro/dados_membro_form.html'
    form_class = MembroCreateForm  
    
    success_url = 'appmembro_home'

    def get_object(self, queryset=None):
        return self.request.user
     
    def get_success_url(self):
        messages.success(self.request, 'Seus dados foram alterados com sucesso!')
        return reverse(self.success_url)

class EventoListView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'appmembro/evento_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaEventoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaEventoForm()
        return context

    def get_queryset(self):                
        qs = super().get_queryset().filter(is_active=True)
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaEventoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaEventoForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(nome__icontains=pesquisa) | Q(coordenador__nome__icontains=pesquisa) | Q(instituicao__nome__icontains=pesquisa) | Q(instituicao__sigla__icontains=pesquisa) | Q(descricao__icontains=pesquisa))   
            
        return qs

class SubmissaoListView(LoginRequiredMixin, MembroRequiredMixin, ListView):
    model = Submissao
    template_name = 'appmembro/submissao_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaSubmissaoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaSubmissaoForm()
        return context

    def get_queryset(self):                
        qs = Submissao.objects.all()
        qs = qs.filter(responsavel = self.request.user)      
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaSubmissaoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaSubmissaoForm()

        if form.is_valid():            
            situacao = form.cleaned_data.get('situacao')            
            pesquisa = form.cleaned_data.get('pesquisa')    
                
            if situacao:
                qs = qs.filter(status=situacao)        
                
            if pesquisa:
                qs = qs.filter(Q(evento__coordenador__nome__icontains=pesquisa) | Q(evento__nome__icontains=pesquisa) | Q(titulo__icontains=pesquisa) | Q(resumo__icontains=pesquisa) | Q(responsavel__nome__icontains=pesquisa))
                
        return qs


class SubmissaoCreateView(LoginRequiredMixin, MembroRequiredMixin, CreateView):
    model = Submissao
    template_name = 'appmembro/submissao_form.html'
    form_class = SubmissaoForm
    success_url = 'appmembro_submissao_list'

    def form_valid(self, form):
        try:
            # messages.warning(self.request, 'PASSEI')
            submissao = form.save(commit=False)
            submissao.responsavel = self.request.user
            submissao.save()
            self.object = submissao
        except Exception as e:
            messages.error(self.request, 'Erro ao submeter o projeto. %s' % e)
        
        return super(SubmissaoCreateView, self).form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Sua submissão foi gravada e enviada com sucesso!')
        return reverse(self.success_url)


class SubmissaoUpdateView(LoginRequiredMixin, MembroRequiredMixin, UpdateView):
    model = Submissao
    template_name = 'appmembro/submissao_form.html'
    form_class = SubmissaoForm
    success_url = 'appmembro_submissao_list'
    
    def form_valid(self, form):
        try:
            submissao = form.save(commit=False)
            submissao.dt_atualizacao_submissao = datetime.now()
            submissao.save()
            self.object = submissao
        except Exception as e:
            messages.error(self.request, 'Erro ao atualizar o projeto. %s' % e)
        
        return super(SubmissaoUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Sua submissão foi alterada, gravada e enviada com sucesso!')
        return reverse(self.success_url)
    
    
class SubmissaoPendenteUpdateView(LoginRequiredMixin, MembroRequiredMixin, UpdateView):
    model = Submissao
    template_name = 'appmembro/submissao_corrigir_form.html'
    fields = ['arquivo_atualizacao_pendencia_projeto']
    success_url = 'appmembro_submissao_list'

    def get_object(self,queryset=None):
        obj = super().get_object(queryset)
        return obj
        
        # if obj.permite_corrigir:
        #     return obj
        # else:
        #     raise Http404()
    
    def get_success_url(self):
        return reverse(self.success_url)
    

class SubmissaoAprovadoUpdateView(LoginRequiredMixin, UpdateView):
    model = Submissao
    fields = ['arquivo_comite_etica', 'arquivo_relatorio_parcial', 'arquivo_relatorio_final', 
              'registros_apos_aprovacao', 'arquivo_emenda1', 'arquivo_emenda2', 'arquivo_emenda3']
    template_name = 'appmembro/submissao_aprovado_form.html'
    success_url = 'appmembro_submissao_list'

    def get_object(self,queryset=None):
        obj = super().get_object(queryset)
        return obj
    
    def form_valid(self, form):
        try:
            submissao = form.save(commit=False)
            submissao.dt_atualizacao_submissao = datetime.now()
            submissao.save()
            self.object = submissao
        except Exception as e:
            messages.error(self.request, 'Erro ao atualizar o projeto. %s' % e)
        
        return super(SubmissaoAprovadoUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse(self.success_url)


class SubmissaoDeleteView(LoginRequiredMixin, MembroRequiredMixin, DeleteView):
    model = Submissao
    template_name = 'appmembro/submissao_confirm_delete.html'
    success_url = 'appmembro_submissao_list'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        # success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(request, 'Sucesso em excluir sua submissão!')
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à essa submissão, permissão negada!')
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        try:
            submissao = Submissao.objects.get(slug=kwargs['slug'])
            if submissao.responsavel != request.user:
                raise Exception('Você não tem permissão para deletar esta submissão!')
        except Exception as e:
            messages.error(request, e)
            return redirect(self.success_url)
        return super(SubmissaoDeleteView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(self.success_url)


class MinhaAvaliacaoListView(LoginRequiredMixin, MembroRequiredMixin, ListView):
    model = Avaliacao
    template_name = 'appmembro/minha_avaliacao_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dado filtrando
            context['form'] = BuscaMinhasAvaliacoesForm(data=self.request.GET)
        else:
            #quando acessa sem dado filtrando
            context['form'] = BuscaMinhasAvaliacoesForm()
        return context
        
    def get_queryset(self):
        qs = super(MinhaAvaliacaoListView, self).get_queryset()
        qs = qs.filter(Q(avaliador_responsavel = self.request.user) | Q(avaliador_suplente = self.request.user) | Q(avaliador_convidado = self.request.user))
        
        if self.request.GET:
            #quando ja tem dado filtrando
            form = BuscaMinhasAvaliacoesForm(data=self.request.GET)
        else:
            #quando acessa sem dado filtrando
            # qs = qs.filter(submissao__status = 'EM ANDAMENTO')
            form = BuscaMinhasAvaliacoesForm()

        if form.is_valid():
            evento = form.cleaned_data.get('evento')
            
            if evento:
                qs = qs.filter(submissao__evento=evento)

        return qs
    
class MinhaAvaliacaoResponsavelUpdateView(LoginRequiredMixin, MembroRequiredMixin, UpdateView):
    model = Avaliacao
    form_class = MinhaAvaliacaoResponsavelForm
    template_name = 'appmembro/minha_avaliacao_responsavel_form.html'
    success_url = 'appmembro_minha_avaliacao_list'
    
    def get_object(self, queryset=None):
        #Não deixa entrar no formulário de avaliação se ele não foi designado como 
        #avaliador responsável
        slug = self.kwargs.get('slug')
        try:
            obj = Avaliacao.objects.get(slug=slug, avaliador_responsavel=self.request.user)
        except:
            raise Http404("Você não foi designado como avaliador para esta submissão")
    
        return obj


    def form_valid(self, form):
        #Grava a data avaliação do responsável
        avaliacao = form.save()
        avaliacao.dt_avaliacao_responsavel = timezone.now()
        avaliacao.parecer_liberado = 'SIM'
        avaliacao.save()
        return super(MinhaAvaliacaoResponsavelUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Seu parecer como avaliador 1 foi enviado com sucesso!')
        return reverse(self.success_url)


class MinhaAvaliacaoSuplenteUpdateView(LoginRequiredMixin, MembroRequiredMixin, UpdateView):
    model = Avaliacao
    form_class = MinhaAvaliacaoSuplenteForm
    template_name = 'appmembro/minha_avaliacao_suplente_form.html'
    success_url = 'appmembro_minha_avaliacao_list'

    def get_object(self, queryset=None):
        #Não deixa entrar no formulário de avaliação se ele não foi designado como 
        #avaliador suplente
        slug = self.kwargs.get('slug')
        try:
            obj = Avaliacao.objects.get(slug=slug, avaliador_suplente=self.request.user)
        except:
            raise Http404("Você não foi designado como avaliador suplente para esta submissão")
        return obj

    def form_valid(self, form):
        #Grava a data avaliação do suplente
        avaliacao = form.save()
        avaliacao.dt_avaliacao_suplente = timezone.now()
        avaliacao.parecer_liberado = 'SIM'
        avaliacao.save()
        return super(MinhaAvaliacaoSuplenteUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Seu parecer como avaliador 2 foi enviado com sucesso!')
        return reverse(self.success_url)
    
    
class MinhaAvaliacaoConvidadoUpdateView(LoginRequiredMixin, MembroRequiredMixin, UpdateView):
    model = Avaliacao
    form_class = MinhaAvaliacaoConvidadoForm
    template_name = 'appmembro/minha_avaliacao_convidado_form.html'
    success_url = 'appmembro_minha_avaliacao_list'

    def get_object(self, queryset=None):
        #Não deixa entrar no formulário de avaliação se ele não foi designado como 
        #avaliador Convidado
        slug = self.kwargs.get('slug')
        try:
            obj = Avaliacao.objects.get(slug=slug, avaliador_convidado=self.request.user)
        except:
            raise Http404("Você não foi designado como avaliador Convidado para esta submissão")
        return obj

    def form_valid(self, form):
        #Grava a data avaliação do Convidado
        avaliacao = form.save()
        avaliacao.dt_avaliacao_convidado = timezone.now()
        avaliacao.save()
        return super(MinhaAvaliacaoConvidadoUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Seu parecer como avaliador convidado foi enviado com sucesso!')
        return reverse(self.success_url)


class AvaliacaoDetailView(LoginRequiredMixin, MembroRequiredMixin, DetailView):
    model = Avaliacao
    template_name = 'appmembro/avaliacao_parecer_detail.html'