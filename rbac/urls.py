"""
URL configuration for rbac project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path,re_path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^$', views.index, name='index'),

    path("login",views.auth_login,name="login"),
  
    path('captcha',views.captcha_code,name="captcha"),
    #管理应用路由
    re_path(r'^users/', include('apps.users.urls', namespace='users')),
    re_path(r'^menus/', include('apps.menus.urls', namespace='menus')),
    re_path(r'^permissions/', include('apps.permissions.urls', namespace='permissions')),
    re_path(r'^resourcess/', include('apps.resourcess.urls', namespace='resourcess')),
    re_path(r'^systems/', include('apps.systems.urls', namespace='systems')),
    re_path(r'^logss/', include('apps.logss.urls', namespace='logss')),
]
