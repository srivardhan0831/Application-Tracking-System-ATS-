from django.contrib import admin
from django.urls import path, include
from core.views import home  # Homepage view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),          # Homepage
    path('admin/', admin.site.urls),      # Admin panel
    path('api/', include('core.urls')),   # Include all URLs from core app
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)