from django.conf.urls import patterns, include, url
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin,auth
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'encuestas.views.home', name='home'),
    # url(r'^encuestas/', include('encuestas.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
  	url(r'^',include('encuestas.apps.home.urls')),
  	url(r'^',include('encuestas.apps.encuestas.urls')),
    url(r'^',include('password_reset.urls')),
    # url(r'^user/password/reset/$','django.contrib.auth.views.password_reset',{'post_reset_redirect' : '/user/password/reset/done/'}, name='password_reset'),
    # (r'^user/password/reset/done/$','django.contrib.auth.views.password_reset_done'),
    # (r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$','django.contrib.auth.views.password_reset_confirm',{'post_reset_redirect':'/user/password/done/'}),
    # (r'^user/password/done/$','django.contrib.auth.views.password_reset_complete'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
)
