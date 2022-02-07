from django.conf.urls import url

from tasks import views

urlpatterns = [
    #используется для загрузки всех туров и экспертных оценок заданного вопроса, если это админ он видит все туры и все оценки , если это эксперт он видит все свои оценки за все туры

    url(r'^/get/$', views.get, name='get'),
    url(r'^/create/$', views.create, name='create'),
    url(r'^/send_comment/$', views.sendComment, name='sendComment'),
    url(r'^/setStatus/$', views.setStatus, name='setStatus'),
    url(r'^/get_comment/$', views.getComment, name='getComment'),

]