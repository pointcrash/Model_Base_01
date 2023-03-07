from django import template
from Models.models import *


register = template.Library()


@register.inclusion_tag('models/menu.html')
def get_menu():
    menu = [
        {'title': "Модели", 'url_name': 'models'},
        {'title': "Фотографы", 'url_name': 'photographers'},
        {'title': "Стилист's", 'url_name': 'stuff'},
        # {'title': "Студии", 'url_name': 'studios'},
        {'title': "Локации", 'url_name': 'locations'},
        {'title': "Галерея", 'url_name': 'gallery'}
        #{'title': "Войти", 'url_name': 'entry'}
    ]
    return {'menu': menu}

@register.inclusion_tag('models/menu_auth.html')
def get_menu_auth():
    menu = [
        {'title': "Модели", 'url_name': 'models'},
        {'title': "Фотографы", 'url_name': 'photographers'},
        {'title': "Стилист's", 'url_name': 'stuff'},
        # {'title': "Студии", 'url_name': 'studios'},
        {'title': "Локации", 'url_name': 'locations'},
        {'title': "Галерея", 'url_name': 'gallery'}
        #{'title': "Войти", 'url_name': 'entry'}
    ]
    return {'menu': menu}

@register.inclusion_tag('models/sidebar.html')
def get_sidebar():

    return None
