"""day_activity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path
from brach_lists import views as brach_lists_views
from brach_lists import urls as brach_lists_urls


urlpatterns = [
    re_path(r'^([a-z,A-Z,0-9]+)?/$', brach_lists_views.view_list, name='view_list'),
    re_path(r'^([a-z,A-Z,0-9]+)?/add_item$', brach_lists_views.add_item, name='add_item'),
    
]
