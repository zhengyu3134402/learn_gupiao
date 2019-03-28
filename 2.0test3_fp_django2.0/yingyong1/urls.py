from django.conf.urls import url

from . import views

urlpatterns = [


    url(r'^$', views.index),
    url(r'^system/$', views.system),
    url(r'^put_database/$', views.put_database),
    url(r'^search/$', views.search),
    url(r'^start_search/$', views.start_search),

]
