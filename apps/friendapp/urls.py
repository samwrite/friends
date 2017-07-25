from django.conf.urls import url
from . import views
app_name = "friendapp"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^add$', views.add, name='add'),
    url(r'^add/(?P<user_id>\d+)$', views.addFriend, name='addFriend'),
    url(r'^view$', views.view, name='view'),
    url(r'^delete/(?P<user_id>\d+)$', views.delete, name='delete'),
]