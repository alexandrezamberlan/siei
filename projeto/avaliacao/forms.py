from django import forms
from django.db import models

from evento.models import Evento
from usuario.models import Usuario 

from .models import Avaliacao


class AvaliacaoForm(forms.ModelForm):
    avaliador_responsavel = forms.ModelChoiceField(label='Selecione um membro como avaliador 1 *', queryset=Usuario.avaliadores.all(), required=True)
    avaliador_suplente = forms.ModelChoiceField(label='Selecione um membro como avaliador 2 *', queryset=Usuario.avaliadores.all(), required=True)
    # avaliador_convidado = forms.ModelChoiceField(label='Selecione um membro como avaliador 3', queryset=Usuario.avaliadores.all(), required=False)

    
    class Meta:
        model = Avaliacao
        fields = ['submissao', 'avaliador_responsavel', 'avaliador_suplente', 'parecer_liberado', 
                    'parecer_avaliador_responsavel', 'parecer_avaliador_suplente', 'parecer_avaliador_convidado',
                    'parecer_reavaliacao_avaliador_responsavel', 'parecer_reavaliacao_avaliador_suplente', 'parecer_reavaliacao_avaliador_convidado',
                    
                    'merito_relevancia_responsavel','merito_contribuicao_responsavel','merito_metodologia_responsavel',
                    'merito_fundamentacao_responsavel','merito_clareza_responsavel','merito_referencias_responsavel',
                    'merito_resultados_responsavel','merito_conclusao_responsavel',
                    'merito_relevancia_suplente','merito_contribuicao_suplente','merito_metodologia_suplente',
                    'merito_fundamentacao_suplente','merito_clareza_suplente','merito_referencias_suplente',
                    'merito_resultados_suplente','merito_conclusao_suplente',
                    'intercorrencias',
                    
                    
                    
                    'nota_final_responsavel', 'nota_final_suplente', 
                    # 'media_final_avaliacao', 
                    'arquivo_corrigido_responsavel', 'arquivo_corrigido_suplente']
        
                    # avaliador_convidado, 'nota_final_convidado', 'merito_relevancia_convidado','merito_contribuicao_convidado','merito_metodologia_convidado',
                    # 'merito_fundamentacao_convidado','merito_clareza_convidado','merito_referencias_convidado',
                    # 'merito_resultados_convidado','merito_conclusao_convidado', 'arquivo_corrigido_convidado'
                    
    
    def clean_avaliador_convidado(self):
        avaliador_responsavel = self.cleaned_data.get('avaliador_responsavel')
        avaliador_suplente = self.cleaned_data.get('avaliador_suplente')
        avaliador_convidado = self.cleaned_data.get('avaliador_convidado')
        submissao = self.cleaned_data.get('submissao')

        if avaliador_responsavel:
            if (avaliador_convidado == avaliador_responsavel):
                raise forms.ValidationError('Um membro não pode ser ao mesmo tempo mais de um avaliador')

        if avaliador_suplente:
            if (avaliador_convidado == avaliador_suplente):
                raise forms.ValidationError('Um membro não pode ser ao mesmo tempo mais de um avaliador')
            
        if (avaliador_convidado == submissao.responsavel):
            raise forms.ValidationError('Um membro não pode ser ao mesmo tempo avaliador de seu próprio trabalho')
        
        return avaliador_convidado
            
    def clean_avaliador_suplente(self):
        avaliador_responsavel = self.cleaned_data.get('avaliador_responsavel')
        avaliador_suplente = self.cleaned_data.get('avaliador_suplente')
        submissao = self.cleaned_data.get('submissao')

        if avaliador_responsavel:
            if (avaliador_suplente == avaliador_responsavel):
                raise forms.ValidationError('Um membro não pode ser ao mesmo tempo mais de um avaliador')

        if (avaliador_suplente == submissao.responsavel):
            raise forms.ValidationError('Um membro não pode ser ao mesmo tempo avaliador de seu próprio trabalho')

        return avaliador_suplente

    def clean_avaliador_responsavel(self):
        avaliador_responsavel = self.cleaned_data.get('avaliador_responsavel')        
        submissao = self.cleaned_data.get('submissao')
        
        if (avaliador_responsavel == submissao.responsavel):
            raise forms.ValidationError('Um membro não pode ser ao mesmo tempo avaliador de seu próprio trabalho')

        return avaliador_responsavel


class BuscaAvaliacaoForm(forms.Form):
    autor = forms.CharField(label='Nome do autor responsável', required=False)
    evento = forms.ModelChoiceField(label='Evento', queryset=Evento.objects.all(), required=False)
    nome_avaliador = forms.CharField(label='Nome do avaliador', required=False)