from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from findmynotes import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('backend.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
