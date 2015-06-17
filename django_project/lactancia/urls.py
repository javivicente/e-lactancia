# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
## EN CASTELLANO
    # ex: /
    url(r'^$', views.landing, name='landing'),
    url(r'^buscar$', views.buscar, name='buscar')
]

'''
    # url(r'^resultado$', views.primer_resultado, name='primer_resultado'),
    # url(r'^alertas$', views.alerta_riesgos, name='alerta_riesgos'),
    # url(r'^creditos$', views.creditos, name='creditos'),
    # url(r'^estadisticas$', views.estadisticas, name='estadisticas'),
    # url(r'^estadisticas_ES$', views.estadisticas_ES, name='estadisticas_ES'),
    # url(r'^lista_negra$', views.lista_negra, name='lista_negra'),
    # url(r'^donativos$', views.donativos, name='donativos'),
    # url(r'^donativo_exito$', views.donativo_exito, name='donativo_exito'),
    # url(r'^donativo_cancelado$', views.donativo_cancelado, name='donativo_cancelado'),
    # url(r'^boletin_error$', views.boletin_error, name='boletin_error'),
    # url(r'^cookies_es$', views.cookies_es, name='cookies_es'),
    # url(r'^privacidad$', views.privacidad, name='privacidad'),
    # url(r'^aviso_legal$', views.aviso_legal, name='aviso_legal'),

'''
'''                   
    # ex: /detalleproducto/5/
    url(r'^producto/(?P<producto_id>\d+)$', views.detalle_p, name='detalle_p'),
    # ex: /detalle_alias/5/
    url(r'^alias_es/(?P<alias_id>\d+)$', views.detalle_ap, name='detalle_ap'),
    # ex: /detale_grupo/5/
    url(r'^grupo/(?P<grupo_id>\d+)$', views.detalle_g, name='detalle_g'),
    # ex: /detalle_marca/5/
    url(r'^marca/(?P<marca_id>\d+)$', views.detalle_m, name='detalle_m'),
'''                   

