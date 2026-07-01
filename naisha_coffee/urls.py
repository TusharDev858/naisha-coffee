from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('coffee.urls')),
    # Serve media files in ALL environments (including production on Render)
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
