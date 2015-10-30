from django.conf.urls import patterns,url,include


urlpatterns = patterns('encuestas.apps.encuestas.views',
	url(r'^agregar/pregunta/$','agregar_pregunta_view', name='vista_agregar_pregunta'),
	url(r'^agregar/alumno/$','agregar_alumno_view', name='vista_agregar_alumno'),
	url(r'^agregar/profesor/$','agregar_profesor_view', name='vista_agregar_profesor'),
	url(r'^agregar/curso/$','agregar_curso_view', name='vista_agregar_curso'),
	url(r'^agregar/grupo/$','agregar_grupo_view', name='vista_agregar_grupo'),
	url(r'^agregar/encuesta/$','agregar_encuesta_con_preguntas_view', name='vista_agregar_encuesta'),
	url(r'^agregar/alumnos/grupos/$','agregar_alumnos_a_grupo_por_curso_view', name='vista_agregar_alumnos_a_grupo_por_curso'),
	url(r'^agregar/tipo/encuesta/$','tipo_de_encuesta_view', name='vista_tipo_encuesta'),
	url(r'^agregar/pregunta/libre/$','agregar_pregunta_libre_view', name='vista_agregar_pregunta_libre'),
	url(r'^agregar/grupo/alumno/(?P<id_profesor>.*)/$','agregar_grupo_a_alumno_view', name='vista_agregar_grupo_a_alumno_view'),
	url(r'^agregar/jefe/grupo/(?P<id_grupo>.*)/$','agregar_jefe_de_grupo_view', name='vista_agregar_jefe_de_grupo'),
	
	url(r'^editar/pregunta/libre/(?P<id_pregunta>.*)/$','editar_pregunta_libre_view', name='vista_editar_pregunta_libre'),
	url(r'^editar/pregunta/(?P<id_pregunta>.*)/$','editar_pregunta_view', name='vista_editar_pregunta'),
	url(r'^editar/encuesta/(?P<id_alumno>.*)/$','eleccion_editar_encuesta_view', name='vista_eleccion_editar_encuesta_view'),
	url(r'^edicion/encuesta/(?P<id_curso>.*)/(?P<id_encuesta>.*)/$','editar_encuesta_view', name='vista_editar_encuesta'),
	url(r'^nuevo/editar/encuesta/$','editar_encuestas_con_preguntas_view', name='vista_editar_encuestas_con_preguntas'),
	
	url(r'^mostrar/preguntas/$','mostrar_preguntas_view', name='vista_mostrar_preguntas'),
	url(r'^mostrar/curso/(?P<id_profesor>.*)/$','mostrar_curso_view', name='vista_mostrar_curso'),
	url(r'^mostrar/respuesta/grupo/(?P<id_encuesta>.*)/(?P<id_curso>.*)/(?P<id_grupo>.*)/$','mostrar_resultados_grupo_view', name='vista_mostrar_resultados_grupo'),
	
	url(r'^enviar/encuesta/$','datos_enviar_encuesta_curso_view', name='vista_datos_enviar_encuesta_curso'),
	url(r'^enviar/encuestas/(?P<id_encuesta>.*)/$','enviar_encuestas_curso_view', name='vista_enviar_encuestas_curso'),
	
	url(r'^elegir/encuesta/$','eleccion_encuesta_alumno_view', name='vista_eleccion_encuesta_alumno'),
	url(r'^seleccionar/encuesta/(?P<id_encuesta>.*)/$','almacenar_encuesta_sesion', name='vista_almacenar_encuesta_sesion'),
	url(r'^seleccionar/curso/(?P<id_curso>.*)/$','almacenar_curso_sesion', name='vista_almacenar_curso_sesion'),
	
	url(r'^responder/encuesta/(?P<id_curso>.*)/(?P<id_encuesta>.*)/$','responder_encuesta_view', name='vista_responder_encuesta'),
	url(r'^crear/encuesta/$','crear_encuesta_profesor_view', name='vista_crear_encuesta_profesor'),
	url(r'^eliminar/pregunta/(?P<id_pregunta>.*)/$','eliminar_pregunta_encuesta_view', name='vista_eliminar_pregunta_encuesta'),
	
	url(r'^encuestas/sin/responder/$','nuevo_eleccion_encuesta_alumno_view', name='vista_nuevo_eleccion_encuesta_alumno'),
	
	url(r'^feedback/$','mostrar_encuestas_finalizadas_view', name='vista_mostrar_encuestas_finalizadas'),
	url(r'^feedback/grafico/(?P<id_encuesta>.*)/$','datos_grafico_alumno', name='vista_datos_grafico'),
	url(r'^feedback/curso/grafico/(?P<id_encuesta>.*)/(?P<id_curso>.*)/$','datos_grafico_profesor_curso_view', name='vista_datos_grafico_profesor_curso'),

	url(r'^revisar/encuestas/$','revisar_encuestas_view', name='vista_revisar_encuestas'),
	url(r'^feedback/profesor/grafico/(?P<id_encuesta>.*)/(?P<id_grupo>.*)/$','datos_grafico_profesor_view', name='vista_datos_grafico_profesor'),
	url(r'^resultados/encuesta/liderazgo/(?P<id_encuesta>.*)/(?P<id_curso>.*)/$','encuesta_liderazgo_view', name='vista_encuesta_liderago'),
	



	#url(r'^feedback/2/profesor/grafico/(?P<id_encuesta>.*)/(?P<id_grupo>.*)/$','datos_grafico_profesor_2_view', name='vista_datos_grafico_profesor_2'),
	)			