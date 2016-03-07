from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/$', auth_views.login, {'redirect_field_name': '/success/'}),
    url(r'^logout',views.logout_view, name='logged out'),
    url(r'^success/$', views.index),
    url(r'^tags/', TemplateView.as_view(template_name="index_tags.html"),name='tags'),
    url(r'^all_problems/', TemplateView.as_view(template_name="index_all_problems.html"),name='all_problems')
]
