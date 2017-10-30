from .views import IndexView, get_graph
from django.conf.urls import url

app_name = 'aquarium'

urlpatterns = [
    url(r'^home/$', IndexView.as_view(), name='home'),
    url(r'^archive/$', get_graph, name='archive'),
    ]
