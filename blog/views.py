import logging
from django.shortcuts import render
from django.conf import settings
logger = logging.getLogger("blog.views")

# Create your views here.
def global_setting(request):
    return {'SITE_NAME': settings.SITE_NAME,
            'SITE_DESC': settings.SITE_DESC}

def index(request):
    return render(request, 'index.html', locals())
