from django.urls import re_path
from . import views


urlpatterns = [
    re_path('^(?P<room>\w+)/$', views.MessageView.as_view())
]
