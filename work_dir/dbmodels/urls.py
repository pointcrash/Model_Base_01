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
    # path('stuff/', StuffView, name='stuff'),
    path('studios/', home, name='studios'),
    # path('locations/', LocationsView, name='locations'),
    path('gallery/', home, name='gallery'),
    path('entry/', home, name='entry'),
    path('post/<int:post_id>/', show_post, name='post'),
    path('create_model/', model_form_view, name='create_model'),
    path('create_ph/', CreatePh.as_view(), name='create_ph'),
    path('upload_photos.html/', UploadPhotosView.as_view(), name='upload_photos'),
    path('photos.html/', view_photos, name='view_photos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)