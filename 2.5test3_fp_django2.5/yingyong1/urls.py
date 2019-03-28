from django.conf.urls import url

from . import views

urlpatterns = [



    url(r'^search_boll/$', views.search_boll),
    url(r'^insert1/$', views.insert_data1),
    url(r'^del_database/$', views.del_database),
]
