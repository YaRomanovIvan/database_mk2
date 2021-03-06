from django.urls import path
from . import views


urlpatterns = [
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
    path('block/edit_block_maker/<int:pk>/', views.edit_block_maker, name='edit_block_maker'),
    path('block/defective_statement/', views.view_defective_statement, name='defective_statement'),
    path('block/create_defective_statement/<int:pk>/', views.create_defective_statement, name='create_defective_statement'),
    path('open_defect_statement/<int:pk>/', views.open_defect_statement, name='open_defect_statement'),
    path('maker/', views.view_block_maker, name='view_block_maker'),
]