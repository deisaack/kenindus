from django.conf.urls import url
from . import views, haris
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^make/$', haris.evaluation_creating, name='evaluation_settings'),
	url(r'^question/q=(?P<slug>[\w\-]+)/$', views.QuestionDetilView.as_view(), name='question_detail'),
	url(r'^question/q?=(?P<slug>[\w\-]+)/update/$', views.QuestionUpdateView.as_view(), name='question_update'),
	url(r'^question/$', views.QuestionList.as_view(), name='question_list'),
	url(r'^question/create/$', views.QuestionCreateView.as_view(), name='question_create'),
	url(r'^flatpage/create/$', views.FlatpageCreateView.as_view(), name='flatpage_create'),
	url(r'^$', views.EvaluationList.as_view(), name='evaluation_list'),
	url(r'^a/(?P<slug>[\w\-]+)/$', views.EvaluationDetilView.as_view(), name='evaluation_detail'),
	url(r'^a/(?P<slug>[\w\-]+)/edit/$', views.EvaluationImproveDetail.as_view(), name='evaluation_improve'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

