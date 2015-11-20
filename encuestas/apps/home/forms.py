# -*- encoding: utf-8 -*-
from django import forms
from encuestas.apps.encuestas.models import *

class contactForm(forms.Form):
	Email	= forms.EmailField(widget=forms.TextInput())
	Titulo	= forms.CharField(widget=forms.TextInput())
	Texto	= forms.CharField(widget=forms.Textarea())

class loginForm(forms.Form):
	username	=	forms.CharField(widget=forms.TextInput(),label='Nombre de usuario',required=True)
	password	=	forms.CharField(widget=forms.PasswordInput(render_value=False),label='Contraseña',required=True)

class editarPerfil(forms.Form):

	username		= forms.CharField(widget=forms.TextInput)
	foto			= forms.ImageField(required=False)
	email			= forms.EmailField(max_length=200,required=True)
	password 		= forms.CharField(widget=forms.PasswordInput(),label='Contraseña',required=False)
	password2		= forms.CharField(widget=forms.PasswordInput(),label='Repita su Contraseña',required=False)