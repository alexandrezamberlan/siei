from __future__ import unicode_literals

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import signals
from django.dispatch import receiver

from django.urls import reverse

from decimal import Decimal

from utils.gerador_hash import gerar_hash 

#NOTA; colocar campo para liberar avaliação/banca ao autor ou por data

class Avaliacao(models.Model):
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    CONCORDA = (
        ('SIM', 'Sim'),
        ('NÃO', 'Não'),
    )
    NOTA = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    submissao = models.OneToOneField('submissao.Submissao', verbose_name='Selecione um artigo submetido para avaliação *', on_delete=models.PROTECT)
    
    avaliador_responsavel = models.ForeignKey('usuario.Usuario', verbose_name='Selecione um membro como avaliador 1 *', related_name='avaliador_responsavel', on_delete=models.PROTECT)
    avaliador_suplente = models.ForeignKey('usuario.Usuario', verbose_name='Selecione um membro como avaliador 2 *', related_name='avaliador_suplente', null=True, blank=True, on_delete=models.PROTECT)
    avaliador_convidado = models.ForeignKey('usuario.Usuario', verbose_name='Selecione um membro como avaliador 3', related_name='avaliador_convidado', null=True, blank=True, on_delete=models.PROTECT)
    
    parecer_liberado = models.CharField('Coordenador, você libera o parecer ao autor?', max_length=4, choices=CONCORDA, null=True,blank=True, default='NÃO')
    
    #Campos de parecer avaliador responsavel
    dt_avaliacao_responsavel = models.DateTimeField('Data da avaliação do avaliador 1', null=True, blank=True)
    parecer_avaliador_responsavel = models.TextField('Parecer do avaliador 1 (10000 caracteres)', max_length=10000, null=True, blank=True, help_text='Atenção: se colar seu texto no campo, confira se ele coube no espaço!!')
    parecer_reavaliacao_avaliador_responsavel = models.TextField('Parecer de REAVALIAÇÃO do avaliador 1 (10000 caracteres)', max_length=10000, null=True, blank=True, help_text='Atenção: se colar seu texto no campo, confira se ele coube no espaço!!')
    
    merito_relevancia_responsavel = models.CharField('Relevância: O artigo aborda um problema atual e/ou relevante na área em que foi submetido ao evento?', max_length=1, choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_contribuicao_responsavel = models.CharField('Contribuição: O trabalho apresenta contribuição para a área em que foi submetido ao evento?', max_length=1, choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_metodologia_responsavel = models.CharField('Metodologia: O artigo apresenta uma metodologia e a utiliza de forma apropriada para o problema proposto?', choices=NOTA, max_length=1, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_fundamentacao_responsavel = models.CharField('Fundamentação teórica: O artigo baseia-se em teorias, fundamentos e conceitos relevantes na área em que foi submetido ao evento?', max_length=1, choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_clareza_responsavel = models.CharField('Clareza e organização: O artigo apresenta escrita clara, organizada e coerente?', max_length=1, choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_referencias_responsavel = models.CharField('Referências bibliográficas: As referências utilizadas no artigo são atualizadas e/ou relevantes? ', max_length=1, choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_resultados_responsavel = models.CharField('Resultados e discussões: Os resultados são apresentados e discutidos adequadamente?', max_length=1, choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_conclusao_responsavel = models.CharField('Conclusões: O trabalho traz considerações finais ou conclusão, apresentando reflexões,  avanços ou soluções ao tema abordado, conforme os objetivos propostos?', max_length=1, choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    
    nota_final_responsavel = models.DecimalField('Final Avaliador 1', max_digits=3, decimal_places=2, validators=[MinValueValidator(0.0), MaxValueValidator(5)], null=True, blank=True, default = 0)    
    arquivo_corrigido_responsavel = models.FileField('Arquivo do artigo corrigido pelo avaliador 1', null=True, blank=True, upload_to='midias', help_text='Use formato .pdf para enviar seu arquivo corrigido')

    #Campos de parecer avaliador suplente
    dt_avaliacao_suplente = models.DateTimeField('Data da avaliação do avaliador 2', null=True, blank=True)
    parecer_avaliador_suplente = models.TextField('Parecer do avaliador 2 (10000 caracteres)', max_length=10000, null=True, blank=True, help_text='Atenção: se colar seu texto no campo, confira se ele coube no espaço!!')
    parecer_reavaliacao_avaliador_suplente = models.TextField('Parecer de REAVALIAÇÃO do avaliador 2 (10000 caracteres)', max_length=10000, null=True, blank=True, help_text='Atenção: se colar seu texto no campo, confira se ele coube no espaço!!')
   
    merito_relevancia_suplente = models.CharField('Relevância: O artigo aborda um problema atual e/ou relevante na área em que foi submetido ao evento?', max_length=1,choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_contribuicao_suplente = models.CharField('Contribuição: O trabalho apresenta contribuição para a área em que foi submetido ao evento?', max_length=1,choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_metodologia_suplente = models.CharField('Metodologia: O artigo apresenta uma metodologia e a utiliza de forma apropriada para o problema proposto?', max_length=1,choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_fundamentacao_suplente = models.CharField('Fundamentação teórica: O artigo baseia-se em teorias, fundamentos e conceitos relevantes na área em que foi submetido ao evento?', max_length=1,choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_clareza_suplente = models.CharField('Clareza e organização: O artigo apresenta escrita clara, organizada e coerente?', max_length=1,choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_referencias_suplente = models.CharField('Referências bibliográficas: As referências utilizadas no artigo são atualizadas e/ou relevantes? ', max_length=1,choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_resultados_suplente = models.CharField('Resultados e discussões: Os resultados são apresentados e discutidos adequadamente?', max_length=1,choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_conclusao_suplente = models.CharField('Conclusões: O trabalho traz considerações finais ou conclusão, apresentando reflexões,  avanços ou soluções ao tema abordado, conforme os objetivos propostos?', max_length=1,choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    
    nota_final_suplente = models.DecimalField('Final Avaliador 2',  max_digits=3, decimal_places=2, validators=[MinValueValidator(0.0), MaxValueValidator(5)], null=True, blank=True, default = 0)         
    arquivo_corrigido_suplente = models.FileField('Arquivo do artigo corrigido pelo avaliador 2', null=True, blank=True, upload_to='midias', help_text='Use formato .pdf para enviar seu arquivo corrigido')

    #campos de parecer avaliador convidado
    dt_avaliacao_convidado = models.DateTimeField('Data da avaliação do avaliador 3', null=True, blank=True)
    parecer_avaliador_convidado = models.TextField('Parecer do avaliador 3 (10000 caracteres)', max_length=10000, null=True, blank=True, help_text='Atenção: se colar seu texto no campo, confira se ele coube no espaço!!')
    parecer_reavaliacao_avaliador_convidado = models.TextField('Parecer de REAVALIAÇÃO do avaliador 3 (10000 caracteres)', max_length=10000, null=True, blank=True, help_text='Atenção: se colar seu texto no campo, confira se ele coube no espaço!!')
    
    merito_relevancia_convidado = models.CharField('Relevância: O artigo aborda um problema atual e/ou relevante na área em que foi submetido ao evento?', max_length=1, choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_contribuicao_convidado = models.CharField('Contribuição: O trabalho apresenta contribuição para a área em que foi submetido ao evento?', max_length=1, choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_metodologia_convidado = models.CharField('Metodologia: O artigo apresenta uma metodologia e a utiliza de forma apropriada para o problema proposto?', max_length=1, choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_fundamentacao_convidado = models.CharField('Fundamentação teórica: O artigo baseia-se em teorias, fundamentos e conceitos relevantes na área em que foi submetido ao evento?', max_length=1, choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_clareza_convidado = models.CharField('Clareza e organização: O artigo apresenta escrita clara, organizada e coerente?', max_length=1, choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_referencias_convidado = models.CharField('Referências bibliográficas: As referências utilizadas no artigo são atualizadas e/ou relevantes? ', max_length=1, choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_resultados_convidado = models.CharField('Resultados e discussões: Os resultados são apresentados e discutidos adequadamente?', max_length=1, choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    merito_conclusao_convidado = models.CharField('Conclusões: O trabalho traz considerações finais ou conclusão, apresentando reflexões,  avanços ou soluções ao tema abordado, conforme os objetivos propostos?', max_length=1, choices=NOTA, null=True, blank=True, help_text='De 1 a 5. Nota 1 equivale a NÃO atende, enquanto, nota 5 atende COMPLETAMENTE.')
    
    nota_final_convidado = models.DecimalField('Final Avaliador 3',  max_digits=3, decimal_places=2, validators=[MinValueValidator(0.0), MaxValueValidator(5)], null=True, blank=True, default = 0)         
    arquivo_corrigido_convidado = models.FileField('Arquivo do artigo corrigido pelo avaliador 3', null=True, blank=True, upload_to='midias', help_text='Use formato .pdf para enviar seu arquivo corrigido')

    media_final_avaliacao = models.DecimalField('Média Final', max_digits=3, decimal_places=2, validators=[MinValueValidator(0.0), MaxValueValidator(5)], null=True, blank=True)    
    intercorrencias = models.TextField('Intercorrências do processo de avaliação (20000 caracteres)', max_length=20000, null=True, blank=True, help_text='Coordenador, use esse espaço para anotar qualquer intercorrência do processo de avaliação!')
    
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)
    
    class Meta:
        ordering = ['submissao__evento','-media_final_avaliacao', 'submissao__responsavel__nome']

    def __str__(self):
        return '%s' % (self.submissao)
    
    def calcular_media_final_avaliacao(self):
        if self.avaliador_convidado and self.nota_final_responsavel and self.nota_final_suplente and self.nota_final_convidado:
            self.media_final_avaliacao = (self.nota_final_responsavel + self.nota_final_suplente + self.nota_final_convidado) / 3
        elif self.nota_final_responsavel and self.nota_final_suplente:
            self.media_final_avaliacao = (self.nota_final_responsavel + self.nota_final_suplente) / 2

    def calcular_nota_responsavel(self):
        if self.parecer_avaliador_responsavel:
            #merito_relevancia_responsavel
            #merito_contribuicao_responsavel
            #merito_metodologia_responsavel
            #merito_fundamentacao_responsavel
            #merito_clareza_responsavel
            #merito_referencias_responsavel
            #merito_resultados_responsavel
            #merito_conclusao_responsavel
            self.nota_final_responsavel = round((int(self.merito_relevancia_responsavel)+
                                           int(self.merito_contribuicao_responsavel)+
                                           int(self.merito_metodologia_responsavel)+
                                           int(self.merito_fundamentacao_responsavel)+
                                           int(self.merito_clareza_responsavel)+
                                           int(self.merito_referencias_responsavel)+
                                           int(self.merito_resultados_responsavel)+
                                           int(self.merito_conclusao_responsavel))/8, 1)

    def calcular_nota_suplente(self):
        if self.parecer_avaliador_suplente:
            self.nota_final_suplente = round((int(self.merito_relevancia_suplente)+
                                           int(self.merito_contribuicao_suplente)+
                                           int(self.merito_metodologia_suplente)+
                                           int(self.merito_fundamentacao_suplente)+
                                           int(self.merito_clareza_suplente)+
                                           int(self.merito_referencias_suplente)+
                                           int(self.merito_resultados_suplente)+
                                           int(self.merito_conclusao_suplente))/8, 1)

    def mudar_status_submissao(self):
        submissao = self.submissao

        if submissao.status == 'EM AVALIACAO' and self.parecer_avaliador_responsavel and self.parecer_avaliador_suplente:
            if self.media_final_avaliacao >= 3.5:
                submissao.status = 'APROVADO'
            else:
                submissao.status = 'REPROVADO'
            submissao.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
            
        print(self.parecer_avaliador_responsavel, self.nota_final_responsavel)
        print(self.parecer_avaliador_suplente, self.nota_final_suplente)
        #criando uma avaliacao, entao, atualiza o status da submissao para EM AVALIACAO
        if not self.id:
            self.submissao.status = 'EM AVALIACAO'
            self.submissao.save()
        self.calcular_nota_responsavel()
        self.calcular_nota_suplente()
        self.calcular_media_final_avaliacao()
        self.mudar_status_submissao()
        super(Avaliacao, self).save(*args, **kwargs)
    
    @property
    def get_absolute_url(self):
        return reverse('avaliacao_update', kwargs={'slug': self.slug})
    
    @property
    def get_delete_url(self):
        return reverse('avaliacao_delete', kwargs={'slug': self.slug})
  
    @property
    def get_avaliacao_coordenador_responsavel_url(self):
        return reverse('minha_avaliacao_responsavel', kwargs={'slug': self.slug})

    @property
    def get_avaliacao_coordenador_suplente_url(self):
        return reverse('minha_avaliacao_suplente', kwargs={'slug': self.slug})

    @property
    def get_admin_avaliacao_responsavel_url(self):
        return reverse('minha_avaliacao_responsavel', kwargs={'slug': self.slug})

    @property
    def get_admin_avaliacao_suplente_url(self):
        return reverse('minha_avaliacao_suplente', kwargs={'slug': self.slug})

    # para appmembro  
    @property
    def get_avaliacao_responsavel_url(self):
        return reverse('appmembro_minha_avaliacao_responsavel', kwargs={'slug': self.slug})

    @property
    def get_avaliacao_suplente_url(self):
        return reverse('appmembro_minha_avaliacao_suplente', kwargs={'slug': self.slug})
    
    @property
    def get_avaliacao_convidado_url(self):
        return reverse('appmembro_minha_avaliacao_convidado', kwargs={'slug': self.slug})

    @property
    def get_media_atualizada(self):
        if  self.avaliador_convidado:
            return (self.nota_final_responsavel + self.nota_final_suplente + self.nota_final_convidado) / 3
        
        return (self.nota_final_responsavel + self.nota_final_suplente) / 2
    
    @property
    def get_parecer_liberado_membro_url(self):
        return reverse('appmembro_avaliacao_detail', kwargs={'slug': self.slug})