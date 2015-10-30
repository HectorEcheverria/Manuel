from django.shortcuts import render_to_response
from django.template import RequestContext
from encuestas.apps.encuestas.models import *
from encuestas.apps.home.forms import *
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives


def index_view(request):
	encuestas = Encuesta.objects.all()
	laEncuesta = ''
	todosLosCursos = []
	print(request.session)
	usuario = request.user
	losProfesores = Profesor.objects.filter(user_id=usuario.id)

	if 'idEncuestaSeleccionada' in request.session:
		idEncuesta = request.session['idEncuestaSeleccionada']
		laEncuesta = Encuesta.objects.get(id=idEncuesta)
		ctx = {'Encuestas':encuestas,
				'nombreEncuestaSeleccionada':laEncuesta.nombreEncuesta}
	else:
		ctx = {'Encuestas':encuestas}

	if request.user.is_authenticated() and len(losProfesores) == 1 :
		elProfesor = Profesor.objects.get(user=request.user)
		todosLosCursos = Curso.objects.filter(profesor=elProfesor)
		ctx['Cursos'] = todosLosCursos

		return render_to_response('home/index.html',ctx, context_instance=RequestContext(request))
	else:
		if request.method == "POST":
			form = loginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					return HttpResponseRedirect('/')
				else:
					mensaje = "Usuario y/o Password incorrecto"
		form = loginForm()
		print(encuestas)
		ctx= {	'form':form,
				'Encuestas':encuestas,
				'nombreEncuestaSeleccionada':laEncuesta,
				'Cursos':todosLosCursos}
		return render_to_response('home/index.html',ctx,context_instance=RequestContext(request))
	#return render_to_response('home/index.html',ctx, context_instance=RequestContext(request))

def encuestas_view(request):
	mensaje =  "Esto es un mensaje desde mi vista"
	ctx = {'msg':mensaje}
	return render_to_response('home/encuestas.html',ctx,context_instance=RequestContext(request))

def preguntas_view(request):
	preg = PreguntaEncuesta.objects.filter(status=True)
	ctx = {'preguntas':preg}
	return render_to_response('home/preguntas.html',ctx,context_instance=RequestContext(request))

def contacto_view(request):
	email = ''
	titulo = ''
	texto = ''
	if request.method == "POST":
		formulario = contactForm(request.POST)
		if formulario.is_valid():
			email = formulario.cleaned_data['Email']
			titulo = formulario.cleaned_data['Titulo']
			texto = formulario.cleaned_data['Texto']
			# Configuracion correo
			to = email
			html_content = "Recuerde realizar la encuesta que se encuentra en %s " %(texto)
			msg = EmailMultiAlternatives('Encuesta 360',html_content, 'contacto@encuestas.com',[to])
			msg.attach_alternative(html_content,'text/html')
			msg.send()
	else:
		formulario = contactForm()
	ctx = {'form':formulario,'email':email,'titulo':titulo,'texto':texto}
	return render_to_response('home/contacto.html', ctx, context_instance=RequestContext(request))

def login_view(request):
	mensaje	=	""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			form = loginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					return HttpResponseRedirect('/')
				else:
					mensaje = "Usuario y/o Password incorrecto"
		form = loginForm()
		ctx= {'form':form,'mensaje':mensaje}
		return render_to_response('home/login.html',ctx,context_instance=RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def editar_perfil_view(request):
	perfil = editarPerfil()
	if request.user.is_authenticated():
		usuario = request.user
		losProfesores = Profesor.objects.filter(user=usuario)
		losAlumnos = Alumno.objects.filter(user=usuario)
		usuarioExtendido =''
		tipo=''
		if len(losProfesores) == 1:
			usuarioExtendido = losProfesores[0]
			tipo='profesor'
		elif len(losAlumnos) == 1:
			usuarioExtendido = losAlumnos[0]
			tipo='profesor'
		else:
			return HttpResponseRedirect('/')

		if request.method == "POST":
			perfil = editarPerfil(request.POST,request.FILES)
			if perfil.is_valid():
				usuarioExtendido.email = perfil.cleaned_data['email']
				usuarioExtendido.foto = perfil.cleaned_data['foto']
				if perfil.cleaned_data['password']==perfil.cleaned_data['password2']:
					usuario.set_password(perfil.cleaned_data['password'])
					usuarioExtendido.save(update_fields=['email','foto'])
					usuario.save()
			return HttpResponseRedirect('/')
					

	ctx = {'Perfil':perfil}
	return render_to_response('encuestas/editarperfil.html',ctx,context_instance= RequestContext(request))
	

