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
from rest_framework.schemas import get_schema_view
from phweb import views
from aquarium import views as aquaviews
from rest_framework_jwt.views import refresh_jwt_token

router = routers.SimpleRouter()
router.register(r'deg', views.DegreeViewSet, base_name='deg')
router.register(r'ph', views.PhViewSet, base_name='ph')
router.register(r'redox', views.RedoxViewSet, base_name='redox')
router.register(r'piscine', views.PiscineViewSet, base_name='piscine')

schema_view = get_schema_view(title='Pastebin API')


urlpatterns = [
    url(r'^', include('rest_auth.urls')),
    url(r'^registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^refresh-token/', refresh_jwt_token),
    url(r'^schema/$', schema_view),
    url(r'^$', aquaviews.IndexView.as_view()),
    url(r'^year/$', aquaviews.YearView.as_view(), name='year'),
    url(r'^archive_of_year/([0-9]{4})/$', aquaviews.get_graph_year, name='archive_year'),
    url(r'^admin/', admin.site.urls),
    # required? It seems not.
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    # required? yes
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    #url(r'^docs/', include('django_mkdocs.urls', namespace='documentation')),
]
