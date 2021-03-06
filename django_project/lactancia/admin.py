# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.forms import ModelForm, TextInput, Textarea, ValidationError
from lactancia.models import Grupo, Riesgo, Marca, Producto, Alias, Otras_escrituras, Bibliografia, Mensaje, LactUser, Comentario, Visita, Pais, Idioma, Aval, Patrocinador, Cajita, Icono, Docs
from lactancia.models import Visita_grupo_total, Visita_grupo_perfil
from lactancia.models import Visita_producto_total, Visita_producto_perfil
from lactancia.models import Visita_alias_total, Visita_alias_perfil
from lactancia.models import Visita_otras_escrituras_total, Visita_otras_escrituras_perfil
from lactancia.models import Visita_marca_total, Visita_marca_perfil
from django import forms
from django.db import models
from suit.widgets import EnclosedInput, AutosizedTextarea
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _
import csv
from suit.admin import SortableModelAdmin
from django_select2.forms import Select2Widget, Select2MultipleWidget, ModelSelect2Widget, ModelSelect2MultipleWidget, ModelSelect2TagWidget
from import_export.admin import ExportMixin
from import_export import resources
from import_export import fields


    
    
class GrupoComentariosInline(admin.TabularInline):
        model = Comentario
        #suit_classes = 'suit-tab suit-tab-g_comentarios'
        readonly_fields = ('user', 'comentario','grupo','fecha_creacion','fecha_modificacion',)
        exclude = ('alias','marca','otra_escritura','prod','mensaje','lang',)
        extra = 0

class GrupoForm(ModelForm):
        class Meta:
                widgets = {
                       'nombre_es': AutosizedTextarea(attrs={'rows': 1, 'class': 'span6'}),
                       'nombre_en': AutosizedTextarea(attrs={'rows': 1, 'class': 'span6'}),
                       'relacionados': Select2MultipleWidget(attrs={'rows': 3, 'class': 'span12'}),
                       
                       #'slug': AutosizedTextarea(attrs={'rows': 1, 'class': 'span12'}),
                        }
                        
                exclude= ('nombre','slug',)

class GrupoResource(resources.ModelResource):
    relacionados = fields.Field()
    num_productos = fields.Field()
    visitas = fields.Field()
    
    class Meta: 
        model = Grupo
        fields = ( 'id',
                   'nombre',
                   'relacionados',
                   'num_productos',
                   'visitas',
                   'fecha_modificacion',
                    )
        export_order = ( 'id',
                   'nombre',
                   'relacionados',
                   'num_productos',
                   'visitas',
                   'fecha_modificacion',
                   )
    
    def dehydrate_relacionados(self, object):
        return unicode(object.obten_relacionados())
        
    
    def dehydrate_num_productos(self, obj):
        return unicode(obj.num_productos())
    
    def dehydrate_visitas(self, obj):
        return unicode(obj.visitas())
        
                   
                
class GrupoAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('nombre','slug', 'num_productos','obten_relacionados','opiniones_pendientes','visitas','fecha_modificacion','traducido_al_ingles',)
    ordering = ('nombre',)
    search_fields = ('nombre_es','nombre_en')
    #filter_horizontal = ('relacionados',)
    readonly_fields = ('fecha_creacion', 'fecha_modificacion','visitas','slug',)
    inlines = [GrupoComentariosInline,]
    date_hierarchy = 'fecha_modificacion'
    form = GrupoForm
    resource_class = GrupoResource
    fieldsets = [
                (None, {
                        'classes': ('wide',),
                        'fields': ('nombre_es','nombre_en','slug')
                }),
                (_(u'Grupos relacionados'), {
                        'fields': ('relacionados',)
                }),
                (_('Visitas y fechas'), {
                        'fields': (('fecha_creacion','fecha_modificacion'), 'visitas')
                }),
                
        ]
    
admin.site.register(Grupo, GrupoAdmin)

class RiesgoForm(ModelForm):
        class Meta:
                widgets = {
                       'descripcion_es': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
                       'descripcion_en': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
                        
                        }
                        
                exclude= ('descripcion','nombre',)

class RiesgoAdmin(admin.ModelAdmin):
    list_display = ('nivel','nombre_es','nombre_en','descripcion_es','descripcion_en','num_productos')
    ordering = ('nivel',)
    form = RiesgoForm

admin.site.register(Riesgo, RiesgoAdmin)


class MarcaComentariosInline(admin.TabularInline):
        model = Comentario
        readonly_fields = ('user', 'comentario','marca','fecha_creacion','fecha_modificacion',)
        exclude = ('alias','otra_escritura', 'grupo','prod','mensaje','lang',)
        extra = 0
        
class MarcaForm(ModelForm):
        class Meta:
                widgets = {
                            'paises': Select2MultipleWidget(attrs={'class':'span12'}),
                            'principios_activos': Select2MultipleWidget(attrs={'class':'span12'}),
                        }

       
        def clean(self):
            nombre = self.cleaned_data.get('nombre')
            paises = self.cleaned_data.get('paises')
            if self.instance and self.instance.pk:
                marcas_mismo_nombre = Marca.objects.filter(nombre=nombre).exclude(id=self.instance.pk)
            else:
                marcas_mismo_nombre = Marca.objects.filter(nombre=nombre)
            if marcas_mismo_nombre>0:
                for m in marcas_mismo_nombre:
                    current_paises = m.paises.all()
                    if len(current_paises)==0 and len(paises)==0: # if [] == []:
                        raise ValidationError(_(u"Ya existe una marca con este nombre. Para poder salvarla debes especificar uno o más países de comercialización."))
                    for c in current_paises:
                        if c in paises:
                            raise ValidationError(unicode(_(u'Ya existe una marca con este nombre que se comercializa en ')) + c.nombre + unicode('.'))
        
        def save(self, commit=True):
            # Get the unsave Marca instance
            instance = forms.ModelForm.save(self, False)                   
            #print 'salvamos instancia'
            instance.save()
            #print 'salvamos many2many'
            self.save_m2m()
            return instance

class MarcaResource(resources.ModelResource):
    paises = fields.Field()
    principios_activos = fields.Field()
    visitas = fields.Field()
    
    class Meta: 
        model = Marca
        fields = ( 'id','nombre',
                   'paises',
                   'principios_activos',
                   'visitas',
                   'fecha_modificacion',
                    )
        export_order = ( 'id','nombre',
                   'paises',
                   'principios_activos',
                   'visitas',
                   'fecha_modificacion',
                   )
    
    def dehydrate_paises(self, object):
        return unicode(object.en_paises())
        
    
    def dehydrate_principios_activos(self, obj):
        return unicode(obj.obten_principios())
    
    def dehydrate_visitas(self, obj):
        return unicode(obj.visitas())
            
class MarcaAdmin(ExportMixin, admin.ModelAdmin):
    save_as = True
    list_display = ('nombre','multiples_principios','slug', 'obten_principios','en_paises',
                        'opiniones_pendientes','visitas','fecha_modificacion','traducido_al_ingles',)
    search_fields = ['nombre','principios_activos__nombre',]
    form = MarcaForm
    list_filter = ( 'principios_activos', )
    resource_class = MarcaResource
    ordering = ('nombre',)
    readonly_fields = ('fecha_creacion','fecha_modificacion', 'visitas','slug')
    inlines = [MarcaComentariosInline, ]
    date_hierarchy = 'fecha_modificacion'
    
    fieldsets = (
                (None, {
                        'fields': ('nombre','slug',)
                }),
                (_(u'Países donde se comercializa'), {
                        'fields': ('paises',)
                }),
                (_(u'Principios activos'), {
                        'fields': ('principios_activos',)
                }),
                (_(u'Visitas y fechas'), {
                        'fields': (('fecha_creacion','fecha_modificacion'), 'visitas',)
                }),
        )
        

admin.site.register(Marca, MarcaAdmin)


class AliasComentariosInline(admin.TabularInline):
        model = Comentario
        readonly_fields = ('user', 'comentario','alias','fecha_creacion','fecha_modificacion',)
        exclude = ('marca','grupo','otra_escritura', 'prod','mensaje','lang',)
        extra = 0

class AliasForm(ModelForm):
        class Meta:
                model = Alias
                widgets = {
                        #'slug': AutosizedTextarea(attrs={'rows': 1, 'class': 'span12'}),
                        'nombre_es': AutosizedTextarea(attrs={'rows': 1, 'class': 'span8'}),
                        'nombre_en': AutosizedTextarea(attrs={'rows': 1, 'class': 'span8'}),
                        'producto_principal': Select2Widget(attrs={'rows': 1, 'class': 'span8'}),
                }
                exclude= ('nombre','slug',)
        
        def clean(self):
            nombre_es = self.cleaned_data.get('nombre_es')
            nombre_en = self.cleaned_data.get('nombre_en')
            if not nombre_en and not nombre_es:
                raise ValidationError(_(u"Debes indicar al menos un sinónimo (en inglés o en español)."))

class AliasResource(resources.ModelResource):
    producto_principal = fields.Field()
    visitas = fields.Field()
    
    class Meta: 
        model = Alias
        fields = ( 'nombre',
                   'producto_principal',
                   'visitas',
                   'fecha_modificacion',
                    )
        export_order = ( 'nombre',
                   'producto_principal',
                   'visitas',
                   'fecha_modificacion',
                   )
    
    def dehydrate_paises(self, object):
        return unicode(object.en_paises())
        
    def dehydrate_producto_principal(self, obj):
        return unicode(obj.producto_principal.nombre)
    
    def dehydrate_visitas(self, obj):
        return unicode(obj.visitas())
                
class AliasAdmin(ExportMixin, admin.ModelAdmin):
    form = AliasForm
    resource_class = AliasResource
    list_display = ('producto_principal','nombre_es', 'nombre_en', 'slug',
                        'opiniones_pendientes','visitas', 'fecha_modificacion','en_ambos_idiomas')
    search_fields = ('producto_principal__nombre', 'nombre_es','nombre_en',)
    ordering = ('producto_principal__nombre',)
    list_filter = ( 'producto_principal', )
    readonly_fields = ('fecha_creacion','fecha_modificacion','visitas','slug',)
    inlines = [AliasComentariosInline, ]
    date_hierarchy = 'fecha_modificacion'

    fieldsets = (
                (_(u'Alias'), {
                        'fields': ('nombre_es','nombre_en','slug',)
                }),
                (_(u'Nombre Principal'), {
                        'fields': ('producto_principal',)
                }),
                (_(u'Visitas y fechas'), {
                        'fields': (('fecha_creacion','fecha_modificacion',), 'visitas',)
                }),
        )

    def save_model(self, request, obj, form, change):
        if not obj.nombre_es:
            obj.nombre_es=''
        obj.save()
        
    def delete_model(self, request, obj):
        if not obj.nombre_es:
            obj.nombre_es=''
        obj.delete()
        
admin.site.register(Alias, AliasAdmin)


class Otras_escrituras_ComentariosInline(admin.TabularInline):
        model = Comentario
        readonly_fields = ('user', 'comentario','otra_escritura','fecha_creacion','fecha_modificacion',)
        exclude = ('marca','alias', 'grupo','prod','mensaje','lang',)
        extra = 0

class Otras_escriturasForm(ModelForm):
        class Meta:
                model = Otras_escrituras
                widgets = {
                        #'slug': AutosizedTextarea(attrs={'rows': 1, 'class': 'span12'}),
                        'nombre': AutosizedTextarea(attrs={'rows': 1, 'class': 'span4'}),
                        'producto_principal': Select2Widget(attrs={'rows': 1, 'class': 'span8'}),
                        'escritura': Select2Widget(attrs={'rows': 1, 'class': 'span6'}),
                }
                exclude= ['idioma', 'slug',]
        

class Otras_escriturasResource(resources.ModelResource):
    producto_principal = fields.Field()
    escritura = fields.Field()
    visitas = fields.Field()
    
    class Meta: 
        model = Otras_escrituras
        fields = ( 'id', 'nombre',
                   'producto_principal',
                   'escritura',
                   'visitas',
                   'fecha_modificacion',
                    )
        export_order = ( 'id', 'nombre',
                   'producto_principal',
                   'escritura',
                   'visitas',
                   'fecha_modificacion',
                   )
    
    def dehydrate_paises(self, object):
        return unicode(object.en_paises())
        
    def dehydrate_producto_principal(self, obj):
        return unicode(obj.producto_principal.nombre)
    
    def dehydrate_escritura(self, obj):
        return unicode(obj.escritura.nombre)
    
    def dehydrate_visitas(self, obj):
        return unicode(obj.visitas())
        
class Otras_escriturasAdmin(ExportMixin, admin.ModelAdmin):
    form = Otras_escriturasForm
    resource_class = Otras_escriturasResource
    list_display = ('nombre', 'producto_principal', 'slug', 'escritura',
                        'opiniones_pendientes','visitas', 'fecha_modificacion',)
    search_fields = ('producto_principal__nombre', 'nombre',)
    list_filter=('escritura','producto_principal',)
    #prepopulated_fields = {'slug': ('nombre',)}
    ordering = ('escritura__order','producto_principal__nombre',)
    readonly_fields = ('fecha_creacion','fecha_modificacion','visitas','slug')
    
    inlines = [Otras_escrituras_ComentariosInline, ]
    date_hierarchy = 'fecha_modificacion'

    fieldsets = (
                (_(u'Otras escrituras'), {
                        'fields': ('nombre','escritura','slug',)
                }),
                (_(u'Nombre Principal'), {
                        'fields': ('producto_principal',)
                }),
                (_(u'Visitas y fechas'), {
                        'fields': (('fecha_creacion','fecha_modificacion',), 'visitas',)
                }),
        )

admin.site.register(Otras_escrituras, Otras_escriturasAdmin)


class BiblioForm(ModelForm):
        class Meta:
                model = Bibliografia
                widgets = {
                        'autores': AutosizedTextarea(attrs={'rows': 1, 'class': 'span12'}),
                        'titulo': AutosizedTextarea(attrs={'rows': 1, 'class': 'span12'}),
                        'publicacion': AutosizedTextarea(attrs={'rows': 1, 'class': 'span8'}),
                        'anyo': AutosizedTextarea(attrs={'rows': 1, 'class': 'input-small'}),
                        'detalle_publicacion': AutosizedTextarea(attrs={'rows': 1, 'class': 'span8'}),
                        'productos': Select2MultipleWidget(attrs={'rows': 5, 'class': 'span12'}),
                        }
                fields= '__all__'
        
        #productos = forms.ModelMultipleChoiceField(queryset=Producto.objects.all(),required=False,widget=FilteredSelectMultiple(verbose_name=u'Productos', is_stacked=True))
        # Overriding __init__ here allows us to provide initial
        # data for 'productos' field
        def __init__(self, *args, **kwargs):
                super(BiblioForm, self).__init__(*args, **kwargs)
                # Only in case we build the form from an instance
                # (otherwise, 'biblio' list should be empty)
                if self.instance and self.instance.pk:
                #if 'instance' in kwargs:
                    # We get the 'initial' keyword argument or initialize it
                    # as a dict if it didn't exist.                
                    initial = kwargs.setdefault('initial', {})
                    # The widget for a ModelMultipleChoiceField expects
                    # a list of primary key for the selected data.
                    initial['productos'] = [t.pk for t in kwargs['instance'].productos.all()]

                forms.ModelForm.__init__(self, *args, **kwargs)
                #ModelSelect2MultipleWidget.__init__(self, *args, **kwargs)

        # Overriding save allows us to process the value of 'bibliography' field    
        def save(self, commit=True):
                # Get the unsave Producto instance
                instance = forms.ModelForm.save(self, False)
        
                # Prepare a 'save_m2m' method for the form,
                old_save_m2m = self.save_m2m
                def save_m2m():
                   old_save_m2m()
                   # This is where we actually link the Producto with Bibliografia

                   # first we add those articles already selected in the widget
                   instance.productos.clear()
                   for p in self.cleaned_data['productos']:
                        instance.productos.add(p)
                        # we save each product in order to
                        # update its last accessed date field
                        # ------------ Updated at 06-12-2014 ------
                        # Administrators don´t want products to be
                        # updated every time we add bibliography:
                        #p.save()
                               
                   
                self.save_m2m = save_m2m

                # Do we need to save all changes now?
                if commit:
                    instance.save()
                    self.save_m2m()

                return instance
        
class BiblioResource(resources.ModelResource):
    productos = fields.Field()
    pdf_link = fields.Field()
    
    class Meta: 
        model = Bibliografia
        fields = ( 'titulo',
                   'autores',
                   'publicacion',
                   'anyo',
                   'detalle_publicacion',
                   'productos',
                   'abstract_link',
                   'full_text_link',
                   'pdf_link',
                   'fecha_modificacion',
                    )
        export_order = ( 'titulo',
                   'autores',
                   'publicacion',
                   'anyo',
                   'detalle_publicacion',
                   'productos',
                   'abstract_link',
                   'full_text_link',
                   'pdf_link',
                   'fecha_modificacion',
                   )
    
    def dehydrate_paises(self, object):
        return unicode(object.en_paises())
        
    def dehydrate_pdf_link(self, obj):
        if obj.pdf:
            return unicode('http://www.e-lactancia.org' + obj.pdf.url)
        return ''
    
    def dehydrate_visitas(self, obj):
        return unicode(obj.visitas())
        
class BibliografiaAdmin(ExportMixin, admin.ModelAdmin):
        form = BiblioForm
        resource_class = BiblioResource
        list_display = ('titulo', 'anyo', 'publicacion', 'autores', 'obten_productos', 'tiene_pdf','fecha_modificacion',)
        search_fields = ('publicacion', 'titulo', 'autores','productos__nombre')
        ordering = ('-anyo',)
        readonly_fields = ('fecha_creacion','fecha_modificacion',)
        #filter_horizontal = ('productos',)
        list_filter = ('productos','fecha_modificacion',)
        
        

        fieldsets = (
                (None, {
                        'classes': ('wide',),
                        'fields': ('autores','titulo','publicacion', 'anyo', 'detalle_publicacion',)
                }),
                (_(u'Enlaces'), {
                        'fields': ('abstract_link', 'full_text_link','pdf')
                }),        
                (_(u'Productos que cita este trabajo'), {
                        'classes': ('collapse',),
                        'fields': ('productos',)
                }),        
        )

admin.site.register(Bibliografia, BibliografiaAdmin)



        
class ProductoForm(ModelForm):
        
        
        class Meta:
                model = Producto
                widgets = {
                        #'slug': AutosizedTextarea(attrs={'rows': 1, 'class': 'span12'}),
                        'nombre_es': AutosizedTextarea(attrs={'rows': 1, 'class': 'span4'}),
                        'nombre_en': AutosizedTextarea(attrs={'rows': 1, 'class': 'span4'}),
                        'comentario_es': AutosizedTextarea(attrs={'rows': 15, 'class': 'span12'}),
                        'comentario_en': AutosizedTextarea(attrs={'rows': 15, 'class': 'span12'}),
                        'biodisponibilidad': EnclosedInput(append='%'),
                        'peso_molecular': EnclosedInput(append='daltons'),
                        'union_proteinas': EnclosedInput(append='%'),
                        'volumen_distrib': EnclosedInput(append='l/Kg'),
                        'pka': EnclosedInput(append=''),
                        't_maximo': EnclosedInput(append='horas'),
                        't_medio': EnclosedInput(append='horas'),
                        'indice_leche_plasma': EnclosedInput(append=''),
                        'dosis_teorica': EnclosedInput(append='mg/Kg/d'),
                        'dosis_relativa': EnclosedInput(append='%'),
                        'dosis_terapeutica': EnclosedInput(append='%'),
                        'grupo': Select2MultipleWidget(attrs={'rows': 1, 'class': 'span12'}),
                        'alternativas': Select2MultipleWidget(attrs={'rows': 1, 'class': 'span12'}),
                        'referencia_otros_productos': Select2MultipleWidget(attrs={'rows': 1, 'class': 'span12'}),
                        'referencia_grupos': Select2MultipleWidget(attrs={'rows': 1, 'class': 'span12'}),
                        'biblio': Select2MultipleWidget(attrs={'rows': 5, 'class': 'span12'}),
                        }
                exclude = ('nombre', 'comentario',)
        
        #biblio = forms.ModelMultipleChoiceField(queryset=Bibliografia.objects.all(),required=False,widget=FilteredSelectMultiple(verbose_name=_(u'Artículos'), is_stacked=True))
        # Overriding __init__ here allows us to provide initial
        # data for 'biblio' field
        def __init__(self, *args, **kwargs):
                super(ProductoForm, self).__init__(*args, **kwargs)
                # Only in case we build the form from an instance
                # (otherwise, 'biblio' list should be empty)
                if self.instance and self.instance.pk:
                #if 'instance' in kwargs:
                    # We get the 'initial' keyword argument or initialize it
                    # as a dict if it didn't exist.                
                    initial = kwargs.setdefault('initial', {})
                    # The widget for a ModelMultipleChoiceField expects
                    # a list of primary key for the selected data.
                    initial['biblio'] = [t.pk for t in kwargs['instance'].biblio.all()]

                forms.ModelForm.__init__(self, *args, **kwargs)

        
        # Overriding save allows us to process the value of 'bibliography' field    
        def save(self, commit=True):

                # Get the unsave Producto instance
                instance = forms.ModelForm.save(self, False)

                
                # Let's update the last modified date of the Grupo
                # by saving it (in that way, it reflects the last time a member
                # of Grupo was updated:
                for g in self.cleaned_data['grupo']:
                  g.save()
        
                # Prepare a 'save_m2m' method for the form,
                old_save_m2m = self.save_m2m


                # Check if there is a change in the risk associated to the
                # product. If so, an alert will be created to display in the web.
                
                # Get the current risk associated to the product
                try:
                        orig = Producto.objects.get(nombre_es=self.cleaned_data['nombre_es'])
                except Producto.DoesNotExist:
                        pass
                else:
                        new_risk = self.cleaned_data['riesgo']
                        if orig.riesgo.nivel != new_risk.nivel:
                                
                                if orig.riesgo.nivel < new_risk.nivel:
                                        m, created = Mensaje.objects.get_or_create(
                                                            nombre = orig.nombre,
                                                            nivel = 'warning',
                                                            tipo = 'cambio_riesgo')
                                        m.titulo_es = '<p class="text-error">' + u'Nivel de riesgo incrementado' + '</p>'
                                        m.titulo_en = '<p class="text-error">' + u'Increased level of risk' + '</p>'
                                else:
                                        m, created = Mensaje.objects.get_or_create(
                                                            nombre = orig.nombre,
                                                            nivel = 'warning',
                                                            tipo = 'cambio_riesgo')
                                        m.titulo_es = u'<p class="text-success">Nivel de riesgo rebajado</p>'
                                        m.titulo_en = u'<p class="text-success">Decreased level of risk</p>'
                                m.contenido_es = u'Nuevas evidencias científicas han llevado al equipo de Apilam a actualizar el nivel de riesgo asociado a este producto.<br/><strong>El nivel de riesgo anterior, ' + orig.riesgo.nombre_es + u', pasa a ser ' + new_risk.nombre_es + u'</strong>.'
                                m.contenido_en = u'New scientific evidences have driven the Apilam staff to update the level of risk associated to this product.<br/><strong>Former level of risk, which was ' + orig.riesgo.nombre_en + u', is now set to ' + new_risk.nombre_en + u'</strong>.'
                                m.producto = orig
                                m.save()
                
                def save_m2m():
                   old_save_m2m()
                   # This is where we actually link the Producto with Bibliografia

                   # first we add those articles already selected in the widget
                   instance.biblio.clear()
                   for article in self.cleaned_data['biblio']:
                        instance.biblio.add(article)
                               
                   # second, we add the articles in the csv file    
                   # BUT ONLY IN CASE THE FILE HAS CHANGED
                   # (this is the desired behaviour for administrators since they might
                   # edit the list AFTER the CSV is loaded and remove some item(s).
                   # If we dont control this, each time the product is saved the list of
                   # papers from the csv will override their content paper curation.)
                   if instance.csvfile != self.cleaned_data['csvfile']:
                       file = self.cleaned_data['csvfile']
                       if file and file.name.endswith('.csv'):
                            records = csv.reader(file)
                            for line in records:
                                    if line[0] != 'Title':
                                            b, created = Bibliografia.objects.get_or_create(
                                                        titulo=line[0],
                                                        autores=line[2],
                                                        publicacion = line[4][:-4],
                                                        anyo = line[4][-4:]
                                                        )
                                            
                                            b.abstract_link="http://www.ncbi.nlm.nih.gov"+ line[1]
                                            b.detalle_publicacion = line[3].split(' doi')[0]
                                            b.save()
                                            instance.biblio.add(b)
                self.save_m2m = save_m2m

                
                
                # Do we need to save all changes now?
                if commit:
                    instance.save()
                    self.save_m2m()

                return instance
        

class AliasInline(admin.TabularInline):
        model = Alias
        form = AliasForm
        suit_classes = 'suit-tab suit-tab-nombre'
        extra = 0
        
class Otras_escriturasInline(admin.TabularInline):
        model = Otras_escrituras
        sortable = 'order'
        form = Otras_escriturasForm
        suit_classes = 'suit-tab suit-tab-nombre'
        extra = 0
        
class ProdComentariosInline(admin.TabularInline):
        model = Comentario
        suit_classes = 'suit-tab suit-tab-p_comentarios'
        readonly_fields = ('user', 'comentario','prod','fecha_creacion','fecha_modificacion',)
        exclude = ('alias','otra_escritura','marca','grupo','mensaje','lang',)
        extra = 0

class ProductoResource(resources.ModelResource):
    riesgo = fields.Field()
    grupos = fields.Field()
    visitas = fields.Field()
    alternativas = fields.Field()
    num_referencias_biblio = fields.Field()
    comentario_productos = fields.Field()
    comentario_grupos = fields.Field()
    
    class Meta: 
        model = Producto
        fields = ( 'id','nombre',
                   'riesgo',
                   'grupos',
                   'comentario',
                   'comentario_productos',
                   'comentario_grupos',
                   'alternativas',
                   'biodisponibilidad',
                   'peso_molecular',
                   'union_proteinas',
                   'volumen_distrib',
                   'pka',
                   't_maximo',
                   't_medio', 
                   'indice_leche_plasma', 
                   'dosis_teorica',
                   'dosis_relativa',
                   'dosis_terapeutica',
                   'visitas',
                   'num_referencias_biblio',
                   'fecha_modificacion',
                    )
        export_order = ( 'id','nombre',
                   'riesgo',
                   'grupos',
                   'comentario',
                   'comentario_productos',
                   'comentario_grupos',
                   'alternativas',
                   'biodisponibilidad',
                   'peso_molecular',
                   'union_proteinas',
                   'volumen_distrib',
                   'pka',
                   't_maximo',
                   't_medio', 
                   'indice_leche_plasma', 
                   'dosis_teorica',
                   'dosis_relativa',
                   'dosis_terapeutica',
                   'visitas',
                   'num_referencias_biblio',
                   'fecha_modificacion',
                    )
    
    def dehydrate_riesgo(self, object):
        if object.riesgo:
            return unicode(object.riesgo.nivel)
        else:
            return ''
    
    def dehydrate_grupos(self, obj):
        return unicode(obj.obten_grupos())
    
    def dehydrate_alternativas(self, obj):
        return unicode(obj.obten_alternativas())
        
    def dehydrate_comentario_productos(self, obj):
        return unicode(obj.obten_referencia_otros_productos())
    
    def dehydrate_comentario_grupos(self, obj):
        return unicode(obj.obten_referencia_grupos())
        
    def dehydrate_visitas(self, obj):
        return unicode(obj.visitas())
        
    def dehydrate_num_referencias_biblio(self, object):
        return unicode(object.num_biblio())

        
class ProductoAdmin(ExportMixin, admin.ModelAdmin):
        
    form = ProductoForm
    resource_class = ProductoResource
    list_display = ('nombre', 'riesgo', 'obten_alternativas', 'obten_grupos', 'obten_marcas', 'num_biblio','biblio_en_vancouver', 'es_principio_activo','opiniones_pendientes','visitas', 'fecha_modificacion','traducido_al_ingles',)
    #list_display = ('nombre', 'riesgo', 'obten_alternativas', 'obten_grupos', 'num_marcas', 'tiene_biblio','num_biblio', 'es_principio_activo','opiniones_pendientes', 'fecha_modificacion','traducido_al_ingles',)
    list_filter = ( 'riesgo', 'grupo', )
    ordering = ('nombre',)
    search_fields = ('nombre_es', 'nombre_en',)
    #filter_horizontal = ('grupo','alternativas','marcas','biblio',)
    #filter_horizontal = ('biblio',)
    readonly_fields = ('fecha_creacion','fecha_modificacion', 'visitas','slug',)
    #readonly_fields = ('fecha_creacion','fecha_modificacion', )
    inlines = [Otras_escriturasInline, AliasInline, ProdComentariosInline, ]
    date_hierarchy = 'fecha_modificacion'
    list_select_related = True
    
    fieldsets = [
                (None, {
                        'classes': ('suit-tab suit-tab-nombre',),
                        'fields': []
                }),
                ('Nombre principal', {
                        'fields': ('nombre_es','nombre_en','slug',)
                }),
                #(None, {
                #        'classes': ('suit-tab suit-tab-marcas',),
                #        'fields': ['marcas']
                #}),
                (None, {
                        'classes': ('suit-tab suit-tab-r_y_g',),
                        'fields': ['riesgo','grupo']
                }),        
                (None, {
                        'classes': ('suit-tab suit-tab-comentarios',),
                        'fields': ['comentario_es','comentario_en','referencia_otros_productos','referencia_grupos',]
                }),
                (None, {
                        'classes': ('suit-tab suit-tab-alternativas',),
                        'fields': ['no_alternativas', 'alternativas']
                }),
                (None, {
                        'classes': ('suit-tab suit-tab-farma',),
                        'fields': ['biodisponibilidad',
                                   'peso_molecular',
                                   'union_proteinas',
                                   'volumen_distrib',
                                   'pka',
                                   't_maximo',
                                   't_medio', 
                                   'indice_leche_plasma', 
                                   'dosis_teorica',
                                   'dosis_relativa',
                                   'dosis_terapeutica']
                }),
                (None, {
                        'classes': ('suit-tab suit-tab-biblio',),
                        'fields': ['tiene_biblio','csvfile','biblio']
                }),
                (None, {
                        'classes': ('suit-tab suit-tab-p_comentarios',),
                        'fields': (('fecha_creacion','fecha_modificacion'),'visitas',)
                }),
        ]

    suit_form_tabs = (('nombre', _(u'Nombre(s)')),
                          #('marcas', _(u'Marcas')),
                          ('r_y_g', _(u'Riesgo y Grupos')),
                          ('comentarios',_(u'Comentario')),
                          ('alternativas', _(u'Alternativas')),
                          ('farma', _(u'Farmac')),
                          ('biblio', _(u'Biblio')),
                          ('p_comentarios', _(u'Opiniones'))
                          )

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            if obj.dime_que_eres()==u'alias':
                if not obj.nombre_es:
                    obj.nombre_es=''
            obj.delete()
        for instance in instances:
            if instance.dime_que_eres()==u'alias':
                if not instance.nombre_es:
                    instance.nombre_es=''
                    #instance.nombre=instance.nombre_en
            instance.save()
        formset.save_m2m()
    
    
admin.site.register(Producto, ProductoAdmin)


class MensajeForm(ModelForm):
        class Meta:
                widgets = {
                        'contenido_es': AutosizedTextarea(attrs={'rows': 3, 'class': 'span-12'}),
                        'contenido_en': AutosizedTextarea(attrs={'rows': 3, 'class': 'span-12'}),
                        }
                exclude=('contenido','titulo',)


class MensajeAdmin(admin.ModelAdmin):
    list_display = ('nombre','nivel','tipo','producto', 'active_30', 'active_90','fecha_modificacion','traducido_al_ingles',)
    list_filter = ('fecha_modificacion', 'nivel', 'tipo',)
    ordering = ('nombre',)
    search_fields = ('nombre', 'nivel','tipo','producto__nombre',)
    readonly_fields = ('fecha_creacion','fecha_modificacion',)
    form = MensajeForm                

admin.site.register(Mensaje, MensajeAdmin)



class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('user','item_name','comentario','lang','leido','fecha_modificacion')
    list_filter = ('leido','fecha_modificacion', 'user__perfil', 'lang',)
    ordering = ('-fecha_modificacion',)
    search_fields = ('prod__nombre','alias__nombre','comentario', 'marca__nombre', 'grupo__nombre', 'mensaje__nombre')
    readonly_fields = ('user', 'comentario', 'prod','alias','marca','grupo','mensaje','lang', 'fecha_creacion','fecha_modificacion',)

    fieldsets = (
                (_(u'Comentario sobre:'), {
                        'fields': ('prod','alias', 'marca', 'grupo', 'mensaje',)
                }),
                (_(u'Del usuario:'), {
                        'fields': ('user', 'lang',)
                }),
                (_(u'Texto:'), {
                        'fields': ('comentario','leido', ('fecha_creacion','fecha_modificacion',),)
                }),
        )


admin.site.register(Comentario, ComentarioAdmin)


class Pais_Admin(admin.ModelAdmin):
    model = Pais
    list_display=( 'nombre_es', 'nombre_en',)
    search_fields=('nombre_es', 'nombre_en',)
    exclude = ('nombre',)
    ordering=('nombre_es',)

admin.site.register(Pais, Pais_Admin)

class Idioma_Admin(SortableModelAdmin):
    model = Idioma
    sortable = 'order'
    list_display=( 'nombre_es', 'nombre_en', 'productos',)
    search_fields=('nombre_es', 'nombre_en',)
    exclude = ('nombre',)
    ordering=('nombre_es',)

admin.site.register(Idioma, Idioma_Admin)

class AvalForm(ModelForm):
    class Meta:
        model = Aval
        
        widgets = {
                        'extracto_es': AutosizedTextarea(attrs={'rows': 8, 'class': 'span-12'}),
                        'extracto_en': AutosizedTextarea(attrs={'rows': 8, 'class': 'span-12'}),
        }
        
        exclude= ['extracto', 'carta']
        
        
class Aval_Admin(SortableModelAdmin):
    form = AvalForm
    sortable = 'order'
    list_display=( 'entidad', 'pais', 'visible',)
    search_fields=('entidad',)
    ordering=('entidad',)

    fieldsets = (
                ('', {
                        'fields': ('entidad','URL', 'logo', 'pais', 'visible', 'extracto_es', 'carta_es', 'extracto_en', 'carta_en')
                }),
        )
admin.site.register(Aval, Aval_Admin)



class PatrocinadorForm(ModelForm):
    class Meta:
        model = Aval
        
        widgets = {
                        'descripcion_es': AutosizedTextarea(attrs={'rows': 8, 'class': 'span-12'}),
                        'descripcion_en': AutosizedTextarea(attrs={'rows': 8, 'class': 'span-12'}),
        }
        
        exclude= ['descripcion',]
        
        
class Patrocinador_Admin(SortableModelAdmin):
    form = PatrocinadorForm
    sortable = 'order'
    list_display=( 'entidad', 'pais', 'visible',)
    search_fields=('entidad',)
    ordering=('entidad',)

    fieldsets = (
                ('', {
                        'fields': ('entidad','URL', 'logo', 'pais', 'visible', 'descripcion_es', 'descripcion_en')
                }),
        )
admin.site.register(Patrocinador, Patrocinador_Admin)



class Icono_Admin(admin.ModelAdmin):
    model = Icono
    list_display=( 'nombre', 'fontawesome_nombre', 'vista_previa')
    search_fields=('nombre','fontawesome_nombre')
    ordering=('nombre',)
 
admin.site.register(Icono, Icono_Admin)


class CajitaForm(ModelForm):
    class Meta:
        
        
        widgets = {
                        'texto_es': AutosizedTextarea(attrs={'rows': 12, 'class': 'span-12'}),
                        'texto_en': AutosizedTextarea(attrs={'rows': 12, 'class': 'span-12'}),
        }
        exclude= ('titulo', 'texto', 'link', 'texto_link', 'order',)

class Cajita_Admin(SortableModelAdmin):
    form = CajitaForm
    sortable = 'order'
    list_display=( 'titulo', 'vista_previa_icono', 'visible','publicidad')
    search_fields=('titulo_en','titulo_es')
    ordering=('order',)

    fieldsets = (
                ('' , {
                        'fields': ('titulo_es','titulo_en', 'icono', 'texto_es', 'texto_en','link_es','texto_link_es','link_en','texto_link_en','publicidad', 'visible',)
                }),
        )
admin.site.register(Cajita, Cajita_Admin)


class DocsForm(ModelForm):
    class Meta:
        
        
        widgets = {
                        'content_es': AutosizedTextarea(attrs={'rows': 12, 'class': 'span-12'}),
                        'content_en': AutosizedTextarea(attrs={'rows': 12, 'class': 'span-12'}),
        }
        exclude= ('title', 'content',)

class Docs_Admin(admin.ModelAdmin):
    form = DocsForm
    list_display=('title', 'order', 'type','visible',)
    list_filter = ('type', )
    search_fields=('titulo_en','titulo_es',)
    ordering=('type','order',)

    fieldsets = (
                ('' , {
                        'fields': ('type', 'order','visible', 'title_es','title_en', 'content_es', 'content_en',)
                }),
        )
admin.site.register(Docs, Docs_Admin)



class Visita_grupo_total_Admin(admin.ModelAdmin):
    model = Visita_grupo_total
    ordering=('-visitas',)
    list_select_related = True
    list_display=('grupo', 'visitas', 'fecha_modificacion','ultima_modificacion_termino',)
    readonly_fields=('grupo', 'visitas', 'fecha_modificacion',)
    search_fields = ( 'grupo__nombre_es', 'grupo__nombre_en',)
    
    def ultima_modificacion_termino(self, obj):
        return obj.grupo.fecha_modificacion
    ultima_modificacion_termino.allow_tags = True
    ultima_modificacion_termino.short_description = _(u'Última edición grupo')


admin.site.register(Visita_grupo_total, Visita_grupo_total_Admin)


class Visita_producto_total_Admin(admin.ModelAdmin):
    model = Visita_producto_total
    ordering=('-visitas',)
    list_filter = ('producto__nombre','producto__grupo',)
    list_select_related = True
    list_display=('producto', 'visitas', 'fecha_modificacion','ultima_modificacion_termino',)
    readonly_fields=('producto', 'visitas', 'fecha_modificacion',)
    search_fields = ( 'producto__nombre_es', 'producto__nombre_en',)
    
    def ultima_modificacion_termino(self, obj):
        return obj.producto.fecha_modificacion
    ultima_modificacion_termino.allow_tags = True
    ultima_modificacion_termino.short_description = _(u'Última edición producto')


admin.site.register(Visita_producto_total, Visita_producto_total_Admin)

class Visita_alias_total_Admin(admin.ModelAdmin):
    model = Visita_alias_total
    ordering=('-visitas',)
    list_select_related = True
    list_filter = ('alias__producto_principal',)
    list_display=('alias', 'visitas', 'fecha_modificacion','ultima_modificacion_alias','ultima_modificacion_producto')
    readonly_fields=('alias', 'visitas', 'fecha_modificacion',)
    search_fields = ( 'alias__nombre_es', 'alias__nombre_en',)
    
    def ultima_modificacion_alias(self, obj):
        return obj.alias.fecha_modificacion
    ultima_modificacion_alias.allow_tags = True
    ultima_modificacion_alias.short_description = _(u'Última edición sinónimo')
    
    def ultima_modificacion_producto(self, obj):
        return obj.alias.producto_principal.fecha_modificacion
    ultima_modificacion_producto.allow_tags = True
    ultima_modificacion_producto.short_description = _(u'Última edición producto')

admin.site.register(Visita_alias_total, Visita_alias_total_Admin)

class Visita_marca_total_Admin(admin.ModelAdmin):
    model = Visita_marca_total
    ordering=('-visitas',)
    list_filter = ('marca__principios_activos',)
    list_select_related = True
    list_display=('marca', 'visitas', 'fecha_modificacion','ultima_modificacion_termino',)
    readonly_fields=('marca', 'visitas', 'fecha_modificacion',)
    search_fields = ( 'marca__nombre',)
    
    def ultima_modificacion_termino(self, obj):
        return obj.marca.fecha_modificacion
    ultima_modificacion_termino.allow_tags = True
    ultima_modificacion_termino.short_description = _(u'Última edición marca')


admin.site.register(Visita_marca_total, Visita_marca_total_Admin)


class Visita_otras_escrituras_total_Admin(admin.ModelAdmin):
    model = Visita_otras_escrituras_total
    ordering=('-visitas',)
    list_select_related = True
    list_filter = ('otras_escrituras__producto_principal',)
    list_display=('otras_escrituras', 'visitas', 'fecha_modificacion','ultima_modificacion_termino','ultima_modificacion_producto',)
    readonly_fields=('otras_escrituras', 'visitas', 'fecha_modificacion',)
    search_fields = ( 'otras_escrituras__nombre',)
    
    def ultima_modificacion_termino(self, obj):
        return obj.otras_escrituras.fecha_modificacion
    ultima_modificacion_termino.allow_tags = True
    ultima_modificacion_termino.short_description = _(u'Última edición otra escritura')

    def ultima_modificacion_producto(self, obj):
        return obj.otras_escrituras.producto_principal.fecha_modificacion
    ultima_modificacion_producto.allow_tags = True
    ultima_modificacion_producto.short_description = _(u'Última edición producto')

admin.site.register(Visita_otras_escrituras_total, Visita_otras_escrituras_total_Admin)

class Visita_grupo_perfil_Admin(admin.ModelAdmin):
    model = Visita_grupo_perfil
    ordering=('-visitas',)
    list_select_related = True
    list_display=('grupo', 'perfil','visitas', 'fecha_modificacion','ultima_modificacion_termino',)
    readonly_fields=('grupo', 'perfil','visitas', 'fecha_modificacion',)
    search_fields = ( 'grupo__nombre_es', 'grupo__nombre_en',)
    list_filter = ('perfil',)
    def ultima_modificacion_termino(self, obj):
        return obj.grupo.fecha_modificacion
    ultima_modificacion_termino.allow_tags = True
    ultima_modificacion_termino.short_description = _(u'Última edición grupo')


admin.site.register(Visita_grupo_perfil, Visita_grupo_perfil_Admin)


class Visita_producto_perfil_Admin(admin.ModelAdmin):
    model = Visita_producto_perfil
    ordering=('-visitas',)
    list_select_related = True
    list_display=('producto', 'perfil','visitas', 'fecha_modificacion','ultima_modificacion_termino',)
    readonly_fields=('producto', 'perfil','visitas', 'fecha_modificacion',)
    search_fields = ( 'producto__nombre_es', 'producto__nombre_en',)
    list_filter = ('producto__nombre','producto__grupo','perfil',)
    def ultima_modificacion_termino(self, obj):
        return obj.producto.fecha_modificacion
    ultima_modificacion_termino.allow_tags = True
    ultima_modificacion_termino.short_description = _(u'Última edición producto')


admin.site.register(Visita_producto_perfil, Visita_producto_perfil_Admin)


class Visita_alias_perfil_Admin(admin.ModelAdmin):
    model = Visita_alias_perfil
    ordering=('-visitas',)
    list_select_related = True
    list_display=('alias', 'perfil','visitas', 'fecha_modificacion','ultima_modificacion_termino',)
    readonly_fields=('alias', 'perfil','visitas', 'fecha_modificacion',)
    search_fields = ( 'alias__nombre_es', 'alias__nombre_en',)
    list_filter = ('alias__producto_principal','perfil',)
    def ultima_modificacion_termino(self, obj):
        return obj.alias.fecha_modificacion
    ultima_modificacion_termino.allow_tags = True
    ultima_modificacion_termino.short_description = _(u'Última edición sinónimo')


admin.site.register(Visita_alias_perfil, Visita_alias_perfil_Admin)


class Visita_marca_perfil_Admin(admin.ModelAdmin):
    model = Visita_marca_perfil
    ordering=('-visitas',)
    list_select_related = True
    list_display=('marca', 'perfil','visitas', 'fecha_modificacion','ultima_modificacion_termino',)
    readonly_fields=('marca', 'perfil','visitas', 'fecha_modificacion',)
    search_fields = ( 'alias__nombre',)
    list_filter = ('marca__principios_activos','perfil',)
    def ultima_modificacion_termino(self, obj):
        return obj.marca.fecha_modificacion
    ultima_modificacion_termino.allow_tags = True
    ultima_modificacion_termino.short_description = _(u'Última edición marca')


admin.site.register(Visita_marca_perfil, Visita_marca_perfil_Admin)


class Visita_otras_escrituras_perfil_Admin(admin.ModelAdmin):
    model = Visita_otras_escrituras_perfil
    ordering=('-visitas',)
    list_select_related = True
    list_display=('otras_escrituras', 'perfil','visitas', 'fecha_modificacion','ultima_modificacion_termino',)
    readonly_fields=('otras_escrituras', 'perfil','visitas', 'fecha_modificacion',)
    search_fields = ( 'otras_escrituras__nombre',)
    list_filter = ('otras_escrituras__producto_principal','perfil',)
    def ultima_modificacion_termino(self, obj):
        return obj.otras_escrituras.fecha_modificacion
    ultima_modificacion_termino.allow_tags = True
    ultima_modificacion_termino.short_description = _(u'Última edición otra escritura')


admin.site.register(Visita_otras_escrituras_perfil, Visita_otras_escrituras_perfil_Admin)


'''
##class UserVisitsInline(admin.TabularInline):
##        model = Visita
##        suit_classes = 'suit-tab suit-tab-u_visitas'
##
##class UserComentariosInline(admin.TabularInline):
##        model = Comentario
##        suit_classes = 'suit-tab suit-tab-u_comentarios'
##
##
##                
##class LactUserAdmin(admin.ModelAdmin):
##        list_display = ('user', 'perfil','country_name','num_visitas', 'num_comentarios','ultima_visita')
##        search_fields = ('perfil','country_name',)
##        readonly_fields = ('session', 'user', 'ip_address', 'email', 'perfil', 'profile', 'city', 'longitude', 'latitude', 'country_name', 'country_code', 'country_code3', 'fecha_creacion')
##        ordering = ('user',)
##        inlines = [UserVisitsInline, UserComentariosInline,]
##        
##        fieldsets = [
##                (None, {
##                        'classes': ('suit-tab suit-tab-u_nombre',),
##                        'fields': ['user','perfil', 'email', 'ip_address', 'fecha_creacion']
##                }),
##                (None, {
##                        'classes': ('suit-tab suit-tab-u_geo',),
##                        'fields': (('longitude','latitude'), ('city', 'country_name'))
##                }),
##                (None, {
##                        'classes': ('suit-tab suit-tab-u_comentarios',),
##                        'fields': ()
##                }),
##                (None, {
##                        'classes': ('suit-tab suit-tab-u_visitas',),
##                        'fields': ()
##                }),
##        ]
##        
##        suit_form_tabs = (('u_nombre', 'Datos'),
##                          ('u_geo', u'Geografía'),
##                          ('u_visitas', 'Visitas'),
##                          ('u_comentarios','Comentarios'),
##                          )
                




#admin.site.register(LactUser, LactUserAdmin)
'''