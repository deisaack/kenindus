from django.conf.urls import url, include
from django.contrib import admin
from evaluation import urls as evaluation_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^evaluation/', include(evaluation_urls, namespace='evaluation')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^froala_editor/', include('froala_editor.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
