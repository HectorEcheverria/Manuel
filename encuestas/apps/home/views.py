from django.shortcuts import render_to_response,render,redirect
from django.template import RequestContext
from encuestas.apps.encuestas.models import *
from encuestas.apps.home.forms import *
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.views.generic.edit import UpdateView

def index_view(request):
	encuestas = Encuesta.objects.all()
	laEncuesta = ''
	mensaje =''
	todosLosCursos = []
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
					print 'entro'
					mensaje = "Usuario y/o Password incorrecto"
					ctx = {'mensaje':mensaje,
							'form': form}
					return render(request,'home/index.html',ctx)
		form = loginForm()
		print mensaje
		ctx= {	'form':form,
				'Encuestas':encuestas,
				'nombreEncuestaSeleccionada':laEncuesta,
				'Cursos':todosLosCursos,
				'mensaje':mensaje}
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
	redirect_to = request.REQUEST.get('next', '')
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
					return HttpResponseRedirect(redirect_to)
			else:
				return HttpResponseRedirect('/login/')
				mensaje = "Usuario y/o Password incorrecto"
		form = loginForm()
		ctx= {'form':form,'mensaje':mensaje, 'next':redirect_to}
		return render_to_response('home/login.html',ctx,context_instance=RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def editar_perfil_view(request):
	
	if request.user.is_authenticated():
		usuario = request.user
		try:
			usuarioAlumno = Alumno.objects.get(user=usuario)
		except:
			usuarioAlumno = Profesor.objects.get(user=usuario)
		

		ctx = {'Usuario':usuario,
			'Alumno':usuarioAlumno}
		return render_to_response('home/editarperfil.html',ctx,context_instance= RequestContext(request))		


	return HttpResponseRedirect('/')	
	

def actualizar_perfil(request):
	formulario = editarPerfil()
	usuario = request.user
	verificacionUsuario = ''
	try:
		usuarioAlumno = Alumno.objects.get(user=usuario)
	except:
		usuarioAlumno = Profesor.objects.get(user=usuario)
	if request.user.is_authenticated():
		if request.method == 'POST':
			formulario = editarPerfil(request.POST, request.FILES)
			
			if formulario.is_valid():
				verificacionUsuario = User.objects.all().filter(username=formulario.cleaned_data['username'])
				if 	verificacionUsuario != '' and usuarioAlumno.user.username != formulario.cleaned_data['username']:
					info = 'El nombre de usuario ya existe'
					ctx = {'form':formulario,'informacion':info}
					return render_to_response('home/updateperfil.html',ctx,context_instance= RequestContext(request))
				else:
	 
					request.user.username = formulario.cleaned_data['username']
					request.user.email = formulario.cleaned_data['email']
					usuarioAlumno.foto = formulario.cleaned_data['foto']
					if formulario.cleaned_data['password']==formulario.cleaned_data['password2']:
						usuario.set_password(formulario.cleaned_data['password'])
					usuarioAlumno.save(update_fields=['email','foto'])
					request.user.save()
				return HttpResponseRedirect('/editar/perfil/')
		else:
			formulario = editarPerfil(initial={'username':usuario.username,
												'email':usuario.email,
												'foto':usuarioAlumno.foto})
		ctx = {'form':formulario}
	return render_to_response('home/updateperfil.html',ctx,context_instance= RequestContext(request))
