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
    path('home', home, name='home'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit', edit_profile, name='edit_profile'),
    path('models/', ModelsPage.as_view(), name='models'),
    path('photographer/', PhotographerPage.as_view(), name='photographers'),
    # path('staff/', StuffView, name='staff'),
    path('studios/', home, name='studios'),
    # path('locations/', LocationsView, name='locations'),
    path('models/post/<int:post_id>/', show_model_post, name='model_post'),
    path('ph/post/<int:post_id>/', show_ph_post, name='ph_post'),
    path('create_model/', model_form_view, name='create_model'),
    path('create_ph/', create_ph, name='create_ph'),
    path('delete-photo/<int:photo_id>/', delete_photo, name='delete_photo'),
    path('delete-photo-ph/<int:photo_id>/', delete_photo_ph, name='delete_photo'),
    path('create-album/', create_album, name='create_album'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)