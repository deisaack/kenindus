from django.conf.urls import url
from . import views, haris
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^make/$', haris.appraisal_creating, name='appraisal_settings'),
	url(r'^question/q=(?P<slug>[\w\-]+)/$', views.QuestionDetilView.as_view(), name='question_detail'),
	url(r'^question/q?=(?P<slug>[\w\-]+)/update/$', views.QuestionUpdateView.as_view(), name='question_update'),
	url(r'^question/$', views.QuestionList.as_view(), name='question_list'),
	url(r'^question/create/$', views.QuestionCreateView.as_view(), name='question_create'),
	url(r'^flatpage/create/$', views.FlatpageCreateView.as_view(), name='flatpage_create'),
	url(r'^$', views.AppraisalList.as_view(), name='appraisal_list'),
	url(r'^a/(?P<slug>[\w\-]+)/$', views.AppraisalDetilView.as_view(), name='appraisal_detail'),
	url(r'^a/(?P<slug>[\w\-]+)/edit/$', views.AppraisalImproveDetail.as_view(), name='appraisal_improve'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

