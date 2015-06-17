# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
#from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from lactancia.models import Riesgo, Producto, Alias, Marca, Otras_escrituras, Grupo, Mensaje, LactUser, Visita, Comentario, Bibliografia
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



def index(request):
    return HttpResponse("Hello, world! This is our first view.")
    
def typeahead_productos():
    
    productos = Producto.objects.all().distinct().order_by('nombre')
    N = len(productos)
    PRODUCTOS = '['
    for index, p in enumerate(productos):
        PRODUCTOS += '{ "termino": "'
        PRODUCTOS += p.nombre
        PRODUCTOS += '", '
        PRODUCTOS += '"id": "'
        PRODUCTOS += str(p.id)
        PRODUCTOS += '"}'
        if index < len(productos)-1:
            PRODUCTOS +=', '
    PRODUCTOS += ']'
    
    #PRODUCTOS = '[{ "termino": "Púlpito", "id": "1"}, { "termino": "Pupila", "id": "2"}, { "termino": "Patata", "id": "9"}, { "termino": "Ácido", "id": "3"}, { "termino": "Acidez", "id": "4"}, { "termino": "Tétanos", "id": "5"}, { "termino": "Televisión", "id": "6"}, { "termino": "Óseo", "id": "7"}, { "termino": "Osamenta", "id": "8"}]'
    #N= 8
    return PRODUCTOS, N
    
def typeahead_grupos():
    grupos = Grupo.objects.all().distinct().order_by('nombre')
    N = len(grupos)
    GRUPOS = '['
    for index, p in enumerate(grupos):
        GRUPOS += '{ "termino": "'
        GRUPOS += p.nombre
        GRUPOS += '", '
        GRUPOS += '"id": "'
        GRUPOS += str(p.id)
        GRUPOS += '"}'
        if index < len(grupos)-1:
            GRUPOS +=', '
    GRUPOS += ']'
    
    return GRUPOS, N
    
def typeahead_sinonimos():
    alias = Alias.objects.all().distinct().order_by('nombre')
    N = len(alias)
    SINONIMOS = '['
    for index, p in enumerate(alias):
        SINONIMOS += '{ "termino": "'
        SINONIMOS += p.nombre
        SINONIMOS += '", '
        SINONIMOS += '"id": "'
        SINONIMOS += str(p.id)
        SINONIMOS += '"}'
        if index < len(alias)-1:
            SINONIMOS +=', '
    SINONIMOS += ']'
    
    return SINONIMOS, N

def typeahead_otras_escrituras():
    o_escrit = Otras_escrituras.objects.all().distinct().order_by('nombre')
    N = len(o_escrit)
    ESCRITURAS = '['
    for index, p in enumerate(o_escrit):
        ESCRITURAS += '{ "termino": "'
        ESCRITURAS += p.nombre
        ESCRITURAS += '", '
        ESCRITURAS += '"id": "'
        ESCRITURAS += str(p.id)
        ESCRITURAS += '"}'
        if index < len(o_escrit)-1:
            ESCRITURAS +=', '
    ESCRITURAS += ']'
    
    return ESCRITURAS, N
    
    
    
def typeahead_marcas():
    marcas = Marca.objects.all().distinct().order_by('nombre')
    N = len(marcas)
    MARCAS = '['
    for index, p in enumerate(marcas):
        MARCAS += '{ "termino": "'
        MARCAS += p.nombre
        MARCAS += '", '
        MARCAS += '"id": "'
        MARCAS += str(p.id)
        MARCAS += '"}'
        if index < len(marcas)-1:
            MARCAS +=', '
    MARCAS += ']'
    
    return MARCAS, N
    
    
'''returns the message of active alert(s) for risk level change of a product
    (top button of the top bar)
'''
def get_alert_risk():
    

    now = timezone.now()

    month = now - datetime.timedelta(days=30)

    return Mensaje.objects.filter(fecha_modificacion__range=[month, now]).exists()
def get_alert_risk(context):
    now = timezone.now()
    month = now - datetime.timedelta(days=30)
    alert_risk =  Mensaje.objects.filter(fecha_modificacion__range=[month, now]).exists()    
    context.update({ 'alert_risk': alert_risk, })
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
    context=get_alert_risk(context)
    return context
    

    
# CACHE OF INITIAL CONTEXT
timeout = 60 * 2 # Default cache timeout is 300 (5 mins) use this (1hour) for things that do not change very often
initial_context = cache.get('initial_context')
if initial_context == None:
    initial_context = load_initial_context()
    cache.set('initial_context', initial_context, timeout)


def landing(request):

    last_update = cache.get('prod_last_update')
    if last_update == None:
        last_update = Producto.objects.latest('fecha_modificacion').fecha_modificacion
        cache.set('prod_last_update',last_update)
        
    context = {
                'last_update': last_update,
                }
                
    context.update(initial_context)    
    return render(request, 'lactancia/landing.html', context)
    
    
    
    
def buscar(request):
    return HttpResponse("Buscando alegremente.")
