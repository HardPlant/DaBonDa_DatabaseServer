from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.sound_data, name='sound_data')
]