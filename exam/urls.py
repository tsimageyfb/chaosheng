from django.conf.urls import url
from exam import views

urlpatterns = [
    url(r'^$', views.entry, name='entry'),
    url(r'^answer/$', views.index, name='answer'),
    url(r'^score/$', views.score, name='score'),
    url(r'^statistics/$', views.statistics, name='statistics'),
    url(r'^ajax-create-user', views.ajax_create_user, name='create-user'),
    url(r'^ajax-post-answer', views.ajax_post_answer, name='post-answer'),
]
