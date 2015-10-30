from django.db import models
from django.contrib.auth.models import User

class perfilUsuario(models.Model):
	
	def url(self,filename):
		ruta	=	"MultimediaData/Usuarios/%s/%s"%(self.user.username, filename)
		return ruta

	user	=	models.OneToOneField(User, unique=True)
	foto	=	models.ImageField(upload_to=url,null=True,blank=True)
	correo	=	models.EmailField(max_length=200)#Validar a correo??

	def __unicode__(self):
		return self.user.username
