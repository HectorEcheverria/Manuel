# -*- encoding: utf-8 -*-
from django import forms
from encuestas.apps.encuestas.models import *
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_integer

class agregarCurso(forms.ModelForm):
	class Meta:
		model 	= Curso
		exclude ={'status',}

class agregarGrupo(forms.ModelForm):
	class Meta:
		model 	= GruposPorCurso
		exclude ={'status',}

class agregarPregunta(forms.Form):
	pregunta 	= forms.CharField(widget=forms.TextInput(),label='Pregunta')
	descripcionPregunta = forms.CharField(widget=forms.TextInput(), label='Descripición de la pregunta')
	respuesta1	= forms.CharField(widget=forms.TextInput(),label='Respuesta nivel muy bajo')
	respuesta2  = forms.CharField(widget=forms.TextInput(),label='Respuesta nivel bajo')
	respuesta3  = forms.CharField(widget=forms.TextInput(),label='Respuesta nivel medio')
	respuesta4  = forms.CharField(widget=forms.TextInput(),label='Respuesta nivel alto')
	respuesta5  = forms.CharField(widget=forms.TextInput(),label='Respuesta nivel muy alto')

class agregarAlumno(forms.Form):
	nombre 		= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Francisco'}))
	apellido	= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Fernández'}))
	email		= forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'francisco.fernandez@usach.cl'}),label='Email')
	rut			= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'11111111'}),label='RUT',)

	def clean(self):
		cd=self.cleaned_data
		validate_integer(cd.get('rut', None))
	
class agregarProfesor(forms.Form):
	nombre 		= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Francisco'}))
	apellido	= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Fernández'}))
	email		= forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'francisco.fernandez@usach.cl'}),label='Email')
	rut			= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'11111111'}),label='RUT (Sin puntos ni guiones)')

	def clean(self):
		cd=self.cleaned_data
		validate_integer(cd.get('rut', None))

class agregarEncuesta(forms.ModelForm):
	
	detalles 		= forms.CharField(required=True)
	modulo			= forms.FloatField(required=True)
	class Meta:
		model 	= Encuesta	
		exclude ={'curso','cerrada','nombreEncuesta','descripcion','preguntas','preguntasLibres','plantilla','fechaCreacion','tipoEncuesta'}


class AgregarEncuestaAdmin(forms.ModelForm):
	class Meta:
		model 	= Encuesta	
		exclude ={'curso','cerrada','preguntas','preguntasLibres','plantilla','fechaCreacion','detalles','modulo'}

class AgregarJefeGrupo(forms.ModelForm):
	class Meta:
		model = JefesDeGrupo
		exclude = {'grupo'}
		

class CamposTexto(forms.Form):
	def __init__(self, titulos, elecciones, *args, **kwargs):
		super(CamposTexto, self).__init__(*args, **kwargs)
		self.fields[titulos] = forms.ChoiceField(  choices = elecciones )

class ListaEleccion(forms.Form):
	def __init__(self, titulo, elecciones, *args, **kwargs):
		super(ListaEleccion, self).__init__(*args, **kwargs)
		self.fields[titulo] = forms.ChoiceField( choices = elecciones, widget=forms.RadioSelect() )
			
class CamposRecibidos(forms.Form):
	def __init__(self, titulos, *args, **kwargs):
		super(CamposRecibidos, self).__init__(*args, **kwargs)
		self.fields[titulos] = forms.CharField( initial="")

class ChoiceResults(forms.Form):
    def __init__(self, newid, *args, **kwargs):
        super(ChoiceResults, self).__init__(*args, **kwargs)

        self.fields['choice'] = forms.TextField( initial="" )

class AgregarEncuestaConPregunta(forms.ModelForm):
	class Meta:
		model = Encuesta
		exclude	={'curso','preguntas','plantilla','detalles','preguntasLibres','modulo','cerrada','fechaCreacion', 'tipoEncuesta'}
		

class TipoEncuestaForm(forms.ModelForm): 
	#tipoEncuesta 	= forms.CharField(widget=forms.TextInput(),label='Ingrese un nuevo tipo de encuesta')
	class Meta:
		model = TipoEncuesta
		exclude = {}			

class agregarPreguntaLibre(forms.Form):
	pregunta 	= forms.CharField(widget=forms.TextInput(),label='Pregunta')
	descripcion	= forms.CharField(widget=forms.TextInput(),label='Descripición de la pregunta')
	respuesta1  = forms.CharField(widget=forms.TextInput(),label='Respuesta')
	
