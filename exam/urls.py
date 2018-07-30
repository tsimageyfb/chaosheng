from django.conf.urls import url
from exam import views

urlpatterns = [
    url(r'^$', views.entry, name='entry'),
    url(r'^answer/$', views.index, name='answer'),
    url(r'^score/$', views.score, name='score'),
    url(r'^ajax-create-user', views.ajax_create_user, name='create-user'),
]
