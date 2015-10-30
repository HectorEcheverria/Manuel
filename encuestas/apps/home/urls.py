from django.conf.urls import patterns,url

urlpatterns = patterns('encuestas.apps.home.views',
	url(r'^$','index_view', name='vista_principal'),
	url(r'^encuestas/$', 'encuestas_view', name='vista_encuestas'),
	url(r'^preguntas/$', 'preguntas_view', name='vista_preguntas'),
	url(r'^contacto/$','contacto_view', name='vista_contacto'),
	url(r'^login/$','login_view', name='vista_login'),
	url(r'^logout/$','logout_view', name='vista_logout'),
	url(r'^editar/perfil/$','editar_perfil_view',name='vista_editar_perfil')	
)