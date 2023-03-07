"""dbmodels URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Models.views import *
from dbmodels import settings

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('models/', ModelsPage.as_view(), name='models'),
    path('', HomePageView, name='home'),
    path('photographer/', PhotographerPage.as_view(), name='photographers'),
    path('stuff/', StuffView, name='stuff'),
    path('studios/', HomePageView, name='studios'),
    path('locations/', LocationsView, name='locations'),
    path('gallery/', HomePageView, name='gallery'),
    path('entry/', HomePageView, name='entry'),
    path('post/<int:post_id>/', show_post, name='post'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('create_model/', CreateModel.as_view(), name='create_model'),
    path('create_ph/', CreatePh.as_view(), name='create_ph')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)