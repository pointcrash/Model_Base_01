from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django_filters.views import FilterView

from Models.filters import ModelFilter
from Models.forms import *
from Models.models import *


def HomePageView(request):
    return render(request, 'models/homepage.html', {'menu': menu})


#menu = ['Модели', 'Фотографы', 'Макияж', 'Причёски', 'Студии', 'Локации', 'Галерея', 'Войти']

menu = [
    {'title': "Модели", 'url_name': 'models'},
    {'title': "Фотографы", 'url_name': 'photographers'},
    {'title': "Дополнительно", 'url_name': 'stuff'},
    # {'title': "Студии", 'url_name': 'studios'},
    {'title': "Локации", 'url_name': 'locations'},
    {'title': "Галерея", 'url_name': 'gallery'},
    # {'title': "Войти", 'url_name': 'entry'}
]

class ModelsPage(FilterView):
    model = Model
    menu = menu
    create = 'create_model'
    template_name = 'models/content.html'
    filterset_class = ModelFilter
    paginate_by = 10
    extra_context = {'menu': menu, 'create': create, 'title': 'Модели'}

# class ModelsPage(ListView):
#     model = Model
#     menu = menu
#     create = 'create_model'
#     template_name = 'models/content.html'
#     context_object_name = "posts"
#     extra_context = {'menu': menu, 'create': create, 'title': 'Модели'}
#
#     def get_queryset(self):
#         return Model.objects.filter(is_published=True)

class PhotographerPage(ListView):
    model = Photographer
    menu = menu
    create = 'create_ph'
    template_name = 'models/content.html'
    context_object_name = "posts"
    extra_context = {'menu': menu, 'create': create, 'title': 'Фотографы'}

    def get_queryset(self):
        return Photographer.objects.filter(is_published=True)

def StuffView(request):
    posts = Stuff.objects.all()
    title = 'Стаф'
    return render(request, 'models/content.html', {'posts': posts, 'menu': menu, 'title': title})

def LocationsView(request):
    posts = Model.objects.all()
    title = 'Локации'
    return render(request, 'models/content.html', {'posts': posts, 'menu': menu, 'title': title})

# def StudiosView(request):
#     posts = Model.objects.all()
#     title = 'Студии'
#     return render(request, 'models/base.html', {'posts': posts, 'menu': menu, 'title': title})

def GalleryView(request):
    posts = Model.objects.all()
    title = 'Галерея'
    return render(request, 'models/base.html', {'posts': posts, 'menu': menu, 'title': title})

def EntryView(request):
    posts = Model.objects.all()
    title = 'Вход'
    return render(request, 'models/base.html', {'posts': posts, 'menu': menu, 'title': title})

def show_post(request, post_id):
    return HttpResponse(f'Страница {post_id}')


#<link type="text/css" href="{% static 'models/css/styles.css' %}" rel="stylesheet" />

# def login(request):
#     return HttpResponse('Login')

class RegisterUser(CreateView):
    form_class = UserCreationForm
    menu = menu
    template_name = 'models/register.html'
    success_url = reverse_lazy('models')
    extra_context = {'menu': menu, 'title': 'Модели'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('models')

class LoginUser(LoginView):
    form_class = AuthenticationForm
    menu = menu
    template_name = 'models/login.html'
    success_url = reverse_lazy('models')
    extra_context = {'menu': menu, 'title': 'Модели'}

    def get_success_url(self):
        return reverse_lazy('models')

def logout_user(request):
    logout(request)
    return redirect('login')

class CreateModel(CreateView):
    form_class = CreateModel
    menu = menu
    template_name = 'models/create_model.html'
    extra_context = {'menu': menu, 'title': 'Модели'}

class CreatePh(CreateView):
    form_class = CreatePh
    menu = menu
    template_name = 'models/create_ph.html'
    extra_context = {'menu': menu, 'title': 'Модели'}