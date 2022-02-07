from django.conf.urls import url

from catalog import views

urlpatterns = [
    #используется для загрузки всех туров и экспертных оценок заданного вопроса, если это админ он видит все туры и все оценки , если это эксперт он видит все свои оценки за все туры

    url(r'^get_reconciliation/$', views.getReconciliation, name='getReconciliation'),
    url(r'^create_reconciliation/$', views.createReconciliation, name='createReconciliation'),
    url(r'^reconciliationEdit/$', views.editReconciliation, name='editReconciliation'),
    # url(r'^list/$', views.list, name='list'),
    
    url(r'^get_comments/$', views.getComments, name='get_detail'),
    url(r'^set_comment/$', views.setComment, name='get_detail'),
    
    url(r'^getSharedFileVersions/$', views.getSharedFileVersions, name='getSharedFileVersions'),
    url(r'^get_files/$', views.getFiles, name='get_files'),
    url(r'^applyReconciliation/$', views.applyReconciliation, name='applyReconciliation'),

    url(r'^deleteReconciliation/$', views.deleteReconciliation, name='deleteReconciliation'),
    url(r'^deleteTemplate/$', views.deleteTemplate, name='deleteTemplate'),

    url(r'^getTemplates/$', views.getTemplates, name='getTemplates'),
    url(r'^createTemplates/$', views.createTemplates, name='createTemplates'),
    url(r'^load/$', views.load, name='load'),
    #url(r'^add/$', views.registration, name='add'),

]