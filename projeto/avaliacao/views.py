from __future__ import unicode_literals

from datetime import datetime, timezone

from django import forms
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView

from django.views.generic.edit import CreateView, UpdateView, DeleteView

# from easy_pdf.views import PDFTemplateResponseMixin

from utils.decorators import LoginRequiredMixin, CoordenadorRequiredMixin

from .models import Avaliacao

from .forms import AvaliacaoForm, BuscaAvaliacaoForm

from appmembro.forms import MinhaAvaliacaoResponsavelForm, MinhaAvaliacaoSuplenteForm, MinhaAvaliacaoConvidadoForm

from submissao.models import Submissao

from appmembro.forms import BuscaMinhasAvaliacoesForm


class AvaliacaoListView(LoginRequiredMixin, CoordenadorRequiredMixin, ListView):
    model = Avaliacao
    template_name = 'avaliacao/avaliacao_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dado filtrando
            context['form'] = BuscaAvaliacaoForm(data=self.request.GET)
        else:
            #quando acessa sem dado filtrando
            context['form'] = BuscaAvaliacaoForm()
        return context
    
    def get_queryset(self):
        qs = Avaliacao.objects.all()
        if self.request.GET:
            #quando ja tem dado filtrando
            form = BuscaAvaliacaoForm(data=self.request.GET)
        else:
            #quando acessa sem dado filtrando
            form = BuscaAvaliacaoForm()
            
        if form.is_valid():
            autor = form.cleaned_data.get('autor')
            evento = form.cleaned_data.get('evento')
            nome_avaliador = form.cleaned_data.get('nome_avaliador')

            if autor:
                qs = qs.filter(submissao__responsavel__nome__icontains=autor)
                
            if evento:
                qs = qs.filter(submissao__evento=evento) 

            if nome_avaliador:
                qs = qs.filter(Q(avaliador_responsavel__nome__icontains=nome_avaliador) | Q(avaliador_suplente__nome__icontains=nome_avaliador) | Q(avaliador_convidado__nome__icontains=nome_avaliador))
                
        return qs


class AvaliacaoAndamentoListView(LoginRequiredMixin, CoordenadorRequiredMixin, ListView):
    model = Avaliacao
    template_name = 'avaliacao/avaliacao_andamento_list.html' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dado filtrando
            context['form'] = BuscaAvaliacaoForm(data=self.request.GET)
        else:
            #quando acessa sem dado filtrando
            context['form'] = BuscaAvaliacaoForm()
        return context

    def get_queryset(self):
        # qs = Avaliacao.objects.all()
        qs = Avaliacao.objects.all().filter(submissao__status = 'EM ANDAMENTO')

        if self.request.GET:
            #quando ja tem dado filtrando
            form = BuscaAvaliacaoForm(data=self.request.GET)
        else:
            #quando acessa sem dado filtrando
            form = BuscaAvaliacaoForm()

        if form.is_valid():
            autor = form.cleaned_data.get('autor')
            evento = form.cleaned_data.get('evento')
            nome_avaliador = form.cleaned_data.get('nome_avaliador')
            
            if autor:
                qs = qs.filter(submissao__responsavel__nome__icontains=autor)

            if evento:
                qs = qs.filter(submissao__evento=evento)
    
            if nome_avaliador:				
                qs = qs.filter(Q(avaliador_responsavel__nome__icontains=nome_avaliador) | Q(avaliador_suplente__nome__icontains=nome_avaliador) | Q(avaliador_convidado__nome__icontains=nome_avaliador))

        return qs


class AvaliacaoMinhasAndamentoListView(LoginRequiredMixin, ListView):
    model = Avaliacao
    template_name = 'avaliacao/avaliacao_andamento_minhas_list.html' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dado filtrando
            context['form'] = BuscaAvaliacaoForm(data=self.request.GET)
        else:
            #quando acessa sem dado filtrando
            context['form'] = BuscaAvaliacaoForm()
        return context

    def get_queryset(self):
        # qs = Avaliacao.objects.all()
        qs = Avaliacao.objects.all().filter(Q(submissao__status = 'EM ANDAMENTO'))
        qs = qs.filter(Q(submissao__avaliacao__avaliador_responsavel = self.request.user) | Q(submissao__avaliacao__avaliador_suplente = self.request.user) | Q(submissao__orientador = self.request.user))

        
        if self.request.GET:
            #quando ja tem dado filtrando
            form = BuscaAvaliacaoForm(data=self.request.GET)
        else:
            #quando acessa sem dado filtrando
            form = BuscaAvaliacaoForm()

        if form.is_valid():
            autor = form.cleaned_data.get('autor')
            evento = form.cleaned_data.get('evento')
            nome_avaliador = form.cleaned_data.get('nome_avaliador')
            
            if autor:
                qs = qs.filter(submissao__responsavel__nome__icontains=autor)

            if evento:
                qs = qs.filter(submissao__evento=evento)
    
            if nome_avaliador:				
                qs = qs.filter(Q(avaliador_responsavel__nome__icontains=nome_avaliador) | Q(avaliador_suplente__nome__icontains=nome_avaliador) | Q(avaliador_convidado__nome__icontains=nome_avaliador))

        return qs



class AvaliacaoImpressaoListView(LoginRequiredMixin, CoordenadorRequiredMixin, ListView):
    model = Avaliacao   
    template_name = 'avaliacao/impressao_avaliacao_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dado filtrando
            context['form'] = BuscaAvaliacaoForm(data=self.request.GET)
        else:
            #quando acessa sem dado filtrando
            context['form'] = BuscaAvaliacaoForm()
        return context
    
    def get_queryset(self):
        qs = Avaliacao.objects.all().filter(submissao__status='FINALIZADO')
        if self.request.GET:
            #quando ja tem dado filtrando
            form = BuscaAvaliacaoForm(data=self.request.GET)
        else:
            #quando acessa sem dado filtrando
            form = BuscaAvaliacaoForm()
            
        if form.is_valid():
            autor = form.cleaned_data.get('autor')
            evento = form.cleaned_data.get('evento')
            nome_avaliador = form.cleaned_data.get('nome_avaliador')
            
            if autor:
                qs = qs.filter(submissao__responsavel__nome__icontains=autor)

            if evento:
                qs = qs.filter(submissao__evento=evento)
    
            if nome_avaliador:				
                qs = qs.filter(Q(avaliador_responsavel__nome__icontains=nome_avaliador) | Q(avaliador_suplente__nome__icontains=nome_avaliador) | Q(avaliador_convidado__nome__icontains=nome_avaliador))

        return qs
    
    
class MinhaAvaliacaoListView(LoginRequiredMixin, CoordenadorRequiredMixin, ListView):
    model = Avaliacao
    template_name = 'avaliacao/minha_avaliacao_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            # quando ja tem dado filtrando
            context['form'] = BuscaMinhasAvaliacoesForm(data=self.request.GET)
        else:
            # quando acessa sem dado filtrando
            context['form'] = BuscaMinhasAvaliacoesForm()
        return context

    def get_queryset(self):
        qs = super(MinhaAvaliacaoListView, self).get_queryset()
        qs = qs.filter(Q(avaliador_responsavel=self.request.user) | Q(avaliador_suplente=self.request.user) | Q(
            avaliador_convidado=self.request.user))

        if self.request.GET:
            # quando ja tem dado filtrando
            form = BuscaMinhasAvaliacoesForm(data=self.request.GET)
        else:
            # quando acessa sem dado filtrando
            # qs = qs.filter(submissao__status = 'EM ANDAMENTO')
            form = BuscaMinhasAvaliacoesForm()

        if form.is_valid():
            evento = form.cleaned_data.get('evento')

            if evento:
                qs = qs.filter(submissao__evento=evento)

        return qs


class AvaliacaoMinhaCoordenacaoListView(LoginRequiredMixin, CoordenadorRequiredMixin, ListView):
    model = Avaliacao
    template_name = 'avaliacao/avaliacao_andamento_list.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        return qs.filter(submissao__evento__coordenador=self.request.user)


class AvaliacaoCreateView(LoginRequiredMixin, CoordenadorRequiredMixin, CreateView):
	model = Avaliacao
	form_class = AvaliacaoForm
	success_url = 'submissao_list'

	def get_initial(self):
		initials = super().get_initial()
		initials['submissao'] = Submissao.objects.get(id=self.request.GET.get('submissao_id'))
		return initials

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['submissao'] = Submissao.objects.get(id=self.request.GET.get('submissao_id'))
		return context

	def get_success_url(self):
		messages.success(self.request, 'Instância de avaliação criada com sucesso!!')
		return reverse(self.success_url)


class AvaliacaoUpdateView(LoginRequiredMixin, CoordenadorRequiredMixin, UpdateView):
	model = Avaliacao
	form_class = AvaliacaoForm
	success_url = 'avaliacao_list'
 
	def form_valid(self, form):
    	#Grava a data avaliação do coordenador ou como orientador, ou como resposavel, ou como suplente
		
		avaliacao = form.save(commit=False)
		# print('usuario logado: ', self.request.user)
		# print('parecer orientador: ', avaliacao.dt_avaliacao_orientador)
		# print('parecer responsavel: ', avaliacao.dt_avaliacao_responsavel)
		# print('parecer suplente: ', avaliacao.dt_avaliacao_suplente)
  
		if (self.request.user == avaliacao.avaliador_responsavel):
			avaliacao.dt_avaliacao_responsavel = timezone.now()
		elif (self.request.user == avaliacao.avaliador_suplente):
			avaliacao.dt_avaliacao_suplente = timezone.now()
   
		if avaliacao.dt_avaliacao_responsavel or avaliacao.dt_avaliacao_suplente:
			avaliacao.parecer_liberado = 'SIM'

		avaliacao.save()
		return super().form_valid(form)
  		# return super(AvaliacaoForm, self).form_valid(form)

	def get_success_url(self):
		messages.success(self.request, 'Avaliação atualizada com sucesso!!')
		return reverse(self.success_url)


class MinhaAvaliacaoResponsavelUpdateView(LoginRequiredMixin, CoordenadorRequiredMixin, UpdateView):
    model = Avaliacao
    form_class = MinhaAvaliacaoResponsavelForm
    template_name = 'avaliacao/minha_avaliacao_responsavel_form.html'
    success_url = 'avaliacao_minhas_andamento_list'
    
    def get_object(self, queryset=None):
        #Não deixa entrar no formulário de avaliação se ele não foi designado como 
        #avaliador responsável
        pk = self.kwargs.get('pk')
        try:
            obj = Avaliacao.objects.get(pk=pk, avaliador_responsavel=self.request.user)
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


class MinhaAvaliacaoSuplenteUpdateView(LoginRequiredMixin, CoordenadorRequiredMixin, UpdateView):
    model = Avaliacao
    form_class = MinhaAvaliacaoSuplenteForm
    template_name = 'avaliacao/minha_avaliacao_suplente_form.html'
    success_url = 'avaliacao_minhas_andamento_list'

    def get_object(self, queryset=None):
        #Não deixa entrar no formulário de avaliação se ele não foi designado como 
        #avaliador suplente
        pk = self.kwargs.get('pk')
        try:
            obj = Avaliacao.objects.get(pk=pk, avaliador_suplente=self.request.user)
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

class MinhaAvaliacaoConvidadoUpdateView(LoginRequiredMixin, CoordenadorRequiredMixin, UpdateView):
    model = Avaliacao
    form_class = MinhaAvaliacaoConvidadoForm
    template_name = 'avaliacao/minha_avaliacao_convidado_form.html'
    success_url = 'avaliacao_minhas_andamento_list'

    def get_object(self, queryset=None):
        #Não deixa entrar no formulário de avaliação se ele não foi designado como 
        #avaliador suplente
        pk = self.kwargs.get('pk')
        try:
            obj = Avaliacao.objects.get(pk=pk, avaliador_suplente=self.request.user)
        except:
            raise Http404("Você não foi designado como avaliador convidado para esta submissão")
        return obj

    def form_valid(self, form):
        #Grava a data avaliação do suplente
        avaliacao = form.save()
        avaliacao.dt_avaliacao_suplente = timezone.now()
        avaliacao.parecer_liberado = 'SIM'
        avaliacao.save()
        return super(MinhaAvaliacaoSuplenteUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Seu parecer como avaliador convidado foi enviado com sucesso!')
        return reverse(self.success_url)


class AvaliacaoDeleteView(LoginRequiredMixin, CoordenadorRequiredMixin, DeleteView):
    model = Avaliacao
    success_url = 'avaliacao_list'
 
    def get_success_url(self):
        messages.success(self.request, 'Avaliação excluída com sucesso!')
        return reverse(self.success_url)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, 'Avaliação excluída com sucesso!') 
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à essa avaliação, permissão negada!')
        return redirect(self.success_url)


class AvaliacaoDetailView(LoginRequiredMixin, DetailView):
    model = Avaliacao
    template_name = 'avaliacao/avaliacao_parecer_detail.html'
    success_url = 'avaliacao_andamento_list'
    
    
# class AvaliacaoPdfView(LoginRequiredMixin, PDFTemplateResponseMixin, DetailView):
#     model = Avaliacao
#     template_name = 'avaliacao/impressoes/avaliacao_pdf.html'


class MinhaAvaliacaoResponsavelUpdateView(LoginRequiredMixin, CoordenadorRequiredMixin, UpdateView):
    model = Avaliacao
    form_class = MinhaAvaliacaoResponsavelForm
    template_name = 'avaliacao/minha_avaliacao_responsavel_form.html'
    success_url = 'minha_avaliacao_list'

    def get_object(self, queryset=None):
        # Não deixa entrar no formulário de avaliação se ele não foi designado como
        # avaliador responsável
        slug = self.kwargs.get('slug')
        try:
            obj = Avaliacao.objects.get(slug=slug, avaliador_responsavel=self.request.user)
        except:
            raise Http404("Você não foi designado como avaliador para esta submissão")

        return obj

    def form_valid(self, form):
        # Grava a data avaliação do responsável
        avaliacao = form.save()
        avaliacao.dt_avaliacao_responsavel = timezone.now()
        avaliacao.parecer_liberado = 'SIM'
        avaliacao.save()
        return super(MinhaAvaliacaoResponsavelUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Seu parecer como avaliador 1 foi enviado com sucesso!')
        return reverse(self.success_url)


class MinhaAvaliacaoSuplenteUpdateView(LoginRequiredMixin, CoordenadorRequiredMixin, UpdateView):
    model = Avaliacao
    form_class = MinhaAvaliacaoSuplenteForm
    template_name = 'avaliacao/minha_avaliacao_suplente_form.html'
    success_url = 'minha_avaliacao_list'

    def get_object(self, queryset=None):
        # Não deixa entrar no formulário de avaliação se ele não foi designado como
        # avaliador suplente
        slug = self.kwargs.get('slug')
        try:
            obj = Avaliacao.objects.get(slug=slug, avaliador_suplente=self.request.user)
        except:
            raise Http404("Você não foi designado como avaliador suplente para esta submissão")
        return obj

    def form_valid(self, form):
        # Grava a data avaliação do suplente
        avaliacao = form.save()
        avaliacao.dt_avaliacao_suplente = timezone.now()
        avaliacao.parecer_liberado = 'SIM'
        avaliacao.save()
        return super(MinhaAvaliacaoSuplenteUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Seu parecer como avaliador 2 foi enviado com sucesso!')
        return reverse(self.success_url)
