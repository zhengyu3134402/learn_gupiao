from django.conf.urls import url

from . import views

urlpatterns = [


    url(r'^index/$', views.index),
    url(r'^search_boll/$', views.search_boll),
    url(r'^insert1/$', views.insert_data1),
]
