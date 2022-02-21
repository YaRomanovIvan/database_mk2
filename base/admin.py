from django.contrib import admin

from .models import (Component, Defect_statement, Maker, Order,
                     Maker_company, Record_block, Record_component,
                     Type_block, Unit, Post)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'pub_date')


class ComponentsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type_component",
        "marking",
        "note",
        "amount_eis",
        "amount_trk",
        "amount_vts",
        "price",
    )
    list_filter = ("id", "type_component", "marking", "note")
    empty_value_display = "--пусто--"


class Type_blockAdmin(admin.ModelAdmin):
    list_display = ("id", "name_block", 'show_maker', 'show_components')
    list_filter = ("name_block",)
    search_fields = ['name_block__icontains']

    def show_components(self, obj):
        return "\n".join([a.marking for a in obj.components.all()])
    
    def show_maker(self, obj):
        return obj.maker


class UnitAdmin(admin.ModelAdmin):
    list_display = ("id", "region")
    list_filter = ("region",)


class Record_blockAdmin(admin.ModelAdmin):
    list_display = (
        "number_block",
        "name_block",
        "serial_number",
        "region",
        "date_add",
        "date_repair",
        "date_shipment",
        "FIO",
        "status",
        "note",
        "passed",
    )
    list_filter = (
        "name_block__name_block",
        "region",
        "date_add",
        "date_repair",
        "date_shipment",
        "FIO",
        "status",
        "passed",
    )
    empty_value_display = "--пусто--"


class Record_componentsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "component",
        "block",
        "company",
        "amount",
        "date_add",
    )
    list_filter = ("id", "component", "block", "company", "date_add")


class MakerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "number_block",
        "name_block",
        "serial_number",
        "maker",
        "date_shipment_maker",
        "date_add_maker",
        "maker_status",
        "reason",
    )
    list_filter = ("id", "name_block", "maker", "date_shipment_maker", "date_add_maker", "maker_status")
    empty_value_display = "--пусто--"


class Maker_companyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    list_filter = (
        "id",
        "name",
    )
    empty_value_display = "--пусто--"


class RequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'component',
        'created',
        'user',
        'status',
    )
    empty_value_display = "--пусто--"


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'component',
        'amount',
        'amount_order',
        'amount_commit',
        'date_created',
        'date_processing',
        'date_order',
        'date_commit',
        'provider',
        'status',
        'invoice_number',
        'user',
        'note',
    )
    empty_value_display = "--пусто--"


class DefectAdmin(admin.ModelAdmin):
    list_display = (
        'block',
        'region',
        'date_add',
        'defect_1',
        'result',
    )
    empty_value_display = "--пусто--"


admin.site.register(Post, PostAdmin)
admin.site.register(Component, ComponentsAdmin)
admin.site.register(Type_block, Type_blockAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Record_block, Record_blockAdmin)
admin.site.register(Record_component, Record_componentsAdmin)
admin.site.register(Maker, MakerAdmin)
admin.site.register(Maker_company, Maker_companyAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Defect_statement, DefectAdmin)
