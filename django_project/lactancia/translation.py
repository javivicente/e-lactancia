# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from modeltranslation.translator import translator, TranslationOptions
from lactancia.models import Grupo, Riesgo, Marca, Producto, Alias, Mensaje, LactUser, Comentario, Visita, Idioma, Pais, Aval, Cajita

class Grupo_TO(TranslationOptions):
    fields = ('nombre',)
 
translator.register(Grupo, Grupo_TO)

class Riesgo_TO(TranslationOptions):
    fields = ('descripcion','nombre',)
 
translator.register(Riesgo, Riesgo_TO)

class Producto_TO(TranslationOptions):
    fields = ('nombre','comentario',)
 
translator.register(Producto, Producto_TO)

class Alias_TO(TranslationOptions):
    fields = ('nombre',)
 
translator.register(Alias, Alias_TO)

class Idioma_TO(TranslationOptions):
    fields = ('nombre',)
 
translator.register(Idioma, Idioma_TO)

class Pais_TO(TranslationOptions):
    fields = ('nombre',)
 
translator.register(Pais, Pais_TO)

class Aval_TO(TranslationOptions):
    fields = ('extracto',)
 
translator.register(Aval, Aval_TO)

class Cajita_TO(TranslationOptions):
    fields = ('titulo', 'texto', 'link', 'texto_link')
 
translator.register(Cajita, Cajita_TO)

class Marca_TO(TranslationOptions):
    fields = ('comentario','nombre_paises')
 
translator.register(Marca, Marca_TO)


class Mensaje_TO(TranslationOptions):
    fields = ('titulo', 'contenido',)
 
translator.register(Mensaje, Mensaje_TO)

