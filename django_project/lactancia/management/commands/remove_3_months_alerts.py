# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from lactancia.models import Mensaje
from django.utils import timezone
import datetime
from django.db import connection

class Command(BaseCommand):
    args = 'None'
    help = 'Removes the warning messages for risk level in a product older than 3 months.'


    def handle(self, *args, **options):

        mensajes = Mensaje.objects.filter(tipo='cambio_riesgo')

        for m in mensajes:
            if m.fecha_modificacion < timezone.now() - datetime.timedelta(days=90):
                #print 'deleting...'
                #print m
                m.delete()
