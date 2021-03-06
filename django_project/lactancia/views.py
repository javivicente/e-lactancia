# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
#from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from lactancia.models import Riesgo, Producto, Alias, Marca, Otras_escrituras, Grupo, Mensaje, LactUser, Visita, Comentario, Bibliografia, Cajita, Aval, Patrocinador, Docs
from lactancia.models import Visita_grupo_total, Visita_grupo_perfil, Visita_producto_total, Visita_producto_perfil, Visita_marca_total, Visita_marca_perfil
from lactancia.models import Visita_alias_total, Visita_alias_perfil, Visita_otras_escrituras_total, Visita_otras_escrituras_perfil
#from lactancia.extra import Lactancia_words
#from lactancia.extra import correct_list
from lactancia.forms import PerfilForm, Subscription, ComentarioForm
#from django.utils.html import escape
from django.utils.safestring import mark_safe
import re
import random
from django.db.models import Q
from ratings.handlers import ratings
from django.core.cache import cache
import sys
from django.utils import timezone
import datetime
from django.template.defaultfilters import date as _date
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from meta.views import Meta
from django.templatetags.static import static

timeout = 60 * 2 # Default cache timeout is 300 (5 mins) use this (1hour) for things that do not change very often
PROJECT_PATH = '/home/django'



def index(request):
    return HttpResponse("Hello, world! This is our first view.")
    
def typeahead_productos():
    PRODUCTOS = cache.get('PRODUCTOS')
    if PRODUCTOS == None:
        productos = Producto.objects.all().distinct().values('nombre_es', 'nombre_en', 'id').order_by('nombre')
        N = len(productos)
        data = list(productos)
        PRODUCTOS = json.dumps(data, ensure_ascii=False).encode('utf8')
        cache.set('PRODUCTOS', PRODUCTOS)
        cache.set('N_productos', N)
    else: 
        N = cache.get('N_productos')
    return PRODUCTOS, N
    
def typeahead_grupos():
    GRUPOS = cache.get('GRUPOS')
    if GRUPOS == None:
        grupos = Grupo.objects.all().distinct().values('nombre_es', 'nombre_en', 'id').order_by('nombre')
        N = len(grupos)
        data = list(grupos)
        GRUPOS = json.dumps(data, ensure_ascii=False).encode('utf8')
        cache.set('GRUPOS', GRUPOS)
        cache.set('N_grupos', N)
    else:
        N = cache.get('N_grupos')
    return GRUPOS, N
    
def typeahead_sinonimos():
    SINONIMOS = cache.get('SINONIMOS')
    if SINONIMOS == None:
        alias = Alias.objects.all().distinct().values('nombre_es', 'nombre_en', 'id').order_by('nombre')
        N = len(alias)
        data = list(alias)
        SINONIMOS = json.dumps(data, ensure_ascii=False).encode('utf8')
        cache.set('SINONIMOS', SINONIMOS)
        cache.set('N_sinonimos', N)
    else:
        N = cache.get('N_sinonimos')
    return SINONIMOS, N

def typeahead_otras_escrituras():
    ESCRITURAS = cache.get('ESCRITURAS')
    if ESCRITURAS == None:
        o_escrit = Otras_escrituras.objects.all().distinct().values('nombre', 'id').order_by('nombre')
        N = len(o_escrit)
        data = list(o_escrit)
        ESCRITURAS = json.dumps(data, ensure_ascii=False).encode('utf8')
        cache.set('ESCRITURAS', ESCRITURAS)
        cache.set('N_escrituras', N)
    else:
        N = cache.get('N_escrituras')
    return ESCRITURAS, N
    
    
    
def typeahead_marcas():
    MARCAS = cache.get('MARCAS')
    if MARCAS == None:
        marcas = Marca.objects.all().distinct().values('nombre_paises_es', 'nombre_paises_en', 'id').order_by('nombre')
        N = len(marcas)
        data = list(marcas)
        '''for i, item in enumerate(data):
            pa_es = Marca.objects.values_list('principios_activos__nombre_es', flat=True).filter(id=data[i]['id'])
            pa_en = Marca.objects.values_list('principios_activos__nombre_en', flat=True).filter(id=data[i]['id'])
            pais_es = Marca.objects.values_list('paises__nombre_es', flat=True).filter(id=data[i]['id'])
            pais_en = Marca.objects.values_list('paises__nombre_en', flat=True).filter(id=data[i]['id'])
            
            data[i]['nombre_es']= data[i]['nombre'] + ' (' 
            data[i]['nombre_en']= data[i]['nombre'] + ' (' 
            for index, princip in enumerate(pa_es):
                if princip:
                    data[i]['nombre_es'] += princip + ' '
                    data[i]['nombre_en'] += pa_en[index] + ' ' 
            data[i]['nombre_es'] += ')'
            data[i]['nombre_en'] += ')'
            #for index, pais in pais_es:
            #    if pais:
            #        data[i]['nombre_es'] += ' ' + pais
            #        data[i]['nombre_es'] += ' ' + pais_en[index]
                        
        '''
        MARCAS = json.dumps(data, ensure_ascii=False).encode('utf8')
        cache.set('MARCAS', MARCAS)
        cache.set('N_marcas', N)
    else:
        N = cache.get('N_marcas')
    return MARCAS, N
    

'''returns the message of active alert(s) for risk level change of a product
    (top button of the top bar)
'''    
def get_alert_risk(context):
    alert_risk = cache.get('alert_risk')
    if alert_risk == None:
        now = timezone.now()
        month = now - datetime.timedelta(days=30)
        alert_risk =  Mensaje.objects.filter(fecha_modificacion__range=[month, now]).exists()    
        cache.set('alert_risk', alert_risk)
        
    context.update({ 'alert_risk': alert_risk, })
    return context
    
'''returns the message of active alert(s) for risk level change of a product
    (top button of the top bar)
'''    
def get_current_aval(context):
    aval = cache.get('aval')
    if aval == None:
        aval =  Aval.objects.filter(visible=True).order_by('?')[0] 
        cache.set('aval', aval)
        
    context.update({ 'aval': aval})
    return context    
    
    
def load_initial_context():
    PRODS, N_prods = typeahead_productos()
    SINON, N_sinon = typeahead_sinonimos()
    GRUPOS, N_grupos = typeahead_grupos()
    MARCAS, N_marcas = typeahead_marcas()
    ESCRITURAS, N_escrituras = typeahead_otras_escrituras()
    N = N_escrituras + N_grupos + N_marcas + N_prods + N_sinon
    context={'PRODUCTOS':    mark_safe(PRODS),
                  'SINONIMOS':    mark_safe(SINON),
                  'GRUPOS':         mark_safe(GRUPOS),
                  'MARCAS':         mark_safe(MARCAS),
                  'ESCRITURAS':   mark_safe(ESCRITURAS),
                  'N': N,

                }
                
    context=get_current_aval(context)
    context=get_alert_risk(context)
    return context 
    
initial_context = load_initial_context()


def set_meta(request,producto=None,grupo=None,marca=None,otra_escritura=None,alias=None):
    
    title =_(u'e-lactancia.org')
    description = _(u'Información sobre compatibilidad de medicamentos y otros productos con la lactancia materna, desarrollada por la Asociación para la Promoción científica y cultural de la Lactancia Materna, APILAM.')
    
    if producto:
        title= producto.nombre + ': ' + _(u'Nivel de riesgo para la lactancia según e-lactancia.org')
        description = producto.comentario
        
    if marca:
        title= marca.nombre + ': ' + _(u'Nivel de riesgo para la lactancia según e-lactancia.org')
        description = marca.obten_riesgo_mas_alto_descripcion()
    
    if alias:
        title= alias.nombre + ': ' + _(u'Nivel de riesgo para la lactancia según e-lactancia.org')
        description = alias.producto_principal.comentario
        
    if otra_escritura:
        title= otra_escritura.nombre + ': ' + _(u'Nivel de riesgo para la lactancia según e-lactancia.org')
        description = otra_escritura.producto_principal.comentario    
    if grupo:
        title= grupo.nombre + ': ' + _(u'Niveles de riesgo para la lactancia según e-lactancia.org')
        description = _(u'Listado de la familia') + ' ' + grupo.nombre + ' ' + _(u'por nivel de riesgo según e-lactancia.org')
    
    current_lang = get_language()
    meta = Meta(
        title=title,
        description= description,
        image= static('img/RRSS-elactancia.jpg') if current_lang == 'es'  else static('img/RRSS-elactancia_EN.jpg'),
        url = request.build_absolute_uri(),
        locale = current_lang,
    )
    
    return meta
    
    
def landing(request):

    last_update = cache.get('prod_last_update')
    if last_update == None:
        last_update = Producto.objects.latest('fecha_modificacion').fecha_modificacion
        cache.set('prod_last_update',last_update)
    
    cajitas = cache.get('cajitas')
    if cajitas == None:
        cajitas = Cajita.objects.filter(visible=True).order_by('order')
        cache.set('cajitas', cajitas)
    cajitas = cache.get('cajitas')
    
    avales = cache.get('avales')
    if avales == None:
        avales = Aval.objects.filter(visible=True).order_by('order')
        cache.set('avales', avales)
    avales = cache.get('avales')
    
    patrocinadores = cache.get('patrocinadores')
    if patrocinadores == None:
        patrocinadores = Patrocinador.objects.filter(visible=True).order_by('order')
        cache.set('patrocinadores', patrocinadores)
    patrocinadores = cache.get('patrocinadores')
    
    span_recomendados = 'col-xs-12'
    num_recomendaciones = len(cajitas) - 3
    if num_recomendaciones == 2:
        span_recomendados = 'col-xs-12 col-sm-6 col-md-6'
    if num_recomendaciones > 2:
        span_recomendados = 'col-xs-12 col-sm-4 col-md-4'
    
    span_sponsors = 'col-xs-12'
    num_sponsors = len(patrocinadores)
    if num_sponsors == 2:
        span_sponsors = 'col-xs-12 col-sm-6'
    if num_sponsors == 3:
        span_sponsors = 'col-xs-12 col-sm-4'
    if num_sponsors == 4:
        span_sponsors = 'col-xs-12 col-sm-3'
    if num_sponsors == 5:
        span_sponsors = 'col-xs-12 col-sm-4'
    if num_sponsors == 6:
        span_sponsors = 'col-xs-12 col-sm-4'
    if num_sponsors >= 7:
        span_sponsors = 'col-xs-12 col-sm-3'
    
    span_avales= 'col-xs-6 col-sm-4'
    
    context = {
                'last_update': last_update,
                'cajitas': cajitas,
                'span_recomendados': span_recomendados,
                'span_sponsors': span_sponsors,
                'span_sponsors': span_sponsors,
                'span_avales': span_avales,
                'avales': avales,
                'patrocinadores': patrocinadores,
                'meta': set_meta(request),
                }
                
    context.update(initial_context)    
    return render(request, 'lactancia/home-b3.html', context)
    
    
    
    
def buscar(request):
    if ('term_id' in request.GET):
        term = request.GET['term_type']
        id = int(request.GET['term_id'])
        if term == 'producto':
            return redirect('lactancia:detalle_p', id)
        elif term == 'grupo':
            return redirect('lactancia:detalle_g', id)
        elif term == 'sinonimo':
            return redirect('lactancia:detalle_ap', id)
        elif term == 'marca':
            return redirect('lactancia:detalle_m', id)
        elif term == 'escritura':
            return redirect('lactancia:detalle_oe', id)
    else:
        here = request.META.get('HTTP_REFERER')
        if here:
            return redirect(here)
        else:
            return redirect('lactancia:landing')
    


'''dynamic calculation of the span of names of the product (alias, trademarks and groups)'''
def calcula_span_product_names(product):
    '''
    # by default, there's only one column (group)...
    span='span12' 

    # if there are alias and trademarks (there will be 3 columns)
    if (product.hay_marcas() and (product.hay_alias() or product.hay_escrituras())):
        span='span4'
    # if there is only trades or alias (there will be 2 columns)
    elif (product.hay_marcas() or (product.hay_alias() or product.hay_escrituras())):
        span='span6'
    '''
    
    ''' Boostrap 3 version'''
    # by default, there's only one column (group)...
    span='col-xs-12 col-md-12' 

    # if there are alias and trademarks (there will be 3 columns)
    if (product.hay_marcas() and (product.hay_alias() or product.hay_escrituras())):
        span='col-xs-12 col-md-4'
    # if there is only trades or alias (there will be 2 columns)
    elif (product.hay_marcas() or (product.hay_alias() or product.hay_escrituras())):
        span='col-xs-12 col-md-6'

        
    return span


'''dynamic calculation of the span for biblio and pharmacokinetics'''
def calcula_span_product_pharma_biblio(product):
    
    '''
    # by default, there's only one column (group)...
    span='span12'

    # if there are phamacokinetics (there will be 2 columns)
    if product.es_principio_activo():
        span='span6'
    '''

    '''Boostrap 3 Version '''
    # by default, there's only one column (group)...
    span='col-md-12'

    # if there are phamacokinetics (there will be 2 columns)
    if product.es_principio_activo():
        span='col-md-6'    
        
    return span


'''dynamic calculation of the span of the table of risk (includes risk, comment, and alternatives)'''
def calcula_span_product_risk(product):
    
    '''
    span = {
        'span_nivel': 'span4',
        'span_nivel_desc': 'span4',
        'span_alternativas': 'span3',
        'span_comment': 'span8'
    }
    '''
        
    # version Bootstrap 3
    span = {
        'span_nivel': 'col-xs-12 col-sm-12 col-md-3',
        'span_alternativas': 'col-xs-12 col-sm-12 col-md-3',
        'span_comment': 'col-xs-12 col-sm-12 col-md-6'
        }
    
    return span


'''dynamic calculation of the span of the active ingredients (in tradenames)'''
def calcula_span_marca(marca):

    
    span = {'span_comentario': 'span0',
            'span_principios': 'span6',
            'span_disclaimer': 'span6'
            }

    #if marca.comentario != '':
    #    span.update({'span_comentario': 'span3'})
    #    span.update({'span_principios': 'span3'})
    return span


    
    
    
    
'''dynamic calculation of the span of risks and related products of a group'''
def calcula_span_grupo(grupo):

    span = calcula_span_block_risk(False)
    span.update({'span_r0': 'span3',
            'span_r1': 'span3',
            'span_r2': 'span3',
            'span_r3': 'span3'})
                
    span.update({'span_risks': 'span8'})
    return span


    
    
''' returns the message of active alert(s) for risk level change of
the list of a product
    (text globe of the profile of the product)
'''
def get_alert_risk_for_producto(product):

    try:
        alert = Mensaje.objects.get(producto=product.id)
    except Mensaje.DoesNotExist:
        return None

    return alert
 

''' returns the message of active alert(s) for risk level change of
the list of products associated to a Marca
    (text globe of the profile of the product)
'''
def get_alert_risk_for_marca(marca):

    prods = marca.principios_activos.all()
    pk_list = [item.pk for item in prods]
    alerts = Mensaje.objects.filter(producto__in=pk_list)
    return alerts

    
''' returns the message of active alert(s) for risk level change of
the list of products associated to a Group
    (text globe of the profile of the product)
'''
def get_alert_risk_for_grupo(grupo):

    prods = Producto.objects.filter(grupo=grupo.pk)
    pk_list = [item.pk for item in prods]
    alerts = Mensaje.objects.filter(producto__in=pk_list)    
    return alerts


    

def get_context_for_product(request, prod):
    timeout = 60 * 60 # Default cache timeout is 300 (5 mins) use this (1hour) for things that do not change very often

    
    help_p_molecular = cache.get('help_p_molecular')
    if help_p_molecular == None:
        help_p_molecular = Mensaje.objects.get(nombre__icontains='peso_molecular')
        cache.set('help_p_molecular',help_p_molecular,timeout)
    help_u_prot = cache.get('help_u_prot')
    if help_u_prot ==None:
        help_u_prot = Mensaje.objects.get(nombre__icontains='union_proteinas')
        cache.set('help_u_prot',help_u_prot,timeout)
    help_vol_dist = cache.get('help_vol_dist')
    if help_vol_dist == None:
        help_vol_dist = Mensaje.objects.get(nombre__icontains='volumen_distrib')
        cache.set('help_vol_dist',help_vol_dist,timeout)
    help_i_l_p = cache.get('help_i_l_p')
    if help_i_l_p == None:
        help_i_l_p = Mensaje.objects.get(nombre__icontains='indice_leche_plasma')
        cache.set('help_i_l_p',help_i_l_p,timeout)
    help_tmax = cache.get('help_tmax')
    if help_tmax == None:
        help_tmax = Mensaje.objects.get(nombre__icontains='t_maximo')
        cache.set('help_tmax',help_tmax,timeout)
    help_tmed = cache.get('help_tmed')
    if help_tmed == None:
        help_tmed = Mensaje.objects.get(nombre__icontains='t_medio')
        cache.set('help_tmed',help_tmed,timeout)
    help_biod = cache.get('help_biod')
    if help_biod == None:
        help_biod = Mensaje.objects.get(nombre__icontains='biodisponibilidad')
        cache.set('help_biod',help_biod,timeout)
    help_pka = cache.get('help_pka')
    if help_pka == None:
        help_pka = Mensaje.objects.get(nombre__icontains='pka')
        cache.set('help_pka',help_pka,timeout)
    help_d_teor = cache.get('help_d_teor')
    if help_d_teor == None:
        help_d_teor = Mensaje.objects.get(nombre__icontains='dosis_teorica')
        cache.set('help_d_teor',help_d_teor,timeout)
    help_d_rel = cache.get('help_d_rel')
    if help_d_rel == None:
        help_d_rel = Mensaje.objects.get(nombre__icontains='dosis_relativa')
        cache.set('help_d_rel',help_d_rel,timeout)
    help_d_terap = cache.get('help_d_terap')
    if help_d_terap == None:
        help_d_terap = Mensaje.objects.get(nombre__icontains='dosis_terapeutica')
        cache.set('help_d_terap',help_d_terap,timeout)
    #hints = mark_safe(get_rating_hints())
    span_risk = calcula_span_product_risk(prod)
    span_biblio = calcula_span_product_pharma_biblio(prod)
    
    '''calling the messages in the page'''
    prod_disclaimer = cache.get('prod_disclaimer')
    if prod_disclaimer == None:
        prod_disclaimer = Mensaje.objects.get(nombre__icontains='info_productos_madres')
        cache.set('prod_disclaimer',prod_disclaimer,timeout)
    risk0_info = cache.get('risk0_info')
    if risk0_info == None:
        risk0_info = Mensaje.objects.get(nombre__icontains='riesgo_n0')
        cache.set('risk0_info',risk0_info,timeout)
    risk1_info = cache.get('risk1_info')
    if risk1_info == None:
        risk1_info = Mensaje.objects.get(nombre__icontains='riesgo_n1')
        cache.set('risk1_info',risk1_info,timeout)
    risk2_info = cache.get('risk2_info')
    if risk2_info == None:
        risk2_info = Mensaje.objects.get(nombre__icontains='riesgo_n2')
        cache.set('risk2_info',risk2_info,timeout)
    risk3_info = cache.get('risk3_info')
    if risk3_info == None:
        risk3_info = Mensaje.objects.get(nombre__icontains='riesgo_n3')
        cache.set('risk3_info',risk3_info,timeout)
    risk0_leyenda = cache.get('risk0_leyenda')
    if risk0_leyenda == None:
        risk0_leyenda = Riesgo.objects.get(nivel=0)
        cache.set('risk0_leyenda',risk0_leyenda,timeout)
    risk1_leyenda = cache.get('risk1_leyenda')
    if risk1_leyenda == None:
        risk1_leyenda = Riesgo.objects.get(nivel=1)
        cache.set('risk1_leyenda',risk1_leyenda,timeout)
    risk2_leyenda = cache.get('risk2_leyenda')
    if risk2_leyenda == None:
        risk2_leyenda = Riesgo.objects.get(nivel=2)
        cache.set('risk2_leyenda',risk2_leyenda,timeout)
    risk3_leyenda = cache.get('risk3_leyenda')
    if risk3_leyenda == None:
        risk3_leyenda = Riesgo.objects.get(nivel=3)
        cache.set('risk3_leyenda',risk3_leyenda,timeout)

    prod_alias= None 
    if get_language()=='es':
        prod_alias = Alias.objects.exclude(nombre_es__isnull=True).exclude(nombre_es__exact='').filter(producto_principal=prod.id).order_by('nombre')
    else:
        prod_alias = Alias.objects.exclude(nombre_en__isnull=True).exclude(nombre_en__exact='').filter(producto_principal=prod.id).order_by('nombre')
        
    span_names = calcula_span_product_names(prod)
    
    prod_otras_escrituras = Otras_escrituras.objects.filter(producto_principal=prod.id)
    
    #risk alert on top
    prod_alert = get_alert_risk_for_producto(prod)

    visits=get_visits(prod)
    
    context = {'prod': prod,
               'prod_alias': prod_alias,
               'prod_otras_escrituras': prod_otras_escrituras,
               'perfil': None,
               'perfil_text': None,
               'perfil_form': None,
               'comment_form': None,
               'comentario': None,
               'mostrar_exito_comentario': False,
               'desplegar_comentario': False,
               'subscription_form': None,
               'exito_subscription': False,
               'user_email': '',
               'user_fname': '',
               'prod_alert': prod_alert,
               'span_names': span_names,
               'span_risk': span_risk,
               'span_biblio': span_biblio,
               'prod_disclaimer': prod_disclaimer,
               'risk0_info': risk0_info,
               'risk1_info': risk1_info,
               'risk2_info': risk2_info,
               'risk3_info': risk3_info,
               'risk0_leyenda': risk0_leyenda,
               'risk1_leyenda': risk1_leyenda,
               'risk2_leyenda': risk2_leyenda,
               'risk3_leyenda': risk3_leyenda,
               'help_biod': help_biod,
               'help_p_molecular': help_p_molecular,
               'help_u_prot': help_u_prot,
               'help_vol_dist': help_vol_dist,
               'help_pka': help_pka,
               'help_tmax': help_tmax,
               'help_tmed': help_tmed,
               'help_i_l_p': help_i_l_p,
               'help_d_teor': help_d_teor,
               'help_d_rel': help_d_rel,
               'help_d_terap': help_d_terap,
               'visits':visits,
               
            }
    
            
    return context


    
def update_context_profile(request, context, u):

    # we update context variables related with the profile:
    # profile:
    context.update({'perfil': u.perfil})
    # we also store it in the session so the rating handler can detect which is
    # the correct key  
    request.session['perfil'] = u.perfil
    # we update accordingly the initial values of the forms
    perfil_form = PerfilForm(initial = {'perfil': u.perfil})
    context.update({'perfil_form': perfil_form})
    # this is for storing the text (not the value) of the perfil
    perfil_text = dict(perfil_form.fields['perfil'].choices)[u.perfil]
    context.update({'perfil_text': perfil_text})
    
    return context

def update_context_comment(request, context, u, item):

    # we update context variables related with the opinion form:
    comentario = get_comment(u, item)
    if comentario != None:
        context.update({'desplegar_comentario': True})
    context.update({'comentario': comentario})
    comment_form = ComentarioForm(initial = {'comentario': comentario})
    context.update({'comment_form': comment_form})

    return context
    
    
def get_rating_hints():
    hints = _('[\'muy mala\', \'mala\', \'regular\', \'buena\', \'muy buena\']')
    return hints        
    
'''
def get_visits(item):
    timeout = 60 * 60 # Default cache timeout is 300 (5 mins) use this (1hour) for things that do not change very often
    
    iam = item.dime_que_eres()
    cache_key = iam + '_visits_' + str(item.pk)

    visits = cache.get(cache_key)
    if visits == None:
        visits=[0]*15
    
        aux=None
        if iam==u'producto':
            aux = Visita.objects.filter(prod=item.pk)
        elif iam==u'marca':
            aux = Visita.objects.filter(marca=item.pk)
        elif iam==u'alias':
            aux = Visita.objects.filter(alias=item.pk)
        elif iam==u'grupo':
            aux = Visita.objects.filter(grupo=item.pk)
        elif iam==u'otra_escritura':
            aux = Visita.objects.filter(otra_escritura=item.pk)

        visits[0]=aux.count()
        visits[1]= aux.filter(user__perfil='1').count()
        visits[14]= aux.filter(user__perfil='14').count()
        visits[2]= aux.filter(user__perfil='2').count()
        visits[3]= aux.filter(user__perfil='3').count()
        visits[4]= aux.filter(user__perfil='4').count()
        visits[5]= aux.filter(user__perfil='5').count()
        visits[13]= aux.filter(user__perfil='13').count()
        visits[6]= aux.filter(user__perfil='6').count()
        visits[7]= aux.filter(user__perfil='7').count()
        visits[8]= aux.filter(user__perfil='8').count()
        visits[9]= aux.filter(user__perfil='9').count()
        visits[10]= aux.filter(user__perfil='10').count()
        visits[11]= aux.filter(user__perfil='11').count()
        visits[12]= aux.filter(user__perfil='12').count()
        cache.set(cache_key, visits, timeout)
        
    return visits
'''
def get_visits(item):
    iam = item.dime_que_eres()
    if iam==u'grupo':
        try:
            v = Visita_grupo_total.objects.get(grupo=item.pk)
            return v.visitas
        except Visita_grupo_total.DoesNotExist:
            return 0
    elif iam==u'marca':
        try:
            v = Visita_marca_total.objects.get(marca=item.pk)
            return v.visitas
        except Visita_marca_total.DoesNotExist:
            return 0
    elif iam==u'alias':
        try:
            v = Visita_alias_total.objects.get(alias=item.pk)
            return v.visitas
        except Visita_alias_total.DoesNotExist:
            return 0
    elif iam==u'producto':
        try:
            v = Visita_producto_total.objects.get(producto=item.pk)
            return v.visitas
        except Visita_producto_total.DoesNotExist:
            return 0
    elif iam==u'otra_escritura':
        try:
            v = Visita_otras_escrituras_total.objects.get(otras_escrituras=item.pk)
            return v.visitas
        except Visita_otras_escrituras_total.DoesNotExist:
            return 0
    
    return 0           
                
                
def get_client_ip(request):
    ip = request.META.get('HTTP_X_REAL_IP')
    meta = 'HTTP_X_REAL_IP'
    if ip:
        pass
    else:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        meta = 'HTTP_X_FORWARDED_FOR'
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
            meta = 'REMOTE_ADDR'
#    print >> sys.stderr, 'Logging: get_clients_ip ' + ip + ' ' + meta
    return ip, meta

    
    
from django.contrib.gis.geoip import GeoIP
from django.contrib.sessions.models import Session

# returns the user and whether it has been created or updated
def set_user_profile(request, perfil):
        user_ip, ip_meta = get_client_ip(request)
        s = Session.objects.get(pk=request.session.session_key)
        u, created = LactUser.objects.get_or_create(session=s, ip_address=user_ip)
        if request.user.is_authenticated():
            u.user = request.user
        u.perfil = perfil
        g = GeoIP()
        geo_data = g.city(user_ip)
        if geo_data is not None:
            u.city = g.city(user_ip)['city']
            u.longitude = g.city(user_ip)['longitude']
            u.latitude = g.city(user_ip)['latitude']
            u.country_name = g.city(user_ip)['country_name']
            u.country_code = g.city(user_ip)['country_code']
            u.country_code3 = g.city(user_ip)['country_code3']
        u.save()
        return u, created
        
def get_user_profile(request):

    try:
        # get the user
        if not request.session.exists(request.session.session_key):
            request.session.create()
        aux = Session.objects.get(pk=request.session.session_key)
        u = LactUser.objects.get(session=aux)
        ''' Added on 27/11/2014:
        After installing Nginx as a reverse Proxy, we wrongly 
        stored the IP addresses. Now we need to update them correctly
        '''
        #let´s update the ip_address if the one stored is
        # from the US (we were storing the e-lactancia.org ip, 184.73.227.34
        # and the ip of the search engines, most of them located in the US
        if u.country_code == u'US':
            user_ip, meta = get_client_ip(request)
            old_ip = u.ip_address
            u.ip_address = user_ip
            g = GeoIP()
            # sometimes GeoIP doesn't know the city
            if g.city(user_ip)['city'] is not None:
                u.city = g.city(user_ip)['city']
                u.longitude = g.city(user_ip)['longitude']
                u.latitute = g.city(user_ip)['latitude']
            if g.city(user_ip)['country_name'] is not None:
                u.country_name = g.city(user_ip)['country_name']
                u.country_code = g.city(user_ip)['country_code']
                u.country_code3 = g.city(user_ip)['country_code3']
            #    print >>sys.stderr, '(from ' + u.country_name + ')'
            u.save()
    except LactUser.DoesNotExist:
        return None
    return u

# returns the user and whether it has been created or updated
def update_user(u):
        user_ip, meta = get_client_ip(request)
        s = Session.objects.get(pk=request.session.session_key)
        #print 'creating or updating user-ip ' + user_ip
        u, created = LactUser.objects.get_or_create(session=s, ip_address=user_ip)
        if request.user.is_authenticated():
            u.user = request.user
        u.perfil = perfil
        g = GeoIP()
        geo_data = g.city(user_ip)
        if geo_data is not None:
            u.city = g.city(user_ip)['city']
            u.longitude = g.city(user_ip)['longitude']
            u.latitute = g.city(user_ip)['latitude']
            u.country_name = g.city(user_ip)['country_name']
            u.country_code = g.city(user_ip)['country_code']
            u.country_code3 = g.city(user_ip)['country_code3']
        u.save()
        return u, created    
    
def update_user_mail_and_name(u, fullname, mail):
    u.email = mail
    u.nombre = fullname
    u.save()


def save_comment(u, item, comentario):
    
    if item.dime_que_eres()==u'producto':
        c, created = Comentario.objects.get_or_create(user=u, prod=item)
    elif item.dime_que_eres()==u'alias':
        c, created = Comentario.objects.get_or_create(user=u, alias=item)
    elif item.dime_que_eres()==u'marca':
        c, created = Comentario.objects.get_or_create(user=u, marca=item)
    elif item.dime_que_eres()==u'grupo':
        c, created = Comentario.objects.get_or_create(user=u, grupo=item)
    elif item.dime_que_eres()==u'mensaje':
        c, created = Comentario.objects.get_or_create(user=u, mensaje=item)
    elif item.dime_que_eres()==u'otra_escritura':
        c, created = Comentario.objects.get_or_create(user=u, otra_escritura=item)
    c.lang=get_language()
    c.comentario=comentario
    c.save()
    
        
def get_comment(u, item):
    
    if item.dime_que_eres()==u'producto':
        try:
            c = Comentario.objects.get(user=u, prod=item)
        except:
            return None
    elif item.dime_que_eres()==u'alias':
        try:
            c = Comentario.objects.get(user=u, alias=item)
        except:
            return None
    elif item.dime_que_eres()==u'marca':
        try:
            c = Comentario.objects.get(user=u, marca=item)
        except:
            return None
    elif item.dime_que_eres()==u'grupo':
        try:
            c = Comentario.objects.get(user=u, grupo=item)
        except:
            return None
    elif item.dime_que_eres()=='mensaje':
        try:
            c = Comentario.objects.get(user=u, mensaje=item)
        except:
            return None
    elif item.dime_que_eres()==u'otra_escritura':
        try:
            c = Comentario.objects.get(user=u, otra_escritura=item)
        except:
            return None
    return c.comentario
    
    
    
def save_visit(u, item):
    if item.dime_que_eres()==u'producto':
        Visita.objects.create(user=u, prod=item, lang=get_language())
    elif item.dime_que_eres()==u'alias':
        Visita.objects.create(user=u, alias=item, lang=get_language())
    elif item.dime_que_eres()==u'marca':
        Visita.objects.create(user=u, marca=item, lang=get_language())
    elif item.dime_que_eres()==u'grupo':
        Visita.objects.create(user=u, grupo=item, lang=get_language())
    elif item.dime_que_eres()==u'otra_escritura':
        Visita.objects.create(user=u, otra_escritura=item, lang=get_language())


    
    
def update_context_comment(request, context, u, item):

    # we update context variables related with the opinion form:
    comentario = get_comment(u, item)
    if comentario != None:
        context.update({'desplegar_comentario': True})
    context.update({'comentario': comentario})
    comment_form = ComentarioForm(initial = {'comentario': comentario})
    context.update({'comment_form': comment_form})

    return context

    
    
    
def update_context(request, item, context):

    perfil_form = PerfilForm()
    context.update({'perfil_form': perfil_form})
    
    if request.method == 'POST':
        if "perfil" in request.POST:
            perfil = request.POST['perfil']
            u, u_created = set_user_profile(request, perfil)
            lang = get_language()
            news_form = Subscription()
            update_context_comment(request, context, u, item)
        if "form_opinion" in request.POST:
            u = get_user_profile(request)
            form = ComentarioForm(request.POST)
            news_form = Subscription()
            context.update({'comment_form': form})
            context.update({'desplegar_comentario': True})
            if form.is_valid():
                cd = form.cleaned_data
                comentario = cd['comentario']
                context.update({'comentario': comentario})
                context.update({'mostrar_exito_comentario': True})
                save_comment(u, item, comentario)
            else:
                comentario=None
        if "form_subscribe" in request.POST:
            u = get_user_profile(request)
            news_form = Subscription(request.POST)
            if news_form.is_valid(): # All validation rules pass
                fullname = news_form.cleaned_data['nombre']
                mail = news_form.cleaned_data['email']
                update_user_mail_and_name(u, fullname, mail)
                context.update({'exito_subscription': True})
                context.update({'user_email': mail})
                context.update({'user_fname': fullname})
                update_context_comment(request, context, u, item)
        else:
            u = get_user_profile(request)
            news_form = Subscription()
        context.update({'subscription_form': news_form})
        update_context_profile(request, context, u)

    if request.method == 'GET':
        u = get_user_profile(request)
        
        if u == None:
            
            # we create a user with an anonymous profile (12) and save the visit:
            u, u_created = set_user_profile(request, '12')
        else:            
            update_context_profile(request, context, u)
            update_context_comment(request, context, u, item)
        # save the visit (we only do this in GET to prevent extra visits when POSTing forms).
        # TO-DO: currently we don't prevent registering
        # extra visits when a user rates a product.
        save_visit(u, item)
        
        news_form = Subscription()
        context.update({'subscription_form': news_form})
        
    return context

    
def get_context_for_alias(request, alias):
    prod = Producto.objects.prefetch_related('grupo','alternativas','marcas','biblio').get(pk=alias.producto_principal.id)
    context = get_context_for_product(request, prod)
    visits = get_visits(alias)
    context.update({'aliasp': alias,
                   'visits': visits,
                   
                   })
    return context

def get_context_for_otra_escritura(request, otra_escritura):
    prod = Producto.objects.prefetch_related('grupo','alternativas','marcas','biblio').get(pk=otra_escritura.producto_principal.id)
    context = get_context_for_product(request, prod)
    visits = get_visits(otra_escritura)
    context.update({'otra_escritura': otra_escritura,
                   'visits': visits,
                   
                   })
    return context
    
def get_context_for_marca(request, marca):
    try:
        prod = Producto.objects.prefetch_related('alternativas').get(nombre__iexact=marca.obten_pa_con_riesgo_mas_alto())
    except Producto.DoesNotExist:
        prod = None
    span_risk = calcula_span_product_risk(prod)
    span_marca = calcula_span_marca(marca)
    
    '''calling the messages in the page'''
    prod_disclaimer = cache.get('prod_disclaimer')
    if prod_disclaimer == None:
        prod_disclaimer = Mensaje.objects.get(nombre__icontains='info_productos_madres')
        cache.set('prod_disclaimer',prod_disclaimer,timeout)
    risk0_info = cache.get('risk0_info')
    if risk0_info == None:
        risk0_info = Mensaje.objects.get(nombre__icontains='riesgo_n0')
        cache.set('risk0_info',risk0_info,timeout)
    risk1_info = cache.get('risk1_info')
    if risk1_info == None:
        risk1_info = Mensaje.objects.get(nombre__icontains='riesgo_n1')
        cache.set('risk1_info',risk1_info,timeout)
    risk2_info = cache.get('risk2_info')
    if risk2_info == None:
        risk2_info = Mensaje.objects.get(nombre__icontains='riesgo_n2')
        cache.set('risk2_info',risk2_info,timeout)
    risk3_info = cache.get('risk3_info')
    if risk3_info == None:
        risk3_info = Mensaje.objects.get(nombre__icontains='riesgo_n3')
        cache.set('risk3_info',risk3_info,timeout)
    risk0_leyenda = cache.get('risk0_leyenda')
    if risk0_leyenda == None:
        risk0_leyenda = Riesgo.objects.get(nivel=0)
        cache.set('risk0_leyenda',risk0_leyenda,timeout)
    risk1_leyenda = cache.get('risk1_leyenda')
    if risk1_leyenda == None:
        risk1_leyenda = Riesgo.objects.get(nivel=1)
        cache.set('risk1_leyenda',risk1_leyenda,timeout)
    risk2_leyenda = cache.get('risk2_leyenda')
    if risk2_leyenda == None:
        risk2_leyenda = Riesgo.objects.get(nivel=2)
        cache.set('risk2_leyenda',risk2_leyenda,timeout)
    risk3_leyenda = cache.get('risk3_leyenda')
    if risk3_leyenda == None:
        risk3_leyenda = Riesgo.objects.get(nivel=3)
        cache.set('risk3_leyenda',risk3_leyenda,timeout)

    if marca.multiples_principios():
        marca_info_disclaimer = Mensaje.objects.get(nombre__icontains='marca_compuesto')
    else:
        marca_info_disclaimer = Mensaje.objects.get(nombre__icontains='marca_sencillo')

    marca_alerts = get_alert_risk_for_marca(marca)

    #hints = mark_safe(get_rating_hints())
    
    visits = get_visits(marca)
    
    context = {'prod': prod,
               'perfil': None,
               'perfil_text': None,
               'perfil_form': None,
               'comment_form': None,
               'comentario': None,
               'mostrar_exito_comentario': False,
               'desplegar_comentario': False,
               'marca_alerts': marca_alerts,
               'span_risk': span_risk,
               'prod_disclaimer': prod_disclaimer,
               'marca_info_disclaimer': marca_info_disclaimer,
               'risk0_info': risk0_info,
               'risk1_info': risk1_info,
               'risk2_info': risk2_info,
               'risk3_info': risk3_info,
               'risk0_leyenda': risk0_leyenda,
               'risk1_leyenda': risk1_leyenda,
               'risk2_leyenda': risk2_leyenda,
               'risk3_leyenda': risk3_leyenda,
               'marcap': marca,
               'visits': visits,
                }

    
    context.update(span_marca)

    return context
    
    
    
    
    
def detalle_p(request, producto_id):

    try:
        # get the product
        term = Producto.objects.get(pk=producto_id)
        return redirect(term, permanent=True)
    except Producto.DoesNotExist:
        raise Http404    
    

        
def ficha_producto(request, slug):

    try:
        # get the product
        term = Producto.objects.prefetch_related('grupo','alternativas','marcas','biblio').get(slug=slug)
        # get the context for the product
        context = get_context_for_product(request, term)
        context= update_context(request, term, context)
        context.update(initial_context)  
        context.update({'meta': set_meta(request, producto=term)})
    except Producto.DoesNotExist:
        raise Http404
    
    return render(request, 'lactancia/d_producto_b3.html', context)

    
def detalle_ap(request, alias_id):

    try:
        # get the product
        term = Alias.objects.get(pk=alias_id)
        return redirect(term, permanent=True)
    except Alias.DoesNotExist:
        raise Http404        
    
def ficha_alias(request, slug):
    try:
        # get the alias
        alias = Alias.objects.get(slug=slug)
        if alias.nombre=='':
            return redirect(alias.producto_principal)
        # set the context
        context = get_context_for_alias(request, alias)
        context= update_context(request, alias, context)
        context.update(initial_context)  
        context.update({'meta': set_meta(request, alias=alias)})
    except Alias.DoesNotExist:
        raise Http404
    
    return render(request, 'lactancia/d_alias_b3.html', context)

def detalle_oe(request, otra_escritura_id):

    try:
        # get the product
        term = Otras_escrituras.objects.get(pk=otra_escritura_id)
        return redirect(term, permanent=True)
    except Otras_escrituras.DoesNotExist:
        raise Http404            
    
def ficha_otra_escritura(request, slug):
    try:
        # get the alias
        otra_esc = Otras_escrituras.objects.get(slug=slug)
        # set the context
        context = get_context_for_otra_escritura(request, otra_esc)
        context= update_context(request, otra_esc, context)
        context.update(initial_context)  
        context.update({'meta': set_meta(request, otra_escritura=otra_esc)})
    except Otras_escrituras.DoesNotExist:
        raise Http404
    
    return render(request, 'lactancia/d_otra_escritura_b3.html', context)

def detalle_m(request, marca_id):
    try:
        # get the marca
        term = Marca.objects.get(pk=marca_id)
        return redirect(term, permanent=True)
    except Marca.DoesNotExist:
        raise Http404
    
def ficha_marca(request, slug):
    try:
        # get the marca
        marca = Marca.objects.get(slug=slug)
        # set the context
        context = get_context_for_marca(request, marca)
        context= update_context(request, marca, context)
        context.update(initial_context)  
        context.update({'meta': set_meta(request, marca=marca)})
    except Marca.DoesNotExist:
        raise Http404
    
    return render(request, 'lactancia/d_marca_b3.html', context)


def get_context_for_grupo(request, grupo):

    prods = None
    exists_r3 = False
    exists_r2 = False
    exists_r1 = False
    exists_r0 = False
    
    
    
    prods = cache.get('grupo_'+str(grupo.id)+'_es')
    if prods == None:
        filterargs = { 'grupo': grupo.id }
        prods = Producto.objects.filter(**filterargs).order_by('nombre')
        cache.set('grupo_'+str(grupo.id)+'_es', prods,timeout)
    
    exists_r3 = cache.get('grupo_r3_'+str(grupo.id)+'_exists_es')
    if exists_r3 == None:
        filterargs = { 'grupo': grupo.id, 'riesgo__nivel': 3 }
        exists_r3 = Producto.objects.filter(**filterargs).exists()
        cache.set('grupo_r3_'+str(grupo.id)+'_exists_es', exists_r3,timeout)

    exists_r2 = cache.get('grupo_r2_'+str(grupo.id)+'_exists_es')    
    if exists_r2 == None:
        filterargs = { 'grupo': grupo.id, 'riesgo__nivel': 2 }
        exists_r2 = Producto.objects.filter(**filterargs).exists()
        cache.set('grupo_r2_'+str(grupo.id)+'_exists_es', exists_r2,timeout)
   
    exists_r1 = cache.get('grupo_r1_'+str(grupo.id)+'_exists_es')   
    if exists_r1 == None:
        filterargs = { 'grupo': grupo.id, 'riesgo__nivel': 1 }
        exists_r1 = Producto.objects.filter(**filterargs).exists()
        cache.set('grupo_r1_'+str(grupo.id)+'_exists_es', exists_r1,timeout)
        
    exists_r0 = cache.get('grupo_r0_'+str(grupo.id)+'_exists_es')
    if exists_r0 == None:
        filterargs = { 'grupo': grupo.id, 'riesgo__nivel': 0 }
        exists_r0 = Producto.objects.filter(**filterargs).exists()
        cache.set('grupo_r0_'+str(grupo.id)+'_exists_es', exists_r0,timeout)
        
    n_r3 = None
    n_r2 = None
    n_r1 = None
    n_r0 = None
    
    
    n_r3 = cache.get('grupo_r3_N_of_'+str(grupo.id)+'_es')
    if n_r3 == None:
        if exists_r3:
            filterargs = { 'grupo': grupo.id, 'riesgo__nivel': 3 }
            n_r3 = Producto.objects.filter(**filterargs).count()
        else:
            n_r3 = 0
        cache.set('grupo_r3_N_of_'+str(grupo.id)+'_es', n_r3,timeout)
    n_r2 = cache.get('grupo_r2_N_of_'+str(grupo.id)+'_es')
    if n_r2 == None:
        if exists_r2:
            filterargs = { 'grupo': grupo.id, 'riesgo__nivel': 2 }
            n_r2 = Producto.objects.filter(**filterargs).count()
        else:
            n_r2 = 0
        cache.set('grupo_r2_N_of_'+str(grupo.id)+'_es', n_r2,timeout)
    n_r1 = cache.get('grupo_r1_N_of_'+str(grupo.id)+'_es')
    if n_r1 == None:
        if exists_r1:
            filterargs = { 'grupo': grupo.id, 'riesgo__nivel': 1 }
            n_r1 = Producto.objects.filter(**filterargs).count()
        else:
            n_r1 = 0
        cache.set('grupo_r1_N_of_'+str(grupo.id)+'_es', n_r1,timeout)
    n_r0 = cache.get('grupo_r0_N_of_'+str(grupo.id)+'_es')
    if n_r0 == None:
        if exists_r0:
            filterargs = { 'grupo': grupo.id, 'riesgo__nivel': 0 }
            n_r0 = Producto.objects.filter(**filterargs).count()
        else:
            n_r0 = 0
        cache.set('grupo_r0_N_of_'+str(grupo.id)+'_es', n_r0,timeout)
    
    
    
    '''calling the messages in the page'''
    prod_disclaimer = cache.get('prod_disclaimer')
    if prod_disclaimer == None:
        prod_disclaimer = Mensaje.objects.get(nombre__icontains='info_productos_madres')
        cache.set('prod_disclaimer',prod_disclaimer,timeout)
    risk0_info = cache.get('risk0_info')
    if risk0_info == None:
        risk0_info = Mensaje.objects.get(nombre__icontains='riesgo_n0')
        cache.set('risk0_info',risk0_info,timeout)
    risk1_info = cache.get('risk1_info')
    if risk1_info == None:
        risk1_info = Mensaje.objects.get(nombre__icontains='riesgo_n1')
        cache.set('risk1_info',risk1_info,timeout)
    risk2_info = cache.get('risk2_info')
    if risk2_info == None:
        risk2_info = Mensaje.objects.get(nombre__icontains='riesgo_n2')
        cache.set('risk2_info',risk2_info,timeout)
    risk3_info = cache.get('risk3_info')
    if risk3_info == None:
        risk3_info = Mensaje.objects.get(nombre__icontains='riesgo_n3')
        cache.set('risk3_info',risk3_info,timeout)
    risk0_leyenda = cache.get('risk0_leyenda')
    if risk0_leyenda == None:
        risk0_leyenda = Riesgo.objects.get(nivel=0)
        cache.set('risk0_leyenda',risk0_leyenda,timeout)
    risk1_leyenda = cache.get('risk1_leyenda')
    if risk1_leyenda == None:
        risk1_leyenda = Riesgo.objects.get(nivel=1)
        cache.set('risk1_leyenda',risk1_leyenda,timeout)
    risk2_leyenda = cache.get('risk2_leyenda')
    if risk2_leyenda == None:
        risk2_leyenda = Riesgo.objects.get(nivel=2)
        cache.set('risk2_leyenda',risk2_leyenda,timeout)
    risk3_leyenda = cache.get('risk3_leyenda')
    if risk3_leyenda == None:
        risk3_leyenda = Riesgo.objects.get(nivel=3)
        cache.set('risk3_leyenda',risk3_leyenda,timeout)

    grupo_alerts = get_alert_risk_for_grupo(grupo)
    
    #span_block_risk = calcula_span_grupo(grupo)

   
    #span_block_risk.update({'span_r0': 'col-xs-3'})
    #span_block_risk.update({'span_r1': 'col-xs-3'})
    #span_block_risk.update({'span_r2': 'col-xs-3'})
    #span_block_risk.update({'span_r3': 'col-xs-3'})
    
    #hints = mark_safe(get_rating_hints())

    visits = get_visits(grupo)
    
    context = {'grupop': grupo,
               'perfil': None,
               'perfil_text': None,
               'perfil_form': None,
               'comment_form': None,
               'comentario': None,
               'mostrar_exito_comentario': False,
               'desplegar_comentario': False,
               'grupo_alerts': grupo_alerts,
               'exists_r3': exists_r3,
               'exists_r2': exists_r2,
               'exists_r1': exists_r1,
               'exists_r0': exists_r0,
               'n_r3': n_r3,
               'n_r2': n_r2,
               'n_r1': n_r1,
               'n_r0': n_r0,
               'prods': prods,
               'prod_disclaimer': prod_disclaimer,
               'risk0_info': risk0_info,
               'risk1_info': risk1_info,
               'risk2_info': risk2_info,
               'risk3_info': risk3_info,
               'risk0_leyenda': risk0_leyenda,
               'risk1_leyenda': risk1_leyenda,
               'risk2_leyenda': risk2_leyenda,
               'risk3_leyenda': risk3_leyenda,
               'visits': visits,
                }
    
    return context



    
def detalle_g(request, grupo_id):
    try:
        # get the grupo
        grupo = Grupo.objects.get(pk=grupo_id)
        return redirect(grupo, permanent=True)
    except Grupo.DoesNotExist:
        raise Http404
    

def ficha_grupo(request, slug):
    try:
        # get the grupo
        grupo = Grupo.objects.prefetch_related('relacionados').get(slug=slug)
        # set the context
        context = get_context_for_grupo(request, grupo)
        context= update_context(request, grupo, context)
        context.update(initial_context)  
        context.update({'meta': set_meta(request, grupo=grupo)})
    except Grupo.DoesNotExist:
        raise Http404
    
    return render(request, 'lactancia/d_grupo_b3.html', context)
    
    
def hay_alertas_de_90_dias():
    
    now = timezone.now()
    start = now - datetime.timedelta(days=90)
    return Mensaje.objects.filter(fecha_modificacion__range=[start, now]).exists()
    
def alerta_riesgos(request):
    try:
        # get the messages
        alerts = cache.get('list_alert_risks')
        if alerts == None:
            alerts = Mensaje.objects.filter(nivel='warning').order_by('-fecha_modificacion')
            cache.set('list_alert_risks',alerts,timeout)
            
        context = {'alerts': alerts, 
                          '90_days_alerts': hay_alertas_de_90_dias()}
        context.update(initial_context)    
        context.update({'meta': set_meta(request)})
    except Mensaje.DoesNotExist:
        raise Http404
    return render(request, 'lactancia/alerta_riesgos_b3.html', context)

 

def creditos(request):
    textos = cache.get('textos_creditos')
    if textos == None:
        textos = Docs.objects.filter(type='c', visible=True).order_by('order')
        cache.set('textos_creditos', textos)

    context = {
                 'textos': textos,
              }
               
    context.update(initial_context)    
    context.update({'meta': set_meta(request)})
    return render(request, 'lactancia/creditos_b3.html', context)
    
    
    

'''Cookies y privacidad'''

def cookies(request):

    context = initial_context
    context.update({'meta': set_meta(request)}),
    return render(request, 'lactancia/uso_cookies-b3.html', context)

def privacidad(request):

    context = initial_context
    context.update({'meta': set_meta(request)})
    return render(request, 'lactancia/privacidad-b3.html', context)


def aviso_legal(request):

    context = initial_context
    context.update({'meta': set_meta(request)}),
    return render(request, 'lactancia/aviso_legal-b3.html', context)


''' Donativos views'''

def donativos(request):
    context = initial_context
    textos = Docs.objects.filter(type='d').order_by('order')
    title =_(u'Tú puedes salvar lactancias')
    description = _(u'Cientos de madres se ven obligadas a interrumpir sus lactancia aunque pocas situaciones lo justifica. Las mamás y sus bebés te necesitan. Salva lactancias. Dona ahora.')
    current_lang = get_language()
    meta = Meta(
        title=title,
        description= description,
        image= static('img/RRSS-donativo-elactancia.jpg') if current_lang == 'es'  else static('img/RRSS-donativo-elactancia_EN.jpg'),
        url = request.build_absolute_uri(),
        locale = current_lang,
    )
    
    
    context.update({'meta': meta, 'textos':textos,})
    return render(request, 'lactancia/donativos-b3.html', context)


def donativo_exito(request):
    
    context = initial_context
    context.update({'meta': set_meta(request)})
    return render(request, 'lactancia/donativo-exito-b3.html', context)



def donativo_cancelado(request):
    
    context = initial_context
    context.update({'meta': set_meta(request)})
    return render(request, 'lactancia/donativo-fallo-b3.html', context)


def boletin_error(request):
    
    context = initial_context
    context.update({'meta': set_meta(request)})
    return render(request, 'lactancia/boletin_error.html', context)
    

def boletin_ok(request):
    
    context = initial_context
    context.update({'meta': set_meta(request)})
    return render(request, 'lactancia/boletin_ok.html', context)
    
    
'''Lista de productos que tienen alternativas con un riesgo mayor que el del
propio producto'''
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def lista_negra(request):

    prods_all = cache.get('products_all_es')
    if prods_all == None:
        prods_all = Producto.objects.all().order_by('nombre')
        cache.set('prods_all_es',prods_all,timeout)
    r0_prods = prods_all.filter(riesgo__nivel=0)
    r1_prods = prods_all.filter(riesgo__nivel=1)
    r2_prods = prods_all.filter(riesgo__nivel=2)
    r3_prods = prods_all.filter(riesgo__nivel=3)

    blacklist_r0 = r0_prods.filter(alternativas__riesgo__nivel__in = [1,2,3]).distinct()
    blacklist_r1 = r1_prods.filter(alternativas__riesgo__nivel__in = [2,3]).distinct()
    blacklist_r2 = r2_prods.filter(alternativas__riesgo__nivel__in = [3]).distinct()
    blacklist_r3 = r3_prods.filter(alternativas__riesgo__nivel__in = [3]).distinct()
    
    context = {
                'blacklist_r0': blacklist_r0,
                'blacklist_r1': blacklist_r1,
                'blacklist_r2': blacklist_r2,
                'blacklist_r3': blacklist_r3,
                }
    context.update(initial_context)    
    context.update({'meta': set_meta(request)})
    return render(request, 'lactancia/lista_negra_b3.html', context)    

@staff_member_required
def limpia_cache(request):
    cache.clear()
    context = load_initial_context()
    return render(request, 'lactancia/limpiar_cache_b3.html', context)
    
''' CALCULO DE VISITAS '''
def calculate_visits():
    
    PROJECT_PATH = '/home/django'
    
    grupos_all = Grupo.objects.all().order_by('id')
    for p in grupos_all:
    
        aux = Visita.objects.filter(grupo=p.pk).count()
        
        # salvamos el número de visitas total a este término
        visita, created = Visita_grupo_total.objects.get_or_create(grupo=p)
        visita.visitas = aux
        visita.save()
        
        
            
    productos_all = Producto.objects.all().order_by('id')
    for p in productos_all:
    
        aux = Visita.objects.filter(prod=p.pk).count()
        
        # salvamos el número de visitas total a este término
        visita, created = Visita_producto_total.objects.get_or_create(producto=p)
        visita.visitas = aux
        visita.save()
        
        
    otras_escrituras_all = Otras_escrituras.objects.all().order_by('id')
    for p in otras_escrituras_all:
    
        aux = Visita.objects.filter(otra_escritura=p.pk).count()
        
        # salvamos el número de visitas total a este término
        visita, created = Visita_otras_escrituras_total.objects.get_or_create(otras_escrituras=p)
        visita.visitas = aux
        visita.save()
        
        
    alias_all = Alias.objects.all().order_by('id')
    for p in alias_all:
    
        aux = Visita.objects.filter(alias=p.pk).count()
        
        # salvamos el número de visitas total a este término
        visita, created = Visita_alias_total.objects.get_or_create(alias=p)
        visita.visitas = aux
        visita.save()
            
    
    marcas_all = Marca.objects.all().order_by('id')
    for p in marcas_all:
    
        aux = Visita.objects.filter(marca=p.pk).count()
        
        # salvamos el número de visitas total a este término
        visita, created = Visita_marca_total.objects.get_or_create(marca=p)
        visita.visitas = aux
        visita.save()
        
    return 0
    
''' ESTADISTICAS '''
def get_context_for_stats_json_v2(request):

    # Terms
    prods_all = Producto.objects.all()
    grupos_all = Grupo.objects.all()
    marcas_all = Marca.objects.all()
    alias_all = Alias.objects.all()
    escrit_all = Otras_escrituras.objects.all()
    
    N_prods = prods_all.count()
    N_grupos = grupos_all.count()
    N_alias = alias_all.count()
    N_marcas = marcas_all.count()
    N_escrituras = escrit_all.count()
    
    N_total = N_prods + N_grupos + N_alias + N_marcas + N_escrituras
    
    
    # Top visits prods
    json_data=file(PROJECT_PATH +'/media/stats_prods_top_1d.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    prods_visits_1d = data

    json_data=file(PROJECT_PATH +'/media/stats_prods_top_1w.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    prods_visits_1w = data

    json_data=file(PROJECT_PATH +'/media/stats_prods_top_1m.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    prods_visits_1m = data
    
    json_data=file(PROJECT_PATH +'/media/stats_prods_top_1y.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    prods_visits_1y = data
    
    json_data=file(PROJECT_PATH +'/media/stats_prods_top_all.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    prods_visits_all = data



    # Visits in time
    json_data=file(PROJECT_PATH +'/media/stats_visits_years.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_yearly = data

    json_data=file(PROJECT_PATH +'/media/stats_consultations_years.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    consultations_yearly = data
    
    json_data=file(PROJECT_PATH +'/media/stats_visits_months.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_monthly = data

    json_data=file(PROJECT_PATH +'/media/stats_consultations_months.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    consultations_monthly = data
    
    json_data=file(PROJECT_PATH +'/media/stats_visits_weeks.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_weekly = data
    
    json_data=file(PROJECT_PATH +'/media/stats_consultations_weeks.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    consultations_weekly = data
    
    json_data=file(PROJECT_PATH +'/media/stats_visits_days.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_daily = data

    json_data=file(PROJECT_PATH +'/media/stats_consultations_days.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    consultations_daily = data
    
    yearly = zip(visits_yearly, consultations_yearly)
    monthly = zip(visits_monthly, consultations_monthly)
    weekly = zip(visits_weekly, consultations_weekly)
    daily = zip(visits_daily, consultations_daily)
    
    

    '''# Visits per profile
    json_data=file(PROJECT_PATH +'/media/stats_profile_1d.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_profile_1d = data

    json_data=file(PROJECT_PATH +'/media/stats_profile_1w.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_profile_1w = data

    json_data=file(PROJECT_PATH +'/media/stats_profile_1m.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_profile_1m = data

    json_data=file(PROJECT_PATH +'/media/stats_profile_1y.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_profile_1y = data

    json_data=file(PROJECT_PATH +'/media/stats_profile_all.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_profile_all = data
    '''
    
    # Top visits countries
    json_data=file(PROJECT_PATH +'/media/stats_country_1d.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_country_1d = data

    json_data=file(PROJECT_PATH +'/media/stats_country_1w.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_country_1w = data

    json_data=file(PROJECT_PATH +'/media/stats_country_1m.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_country_1m = data

    json_data=file(PROJECT_PATH +'/media/stats_country_1y.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_country_1y = data

    
    json_data=file(PROJECT_PATH +'/media/stats_country_all.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_country_all = data
    
    
    
    context = {
                 'N_prods': N_prods,
                 'N_grupos': N_grupos,
                 'N_alias': N_alias,
                 'N_marcas': N_marcas,
                 'N_escrituras': N_escrituras,
                 'N_total': N_total,
                 'prods_visits_1d': prods_visits_1d,
                 'prods_visits_1w': prods_visits_1w,
                 'prods_visits_1m': prods_visits_1m,
                 'prods_visits_1y': prods_visits_1y,
                 'prods_visits_all': prods_visits_all,
                 'visits_country_1d': visits_country_1d,
                 'visits_country_1w': visits_country_1w,
                 'visits_country_1m': visits_country_1m,
                 'visits_country_1y': visits_country_1y,
                 'visits_country_all': visits_country_all,
                 'daily': daily,
                 'weekly': weekly,
                 'monthly': monthly,
                 'yearly' : yearly,
    
            }
    
    context.update(initial_context)    
    return context
    



def get_context_for_stats_json_ES(request):
    import json
    PROJECT_PATH = '/home/django'

    # Terms
    prods_all = Producto.objects.all()
    grupos_all = Grupo.objects.all()
    marcas_all = Marca.objects.all()
    alias_all = Alias.objects.all()
    escrit_all = Otras_escrituras.objects.all()
    
    N_prods = prods_all.count()
    N_grupos = grupos_all.count()
    N_alias = alias_all.count()
    N_marcas = marcas_all.count()
    N_escrituras = escrit_all.count()
    
    N_total = N_prods + N_grupos + N_alias + N_marcas + N_escrituras
    
    
    # Top visits prods
    json_data=file(PROJECT_PATH +'/media/stats_prods_top_1d_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    prods_visits_1d = data

    json_data=file(PROJECT_PATH +'/media/stats_prods_top_1w_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    prods_visits_1w = data

    json_data=file(PROJECT_PATH +'/media/stats_prods_top_1m_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    prods_visits_1m = data
    
    json_data=file(PROJECT_PATH +'/media/stats_prods_top_1y_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    prods_visits_1y = data
    
    json_data=file(PROJECT_PATH +'/media/stats_prods_top_all_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    prods_visits_all = data



    # Visits in time
    json_data=file(PROJECT_PATH +'/media/stats_visits_years_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_yearly = data

    json_data=file(PROJECT_PATH +'/media/stats_consultations_years_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    consultations_yearly = data
    
    json_data=file(PROJECT_PATH +'/media/stats_visits_months_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_monthly = data

    json_data=file(PROJECT_PATH +'/media/stats_consultations_months_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    consultations_monthly = data
    
    json_data=file(PROJECT_PATH +'/media/stats_visits_weeks_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_weekly = data
    
    json_data=file(PROJECT_PATH +'/media/stats_consultations_weeks_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    consultations_weekly = data
    
    json_data=file(PROJECT_PATH +'/media/stats_visits_days_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_daily = data

    json_data=file(PROJECT_PATH +'/media/stats_consultations_days_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    consultations_daily = data
    
    yearly = zip(visits_yearly, consultations_yearly)
    monthly = zip(visits_monthly, consultations_monthly)
    weekly = zip(visits_weekly, consultations_weekly)
    daily = zip(visits_daily, consultations_daily)
    
    
    '''
    # Visits per profile
    json_data=file(PROJECT_PATH +'/media/stats_profile_1d_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_profile_1d = data

    json_data=file(PROJECT_PATH +'/media/stats_profile_1w_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_profile_1w = data

    json_data=file(PROJECT_PATH +'/media/stats_profile_1m_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_profile_1m = data

    json_data=file(PROJECT_PATH +'/media/stats_profile_1y_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_profile_1y = data

    json_data=file(PROJECT_PATH +'/media/stats_profile_all_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_profile_all = data
    '''
    
    # Top visits SPANISH cities
    json_data=file(PROJECT_PATH +'/media/stats_cities_1d_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_cities_1d = data

    json_data=file(PROJECT_PATH +'/media/stats_cities_1w_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_cities_1w = data

    json_data=file(PROJECT_PATH +'/media/stats_cities_1m_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_cities_1m = data

    json_data=file(PROJECT_PATH +'/media/stats_cities_1y_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_cities_1y = data

    
    json_data=file(PROJECT_PATH +'/media/stats_cities_all_ES.json','r')
    data = json.loads(json_data.read().decode("utf-8-sig"))
    visits_cities_all = data
    
    context = {
                 'N_prods': N_prods,
                 'N_grupos': N_grupos,
                 'N_alias': N_alias,
                 'N_marcas': N_marcas,
                 'N_escrituras': N_escrituras,
                 'N_total': N_total,
                 'prods_visits_1d': prods_visits_1d,
                 'prods_visits_1w': prods_visits_1w,
                 'prods_visits_1m': prods_visits_1m,
                 'prods_visits_1y': prods_visits_1y,
                 'prods_visits_all': prods_visits_all,
                 'visits_cities_1d': visits_cities_1d,
                 'visits_cities_1w': visits_cities_1w,
                 'visits_cities_1m': visits_cities_1m,
                 'visits_cities_1y': visits_cities_1y,
                 'visits_cities_all': visits_cities_all,
                 'daily': daily,
                 'weekly': weekly,
                 'monthly': monthly,
                 'yearly' : yearly,
    
            }
            
    context.update(initial_context)
    
    return context
    

def patrocinadores(request):
    
    patrocinadores = cache.get('patrocinadores')
    if patrocinadores == None:
        patrocinadores = Patrocinador.objects.filter(visible=True).order_by('order')
        cache.set('patrocinadores', patrocinadores)
    patrocinadores = cache.get('patrocinadores')
    textos_patrocinadores = cache.get('textos_patrocinadores')
    if textos_patrocinadores == None:
        textos_patrocinadores = Docs.objects.filter(type='s').order_by('order')
        cache.set('textos_patrocinadores', textos_patrocinadores)
    textos_patrocinadores = cache.get('textos_patrocinadores')
    context = {
                'entidades': patrocinadores,
                'textos_patrocinadores': textos_patrocinadores,
                }
    context.update(initial_context)    
    context.update({'meta': set_meta(request)})
    return render(request, 'lactancia/patrocinadores_b3.html', context)


def avales(request):
    
    avales = cache.get('avales')
    if avales == None:
        avales = Aval.objects.filter(visible=True).order_by('order')
        cache.set('avales', avales)
    avales = cache.get('avales')
    textos_avales = cache.get('textos_avales')
    if textos_avales == None:
        textos_avales = Docs.objects.filter(type='a').order_by('order')
        cache.set('textos_avales', textos_avales)
    textos_avales = cache.get('textos_avales')
    
    
    context = {
                'avales': avales,
                'textos_avales': textos_avales,
                }
                
    context.update(initial_context)    
    context.update({'meta': set_meta(request)})
    
    return render(request, 'lactancia/avales_b3.html', context)
    
    
def estadisticas(request):
    context = get_context_for_stats_json_v2(request)
    context.update({'meta': set_meta(request)})
    return render(request, 'lactancia/estadisticas_json_v4-b3.html', context)


def estadisticas_ES(request):
    context = get_context_for_stats_json_ES(request)
    context.update({'meta': set_meta(request)})
    return render(request, 'lactancia/estadisticas_json_ES-b3.html', context)

    
'''API: List of terms'''
def get_date_last_update_list_of_terms(request):
    last_update = cache.get('prod_last_update')
    if last_update == None:
        last_update = Producto.objects.latest('fecha_modificacion').fecha_modificacion
        cache.set('prod_last_update',last_update)
    
    return JsonResponse({'date_last_update': last_update})

def get_list_of_terms(request):
    TERMS = cache.get('TERMS')
    if TERMS == None:
        productos = Producto.objects.all().distinct().values('nombre_es', 'nombre_en', 'id').order_by('nombre')
        TERMS = list(productos)
        cache.set('TERMS', TERMS)
    return JsonResponse({'list': TERMS})
    
def get_term(request, prod_id):

    try:
        # get the product
        term = Producto.objects.values(
            'id','nombre_es', 'nombre_en','riesgo__nivel', 'riesgo__nombre_es', 
            'riesgo__nombre_en', 'riesgo__descripcion_es', 'riesgo__descripcion_en', 'comentario_es', 'comentario_en', 
            'fecha_creacion', 'fecha_modificacion', 'peso_molecular', 'union_proteinas','volumen_distrib', 'indice_leche_plasma', 
            't_maximo', 't_medio', 'biodisponibilidad', 'dosis_teorica', 'dosis_relativa', 'dosis_terapeutica').get(pk=prod_id)
        
        prod = Producto.objects.get(pk=prod_id)
        
        alternatives = prod.alternativas.all().values('id','nombre_es', 'nombre_en','riesgo__nivel')
        group = prod.grupo.all().values('id','nombre_es', 'nombre_en')
        biblio = prod.biblio.all().values('titulo','autores', 'publicacion', 'anyo', 'abstract_link', 'full_text_link')
        tradenames = prod.marcas.all().values('nombre')
    
    except Producto.DoesNotExist:
        return  JsonResponse({'error': 'no existe producto'})
    return JsonResponse({'producto': term, 
                         'alternativas':list(alternatives),
                         'grupo': list(group),
                         'biblio': list(biblio),
                         'marcas': list(tradenames),
                         })
    
    
''' BIBLIOGRAPHIC REFERENCE OF WEBSITE '''

def get_bibtex_reference(item=None):
    now = timezone.localtime(timezone.now())
    if item:
        result =    u'@misc{ e-lactancia, '
        result +=   u' author = "APILAM{,} ' + _(u'Asociación para la Promoción científica y cultural de la Lactancia Materna') + '", '
        result +=   u' title = "' + item.nombre + u' --- e-lactancia.org", '
        result +=   u' year = "' + item.fecha_modificacion.strftime("%d-%m-%Y") + u'", '
        result +=   u' url = "http://e-lactancia.org' + item.get_absolute_url() + u'", '
        result +=   u' note = "[Online; accessed ' + _date(now, "d F, Y") + u']" }'
    else:
        result =    u'@misc{ e-lactancia, ' 
        result +=   u' author = "APILAM\{,\} ' + _(u'Asociación para la Promoción científica y cultural de la Lactancia Materna') + u'", ' 
        result +=   u' title = " e-lactancia.org", ' 
        result +=   u' year = "2002", ' 
        result +=   u' url = "http://e-lactancia.org", ' 
        result +=   u' note = "[Online; accessed ' + _date(now, "d F, Y") + u']" }'
    return unicode(result)
    

def get_RIS_reference(item=None):
    '''
    from https://en.wikipedia.org/wiki/RIS_(file_format)
    TY - ELEC
    AU - APILAM, Asociación para la Promoción científica y cultural de la Lactancia Materna
    Y1 - 2002
    Y2 - fecha acceso
    TI - E-Lactancia (o nombre del término)
    T2 - e-lactancia.org
    UR - http://e-lactancia.org
    ER - 
    '''    
    now = timezone.localtime(timezone.now())    

    if item:
        result =    u'TY - ELEC\n'
        result +=   u'AU - APILAM, ' + _(u'Asociación para la Promoción científica y cultural de la Lactancia Materna') + '\n'
        result +=   u'Y1 - ' + _date(item.fecha_modificacion, "d F, Y") + '\n'
        result +=   u'Y2 - ' + _date(now, "d F, Y") + '\n'
        result +=   u'TI - ' + item.nombre + '\n'
        result +=   u'T2 - e-lactancia.org' + '\n'
        result +=   u'UR - http://e-lactancia.org' + item.get_absolute_url() + '\n'
        result +=   u'ER -' + '\n'
    else:
        result =    u'TY - ELEC'+ '\n'
        result +=   u'AU - APILAM, ' + _(u'Asociación para la Promoción científica y cultural de la Lactancia Materna') + '\n'
        result +=   u'Y1 - 2002' + '\n'
        result +=   u'Y2 - ' + _date(now, "d F, Y") + '\n'
        result +=   u'TI - E-lactancia' + '\n'
        result +=   u'UR - http://e-lactancia.org' + '\n'
        result +=   u'ER -' + '\n'
    return unicode(result)
 
def get_enw_reference(item=None):
    '''
    from https://en.wikipedia.org/wiki/EndNote#Tags_and_fields
    %0 Web Page
    %A APILAM, Asociación para la Promoción científica y cultural de la Lactancia Materna
    %D 2002
    %T E-Lactancia (o nombre del término)
    %[  fecha acceso
    %B e-lactancia.org
    %U http://e-lactancia.org
    '''    

    now = timezone.localtime(timezone.now())    

    if item:
        result =    u'%0 Web Page\n'
        result +=   u'%A APILAM, ' + _(u'Asociación para la Promoción científica y cultural de la Lactancia Materna') + '\n'
        result +=   u'%D ' + _date(item.fecha_modificacion, "Y") + '\n'
        result +=   u'%[ ' + _date(now, "d F, Y") + '\n'
        result +=   u'%T ' + item.nombre + '\n'
        result +=   u'%B e-lactancia.org' + '\n'
        result +=   u'%U http://e-lactancia.org' + item.get_absolute_url() + '\n'
    else:
        result =    u'%0 Web Page\n'
        result +=   u'%A APILAM, ' + _(u'Asociación para la Promoción científica y cultural de la Lactancia Materna') + '\n'
        result +=   u'%D 2002' + '\n'
        result +=   u'%[ ' + _date(now, "d F, Y") + '\n'
        result +=   u'%B e-lactancia.org' + '\n'
        result +=   u'%U http://e-lactancia.org' + '\n'
    return unicode(result)
    
    
def get_APA_reference(item=None):
    now = timezone.localtime(timezone.now())
    # followed instructions in https://en.wikipedia.org/wiki/Wikipedia:Citing_Wikipedia
    # APILAM (Asociación para la promoción e investigación científica y cultural de la lactancia materna). (2002). e-lactancia. Recuperado -aquí el ordenador debe poner la fecha-, a partir de http://e-lactancia.org/
    # Plagiarism. (n.d.). In Wikipedia. Retrieved August 10, 2004, from https://en.wikipedia.org/wiki/Plagiarism
    
    if item:
        result = item.nombre + '. ' + _(u'En e-lactancia.org.') + ' ' + _(u'Recuperado') + ' ' + _date(now, "d F, Y") + ' ' + _(u'a partir de') + ' http://e-lactancia.org' + item.get_absolute_url()
    else:
        result = _(u'APILAM (Asociación para la promoción e investigación científica y cultural de la lactancia materna)') + '. (2002). e-lactancia. ' + _(u'Recuperado') + ' ' + _date(now, "d F, Y") + ' ' + _(u'a partir de') + ' http://e-lactancia.org'
    
    return unicode(result)

def get_vancouver_reference(item=None):
    now = timezone.localtime(timezone.now())
    # followed instructions in https://en.wikipedia.org/wiki/Vancouver_system
    # Drug-interactions.com [homepage on the Internet]. Indianapolis: Indiana University Department of Medicine; 2003 [updated 17 May 2006; cited 30 May 2006]. Available from: http://medicine.iupui.edu/flockhart/
    
    if item:
        result = 'APILAM. ' + item.nombre + '. ' + _(u'En') + ': ' + 'e-lactancia.org. ' + _(u'APILAM: Asociación para la promoción e investigación científica y cultural de la lactancia materna') + '; 2002 ' + _(u'actualizado') + ' ' + _date(item.fecha_modificacion, "d b Y") + '; ' + _(u'acceso') + ' ' + _date(now, "d b Y") + '. ' + _(u'Disponible en') + ' http://e-lactancia.org' + item.get_absolute_url()
    else:
    
        last_update = cache.get('prod_last_update')
        if last_update == None:
            last_update = Producto.objects.latest('fecha_modificacion').fecha_modificacion
            cache.set('prod_last_update',last_update)
        
        result = 'e-lactancia.org. ' + _(u'APILAM: Asociación para la promoción e investigación científica y cultural de la lactancia materna') + '; 2002 ' + _(u'actualizado') + ' ' + _date(last_update, "d b Y") + '; ' + _(u'acceso') + ' ' + _date(now, "d F, Y") + '. ' + _(u'Disponible en') + ' http://e-lactancia.org'
    
    return unicode(result)
    
def get_chicago_reference(item=None):
    now = timezone.localtime(timezone.now())
    # followed instructions in https://en.wikipedia.org/wiki/Wikipedia:Citing_Wikipedia#Chicago_style
    # APILAM (Asociación para la promoción e investigación científica y cultural de la lactancia materna). 2002. "E-Lactancia". http://e-lactancia.org/.
    # Wikipedia, The Free Encyclopedia, s.v. "Plagiarism," (accessed August 10, 2004), https://en.wikipedia.org/w/index.php?title=Plagiarism&oldid=5139350
    
    if item:
        result = _(u'APILAM (Asociación para la promoción e investigación científica y cultural de la lactancia materna)') + '. (2002). "' + item.nombre + '," (' + _(u'accedido el') + ' ' + _date(now, "d F, Y") + '), http://e-lactancia.org' + item.get_absolute_url()
    else:
        result = _(u'APILAM (Asociación para la promoción e investigación científica y cultural de la lactancia materna)') + '. (2002). "e-lactancia," (' + _(u'accedido el') + ' ' + _date(now, "d F, Y") + '), http://e-lactancia.org'
        
    return unicode(result)
    
    
    
import codecs
def generate_citation_link(item=None, citation='bibtex'):

    MEDIA_ROOT = '/home/django/media/'
    MEDIA_URL = '/media/'

    # create a unique filename based on current time
    now = timezone.localtime(timezone.now())
    filename = 'ref-e-lactancia-' + now.strftime("%Y%m%d%H%M%S")
    
    # add file extension according to type of citation file
    if citation == 'bibtext':
        filename += '.bib'
    elif citation == 'RIS':
        filename += '.ris'
    elif citation == 'enw':
        filename += '.enw'
    else:
        filename += '.txt'
    
    # create the file
    handle=codecs.open(MEDIA_ROOT+filename,'w','utf-8')
    
    # write citation in file
    if citation == 'bibtex':
        handle.write(get_bibtex_reference(item))
    if citation == 'RIS':
        handle.write(get_RIS_reference(item))
    if citation == 'enw':
        handle.write(get_enw_reference(item))
    if citation == 'APA':
        handle.write(get_APA_reference(item))
    if citation == 'vancouver':
        handle.write(get_vancouver_reference(item))
    if citation == 'chicago':
        handle.write(get_chicago_reference(item))
    # close the file
    handle.close()
    
    # return relative url where the file is
    return MEDIA_URL+filename
    
def generate_citation_text(item=None, citation='APA'):
    result = ''
    if citation == 'bibtex':
        result = get_bibtex_reference(item)
    if citation == 'RIS':
        result = get_RIS_reference(item)
    if citation == 'enw':
        result = get_enw_reference(item)
    if citation == 'APA':
        result = get_APA_reference(item)
    if citation == 'vancouver':
        result = get_vancouver_reference(item)
    if citation == 'chicago':
        result = get_chicago_reference(item)

    return result
    
    
    
'''get the citation when button pressed'''
def download_citation(request):

    term = None
    id = None
    item = None
    citation = None
    if ('citation_type' in request.GET):
        term = request.GET.get('term_type', None)
        if ('term_id' in request.GET):
            id = int(request.GET.get('term_id', 0))
        citation = request.GET.get('citation_type', 'APA')
        if term == 'producto':
            item = Producto.objects.get(id=id)
        elif term == 'grupo':
            item = Grupo.objects.get(id=id)
        elif term == 'alias':
            item = Alias.objects.get(id=id)
        elif term == 'marca':
            item = Marca.objects.get(id=id)
        elif term == 'otra_escritura':
            item = Otras_escrituras.objects.get(id=id)
    result = ''
    result += '<div class="col-xs-12">' + '<a href="'+ generate_citation_link(item, citation) + '" download id="btn_download_citation" class="btn btn-info">' + _(u'Descargar') + '</a>' + '</div>'
    result += '<div class="col-xs-12" style="margin-top:20px;"><p class="dont-break-out">' + generate_citation_text(item,citation) + '</p></div>'
    
    
    return HttpResponse(result)       
    
    
'''
URLS restructure
'''
import re
import unidecode
from django.utils.text import slugify

def slugify_javivi(text):
    text = unidecode.unidecode(text).lower()
    text = re.sub(r'\W+', ' ', text).strip()
    return re.sub(r'\W+', '-', text)
    
def slugify_groups():
    grupos = Grupo.objects.all()
    
    for g in grupos:
        g.slug='kk'
        g.save()
        '''slug = slugify(g.nombre_en)[0:93]
        duplicated_slug = Grupo.objects.filter(slug=slug).count()
        if duplicated_slug>0:
            slug = slug + '-' + str(duplicated_slug + 1)
        g.slug = slug
        g.save()
        '''
def slugify_products():
    items = Producto.objects.all()
    
    for i in items:
        i.slug='kk'
        i.save()
        '''
        slug = slugify(i.nombre_en)[0:93]
        duplicated_slug = Producto.objects.filter(slug=slug).count()
        if duplicated_slug>0:
            slug = slug + '-' + str(duplicated_slug + 1)
        i.slug = slug
        i.save()
        '''
        
def slugify_alias():
    items = Alias.objects.all()
    
    for i in items:
        i.slug='kk'
        i.save()
        '''
        if i.nombre_en:
            slug = slugify(i.nombre_en)[0:93]
        else:
            slug = slugify(i.nombre_es)[0:93]
        duplicated_slug = Alias.objects.filter(slug=slug).count()
        if duplicated_slug>0:
            slug = slug + '-' + str(duplicated_slug + 1)
        i.slug = slug
        i.save()
        '''
        
def slugify_escrituras():
    items = Otras_escrituras.objects.all()
    
    for i in items:
        i.slug='kk'
        i.save()
        '''
        slug = slugify(i.nombre)[0:93]
        duplicated_slug = Otras_escrituras.objects.filter(slug=slug).count()
        if duplicated_slug>0:
            slug = slug + '-' + str(duplicated_slug + 1)
        i.slug = slug
        i.save()
        '''
        
def compare_slugifies():
    items = Otras_escrituras.objects.all()
    
    for i in items:
        print i.slug
        print 'vs.'
        print slugify(i.nombre)
        print '--------------------------'
        
def slugify_marcas():
    items = Marca.objects.all()
    
    for i in items:
        i.slug='kk'
        i.save()
        '''
        slug = slugify_javivi(i.nombre_paises_en)[0:93]
        duplicated_slug = Marca.objects.filter(slug=slug).exclude(id=i.id).count()
        if duplicated_slug>0:
            slug = slug + '-' + str(duplicated_slug + 1)
        i.slug = slug
        i.save()
        '''