"""
WSGI config for project_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Ubicación del proyecto
PROYECT_URL = '/var/www/html/project_manager'

# Entorno virtual o no de python y sus librerias
VIRTUAL_ENV_URL = '/home/ubuntu/virtual_envs/env_project_manager/lib/python3.6/site-packages'

sys.path.append(PROYECT_URL)
sys.path.append(VIRTUAL_ENV_URL)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_manager.settings")

application = get_wsgi_application()
