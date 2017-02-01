# -*- coding: utf-8 -*-
from django.forms import Form, ChoiceField, CharField, Textarea, TextInput, Select, RadioSelect, EmailField, ValidationError
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _

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

class PerfilForm(Form):
    perfil = ChoiceField(widget=RadioSelect, choices=PROFILE_CHOICES)
    #perfil = ChoiceField(widget=Select(attrs={'onchange': 'this.form.submit();'}), choices=PROFILE_CHOICES, )
    #perfil = ChoiceField(widget=RadioSelect(attrs={'onchange': 'this.form.submit();'}), choices=PROFILE_CHOICES, )

class ComentarioForm(Form):
    comentario = CharField(widget=Textarea(attrs={'class': 'span12', 'rows': 4, 'id':"opinion", 'maxlength':250,  'placeholder': _(u"Espacio para opinión o sugerencia. Para consultas: elactancia.org@gmail.com")}))
    email = EmailField(required=False)
    
    def clean_comentario(self):
        comentario = self.cleaned_data['comentario']
        num_words = len(comentario.split())
        if num_words < 1:
            raise ValidationError(_(u"No hay suficiente texto"))
        return comentario


class Subscription(Form):
    nombre = CharField(widget=TextInput(attrs={'id':"newsletter_nombre", 'maxlength':255,  'placeholder': _(u"Nombre")}),required=True)
    email = EmailField(widget=TextInput(attrs={'id':"newsletter_email", 'maxlength':255, 'placeholder': _(u"Correo electrónico")}),required=True)


my_default_errors = {
    'required': _(u'Este campo es obligatorio'),
    'max_length':_(u'El texto es demasiado largo'),
    'invalid': _(u'Introduzca una dirección de correo válida')
}

