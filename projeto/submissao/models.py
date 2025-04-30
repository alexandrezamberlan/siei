from __future__ import unicode_literals

import os

from django.db import models
from django.dispatch import receiver
from django.urls import reverse

from avaliacao.models import Avaliacao 

from utils.gerador_hash import gerar_hash

class SubmissaoAtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

        # - coautores (lista de usuários ordinários)
        # - numero_maximo de autores        
        # - enviar email de registro de submissão para o responsável       
        # - categoria ou subárea do trabalho (???)
        

class Submissao(models.Model): 
    STATUS = (
        ('EM EDICAO', 'Em edição'),
        ('EM AVALIACAO', 'Em avaliação'),
        ('EM CORRECAO', 'Em correção' ),        
        ('APROVADO', 'Aprovado' ),
        ('RETIRADO PELO RESPONSAVEL', 'Retirado pelo responsável'),
        ('RETIRADO PELO COORDENADOR', 'Retirado pelo coordenador' ),
        ('REPROVADO', 'Reprovado'),
        ('FINALIZADO', 'Finalizado')
    )      
    responsavel = models.ForeignKey('usuario.Usuario', verbose_name= 'Autor responsável pela submissão *', on_delete=models.PROTECT, related_name='responsavel')
    evento = models.ForeignKey('evento.Evento', verbose_name= 'Evento para a submissão *', on_delete=models.PROTECT, related_name='evento')
    data_hora_submissao = models.DateTimeField(auto_now_add=True)
    data_hora_alteracao_submissao = models.DateTimeField(auto_now=True)
    titulo =  models.CharField('Título *', max_length=200, help_text='Se for colar texto de outro aplicativo, certifique-se que o título esteja completo')
    resumo = models.TextField('Resumo *', max_length=1200, help_text='Máximo caracteres: 1200. Se for colar texto de outro aplicativo, certifique-se que o resumo esteja completo')
    abstract = models.TextField('Abstract *', max_length=1200, help_text='Máximo caracteres: 1200. Se for colar texto de outro aplicativo, certifique-se que o abstract esteja completo')
    palavras_chave =  models.CharField('Palavras-chave *', max_length=100, help_text='Escreva as palavras-chave separadas por ponto-e-vígura. Exemplo: Redes Neurais; Aprendizado de Máquina; Descoberta de Conhecimento')
    arquivo_sem_autores = models.FileField('Arquivo PDF de para avaliação (sem autores e identificação)', upload_to='midias', help_text='Utilize arquivo .PDF')
    arquivo_final = models.FileField('Arquivo corrigido para a versão final', null=True, blank=True, upload_to='midias', help_text='Utilize arquivo .DOCX e lembre de incluir dados dos autores')
    arquivo_comite_etica = models.FileField('Arquivo ZIPADO com documentação necessária de pesquisa em Humanos e Animais',null=True, blank=True, upload_to='midias', help_text='Utilize arquivo compactado .ZIP')
    status = models.CharField('Status da submissão', max_length=25, choices=STATUS, default='EM EDICAO')
    observacoes = models.TextField('Caso necessite, área para registro de justificativas e/ou apontamentos para o responsável da submissão', max_length=500,null=True,blank=True)
    is_active = models.BooleanField('Ativo', default=True, help_text='Se ativo, o Submissao está liberado para chamada de artigos')
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    objects = models.Manager()
    submissoes_ativas = SubmissaoAtivoManager()

    class Meta:
        ordering            =   ['-is_active','evento','responsavel']
        unique_together     =   ['responsavel','evento','titulo']
        verbose_name        =   'submissão'
        verbose_name_plural =   'submissões'

    def __str__(self):
        return '%s | %s' % (self.responsavel, self.titulo)

    def atualizar_status_para_publicar(self):
        if self.status == 'APROVADO' and self.arquivo_final:
            self.status = 'FINALIZADO'

    def save(self, *args, **kwargs):        
        if not self.slug:
            self.slug = gerar_hash()
        self.titulo = self.titulo.upper()
        self.palavras_chave = self.palavras_chave.upper()
        self.atualizar_status_para_publicar()
        super(Submissao, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('submissao_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('submissao_delete', kwargs={'slug': self.slug})
    
    @property
    def get_appmembro_absolute_url(self):
        return reverse('appmembro_submissao_update', kwargs={'slug': self.slug})

    @property
    def get_delete_appmembro_url(self):
        return reverse('appmembro_submissao_delete', kwargs={'slug': self.slug})
    
    @property
    def get_coordenador_absolute_url(self):
        return reverse('submissao_coordenador_update', kwargs={'slug': self.slug})
    
    @property
    def get_delete_coordenador_url(self):
        return reverse('submissao_coordenador_delete', kwargs={'slug': self.slug})
    
    @property
    def get_avaliacao(self):
        try:
            return Avaliacao.objects.get(submissao=self)
        except:
            return None

    @property
    def get_avaliacao_create_update_url(self):
        """
            Se existe uma avaliacao para esta submissao,
            retornar a url de edicao desta avaliacao
            caso contrario, envia para a tela de criacao
            de uma avaliacao, passando o id da submissao como
            parametro GET
        """
        try:
            return self.get_avaliacao.get_absolute_url
        except:
            return '%s?submissao_id=%d' % (reverse('avaliacao_create'), self.id)


#triggers para limpeza dos arquivos apagados ou alterados. No Django é chamado de signals
#deleta o arquivo fisico ao excluir o item midia
@receiver(models.signals.post_delete, sender=Submissao)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.arquivo_sem_autores:
        if os.path.isfile(instance.arquivo_sem_autores.path):
            os.remove(instance.arquivo_sem_autores.path)
    
    if instance.arquivo_final:
        if os.path.isfile(instance.arquivo_final.path):
            os.remove(instance.arquivo_final.path)
    
    if instance.arquivo_comite_etica:
        if os.path.isfile(instance.arquivo_comite_etica.path):
            os.remove(instance.arquivo_comite_etica.path)

#deleta o arquivo fisico ao alterar o arquivo do item midia
@receiver(models.signals.pre_save, sender=Submissao)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        obj = Submissao.objects.get(pk=instance.pk)
        if not obj.arquivo_sem_autores:
            return False
        old_file = obj.arquivo_sem_autores
        new_file = instance.arquivo_sem_autores
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

        if not obj.arquivo_final:
            return False
        old_file = obj.arquivo_final
        new_file = instance.arquivo_final
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

        if not obj.arquivo_comite_etica:
            return False
        old_file = obj.arquivo_comite_etica
        new_file = instance.arquivo_comite_etica
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except Submissao.DoesNotExist:
        return False
