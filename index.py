from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assessment_project.settings')

application = get_wsgi_application()

def handler(event, context):
    return application(event, context)

# Vercel requires this
handler = application 