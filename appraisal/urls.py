from django.conf.urls import url
from . import views, haris
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^make/$', haris.appraisal_creating, name='appraisal_settings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

