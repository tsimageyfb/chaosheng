from django.conf.urls import url
from exam import views

urlpatterns = [
    url(r'^$', views.entry, name='entry'),
    url(r'^team/$', views.entry_team, name='team'),
    url(r'^answer/$', views.index, name='answer'),
    url(r'^score/$', views.score, name='score'),
    url(r'^statistics/$', views.statistics, name='statistics'),
    url(r'^stage/$', views.stage, name='stage'),
    url(r'^simulate/$', views.simulate_entry, name='simulate'),
    url(r'^simulate/answer/$', views.simulate_exam, name='simulate-answer'),

    url(r'^ajax-create-user', views.ajax_create_user, name='create-user'),
    url(r'^ajax-post-answer', views.ajax_post_answer, name='post-answer'),
    url(r'^ajax-post-simulate', views.ajax_post_answer_simulate, name='post-answer-simulate'),

    url(r'^robot-tick-answer', views.robot_tick_answer, name='robot-tick-answer'),
    url(r'^robot-submit-answer', views.robot_submit_answer, name='robot-submit-answer'),
    url(r'^robot-get-progress', views.robot_get_progress, name='robot-get-progress'),

    url(r'^team-get-progress', views.team_get_progress, name='team-get-progress'),
    url(r'^team-get-rank', views.team_get_rank, name='team-get-rank'),
    url(r'^team-tick-answer', views.team_tick_answer, name='team-tick-answer'),
    url(r'^team-submit-answer', views.team_submit_answer, name='team-submit-answer'),

    url(r'^audience-get-progress', views.audience_get_progress, name='audience-get-progress'),
    url(r'^audience-get-rank', views.audience_get_rank, name='audience-get-rank'),

    url(r'^rest-seconds', views.rest_seconds, name='rest-seconds'),

    url(r'^wrong-rank', views.wrong_rank, name='wrong-rank'),
    url(r'^show', views.show_exam, name='show-exam'),

    url(r'^get-stage', views.req_get_stage, name='get-stage'),
    url(r'^set-stage', views.req_set_stage, name='set-stage'),
    url(r'^ajax-add-stage', views.add_stage, name='add-stage'),
    url(r'^ajax-sub-stage', views.sub_stage, name='sub-stage'),

    url(r'^all-users-statistics', views.all_users_statistics, name='statistics'),
]
