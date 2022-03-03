from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_components, name='components'),
    path('return_component/<int:pk>/<int:block>/', views.return_component, name='return_component'),
    path('components/new_component/,', views.new_component, name='new_component'),
    path('components/edit_component/<int:pk>/', views.edit_component, name='edit_component'),
    path('components/update_amount/', views.update_amount, name='update_amount'),
    path('components/update_price/', views.update_price, name='update_price'),
    path('components/usage_components/', views.usage_components, name='usage_components'),
]