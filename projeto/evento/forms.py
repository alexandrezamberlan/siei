from django import forms
from django.db import models

from usuario.models import Usuario
from .models import Evento


class EventoForm(forms.ModelForm):
    coordenador = forms.ModelChoiceField(label='Coordenador responsável *', queryset=Usuario.coordenadores.all())
    
    class Meta:
        model = Evento
        fields = ['nome', 'tipo', 'descricao', 'carga_horaria', 'local', 'lotacao', 'site', 'instituicao', 'coordenador', 'email', 'data_inicio', 'data_inscricao', 'is_active']

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if usuario and usuario.tipo == 'COORDENADOR':
            self.fields['nome'].widget.attrs['readonly'] = 'readonly'
            self.fields['tipo'].widget.attrs['readonly'] = 'readonly'
            self.fields['instituicao'].widget.attrs['readonly'] = 'readonly'
            self.fields['coordenador'].widget.attrs['readonly'] = 'readonly'
            self.fields['is_active'].widget.attrs['disabled'] = 'disabled'


class BuscaEventoForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
    