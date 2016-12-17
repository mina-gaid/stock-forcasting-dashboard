from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^about/$', views.about, name='about'),
	url(r'^login/$', views.login, name='login'),
	url(r'^password-reset/$', views.preset, name='password-reset'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^support/$', views.support, name='support'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^terms/$', views.terms, name='terms'),
]
