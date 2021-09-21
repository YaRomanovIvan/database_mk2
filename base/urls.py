from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('viewing_block/', views.viewing_block, name='viewing_block'),
    path('records_block/', views.records_block, name='records_block'),
    path(
        "add_record_block/add_new_record_block/",
        views.add_new_record_block,
        name="add_new_record_block",
    ),
    path(
        "add_record_block/add_new_type_block/",
        views.add_new_type_block,
        name="add_new_type_block",
    ),
    path(
        "add_record_block/add_new_region/",
        views.add_new_region,
        name="add_new_region",
    ),
    path(
        'send_block/', views.send_block, name='send_block',
    ),
    path('send_block/commit/', views.commit_send_block, name='commit_send_block'),
    path('block_info/<int:pk>', views.block_info, name='block_info'),
    path(
        'block_info/<int:pk>/add_components_for_block/',
        views.add_components_for_block,
        name='add_components_for_block',
    ),
    path('block_info/edit_block/<int:pk>/', views.edit_record_block, name='edit_block'),
    path(
        'block_info/repair_block/<int:pk>/', 
        views.repair_block, 
        name='repair_block',
    ),
    path('return_component/<int:pk>/<int:block>/', views.return_component, name='return_component'),
    path('components/', views.view_components, name='components'),
    path('components/new_component/,', views.new_component, name='new_component'),
    path('components/update_amount/', views.update_amount, name='update_amount'),
    path('components/update_price/', views.update_price, name='update_price'),
    path('components/usage_components/', views.usage_components, name='usage_components'),
#    path('order/request/', views.request_component, name='request_component'),
#    path('order/request/create/', views.create_request, name='create_request'),
#    path('order/request/edit/<int:pk>/', views.edit_request, name='edit_request'),
]