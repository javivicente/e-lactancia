from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from lactancia import views
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
   
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('lactancia.urls', namespace="lactancia")),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^', include('ratings.urls')),
    url(r'^select2/', include('django_select2.urls')),
)

    

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
              {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
              {'document_root': settings.STATIC_ROOT}),   
        ) + static('/', document_root='static/')
