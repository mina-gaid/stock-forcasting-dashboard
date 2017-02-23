from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^about/$', views.about, name='about'),
	url(r'^support/$', views.support, name='support'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^terms/$', views.terms, name='terms'),
]
