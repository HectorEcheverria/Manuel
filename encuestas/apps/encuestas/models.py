# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import unicodedata
import string
 
 
def content_file_name(instance, filename):
    nombre = instance.nombre+instance.apellido+'.'+filename.split('.')[-1]
    nombre = nombre.replace (" ", "")
    nombre = ''.join(x for x in unicodedata.normalize('NFKD', nombre) if x in string.ascii_letters).lower()
    return '/'.join(['MultimediaData/Usuarios', nombre, nombre])

class Profesor(models.Model):

	
	user			= models.OneToOneField(User, unique=True)
	foto			= models.ImageField(upload_to=content_file_name,null=True,blank=True)
	nombre 			= models.CharField(max_length=100)
	apellido		= models.CharField(max_length=100)
	rut 			= models.CharField(max_length=100,unique=True)
	email			= models.EmailField(max_length=200)
	status			= models.BooleanField(default=True)

	class Meta:
		permissions = (
			('esProfesor', 'Es Profesor'),
			)
		

	def __unicode__(self):
		return '%s %s' %(self.nombre,self.apellido)

class Curso(models.Model):
	nombrecurso		=models.CharField(max_length=200)
	semestre		=models.CharField(max_length=200)
	year 			=models.CharField(max_length=50)
	status			=models.BooleanField(default=True)
	profesor		=models.ForeignKey(Profesor) 

	def __unicode__(self):
		codigo	= "%s %s %s" %(self.nombrecurso,self.semestre,self.year)
		return codigo

class TipoEncuesta(models.Model):
	tipoEncuesta = models.CharField(max_length=200)

	def __unicode__(self):
		return self.tipoEncuesta

class PreguntaEncuesta(models.Model):	
	pregunta 		=models.CharField(max_length=200)
	descripcionPregunta	=models.TextField(max_length=300)
	respuesta1		=models.TextField(max_length=500)
	respuesta2		=models.TextField(max_length=500)
	respuesta3		=models.TextField(max_length=500)
	respuesta4		=models.TextField(max_length=500)
	respuesta5		=models.TextField(max_length=500)
	status			=models.BooleanField(default=True)

	def __unicode__(self):
		return self.pregunta

class PreguntaLibre(models.Model):	
	pregunta 		=models.CharField(max_length=200)
	descripcion		=models.TextField(max_length=300)
	respuesta1		=models.TextField(max_length=500)

	def __unicode__(self):
		return self.pregunta

class Encuesta(models.Model):
	nombreEncuesta	=models.CharField(max_length=200)	
	descripcion 	=models.CharField(max_length=300)
	curso 			=models.ForeignKey(Curso, null=True,blank=True)
	preguntas 		=models.ManyToManyField(PreguntaEncuesta,blank=True)
	preguntasLibres	=models.ManyToManyField(PreguntaLibre,blank=True)
	tipoEncuesta	=models.ForeignKey(TipoEncuesta,blank=True,null=True,verbose_name='Tipo de Encuesta')
	modulo			=models.FloatField(blank=True,null=True, verbose_name='Módulo')
	plantilla 		=models.BooleanField(default=True)
	detalles		=models.CharField(max_length=300,blank=True, verbose_name='Instancia (nombre único)')
	cerrada 		=models.BooleanField(default=False)
	fechaCreacion	=models.DateField(blank=True,null=True)

	def __unicode__(self):
		return "%s %s" %(self.nombreEncuesta, self.detalles)

class GruposPorCurso(models.Model):
	nombre 			=models.CharField(max_length=200)
	curso 			=models.ForeignKey(Curso)

	def __unicode__(self):
		return "%s %s %s %s" %(self.nombre,self.curso.nombrecurso,self.curso.semestre,self.curso.year)
		
class Alumno(models.Model):

	user			= models.OneToOneField(User, unique=True)
	foto			= models.ImageField(upload_to=content_file_name,null=True,blank=True)
	nombre         	= models.CharField(max_length=200)
	apellido		= models.CharField(max_length=200)
	rut 			= models.CharField(max_length=200,unique=True)
	email			= models.EmailField(max_length=200)
	status			= models.BooleanField(default=True)
	grupo 			= models.ManyToManyField(GruposPorCurso,blank=True)

	class Meta:
		permissions = (
			('esAlumno', 'esAlumno'),
			)
			
	def __unicode__(self):
		return '%s %s' % (self.nombre, self.apellido)

class JefesDeGrupo(models.Model):
	grupo = models.ForeignKey(GruposPorCurso)
	alumno = models.ForeignKey(Alumno)
	
	def __unicode__(self):
		return "%s %s" %(self.grupo, self.alumno)

class RespuestaEncuesta(models.Model):
	idEncuesta		=models.CharField(max_length=200,null=True,blank=True)
	rutEncuestador	=models.CharField(max_length=200)
	rutEncuestado 	=models.CharField(max_length=200)	
	encuesta 		=models.ForeignKey(Encuesta)
	respuestas 		=models.CharField(max_length=200) 
	cursoEncuesta	=models.CharField(max_length=200) # cambiar por un foreingKey
	semestreAnio	=models.CharField(max_length=200)

	def __unicode__(self):
		return 'Encuesta %s detalle %s curso %s semestre y anio %s  - Encuestador %s - Encuestado %s ' %(self.encuesta.nombreEncuesta,self.encuesta.detalles,self.cursoEncuesta,self.semestreAnio, self.rutEncuestador, self.rutEncuestado)

