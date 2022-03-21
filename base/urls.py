from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('blocks/', include('base.urls_blocks')),
    path('components/', include('base.urls_components')),
    path('orders/', include('base.urls_orders')),
]
from django.urls import path

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns += [
    path('sentry-debug/', trigger_error),
]