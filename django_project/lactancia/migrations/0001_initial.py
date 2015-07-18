# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255, blank=True, help_text='Nombre en espa\xf1ol. Si tiene traducci\xf3n al ingl\xe9s, ponla en el campo del nombre en ingl\xe9s. Sino, deja el campo del nombre en ingl\xe9s vac\xedo.', null=True, verbose_name='Sin\xf3nimo del producto', db_index=True)),
                ('nombre_en', models.CharField(max_length=255, blank=True, help_text='Nombre en espa\xf1ol. Si tiene traducci\xf3n al ingl\xe9s, ponla en el campo del nombre en ingl\xe9s. Sino, deja el campo del nombre en ingl\xe9s vac\xedo.', null=True, verbose_name='Sin\xf3nimo del producto', db_index=True)),
                ('nombre_es', models.CharField(max_length=255, blank=True, help_text='Nombre en espa\xf1ol. Si tiene traducci\xf3n al ingl\xe9s, ponla en el campo del nombre en ingl\xe9s. Sino, deja el campo del nombre en ingl\xe9s vac\xedo.', null=True, verbose_name='Sin\xf3nimo del producto', db_index=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creaci\xf3n')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, verbose_name='\xdaltima modificaci\xf3n', db_index=True)),
            ],
            options={
                'verbose_name': 'Sin\xf3nimo de producto',
                'verbose_name_plural': 'Sin\xf3nimos de productos',
            },
        ),
        migrations.CreateModel(
            name='Bibliografia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=1000, verbose_name='T\xedtulo')),
                ('autores', models.CharField(max_length=1000, null=True, verbose_name='Autores', blank=True)),
                ('publicacion', models.CharField(max_length=1000, null=True, verbose_name='Revista', blank=True)),
                ('anyo', models.PositiveSmallIntegerField(null=True, verbose_name='A\xf1o', blank=True)),
                ('abstract_link', models.URLField(help_text='Enlace al abstract del art\xedculo', max_length=500, null=True, blank=True)),
                ('full_text_link', models.URLField(help_text='Enlace al texto completo del art\xedculo', max_length=500, null=True, blank=True)),
                ('pdf', models.FileField(help_text='Sube el pdf del art\xedculo \xfanicamente si no est\xe1 disponible en ning\xfan enlace externo. De lo contrario, usa los campos de enlaces al abstract o al texto completo.', upload_to=b'papers', verbose_name='Documento PDF', blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creaci\xf3n')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, verbose_name='\xdaltima modificaci\xf3n')),
            ],
            options={
                'verbose_name': 'Biblio',
                'verbose_name_plural': 'Biblio',
            },
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comentario', models.CharField(max_length=500, verbose_name='Opini\xf3n')),
                ('leido', models.BooleanField(default=False, verbose_name='Opini\xf3n ya le\xedda')),
                ('lang', models.CharField(max_length=7, verbose_name='Idioma')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creaci\xf3n')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, verbose_name='\xdaltima modificaci\xf3n')),
                ('alias', models.ForeignKey(related_name='comentario_alias', blank=True, to='lactancia.Alias', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=255, verbose_name='Nombre', db_index=True)),
                ('nombre_en', models.CharField(max_length=255, unique=True, null=True, verbose_name='Nombre', db_index=True)),
                ('nombre_es', models.CharField(max_length=255, unique=True, null=True, verbose_name='Nombre', db_index=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creaci\xf3n')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, verbose_name='\xdaltima modificaci\xf3n', db_index=True)),
                ('relacionados', models.ManyToManyField(related_name='relacionados_rel_+', verbose_name='grupos con los que se relaciona', to='lactancia.Grupo', blank=True)),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
            },
        ),
        migrations.CreateModel(
            name='Idioma',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, verbose_name='Idioma o escritura')),
                ('nombre_en', models.CharField(max_length=100, null=True, verbose_name='Idioma o escritura')),
                ('nombre_es', models.CharField(max_length=100, null=True, verbose_name='Idioma o escritura')),
                ('order', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Idioma o escritura',
                'verbose_name_plural': 'Idiomas o escrituras',
            },
        ),
        migrations.CreateModel(
            name='LactUser',
            fields=[
                ('session', models.OneToOneField(primary_key=True, serialize=False, to='sessions.Session')),
                ('ip_address', models.CharField(max_length=256, verbose_name='Direcci\xf3n IP')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='e-Mail', blank=True)),
                ('nombre', models.CharField(max_length=255, null=True, verbose_name='Nombre', blank=True)),
                ('perfil', models.CharField(max_length=2, verbose_name='Tipo de usuario (perfil)', choices=[(b'1', 'Pediatra'), (b'2', 'Ginec\xf3loga/o'), (b'14', 'M\xe9dico de familia'), (b'3', 'Otra especialidad m\xe9dica'), (b'4', 'Matrona'), (b'5', 'Enfermera/o'), (b'13', 'Farmac\xe9utico/a'), (b'6', 'Otro sanitario'), (b'7', 'Consultora lactancia (IBCLC, OMS)'), (b'8', 'Grupo de apoyo'), (b'9', 'Doula'), (b'10', 'Madre/Padre'), (b'11', 'Otro'), (b'12', 'An\xf3nimo')])),
                ('city', models.CharField(max_length=100, null=True, verbose_name='Ciudad', blank=True)),
                ('longitude', models.DecimalField(null=True, verbose_name='Longitud', max_digits=9, decimal_places=6, blank=True)),
                ('latitude', models.DecimalField(null=True, verbose_name='Latitud', max_digits=9, decimal_places=6, blank=True)),
                ('country_name', models.CharField(max_length=255, null=True, verbose_name='Pa\xeds', blank=True)),
                ('country_code', models.CharField(max_length=30, null=True, verbose_name='C\xf3digo pa\xeds', blank=True)),
                ('country_code3', models.CharField(max_length=30, null=True, verbose_name='C\xf3digo pa\xeds 3', blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creaci\xf3n', db_index=True)),
                ('user', models.ForeignKey(verbose_name='Nombre', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Visitante',
                'verbose_name_plural': 'Visitantes',
            },
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre comercial', db_index=True)),
                ('comentario', models.CharField(max_length=255, null=True, verbose_name='Pa\xeds donde se comercializa', blank=True)),
                ('comentario_en', models.CharField(max_length=255, null=True, verbose_name='Pa\xeds donde se comercializa', blank=True)),
                ('comentario_es', models.CharField(max_length=255, null=True, verbose_name='Pa\xeds donde se comercializa', blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creaci\xf3n')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, verbose_name='\xdaltima modificaci\xf3n', db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=255, verbose_name='Nombre')),
                ('nivel', models.CharField(default=b'info', max_length=7, verbose_name='Nivel del mensaje', choices=[(b'info', 'informaci\xf3n'), (b'success', '\xe9xito'), (b'warning', 'alerta'), (b'danger', 'peligro')])),
                ('tipo', models.CharField(max_length=15, verbose_name='Tipo de mensaje (nivel)', choices=[(b'cambio_riesgo', 'cambio en nivel del riesgo'), (b'farmacocinetica', 'mensaje en variable farmacocin\xe9tica'), (b'copyright', 'mensaje sobre copyrigh de marcas'), (b'diclaimer', 'mensaje sobre el uso de e-lactancia'), (b'comentario', 'comentario de usuarios')])),
                ('titulo', models.CharField(max_length=255, verbose_name='T\xedtulo mensaje', db_index=True)),
                ('titulo_en', models.CharField(max_length=255, null=True, verbose_name='T\xedtulo mensaje', db_index=True)),
                ('titulo_es', models.CharField(max_length=255, null=True, verbose_name='T\xedtulo mensaje', db_index=True)),
                ('contenido', models.CharField(db_index=True, max_length=5000, null=True, verbose_name='Cuerpo del mensaje', blank=True)),
                ('contenido_en', models.CharField(db_index=True, max_length=5000, null=True, verbose_name='Cuerpo del mensaje', blank=True)),
                ('contenido_es', models.CharField(db_index=True, max_length=5000, null=True, verbose_name='Cuerpo del mensaje', blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creaci\xf3n')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, verbose_name='\xdaltima modificaci\xf3n', db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Otras_escrituras',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(db_index=True, max_length=255, null=True, verbose_name='Producto en otras escrituras', blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creaci\xf3n')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, verbose_name='\xdaltima modificaci\xf3n', db_index=True)),
                ('escritura', models.ForeignKey(verbose_name='Idioma en que est\xe1 escrito el producto', blank=True, to='lactancia.Idioma', null=True)),
            ],
            options={
                'ordering': ['escritura__order', 'nombre'],
                'verbose_name': 'Otras escrituras del producto',
                'verbose_name_plural': 'Otras escrituras del producto',
            },
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('nombre_en', models.CharField(max_length=100, null=True, verbose_name='Nombre')),
                ('nombre_es', models.CharField(max_length=100, null=True, verbose_name='Nombre')),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name': 'Pa\xeds',
                'verbose_name_plural': 'Pa\xedses',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=255, verbose_name='Nombre', db_index=True)),
                ('nombre_en', models.CharField(max_length=255, unique=True, null=True, verbose_name='Nombre', db_index=True)),
                ('nombre_es', models.CharField(max_length=255, unique=True, null=True, verbose_name='Nombre', db_index=True)),
                ('comentario', models.CharField(max_length=10000, null=True, verbose_name='Comentario', blank=True)),
                ('comentario_en', models.CharField(max_length=10000, null=True, verbose_name='Comentario', blank=True)),
                ('comentario_es', models.CharField(max_length=10000, null=True, verbose_name='Comentario', blank=True)),
                ('no_alternativas', models.BooleanField(default=False, help_text='Marca esta casilla si no tiene sentido que el t\xe9rmino tenga altenativas. Por ejemplo, una enfermedad cong\xe9nita o adquirida.', verbose_name='No puede tener alternativas')),
                ('tiene_biblio', models.BooleanField(default=True, help_text='Indica si el producto poseera referencias bibliogr\xe1ficas. Si no las va a tener ni ahora ni en el futuro, debe desmarcarse esta casilla. Ejemplos de productos que pueden no tener bibliograf\xeda asociada son los de Fitoterapia', verbose_name='Tiene bibliografia (a\xf1adida o pendiente de a\xf1adir)')),
                ('csvfile', models.FileField(upload_to=b'papers/%Y/%m/', verbose_name='Importar biblio con fichero CSV', blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creaci\xf3n')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, verbose_name='\xdaltima modificaci\xf3n', db_index=True)),
                ('peso_molecular', models.CharField(max_length=30, null=True, verbose_name='Peso molecular', blank=True)),
                ('union_proteinas', models.CharField(max_length=30, null=True, verbose_name='Uni\xf3n prote\xednas', blank=True)),
                ('volumen_distrib', models.CharField(max_length=30, null=True, verbose_name='Volumen de distribuci\xf3n', blank=True)),
                ('indice_leche_plasma', models.CharField(max_length=30, null=True, verbose_name='\xcdndice Leche/Plasma', blank=True)),
                ('t_maximo', models.CharField(max_length=30, null=True, verbose_name='Tiempo m\xe1ximo', blank=True)),
                ('t_medio', models.CharField(max_length=30, null=True, verbose_name='Tiempo medio', blank=True)),
                ('biodisponibilidad', models.CharField(max_length=30, null=True, verbose_name='Biodisponibilidad', blank=True)),
                ('dosis_teorica', models.CharField(max_length=30, null=True, verbose_name='Dosis te\xf3rica del lactante', blank=True)),
                ('dosis_relativa', models.CharField(max_length=30, null=True, verbose_name='Dosis relativa del lactante', blank=True)),
                ('dosis_terapeutica', models.CharField(max_length=30, null=True, verbose_name='Porcentaje de la dosis terap\xe9utica', blank=True)),
                ('alternativas', models.ManyToManyField(to='lactancia.Producto', verbose_name='Lista de productos alternativos', blank=True)),
                ('biblio', models.ManyToManyField(to='lactancia.Bibliografia', verbose_name='bibliografia', blank=True)),
                ('grupo', models.ManyToManyField(to='lactancia.Grupo')),
                ('marcas', models.ManyToManyField(to='lactancia.Marca', verbose_name='Listado de marcas comerciales', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Riesgo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nivel', models.IntegerField(unique=True)),
                ('nombre', models.CharField(max_length=200, verbose_name='Nombre')),
                ('nombre_en', models.CharField(max_length=200, null=True, verbose_name='Nombre')),
                ('nombre_es', models.CharField(max_length=200, null=True, verbose_name='Nombre')),
                ('descripcion', models.CharField(max_length=500, verbose_name='Descripci\xf3n')),
                ('descripcion_en', models.CharField(max_length=500, null=True, verbose_name='Descripci\xf3n')),
                ('descripcion_es', models.CharField(max_length=500, null=True, verbose_name='Descripci\xf3n')),
            ],
        ),
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(max_length=7, verbose_name='Idioma')),
                ('time', models.DateTimeField(auto_now=True, verbose_name='Acceso', db_index=True)),
                ('alias', models.ForeignKey(related_name='visita_alias', blank=True, to='lactancia.Alias', null=True)),
                ('grupo', models.ForeignKey(related_name='visita_grupo', blank=True, to='lactancia.Grupo', null=True)),
                ('marca', models.ForeignKey(related_name='visita_marca', blank=True, to='lactancia.Marca', null=True)),
                ('otra_escritura', models.ForeignKey(related_name='visita_otras_escrituras', blank=True, to='lactancia.Otras_escrituras', null=True)),
                ('prod', models.ForeignKey(related_name='visita_producto', blank=True, to='lactancia.Producto', null=True)),
                ('user', models.ForeignKey(to='lactancia.LactUser')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='riesgo',
            field=models.ForeignKey(verbose_name='Nivel de riesgo', to='lactancia.Riesgo'),
        ),
        migrations.AddField(
            model_name='otras_escrituras',
            name='producto_principal',
            field=models.ForeignKey(verbose_name='Nombre principal del producto', to='lactancia.Producto'),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='producto',
            field=models.ForeignKey(verbose_name='Producto vinculado a este mensaje', blank=True, to='lactancia.Producto', null=True),
        ),
        migrations.AddField(
            model_name='marca',
            name='pais',
            field=models.ForeignKey(verbose_name='Pa\xeds donde se comercializa', blank=True, to='lactancia.Pais', null=True),
        ),
        migrations.AddField(
            model_name='marca',
            name='principios_activos',
            field=models.ManyToManyField(to='lactancia.Producto', verbose_name='Listado de principios activos', blank=True),
        ),
        migrations.AddField(
            model_name='comentario',
            name='grupo',
            field=models.ForeignKey(related_name='comentario_grupo', blank=True, to='lactancia.Grupo', null=True),
        ),
        migrations.AddField(
            model_name='comentario',
            name='marca',
            field=models.ForeignKey(related_name='comentario_marca', blank=True, to='lactancia.Marca', null=True),
        ),
        migrations.AddField(
            model_name='comentario',
            name='mensaje',
            field=models.ForeignKey(related_name='comentario_general', blank=True, to='lactancia.Mensaje', null=True),
        ),
        migrations.AddField(
            model_name='comentario',
            name='otra_escritura',
            field=models.ForeignKey(related_name='comentario_otras_escrituras', blank=True, to='lactancia.Otras_escrituras', null=True),
        ),
        migrations.AddField(
            model_name='comentario',
            name='prod',
            field=models.ForeignKey(related_name='comentario_producto', blank=True, to='lactancia.Producto', null=True),
        ),
        migrations.AddField(
            model_name='comentario',
            name='user',
            field=models.ForeignKey(blank=True, to='lactancia.LactUser', null=True),
        ),
        migrations.AddField(
            model_name='bibliografia',
            name='productos',
            field=models.ManyToManyField(to='lactancia.Producto', verbose_name='Productos que referencian este trabajo', blank=True),
        ),
        migrations.AddField(
            model_name='alias',
            name='producto_principal',
            field=models.ForeignKey(verbose_name='Nombre principal del producto', to='lactancia.Producto'),
        ),
        migrations.AlterUniqueTogether(
            name='marca',
            unique_together=set([('nombre', 'comentario')]),
        ),
    ]
