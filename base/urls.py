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
    path('block/send_block_maker/<int:pk>/', views.send_block_maker, name='send_block_maker'),
    path('block/return_block_maker/', views.return_block_maker, name='return_block_maker'),
    path('block/return_block_maker/commit/', views.commit_return_block_maker, name='commit_return_block_maker'),
    path('block/defective_statement/', views.view_defective_statement, name='defective_statement'),
    path('block/create_defective_statement/<int:pk>/', views.create_defective_statement, name='create_defective_statement'),
    path('open_defect_statement/<int:pk>/', views.open_defect_statement, name='open_defect_statement'),
    path('return_component/<int:pk>/<int:block>/', views.return_component, name='return_component'),
    path('components/', views.view_components, name='components'),
    path('components/new_component/,', views.new_component, name='new_component'),
    path('components/update_amount/', views.update_amount, name='update_amount'),
    path('components/update_price/', views.update_price, name='update_price'),
    path('components/usage_components/', views.usage_components, name='usage_components'),
    path('maker/', views.view_block_maker, name='view_block_maker'),
    path('order/', views.view_order, name='view_order'),
    path('order/request/create/', views.create_request, name='create_request'),
    path('order/processing_order/<int:pk>/', views.processing_order, name='processing_order'),
    path('order/order_components/', views.order_components, name='order_components'),
    path('order/incomplete_commit_order/<int:pk>/', views.incomplete_commit_order, name='incomplete_commit_order'),
    path('order/cancel_order/<int:pk>/', views.cancel_order, name='cancel_order'),
    path('order/edit/<int:pk>/', views.edit_order, name='edit_order'),
    path('order/confirmation_form/', views.order_confirmation, name='confirmation_form'),
    path('order/confirmation_commit/', views.confirmation_commit, name='confirmation_commit'),
]