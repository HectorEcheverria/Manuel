# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response, redirect,render
from django.template import RequestContext, loader
from encuestas.apps.encuestas.forms import * 
from encuestas.apps.encuestas.models import *
from encuestas.apps.encuestas.grafico import *
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail, send_mass_mail
from django.core.files import File
from django.conf import settings
import re  # regular expresion
import matplotlib 
matplotlib.use('agg')
from matplotlib import pylab
from pylab import *
import PIL
import PIL.Image
import StringIO
import csv

VariableTipoEncuesta = ['Encuesta 360','Encuesta Liderazgo']



def agregar_pregunta_view(request):

	redirect_to = request.REQUEST.get('next', '')

	if request.user.is_staff or request.user.is_superuser:
		if request.method=="POST":
			form = agregarPregunta(request.POST)
			info = "Inicializando"
			if form.is_valid():
				p = PreguntaEncuesta()
				p.pregunta = form.cleaned_data['pregunta']
				p.descripcionPregunta = form.cleaned_data['descripcionPregunta']
				p.respuesta1 = form.cleaned_data['respuesta1']
				p.respuesta2 = form.cleaned_data['respuesta2']
				p.respuesta3 = form.cleaned_data['respuesta3']
				p.respuesta4 = form.cleaned_data['respuesta4']
				p.respuesta5 = form.cleaned_data['respuesta5']
				p.status	= True
				p.save() # Para guardar
				info = "Se guardoo bien"
				return HttpResponseRedirect(redirect_to)
			else:
				info = ""
				ctx = {'form':form, 'informacion':info}
				return render(request,'encuestas/addpregunta.html',ctx)


			form = agregarPregunta()
			ctx = {'form':form, 'informacion':info}
			return render_to_response('encuestas/addpregunta.html',ctx,context_instance=RequestContext(request))

		else:
			form = agregarPregunta()
			ctx = {'form':form}
		return render_to_response('encuestas/addpregunta.html',ctx,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def editar_pregunta_view(request,id_pregunta):

	redirect_to = request.REQUEST.get('next', '')
	pregunta = PreguntaEncuesta.objects.get(id=id_pregunta)

	form = agregarPregunta(initial={'pregunta':pregunta.pregunta,
									'descripcionPregunta':pregunta.descripcionPregunta,
												'respuesta1':pregunta.respuesta1,
												'respuesta2':pregunta.respuesta2,
												'respuesta3':pregunta.respuesta3,
												'respuesta4':pregunta.respuesta4,
												'respuesta5':pregunta.respuesta5})

	if request.user.is_staff or request.user.is_superuser:
		if request.method=="POST":
			form = agregarPregunta(request.POST)
			info = "Inicializando"
			if form.is_valid():
				#p = preguntaEncuesta()
				pregunta.pregunta = form.cleaned_data['pregunta']
				pregunta.descripcionPregunta = form.cleaned_data['descripcionPregunta']
				pregunta.respuesta1 = form.cleaned_data['respuesta1']
				pregunta.respuesta2 = form.cleaned_data['respuesta2']
				pregunta.respuesta3 = form.cleaned_data['respuesta3']
				pregunta.respuesta4 = form.cleaned_data['respuesta4']
				pregunta.respuesta5 = form.cleaned_data['respuesta5']
				pregunta.status	= True
				pregunta.save() # Para guardar
				info = "Se guardoo bien"
				return HttpResponseRedirect(redirect_to)
			else:
				info = "Datos incorrectos"
				ctx = {'form':form, 'informacion':info}
				return render(request,'encuestas/addpregunta.html',ctx)

			form = agregarPregunta(instance=pregunta)
			ctx = {'form':form, 'informacion':info}
			return render_to_response('encuestas/editarpregunta.html',ctx,context_instance=RequestContext(request))

		else:
			
			ctx = {'form':form}
		return render_to_response('encuestas/editarpregunta.html',ctx,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def agregar_alumno_view(request): # Cambiada
	
	if request.user.is_staff or request.user.is_superuser:
		if request.method=="POST":
			todosLosAlumnos = Alumno.objects.all()
			todosLosProfesores = Profesor.objects.all()
			todosLosUsuarios = User.objects.all()
			existeUsuario = False
			existeRut	= False
			datoRepetido = ''
			form = agregarAlumno(request.POST)
			info = ""
			if form.is_valid(): 
				a = Alumno()
				a.nombre 	= form.cleaned_data['nombre']
				a.apellido 	= form.cleaned_data['apellido']
				a.rut 		= form.cleaned_data['rut']
				a.email		= form.cleaned_data['email']
				a.status	= True
				username	= '%s%s' %(a.nombre,a.apellido)
				for cadaAlumno in todosLosAlumnos:
					if cadaAlumno.rut == a.rut:
						existeRut = True
						break
				if existeRut == False:
					for cadaProfesor in todosLosProfesores:
						if cadaProfesor.rut == a.rut:
							existeRut = True
							break
				for cadaUsuario in todosLosUsuarios:
					if cadaUsuario.username == username:
						existeUsuario = True
						break # Dance
				if existeRut == False and existeUsuario == False:
					user = User.objects.create_user(username, form.cleaned_data['email'], form.cleaned_data['rut'])
					print(user.id)
					a.user = user
					a.save()
					info = "Un nuevo alumno se ha creado"
				else:
					if existeRut == True:
						datoRepetido = 'RUT'
					if existeUsuario == True:
						datoRepetido = datoRepetido + ' Usuario'

					info = 'Datos inválidos (%s) repetido' %(datoRepetido)
			else:
				ctx = {'form':form, 'informacion':info}
				return render(request,'encuestas/addprofesor.html',ctx)

			form = agregarAlumno()
			ctx = {'form':form, 'informacion':info}
			return render_to_response('encuestas/addalumno.html',ctx,context_instance=RequestContext(request))
		else:
			form =agregarAlumno()
			ctx = {'form':form}
		return render_to_response('encuestas/addalumno.html',ctx,context_instance= RequestContext(request))
	else:
		return HttpResponseRedirect('/')	

def agregar_profesor_view(request):
	if request.user.is_superuser:
		if request.method=="POST":
			form = agregarProfesor(request.POST)
			info = ""
			todosLosAlumnos = Alumno.objects.all()
			todosLosProfesores = Profesor.objects.all()
			existe = False
			if form.is_valid():
				p = Profesor()
				p.nombre 	= form.cleaned_data['nombre']
				p.apellido 	= form.cleaned_data['apellido']
				p.rut 		= form.cleaned_data['rut']
				p.email		= form.cleaned_data['email']
				p.status	= True
				username	= '%s%s' %(p.nombre,p.apellido)
				for cadaProfesor in todosLosProfesores:
					if cadaProfesor.rut == p.rut:
						existe = True
						break

				if existe == False:
					for cadaAlumno in todosLosAlumnos:
						if cadaAlumno.rut == p.rut:
							existe = True
							break

				if existe == False:
					user = User.objects.create_user(username, form.cleaned_data['email'], form.cleaned_data['rut'])
					print(user.id)
					user.is_staff = True
					user.save()
					p.user = user
					p.save()
					info = "Datos bien guardados"
				else:
					info = 'Datos inválidos'
			else:
				ctx = {'form':form, 'informacion':info}
				return render(request,'encuestas/addprofesor.html',ctx)

			form = agregarProfesor()
			ctx = {'form':form, 'informacion':info}
			return render_to_response('encuestas/addprofesor.html',ctx,context_instance=RequestContext(request))
		else:
			form =agregarProfesor()
			ctx = {'form':form}
		return render_to_response('encuestas/addprofesor.html',ctx,context_instance= RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def agregar_curso_view(request):
	if request.user.is_staff or request.user.is_superuser:	
		info = ""
		if request.method == "POST":
			form = agregarCurso(request.POST)
			if form.is_valid():
				add 		= form.save(commit=False)
				add.status 	= True
				add.save()
				info = "Guardado satisfactoriamente"
			else:
				ctx = {'form':form, 'informacion':info}
				return render(request,'encuestas/addcurso.html',ctx)
		else:
			form = agregarCurso()
		form = agregarCurso()
	ctx = { 'form': form,'informacion':info}
	return render_to_response('encuestas/addcurso.html',ctx,context_instance= RequestContext(request))

def agregar_grupo_view(request):
	redirect_to = request.REQUEST.get('next', '')
	if request.user.is_staff or request.user.is_superuser:

		info = "iniciando"
		if request.method == "POST":
			form = agregarGrupo(request.POST)
			if form.is_valid():
				add 		= form.save(commit=False)
				add.status 	= True
				add.save()
				info = "Guardado satisfactoriamente"
				return HttpResponseRedirect(redirect_to)
			else:
				ctx = {'form':form, 'informacion':info}
				return render(request,'encuestas/addgrupo.html',ctx)

		else:
			form = agregarGrupo()
		form = agregarGrupo()
		ctx = { 'form': form,'informacion':info}
		return render_to_response('encuestas/addgrupo.html',ctx,context_instance= RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def agregar_encuesta_view(request):
	info = ''
	if request.method =='POST':
		form = agregarEncuesta(request.POST)
		if form.is_valid():
			add 	= form.save(commit=False)
			add.save()
			#add.save
			form.save_m2m()
			info = 'Guardado exitosamente'
		else:
			ctx = {'form':form, 'informacion':info}
			return render(request,'encuestas/addencuesta.html',ctx)
	else:
		form = agregarEncuesta()
	form = agregarEncuesta()
	ctx = { 'form':form, 'informacion':info}
	return render_to_response('encuestas/addencuesta.html',ctx,context_instance= RequestContext(request))

def agregar_grupo_a_alumno_view(request,id_profesor): # Sacado de mostrar Curso profesor

	# DATOS
	alumnos 			=[]
	elProfesor 			= Profesor.objects.get(user_id=id_profesor)
	cursoElegido		= 0
	grupoElegido 		= 0
	info 				= ''
	muchosCursos		= Curso.objects.all().filter(profesor=elProfesor)
	todosLosGrupos		= GruposPorCurso.objects.all().filter(curso=cursoElegido) #nuevo
	todosLosAlumnos 	= Alumno.objects.all().filter(grupo=grupoElegido)
	nombreCursoElegido 	= ''
	nombreGrupoElegido 	= ''
	idEncuestas			= []
	idCursoInicial		= ''
	idGrupoInicial		= ''
	encuestasSeleccionadas = []

	if request.user.is_superuser or request.user.is_staff:  # verifica usuario
	# POSTEO			
		if request.method == "POST":	# revisa el método de envío de datos	
			cursoConSemestre = []
			nombreCursoDividido = []
			if 'elCurso' in request.POST:
				nombreCursoElegido  = request.POST['elCurso']
				cursoConSemestre = nombreCursoElegido.split(' ')
				contador = 0
				semestre = cursoConSemestre[len(cursoConSemestre)-2]
				anio = cursoConSemestre[len(cursoConSemestre)-1]

				while (len(cursoConSemestre) - (contador + 2)) > 0:
					variable = ''
					variable = cursoConSemestre[contador]
					nombreCursoDividido.append(variable)
					contador +=1
				if len(nombreCursoDividido) != 1:
					nombreCursoElegido = " ".join(str(x) for x in nombreCursoDividido)
				else:
					nombreCursoElegido = nombreCursoDividido[0]
				cursoElegido = Curso.objects.get(nombrecurso=nombreCursoElegido,year=anio,semestre=semestre)
				todosLosGrupos = GruposPorCurso.objects.all().filter(curso=cursoElegido)
				idCursoInicial = cursoElegido.id
			
			if 'elGrupo' in request.POST:
				nombreGrupoElegido	= request.POST['elGrupo']
 				cursoElegido 		= Curso.objects.get(id=request.POST['elCurso_oculto'])
 				semestreYAnio		='%s-%s' %(cursoElegido.semestre,cursoElegido.year)
 				grupoElegido 		= GruposPorCurso.objects.get(nombre=nombreGrupoElegido,curso=request.POST['elCurso_oculto'])
 				obtenerEncuestas	= RespuestaEncuesta.objects.all().filter(cursoEncuesta=cursoElegido.nombrecurso,semestreAnio=semestreYAnio)

 				for encuestas in obtenerEncuestas:
 					encuestasSeleccionadas.append(encuestas.idEncuesta) 

 				encuestasSeleccionadas = list(set(encuestasSeleccionadas))

 				idGrupoInicial = grupoElegido.id
 				todosLosGrupos = GruposPorCurso.objects.all().filter(curso=cursoElegido)

				idCursoInicial = cursoElegido.id
				idGrupoInicial = grupoElegido.id
				todosLosAlumnos= Alumno.objects.all()
				# print(todosLosAlumnos)
				# print(muchosCursos)


			if 'losAlumnos' in request.POST:
				# print(request.POST.getlist('losAlumnos'))
				idAlumnosSeleccionados	= request.POST.getlist('losAlumnos')
				for cadaIdAlumno in idAlumnosSeleccionados:
					elAlumno = Alumno.objects.get(id=cadaIdAlumno)
					elAlumno.grupo.add(request.POST['elGrupo_oculto'])
					elAlumno.save()


				return HttpResponseRedirect('%s/agregar/grupo/alumno/%s/' %(settings.URL_GEN,elProfesor.id))

		ctx = {	'Cursos':muchosCursos,
				'Grupos':todosLosGrupos,
				'Alumnos':todosLosAlumnos,
				'idCursoInicial':idCursoInicial,
				'idGrupoInicial':idGrupoInicial
				}

		return render_to_response('rencuestas/agregargrupoalumno.html',ctx,context_instance=RequestContext(request))

def agregar_jefe_de_grupo_view(request,id_grupo):
	redirect_to = request.REQUEST.get('next', '')

	if request.user.is_staff or request.user.is_superuser:

		elGrupo = GruposPorCurso.objects.get(id=id_grupo)
		alumnosGrupo = Alumno.objects.all().filter(grupo=elGrupo)
		ctx={}
		if JefesDeGrupo.objects.filter(grupo=elGrupo).exists():
			jefe = JefesDeGrupo.objects.get(grupo=elGrupo)
		else :
			jefe = JefesDeGrupo()
		if request.method == "POST":
			form = AgregarJefeGrupo(request.POST)
			if form.is_valid():
				# jefe = JefesDeGrupo()
				jefe.grupo = elGrupo
				jefe.alumno = form.cleaned_data['alumno']
				jefe.save()
				return HttpResponseRedirect(redirect_to)
			else:
				ctx = {'form':form,
						'Alumnos':alumnosGrupo}
				return render(request,'encuestas/agregarjefegrupo.html',ctx)

		else:
			form = AgregarJefeGrupo()
			ctx = {'Form':form,
					'Alumnos':alumnosGrupo}

		return render_to_response('encuestas/agregarjefegrupo.html',ctx,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

@login_required(login_url="/login/")
def responder_encuesta_view(request,id_encuesta,id_curso):
	
	if request.user.is_authenticated():  # verifica usuario
		try:
			request.user.alumno in Alumno.objects.all()
		except:
			return HttpResponseRedirect('/')
		elecciones = []
		todosLosAlumnos = []
		todosLosGrupos = []
		todosLosEncuestados = []
		info = ''
		elUsuario = request.user
		usuario = Alumno.objects.get(user=elUsuario)
		nombreUsuario = '%s %s' %(usuario.nombre,usuario.apellido)
		mensaje = ''
		losAlumnos = []
		rutDelEncuestador = ''
		elGrupo = ''
		encuestaRepetida = []


		laEncuesta 	= Encuesta.objects.get(id=id_encuesta) # Acá busco la encuesta
		verificador = laEncuesta.tipoEncuesta

		preguntas 	= laEncuesta.preguntas.all()			# Copio las preguntas

		elCurso		= Curso.objects.get(id=id_curso)
		grupos		= GruposPorCurso.objects.all().filter(curso=elCurso)
		alumnos 	= Alumno.objects.all()
		semestreYAnio	= '%s-%s' %(elCurso.semestre,elCurso.year)
		respuestasDeAlumnosEncuestados = RespuestaEncuesta.objects.all().filter(idEncuesta=id_encuesta,rutEncuestador=usuario.rut,cursoEncuesta=elCurso.nombrecurso,semestreAnio=semestreYAnio)
		gruposDelUsuario = usuario.grupo.all()

		for cadaGrupo in grupos:
			for cadaGrupoUsuario in gruposDelUsuario:
				if cadaGrupoUsuario == cadaGrupo:
					elGrupo = GruposPorCurso.objects.get(id=cadaGrupoUsuario.id)
					alumnosGrupo = Alumno.objects.all().filter(grupo=cadaGrupoUsuario)
					for cadaAlumno in alumnosGrupo:
						todosLosEncuestados.append(cadaAlumno)
						for cadaRespuesta in respuestasDeAlumnosEncuestados:
							if cadaRespuesta.rutEncuestado == cadaAlumno.rut:
								todosLosEncuestados.remove(cadaAlumno)


		if verificador.tipoEncuesta == VariableTipoEncuesta[1]:
			jefeGrupo = JefesDeGrupo.objects.get(grupo=elGrupo)
			todosLosEncuestados = [jefeGrupo.alumno]

			
		if request.method == "POST":	# revisa el método de envío de datos


			preguntasrecibidas = []    # la misma wea de laEncuesta
			laRespuesta = RespuestaEncuesta()  # Está wea la cree para recibir datos que se almacenarán

			
			for p in preguntas:						# Acá reviso las preguntas
				if p.pregunta in request.POST:		# Me meto al POST para revisar las preguntas.... mira
					preguntasrecibidas.append(request.POST[p.pregunta]) # Por comparación pego las respuestas a las preguntas...


			#############################
			nombreEncuestador = request.POST['elEncuestador']
			# print(request.POST['elEncuestador'])

			for a in alumnos:
				elNombre = '%s %s' %(a.nombre,a.apellido)
				# print(elNombre)
				if nombreEncuestador == elNombre:
					rutDelEncuestador = a.rut
					break

			laRespuesta.rutEncuestador = rutDelEncuestador

			#######################
			nombreEncuestado = request.POST['elEncuestado']
			for a in alumnos:
				elNombre = '%s %s' %(a.nombre,a.apellido)
				if nombreEncuestado == elNombre:
					rutDelEncuestado = a.rut
					break
			if rutDelEncuestador ==  usuario.rut: # Verificador de respuesta
				info = nombreEncuestador + ' ' + nombreEncuestador
				laRespuesta.cursoEncuesta	= elCurso.nombrecurso
				laRespuesta.semestreAnio	= '%s-%s' %(elCurso.semestre,elCurso.year)
				laRespuesta.idEncuesta 		= id_encuesta
				laRespuesta.rutEncuestado 	= rutDelEncuestado
				laRespuesta.respuestas 		= preguntasrecibidas
				laRespuesta.encuesta 		= laEncuesta 

				encuestaRepetida = RespuestaEncuesta.objects.all().filter(rutEncuestado=rutDelEncuestado,rutEncuestador=rutDelEncuestador,encuesta=laEncuesta)
				print encuestaRepetida
				if len(encuestaRepetida) > 0:
					return HttpResponseRedirect('/encuestas/sin/responder')
				else:

					laRespuesta.save()

				return HttpResponseRedirect('/encuestas/sin/responder')
			else:
				mensaje = 'El encuestador no corresponde al usuario'
			

		else:	
			laEncuesta 	= Encuesta.objects.get(id=id_encuesta)
			preguntas 	= laEncuesta.preguntas.all()
			#elCurso		= laEncuesta.curso
			grupos		= GruposPorCurso.objects.all().filter(id=id_curso)
			losGrupos = []
			for g in grupos:
				losGrupos.append( (g.nombre,g.nombre) )
				alumnos 	= Alumno.objects.all().filter(grupo=g.id)
				losAlumnos = []
				for a in alumnos:
					nombreCompleto = '%s %s' %(a.nombre,a.apellido)
					losAlumnos.append( (nombreCompleto,nombreCompleto) )
				todosLosAlumnos = CamposTexto('Alumnos',losAlumnos)
				encuestados 	= Alumno.objects.all().filter(grupo=g.id)
				losEncuestados = []
				# for e in encuestados:
				# 	nombreCompleto = '%s %s' %(e.nombre,e.apellido)
				# 	losEncuestados.append( (nombreCompleto,nombreCompleto) )
				# todosLosEncuestados = CamposTexto('encuestados',losEncuestados)
			todosLosGrupos = CamposTexto('Grupo', losGrupos)
			for pregunta in preguntas:
				respuestas = []
				respuestas.append( ('1',pregunta.respuesta1) )
				respuestas.append( ('2',pregunta.respuesta2) )
				respuestas.append( ('3',pregunta.respuesta3) )
				respuestas.append( ('4',pregunta.respuesta4) )
				respuestas.append( ('5',pregunta.respuesta5) )
				elecciones.append( ListaEleccion(pregunta.pregunta, respuestas) )

		ctx = {'elecciones':elecciones,
		  		'todosLosGrupos':todosLosGrupos,
		  		'todosLosAlumnos':todosLosAlumnos,
		  		'todosLosEncuestados':todosLosEncuestados,
		  		'Encuestador': usuario,
		  		'NombreEncuestador': nombreUsuario,
		  		'mensaje':mensaje,
		  		'info':info }

		return render_to_response('tomaencuestas/tomaencuesta.html',ctx,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def mostrar_preguntas_view(request):
	if request.user.is_authenticated():
		
		preguntas = PreguntaEncuesta.objects.filter(status=True)

	ctx = {'preguntas':preguntas}
	return render_to_response('encuestas/preguntas.html',ctx,context_instance=RequestContext(request))

def mostrar_curso_view(request,id_profesor): 
	# DATOS
	alumnos 			=[]
	elProfesor 			= Profesor.objects.get(user_id=id_profesor)
	cursoElegido		= 0
	grupoElegido 		= 0
	info 				= ''
	muchosCursos		= Curso.objects.all().filter(profesor=elProfesor)
	todosLosGrupos		= GruposPorCurso.objects.all().filter(curso=cursoElegido) #nuevo
	todosLosAlumnos 	= Alumno.objects.all().filter(grupo=grupoElegido)
	nombreCursoElegido 	= ''
	nombreGrupoElegido 	= ''
	idEncuestas			= []
	idCursoInicial		= ''
	idGrupoInicial		= ''
	encuestasSeleccionadas = []

	if request.user.is_staff or request.user.is_superuser:  # verifica usuario		
		if request.method == "POST":	# revisa el método de envío de datos	
			cursoConSemestre = []
			nombreCursoDividido = []
			if 'elCurso' in request.POST:
				nombreCursoElegido  = request.POST['elCurso']
				cursoConSemestre = nombreCursoElegido.split(' ')
				contador = 0
				semestre = cursoConSemestre[len(cursoConSemestre)-2]
				anio = cursoConSemestre[len(cursoConSemestre)-1]

				while (len(cursoConSemestre) - (contador + 2)) > 0:
					variable = ''
					variable = cursoConSemestre[contador]
					nombreCursoDividido.append(variable)
					contador +=1
				if len(nombreCursoDividido) != 1:
					nombreCursoElegido = " ".join(str(x) for x in nombreCursoDividido)
				else:
					nombreCursoElegido = nombreCursoDividido[0]
				cursoElegido = Curso.objects.get(nombrecurso=nombreCursoElegido,year=anio,semestre=semestre)
				todosLosGrupos = GruposPorCurso.objects.all().filter(curso=cursoElegido)
				idCursoInicial = cursoElegido.id
		
			if 'elGrupo' in request.POST:
				nombreGrupoElegido	= request.POST['elGrupo']
 				cursoElegido 		= Curso.objects.get(id=request.POST['elCurso_oculto'])
 				semestreYAnio		='%s-%s' %(cursoElegido.semestre,cursoElegido.year)
 				grupoElegido 		= GruposPorCurso.objects.get(nombre=nombreGrupoElegido,curso=request.POST['elCurso_oculto'])
 				obtenerEncuestas	= RespuestaEncuesta.objects.all().filter(cursoEncuesta=cursoElegido.nombrecurso,semestreAnio=semestreYAnio)

 				for encuestas in obtenerEncuestas:
 					encuestasSeleccionadas.append(encuestas.idEncuesta) 

 				encuestasSeleccionadas = list(set(encuestasSeleccionadas))

 				idGrupoInicial = grupoElegido.id
 				todosLosGrupos = GruposPorCurso.objects.all().filter(curso=cursoElegido)

				idCursoInicial = cursoElegido.id
				idGrupoInicial = grupoElegido.id

			if 'laEncuesta' in request.POST:
				nombreEncuestaElegida	= request.POST['laEncuesta']
				encuestaElegida 		= Encuesta.objects.get(id=nombreEncuestaElegida)
				cursoElegido 			= Curso.objects.get(id=request.POST['elCurso_oculto'])
				grupoElegido			= GruposPorCurso.objects.get(id=request.POST['elGrupo_oculto'])

				semestreYAnio			='%s-%s' %(cursoElegido.semestre,cursoElegido.year)
 				grupoElegido 			= GruposPorCurso.objects.get(nombre=grupoElegido.nombre,curso=request.POST['elCurso_oculto'])
				idCursoInicial			= cursoElegido.id
				idGrupoInicial			= grupoElegido.id



				return HttpResponseRedirect('/mostrar/respuesta/grupo/%s/%s/%s' %(encuestaElegida.id,idCursoInicial,idGrupoInicial))

		ctx = {	'Cursos':muchosCursos,
				'Grupos':todosLosGrupos,
				'Encuestas':encuestasSeleccionadas,
				'idCursoInicial':idCursoInicial,
				'idGrupoInicial':idGrupoInicial
				}

		return render_to_response('rencuestas/cursos.html',ctx,context_instance=RequestContext(request))

def mostrar_resultados_grupo_view(request,id_grupo,id_encuesta,id_curso):
	# Datos	
	respuestasSeleccionadas = []
	cursoElegido 			= Curso.objects.get(id=id_curso)
	laEncuesta 				= Encuesta.objects.get(id=id_encuesta)
	nombreProfesor			= cursoElegido.profesor
	nombreEncuesta 			= laEncuesta.nombreEncuesta
	nombreCursoElegido		= cursoElegido.nombrecurso
	semestre				= '%s-%s' %(cursoElegido.semestre,cursoElegido.year)
	encuestados 			= []
	encuestados1 			= []
	encuestadores			= []
	elEncuestado 			= ''
	encuestador 			= ''
	promediosAlumnos		= []
	modulador 				= laEncuesta.modulo	
	datosModulados			= []
	total					= 0
	rutPromedio				= []
	cantidadPreguntas = len(laEncuesta.preguntas.all())
	### Parte de Promedios
	print('Comienzo el weveo:\n')
	if request.user.is_staff or request.user.is_superuser:
		respuestasSeleccionadas = RespuestaEncuesta.objects.all().filter(idEncuesta=id_encuesta, cursoEncuesta=cursoElegido.nombrecurso, semestreAnio=semestre)
	
		for r in respuestasSeleccionadas:
			elEncuestado= r.rutEncuestado
			encuestados.append(elEncuestado)

		encuestados1 = list(set(encuestados)) # RUT unicos
		# print(encuestados1)
		for rut in encuestados1:
			sumaPorEncuestado = []
			for r in respuestasSeleccionadas:
				if r.rutEncuestado == rut:
					res = re.sub('\D','', r.respuestas)
					print('veamos res:\n')
					print (res)
					if res != '':
						nuevoRes = list(res)
					 	for n in nuevoRes:
					 		sumaPorEncuestado.append(float(n))
					print('Suma por encuestado:')		 		
					print(sumaPorEncuestado)		 			
			if len(sumaPorEncuestado) != 0:
				for x in range(cantidadPreguntas):
					total = 0
					for cadaCompanero in range(len(encuestados1)):
						total = total + sumaPorEncuestado[cadaCompanero*(cantidadPreguntas)]
					total = total/len(encuestados1)
					dicc = {}
					dicc['RUT']= rut
					# print('RUT')
					# print(dicc['RUT'])
					dicc[x] = total 
					# print('Diccionario promedio por Pregunta')
					# print(dicc[x])
					promediosAlumnos.append(dicc)

		### Parte de Módulos   TODO BIEN HASTA ACÁ//////ARREGLAR ESTA PARTE
		promedioDatosPreguntas = []
		print('Promedio alumnos')
		print(promediosAlumnos)
		for numeroDePregunta in range(cantidadPreguntas):
			promedioDelPromedio = 0
			promedioPorPregunta = 0
			for r in promediosAlumnos:
				if numeroDePregunta in r:
					# print ('Promedio por nota:')
					# print r[numeroDePregunta]
					promedioPorPregunta = promedioPorPregunta + r[numeroDePregunta]
			promedioPregunta = {}
			promedioPregunta[numeroDePregunta] = promedioPorPregunta/len(encuestados1)
			print promedioPregunta[numeroDePregunta]
			promedioDatosPreguntas.append(promedioPregunta)
 		print('El promedio de las preguntas es:')
 		print promedioDatosPreguntas
 		promedioGrupo = 0
 		for cadaPromedio in promedioDatosPreguntas:
 			for x in range(cantidadPreguntas):
 				if x in cadaPromedio:
 					promedioGrupo = cadaPromedio[x] + promedioGrupo
 		promedioGrupo = promedioGrupo/len(promedioDatosPreguntas)

 		modulo = 0
		
		for cadaEncuestado in encuestados1:
			for numeroDePregunta in range(cantidadPreguntas):
				for promedios in promediosAlumnos:
					if cadaEncuestado == promedios['RUT']:
						if numeroDePregunta in promedios:
							modulo = modulo + promedios[numeroDePregunta]
			modulo = modulo/cantidadPreguntas
			modulo = (modulo - promedioGrupo)/modulador
			if modulo <= -1.5:
				modulo = -1.5
			elif modulo >= 1.5:
				modulo = 1.5
			modulosAlumnos	= {}
			modulosAlumnos['RUT'] = cadaEncuestado 
			modulosAlumnos['Modulo'] = modulo 

			datosModulados.append(modulosAlumnos)

		datos = {}

		datos['NombreEncuesta'] = nombreEncuesta
		datos['Curso']			= cursoElegido.nombrecurso
		datos['NombreProfesor']	= nombreProfesor


		ctx = { 'Datos':datos,
				'Encuestados':encuestados1,
				'Resultados':promediosAlumnos,
				'Modulos':datosModulados}

	return render_to_response('rencuestas/vistaporgrupo.html',ctx,context_instance=RequestContext(request))

def enviar_encuestas_curso_view(request,id_encuesta):

	if request.user.is_staff or request.user.is_superuser:
		mailMasivo = []

		laEncuesta 		= Encuesta.objects.get(id=id_encuesta)
		elCurso 		= laEncuesta.curso
		grupos 			= GruposPorCurso.objects.all().filter(curso=elCurso)
		alumnos 		= Alumno.objects.all()
		for cadaGrupo in grupos:
			print(cadaGrupo)
			for cadaAlumno in alumnos:
				for grupo in cadaAlumno.grupo.all():
					if cadaGrupo.id == grupo.id:
						mailMasivo.append(cadaAlumno.email)
		mailMasivo = list(set(mailMasivo))

		mensaje = 'Por favor responder la encuesta 360:\n %s/responder/encuesta/%s/%s' %(settings.URL_GEN,elCurso.id,id_encuesta)
		send_mail('Encuesta 360', mensaje , 'contacto.encuestas.2015@gmail.com', mailMasivo )

	return HttpResponseRedirect('/')

def datos_enviar_encuesta_curso_view(request):
	usuario 			= request.user
	alumnos 			=[]
	elProfesor 			= Profesor.objects.get(user=usuario)
	cursoElegido		= 0
	info 				= ''
	muchosCursos		= Curso.objects.all().filter(profesor=elProfesor)
	nombreCursoElegido 	= ''
	nombreGrupoElegido 	= ''
	idEncuestas			= []
	idCursoInicial		= ''
	idEncuestaInicial	= ''
	encuestaElegida 	= ''
	todasLasEncuestas 	= []
	idEncuestaElegida	= ''

	if request.user.is_staff or request.user.is_superuser: # verifica usuario
		# Posteo			
		if request.method == "POST":	# revisa el método de envío de datos	
			cursoConSemestre = []
			nombreCursoDividido = []
			if 'elCurso' in request.POST:
				idCursoElegido = request.POST['elCurso']
				cursoElegido = Curso.objects.get(id=idCursoElegido)
				idCursoInicial = cursoElegido.id
				todasLasEncuestas = Encuesta.objects.all().filter(plantilla=False,curso=cursoElegido)

			if 'Mostrar' in request.POST:	
				idEncuestaElegida = request.POST['laEncuesta']
				encuestaElegida = Encuesta.objects.get(id=idEncuestaElegida)
				cursoElegido 	= Curso.objects.get(id=request.POST['elCurso_oculto'])
				idEncuestaInicial = encuestaElegida.id
				print idEncuestaInicial
				todasLasEncuestas = Encuesta.objects.all().filter(plantilla=False,curso=cursoElegido)
				idCursoInicial = cursoElegido.id

				ctx = {	'Cursos':muchosCursos,
						'Encuestas':todasLasEncuestas,
						'idCursoInicial':idCursoInicial,
						'idEncuestaInicial':idEncuestaInicial,
						'LaEncuesta': encuestaElegida,
						}

				return render_to_response('rencuestas/vistaenvioencuestas.html',ctx,context_instance=RequestContext(request))
			
			if 'laEncuesta' in request.POST:
				idEncuestaElegida		= request.POST['laEncuesta']
				encuestaElegida 			= Encuesta.objects.get(id=idEncuestaElegida)
				cursoElegido 				= Curso.objects.get(id=request.POST['elCurso_oculto'])
				
				idCursoInicial = request.POST['elCurso_oculto']
				return HttpResponseRedirect('/enviar/encuestas/%s/' %(encuestaElegida.id))


		ctx = {	'Cursos':muchosCursos,
				'Encuestas':todasLasEncuestas,
				'idCursoInicial':idCursoInicial,
				'idEncuestaInicial':idEncuestaElegida,
				'LaEncuesta': encuestaElegida,
				}

		return render_to_response('rencuestas/vistaenvioencuestas.html',ctx,context_instance=RequestContext(request))

def eleccion_encuesta_alumno_view(request):

	# DATOS
	cursoElegido			= 0
	grupoElegido 			= 0
	info 					= ''
	alumnos 				= []
	nombreCursoElegido 		= ''
	nombreGrupoElegido 		= ''
	idEncuestas				= []
	idCursoInicial			= ''
	idGrupoInicial			= ''
	encuestasSeleccionadas	= []
	elUsuario				= request.user
	idUsuario 				= elUsuario.id
	elAlumno 				= Alumno.objects.get(user_id=idUsuario)
	encuestasLista 			= RespuestaEncuesta.objects.all()
	todosLosAlumnos			= Alumno.objects.all()
	todasLasEncuestas		= Encuesta.objects.all()
	cursosAlumno			= []
	gruposDelAlumno 		= elAlumno.grupo.all()
	companerosAlumno		= []

	for cadaGrupo in gruposDelAlumno:
		cursosAlumno.append(cadaGrupo.curso)
		for cadaAlumno in todosLosAlumnos:			
			for cadaGrupoDelAlumno in cadaAlumno.grupo.all():
				if cadaGrupoDelAlumno == cadaGrupo:					
					companerosAlumno.append(cadaAlumno.rut)

	cursosAlumno = list(set(cursosAlumno))
	companerosAlumno = list(set(companerosAlumno))
	print(companerosAlumno)
	print(cursosAlumno)

	if request.user.is_authenticated():  # verifica usuario
		if request.method == "POST":	# revisa el método de envío de datos	
			cursoConSemestre = []
			nombreCursoDividido = []
			if 'elCurso' in request.POST:
				nombreCursoElegido  = request.POST['elCurso']
				cursoConSemestre = nombreCursoElegido.split(' ')
				contador = 0
				semestre = cursoConSemestre[len(cursoConSemestre)-2]
				anio = cursoConSemestre[len(cursoConSemestre)-1]

				while (len(cursoConSemestre) - (contador + 2)) > 0:
					variable = ''
					variable = cursoConSemestre[contador]
					nombreCursoDividido.append(variable)
					contador +=1
				if len(nombreCursoDividido) != 1:
					nombreCursoElegido = " ".join(str(x) for x in nombreCursoDividido)
				else:
					nombreCursoElegido = nombreCursoDividido[0]
				cursoElegido = Curso.objects.get(nombrecurso=nombreCursoElegido,year=anio,semestre=semestre)
				idCursoInicial = cursoElegido.id
				elSemestreAnio = '%s-%s' %(semestre,anio)
				todasLasRespuestas = RespuestaEncuesta.objects.all().filter(cursoEncuesta=nombreCursoElegido,semestreAnio=elSemestreAnio,rutEncuestador=elAlumno.rut)


				for cadaEncuesta in todasLasEncuestas:
					todosLosCursosPorEncuesta = cadaEncuesta.curso.all()
					for cadaCursoenEncuestas in todosLosCursosPorEncuesta:
						if cadaCursoenEncuestas == cursoElegido:
							encuestasSeleccionadas.append(cadaEncuesta)

			if 'laEncuesta' in request.POST:
				idEncuestaElegida		= request.POST['laEncuesta']
				encuestaElegida 		= Encuesta.objects.get(id=idEncuestaElegida)
				cursoElegido 			= Curso.objects.get(id=request.POST['elCurso_oculto'])

				semestreYAnio			='%s-%s' %(cursoElegido.semestre,cursoElegido.year)
 				idCursoInicial			= cursoElegido.id

				return HttpResponseRedirect('%s/responder/encuesta/%s/%s' %(settings.URL_GEN,idCursoInicial,encuestaElegida.id))

		ctx = {	'Cursos':cursosAlumno,
				'Grupos':gruposDelAlumno,
				'Encuestas':encuestasSeleccionadas,
				'idCursoInicial':idCursoInicial,
				}
	return render_to_response('tomaencuestas/eleccionencuestaalumno.html',ctx,context_instance=RequestContext(request))

def eleccion_editar_encuesta_view(request,id_alumno):

	# DATOS
	cursoElegido			= 0
	grupoElegido 			= 0
	info 					= ''
	alumnos 				= []
	nombreCursoElegido 		= ''
	nombreGrupoElegido 		= ''
	idEncuestas				= []
	idCursoInicial			= ''
	idGrupoInicial			= ''
	encuestasSeleccionadas	= []
	elAlumno 				= Alumno.objects.get(user_id=id_alumno)
	encuestasLista 			= RespuestaEncuesta.objects.all()
	todosLosAlumnos			= Alumno.objects.all()
	todasLasEncuestas		= Encuesta.objects.all()
	cursosAlumno			= []
	print(elAlumno)
	gruposDelAlumno 		= elAlumno.grupo.all()
	companerosAlumno		= []

	for cadaGrupo in gruposDelAlumno:
		cursosAlumno.append(cadaGrupo.curso)
		print (cadaGrupo.id)
		for cadaAlumno in todosLosAlumnos:
			for cadaGrupoDelAlumno in cadaAlumno.grupo.all():
				if cadaGrupoDelAlumno == cadaGrupo:
					companerosAlumno.append(cadaAlumno.rut)

	cursosAlumno = list(set(cursosAlumno))
	companerosAlumno = list(set(companerosAlumno))

	if request.user.is_authenticated():  # verifica usuario
		if request.method == "POST":	# revisa el método de envío de datos	
			cursoConSemestre = []
			nombreCursoDividido = []
			if 'elCurso' in request.POST:
				nombreCursoElegido  = request.POST['elCurso']
				cursoConSemestre = nombreCursoElegido.split(' ')
				contador = 0
				semestre = cursoConSemestre[len(cursoConSemestre)-2]
				anio = cursoConSemestre[len(cursoConSemestre)-1]

				while (len(cursoConSemestre) - (contador + 2)) > 0:
					variable = ''
					variable = cursoConSemestre[contador]
					nombreCursoDividido.append(variable)
					contador +=1
				if len(nombreCursoDividido) != 1:
					nombreCursoElegido = " ".join(str(x) for x in nombreCursoDividido)
				else:
					nombreCursoElegido = nombreCursoDividido[0]
				cursoElegido = Curso.objects.get(nombrecurso=nombreCursoElegido,year=anio,semestre=semestre)
				idCursoInicial = cursoElegido.id
				elSemestreAnio = '%s-%s' %(semestre,anio)
				todasLasRespuestas = RespuestaEncuesta.objects.all().filter(cursoEncuesta=nombreCursoElegido,semestreAnio=elSemestreAnio,rutEncuestador=elAlumno.rut)


				for cadaEncuesta in todasLasEncuestas:
					todosLosCursosPorEncuesta = cadaEncuesta.curso.all()
					for cadaCursoenEncuestas in todosLosCursosPorEncuesta:
						if cadaCursoenEncuestas == cursoElegido:
							encuestasSeleccionadas.append(cadaEncuesta)


			if 'laEncuesta' in request.POST:
				nombreEncuestaElegida	= request.POST['laEncuesta']
				encuestaElegida 		= Encuesta.objects.get(nombreEncuesta=nombreEncuestaElegida)
				cursoElegido 			= Curso.objects.get(id=request.POST['elCurso_oculto'])

				semestreYAnio			='%s-%s' %(cursoElegido.semestre,cursoElegido.year)
 				idCursoInicial			= cursoElegido.id

				return HttpResponseRedirect('%s/edicion/encuesta/%s/%s' %(settings.URL_GEN,idCursoInicial,encuestaElegida.id))

		ctx = {	'Cursos':cursosAlumno,
				'Grupos':gruposDelAlumno,
				'Encuestas':encuestasSeleccionadas,
				'idCursoInicial':idCursoInicial,
				}
	return render_to_response('tomaencuestas/eleccioneditarencuesta.html',ctx,context_instance=RequestContext(request))

def editar_encuesta_view(request,id_encuesta,id_curso):

	elecciones = []
	todosLosAlumnos = []
	todosLosGrupos = []
	todosLosEncuestados = []
	info = ''
	elUsuario = request.user
	usuario = Alumno.objects.get(user=elUsuario)
	nombreUsuario = '%s %s' %(usuario.nombre,usuario.apellido)
	mensaje = ''
	editar = ''
	losAlumnos = []
	rutDelEncuestador = ''
	laEncuesta 	= Encuesta.objects.get(id=id_encuesta) # Acá busco la encuesta
	preguntas 	= laEncuesta.preguntas.all()			# Copio las preguntas
	elCurso		= Curso.objects.get(id=id_curso)
	grupos		= gruposPorCurso.objects.all().filter(id=id_curso)
	alumnos 	= Alumno.objects.all()
	semestreYAnio	= '%s-%s' %(elCurso.semestre,elCurso.year)
	respuestasDeAlumnosEncuestados = RespuestaEncuesta.objects.all().filter(idEncuesta=id_encuesta,rutEncuestador=usuario.rut,cursoEncuesta=elCurso.nombrecurso,semestreAnio=semestreYAnio)
	gruposDelUsuario = usuario.grupo.all()

	for cadaGrupo in grupos:
		for cadaGrupoUsuario in gruposDelUsuario:
			if cadaGrupoUsuario == cadaGrupo:
				alumnosGrupo = Alumno.objects.all().filter(grupo=cadaGrupoUsuario)
				for cadaAlumno in alumnosGrupo:
					todosLosEncuestados.append(cadaAlumno)

	print('Los encuestados son')
	print(todosLosEncuestados)


	if request.user.is_authenticated():  # verifica usuario
		
		if request.method == "POST":	# revisa el método de envío de datos

			preguntasrecibidas = []    # la misma wea de laEncuesta
			laRespuesta = RespuestaEncuesta()  # Está wea la cree para recibir datos que se almacenarán
			
			for p in preguntas:						# Acá reviso las preguntas
				if p.pregunta in request.POST:		# Me meto al POST para revisar las preguntas.... mira
					preguntasrecibidas.append(request.POST[p.pregunta]) # Por comparación pego las respuestas a las preguntas...

			nombreEncuestador = request.POST['elEncuestador']

			for a in alumnos:
				elNombre = '%s %s' %(a.nombre,a.apellido)
				print(elNombre)
				if nombreEncuestador == elNombre:
					rutDelEncuestador = a.rut
					break

			laRespuesta.rutEncuestador = rutDelEncuestador

			nombreEncuestado = request.POST['encuestados']
			for a in alumnos:
				elNombre = '%s %s' %(a.nombre,a.apellido)
				if nombreEncuestado == elNombre:
					rutDelEncuestado = a.rut
					break

			if rutDelEncuestador ==  usuario.rut: # Verificador de respuesta
				info = nombreEncuestador + ' ' + nombreEncuestador
				laRespuesta.cursoEncuesta	= elCurso.nombrecurso
				laRespuesta.semestreAnio	= '%s-%s' %(elCurso.semestre,elCurso.year)
				laRespuesta.idEncuesta 		= id_encuesta
				laRespuesta.rutEncuestado 	= rutDelEncuestado
				laRespuesta.respuestas 		= preguntasrecibidas
				laRespuesta.encuesta 		= laEncuesta 

				laRespuesta.save()		
			else:
				mensaje = 'El encuestador no corresponde al usuario'
			editar = 'edita'
		else:	
			laEncuesta 	= Encuesta.objects.get(id=id_encuesta)
			preguntas 	= laEncuesta.preguntas.all()
			#elCurso		= laEncuesta.curso
			grupos		= GruposPorCurso.objects.all().filter(id=id_curso)
			losGrupos = []
			for g in grupos:
				losGrupos.append( (g.nombre,g.nombre) )
				alumnos 	= Alumno.objects.all().filter(grupo=g.id)
				losAlumnos = []
				for a in alumnos:
					nombreCompleto = '%s %s' %(a.nombre,a.apellido)
					losAlumnos.append( (nombreCompleto,nombreCompleto) )
				todosLosAlumnos = CamposTexto('Alumnos',losAlumnos)
				encuestados 	= Alumno.objects.all().filter(grupo=g.id)
				losEncuestados = []
				# for e in encuestados:
				# 	nombreCompleto = '%s %s' %(e.nombre,e.apellido)
				# 	losEncuestados.append( (nombreCompleto,nombreCompleto) )
				# todosLosEncuestados = CamposTexto('encuestados',losEncuestados)
			#todosLosGrupos = CamposTexto('Grupo', losGrupos)
			todosLosGrupos = grupos
			for pregunta in preguntas:
				respuestas = []
				respuestas.append( ('1',pregunta.respuesta1) )
				respuestas.append( ('2',pregunta.respuesta2) )
				respuestas.append( ('3',pregunta.respuesta3) )
				respuestas.append( ('4',pregunta.respuesta4) )
				respuestas.append( ('5',pregunta.respuesta5) )
				elecciones.append( ListaEleccion(pregunta.pregunta, respuestas) )

	ctx = {'elecciones':elecciones,
	  		'todosLosGrupos':todosLosGrupos,
	  		'todosLosAlumnos':todosLosAlumnos,
	  		'todosLosEncuestados':todosLosEncuestados,
	  		'Encuestador': usuario,
	  		'NombreEncuestador': nombreUsuario,
	  		'Editar':editar,
	  		'mensaje':mensaje,
	  		'info':info }

	return render_to_response('tomaencuestas/editarencuesta.html',ctx,context_instance=RequestContext(request))

def almacenar_encuesta_sesion(request,id_encuesta):

	if request.user.is_authenticated():
		laEncuesta = Encuesta.objects.get(id=id_encuesta)
		idEncuesta = laEncuesta.id
		request.session['idEncuestaSeleccionada'] = idEncuesta
		request.session['nombreEncuestaSeleccionada'] = laEncuesta.nombreEncuesta
		print(idEncuesta)

	return HttpResponseRedirect('/')

def agregar_encuesta_con_preguntas_view(request):
	info = ''

	if request.user.is_staff or request.user.is_superuser:

		if request.method =='POST':
			formularioDeEncuesta = AgregarEncuestaAdmin(request.POST)
			formularioDePregunta = agregarPregunta(request.POST)

			if formularioDeEncuesta.is_valid():
				laEncuesta = Encuesta()
				laEncuesta = formularioDeEncuesta.save(commit=False)
				if formularioDePregunta.is_valid():
					p = PreguntaEncuesta()
					p.pregunta = formularioDePregunta.cleaned_data['pregunta']
					p.descripcionPregunta = formularioDePregunta.cleaned_data['descripcionPregunta']
					p.respuesta1 = formularioDePregunta.cleaned_data['respuesta1']
					p.respuesta2 = formularioDePregunta.cleaned_data['respuesta2']
					p.respuesta3 = formularioDePregunta.cleaned_data['respuesta3']
					p.respuesta4 = formularioDePregunta.cleaned_data['respuesta4']
					p.respuesta5 = formularioDePregunta.cleaned_data['respuesta5']
					p.status	= True
					p.save() # Para guardar

				laEncuesta.save()
				laEncuesta.preguntas.add(p)	
				almacenar_encuesta_sesion(request,laEncuesta.id)	
				return redirect('/nuevo/editar/encuesta/')
				info = 'Guardado exitosamente'
			else:
				ctx = { 'FormularioEncuesta':formularioDeEncuesta,
						'FormularioPregunta':formularioDePregunta, 
						'informacion':info}

				return render(request,'encuestas/addencuesta.html',ctx)
		else:
			formularioDeEncuesta = AgregarEncuestaAdmin()
			formularioDePregunta = agregarPregunta()

		ctx = { 'FormularioEncuesta':formularioDeEncuesta,
				'FormularioPregunta':formularioDePregunta, 
				'informacion':info}

		return render_to_response('encuestas/addencuesta.html',ctx,context_instance= RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def editar_encuestas_con_preguntas_view(request):
	
	formularioDeEncuesta = AgregarEncuestaConPregunta() 
	formularioDePregunta = agregarPregunta()
	formularioDePreguntaVacio = agregarPregunta() 
	todasLasPreguntasComoFormulario = []
	info = ''
	idPreguntas = []
	encuestas = Encuesta.objects.all()

	if request.user.is_superuser:
		if 'idEncuestaSeleccionada' in request.session:


			if 'idEncuestaSeleccionada' in request.session:
				laEncuesta = Encuesta.objects.get(id=request.session['idEncuestaSeleccionada'])
				todasLasPreguntas = laEncuesta.preguntas.all()
				
				for cadaPregunta in todasLasPreguntas:
					laPregunta = agregarPregunta(initial={'pregunta':cadaPregunta.pregunta,
														'descripcionPregunta':cadaPregunta.descripcionPregunta,
														'respuesta1':cadaPregunta.respuesta1,
														'respuesta2':cadaPregunta.respuesta2,
														'respuesta3':cadaPregunta.respuesta3,
														'respuesta4':cadaPregunta.respuesta4,
														'respuesta5':cadaPregunta.respuesta5})

					todasLasPreguntasComoFormulario.append(laPregunta)
					idPreguntas.append(cadaPregunta.id)
				
				
				formularioDeEncuesta = AgregarEncuestaConPregunta(initial={'nombreEncuesta':laEncuesta.nombreEncuesta,
																'descripcion':laEncuesta.descripcion})
				if request.method =='POST':

					formularioDeEncuesta = AgregarEncuestaConPregunta(request.POST)
					formularioDePregunta = agregarPregunta(request.POST)

					if formularioDeEncuesta.is_valid():
					
						if formularioDePregunta.is_valid():
							p = PreguntaEncuesta()
							p.pregunta = formularioDePregunta.cleaned_data['pregunta']
							p.descripcionPregunta = formularioDePregunta.cleaned_data['descripcionPregunta']
							p.respuesta1 = formularioDePregunta.cleaned_data['respuesta1']
							p.respuesta2 = formularioDePregunta.cleaned_data['respuesta2']
							p.respuesta3 = formularioDePregunta.cleaned_data['respuesta3']
							p.respuesta4 = formularioDePregunta.cleaned_data['respuesta4']
							p.respuesta5 = formularioDePregunta.cleaned_data['respuesta5']
							p.status	= True
							p.save() # Para guardar

							laEncuesta.preguntas.add(p)		
							laEncuesta.save()
							nuevaPregunta = agregarPregunta(initial={'pregunta':p.pregunta,
															'respuesta1':p.respuesta1,
															'respuesta2':p.respuesta2,
															'respuesta3':p.respuesta3,
															'respuesta4':p.respuesta4,
															'respuesta5':p.respuesta5})
							todasLasPreguntasComoFormulario.append(nuevaPregunta)
							info = 'Guardado exitosamente'
							return redirect('/nuevo/editar/encuesta/')
						else:
							ctx = { 'FormularioEncuesta':formularioDeEncuesta,
									'FormularioPregunta':formularioDePregunta,
									'FormularioDePreguntaVacio':formularioDePreguntaVacio, 
									'Preguntas':todasLasPreguntasComoFormulario,
									'IdPreguntas':idPreguntas,
									'Encuestas':encuestas,
									'informacion':info}
							return render(request,'encuestas/editarencuesta.html',ctx)
					else:

						ctx = { 'FormularioEncuesta':formularioDeEncuesta,
								'FormularioPregunta':formularioDePregunta,
								'FormularioDePreguntaVacio':formularioDePreguntaVacio, 
								'Preguntas':todasLasPreguntasComoFormulario,
								'IdPreguntas':idPreguntas,
								'Encuestas':encuestas,
								'informacion':info}
						return render(request,'encuestas/editarencuesta.html',ctx)



		ctx = { 'FormularioEncuesta':formularioDeEncuesta,
				'FormularioPregunta':formularioDePregunta,
				'FormularioDePreguntaVacio':formularioDePreguntaVacio, 
				'Preguntas':todasLasPreguntasComoFormulario,
				'IdPreguntas':idPreguntas,
				'Encuestas':encuestas,
				'informacion':info}
		return render_to_response('encuestas/editarencuesta.html',ctx,context_instance= RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def crear_encuesta_profesor_view(request):
	# DATOS
	alumnos 			=[]
	usuario 			= request.user
	elProfesor 			= Profesor.objects.get(user=usuario)
	cursoElegido		= 0
	grupoElegido 		= 0
	info 				= ''
	muchosCursos		= Curso.objects.all().filter(profesor=elProfesor)
	todosLosGrupos		= GruposPorCurso.objects.all().filter(curso=cursoElegido) #nuevo
	todosLosAlumnos 	= Alumno.objects.all().filter(grupo=grupoElegido)
	nombreCursoElegido 	= ''
	nombreGrupoElegido 	= ''
	idEncuestas			= []
	idCursoInicial		= ''
	idGrupoInicial		= ''
	encuestasSeleccionadas = Encuesta.objects.filter(plantilla=True)

	formularioLaEncuesta = agregarEncuesta()
	encuestaParaCurso = Encuesta()

	if request.user.is_staff or request.user.is_superuser:  # verifica usuario
	# POSTEO			
		if request.method == "POST":	# revisa el método de envío de datos	
			cursoConSemestre = []
			nombreCursoDividido = []
			if 'elCurso' and 'laEncuesta' in request.POST:
				idCursoElegido = request.POST['elCurso']

				cursoElegido = Curso.objects.get(id=idCursoElegido)

				todosLosGrupos = GruposPorCurso.objects.all().filter(curso=cursoElegido)
				idCursoInicial = cursoElegido.id

				idEncuestaElegida	= request.POST['laEncuesta']
				encuestaElegida 	= Encuesta.objects.get(id=idEncuestaElegida)
				listadoPreguntas = encuestaElegida.preguntas.all()

				semestreYAnio			='%s-%s' %(cursoElegido.semestre,cursoElegido.year)
				idCursoInicial			= cursoElegido.id

				form = agregarEncuesta(request.POST)
				if form.is_valid():	

					encuestaParaCurso.nombreEncuesta = encuestaElegida.nombreEncuesta
					encuestaParaCurso.descripcion = encuestaElegida.descripcion
					
					encuestaParaCurso.curso = cursoElegido
					encuestaParaCurso.plantilla = False
					encuestaParaCurso.detalles = request.POST['detalles']
					encuestaParaCurso.tipoEncuesta = encuestaElegida.tipoEncuesta
					encuestaParaCurso.modulo = form.cleaned_data['modulo']
					encuestaParaCurso.fechaCreacion =datetime.date.today()
					encuestaParaCurso.pk =None

					encuestaParaCurso.save()
					for cadaPregunta in listadoPreguntas:
				 		encuestaParaCurso.preguntas.add(cadaPregunta)
					
					almacenar_encuesta_sesion(request,encuestaParaCurso.pk)
				else:
					ctx = {	'Cursos':muchosCursos,
							'Grupos':todosLosGrupos,
							'Encuestas':encuestasSeleccionadas,
							'idCursoInicial':idCursoInicial,
							'idGrupoInicial':idGrupoInicial,
							'Formulario':form,
							}
					return render(request,'encuestas/agregarencuestaprofesor.html',ctx)



				return HttpResponseRedirect('/')

		ctx = {	'Cursos':muchosCursos,
				'Grupos':todosLosGrupos,
				'Encuestas':encuestasSeleccionadas,
				'idCursoInicial':idCursoInicial,
				'idGrupoInicial':idGrupoInicial,
				'Formulario':formularioLaEncuesta,
				}

		return render_to_response('encuestas/agregarencuestaprofesor.html',ctx,context_instance=RequestContext(request))

def almacenar_curso_sesion(request,id_curso):

	if request.user.is_authenticated():
		elCurso = Curso.objects.get(id=id_curso)
		idCurso = elCurso.id
		request.session['idCursoSeleccionado'] = idCurso
		request.session['nombreCursoSeleccionado'] = elCurso.nombrecurso

	return HttpResponseRedirect('/agregar/alumnos/grupos/')

def agregar_alumnos_a_grupo_por_curso_view(request):

	todos = []
	integrantes=[]
	elCurso = Curso.objects.get(id=request.session['idCursoSeleccionado'])
	todosLosAlumnos = Alumno.objects.filter(status=True)
	todosLosApellidos = []
	todosLosRUT = []
	todosLosGrupos 	= GruposPorCurso.objects.filter(curso=elCurso)
	valorIdMaximo	= Alumno.objects.latest('id')
	grupoSeleccionado	= ''
	idGrupoOculto = ''
	elGrupo = ''
	ctx ={	'Alumnos':todosLosAlumnos,
			'Grupos':todosLosGrupos,
			'idGrupoSeleccionado':grupoSeleccionado,
			}
	if request.user.is_staff or request.user.is_superuser:

		if request.method=='POST':
			if 'idGrupoOculto' in request.POST:
				
				elGrupo = GruposPorCurso.objects.get(id=request.POST['idGrupoOculto'])
				idGrupoOculto = elGrupo.id
				integrantes = Alumno.objects.filter(grupo=elGrupo).order_by('apellido', 'nombre')
				if 'buscado' in request.POST:
					if request.POST['buscado'] != '':
						todosLosAlumnos = Alumno.objects.filter(nombre__contains=request.POST['buscado'])
						todosLosApellidos = Alumno.objects.filter(apellido__contains=request.POST['buscado'])
						todosLosRUT = Alumno.objects.filter(rut__contains=request.POST['buscado'])
						for elApellido in todosLosApellidos:
							todos.append(elApellido)
						for elAlumno in todosLosAlumnos:
							todos.append(elAlumno)
						for elRUT in todosLosRUT:
							todos.append(elRUT)

						todos = list(set(todos))

						ctx ={	'Alumnos':todos,
								'Grupos':todosLosGrupos,
								'idGrupoSeleccionado':idGrupoOculto,
								'Integrantes':integrantes
						}
					else:
						ctx ={	'Alumnos':todosLosAlumnos,
								'Grupos':todosLosGrupos,
								'idGrupoSeleccionado':idGrupoOculto,
								'Integrantes':integrantes
								}

			if 'Eliminar' in request.POST:
				
				if 'elGrupo' in request.POST:
					elGrupo = GruposPorCurso.objects.get(id=request.POST['elGrupo'])
					idElGrupo = elGrupo.id
					for i in range(0,valorIdMaximo.id+1):
						if '%s'%i in request.POST:
							elAlumno = Alumno.objects.get(id=i)
							listadeGruposDelAlumno = elAlumno.grupo.all()
							if elGrupo in listadeGruposDelAlumno:
								elAlumno.grupo.remove(elGrupo)
							
					integrantes = Alumno.objects.filter(grupo=elGrupo).order_by('apellido', 'nombre')
					ctx={'Alumnos':todosLosAlumnos,
						'Grupos':todosLosGrupos,
						'idGrupoSeleccionado':idElGrupo,
						'Integrantes':integrantes}

				return render_to_response('encuestas/agregaralumnoagrupoporcurso.html',ctx,context_instance=RequestContext(request))


			else:
				if 'elGrupo' in request.POST:
					print 'llego a meter'
					print request.POST['elGrupo']
					elGrupo = GruposPorCurso.objects.get(id=request.POST['elGrupo'])
					idElGrupo = elGrupo.id
					for i in range(0,valorIdMaximo.id+1):
						if '%s'%i in request.POST:
							elAlumno = Alumno.objects.get(id=i)
							listadeGruposDelAlumno = elAlumno.grupo.all()
							if elGrupo in listadeGruposDelAlumno:
								print('Ya está')
							else:
								elAlumno.grupo.add(elGrupo)
					integrantes = Alumno.objects.filter(grupo=elGrupo).order_by('apellido', 'nombre')
					ctx={'Alumnos':todosLosAlumnos,
						'Grupos':todosLosGrupos,
						'idGrupoSeleccionado':elGrupo.id,
						'Integrantes':integrantes}

				return render_to_response('encuestas/agregaralumnoagrupoporcurso.html',ctx,context_instance=RequestContext(request))
		
		return render_to_response('encuestas/agregaralumnoagrupoporcurso.html',ctx,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def eliminar_pregunta_encuesta_view(request,id_pregunta):
	redirect_to = request.REQUEST.get('next', '')
	if request.user.is_staff or request.user.is_superuser:

		if 'idEncuestaSeleccionada' in request.session:
			laEncuesta = Encuesta.objects.get(id=request.session['idEncuestaSeleccionada'])
			#laPregunta = preguntaEncuesta.objects.get(id=id_pregunta)

			laEncuesta.preguntas.remove(id_pregunta)
			return HttpResponseRedirect(redirect_to) 
	else:
		return HttpResponseRedirect('/')

def tipo_de_encuesta_view(request): 
	tipoEncuestaExistente = TipoEncuesta.objects.all()
	if request.user.is_superuser:

		for cadaTipo in VariableTipoEncuesta:
			agregarTipo = TipoEncuesta()
			salir = False
			for cadaTipoExistente in tipoEncuestaExistente:
				if cadaTipo == cadaTipoExistente:
					salir = True
			if salir ==True:
				agregarTipo.tipoEncuesta = cadaTipo
				agregarTipo.save()

	return HttpResponseRedirect('/')
	
def agregar_pregunta_libre_view(request):

	redirect_to = request.REQUEST.get('next', '')

	if request.user.is_superuser or request.user.is_staff:
		if request.method=="POST":
			form = agregarPreguntaLibre(request.POST)
			info = "Inicializando"
			if form.is_valid():
				p = preguntaLibre()
				p.pregunta = form.cleaned_data['pregunta']
				p.descripcion = form.cleaned_data['descripcion']
				p.respuesta1 = form.cleaned_data['respuesta1']
	
				p.save() # Para guardar
				info = "Se guardoo bien"
				return HttpResponseRedirect(redirect_to)
			
		else:
			form = agregarPreguntaLibre()
			ctx = {'form':form}
		return render_to_response('encuestas/agregarpreguntalibre.html',ctx,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def editar_pregunta_libre_view(request,id_pregunta):

	redirect_to = request.REQUEST.get('next', '')
	pregunta = PreguntaLibre.objects.get(id=id_pregunta)

	form = agregarPreguntaLibre(initial={'pregunta':pregunta.pregunta,
												'descripcion':pregunta.descripcion,
												'respuesta2':pregunta.respuesta1})

	if request.user.is_superuser or request.user.is_staff:
		if request.method=="POST":
			form = agregarPreguntaLibre(request.POST)
			info = "Inicializando"
			if form.is_valid():
				pregunta.pregunta = form.cleaned_data['pregunta']
				pregunta.descripcion = form.cleaned_data['descripcion']
				pregunta.respuesta1 = form.cleaned_data['respuesta1']
				
				pregunta.save() # Para guardar
				info = "Se guardoo bien"
				return HttpResponseRedirect(redirect_to)

		else:
			
			ctx = {'form':form}
		return render_to_response('encuestas/agregarpreguntalibre.html',ctx,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def nuevo_eleccion_encuesta_alumno_view(request):

	# DATOS
	cursoElegido			= 0
	grupoElegido 			= 0
	info 					= ''
	alumnos 				= []
	nombreCursoElegido 		= ''
	nombreGrupoElegido 		= ''
	idEncuestas				= []
	idCursoInicial			= ''
	idGrupoInicial			= ''
	encuestasSeleccionadas	= []
	encuestasMostrar		= []
	elUsuario				= request.user
	idUsuario 				= elUsuario.id
	elAlumno 				= Alumno.objects.get(user_id=idUsuario)
	encuestasListas			= RespuestaEncuesta.objects.all().filter(rutEncuestador=elAlumno.rut)
	todosLosAlumnos			= Alumno.objects.all()
	todasLasEncuestas		= Encuesta.objects.all().filter(plantilla=False)# agregar luego las cerradas
	tipoLiderazgo 			= TipoEncuesta.objects.get(tipoEncuesta=VariableTipoEncuesta[1])
	cursosAlumno			= []
	gruposDelAlumno 		= elAlumno.grupo.all()
	companerosAlumno		= []
	todosLosCursoEncuesta 	= []
	datos = {}

	for cadaGrupo in gruposDelAlumno:
		cursosAlumno.append(cadaGrupo.curso)
		for cadaAlumno in todosLosAlumnos:			
			for cadaGrupoDelAlumno in cadaAlumno.grupo.all():
				if cadaGrupoDelAlumno == cadaGrupo:					
					companerosAlumno.append(cadaAlumno.rut)

	cursosAlumno = list(set(cursosAlumno))
	companerosAlumno = list(set(companerosAlumno))
	alumnosCompanero = []
	for cadaCompanero in companerosAlumno:
		alumnosCompanero.append(Alumno.objects.filter(rut=cadaCompanero))

	if request.user.is_authenticated():  # verifica usuario



		for cadaEncuesta in todasLasEncuestas:
			for cadaCurso in cursosAlumno:
					if cadaEncuesta.curso  == cadaCurso:
						encuestasSeleccionadas.append(cadaEncuesta)

		for cadaEncuesta in encuestasSeleccionadas:
			respuestasEncuesta = []

			for cadaEncuestaLista in encuestasListas:
				if cadaEncuestaLista.encuesta == cadaEncuesta:
					respuestasEncuesta.append(cadaEncuestaLista)


			for cadaGrupo in gruposDelAlumno:
				
				companerosPorGrupo = Alumno.objects.all().filter(grupo=cadaGrupo)
				contador = len(companerosPorGrupo)
				for cadaRespuesta in respuestasEncuesta:
					for cadaCompanero in companerosPorGrupo:
						if cadaRespuesta.rutEncuestado == cadaCompanero.rut:
							contador -= 1 
				if  contador != 0 :
					encuestasMostrar.append(cadaEncuesta)
				if contador < len(companerosPorGrupo) and cadaEncuesta.tipoEncuesta == tipoLiderazgo:
					encuestasMostrar.remove(cadaEncuesta)

		cursosDeEncuestas = []
		for cadaEncuesta in encuestasMostrar:
			cursosDeEncuestas.append(cadaEncuesta.curso)

		cursosDeEncuestas = list(set(cursosDeEncuestas))
		encuestasMostrar = list(set(encuestasMostrar))


		# print encuestasMostrar
		ctx = {	'Encuestas': encuestasMostrar,
				'Cursos': cursosDeEncuestas
				}
	return render_to_response('rencuestas/encuestassinterminarporalumno.html',ctx,context_instance=RequestContext(request))

def mostrar_encuestas_finalizadas_view(request):
	#### ARREGLAR
	if request.user.is_authenticated():
		usuario = request.user
		elAlumno = Alumno.objects.get(user=usuario)
		gruposAlumno = elAlumno.grupo.all()
		cursosAlumno = []
		companerosAlumno = []
		todasLasRespuestas = []
		encuestasTerminadas = []
		laEncuesta = ''
		todasLasEncuestas = []

		for cadaGrupo in gruposAlumno:
			cursosAlumno.append(cadaGrupo.curso)
		for cadaCurso in cursosAlumno:
			todasLasEncuestas = Encuesta.objects.all().filter(plantilla=False, curso=cadaCurso)
			for cadaEncuesta in todasLasEncuestas:
				encuestasTerminadas.append(cadaEncuesta)
		encuestasTerminadas = set(list(encuestasTerminadas))
		print encuestasTerminadas

		for cadaEncuesta in todasLasEncuestas:
			for cadaGrupo in gruposAlumno:
				if cadaEncuesta.curso == cadaGrupo.curso:
					companerosAlumno = Alumno.objects.all().filter(grupo=cadaGrupo)
					todasLasRespuestas = RespuestaEncuesta.objects.all().filter(encuesta=cadaEncuesta)

					for cadaCompanero in companerosAlumno:
						estaEncuestados = False
						for cadaCompanero1 in companerosAlumno:
							estaEncuestados = False
							for cadaRespuesta in todasLasRespuestas:
								if cadaCompanero.rut == cadaRespuesta.rutEncuestador and cadaCompanero1.rut == cadaRespuesta.rutEncuestado:
									estaEncuestados = True
									break

							if estaEncuestados == False:
								if cadaEncuesta in encuestasTerminadas:
									encuestasTerminadas.remove(cadaEncuesta)
		ctx = {'EncuestasTerminadas':encuestasTerminadas,
		}
		return render_to_response('rencuestas/feedback.html',ctx,context_instance=RequestContext(request))

def modulacion_alumno(id_alumno,id_grupo,id_encuesta):
	elAlumno = Alumno.objects.get(id=id_alumno)
	elGrupo = GruposPorCurso.objects.get(id=id_grupo)
	laEncuesta = Encuesta.objects.get(id=id_encuesta)
	respuestasSeleccionadas = RespuestaEncuesta.objects.all().filter(encuesta=laEncuesta)
	companerosDeGrupo = Alumno.objects.all().filter(grupo=elGrupo)
	promediosAlumnos = []
	cantidadPreguntas = len(laEncuesta.preguntas.all())
	promediosElAlumno = []
	modulador = laEncuesta.modulo 

	promediosElAlumno2 =[]
	promediosPreguntas2 = []


	for cadaCompanero in companerosDeGrupo:
		sumaPorEncuestado = []
		for r in respuestasSeleccionadas:
			if r.rutEncuestado == cadaCompanero.rut:
				res = re.sub('\D','', r.respuestas) # obtengo string que representa todas las respuestas
				if res != '':
					nuevoRes = list(res) # convierto en lista
				 	for n in nuevoRes:
				 		sumaPorEncuestado.append(float(n))

		if len(sumaPorEncuestado) != 0:
			for x in range(cantidadPreguntas):
				total = 0
				for c in range(len(companerosDeGrupo)):
					total = total + sumaPorEncuestado[(x*c)]
					# print ('Lo que se suma al total es')
					# print sumaPorEncuestado[c*cantidadPreguntas]
				
				total = total/len(companerosDeGrupo)
				# print ('El total de una pregunta es')
				# print total
				

				dicc = {}
				dicc['RUT']= cadaCompanero.rut
				dicc[x] = total 

				promediosAlumnos.append(dicc)
				if elAlumno.rut == cadaCompanero.rut:
					promediosElAlumno.append(dicc)
					promediosElAlumno2.append(round(total,3))
		# print ('Todas las respuestas recibidas ')
		# print sumaPorEncuestado



	### Parte de Módulos 
	promedioDatosPreguntas = []
	# print('Promedio alumnos')
	# print(promediosAlumnos)
	for numeroDePregunta in range(cantidadPreguntas):
		promedioPorPregunta = 0
		for r in promediosAlumnos:
			if numeroDePregunta in r:
				# print ('Promedio por nota:')
				# print r[numeroDePregunta]
				promedioPorPregunta = promedioPorPregunta + r[numeroDePregunta]
		promedioPregunta = {}
		promedioPregunta[numeroDePregunta] = promedioPorPregunta/len(companerosDeGrupo)
		promediosPreguntas2.append(round(promedioPorPregunta/len(companerosDeGrupo),3))
		# print promedioPregunta[numeroDePregunta]
		promedioDatosPreguntas.append(promedioPregunta)

		# print('El promedio de las preguntas es:')
		# print promedioDatosPreguntas
		promedioGrupo = 0
		for cadaPromedio in promedioDatosPreguntas:
			for x in range(cantidadPreguntas):
				if x in cadaPromedio:
					promedioGrupo = cadaPromedio[x] + promedioGrupo
		promedioGrupo = promedioGrupo/len(promedioDatosPreguntas)

		modulo = 0

	for cadaEncuestado in companerosDeGrupo:
		if cadaEncuestado.rut == elAlumno.rut:
			for numeroDePregunta in range(cantidadPreguntas):
				for promedios in promediosAlumnos: # promedios es un diccionario con numero pregunta 
					if cadaEncuestado.rut == promedios['RUT']:
						if numeroDePregunta in promedios:
							modulo = modulo + promedios[numeroDePregunta]
						
			modulo = modulo/cantidadPreguntas
			modulo = (modulo - promedioGrupo)/(2/modulador)
		
			if modulo <= -(modulador):
				modulo = -(modulador)
			elif modulo >= (modulador):
				modulo = (modulador)

	ctx = { 'ModuloAlumno':modulo,
			'PromediosElAlumno':promediosElAlumno2,
			'PromediosPreguntas':promediosPreguntas2}


	return ctx

def modulacion_por_grupo(id_grupo,id_encuesta):
	
	elGrupo = GruposPorCurso.objects.get(id=id_grupo)
	laEncuesta = Encuesta.objects.get(id=id_encuesta)
	respuestasSeleccionadas = RespuestaEncuesta.objects.all().filter(encuesta=laEncuesta)
	alumnosDelGrupo = Alumno.objects.all().filter(grupo=elGrupo)
	promediosAlumnos = []
	cantidadPreguntas = len(laEncuesta.preguntas.all())
	promediosElAlumno = []
	modulador = laEncuesta.modulo 

	for cadaCompanero in alumnosDelGrupo:
		sumaPorEncuestado = []
		for r in respuestasSeleccionadas:
			if r.rutEncuestado == cadaCompanero.rut:
				res = re.sub('\D','', r.respuestas) # obtengo string que representa todas las respuestas
				if res != '':
					nuevoRes = list(res) # convierto en lista
				 	for n in nuevoRes:
				 		sumaPorEncuestado.append(float(n))

		if len(sumaPorEncuestado) != 0:
			for x in range(cantidadPreguntas):
				total = 0
				for c in range(len(alumnosDelGrupo)):
					total = total + sumaPorEncuestado[(x*c)]

				total = total/len(alumnosDelGrupo)

				dicc = {}
				dicc['RUT']= cadaCompanero.rut
				dicc[x] = total 

				promediosAlumnos.append(dicc)

	### Parte de Módulos 
	promedioDatosPreguntas = []

	for numeroDePregunta in range(cantidadPreguntas):
		promedioPorPregunta = 0
		for r in promediosAlumnos:
			if numeroDePregunta in r:

				promedioPorPregunta = promedioPorPregunta + r[numeroDePregunta]
		promedioPregunta = {}
		if len(alumnosDelGrupo) !=0:
			promedioPregunta[numeroDePregunta] = promedioPorPregunta/len(alumnosDelGrupo)
	
		promedioDatosPreguntas.append(promedioPregunta)
	
		promedioGrupo = 0
		for cadaPromedio in promedioDatosPreguntas:
			for x in range(cantidadPreguntas):
				if x in cadaPromedio:
					promedioGrupo = cadaPromedio[x] + promedioGrupo
		promedioGrupo = promedioGrupo/len(promedioDatosPreguntas)


	ctx = { #'ModuloAlumno':modulo,
			'PromediosPreguntas':promedioDatosPreguntas,
			}


	return ctx

def datos_grafico_alumno(request,id_encuesta):

	import numpy as np
	import matplotlib.pyplot as plt
	from matplotlib.path import Path
	from matplotlib.spines import Spine
	from matplotlib.projections.polar import PolarAxes
	from matplotlib.projections import register_projection
	import random
	import django
	import datetime

	from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
	from matplotlib.figure import Figure
	from matplotlib.dates import DateFormatter
	import base64
	import cStringIO


	def radar_factory(num_vars, frame='circle'):
		"""Create a radar chart with `num_vars` axes.

		This function creates a RadarAxes projection and registers it.

		Parameters
		----------
		num_vars : int
		    Number of variables for radar chart.
		frame : {'circle' | 'polygon'}
		    Shape of frame surrounding axes.

		"""
		# calculate evenly-spaced axis angles
		theta = 2*np.pi * np.linspace(0, 1-1./num_vars, num_vars)
		# rotate theta such that the first axis is at the top
		theta += np.pi/2

		def draw_poly_patch(self):
			verts = unit_poly_verts(theta)
			return plt.Polygon(verts, closed=True, edgecolor='k')

		def draw_circle_patch(self):
			# unit circle centered on (0.5, 0.5)
			return plt.Circle((0.5, 0.5), 0.5)

		patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
		if frame not in patch_dict:
			raise ValueError('unknown value for `frame`: %s' % frame)

		class RadarAxes(PolarAxes):

			name = 'radar'
			# use 1 line segment to connect specified points
			RESOLUTION = 1
			# define draw_frame method
			draw_patch = patch_dict[frame]

			def fill(self, *args, **kwargs):
				"""Override fill so that line is closed by default"""
				closed = kwargs.pop('closed', True)
				return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

			def plot(self, *args, **kwargs):
				"""Override plot so that line is closed by default"""
				lines = super(RadarAxes, self).plot(*args, **kwargs)
				for line in lines:
					self._close_line(line)

			def _close_line(self, line):
				x, y = line.get_data()
				# FIXME: markers at x[0], y[0] get doubled-up
				if x[0] != x[-1]:
					x = np.concatenate((x, [x[0]]))
					y = np.concatenate((y, [y[0]]))
					line.set_data(x, y)

			def set_varlabels(self, labels):
				self.set_thetagrids(theta * 180/np.pi, labels)

			def _gen_axes_patch(self):
				return self.draw_patch()

			def _gen_axes_spines(self):
				if frame == 'circle':
				    return PolarAxes._gen_axes_spines(self)
				# The following is a hack to get the spines (i.e. the axes frame)
				# to draw correctly for a polygon frame.

				# spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
				spine_type = 'circle'
				verts = unit_poly_verts(theta)
				# close off polygon by repeating first vertex
				verts.append(verts[0])
				path = Path(verts)

				spine = Spine(self, spine_type, path)
				spine.set_transform(self.transAxes)
				return {'polar': spine}

		register_projection(RadarAxes)
		return theta


	def unit_poly_verts(theta):
		"""Return vertices of polygon for subplot axes.

		This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
		"""
		x0, y0, r = [0.5] * 3
		verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
		return verts

	#DATOS
	laEncuesta = Encuesta.objects.get(id=id_encuesta)
	usuario = request.user
	elAlumno = Alumno.objects.get(user=usuario)
	gruposAlumno = elAlumno.grupo.all()
	elGrupo = ''
	#### Si la encuesta no tiene Curso se cae#### Revisar
	for cadaGrupo in gruposAlumno:
		if cadaGrupo.curso == laEncuesta.curso:
			elGrupo = cadaGrupo


	preguntas = laEncuesta.preguntas.all()
	lasPreguntas = []
	for cadaPregunta in preguntas:
		lasPreguntas.append(cadaPregunta.pregunta)

	ctx = {}

	ctx = modulacion_alumno(elAlumno.id,elGrupo.id,id_encuesta)
	promediosPreguntas = []
	promediosAlumno = []

	if 'PromediosPreguntas' in ctx:
		promediosPreguntas = ctx['PromediosPreguntas']

	if 'PromediosElAlumno' in ctx:
		promediosAlumno = ctx['PromediosElAlumno']

	if 'ModuloAlumno' in ctx:
		moduloAlumno = ctx['ModuloAlumno']
		

	print promediosAlumno
	# print promediosPreguntas


	data = {}
	listas = []
	for cadaPregunta in lasPreguntas:
		listas.append(cadaPregunta)
	data['column names'] = listas
	
	data['Modulacion'] =[promediosPreguntas,promediosAlumno]

	print('los datos son:')
	print data



	N = len(listas)
	theta = radar_factory(N, frame='polygon')

	preguntasParaPagina  = data.pop('column names')

	spoke_labels = list(range(1,(len(preguntasParaPagina))+1))
	#data = example_data()

	fig = plt.figure(figsize=(8, 8), facecolor='white')
	fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.15)

	colors = ['b', 'g']
	# Plot the four cases from the example data on separate axes
	for n, title in enumerate(data.keys()):
		ax = fig.add_subplot(2, 2, n+1, projection='radar')
		plt.rgrids([1,2,3,4,5,6])
		ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1), horizontalalignment='center', verticalalignment='center')
		for d, color in zip(data[title], colors):
			ax.plot(theta, d, color=color)
			ax.fill(theta, d, facecolor=color, alpha=0.15)
		ax.set_varlabels(spoke_labels)
		ax.set_xlim([0, 5])
		ax.set_ylim([0, 5])

	# add legend relative to top-left plot
	plt.subplot(2, 2, 1)
	alumnoConModulo = unicode(elAlumno)+' modulo '+str(round(moduloAlumno, 3))
	labels = ('Promedio Curso', alumnoConModulo)
	legend = plt.legend(labels, loc=(0.9, .95), labelspacing=0.1)
	plt.setp(legend.get_texts(), fontsize='small')

	plt.figtext(0.5, 0.965, 'Modulacion comparada con promedio curso', ha='center', color='black', weight='bold', size='large')

	buffer = cStringIO.StringIO()
	fig.savefig(buffer,bbox_inches='tight')
	plt.close(fig)
	grafico = base64.b64encode(buffer.getvalue())
	buffer.close()
	listaPreguntaPromedio = zip(preguntasParaPagina,promediosPreguntas,promediosAlumno)

	contexto = {'grafico':grafico,	
				'IdEncuesta':id_encuesta,
				'Preguntas':listaPreguntaPromedio}

	
	return render(request,'rencuestas/vistagraficos.html',contexto)

def datos_grafico_profesor_view(request,id_encuesta,id_grupo):

	import numpy as np
	import matplotlib.pyplot as plt
	from matplotlib.path import Path
	from matplotlib.spines import Spine
	from matplotlib.projections.polar import PolarAxes
	from matplotlib.projections import register_projection
	import random
	import django
	import datetime

	from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
	from matplotlib.figure import Figure
	from matplotlib.dates import DateFormatter
	import base64
	import cStringIO




	def radar_factory(num_vars, frame='circle'):
		"""Create a radar chart with `num_vars` axes.

		This function creates a RadarAxes projection and registers it.

		Parameters
		----------
		num_vars : int
		    Number of variables for radar chart.
		frame : {'circle' | 'polygon'}
		    Shape of frame surrounding axes.

		"""
		# calculate evenly-spaced axis angles
		theta = 2*np.pi * np.linspace(0, 1-1./num_vars, num_vars)
		# rotate theta such that the first axis is at the top
		theta += np.pi/2

		def draw_poly_patch(self):
			verts = unit_poly_verts(theta)
			return plt.Polygon(verts, closed=True, edgecolor='k')

		def draw_circle_patch(self):
			# unit circle centered on (0.5, 0.5)
			return plt.Circle((0.5, 0.5), 0.5)

		patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
		if frame not in patch_dict:
			raise ValueError('unknown value for `frame`: %s' % frame)

		class RadarAxes(PolarAxes):

			name = 'radar'
			# use 1 line segment to connect specified points
			RESOLUTION = 1
			# define draw_frame method
			draw_patch = patch_dict[frame]

			def fill(self, *args, **kwargs):
				"""Override fill so that line is closed by default"""
				closed = kwargs.pop('closed', True)
				return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

			def plot(self, *args, **kwargs):
				"""Override plot so that line is closed by default"""
				lines = super(RadarAxes, self).plot(*args, **kwargs)
				for line in lines:
					self._close_line(line)

			def _close_line(self, line):
				x, y = line.get_data()
				# FIXME: markers at x[0], y[0] get doubled-up
				if x[0] != x[-1]:
					x = np.concatenate((x, [x[0]]))
					y = np.concatenate((y, [y[0]]))
					line.set_data(x, y)

			def set_varlabels(self, labels):
				self.set_thetagrids(theta * 180/np.pi, labels)

			def _gen_axes_patch(self):
				return self.draw_patch()

			def _gen_axes_spines(self):
				if frame == 'circle':
				    return PolarAxes._gen_axes_spines(self)
				# The following is a hack to get the spines (i.e. the axes frame)
				# to draw correctly for a polygon frame.

				# spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
				spine_type = 'circle'
				verts = unit_poly_verts(theta)
				# close off polygon by repeating first vertex
				verts.append(verts[0])
				path = Path(verts)

				spine = Spine(self, spine_type, path)
				spine.set_transform(self.transAxes)
				return {'polar': spine}

		register_projection(RadarAxes)
		return theta

	def unit_poly_verts(theta):
		"""Return vertices of polygon for subplot axes.

		This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
		"""
		x0, y0, r = [0.5] * 3
		verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
		return verts

	if request.user.is_staff or request.user.is_superuser:
		#DATOS
		laEncuesta = Encuesta.objects.get(id=id_encuesta)
		usuario = request.user
		elProfesor = Profesor.objects.get(user=usuario)
		elGrupo = GruposPorCurso.objects.get(id=id_grupo)
		alumnos = Alumno.objects.all().filter(grupo=elGrupo)
		valorIdMaximo	= Alumno.objects.latest('id')
		listaAlumnos = []
		IdEncuesta = ''
		IdGrupo = ''
		modulacionAlumno = []
		modulosParaGraficos = []	

		if request.method == 'POST':
			print ('Entro \n\n\n\n')
			for i in range(0,valorIdMaximo.id+1):
				if '%s'%i in request.POST:
					elAlumno = Alumno.objects.get(id=i)
					listaAlumnos.append(elAlumno)


					
		# for cadaGrupo in gruposAlumno:
		# 	if cadaGrupo.curso == laEncuesta.curso:
		# 		elGrupo = cadaGrupo

		preguntas = laEncuesta.preguntas.all()
		lasPreguntas = []
		for cadaPregunta in preguntas:
			lasPreguntas.append(cadaPregunta.pregunta)

		ctx = {}

		ctx = modulacion_por_grupo(elGrupo.id,id_encuesta)
		promediosPreguntas = []
		promediosAlumno = []

		if 'PromediosPreguntas' in ctx:
			promediosPreguntas = ctx['PromediosPreguntas']

		# if 'PromediosElAlumno' in ctx:
		# 	promediosAlumno = ctx['PromediosElAlumno']

		# print promediosAlumno


		data = {}
		listas = []
		for cadaPregunta in lasPreguntas:
			listas.append(cadaPregunta)
		data['column names'] = listas
		
		promedioCursoParaGraficos = []
		for cadaPromedio in promediosPreguntas:
			for x in range(len(listas)):
					if x in cadaPromedio:
						promedioCursoParaGraficos.append(round(cadaPromedio[x], 3))
		# print ('los alumnos son:')
		# print listaAlumnos


		data['Modulacion'] =[promedioCursoParaGraficos]

		# print ('La modulacion del curso es')
		# print data['Modulacion']

		for cadaAlumno in listaAlumnos:
			modulacionAlumno = modulacion_alumno(cadaAlumno.id,elGrupo.id,laEncuesta.id)
			modulo = 0
			# print ('La modulacion del alumno es:')
			modulo = modulacionAlumno['ModuloAlumno']
			modulosParaGraficos.append(modulo)
			# print modulacionAlumno
			modulacionAlumno = modulacionAlumno['PromediosElAlumno'] 
			data['Modulacion'].append(modulacionAlumno)


		# print ('La modulacion final es:')
		# print data['Modulacion']
		# print ('modulos para graficos')
		# print (modulosParaGraficos)
		print ('los promedios del curso son:')
		print promedioCursoParaGraficos


		N = len(listas)
		theta = radar_factory(N, frame='polygon')

		preguntasParaPagina  = data.pop('column names')

		spoke_labels = list(range(1,(len(preguntasParaPagina))+1))
		fig = plt.figure(figsize=(12, 12), facecolor='white')
		fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.15)

		colors = ['b', 'g','r','c','m','k','y']
		# Plot the four cases from the example data on separate axes
		for n, title in enumerate(data.keys()):
			ax = fig.add_subplot(2, 2, n+1, projection='radar')
			plt.rgrids([1,2,3,4,5])
			ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1), horizontalalignment='center', verticalalignment='center')
			for d, color in zip(data[title], colors):
				ax.plot(theta, d, color=color)
				ax.fill(theta, d, facecolor=color, alpha=0.15)
			ax.set_varlabels(spoke_labels)
			ax.set_xlim([0, 5])
			ax.set_ylim([0, 5])

		# add legend relative to top-left plot
		plt.subplot(2, 2, 1)

		labels = ['Promedio Curso']
		alumnoConModulo = ''
		for contador, cadaAlumno in enumerate(listaAlumnos):
			alumnoConModulo = str(cadaAlumno)+' modulo '+str(round(modulosParaGraficos[contador], 3))
			labels.append( unicode(alumnoConModulo, 'utf-8') )
		legend = plt.legend(labels, loc=(0.9, .95), labelspacing=0.1)
		plt.setp(legend.get_texts(), fontsize='small')

		plt.figtext(0.5, 0.965, unicode('Modulación','utf-8'), ha='center', color='black', weight='bold', size='large')

		buffer = cStringIO.StringIO()
		fig.savefig(buffer,bbox_inches='tight')
		plt.close(fig)
		grafico = base64.b64encode(buffer.getvalue())
		buffer.close()
		listaPreguntaPromedio = zip(preguntasParaPagina,promedioCursoParaGraficos)
		contexto = {'grafico':grafico,	
					'Alumnos':alumnos,
					'IdEncuesta':id_encuesta,
					'IdGrupo':id_grupo,
					'Preguntas':listaPreguntaPromedio}


		return render(request,'rencuestas/vistagraficos.html',contexto)
	else:
		return HttpResponseRedirect('/')	

def encuesta_terminada(idCurso):
	idEncuestasTerminadas = []
	tipo360 = TipoEncuesta.objects.get(tipoEncuesta=VariableTipoEncuesta[0])
	tipoLiderazgo = TipoEncuesta.objects.get(tipoEncuesta=VariableTipoEncuesta[1])
	elCurso = Curso.objects.get(id=idCurso)
	gruposDelCurso = GruposPorCurso.objects.filter(curso=elCurso)
	encuestasDelCurso = Encuesta.objects.all().filter(curso=elCurso,plantilla=False,tipoEncuesta=tipo360)
	encuestasDelCursoLiderazgo = Encuesta.objects.all().filter(curso=elCurso,plantilla=False,tipoEncuesta=tipoLiderazgo)
	grupoTerminado = False
	alumnoEncuestado = False
	for cadaEncuesta in encuestasDelCurso:
		todasLasRespuestasPorEncuesta = RespuestaEncuesta.objects.filter(encuesta=cadaEncuesta)
		for cadaGrupo in gruposDelCurso:
			print cadaGrupo
			grupoTerminado = False
			losAlumnos = Alumno.objects.all().filter(grupo=cadaGrupo)
			print losAlumnos
			for cadaAlumnoEncuestador in losAlumnos:
				print 'Alumnos'
				print cadaAlumnoEncuestador
				for cadaAlumnoEncuestado in losAlumnos:
					alumnoEncuestado = False
					for cadaRespuesta in todasLasRespuestasPorEncuesta:
						if cadaRespuesta.rutEncuestador == cadaAlumnoEncuestador.rut and cadaRespuesta.rutEncuestado == cadaAlumnoEncuestado.rut:
							alumnoEncuestado = True
						if alumnoEncuestado == True:
							break
					if alumnoEncuestado == False:
						break
				if alumnoEncuestado == False:
					break
			if alumnoEncuestado == False and len(losAlumnos) != 0:
				grupoTerminado = False
				break
			else:
				grupoTerminado = True

		if grupoTerminado == True:
			idEncuestasTerminadas.append(cadaEncuesta)

	for cadaEncuesta in encuestasDelCursoLiderazgo:
		todasLasRespuestasPorEncuesta = RespuestaEncuesta.objects.filter(encuesta=cadaEncuesta)
		for cadaGrupo in gruposDelCurso:
			grupoTerminado = False
			losAlumnos = Alumno.objects.all().filter(grupo=cadaGrupo)
			for cadaAlumnoEncuestador in losAlumnos:
				alumnoEncuestado = False
				for cadaRespuesta in todasLasRespuestasPorEncuesta:
					if cadaRespuesta.rutEncuestador == cadaAlumnoEncuestador.rut:
						alumnoEncuestado = True
					if alumnoEncuestado == True:
						break
				if alumnoEncuestado == False:
					break
				if alumnoEncuestado == False:
					break
			if alumnoEncuestado == False:
				grupoTerminado = False
				break
			else:
				grupoTerminado = True
		if grupoTerminado == True:
			idEncuestasTerminadas.append(cadaEncuesta)
	print idEncuestasTerminadas

	return idEncuestasTerminadas

def encuesta_no_terminada_con_porcentaje_alumnos(id_encuesta):
	diccionario = {}
	laEncuesta = Encuesta.objects.get(id=id_encuesta)
	losGrupos = GruposPorCurso.objects.all().filter(curso=laEncuesta.curso)
	todasLasRespuestas = RespuestaEncuesta.objects.all().filter(encuesta=laEncuesta)
	diccGrupo = []
	# print 'Revisando las encuestas no terminadas'
	# print laEncuesta
	if len(losGrupos) > 0:
		for cadaGrupo in losGrupos:
			alumnosGrupo = Alumno.objects.all().filter(grupo=cadaGrupo)
			# print alumnosGrupo
			# print cadaGrupo
			for cadaAlumno in alumnosGrupo:
				# print ('Revisar Alumnos para porcentaje')
				# print cadaAlumno
				#bandera = False
				contador = len(alumnosGrupo)
				# print contador
				for cadaAlumnoEncuestado in alumnosGrupo:
					# print ('Revisar Alumnos encuestados para porcentaje')
					# print cadaAlumnoEncuestado
					for cadaRespuesta in todasLasRespuestas:
						# print 'entro a mirar'
						if cadaAlumno.rut == cadaRespuesta.rutEncuestador and cadaAlumnoEncuestado.rut == cadaRespuesta.rutEncuestado:
							# print cadaAlumno
							# print ('Entro 1 vez')
							#bandera = True
							contador -= 1
							# print contador
							break
				if contador != 0:
					# print 'Que hay en el diccionario'
					# print cadaAlumno
					diccionario[cadaAlumno] = 100*contador/len(alumnosGrupo)

	return diccionario

def enviar_encuestas_alumno(mensaje,id_alumno):

	if request.user.is_staff or request.user.is_superuser:

		elMensaje = mensaje
		elAlumno = Alumno.objects.get(id=id_alumno)
		correo = [elAlumno.email]

		elMensaje = elMensaje + '\n %s/encuestas/sin/responder/' %(settings.URL_GEN)
		send_mail('Encuesta 360', elMensaje , 'contacto.encuestas.2015@gmail.com', correo )
	else:
		return HttpResponseRedirect('/')

def revisar_encuestas_view(request):
	usuario 			= request.user
	elProfesor 			= Profesor.objects.get(user=usuario)
	cursoElegido		= 0
	muchosCursos		= Curso.objects.all().filter(profesor=elProfesor)
	todosLosAlumnos		= Alumno.objects.all()
	idEncuestas			= []
	idCursoInicial		= ''
	idTipoElegido 		= ''
	todasLasEncuestas 	= []
	encuestasTerminadas = []
	encuestasNoTerminadas = []
	infoEncuestasNoTerminadas = []
	gruposDelCurso = []
	gruposConAlumnos = []
	gruposAlumno = []
	bandera = False
	encuesta360 = False
	diccionario = {}
	tipoElegido = ''

	if request.user.is_authenticated():  # verifica usuario
		# Posteo			
		if request.method == "POST":	# revisa el método de envío de datos	
			cursoConSemestre = []
			nombreCursoDividido = []
			if 'elCurso' in request.POST:
				tipoDeEncuesta 		= TipoEncuesta.objects.all()
				
				idCursoElegido = request.POST['elCurso']
							
				cursoElegido = Curso.objects.get(id=idCursoElegido)
				idCursoInicial = cursoElegido.id
				if 'elTipoEncuesta' in request.POST:
					tipoElegido = TipoEncuesta.objects.get(id=request.POST['elTipoEncuesta'])
					idTipoElegido = tipoElegido.id

					todasLasEncuestas = Encuesta.objects.all().filter(plantilla=False,tipoEncuesta=tipoElegido,curso=muchosCursos)

					encuestasTerminadas = encuesta_terminada(idCursoElegido)
				
					for cadaEncuesta in encuestasTerminadas:
						if cadaEncuesta.tipoEncuesta != tipoElegido:
							encuestasTerminadas.remove(cadaEncuesta)

					gruposDelCurso = GruposPorCurso.objects.all().filter(curso=cursoElegido)


					for cadaGrupo in gruposDelCurso:
						for cadaAlumno in todosLosAlumnos:
							bandera = False
							gruposAlumno = cadaAlumno.grupo.all()
							for cadaGrupoDelAlumno in gruposAlumno:
								if cadaGrupoDelAlumno == cadaGrupo:
									gruposConAlumnos.append(cadaGrupo)
									bandera = True
									break
							if bandera == True:
								break
							
					for cadaEncuesta in todasLasEncuestas:
						bandera = False
						for cadaEncuestaTerminada in encuestasTerminadas:
							if cadaEncuesta == cadaEncuestaTerminada:
								bandera = True
								break
						if bandera == False:
							encuestasNoTerminadas.append(cadaEncuesta)
							if len(encuesta_no_terminada_con_porcentaje_alumnos(cadaEncuesta.id)) != 0:
								#infoEncuestasNoTerminadas.append(encuesta_no_terminada_con_porcentaje_alumnos(cadaEncuesta.id))
								infoEncuestasNoTerminadas = encuesta_no_terminada_con_porcentaje_alumnos(cadaEncuesta.id)
								diccionario[cadaEncuesta] = infoEncuestasNoTerminadas

			
			## Agregar envío encuesta acá directamente desde un formulario que se creará bajo los porcentajes...
			if 'elAlumno' in request.POST and 'mensaje' in request.POST:
				enviar_encuestas_alumno(request.POST['mensaje'],request.POST['elAlumno'])
			if 'laEncuesta' in request.POST:
				encuestaObtenida = Encuesta.objects.get(id=request.POST['laEncuesta'])
				for llave,valor in diccionario.iteritems():
					

					if llave == encuestaObtenida:
						for cadaAlumno,porcentaje in valor.iteritems():
							mensaje = "Usted no ha terminado de responder la encuesta 360"
							enviar_encuestas_alumno(mensaje,cadaAlumno.id)
	
			
			if tipoElegido != '' and tipoElegido.tipoEncuesta == VariableTipoEncuesta[0]:
				encuesta360 = True
			ctx = {	'Cursos':muchosCursos,
					'Encuestas':todasLasEncuestas,
					'idCursoInicial':idCursoInicial,
					'idTipoInicial':idTipoElegido,
					'EncuestasTerminadas':encuestasTerminadas,
					'EncuestasNoTerminadas':encuestasNoTerminadas,
					'GruposDelCurso':gruposConAlumnos,
					'DatosEncuestasNoTerminadas':diccionario,
					'TiposEncuesta':tipoDeEncuesta,
					'Encuesta360':encuesta360,
					}

		else:
			ctx = {	'Cursos':muchosCursos,
				'Encuestas':todasLasEncuestas,
				'idCursoInicial':idCursoInicial,
				'EncuestasTerminadas':encuestasTerminadas,
				'EncuestasNoTerminadas':encuestasNoTerminadas,
				'GruposDelCurso':gruposConAlumnos,
				'DatosEncuestasNoTerminadas':diccionario,
				}

		return render_to_response('rencuestas/resultadoencuestaporcurso.html',ctx,context_instance=RequestContext(request))

def encuesta_liderazgo_view(request,id_encuesta,id_curso):
	laEncuesta 	= Encuesta.objects.get(id=id_encuesta)
	elCurso 	= Curso.objects.get(id=id_curso)
	todosLosAlumnos = Alumno.objects.all()
	alumnosDelCurso = []

	datosEncuesta 	= {}
	evaluaciones = []

	if request.user.is_staff or request.user.is_superuser:
		todosLosGrupos = GruposPorCurso.objects.all().filter(curso=elCurso)
		todasLasRespuestas = RespuestaEncuesta.objects.all().filter(encuesta=laEncuesta)

		for cadaGrupo in todosLosGrupos:
			for cadaAlumno in todosLosAlumnos:
				for cadaGrupoDelAlumno in cadaAlumno.grupo.all():
					if cadaGrupoDelAlumno == cadaGrupo:
						alumnosDelCurso.append(cadaAlumno)
						break
		alumnosDelCurso = list(set(alumnosDelCurso))

		for i,cadaRespuesta in enumerate(todasLasRespuestas):
			listaParaDicc = []
			listaParaDicc.append(Alumno.objects.get(rut=cadaRespuesta.rutEncuestador))
			for lasRespuestas in cadaRespuesta.respuestas:
				res = re.sub('\D','', lasRespuestas)
				if res != '':
					nuevoRes = list(res)
				 	for n in nuevoRes:
				 		listaParaDicc.append(float(n))
			valorTemporal = listaParaDicc.pop()
			listaParaDicc.append(Alumno.objects.get(rut=cadaRespuesta.rutEncuestado))
			listaParaDicc.append(valorTemporal)
			datosEncuesta[i] = listaParaDicc

			for cadaEncuesta,valor in datosEncuesta.iteritems():
				for cadaValor in valor:
					print cadaValor

	
		ctx = {	'Tabla':datosEncuesta,}

		return render_to_response('rencuestas/resultadoencuestaliderazgo.html',ctx,context_instance=RequestContext(request))

def datos_grafico_profesor_curso_view(request,id_encuesta,id_curso):

	import numpy as np
	import matplotlib.pyplot as plt
	from matplotlib.path import Path
	from matplotlib.spines import Spine
	from matplotlib.projections.polar import PolarAxes
	from matplotlib.projections import register_projection
	import random
	import django
	import datetime

	from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
	from matplotlib.figure import Figure
	from matplotlib.dates import DateFormatter
	import base64
	import cStringIO




	def radar_factory(num_vars, frame='circle'):
		"""Create a radar chart with `num_vars` axes.

		This function creates a RadarAxes projection and registers it.

		Parameters
		----------
		num_vars : int
		    Number of variables for radar chart.
		frame : {'circle' | 'polygon'}
		    Shape of frame surrounding axes.

		"""
		# calculate evenly-spaced axis angles
		theta = 2*np.pi * np.linspace(0, 1-1./num_vars, num_vars)
		# rotate theta such that the first axis is at the top
		theta += np.pi/2

		def draw_poly_patch(self):
			verts = unit_poly_verts(theta)
			return plt.Polygon(verts, closed=True, edgecolor='k')

		def draw_circle_patch(self):
			# unit circle centered on (0.5, 0.5)
			return plt.Circle((0.5, 0.5), 0.5)

		patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
		if frame not in patch_dict:
			raise ValueError('unknown value for `frame`: %s' % frame)

		class RadarAxes(PolarAxes):

			name = 'radar'
			# use 1 line segment to connect specified points
			RESOLUTION = 1
			# define draw_frame method
			draw_patch = patch_dict[frame]

			def fill(self, *args, **kwargs):
				"""Override fill so that line is closed by default"""
				closed = kwargs.pop('closed', True)
				return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

			def plot(self, *args, **kwargs):
				"""Override plot so that line is closed by default"""
				lines = super(RadarAxes, self).plot(*args, **kwargs)
				for line in lines:
					self._close_line(line)

			def _close_line(self, line):
				x, y = line.get_data()
				# FIXME: markers at x[0], y[0] get doubled-up
				if x[0] != x[-1]:
					x = np.concatenate((x, [x[0]]))
					y = np.concatenate((y, [y[0]]))
					line.set_data(x, y)

			def set_varlabels(self, labels):
				self.set_thetagrids(theta * 180/np.pi, labels)

			def _gen_axes_patch(self):
				return self.draw_patch()

			def _gen_axes_spines(self):
				if frame == 'circle':
				    return PolarAxes._gen_axes_spines(self)
				# The following is a hack to get the spines (i.e. the axes frame)
				# to draw correctly for a polygon frame.

				# spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
				spine_type = 'circle'
				verts = unit_poly_verts(theta)
				# close off polygon by repeating first vertex
				verts.append(verts[0])
				path = Path(verts)

				spine = Spine(self, spine_type, path)
				spine.set_transform(self.transAxes)
				return {'polar': spine}

		register_projection(RadarAxes)
		return theta

	def unit_poly_verts(theta):
		"""Return vertices of polygon for subplot axes.

		This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
		"""
		x0, y0, r = [0.5] * 3
		verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
		return verts

	if request.user.is_staff or request.user.is_superuser:
		#DATOS
		laEncuesta = Encuesta.objects.get(id=id_encuesta)
		usuario = request.user
		elProfesor = Profesor.objects.get(user=usuario)
		elCurso = Curso.objects.get(id=id_curso)
		todosLosGruposCurso = GruposPorCurso.objects.all().filter(curso=elCurso)
		valorIdMaximo	= GruposPorCurso.objects.latest('id')
		IdEncuesta = ''
		IdGrupo = ''
		modulacionAlumno = []
		modulosParaGraficos = []
		modulacionDelGrupo = []
		modulacionGrupo =[]
		listaGrupos=[]	
		todosLosAlumnos=[]
		todosLosGrupoFiltrados = []

		if request.method == 'POST': #### Para cambiar los datos del gráfico
			for i in range(0,valorIdMaximo.id+1):
				if '%s'%i in request.POST:
					elGrupo = GruposPorCurso.objects.get(id=i)
					listaGrupos.append(elGrupo)


		preguntas = laEncuesta.preguntas.all()
		lasPreguntas = []
		for cadaPregunta in preguntas:
			lasPreguntas.append(cadaPregunta.pregunta)

		for cadaGrupo in todosLosGruposCurso:
			todosLosAlumnos = Alumno.objects.all().filter(grupo=cadaGrupo)
			if len(todosLosAlumnos) != 0:
				todosLosGrupoFiltrados.append(cadaGrupo)
				todosLosAlumnos = []
		todosLosGruposCurso = todosLosGrupoFiltrados
		ctx = {}

		for cadaGrupo in todosLosGruposCurso:
			ctx[cadaGrupo] = modulacion_por_grupo(cadaGrupo.id,id_encuesta)



		# ctx = modulacion_por_grupo(elGrupo.id,id_encuesta) ## Recive un diccionario que tiene el número de la pregunta y el promedio
		promediosPreguntas = []
		diccionarioPromedioPregunta = {}
		promediosAlumno = []

		data = {}
		listas = []
		for cadaPregunta in lasPreguntas:
			listas.append(cadaPregunta)
		data['column names'] = listas
		for x in range(len(listas)):
			diccionarioPromedioPregunta[x]=0
		

		
		for key,promedioPreguntaGrupo in ctx.iteritems():
			for cadaPromedio in promedioPreguntaGrupo['PromediosPreguntas']:
				# print cadaPromedio
				for x in range(len(listas)):
					if x in cadaPromedio:
						# print cadaPromedio[x]
						diccionarioPromedioPregunta[x] = diccionarioPromedioPregunta[x] + cadaPromedio[x] #### arreglar esto... encontrar la forma de poder guardar en un diccionario
		
		print len(todosLosGruposCurso)
		for x in range(len(listas)):
			diccionarioPromedioPregunta[x] = (diccionarioPromedioPregunta[x]/len(todosLosGruposCurso))
		print diccionarioPromedioPregunta


		
		promedioCursoParaGraficos = []

		for x in range(len(listas)):
			promedioCursoParaGraficos.append(diccionarioPromedioPregunta[x])
		# print promedioCursoParaGraficos
		# print listaAlumnos


		data['Modulacion'] =[promedioCursoParaGraficos]

		# print ('La modulacion del curso es')
		# print data['Modulacion']

		for cadaGrupo in listaGrupos:
			modulacionGrupo = []
			modulacionDelGrupo = modulacion_por_grupo(cadaGrupo.id,laEncuesta.id)
			modulacionDelGrupo = modulacionDelGrupo['PromediosPreguntas']
			print 'Modulos por cada Grupo'
			print modulacionDelGrupo
			for valor in modulacionDelGrupo:
				for llave,promedio in valor.iteritems():
					print 'entro'
					modulacionGrupo.append(promedio)
			print 'Modulacion por grupo'
			print modulacionGrupo
			data['Modulacion'].append(modulacionGrupo)
			

		N = len(listas)
		theta = radar_factory(N, frame='polygon')

		preguntasParaPagina  = data.pop('column names')

		spoke_labels = list(range(1,(len(preguntasParaPagina))+1))
		fig = plt.figure(figsize=(12, 12), facecolor='white')
		fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.15)

		colors = ['b', 'g','r','c','m','k','y']
		# Plot the four cases from the example data on separate axes
		for n, title in enumerate(data.keys()):
			ax = fig.add_subplot(2, 2, n+1, projection='radar')
			plt.rgrids([1,2,3,4,5])
			ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1), horizontalalignment='center', verticalalignment='center')
			for d, color in zip(data[title], colors):
				ax.plot(theta, d, color=color)
				ax.fill(theta, d, facecolor=color, alpha=0.15)
			ax.set_varlabels(spoke_labels)
			ax.set_xlim([0, 5])
			ax.set_ylim([0, 5])

		# add legend relative to top-left plot
		plt.subplot(2, 2, 1)

		labels = ['Promedio Curso']
		grupoParaEtiqueta = ''
		for contador, cadaGrupo in enumerate(listaGrupos):
			grupoParaEtiqueta = str(cadaGrupo)
			labels.append( unicode(grupoParaEtiqueta, 'utf-8') )
		legend = plt.legend(labels, loc=(0.9, .95), labelspacing=0.1)
		plt.setp(legend.get_texts(), fontsize='small')

		plt.figtext(0.5, 0.965, unicode('Modulación','utf-8'), ha='center', color='black', weight='bold', size='large')

		buffer = cStringIO.StringIO()
		fig.savefig(buffer,bbox_inches='tight')
		plt.close(fig)
		grafico = base64.b64encode(buffer.getvalue())
		buffer.close()
		listaPreguntaPromedio = zip(preguntasParaPagina,promedioCursoParaGraficos)
		contexto = {'grafico':grafico,	
					'Grupos':todosLosGruposCurso,
					'IdEncuesta':id_encuesta,
					# 'IdGrupo':id_grupo,
					'Preguntas':listaPreguntaPromedio}

		return render(request,'rencuestas/vistagraficosporgrupo.html',contexto)
	else:
		return HttpResponseRedirect('/')				

def agregar_alumno_por_archivo(elNombre,elApellido,elRut,elEmail):

	todosLosAlumnos = Alumno.objects.all()
	todosLosUsuarios = User.objects.all()
	todosLosProfesores = Profesor.objects.all()
	existeUsuario = False
	existeRut	= False
	datoRepetido = ''
	a = Alumno()
	a.nombre 	= elNombre
	a.apellido 	= elApellido
	a.rut 		= elRut
	a.email		= elEmail
	a.status	= True
	username	= elNombre+elApellido
	for cadaAlumno in todosLosAlumnos:
		if cadaAlumno.rut == a.rut:
			existeRut = True
			break
	if existeRut == False:
		for cadaProfesor in todosLosProfesores:
			if cadaProfesor.rut == a.rut:
				existeRut = True
				break
	for cadaUsuario in todosLosUsuarios:
		if cadaUsuario.username == username:
			existeUsuario = True
			break # Dance
	if existeRut == False and existeUsuario == False:
		user = User.objects.create_user(username, elEmail, elRut)
		a.user = user
		a.save()
	else:
		if existeRut == True:
			datoRepetido = 'RUT '
		if existeUsuario == True:
			datoRepetido = datoRepetido + 'y usuario '
		return ('Existe ' + datoRepetido + 'de ' + username)
	return 'No esta'

def importar_datos_csv(request):
	erroresSubida = []
	ctx = {'Estado':erroresSubida}
	if request.user.is_staff or request.user.is_superuser:
		
		estado = ''
		if request.method=="POST":
			if request.FILES:
				csvfile = request.FILES['csv_file']
				reader = csv.reader(csvfile)
				for row in reader:
					estado = agregar_alumno_por_archivo(row[0],row[1],row[2],row[3])
					if estado != 'No esta':
						erroresSubida.append(estado)
				csvfile.close()		
	return render_to_response('rencuestas/importardatos.html',ctx,context_instance=RequestContext(request))
	