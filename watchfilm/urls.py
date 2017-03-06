from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^recommend/$', views.recommend, name='recommend'),
    url(r'^mylist/$', views.mylist, name='mylist'),
    url(r'^seen/$', views.seen, name='seen'),
    url(r'^add_to_list/$', views.add_to_list, name='add_to_list'),

]