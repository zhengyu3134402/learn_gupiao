from django.conf.urls import url

from . import views

urlpatterns = [


    # url(r'^$', views.index),
    # url(r'^system/$', views.system),
    url(r'^del_database/$', views.del_database),
    url(r'^insert1/$', views.insert),
    url(r'^search_boll/$', views.search_boll),

]
