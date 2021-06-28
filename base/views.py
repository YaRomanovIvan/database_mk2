from django.shortcuts import get_object_or_404, render, redirect
import datetime
from django.contrib import messages
from .models import Post, Record_block, Unit, Type_block
from .filters import Block_filter, One_block_filter
from .forms_block import Record_block_form, Type_block_form, Unit_form, Send_block_form


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
    """ управление блоками """
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
                "type_block_form": Type_block_form(),
                "unit_form": Unit_form(),
                "record_block_form": Record_block_form(),
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
            "type_block_form": Type_block_form(),
            "unit_form": Unit_form(),
            "record_block_form": Record_block_form(),
        },
    )


def add_new_record_block(request):
    """ добавляем новый блок в ремонт """
    if request.method != "POST":
        return redirect("records_block")
    record_block_form = Record_block_form(request.POST)
    if not record_block_form.is_valid():
        messages.error(request, "Что-то пошло не так!")
        return redirect("records_block")
    record_block_form.save()
    messages.success(
        request, f'Блок с номером {request.POST["number_block"]} добавлен!'
    )
    return redirect("records_block")


def add_new_type_block(request):
    """ добавляем новое наименование блока """
    if request.method != "POST":
        return redirect("records_block")
    type_block_form = Type_block_form(request.POST)
    if not type_block_form.is_valid():
        messages.error(
            request, "Что-то пошло не так! Возможно такой блок уже существует!"
        )
        return redirect("records_block")
    type_block_form.save()
    messages.success(
        request, f'Наименование {request.POST["name_block"]} добавлено!'
    )
    return redirect("records_block")


def add_new_region(request):
    """ добавляем новый участок """
    if request.method != "POST":
        return redirect("records_block")
    unit_form = Unit_form(request.POST)
    if not unit_form.is_valid():
        messages.error(
            request,
            "Что-то пошло не так! Вероятно такой участок уже существует!",
        )
        return redirect("records_block")
    unit_form.save()
    messages.success(request, f'Участок {request.POST["region"]} добавлен!')
    return redirect("records_block")


def send_block(request):
    """ промежуточная страница отправки блоков """
    number_id = request.GET.getlist("checkbox")
    if not number_id:
        messages.error(request, "Выберите блоки для отправки!")
        return redirect("records_block")
    queryset = Record_block.objects.prefetch_related(
        "name_block", "region"
    ).filter(number_block__in=number_id)
    data_filter = Block_filter(request.GET, queryset=queryset)
    cnt = data_filter.qs.count()

    return render(
        request,
        "send_block.html",
        {
            "data_filter": data_filter,
            "cnt": cnt,
            'send_block': Send_block_form(),
        },
    )


def commit_send_block(request):
    """ отправка блоков """
    if request.method != 'POST':
        return redirect('send_block')
    send = Send_block_form(request.POST)
    if not send.is_valid():
        messages.error(request, "Что-то пошло не так!")
        return redirect("send_block")
    number_id = request.POST.getlist("checkbox")
    if not number_id:
        messages.error(request, "Выберите блоки для отправки!")
        return redirect("send_block")
    send.save(commit=False)
    passed = send.cleaned_data.get("passed")
    date_shipment = datetime.date.today()
    for id in number_id:
        block = Record_block.objects.get(pk=id)
        block.passed = passed
        block.date_shipment = date_shipment
        block.status = 'отправлен'
        block.save()
    messages.success(request, "Блоки отправлены!")
    return redirect("records_block")


def block_info(request, pk):
    """ информация о блоке """
    about_block = Record_block.objects.get(pk=pk)
    context = {
        'about_block': about_block,
    }
    return render(request, 'block_info.html', context)