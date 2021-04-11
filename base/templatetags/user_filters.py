from django import template
from django.template.defaultfilters import stringfilter
# В template.Library зарегистрированы все теги и фильтры шаблонов
# добавляем к ним и наш фильтр
register = template.Library()


@register.filter(name='addclass')
def addclass(field, css):
        return field.as_widget(attrs={"class": css})


# синтаксис @register... , под которой описана функция addclass() - 
# это применение "декораторов", функций, обрабатывающих функции
# мы скоро про них расскажем. Не бойтесь соб@к 