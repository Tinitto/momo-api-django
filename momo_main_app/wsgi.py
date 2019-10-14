"""
WSGI config for momo_api_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=env_path)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'momo_main_app.settings')

application = get_wsgi_application()
