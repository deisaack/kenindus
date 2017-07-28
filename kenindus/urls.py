from django.conf.urls import url, include
from django.contrib import admin
from appraisal import urls as appraisal_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^appraisal/', include(appraisal_urls, namespace='appraisal')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^froala_editor/', include('froala_editor.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

]
