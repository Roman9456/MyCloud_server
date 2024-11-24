from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
import logging

# Logger for debugging
logger = logging.getLogger(__name__)

# Simple view for the homepage
def home(request):
    return HttpResponse("Welcome to the homepage!")

# Main URL list
urlpatterns = [
    # Path for the admin panel
    path('admin/', admin.site.urls),
    # Path for the API
    path('api/', include('mycloud_api.urls')),
    # Path for the homepage
    path('', home, name='home'),
]

# Add static files and debug toolbar in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Add Django Debug Toolbar
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    
    # Logging for debugging
    logger.debug("Static files and debug toolbar are activated.")
