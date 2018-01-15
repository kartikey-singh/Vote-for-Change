from django.conf.urls import url,include
from .views import *
from django.contrib.auth import views
from django.contrib.auth.views import *

urlpatterns=[
    url(r'^$', home),       
    url(r'^home/$', home, name='home'),
    url(r'^about/$', about, name='about'),
    url(r'^rightbar/$', rightbar, name='rightbar'),
    url(r'^nobar/$', nobar, name='nobar'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^login/$', LoginView, name='login'),
    url(r'^logout/$', LogoutView, name='logout'),
    url(r'^dashboard/$', DashboardView, name='dashboard'),
    url(r'^registration/$', RegistrationView, name='registration'),
    url(r'^getcausedata/$', getCauseData, name='getCauseData'),
    url(r'^submitcausedata/$', submitCauseData, name='submitCauseData'),
]
