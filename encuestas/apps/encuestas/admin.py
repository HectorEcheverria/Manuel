from django.contrib	import admin
#from encuestas.apps.encuestas.models	import curso,alumno,preguntaEncuesta,profesor,gruposPorCurso,encuesta
from encuestas.apps.encuestas.models	import *

admin.site.register(Curso)
admin.site.register(Alumno)
admin.site.register(PreguntaEncuesta)
admin.site.register(Profesor)
admin.site.register(GruposPorCurso)
admin.site.register(Encuesta)
admin.site.register(RespuestaEncuesta)
admin.site.register(PreguntaLibre)
admin.site.register(TipoEncuesta)
admin.site.register(JefesDeGrupo)