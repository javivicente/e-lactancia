# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from lactancia.models import Riesgo, Producto, Alias, Marca, Otras_escrituras, Grupo, Mensaje, LactUser, Visita, Comentario, Bibliografia
from django.db.models import Count, Avg, Max, Q
from django.utils import timezone
import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
        
class Command(BaseCommand):
    args = 'None'
    help = 'Calculates visits per term of e-lactancia and saves them in text files'

    
    def handle(self, *args, **options):

        
        PROJECT_PATH = '/home/django'
        
        
        grupos_all = Grupo.objects.all().order_by('id')
        kk =[]
        for p in grupos_all:
            visits=[0]*15
            aux = Visita.objects.filter(grupo=p.pk)
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
            kk.append({'id': p.id, 'visits': visits})
        fd = open(PROJECT_PATH+"/media/visitas_grupos.json","w")
        fd.write(json.dumps(kk, ensure_ascii=False).encode('utf8'))
        fd.close()
        
        
        
        prods_all = Producto.objects.all().order_by('id')
        kk =[]
        for p in prods_all:
            visits=[0]*15
            aux = Visita.objects.filter(prod=p.pk)
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
            kk.append({'id': p.id, 'visits': visits})
        fd = open(PROJECT_PATH+"/media/visitas_productos.json","w")
        fd.write(json.dumps(kk, ensure_ascii=False).encode('utf8'))
        fd.close()
        
        
        
        
        escrituras_all = Otras_escrituras.objects.all().order_by('id')
        kk =[]
        for p in escrituras_all:
            visits=[0]*15
            aux = Visita.objects.filter(otra_escritura=p.pk)
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
            kk.append({'id': p.id, 'visits': visits})
        fd = open(PROJECT_PATH+"/media/visitas_escrituras.json","w")
        fd.write(json.dumps(kk, ensure_ascii=False).encode('utf8'))
        fd.close()
        
        alias_all = Alias.objects.all().order_by('id')
        kk =[]
        for p in alias_all:
            visits=[0]*15
            aux = Visita.objects.filter(alias=p.pk)
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
            kk.append({'id': p.id, 'visits': visits})
        fd = open(PROJECT_PATH+"/media/visitas_alias.json","w")
        fd.write(json.dumps(kk, ensure_ascii=False).encode('utf8'))
        fd.close()
        
        marcas_all = Marca.objects.all().order_by('id')
        kk =[]
        for p in marcas_all:
            visits=[0]*15
            aux = Visita.objects.filter(marca=p.pk)
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
            kk.append({'id': p.id, 'visits': visits})
        fd = open(PROJECT_PATH+"/media/visitas_marcas.json","w")
        fd.write(json.dumps(kk, ensure_ascii=False).encode('utf8'))
        fd.close()
        