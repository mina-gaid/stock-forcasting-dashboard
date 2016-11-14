from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^control-panel/$', views.panel, name='control-panel'),
	url(r'^tables/$', views.tables, name='tables'),
	url(r'^charts/$', views.charts, name='charts'),
]
