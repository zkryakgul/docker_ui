"""django_ui URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^containers$', views.containers),
    url(r'^containers/add$', views.container_add),
    url(r'^containers/(?P<c_id>\w+)$', views.container_detail),
    url(r'^containers/(?P<c_id>\w+)/delete$', views.container_delete),
    url(r'^containers/(?P<c_id>\w+)/start$', views.container_start),
    url(r'^containers/(?P<c_id>\w+)/log$', views.container_logs),
    url(r'^networks$', views.networks),
    url(r'^networks/add$', views.network_add),
    url(r'^networks/(?P<n_id>\w+)$', views.network_detail),
    url(r'^networks/(?P<n_id>\w+)/delete$', views.network_delete),
    url(r'^volumes$', views.volumes),
    url(r'^volumes/add$', views.volume_add),
    url(r'^volumes/(?P<vol_name>[\w-]+)/delete$', views.volume_delete),
    url(r'^instruction$', views.instruction),
    url(r'^info$', views.info),
    url(r'^error$', views.error)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
