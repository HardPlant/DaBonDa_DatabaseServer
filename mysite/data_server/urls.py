from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.handle_sound_data_list, name='sound_data_list')
]