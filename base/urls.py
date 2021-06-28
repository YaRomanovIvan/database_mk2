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
]