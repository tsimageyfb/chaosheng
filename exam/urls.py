from django.conf.urls import url
from exam import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^score/$', views.score, name='score'),
]
