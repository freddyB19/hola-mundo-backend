"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls.static import static
try:
    from core.settings import local as setting_file
except Exception as e:
    from core.settings import prod as setting_file


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('account/', include("applications.users.apiv1.urls")),
    re_path("game/", include("applications.game.apiv1.urls")),
] + static(setting_file.MEDIA_URL, document_root = setting_file.MEDIA_ROOT)
