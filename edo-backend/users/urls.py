from django.conf.urls import url

from users import views

urlpatterns = [
    #используется для загрузки всех туров и экспертных оценок заданного вопроса, если это админ он видит все туры и все оценки , если это эксперт он видит все свои оценки за все туры
    url(r'^get/$', views.get, name='get'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^load/$', views.load, name='load'),
    url(r'^get_detail/$', views.getDetail, name='get_detail'),

    url(r'^checkLogin/$', views.checkLogin, name='checkLogin'),
    url(r'^getCurrentUser/$', views.getCurrentUser, name='getCurrentUser'),
    #url(r'^add/$', views.registration, name='add'),

]