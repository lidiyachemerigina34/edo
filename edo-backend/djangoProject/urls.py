"""djangoProject6 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from blog import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('blog', include('blog.urls')),
    path('map', include('map.urls')),
    path('bots', include('bots.urls')),
    path('tasks', include('tasks.urls')),
    path('sitemap', include('data.urls')),
    url(r'^contact/$', views.contact, name='contact'),
    path('catalog/', include('catalog.urls')),
    path('place', include('place.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
