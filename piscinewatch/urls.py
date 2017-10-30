"""piscinewatch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from phweb import views
from aquarium import views as aquaviews

router = routers.SimpleRouter()
router.register(r'deg', views.DegreeViewSet, base_name='deg')
router.register(r'ph', views.PhViewSet, base_name='ph')
router.register(r'redox', views.RedoxViewSet, base_name='redox')

urlpatterns = [
    url(r'^$', aquaviews.IndexView.as_view()),
    url(r'^year/$', aquaviews.YearView.as_view(), name='year'),
    url(r'^archive_of_year/([0-9]{4})/$', aquaviews.get_graph_year, name='archive_year'),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    #url(r'^docs/', include('django_mkdocs.urls', namespace='documentation')),
]
