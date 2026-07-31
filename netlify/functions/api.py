import os
import sys

# Add project root directory to python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodhub.settings')

try:
    import django
    django.setup()
    from django.core.management import call_command
    call_command('migrate', interactive=False)
except Exception:
    pass

import serverless_wsgi
from foodhub.wsgi import application

def handler(event, context):
    return serverless_wsgi.handle_request(application, event, context)
