from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_order, name='view_order'),
    path('order/request/create/', views.create_request, name='create_request'),
    path('order/processing_order/<int:pk>/', views.processing_order, name='processing_order'),
    path('order/order_components/', views.order_components, name='order_components'),
    path('order/incomplete_commit_order/<int:pk>/', views.incomplete_commit_order, name='incomplete_commit_order'),
    path('order/cancel_order/<int:pk>/', views.cancel_order, name='cancel_order'),
    path('order/edit/<int:pk>/', views.edit_order, name='edit_order'),
    path('order/confirmation_form/', views.order_confirmation, name='confirmation_form'),
    path('order/confirmation_commit/', views.confirmation_commit, name='confirmation_commit'),
    path('order/create_report/', views.create_report, name='create_report'),
    path('order/create_unit_order/', views.create_unit_order, name='create_unit_order'),
    path('order/create_purpose_order/', views.create_purpose_order, name='create_purpose_order'),
]