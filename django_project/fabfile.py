# -*- coding: utf-8 -*-
from fabric.api import local, lcd

def deploy():
    with lcd('/home/django/prod/lactancia/'):
        local('git pull /home/django/dev/lactancia/')
    #with lcd('/home/django/prod/lactancia/django_project/'):
        #local('python manage.py migrate lactancia')
        #local('python manage.py collectstatic --noinput')
        #local('python manage.py test wildcaribe')
    #with lcd('/home/django/prod/lactancia/django_project/lactancia/'):        
    #    local('python ../manage.py compilemessages')
        local('echo DO NOT FORGET TO "sudo service gunicorn restart"')
