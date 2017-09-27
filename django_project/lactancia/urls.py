# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
## EN CASTELLANO
    # ex: /
    url(r'^$', views.landing, name='landing'),
    url(r'^buscar/$', views.buscar, name='buscar'),
    url(r'^cookies/$', views.cookies, name='cookies'),
    url(r'^privacidad/$', views.privacidad, name='privacidad'),
    url(r'^aviso_legal/$', views.aviso_legal, name='aviso_legal'),
    url(r'^avales/$', views.avales, name='avales'), 
    url(r'^patrocinadores/$', views.patrocinadores, name='patrocinadores'), 
    url(r'^donativos/$', views.donativos, name='donativos'), 
    url(r'^donativo_exito/$', views.donativo_exito, name='donativo_exito'),
    url(r'^donativo_cancelado/$', views.donativo_cancelado, name='donativo_cancelado'),
    url(r'^boletin_error/$', views.boletin_error, name='boletin_error'),
    url(r'^alertas/$', views.alerta_riesgos, name='alerta_riesgos'),
    url(r'^creditos/$', views.creditos, name='creditos'),
    url(r'^lista_negra/$', views.lista_negra, name='lista_negra'),
    url(r'^limpia_cache/$', views.limpia_cache, name='limpia_cache'),
    url(r'^estadisticas/$', views.estadisticas, name='estadisticas'),
    url(r'^estadisticas_ES/$', views.estadisticas_ES, name='estadisticas_ES'),
    url(r'^producto/(?P<producto_id>\d+)/$', views.detalle_p, name='detalle_p'),
    url(r'^grupo/(?P<grupo_id>\d+)/$', views.detalle_g, name='detalle_g'),
    url(r'^marca/(?P<marca_id>\d+)/$', views.detalle_m, name='detalle_m'),
    url(r'^sinonimo/(?P<alias_id>\d+)/$', views.detalle_ap, name='detalle_ap'),
    url(r'^otra_escritura/(?P<otra_escritura_id>\d+)/$', views.detalle_oe, name='detalle_oe'),
    url(r'^download-citation/$', views.download_citation, name='download_citation'),
    url(r'^API/get_list_of_terms$', views.get_list_of_terms, name='get_list_of_terms'),
    url(r'^API/get_date_last_update_list_of_terms$', views.get_date_last_update_list_of_terms, name='get_date_last_update_list_of_terms'),
    url(r'^API/get_term/(?P<prod_id>\d+)$', views.get_term, name='get_term'),
    
    
]

'''
    # url(r'^resultado$', views.primer_resultado, name='primer_resultado'),
    # 
    # 
    # url(r'^estadisticas$', views.estadisticas, name='estadisticas'),
    # url(r'^estadisticas_ES$', views.estadisticas_ES, name='estadisticas_ES'),
    # url(r'^lista_negra$', views.lista_negra, name='lista_negra'),
    # url(r'^donativos$', views.donativos, name='donativos'),
    # url(r'^donativo_exito$', views.donativo_exito, name='donativo_exito'),
    # url(r'^donativo_cancelado$', views.donativo_cancelado, name='donativo_cancelado'),
    # url(r'^boletin_error$', views.boletin_error, name='boletin_error'),
    # url(r'^cookies_es$', views.cookies_es, name='cookies_es'),
    # url(r'^privacidad$', views.privacidad, name='privacidad'),
    # 

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

