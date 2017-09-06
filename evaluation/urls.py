from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
	url(r'^clear/$', views.clear_database, name='clear_database'),
	url(r'^basic-upload/$', views.BasicUploadView.as_view(), name='basic_upload'),
	url(r'^progress-bar-upload/$', views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
	url(r'^drag-and-drop-upload/$', views.DragAndDropUploadView.as_view(), name='drag_and_drop_upload'),
	url('api/chart/data/$', views.ChartData.as_view(), name='chart_data'),
	url(r'^staff/create/$', views.StaffCreateView.as_view(), name='staff_create'),
	url(r'^staff/$', views.StaffListView.as_view(), name='staff_list'),
	url(r'^staff/S-(?P<staff_no>[\w\-]+)/$', views.StaffDetailView.as_view(), name='staff_detail'),
	url(r'^staff/S-(?P<staff_no>[\w\-]+)/appraise/$', views.ApraisalCreateView.as_view(), name='apraisal_create'),
	url(r'^make/$', views.evaluation_creating, name='evaluation_create'),
	url(r'^question/q=(?P<slug>[\w\-]+)/$', views.QuestionDetilView.as_view(), name='question_detail'),
	url(r'^question/q?=(?P<slug>[\w\-]+)/update/$', views.QuestionUpdateView.as_view(), name='question_update'),
	url(r'^question/$', views.QuestionList.as_view(), name='question_list'),
	url(r'^question/create/$', views.QuestionCreateView.as_view(), name='question_create'),
	url(r'^$', views.EvaluationList.as_view(), name='evaluation_list'),
	url(r'^a/(?P<slug>[\w\-]+)/$', views.EvaluationDetilView.as_view(), name='evaluation_detail'),
	url(r'^a/(?P<slug>[\w\-]+)/edit/$', views.EvaluationImproveDetail.as_view(), name='evaluation_improve'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

