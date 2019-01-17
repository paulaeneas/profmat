#!/usr/bin/env python
import os
import sys


#Executar o ambiente virtual
#myvenv\Scripts\activate

#Inciando o servidor web
#python manage.py runserver

#Criar usuario administrador
# python manage.py createsuperuser

#usuario admin
#user: profmat
#senha: profmat

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
