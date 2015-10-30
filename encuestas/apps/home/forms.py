from django import forms
from encuestas.apps.encuestas.models import *

class contactForm(forms.Form):
	Email	= forms.EmailField(widget=forms.TextInput())
	Titulo	= forms.CharField(widget=forms.TextInput())
	Texto	= forms.CharField(widget=forms.Textarea())

class loginForm(forms.Form):
	username	=	forms.CharField(widget=forms.TextInput())
	password	=	forms.CharField(widget=forms.PasswordInput(render_value=False))

class editarPerfil(forms.Form):

	foto			= forms.FileField()
	email			= forms.EmailField(max_length=200)
	password 		= forms.CharField(widget=forms.PasswordInput(render_value=False))
	password2 		= forms.CharField(widget=forms.PasswordInput(render_value=False))
	