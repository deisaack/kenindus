from django.conf.urls import url, include
from django.contrib import admin
from evaluation import urls as evaluation_urls
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(evaluation_urls, namespace='evaluation')),
]
if settings.DEBUG:
    pass
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
