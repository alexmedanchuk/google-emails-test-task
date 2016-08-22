from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^emails/$', views.ListUsers.as_view(), name="emails"),
]