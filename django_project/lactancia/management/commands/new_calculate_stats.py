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
    help = 'Calculates visits stats of e-lactancia and saves them in text files'

    
    def handle(self, *args, **options):

        
        PROJECT_PATH = '/home/django'
        
        def dictfetchall(cursor):
            'Returns all rows from a cursor as a dict'
            desc = cursor.description
            return [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        
        cursor = connection.cursor()
        
        #biblio_all = Bibliografia.objects.all().order_by('-anyo')
        visits_all = Visita.objects.all().order_by('-time')
    
        prods_all = Producto.objects.all().order_by('nombre')
        grupos_all = Grupo.objects.all().order_by('nombre')
        marcas_all = Marca.objects.all().order_by('nombre')
        alias_all = Alias.objects.all().order_by('nombre')
        escrit_all = Otras_escrituras.objects.all().order_by('nombre')
        
        '''N_prods = prods_all.count()
        N_grupos = grupos_all.count()
        N_alias = alias_all.count()
        N_marcas = marcas_all.count()
        N_total = N_prods + N_grupos + N_alias + N_marcas

        kk = [ {"nombre": 'Productos', 'nombre_ingles': 'Products', 'N': N_prods}, \
               {"nombre": 'Alias', 'nombre_ingles': 'Alias', 'N': N_alias}, \
               {"nombre": 'Grupos', 'nombre_ingles': 'Groups', 'N': N_grupos}, \
               {"nombre": 'Marcas', 'nombre_ingles': 'Tradenames', 'N': N_marcas}, \
               {"nombre": 'Total', 'nombre_ingles': 'Total', 'N': N_total}]
        fd = open(PROJECT_PATH+"/media/stats_terms.json","w")
        fd.write(json.dumps(kk, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()'''

        '''Times we are showing'''
        '''last day, week, month, year and all'''
        now = timezone.now()

        day = now - datetime.timedelta(days=1)
        week = now - datetime.timedelta(days=7)
        month = now - datetime.timedelta(days=30)
        year = now - datetime.timedelta(days=365)

        """
        '''STATS FOR 2015'''
        INIT_2015 = timezone.localtime(timezone.now()).replace(year=2015, month=1, day=01,hour=0, minute=0, second=0, microsecond=0)
        END_2015 = timezone.localtime(timezone.now()).replace(year=2016, month=1, day=01,hour=0, minute=0, second=0, microsecond=0)
    
        # ranking consultations 2015
        aux = visits_all.filter(time__range=[INIT_2015,END_2015]).values('prod__nombre_es', 'prod__nombre_en').annotate(n_consultations=Count('prod__id'))
        top_prods_2015 = aux.order_by('-n_consultations')[:150]
        data = list(top_prods_2015)
        fd = open(PROJECT_PATH +"/media/stats_prods_top_2015.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # visits by profile 2015
        #Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time between '2015-01-01' and '2016-01-01' group by profile;''')
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_profile_2015.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # visits by country 2015 
        # Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.country_name as country from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time between '2015-01-01' and '2016-01-01' group by country;''')
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_country_2015.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        """
        
        '''Stats on terms updated'''
        '''We get the list of terms updated the last day, week, month, year and all'''
        
        prods_updated_1d = prods_all.filter(fecha_modificacion__range=[day, now]).values('nombre_es', 'nombre_en','id')
        prods_updated_1w = prods_all.filter(fecha_modificacion__range=[week, now]).values('nombre_es', 'nombre_en','id')
        prods_updated_1m = prods_all.filter(fecha_modificacion__range=[month, now]).values('nombre_es', 'nombre_en','id')
        prods_updated_1y = prods_all.filter(fecha_modificacion__range=[year, now]).values('nombre_es', 'nombre_en','id')

        data=list(prods_updated_1d)
        fd = open(PROJECT_PATH +"/media/stats_prods_updated_1d.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()
        
        data=list(prods_updated_1w)
        fd = open(PROJECT_PATH +"/media/stats_prods_updated_1w.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()

        data=list(prods_updated_1m)
        fd = open(PROJECT_PATH +"/media/stats_prods_updated_1m.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()
        
        data=list(prods_updated_1y)
        fd = open(PROJECT_PATH +"/media/stats_prods_updated_1y.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()
        
        

        
        '''Stats on consultations from users'''
        '''We get the list of consultations the last day, week and month'''
        
        aux = visits_all.values('prod__nombre_es', 'prod__nombre_en').annotate(n_consultations=Count('prod__id'))
        top_prods_all = aux.order_by('-n_consultations')[:150]
        data = list(top_prods_all)
        fd = open(PROJECT_PATH +"/media/stats_prods_top_all.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()

        aux = visits_all.filter(time__range=[day,now]).values('prod__nombre_es', 'prod__nombre_en').annotate(n_consultations=Count('prod__id'))
        top_prods_1d = aux.order_by('-n_consultations')[:150]
        data = list(top_prods_1d)
        fd = open(PROJECT_PATH +"/media/stats_prods_top_1d.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()

        aux = visits_all.filter(time__range=[week,now]).values('prod__nombre_es', 'prod__nombre_en').annotate(n_consultations=Count('prod__id'))
        top_prods_1w = aux.order_by('-n_consultations')[:150]
        data = list(top_prods_1w)
        fd = open(PROJECT_PATH +"/media/stats_prods_top_1w.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()

        aux = visits_all.filter(time__range=[month,now]).values('prod__nombre_es', 'prod__nombre_en').annotate(n_consultations=Count('prod__id'))
        top_prods_1m = aux.order_by('-n_consultations')[:150]
        data = list(top_prods_1m)
        fd = open(PROJECT_PATH +"/media/stats_prods_top_1m.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()

        aux = visits_all.filter(time__range=[year,now]).values('prod__nombre_es', 'prod__nombre_en').annotate(n_consultations=Count('prod__id'))
        top_prods_1y = aux.order_by('-n_consultations')[:150]
        data = list(top_prods_1y)
        fd = open(PROJECT_PATH +"/media/stats_prods_top_1y.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        
        ''' Top consultations in Spain '''
        
        aux = visits_all.filter(user__country_name='Spain').values('prod__nombre_es', 'prod__nombre_en').annotate(n_consultations=Count('prod__id'))
        top_prods_all = aux.order_by('-n_consultations')[:150]
        data = list(top_prods_all)
        fd = open(PROJECT_PATH +"/media/stats_prods_top_all_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()

        aux = visits_all.filter(user__country_name='Spain', time__range=[day,now]).values('prod__nombre_es', 'prod__nombre_en').annotate(n_consultations=Count('prod__id'))
        top_prods_1d = aux.order_by('-n_consultations')[:150]
        data = list(top_prods_1d)
        fd = open(PROJECT_PATH +"/media/stats_prods_top_1d_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()

        aux = visits_all.filter(user__country_name='Spain', time__range=[week,now]).values('prod__nombre_es', 'prod__nombre_en').annotate(n_consultations=Count('prod__id'))
        top_prods_1w = aux.order_by('-n_consultations')[:150]
        data = list(top_prods_1w)
        fd = open(PROJECT_PATH +"/media/stats_prods_top_1w_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()

        aux = visits_all.filter(user__country_name='Spain', time__range=[month,now]).values('prod__nombre_es', 'prod__nombre_en').annotate(n_consultations=Count('prod__id'))
        top_prods_1m = aux.order_by('-n_consultations')[:150]
        data = list(top_prods_1m)
        fd = open(PROJECT_PATH +"/media/stats_prods_top_1m_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        aux = visits_all.filter(user__country_name='Spain', time__range=[year,now]).values('prod__nombre_es', 'prod__nombre_en').annotate(n_consultations=Count('prod__id'))
        top_prods_1y = aux.order_by('-n_consultations')[:150]
        data = list(top_prods_1y)
        fd = open(PROJECT_PATH +"/media/stats_prods_top_1y_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        
        
        '''STATISTICS FROM COUNTRIES'''
        '''See http://stackoverflow.com/questions/12733644/ms-sql-query-to-calculate-average-monthly-unique-visitors
        theanswer = use a custom SQL (which is really fast) to get at the same time consultations and unique visits:'''
        '''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits,
        lactancia_lactuser.country_name as country from lactancia_lactuser, lactancia_visita 
        where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time > date_sub(curdate(),interval 1 day) group by country;'''
        
        
        
        # last day
        
        # MYSQL
        #cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.country_name as country from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time > date_sub(curdate(),interval 1 day) group by country;''')
        
        # Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.country_name as country from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time > CURRENT_TIMESTAMP - interval  '1 days' group by country;''')
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_country_1d.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # last week
        # MYSQL
        #cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.country_name as country from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time > date_sub(curdate(),interval 1 week) group by country;''')
        #Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.country_name as country from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time > CURRENT_TIMESTAMP - interval  '1 weeks' group by country;''')
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_country_1w.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # last month
        #mysql
        #cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.country_name as country from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time > date_sub(curdate(),interval 1 month) group by country;''')
        #Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.country_name as country from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time > CURRENT_TIMESTAMP - interval  '1 months' group by country;''')
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_country_1m.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # last year
        # MYSQL
        #cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.country_name as country from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time > date_sub(curdate(),interval 1 year) group by country;''')
        #Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.country_name as country from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time > CURRENT_TIMESTAMP - interval  '1 year' group by country;''')
        
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_country_1y.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # TOTAL
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.country_name as country from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id group by country;''')
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_country_all.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        
        # '''Visits in Spain by cities'''
        # last day
        # MYSQL
        #cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.city as city from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' and lactancia_visita.time > date_sub(curdate(),interval 1 day) group by city order by visits desc, consultations desc;''')
        #Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.city as city from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' and lactancia_visita.time > CURRENT_TIMESTAMP - interval  '1 days' group by city order by visits desc, consultations desc;''')
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_cities_1d_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # last week
        # MYSQL
        #cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.city as city from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' and lactancia_visita.time > date_sub(curdate(),interval 1 week) group by city order by visits desc, consultations desc;''')
        #Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.city as city from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' and lactancia_visita.time > CURRENT_TIMESTAMP - interval  '1 weeks'  group by city order by visits desc, consultations desc;''')
        
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_cities_1w_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # last month
        # MYSQL
        #cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.city as city from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' and lactancia_visita.time > date_sub(curdate(),interval 1 month) group by city order by visits desc, consultations desc;''')
        #Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.city as city from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' and lactancia_visita.time > CURRENT_TIMESTAMP - interval  '1 months' group by city order by visits desc, consultations desc;''')
        
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_cities_1m_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # last year
        # MYSQL
        #cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.city as city from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' and lactancia_visita.time > date_sub(curdate(),interval 1 year) group by city order by visits desc, consultations desc;''')
        #Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.city as city from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' and lactancia_visita.time > CURRENT_TIMESTAMP - interval  '1 year' group by city order by visits desc, consultations desc;''')
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_cities_1y_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # # # TOTAL
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.city as city from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' group by city order by visits desc, consultations desc;''')
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_cities_all_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        
        
        
        # '''Visits by profile'''
        # last day
        # MYSQL
        #cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time > date_sub(curdate(),interval 1 day) group by profile;''')
        #Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time > CURRENT_TIMESTAMP - interval  '1 days' group by profile;''')
        
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_profile_1d.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # last week
        # MYSQL
        #cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time > date_sub(curdate(),interval 1 week) group by profile;''')
        #Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time > CURRENT_TIMESTAMP - interval  '1 weeks' group by profile;''')
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_profile_1w.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # last month
        # MYSQL
        #cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time > date_sub(curdate(),interval 1 month) group by profile;''')
        #Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time > CURRENT_TIMESTAMP - interval  '1 months' group by profile;''')
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_profile_1m.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # last year
        # MYSQL
        #cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time > date_sub(curdate(),interval 1 year) group by profile;''')
        #Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_visita.time > CURRENT_TIMESTAMP - interval  '1 years' group by profile;''')
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_profile_1y.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # TOTAL
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id group by profile;''')
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_profile_all.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        
        # '''Visits profile in Spain'''
        # last day
        # MYSQL
        #cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' and lactancia_visita.time > date_sub(curdate(),interval 1 day) group by profile;''')
        # Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' and lactancia_visita.time > CURRENT_TIMESTAMP - interval  '1 days' group by profile;''')
        
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_profile_1d_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # last week
        # MYSQL
        #cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' and lactancia_visita.time > date_sub(curdate(),interval 1 week) group by profile;''')
        #Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' and lactancia_visita.time > CURRENT_TIMESTAMP - interval  '1 weeks'  group by profile;''')
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_profile_1w_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # last month
        # MYSQL
        #cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' and lactancia_visita.time > date_sub(curdate(),interval 1 month) group by profile;''')
        #Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' and lactancia_visita.time > CURRENT_TIMESTAMP - interval  '1 months' group by profile;''')
        
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_profile_1m_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # last year
        # MYSQL
        #cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' and lactancia_visita.time > date_sub(curdate(),interval 1 year) group by profile;''')
        #Posgresql
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' and lactancia_visita.time > CURRENT_TIMESTAMP - interval  '1 year' group by profile;''')
        
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_profile_1y_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        # # TOTAL
        cursor.execute('''select count(lactancia_lactuser.ip_address) as consultations, count(distinct lactancia_lactuser.ip_address) as visits, lactancia_lactuser.perfil as profile from lactancia_lactuser, lactancia_visita where lactancia_visita.user_id=lactancia_lactuser.session_id and lactancia_lactuser.country_code='ES' group by profile;''')
        data = dictfetchall(cursor)
        fd = open(PROJECT_PATH +"/media/stats_profile_all_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, indent=4).encode('utf8'))
        fd.close()
        
        
        
        
        
        
        


        '''Visits and consultations per different period of time'''  


        '''Consultations'''
        
        # "yearly consultations"
        
        truncate_date = connection.ops.date_trunc_sql('year','time')
        visitas = Visita.objects.extra({'year':truncate_date}).values('year').annotate(n_visits=Count('user'))
        data = list(visitas)
        fd = open(PROJECT_PATH +"/media/stats_consultations_years.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()
        
        # "monthly consultations"
        truncate_date = connection.ops.date_trunc_sql('month','time')
        visitas = Visita.objects.extra({'mes':truncate_date}).values('mes').annotate(n_visits=Count('user'))
        data = list(visitas)
        fd = open(PROJECT_PATH +"/media/stats_consultations_months.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()
        
        # "weekly consultations"
        #truncate_date = connection.ops.date_trunc_sql('week','time')
        #visitas = Visita.objects.extra({'semana':'week(time)+1','year':'year(time)'}).values('semana','year').annotate(n_visits=Count('user'))
        visitas = Visita.objects.extra({'semana':'EXTRACT(week FROM time)','year':'EXTRACT(year FROM time)'}).values('semana','year').annotate(n_visits=Count('user'))
        data = list(visitas)
        fd = open(PROJECT_PATH +"/media/stats_consultations_weeks.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()
        # "daily consultations"
        truncate_date = connection.ops.date_trunc_sql('day','time')
        visitas = Visita.objects.extra({'dia':'date(time)'}).values('dia').annotate(n_visits=Count('user'))
        data = list(visitas)
        fd = open(PROJECT_PATH +"/media/stats_consultations_days.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()

        
        '''SPAIN Consultations'''
        
        # "ES yearly consultations"
        truncate_date = connection.ops.date_trunc_sql('year','time')
        visitas = Visita.objects.filter(user__country_name='Spain').extra({'year':truncate_date}).values('year').annotate(n_visits=Count('user')).order_by('year')
        data = list(visitas)
        fd = open(PROJECT_PATH +"/media/stats_consultations_years_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()
        
        # "ES monthly consultations"
        truncate_date = connection.ops.date_trunc_sql('month','time')
        visitas = Visita.objects.filter(user__country_name='Spain').extra({'mes':truncate_date}).values('mes').annotate(n_visits=Count('user')).order_by('mes')
        data = list(visitas)
        fd = open(PROJECT_PATH +"/media/stats_consultations_months_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()

        # "ES weekly consultations"
        #truncate_date = connection.ops.date_trunc_sql('week','time')
        #visitas = Visita.objects.filter(user__country_name='Spain').extra({'semana':'week(time)+1','year':'year(time)'}).values('semana','year').annotate(n_visits=Count('user')).order_by('semana')
        visitas = Visita.objects.filter(user__country_name='Spain').extra({'semana':'EXTRACT(week FROM time)','year':'EXTRACT(year FROM time)'}).values('semana','year').annotate(n_visits=Count('user'))
        data = list(visitas)
        fd = open(PROJECT_PATH +"/media/stats_consultations_weeks_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()

        # "ES daily consultations"
        truncate_date = connection.ops.date_trunc_sql('day','time')
        visitas = Visita.objects.filter(user__country_name='Spain').extra({'dia':'date(time)'}).values('dia').annotate(n_visits=Count('user')).order_by('dia')
        data = list(visitas)
        fd = open(PROJECT_PATH +"/media/stats_consultations_days_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()
        

        # ''visits per time period''

        # "yearly visits"
        truncate_date = connection.ops.date_trunc_sql('year','time')
        visitas = Visita.objects.extra({'year':truncate_date}).values('year').annotate(n_visits=Count('user', distinct=True))
        data = list(visitas)
        fd = open(PROJECT_PATH +"/media/stats_visits_years.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()
                
        # "monthly visits"
        truncate_date = connection.ops.date_trunc_sql('month','time')
        visitas = Visita.objects.extra({'mes':truncate_date}).values('mes').annotate(n_visits=Count('user', disctinct=True))
        data = list(visitas)
        fd = open(PROJECT_PATH +"/media/stats_visits_months.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()

        #"weekly visits"
        #truncate_date = connection.ops.date_trunc_sql('week','time')
        #visitas = Visita.objects.extra({'semana':'week(time)+1','year':'year(time)'}).values('semana','year').annotate(n_visits=Count('user', distinct=True))
        visitas = Visita.objects.extra({'semana':'EXTRACT(week FROM time)','year':'EXTRACT(year FROM time)'}).values('semana','year').annotate(n_visits=Count('user', disctinct=True))
        data = list(visitas)
        fd = open(PROJECT_PATH +"/media/stats_visits_weeks.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()

        # "daily visits"
        truncate_date = connection.ops.date_trunc_sql('day','time')
        visitas = Visita.objects.extra({'dia':'date(time)'}).values('dia').annotate(n_visits=Count('user', distinct=True))
        data = list(visitas)
        fd = open(PROJECT_PATH +"/media/stats_visits_days.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()
        

        # ''SPAIN visits per time period''

        # "ES yearly visits"
        truncate_date = connection.ops.date_trunc_sql('year','time')
        visitas = Visita.objects.filter(user__country_name='Spain').extra({'year':truncate_date}).values('year').annotate(n_visits=Count('user', distinct=True)).order_by('year')
        data = list(visitas)
        fd = open(PROJECT_PATH +"/media/stats_visits_years_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()
                
        # "monthly visits"
        truncate_date = connection.ops.date_trunc_sql('month','time')
        visitas = Visita.objects.filter(user__country_name='Spain').extra({'mes':truncate_date}).values('mes').annotate(n_visits=Count('user', disctinct=True)).order_by('mes')
        data = list(visitas)
        fd = open(PROJECT_PATH +"/media/stats_visits_months_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()

        # "weekly visits"
        truncate_date = connection.ops.date_trunc_sql('week','time')
        #visitas = Visita.objects.filter(user__country_name='Spain').extra({'semana':'week(time)+1','year':'year(time)'}).values('semana','year').annotate(n_visits=Count('user', distinct=True)).order_by('semana')
        visitas = Visita.objects.filter(user__country_name='Spain').extra({'semana':'EXTRACT(week FROM time)','year':'EXTRACT(year FROM time)'}).values('semana','year').annotate(n_visits=Count('user', disctinct=True))
        data = list(visitas)
        fd = open(PROJECT_PATH +"/media/stats_visits_weeks_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()

        # "daily visits"
        truncate_date = connection.ops.date_trunc_sql('day','time')
        visitas = Visita.objects.filter(user__country_name='Spain').extra({'dia':'date(time)'}).values('dia').annotate(n_visits=Count('user', distinct=True)).order_by('dia')
        data = list(visitas)
        fd = open(PROJECT_PATH +"/media/stats_visits_days_ES.json","w")
        fd.write(json.dumps(data, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4).encode('utf8'))
        fd.close()
        
        
        self.stdout.write('Successfully written stats at ' + now.strftime("%Y-%m-%d %H:%M:%S"))
