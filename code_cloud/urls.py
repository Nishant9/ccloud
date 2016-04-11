from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from . import views
from .forms import ProblemForm, TagForm

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/$', auth_views.login, {'redirect_field_name': '/success/'}),
    url(r'^accounts/register/$', views.adduser),
    url(r'^logout',views.logout_view, name='logged out'),
    url(r'^success/$', views.index),
    url(r'^tags/', views.tagsview, name='tags'),
    url(r'^all_problems/', views.allproblemsview, name='all_problems'),
    url(r'^shared_problems/', views.sharedproblemsview, name='shared_problems'),
    url(r'^new_problem/', CreateView.as_view(template_name='new_problem.html', form_class=ProblemForm, success_url='/code_cloud/'),name='new_problem'),
    url(r'^update_problem/(?P<pk>\d+)$', views.ProblemUpdate.as_view(),name='update_problem'),
    url(r'^delete_problem/(?P<pk>\d+)$', views.ProblemDelete.as_view(),name='delete_problem'),
    url(r'^query/',views.query, name='query'),
    url(r'^edit_tags/', views.edit_tag, name='edit_tag'),
    url(r'^share_problem/', views.share_problem, name='share_problem'),
    url(r'^view_problem/',views.view_problem, name='view_problem'),
    url(r'^download_problem/',views.download_problem, name='download_problem'),
    url(r'^(?P<page>.+\.(html|.css))$', views.StaticView.as_view()),
]
