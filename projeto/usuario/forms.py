from django import forms
from django.db import models

from .models import Usuario

class BuscaUsuarioForm(forms.Form):    
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    TIPOS_USUARIOS = (
        (None, '-----'),
        ('ADMINISTRADOR', 'Administrador'),
        ('COORDENADOR', 'Coordenador de Evento' ),
        ('PARTICIPANTE', 'Participante'),
    )
   
    tipo = forms.ChoiceField(label='Tipo de usuário', choices=TIPOS_USUARIOS, required=False)
       
    
class UsuarioRegisterForm(forms.ModelForm):
    TIPOS_USUARIOS = (
        ('PARTICIPANTE', 'Participante'),
    )
    
    tipo = forms.ChoiceField(label='Tipo *',choices=TIPOS_USUARIOS, help_text='Este processo cadastra somente participante', required=True)
    nome = forms.CharField(label='Nome completo *', help_text='* Campos obrigatórios',required=True)
    
    instituicao = forms.CharField(label='Instituição a que pertence *', help_text='Registre a instituição, ou universidade, ou empresa',required=True)
    email = forms.EmailField(label='Email *', help_text='Use o email válido. Será usado para acessar sistema e recuperar senha!',required=True)
    celular = forms.CharField(label='Número celular com DDD *', help_text="Use DDD, por exemplo 55987619832",required=True)
    cpf = forms.CharField(label='CPF *',required=True)    
    password = forms.CharField(label= "Senha *", widget=forms.PasswordInput,required=True)
    aceita_termo = forms.BooleanField(label='Aceito', required=True, help_text='Se marcado, você aceita o termo de consentimento de uso do sistema')
        
    class Meta:
        model = Usuario
        fields = ['tipo','nome','instituicao', 'email', 'celular', 'cpf', 'password','aceita_termo']
