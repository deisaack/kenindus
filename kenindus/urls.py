from django.conf.urls import url, include
from django.contrib import admin
from appraisal import urls as appraisal_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^appraisal/', include(appraisal_urls, namespace='appraisal'))
]
