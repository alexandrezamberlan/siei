from django import forms

from django.core.validators import MaxValueValidator, MinValueValidator

from avaliacao.models import Avaliacao
from evento.models import Evento
from submissao.models import Submissao
from usuario.models import Usuario


class MembroCreateForm(forms.ModelForm):
    #(técnico, graduando, graduado, especialista, mestre, doutor)
    TITULACAO = (
        ('TECNICO', 'Técnico'),
        ('GRADUANDO', 'Graduando' ),
        ('GRADUADO', 'Graduado' ),        
        ('ESPECIALISTA', 'Especialista'),
        ('MESTRE', 'Mestre' ),
        ('DOUTOR', 'Doutor' ),        
    )

    #(Ciências Humana, Ciências da Saúde, Ciências Sociais, Ciências Tecnológicas)
    AREA = (
        ('HUMANAS', 'Ciências Humanas'),
        ('SAUDE', 'Ciências da Saúde' ),
        ('SOCIAIS', 'Ciências Sociais' ),        
        ('TECNOLOGICA', 'Ciências Tecnológicas'),        
    )

    nome = forms.CharField(label='Nome completo *', help_text='* Campos obrigatórios',required=True)
    titulacao = forms.ChoiceField(label='Titulação *',choices=TITULACAO, help_text='Selecione a maior titulação', required=False)
    area = forms.ChoiceField(label='Área de pesquisa do usuário *', choices=AREA, help_text='Escolha área de interesse de trabalho',required=True)
    instituicao = forms.CharField(label='Instituição a que pertence *', help_text='Registre a instituição, ou universidade, ou empresa',required=True)
    email = forms.EmailField(label='Email *', help_text='Use o email válido. Será usado para acessar sistema e recuperar senha!',required=True)
    celular = forms.CharField(label='Número celular com DDD *', help_text="Use DDD, por exemplo 55987619832",required=True)
    cpf = forms.CharField(label='CPF *',required=True)    
    
        
    class Meta:
        model = Usuario
        fields = ['nome','titulacao', 'area', 'instituicao', 'email', 'celular', 'cpf']


class SubmissaoForm(forms.ModelForm):
    evento = forms.ModelChoiceField(label='Evento para a submissão *', queryset=Evento.eventos_ativos_data_aberta.all(), required=True)
 
    class Meta:
        model = Submissao
        fields = ['evento', 'titulo', 'resumo' , 'abstract', 'palavras_chave', 'arquivo_sem_autores', 'arquivo_final',
                  'arquivo_comite_etica', 'observacoes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.id:
            del self.fields['evento']

    # def clean_colaborador(self):
    #     colaborador = self.cleaned_data.get('colaborador')
    #     responsavel = self.cleaned_data.get('responsavel')

    #     if (responsavel in colaborador.all()):
    #         raise forms.ValidationError('Um membro não pode ser ao mesmo tempo responsável e colaborador')
    #     return colaborador


class BuscaSubmissaoForm(forms.Form):     
    STATUS = (
        (None, '-----------'),
        ('EM EDICAO', 'Em edição'),
        ('EM AVALICAO', 'Em avaliação'),
        ('EM CORRECAO', 'Em correção' ),        
        ('APROVADO', 'Aprovado' ),
        ('RETIRADO PELO RESPONSAVEL', 'Retirado pelo responsável'),
        ('RETIRADO PELO COORDENADOR', 'Retirado pelo coordenador' ),
        ('REPROVADO', 'Reprovado' ),
        ('FINALIZADO', 'Finalizado')
    )         
    
    situacao = forms.ChoiceField(label='Status da submissão', choices=STATUS, required=False)
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
    
class MinhaAvaliacaoResponsavelForm(forms.ModelForm):
    NOTA = (
        (None, '---------'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    parecer_avaliador_responsavel = forms.CharField(label='Parecer do avaliador (10000 caracteres)', max_length=10000, widget=forms.widgets.Textarea(), help_text='Atenção: se colar seu texto no campo, confira se ele coube no espaço!!')
    parecer_rebanca_avaliador_responsavel = forms.CharField(label='Parecer de rebanca do avaliador (10000 caracteres)', max_length=10000, widget=forms.widgets.Textarea(),  help_text='Atenção: se colar seu texto no campo, confira se ele coube no espaço!!', required=False)
    
    merito_relevancia_responsavel = forms.ChoiceField(label='Relevância: O artigo aborda um problema atual e/ou relevante na área em que foi submetido ao evento?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_contribuicao_responsavel = forms.ChoiceField(label='Contribuição: O trabalho apresenta contribuição para a área em que foi submetido ao evento?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_metodologia_responsavel = forms.ChoiceField(label='Metodologia: O artigo apresenta uma metodologia e a utiliza de forma apropriada para o problema proposto?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_fundamentacao_responsavel = forms.ChoiceField(label='Fundamentação teórica: O artigo baseia-se em teorias, fundamentos e conceitos relevantes na área em que foi submetido ao evento?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_clareza_responsavel = forms.ChoiceField(label='Clareza e organização: O artigo apresenta escrita clara, organizada e coerente?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_referencias_responsavel = forms.ChoiceField(label='Referências bibliográficas: As referências utilizadas no artigo são atualizadas e/ou relevantes? ', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_resultados_responsavel = forms.ChoiceField(label='Resultados e discussões: Os resultados são apresentados e discutidos adequadamente?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_conclusao_responsavel = forms.ChoiceField(label='Conclusões: O trabalho traz considerações finais ou conclusão, apresentando reflexões,  avanços ou soluções ao tema abordado, conforme os objetivos propostos?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    
    #nota_final_responsavel = forms.CharField(label='Final responsavel',help_text='Máximo 10 pontos', required=False)    
    arquivo_corrigido_responsavel = forms.FileField(label='Arquivo do artigo submetido com apontamentos do avaliador',  help_text='Use formato .pdf para enviar seu arquivo corrigido', required=False)
    
    
    class Meta:
        model = Avaliacao
        fields = ['parecer_avaliador_responsavel', 'parecer_rebanca_avaliador_responsavel', 
              'merito_relevancia_responsavel', 'merito_contribuicao_responsavel', 'merito_metodologia_responsavel',
              'merito_fundamentacao_responsavel', 'merito_clareza_responsavel', 'merito_referencias_responsavel',
              'merito_resultados_responsavel', 'merito_conclusao_responsavel', 
              'arquivo_corrigido_responsavel']
                #'nota_final_responsavel'
        
        
class MinhaAvaliacaoSuplenteForm(forms.ModelForm):
    NOTA = (
         (None, '---------'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    parecer_avaliador_suplente = forms.CharField(label='Parecer do avaliador (10000 caracteres)', max_length=10000, widget=forms.widgets.Textarea(), help_text='Atenção: se colar seu texto no campo, confira se ele coube no espaço!!')
    parecer_rebanca_avaliador_suplente = forms.CharField(label='Parecer de rebanca do avaliador (10000 caracteres)', max_length=10000, widget=forms.widgets.Textarea(),  help_text='Atenção: se colar seu texto no campo, confira se ele coube no espaço!!', required=False)
    
    merito_relevancia_suplente = forms.ChoiceField(label='Relevância: O artigo aborda um problema atual e/ou relevante na área em que foi submetido ao evento?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_contribuicao_suplente = forms.ChoiceField(label='Contribuição: O trabalho apresenta contribuição para a área em que foi submetido ao evento?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_metodologia_suplente = forms.ChoiceField(label='Metodologia: O artigo apresenta uma metodologia e a utiliza de forma apropriada para o problema proposto?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_fundamentacao_suplente = forms.ChoiceField(label='Fundamentação teórica: O artigo baseia-se em teorias, fundamentos e conceitos relevantes na área em que foi submetido ao evento?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_clareza_suplente = forms.ChoiceField(label='Clareza e organização: O artigo apresenta escrita clara, organizada e coerente?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_referencias_suplente = forms.ChoiceField(label='Referências bibliográficas: As referências utilizadas no artigo são atualizadas e/ou relevantes? ', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_resultados_suplente = forms.ChoiceField(label='Resultados e discussões: Os resultados são apresentados e discutidos adequadamente?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_conclusao_suplente = forms.ChoiceField(label='Conclusões: O trabalho traz considerações finais ou conclusão, apresentando reflexões,  avanços ou soluções ao tema abordado, conforme os objetivos propostos?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
     
    # nota_final_suplente = forms.CharField(label='Final suplente',help_text='Máximo 10 pontos')    
    arquivo_corrigido_suplente = forms.FileField(label='Arquivo do artigo submetido com apontamentos do avaliador', help_text='Use formato .pdf para enviar seu arquivo corrigido', required=False)
    
    
    class Meta:
        model = Avaliacao
        fields = ['parecer_avaliador_suplente', 'parecer_rebanca_avaliador_suplente', 
              'merito_relevancia_suplente', 'merito_contribuicao_suplente', 'merito_metodologia_suplente',
              'merito_fundamentacao_suplente', 'merito_clareza_suplente', 'merito_referencias_suplente',
              'merito_resultados_suplente', 'merito_conclusao_suplente', 
              'arquivo_corrigido_suplente']
                # 'nota_final_suplente'
        
        
class MinhaAvaliacaoConvidadoForm(forms.ModelForm):
    NOTA = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    parecer_avaliador_convidado = forms.CharField(label='Parecer do avaliador (10000 caracteres)', max_length=10000, widget=forms.widgets.Textarea(), help_text='Atenção: se colar seu texto no campo, confira se ele coube no espaço!!')
    parecer_rebanca_avaliador_convidado = forms.CharField(label='Parecer de rebanca do avaliador (10000 caracteres)', max_length=10000, widget=forms.widgets.Textarea(),  help_text='Atenção: se colar seu texto no campo, confira se ele coube no espaço!!', required=False)
    
    merito_relevancia_convidado = forms.ChoiceField(label='Relevância: O artigo aborda um problema atual e/ou relevante na área em que foi submetido ao evento?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_contribuicao_convidado = forms.ChoiceField(label='Contribuição: O trabalho apresenta contribuição para a área em que foi submetido ao evento?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_metodologia_convidado = forms.ChoiceField(label='Metodologia: O artigo apresenta uma metodologia e a utiliza de forma apropriada para o problema proposto?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_fundamentacao_convidado = forms.ChoiceField(label='Fundamentação teórica: O artigo baseia-se em teorias, fundamentos e conceitos relevantes na área em que foi submetido ao evento?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_clareza_convidado = forms.ChoiceField(label='Clareza e organização: O artigo apresenta escrita clara, organizada e coerente?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_referencias_convidado = forms.ChoiceField(label='Referências bibliográficas: As referências utilizadas no artigo são atualizadas e/ou relevantes? ', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_resultados_convidado = forms.ChoiceField(label='Resultados e discussões: Os resultados são apresentados e discutidos adequadamente?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_conclusao_convidado = forms.ChoiceField(label='Conclusões: O trabalho traz considerações finais ou conclusão, apresentando reflexões,  avanços ou soluções ao tema abordado, conforme os objetivos propostos?', choices=NOTA, help_text='De 0 a 5. Nota 0 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    
    nota_final_convidado = forms.CharField(label='Final convidado',help_text='Máximo 10 pontos')    
    arquivo_corrigido_convidado = forms.FileField(label='Arquivo do artigo submetido com apontamentos do avaliador', help_text='Use formato .pdf para enviar seu arquivo corrigido', required=False)
    
    
    class Meta:
        model = Avaliacao
        fields = ['parecer_avaliador_convidado', 'parecer_rebanca_avaliador_convidado', 
              'merito_relevancia_convidado', 'merito_contribuicao_convidado', 'merito_metodologia_convidado',
              'merito_fundamentacao_convidado', 'merito_clareza_convidado', 'merito_referencias_convidado',
              'merito_resultados_convidado', 'merito_conclusao_convidado', 
              'arquivo_corrigido_convidado', 'nota_final_convidado']
        

class BuscaMinhasAvaliacoesForm(forms.Form):
    evento = forms.ModelChoiceField(label='Evento', queryset=Evento.objects.all(), required=False)