from __future__ import unicode_literals

from django.contrib import messages

from django.db.models import Q

from datetime import datetime

from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from django.urls import reverse

from utils.decorators import LoginRequiredMixin, CoordenadorRequiredMixin

from .models import Submissao

from .forms import BuscaSubmissaoForm, SubmissaoForm, SubmissaoCoordenadorForm


class SubmissaoListView(LoginRequiredMixin, ListView):
    model = Submissao
    template_name = 'submissao/submissao_list.html'

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
        qs = super().get_queryset().all()    
        if self.request.user.tipo == 'COORDENADOR' or self.request.user.tipo == 'COORDENADOR_SUPLENTE':  
            qs = qs.filter(Q(evento__coordenador=self.request.user) | Q(evento__coordenador_suplente=self.request.user))  
            #Q(responsavel=self.request.user) |
            
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
    
    
class SubmissaoCreateView(LoginRequiredMixin, CoordenadorRequiredMixin, CreateView):
    model = Submissao
    form_class = SubmissaoForm
    success_url = 'submissao_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Submissão cadastrada com sucesso na plataforma!')
        return reverse(self.success_url)
    
    
class SubmissaoUpdateView(LoginRequiredMixin, CoordenadorRequiredMixin, UpdateView):
    model = Submissao
    form_class = SubmissaoForm
    success_url = 'submissao_coordenador_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Submissão atualizada com sucesso na plataforma!')
        if self.request.user.tipo in ['ADMINISTRADOR', 'COORDENADOR']:
            return reverse('submissao_list')
        return reverse(self.success_url) 
    

class SubmissaoDeleteView(LoginRequiredMixin, CoordenadorRequiredMixin, DeleteView):            
    model = Submissao
    template_name = 'submissao/submissao_confirm_delete.html'
    success_url = 'submissao_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Submissão removida com sucesso na plataforma!')
        return reverse(self.success_url)

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        try:
            self.object = self.get_object()
        
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à essa Submissão, permissão negada!')
        return redirect(self.success_url)


class CoordenadorSubmissaoListView(LoginRequiredMixin, ListView):
    model = Submissao
    template_name = 'submissao/submissao_coordenador_list.html'

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
        qs = super().get_queryset().filter(responsavel=self.request.user)  
        
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


class CoordenadorSubmissaoCreateView(LoginRequiredMixin, CoordenadorRequiredMixin, CreateView):
    model = Submissao
    template_name = 'submissao/submissao_coordenador_form.html'    
    form_class = SubmissaoCoordenadorForm
    success_url = 'submissao_coordenador_list'

    def form_valid(self, form):
        try:
            # messages.warning(self.request, 'PASSEI')
            submissao = form.save(commit=False)
            submissao.responsavel = self.request.user
            submissao.save()
            self.object = submissao
        except Exception as e:
            messages.error(self.request, 'Erro ao submeter o projeto. %s' % e)
        
        return super(CoordenadorSubmissaoCreateView, self).form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Sua submissão foi gravada e enviada com sucesso!')
        return reverse(self.success_url)
    

class CoordenadorSubmissaoUpdateView(LoginRequiredMixin, CoordenadorRequiredMixin, UpdateView):
    model = Submissao
    template_name = 'submissao/submissao_coordenador_form.html'    
    form_class = SubmissaoCoordenadorForm
    success_url = 'submissao_coordenador_list'
    
    def form_valid(self, form):
        try:
            submissao = form.save(commit=False)
            submissao.dt_atualizacao_submissao = datetime.now()
            submissao.save()
            self.object = submissao
        except Exception as e:
            messages.error(self.request, 'Erro ao atualizar o projeto. %s' % e)
        
        return super(CoordenadorSubmissaoUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Sua submissão foi alterada, gravada e enviada com sucesso!')
        return reverse(self.success_url)
    
    
class CoordenadorSubmissaoDeleteView(LoginRequiredMixin, CoordenadorRequiredMixin, DeleteView):            
    model = Submissao
    template_name = 'submissao/submissao_confirm_delete.html'
    success_url = 'submissao_coordenador_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Submissão removida com sucesso na plataforma!')
        return reverse(self.success_url)

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        try:
            self.object = self.get_object()
        
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à essa Submissão, permissão negada!')
        return redirect(self.success_url)