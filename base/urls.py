from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('blocks/', include('base.urls_blocks')),
    path('components/', include('base.urls_components')),
    path('orders/', include('base.urls_orders')),
]