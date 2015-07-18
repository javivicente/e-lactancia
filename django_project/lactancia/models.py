# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
import datetime
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template.defaultfilters import date as _date

class Grupo(models.Model):
    nombre = models.CharField(_(u'Nombre'), db_index=True, max_length=255, unique=True)
    fecha_creacion = models.DateTimeField(_(u'Fecha de creación'),auto_now_add = True)
    fecha_modificacion = models.DateTimeField(_(u'Última modificación'), db_index=True, auto_now = True)
    relacionados = models.ManyToManyField('self', blank=True, verbose_name=_(u'grupos con los que se relaciona'))

    class Meta:
        verbose_name = _(u'Grupo')
        verbose_name_plural = _(u'Grupos')
        ordering=['nombre',]
        
    def traducido_al_ingles(self):
        return self.nombre_en != self.nombre_es

    traducido_al_ingles.boolean = True
    traducido_al_ingles.admin_order_field = 'nombre'
    traducido_al_ingles.short_description=_(u'Traducido')
    
    def obten_relacionados(self):
        return ";\n".join([g.nombre for g in self.relacionados.all()])
    obten_relacionados.short_description= _(u'Grupos relacionados')

    def hay_relacionados(self):
        return (self.relacionados.count() > 0)
    hay_relacionados.boolean = True
    hay_relacionados.short_description= _(u'Hay grupos relacionados')

    def num_productos(self):
        return Producto.objects.filter(grupo=self.id).count()
    num_productos.short_description= _(u'Nº productos')

    def visitas(self):
        return Visita.objects.filter(grupo=self.id).count()
    visitas.short_description= _(u'Nº visitas')

    def opiniones_pendientes(self):
        filterargs = { 'grupo': self.id, 'leido': False }
        return Comentario.objects.filter(**filterargs).count()>0
    opiniones_pendientes.boolean = True
    opiniones_pendientes.short_description= _(u'Nuevas opiniones')

    def dime_que_eres(self):
        return u'grupo'

    def __unicode__(self):
        return self.nombre

class Riesgo(models.Model):
    nivel = models.IntegerField(unique=True)
    nombre = models.CharField(_(u'Nombre'), max_length=200)
    descripcion = models.CharField(_(u'Descripción'), max_length=500)
    
    def num_productos(self):
        return Producto.objects.filter(riesgo=self.id).count()
    num_productos.short_description= _(u'Número de productos')

    def dime_que_eres(self):
        return u'riesgo'
        

    def __unicode__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(db_index=True, max_length=255, verbose_name=_(u'Nombre'), unique=True)
    grupo = models.ManyToManyField('grupo')
    riesgo = models.ForeignKey('riesgo', verbose_name=_(u'Nivel de riesgo'))
    comentario = models.CharField(max_length = 10000, blank=True, null=True, verbose_name=_(u'Comentario'))
    no_alternativas = models.BooleanField(default=False, verbose_name=_(u'No puede tener alternativas'), help_text=_(u'Marca esta casilla si no tiene sentido que el término tenga altenativas. Por ejemplo, una enfermedad congénita o adquirida.'))
    alternativas = models.ManyToManyField('self', blank=True, symmetrical=False, verbose_name=_(u'Lista de productos alternativos'))
    tiene_biblio = models.BooleanField(default=True, verbose_name=_(u'Tiene bibliografia (añadida o pendiente de añadir)'), help_text=_(u'Indica si el producto poseera referencias bibliográficas. Si no las va a tener ni ahora ni en el futuro, debe desmarcarse esta casilla. Ejemplos de productos que pueden no tener bibliografía asociada son los de Fitoterapia'))
    biblio = models.ManyToManyField('Bibliografia',verbose_name=_(u'bibliografia'),blank=True)
    csvfile = models.FileField(upload_to='papers/%Y/%m/', verbose_name=_(u'Importar biblio con fichero CSV'), blank=True)
    marcas = models.ManyToManyField('Marca',verbose_name=_(u'Listado de marcas comerciales'),blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add = True, verbose_name=_(u'Fecha de creación'))
    fecha_modificacion = models.DateTimeField(db_index=True, auto_now = True, verbose_name=_(u'Última modificación'))
    peso_molecular = models.CharField(max_length=30, blank=True, null=True, verbose_name=_(u'Peso molecular'))
    union_proteinas = models.CharField(max_length=30, verbose_name=_(u'Unión proteínas'), blank=True, null=True)
    volumen_distrib = models.CharField(max_length=30, verbose_name=_(u'Volumen de distribución'), blank=True, null=True,)
    indice_leche_plasma = models.CharField(max_length=30, blank=True, null=True, verbose_name=_(u'Índice Leche/Plasma'))
    t_maximo = models.CharField(max_length=30, blank=True, null=True, verbose_name=_(u'Tiempo máximo'))
    t_medio = models.CharField(max_length=30, blank=True, null=True, verbose_name=_(u'Tiempo medio'))
    biodisponibilidad = models.CharField(max_length=30, blank=True, null=True, verbose_name=_(u'Biodisponibilidad'))
    dosis_teorica = models.CharField(max_length=30, blank=True, null=True, verbose_name=_(u'Dosis teórica del lactante'))
    dosis_relativa = models.CharField(max_length=30, blank=True, null=True, verbose_name=_(u'Dosis relativa del lactante'))
    dosis_terapeutica = models.CharField(max_length=30, blank=True, null=True, verbose_name=_(u'Porcentaje de la dosis terapéutica'))
    
    def traducido_al_ingles(self):
        return self.nombre_es != self.nombre_en and self.comentario_es != self.comentario_en
    traducido_al_ingles.boolean = True
    traducido_al_ingles.admin_order_field = 'nombre'
    traducido_al_ingles.short_description=_(u'Traducido')

    def hay_alias(self):
        return (self.alias_set.count() > 0)
    hay_alias.boolean=True
    hay_alias.short_description=_(u'Hay alias')
    
    def hay_escrituras(self):
        return (self.otras_escrituras_set.count() > 0)
    hay_escrituras.boolean=True
    hay_escrituras.short_description=_(u'Hay escrituras')


    def hay_alternativas(self):
        return (self.alternativas.count() > 0)
    hay_alternativas.boolean=True
    hay_alternativas.short_description=_(u'Hay alternativas')

    def hay_biblio(self):
        return (self.biblio.count() > 0)
    hay_biblio.boolean=True
    hay_biblio.short_description=_(u'Tiene biblio')

    def num_biblio(self):
        return (self.biblio.count())
    num_biblio.short_description=_(u'Nº refs. bibliográficas')

    def hay_marcas(self):
        return (self.marcas.count() > 0)
    hay_marcas.boolean=True
    hay_marcas.short_description=_(u'Hay marcas')

    def obten_marcas(self):
        return ";\n".join([m.nombre for m in self.marcas.all()])
    obten_marcas.short_description=_(u'Marcas')

    def obten_alternativas(self):
        return ";\n".join([s.nombre for s in self.alternativas.all()])
    obten_alternativas.short_description=_(u'Alternativas')

    def obten_grupos(self):
        return ";\n".join([g.nombre for g in self.grupo.all()])
    obten_grupos.short_description=_(u'Grupo(s)')

    def visitas(self):
        return Visita.objects.filter(prod=self.id).count()
    visitas.short_description= _(u'Nº visitas')

    def opiniones_pendientes(self):
        filterargs = { 'prod': self.id, 'leido': False }
        return Comentario.objects.filter(**filterargs).count()>0
    opiniones_pendientes.boolean = True
    opiniones_pendientes.short_description= _(u'Nuevas opiniones')

    def dime_que_eres(self):
        return u'producto'

    def es_principio_activo(self):
        return  (bool(self.peso_molecular) or
                        bool(self.union_proteinas) or
                        bool(self.volumen_distrib) or
                        bool(self.indice_leche_plasma) or
                        bool(self.t_maximo) or
                        bool(self.t_medio) or
                        bool(self.biodisponibilidad) or
                        bool(self.dosis_teorica) or
                        bool(self.dosis_relativa) or
                        bool(self.dosis_terapeutica))
    es_principio_activo.boolean = True
    es_principio_activo.short_description = _(u'Tiene Farmac.')
       
    def __unicode__(self):
        return unicode(self.nombre)

class Bibliografia(models.Model):
    titulo = models.CharField(_(u'Título'),max_length=1000, unique=False)
    autores = models.CharField(_(u'Autores'), max_length=1000, blank=True, null=True)
    publicacion = models.CharField(_(u'Revista'), max_length=1000, blank=True, null=True)
    anyo = models.PositiveSmallIntegerField(verbose_name=_(u'Año'), blank=True, null=True)
    abstract_link = models.URLField(max_length=500, blank=True, null=True, help_text=_(u'Enlace al abstract del artículo'))
    full_text_link = models.URLField(max_length=500, blank=True, null=True, help_text=_(u'Enlace al texto completo del artículo'))
    pdf = models.FileField(upload_to='papers',  blank=True, verbose_name=_(u'Documento PDF'), help_text=_(u'Sube el pdf del artículo únicamente si no está disponible en ningún enlace externo. De lo contrario, usa los campos de enlaces al abstract o al texto completo.'))
    productos = models.ManyToManyField('Producto',verbose_name=_(u'Productos que referencian este trabajo'), through=Producto.biblio.through, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add = True, verbose_name=_(u'Fecha de creación'))
    fecha_modificacion = models.DateTimeField(auto_now = True, verbose_name=_(u'Última modificación'))

    class Meta:
        unique_together = (("titulo", "autores", "publicacion", "anyo"),)

            
    def hay_productos(self):
        return (self.productos.count() > 0)
    hay_productos.admin_order_field='nombre'
    hay_productos.boolean=True
    hay_productos.short_description=_(u'Hay productos que lo referencian')

    def tiene_pdf(self):
        return (self.pdf.name != u'')
    tiene_pdf.admin_order_field='nombre'
    tiene_pdf.boolean=True
    tiene_pdf.short_description=_(u'PDF adjunto')

    def obten_productos(self):
        return ";\n".join([p.nombre for p in self.productos.all()])
    obten_productos.short_description=_(u'Referencia en')

    def dime_que_eres(self):
        return u'bibliografia'
        

    class Meta:
        verbose_name_plural = _(u'Biblio')
        verbose_name= _(u'Biblio')
        
    
    def __unicode__(self):
        return self.titulo + ', ' + unicode(_(u'Publicada en')) + ' ' + self.publicacion +  ', ' + str(self.anyo)


class Alias(models.Model):

    producto_principal= models.ForeignKey('Producto', verbose_name=_(u'Nombre principal del producto'))
    nombre = models.CharField(_(u'Sinónimo del producto'), db_index=True, max_length=255, blank=True, null=True, help_text=_(u'Nombre en español. Si tiene traducción al inglés, ponla en el campo del nombre en inglés. Sino, deja el campo del nombre en inglés vacío.'))
    fecha_creacion = models.DateTimeField(auto_now_add = True, verbose_name=_(u'Fecha de creación'))
    fecha_modificacion = models.DateTimeField(db_index=True, auto_now = True, verbose_name=_(u'Última modificación'))
        

    class Meta:
        verbose_name_plural = _(u'Sinónimos de productos')
        verbose_name = _(u'Sinónimo de producto')

    def en_ambos_idiomas(self):
        return self.nombre_en != self.nombre_es
    en_ambos_idiomas.boolean = True
    en_ambos_idiomas.short_description= _(u'En inglés y español')

    def visitas(self):
        return Visita.objects.filter(alias=self.id).count()
    visitas.short_description= _(u'Número de visitas')

    def opiniones_pendientes(self):
        filterargs = { 'alias': self.id, 'leido': False }
        return Comentario.objects.filter(**filterargs).count()>0
    opiniones_pendientes.boolean = True
    opiniones_pendientes.short_description= _(u'Nuevas opiniones')

    def dime_que_eres(self):
        return u'alias'
        
    def __unicode__(self):
        return self.nombre



class Otras_escrituras(models.Model):

    producto_principal= models.ForeignKey('Producto', verbose_name=_(u'Nombre principal del producto'))
    nombre = models.CharField(_(u'Producto en otras escrituras'), db_index=True, max_length=255, blank=True, null=True,)
    escritura = models.ForeignKey('Idioma', verbose_name=_(u'Idioma en que está escrito el producto'), null=True, blank=True)    
    fecha_creacion = models.DateTimeField(auto_now_add = True, verbose_name=_(u'Fecha de creación'))
    fecha_modificacion = models.DateTimeField(db_index=True, auto_now = True, verbose_name=_(u'Última modificación'))
        

    class Meta:
        ordering = ['escritura__order', 'nombre']    
        verbose_name_plural = _(u'Otras escrituras del producto')
        verbose_name = _(u'Otras escrituras del producto')

    
    def visitas(self):
        return Visita.objects.filter(otra_escritura=self.id).count()
    visitas.short_description= _(u'Número de visitas')

    def opiniones_pendientes(self):
        filterargs = { 'otra_escritura': self.id, 'leido': False }
        return Comentario.objects.filter(**filterargs).count()>0
    opiniones_pendientes.boolean = True
    opiniones_pendientes.short_description= _(u'Nuevas opiniones')

    def dime_que_eres(self):
        return u'otra_escritura'
        
    def __unicode__(self):
        return self.nombre
        
        
    
class Marca(models.Model):
    nombre = models.CharField(db_index=True, max_length=255, verbose_name=_(u'Nombre comercial'), unique=False)
    pais = models.ForeignKey('Pais', verbose_name=_(u'País donde se comercializa'), null=True, blank=True)
    comentario = models.CharField(max_length=255, blank=True, null=True, verbose_name=_(u'País donde se comercializa'))
    fecha_creacion = models.DateTimeField(auto_now_add = True, verbose_name=_(u'Fecha de creación'))
    fecha_modificacion = models.DateTimeField(db_index=True, auto_now = True, verbose_name=_(u'Última modificación'))
    principios_activos = models.ManyToManyField('Producto',verbose_name=_(u'Listado de principios activos'), through=Producto.marcas.through,blank=True)

    class Meta:
        unique_together = (("nombre", "comentario"),)
    
    def traducido_al_ingles(self):
        return self.comentario_es != self.comentario_en
    traducido_al_ingles.boolean=True
    traducido_al_ingles.short_description= _(u'Traducido al inglés')

    def multiples_principios(self):
        return (self.principios_activos.count() > 1)
    multiples_principios.boolean=True
    multiples_principios.short_description= _(u'Compuesto')

    def obten_pa_con_riesgo_mas_alto(self):
        nombre=''
        max_riesgo=0
        for p in self.principios_activos.all():
            if p.riesgo.nivel >= max_riesgo:
                max_riesgo = p.riesgo.nivel
                nombre = p.nombre

        return nombre

    def obten_pa_con_riesgo_mas_alto_en(self):
        nombre=''
        max_riesgo=0
        for p in self.principios_activos.all():
            if p.riesgo.nivel >= max_riesgo:
                max_riesgo = p.riesgo.nivel
                nombre = p.nombre_ingles

        return nombre

    def obten_riesgo_mas_alto_nivel(self):
                
        max_riesgo=0
        for p in self.principios_activos.all():
            if p.riesgo.nivel >= max_riesgo:
                max_riesgo = p.riesgo.nivel
                                

        return max_riesgo

    def obten_riesgo_mas_alto_descripcion(self):
        riesgo=''
        max_riesgo=0
        for p in self.principios_activos.all():
            if p.riesgo.nivel >= max_riesgo:
                max_riesgo = p.riesgo.nivel
                riesgo = p.riesgo.descripcion

        return riesgo

    def obten_riesgo_mas_alto_descripcion_en(self):
        riesgo=''
        max_riesgo=0
        for p in self.principios_activos.all():
            if p.riesgo.nivel >= max_riesgo:
                max_riesgo = p.riesgo.nivel
                riesgo = p.riesgo.descripcion_ingles

        return riesgo

    def tiene_principios(self):
        return (self.principios_activos.count() > 0)
    tiene_principios.boolean=True
    tiene_principios.short_description= _(u'Tiene principios')
        
    def obten_principios(self):
        return ";\n".join([p.nombre for p in self.principios_activos.all()])
    obten_principios.short_description= _(u'Principios Activos')

    def obten_principios_en(self):
        return ";\n".join([p.nombre_ingles for p in self.principios_activos.all()])
    obten_principios_en.short_description= _(u'Principios Activos inglés')

    def visitas(self):
        return Visita.objects.filter(marca=self.id).count()
    visitas.short_description= _(u'Número de visitas')

    def opiniones_pendientes(self):
        filterargs = { 'marca': self.id, 'leido': False }
        return Comentario.objects.filter(**filterargs).count()>0
    opiniones_pendientes.boolean = True
    opiniones_pendientes.short_description= _(u'Nuevas opiniones')

    def dime_que_eres(self):
        return u'marca'
        
    def __unicode__(self):
        return unicode(self.nombre)

class Mensaje(models.Model):
        
    NIVEL_CHOICES = (
                ('info', _(u'información')),
                ('success', _(u'éxito')),
                ('warning', _(u'alerta')),
                ('danger', _(u'peligro')),
                )
    TIPO_CHOICES = (
                ('cambio_riesgo', _(u'cambio en nivel del riesgo')),
                ('farmacocinetica', _(u'mensaje en variable farmacocinética')),
                ('copyright', _(u'mensaje sobre copyrigh de marcas')),
                ('diclaimer', _(u'mensaje sobre el uso de e-lactancia')),
                ('comentario', _(u'comentario de usuarios')),
                )
    nombre = models.CharField(_(u'Nombre'),max_length=255, unique=True)
    nivel = models.CharField(_(u'Nivel del mensaje'), max_length=7, choices=NIVEL_CHOICES, default='info')
    tipo = models.CharField(_(u'Tipo de mensaje (nivel)'), max_length=15, choices=TIPO_CHOICES)
    titulo = models.CharField(_(u'Título mensaje'), db_index=True, max_length=255)
    contenido = models.CharField(_(u'Cuerpo del mensaje'), db_index=True, max_length=5000, blank=True, null=True)
    producto= models.ForeignKey('Producto', verbose_name=_(u'Producto vinculado a este mensaje'), null=True, blank=True)
    fecha_creacion = models.DateTimeField(_(u'Fecha de creación'),auto_now_add = True)
    fecha_modificacion = models.DateTimeField(_(u'Última modificación'), db_index=True, auto_now = True)
        
        
    def traducido_al_ingles(self):
        return self.titulo_es != self.titulo_en and self.contenido_es != self.contenido_en
    traducido_al_ingles.boolean = True
    traducido_al_ingles.short_description= _(u'Traducido al inglés')
        
    def dime_que_eres(self):
        return u'mensaje'

    def active_30(self):
        if self.tipo== 'cambio_riesgo':
            return self.fecha_modificacion >= timezone.now() - datetime.timedelta(days=30)
        else: return True
    active_30.boolean = True
    active_30.short_description = _(u'Alerta 1 mes')

    def active_90(self):
        if self.tipo== 'cambio_riesgo':
            return self.fecha_modificacion >= timezone.now() - datetime.timedelta(days=90)
        else: return True
    active_90.boolean = True
    active_90.short_description = _(u'Alerta 3 meses')

    def __unicode__(self):
        return self.nombre


class LactUser(models.Model):
    PROFILE_CHOICES = (
                ('1', _(u'Pediatra')),
                ('2', _(u'Ginecóloga/o')),
                ('14', _(u'Médico de familia')),
                ('3', _(u'Otra especialidad médica')),
                ('4', _(u'Matrona')),
                ('5', _(u'Enfermera/o')),
                ('13', _(u'Farmacéutico/a')),
                ('6', _(u'Otro sanitario')),
                ('7', _(u'Consultora lactancia (IBCLC, OMS)')),
                ('8', _(u'Grupo de apoyo')),
                ('9', _(u'Doula')),
                ('10', _(u'Madre/Padre')),
                ('11', _(u'Otro')),
                ('12', _(u'Anónimo')),
                )

    

    session= models.OneToOneField(Session, primary_key=True)
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=_(u'Nombre')) # para permitir usuarios anonimos
    ip_address = models.CharField(verbose_name=_(u'Dirección IP'), max_length=256)
    email = models.EmailField(max_length=254, null=True, blank=True, verbose_name=_(u'e-Mail'))
    nombre = models.CharField(_(u'Nombre'),max_length=255, null=True, blank=True) # Nuevo campo para las Newsletters
    perfil = models.CharField(_(u'Tipo de usuario (perfil)'), max_length=2, choices=PROFILE_CHOICES)
    city = models.CharField(_(u'Ciudad'), max_length=100, null=True, blank=True)
    longitude = models.DecimalField(_(u'Longitud'), max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(_(u'Latitud'), max_digits=9, decimal_places=6, null=True, blank=True)
    country_name = models.CharField(_(u'País'), max_length=255, null=True, blank=True)
    country_code = models.CharField(_(u'Código país'), max_length = 30, null=True, blank=True)
    country_code3 = models.CharField(_(u'Código país 3'), max_length = 30, null=True, blank=True)
    fecha_creacion = models.DateTimeField(_(u'Fecha de creación'),db_index=True, auto_now_add = True)
    
    def num_visitas(self):
        return Visita.objects.filter(user=self.pk).count()

    num_visitas.short_description= _(u'Visitas')

    def ultima_visita(self):
        obj = Visita.objects.filter(user=self.pk).order_by('-id')[0]
        return obj.time

    ultima_visita.short_description= _(u'Última visita')

    def num_comentarios(self):
        return Comentario.objects.filter(user=self.pk).count()

    num_comentarios.short_description= _(u'Comentarios')
        
    def dime_que_eres(self):
        return u'usuario'

    class Meta:
        verbose_name = _(u'Visitante')
        verbose_name_plural = _(u'Visitantes')
                
    def __unicode__(self):
        if self.user != None:
            return self.user.username
        elif self.email != None:
            return self.email
        else:
            if self.perfil == 1:
                return unicode(_(u'Pediatra'))
            elif self.perfil == 2:
                return unicode(_(u'Ginecóloga/o'))
            elif self.perfil == 3:
                return unicode(_(u'Otra especialidad medica'))
            elif self.perfil == 14:
                return unicode(_(u'Médico de familia'))
            elif self.perfil == 4:
                return unicode(_(u'Matrona'))
            elif self.perfil == 5:
                return unicode(_(u'Enfermera/o'))
            elif self.perfil == 13:
                return unicode(_(u'Farmacéutico/a'))
            elif self.perfil == 6:
                return unicode(_(u'Otro sanitario'))
            elif self.perfil == 7:
                return unicode(_(u'Consultora lactancia (IBCLC, OMS)'))
            elif self.perfil == 8:
                return unicode(_(u'Grupo de apoyo'))
            elif self.perfil == 9:
                return unicode(_(u'Doula'))
            elif self.perfil == 10:
                return unicode(_(u'Madre/Padre'))
            elif self.perfil == 11:
                return unicode(_(u'Otro'))
            else:
                return unicode(_(u'Anónimo'))

class Visita(models.Model):
    user = models.ForeignKey('LactUser')
    prod = models.ForeignKey('Producto', null=True, blank=True, related_name='visita_producto')
    alias = models.ForeignKey('Alias', null=True, blank=True, related_name='visita_alias')
    otra_escritura = models.ForeignKey('Otras_escrituras', null=True, blank=True, related_name='visita_otras_escrituras')
    marca = models.ForeignKey('Marca', null=True, blank=True, related_name='visita_marca')
    grupo = models.ForeignKey('Grupo', null=True, blank=True, related_name='visita_grupo')
    lang = models.CharField(u'Idioma',max_length=7)
    time = models.DateTimeField(u'Acceso', db_index=True, auto_now = True)

    def item_name(self):
        if self.prod != None:
            return self.prod.nombre
        elif self.alias != None:
            return self.alias.nombre
        elif self.otra_escritura != None:
            return self.otra_escritura.nombre
        elif self.marca != None:
            return self.marca.nombre
        elif self.grupo != None:
            return self.grupo.nombre
        item_name.short_description = _(u'Término visitado')
        

    def __unicode__(self):
        return unicode(self.user) + u' ' + unicode(_(u'ha visitado')) + u' ' + unicode(self.item_name())  + u' ' + unicode(_date(self.time, settings.DATETIME_FORMAT))


class Comentario(models.Model):
    user = models.ForeignKey('LactUser', null=True, blank=True)
    comentario = models.CharField(max_length = 500, verbose_name=_(u'Opinión'))
    leido = models.BooleanField(default=False, verbose_name=_(u'Opinión ya leída'))
    prod = models.ForeignKey('Producto', null=True, blank=True, related_name='comentario_producto')
    alias = models.ForeignKey('Alias', null=True, blank=True, related_name='comentario_alias')
    otra_escritura = models.ForeignKey('Otras_escrituras', null=True, blank=True, related_name='comentario_otras_escrituras')
    marca = models.ForeignKey('Marca', null=True, blank=True, related_name='comentario_marca')
    grupo = models.ForeignKey('Grupo', null=True, blank=True, related_name='comentario_grupo')
    mensaje = models.ForeignKey('Mensaje', null=True, blank=True, related_name='comentario_general')
    lang = models.CharField(_(u'Idioma'),max_length=7)
    fecha_creacion = models.DateTimeField(_(u'Fecha de creación'),auto_now_add = True)
    fecha_modificacion = models.DateTimeField(_(u'Última modificación'), auto_now = True)
        
    def item_name(self):
        if self.prod != None:
            return self.prod.nombre
        elif self.alias != None:
            return self.alias.nombre
        elif self.otra_escritura != None:
            return self.otra_escritura.nombre
        elif self.marca != None:
            return self.marca.nombre
        elif self.grupo != None:
            return self.grupo.nombre
        elif self.mensaje != None:
            return self.mensaje.nombre
    item_name.short_description = _(u'Término')

        #class Meta:
        #        verbose_name = u'Opinion de visitante'
        #        verbose_name_plural = u'Opiniones de visitantes'        

    def __unicode__(self):
        return unicode(self.item_name())

class Idioma(models.Model):
    nombre = models.CharField(_(u'Idioma o escritura'), max_length=100)
    order = models.PositiveIntegerField()
    
    class Meta:
        verbose_name = _(u'Idioma o escritura')
        verbose_name_plural = _(u'Idiomas o escrituras')
        ordering=['order']
        
    def productos(self):
        return ";\n".join([p.producto_principal for p in Otras_escrituras.objects.filter(escritura=self.id)])
    productos.short_description= _(u'Productos en este idioma')
    
    def num_productos(self):
        return Otras_escrituras.objects.filter(escritura=self.id).count()
    num_productos.short_description= _(u'Num de productos en este idioma')
        
    def save(self, *args, **kwargs):
        for field_name in ['nombre', 'nombre_es', 'nombre_en']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.strip().capitalize())
        super(Idioma, self).save(*args, **kwargs) 
        
    def __unicode__(self):
        return self.nombre

class Pais(models.Model):
    nombre = models.CharField(_(u'Nombre'), max_length=100)

    class Meta:
        verbose_name=_(u'País')
        verbose_name_plural =_(u'Países')
        ordering=['nombre']
        
    def __unicode__(self):
        return self.nombre

        
        
        
     
from ratings.handlers import ratings, RatingHandler
from ratings.forms import StarVoteForm

class MyHandler(RatingHandler):
    allow_anonymous = True
    score_range =(1,5)
    score_step=1
    votes_per_ip_address = 0
    form_class=StarVoteForm

    def allow_key(self, request, instance, key):
        return key in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14')
    
    def get_key(self, request, instance):
        key = request.session['perfil']
        return str(key)

ratings.register([Producto, Grupo, Marca], MyHandler)

