from django.conf.urls import url
from . import views

app_name = 'testApp'
urlpatterns = [
    url(r'^index', views.index, name='index'),
	url(r'^$', views.index, name='index'),
	url(r'^upload/', views.upload, name='upload'),
	url(r'^searchNow/', views.formSearch, name='searchNow'),
	url(r'^batchSearch/', views.batchSearch, name='batchSearch'),
	#url(r'^searchgrad/', views.searchUnderGrad, name='searchGrad'),
	url(r'^searchgradaction/',views.searchUnderGrad, name='searchgradaction'),
	url(r'^searchgrad/', views.searchgrad2, name='searchgrad'),
	url(r'^employ/', views.employ, name='employ'),
	url(r'^retrive/', views.retrive, name='retrive'),
	url(r'^filter/', views.filter, name='filter'),
	url(r'^search/', views.search, name='search'),
	url(r'^delete/', views.delete, name='delete'),
	url(r'^remove/', views.remove, name='remove'),
	url(r'^update/(?P<email_id>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.update, name='update'),
	url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^results/$', views.results, name='results'),
    url(r'^allresults/$', views.allresults, name='allresults'), 
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^merge_update/$', views.mergedUpdate, name='mergedUpdate_update'),
	]