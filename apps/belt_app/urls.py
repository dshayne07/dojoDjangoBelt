from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.add),
    url(r'^add_trip$', views.add_trip),
    url(r'^travels/join/(?P<tid>\d+)$', views.join),
    url(r'^travels/destination/(?P<tid>\d+)$', views.destination),
    url(r'^travels/user/(?P<uid>\d+)$', views.user)
]
