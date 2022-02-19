from django import template

# В template.Library зарегистрированы все теги и фильтры шаблонов
# добавляем к ним и наш фильтр
register = template.Library()


@register.filter(name='addclass')
def addclass(field, css):
        return field.as_widget(attrs={"class": css})


@register.simple_tag
def my_url(value, field_name, urlencode=None):
        url = '?{}={}'.format(field_name, value)

        if urlencode:
                querystring = urlencode.split('&')
                filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
                encoded_querystring = '&'.join(filtered_querystring)
                url = '{}&{}'.format(url, encoded_querystring)
        return url


@register.simple_tag(takes_context=True)
def page_range(context):
    c = 5
    if context['paginator'].num_pages < 2 * (c + 1):
        return list(range(1, context['paginator'].num_pages + 1))
    if context['page'].number < c + 2:
        n = range(1, 12)
    elif context['page'].number > context['paginator'].num_pages - (c + 1):
        n = range(context['paginator'].num_pages - 2 * c, context['paginator'].num_pages + 1)
    else:
        n = range(context['page'].number - c, context['page'].number + (c + 1))
    return list(n)

# синтаксис @register... , под которой описана функция addclass() - 
# это применение "декораторов", функций, обрабатывающих функции
# мы скоро про них расскажем. Не бойтесь соб@к 