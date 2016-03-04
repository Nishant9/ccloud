from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/$', auth_views.login, {'redirect_field_name': '/success/'}),
    url(r'^logout',views.logout_view, name='logged out'),
    url(r'^success/$', views.index)
]
