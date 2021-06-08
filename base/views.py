from django.shortcuts import render, redirect
import datetime
from django.contrib import messages
from .models import Post, Record_block, Unit, Type_block
from .filters import Block_filter, One_block_filter


def index(request):
    """ главная страница с информацией """
    queryset = Post.objects.all()
    context = {
        'posts': queryset,
    }
    return render(request, 'index.html', context)


def viewing_block(request):
    """ учет блоков. Информация о блоках в центре """
    today = datetime.date.today()
    last_mounth = today - datetime.timedelta(days=30)
    if "one_block_filter" in request.GET:
        data_filter = One_block_filter(
            request.GET, queryset=Record_block.objects.all()
        )
        cnt = data_filter.qs.count()
        return render(
            request,
            "viewing-block.html",
            {
                "data_filter": data_filter,
                "cnt": cnt,
            },
        )
    if "search_all" in request.GET:
        data_filter = Block_filter(
            request.GET, queryset=Record_block.objects.all()
        )
        cnt = data_filter.qs.count()
        return render(
            request,
            "viewing-block.html",
            {
                "data_filter": data_filter,
                "cnt": cnt,
            },
        )

    queryset = Record_block.objects.prefetch_related(
        "name_block", "region"
    ).filter(date_add__range=(last_mounth, today))
    data_filter = Block_filter(request.GET, queryset=queryset)
    cnt = data_filter.qs.count()

    return render(
        request,
        "viewing-block.html",
        {
            "data_filter": data_filter,
            "cnt": cnt,
        },
    )


def records_block(request):
    today = datetime.date.today()
    last_mounth = today - datetime.timedelta(days=30)
    if "one_block_filter" in request.GET:
        data_filter = One_block_filter(
            request.GET, queryset=Record_block.objects.all()
        )
        cnt = data_filter.qs.count()
        return render(
            request,
            "viewing-block.html",
            {
                "data_filter": data_filter,
                "cnt": cnt,
            },
        )
    if "search_all" in request.GET:
        data_filter = Block_filter(
            request.GET, queryset=Record_block.objects.all()
        )
        cnt = data_filter.qs.count()
        return render(
            request,
            "records-block.html",
            {
                "data_filter": data_filter,
                "cnt": cnt,
            },
        )

    queryset = Record_block.objects.prefetch_related(
        "name_block", "region"
    ).filter(date_add__range=(last_mounth, today))
    data_filter = Block_filter(request.GET, queryset=queryset)
    cnt = data_filter.qs.count()

    return render(
        request,
        "records-block.html",
        {
            "data_filter": data_filter,
            "cnt": cnt,
        },
    )
