import datetime
import os
from django.http import FileResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Defect_statement, Post, Record_block, Type_block, Component, User, Record_component, Maker
from .filters import Block_filter, One_block_filter, Components_filter, Record_components_filter, Maker_filter
from .forms_block import Defect_statement_form, Record_block_form, Repair_block_form, Type_block_form, Unit_form, Send_block_form, MakerForm, Return_maker_block_form
from .forms_components import (
    New_component_form,
    Edit_component_form, Update_amount_form, Update_price_form
)
#from .forms_order import Create_request_form
from .utils import calculate_component, create_statement


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


@login_required
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


@login_required
def add_new_record_block(request):
    """ добавляем новый блок в ремонт """
    if request.method != "POST":
        return redirect("records_block")
    record_block_form = Record_block_form(request.POST)
    if not record_block_form.is_valid():
        print(record_block_form.errors)
        messages.error(request, "Ошибка формы!")
        return redirect("records_block")
    record_block_form = record_block_form.save(commit=False)
    record_block_form.date_add = datetime.datetime.today()
    record_block_form.save()
    messages.success(
        request, f'Блок с номером {request.POST["number_block"]} добавлен!'
    )
    return redirect("records_block")


@login_required
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


@login_required
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


@login_required
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


@login_required
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
        if block.status != 'неисправен':
            block.status = 'отправлен'
        block.save()
    messages.success(request, "Блоки отправлены!")
    return redirect("records_block")



def block_info(request, pk):
    """ информация о блоке """
    about_block = get_object_or_404(Record_block, pk=pk)
    block = get_object_or_404(Type_block, name_block=about_block.name_block)
    if Defect_statement.objects.filter(block=pk).exists():
        defect = True
    else:
        defect = False
    form = Repair_block_form()
    default_choice = [('', '-------------'),]
    choices = [
        ('', name.type_component + ' ' + name.marking + ' ' + name.note) for name in block.components.all()
    ]
    form.fields['components'].choices = default_choice + choices
    components = about_block.record_block.all()
    context = {
        'about_block': about_block,
        'type_block_form': Type_block_form(instance=block),
        'record_block_form': Record_block_form(instance=about_block),
        'defect_form': Defect_statement_form(),
        'maker_form': MakerForm(initial={'block': about_block, 'maker':block.maker}, instance=about_block),
        'repair_block_form': form,
        'components': components,
        'maker': block.maker,
        'defect': defect,
    }
    return render(request, 'block_info.html', context)


@login_required
def add_components_for_block(request, pk):
    """ привязываем компоненты к блоку из информации о блоке """
    if request.method != "POST":
        return redirect("block_info", pk)
    name_block = get_object_or_404(Record_block, pk=pk)
    block = get_object_or_404(Type_block, name_block=name_block.name_block)
    type_block_form = Type_block_form(request.POST, instance=block)
    if not type_block_form.is_valid():
        messages.error(
            request, "Что-то пошло не так!"
        )
        return redirect("block_info", pk)
    type_block_form.save()
    messages.success(
        request, 'Привязанные компоненты изменились!'
    )
    return redirect("block_info", pk)


@login_required
def repair_block(request, pk):
    """ Ремонт блока """
    if request.method != 'POST':
        return redirect("block_info", pk)
    form = Repair_block_form(request.POST)
    if not form.is_valid():
        print(form.errors)
        messages.error(
            request, "Что-то пошло не так!"
        )
        return redirect("block_info", pk)
    components = list(
            zip(
                request.POST.getlist("namecomponent"),
                request.POST.getlist("amountcomponent"),
            ),
        )
    block = get_object_or_404(Record_block, pk=pk)
    date = datetime.datetime.today()
    note = request.POST.get('note')
    repair_chekbox = request.POST.get('not_repair_date')
    defect_checkbox = request.POST.get('not_defect_statement')
    if repair_chekbox:
        date = None
    if defect_checkbox:
        status = "неисправен"
    else:
        status = "готов"
    if not components:
        block.date_repair = date
        block.note = note
        block.status = status
        if request.user.first_name and request.user.last_name:
            first_name = request.user.first_name
            last_name = request.user.last_name
            block.FIO = f"{first_name} {last_name}"
        block.save()
        messages.success(
            request, "Готово!!"
        )
        return redirect("block_info", pk)
    for component, amount in components:
        if int(amount) < 1 or not amount:
            messages.error(
            request, (
                    f"Компоненто <b>{component}</b> не был списан!<br>"
                    "Количество не может быть меньше 1!"
                )
            )
            return redirect("block_info", pk)
        marking = component.split(' ')
        record = Component.objects.get(
            type_component=marking[0],
            marking=marking[1],
        )
        result = calculate_component(
            record.amount_trk,
            record.amount_eis,
            record.amount_vts,
            int(amount),
        )
        if result["spent_trk"] != 0:
            record.amount_trk -= result["spent_trk"]
            add_record_component = Record_component(
            component=record,
            block=block,
            company="ТРК",
            amount=result["spent_trk"],
            )
            if (
                record.amount_trk >= 0
                and result["amount"] == 0
                ):
                add_record_component.save()
                record.save()
            else:
                messages.error(
                    request,
                    f"Нет такого количества компонента {record.marking} ",
                    )
                return redirect("block_info", pk)
        if result["spent_eis"] != 0:
            record.amount_eis -= result["spent_eis"]
            add_record_component = Record_component(
                component=record,
                block=block,
                company="ЭИС",
                amount=result["spent_eis"],
            )
            if (
                record.amount_eis >= 0
                and result["amount"] == 0
            ):
                add_record_component.save()
                record.save()
            else:
                messages.error(
                    request,
                    f"Нет такого количества компонента {record.marking}",
                )
                return redirect("block_info", pk)
        if result["spent_vts"] != 0:
            record.amount_vts -= result["spent_vts"]
            add_record_component = Record_component(
                component=record,
                block=block,
                company="ВТС",
                amount=result["spent_vts"],
            )
            if (
                record.amount_vts >= 0
                and result["amount"] == 0
            ):
                add_record_component.save()
                record.save()
            else:
                messages.error(
                    request,
                    f"Нет такого количества компонента {record.marking} ",
                )
                return redirect("block_info", pk)
    block.date_repair = date
    block.note = note
    block.status = status
    if request.user.first_name and request.user.last_name:
            first_name = request.user.first_name
            last_name = request.user.last_name
            block.FIO = f"{first_name} {last_name}"
    block.save()
    messages.success(
        request, 'Готово!'
    )
    return redirect("block_info", pk)


@login_required
def edit_record_block(request, pk):
    """ редактирования записанного блока """
    block = get_object_or_404(Record_block, pk=pk)
    context = {
        'form': Record_block_form(instance=block),
        'block': block,
    }
    if request.method != "POST":
        return render(request, 'edit_record_block.html', context)
    form = Record_block_form(request.POST, instance=block)
    if not form.is_valid():
        messages.error(
            request, f'{form.errors}'
        )
        return render(request, 'edit_record_block.html', context)
    form.save()
    messages.success(
        request,
        'Изменения приняты!'
    )
    return redirect('block_info', pk)


def view_defective_statement(request):
    """ страница просмотра дефектных ведомостей """
    qs = Defect_statement.objects.all()
    context = {
        'qs': qs,
    }
    return render(request, 'defect_statement.html', context)


@login_required
def create_defective_statement(request, pk):
    """ создание дефектной ведомости """
    block = get_object_or_404(Record_block, pk=pk)
    if block.defect_block.exists():
        messages.error(
            request,
            'Дефектная ведомость уже создана!<br>'
            'Ознакомьтесь в разделе "дефектные ведомости"'
        )
        return redirect('block_info', pk)
    if block.status == 'отправлен':
        messages.error(
            request,
            'Блок уже отправлен! Вы не можете...'
        )
        return redirect('block_info', pk)
    defect_form = Defect_statement_form(request.POST)
    if not defect_form.is_valid():
        messages.error(
            request, "Что-то пошло не так! Форма не прошла проверку!"
        )
        return redirect('block_info', pk)
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    block.status = 'неисправен'
    block.date_repair = datetime.datetime.today()
    block.save()
    defect = defect_form.save(commit=False)
    defect.block = block
    defect.date_add = date
    defect.region = block.region
    create_statement(block, defect_form.cleaned_data, date)
    defect_form.save()
    messages.success(
        request,
        'Блок отмечен, дефектная ведомость успешно создана!'
    )
    return redirect('block_info', pk)

    
def view_block_maker(request):
    if "search_all" in request.GET:
        data_filter = Maker_filter(
            request.GET, queryset=Maker.objects.all()
        )
        return render(request, 'view_block_maker.html', {'data_filter': data_filter})
    today = datetime.date.today()
    last_mounth = today - datetime.timedelta(days=30)
    queryset = Maker.objects.filter(date_shipment_maker__range=(last_mounth, today))
    data_filter = Maker_filter(request.GET, queryset=queryset)
    print(queryset)
    return render(request, 'view_block_maker.html', {'data_filter': data_filter})


def return_block_maker(request):
    """ промежуточная страница возврата блоков """
    number_id = request.GET.getlist("checkbox")
    if not number_id:
        messages.error(request, "Выберите блоки для отправки!")
        return redirect("view_block_maker")
    queryset = Maker.objects.filter(number_block__in=number_id)
    data_filter = Maker_filter(request.GET, queryset=queryset)
    cnt = data_filter.qs.count()
    status_block = ''
    if 'send_block' in request.GET:
        status_block='send_block'
    elif 'return' in request.GET:
        status_block = 'return_block'
    elif 'defect' in request.GET:
        status_block = 'defect_block'

    return render(
        request,
        "return_block_maker.html",
        {
            "data_filter": data_filter,
            "cnt": cnt,
            'return_block': Return_maker_block_form(),
            'status_block': status_block
        },
    )


def commit_return_block_maker(request):
    """ отправка блоков """
    if request.method != 'POST':
        return redirect('view_block_maker')
    return_block = Return_maker_block_form(request.POST)
    if not return_block.is_valid():
        messages.error(request, "Что-то пошло не так!")
        return redirect("view_block_maker")
    number_id = request.POST.getlist("checkbox")
    if not number_id:
        messages.error(request, "Выберите блоки для отправки!")
        return redirect("view_block_maker")
    return_block.save(commit=False)
    passed = return_block.cleaned_data.get("note_maker")
    date_shipment = datetime.date.today()
    if "send_block" in request.POST:
        for id in number_id:
            block = Maker.objects.get(number_block=id)
            return_block = get_object_or_404(Record_block, pk=id)
            block.note_maker = passed
            block.date_shipment_maker = date_shipment
            block.maker_status = 'отправлен'
            return_block.status = 'производитель'
            return_block.save()
            block.save()
        messages.success(request, "Блоки отправлены!")
        return redirect("view_block_maker")
    if "return_block" in request.POST:
        for id in number_id:
            block = Maker.objects.get(number_block=id)
            return_block = get_object_or_404(Record_block, pk=id)
            block.note_maker = passed
            block.date_add_maker = date_shipment
            block.maker_status = 'возвращен'
            return_block.status = 'готов'
            return_block.date_repair = date_shipment
            return_block.save()
            block.save()
        messages.success(request, "Блоки возвращены!")
        return redirect("view_block_maker")
    if "defect_block" in request.POST:
        for id in number_id:
            block = Maker.objects.get(number_block=id)
            return_block = get_object_or_404(Record_block, pk=id)
            block.note_maker = passed
            block.date_add_maker = date_shipment
            block.maker_status = 'забракован'
            return_block.status = 'неисправен'
            return_block.note = 'Забракован производителем'
            return_block.date_repair = date_shipment
            return_block.save()
            block.save()
        messages.success(request, "Блоки возвращены!")
        return redirect("view_block_maker")


def send_block_maker(request, pk):
    block = get_object_or_404(Record_block, pk=pk)
    if request.method != 'POST':
        return redirect('block_info', pk)
    form = MakerForm(request.POST)
    if Maker.objects.filter(block=block).exists():
        messages.error(
            request,
            'Блок с таким номером уже отправлен производителю!'
        )
        return redirect('block_info', pk)
    if not form.is_valid():
        messages.error(
            request,
            f'Ошибка формы отправки блока производителю! {form.errors}',
            form.errors
        )
        return redirect('block_info', pk)
    form = form.save(commit=False)
    form.maker_status = 'ожидает'
    form.save()
    block.status = 'производитель'
    block.save()
    messages.success(
        request,
        'Блок отправлен производителю для ремонта!'
    )
    return redirect('block_info', pk)


def open_defect_statement(request, pk):
    block = get_object_or_404(Record_block, pk=pk)
    try:
        dest_filename = str(
                f"{block.number_block}_{block.serial_number}_{block.name_block}_{block.region}.xlsx"
            )
        path_open = os.path.join(
            os.getcwd(),
            "base/Statement/Defects/{}".format(
                dest_filename.replace("/", "")
            ),
        )
        return FileResponse(
            open(
                path_open,
                "rb",
            )
        )
    except:
        messages.error(
            request,
            'Ошибка! Файл ведомости поврежден!'
        )
        return redirect('block_info', pk)

    
# -----------------------------------------------------------------------------------------------------
# ------------------------------------ Компоненты -----------------------------------------------------


def view_components(request):
    """ страница с информацие о компонентах и расходе за 30 дней. """
    components = Component.objects.annotate(
        summ=Sum("amount_trk") + Sum("amount_eis") + Sum("amount_vts")
    ).order_by("summ")
    component_filter = Components_filter(
        request.GET,
        queryset=components,
    )
    today = datetime.date.today()
    last_mounth = today - datetime.timedelta(days=30)
    result = []
    for record in component_filter.qs:
        summ = record.record_component.filter(
                date_add__range=(last_mounth, today)
            ).aggregate(Sum('amount'))
        result.append([record, summ['amount__sum']])
    context = {
        'result': result,
        "component_filter": component_filter,
        "new_component_form": New_component_form(),
        "edit_component_form": Edit_component_form(),
        "update_amount_form": Update_amount_form(),
        "update_price_form": Update_price_form(),
    }
    return render(request, 'view_components.html', context)


@login_required
def new_component(request):
    """ создать (добавить) новый компонент """
    if request.method != 'POST':
        return redirect("components")
    form = New_component_form(request.POST)
    if not form.is_valid():
        messages.error(
        request, 'Ошибка формы!'
        )
        return redirect("components")
    form.save()
    messages.success(
        request, 'Компонент добавлен успешно!'
    )
    return redirect('components')
    

@login_required
def update_amount(request):
    """ изменить (прибавить) количество компонента """
    if request.method != 'POST':
        return redirect('components')
    update_amount_form = Update_amount_form(request.POST)
    if update_amount_form.is_valid():
        component = update_amount_form.cleaned_data.get("component")
        amount = update_amount_form.cleaned_data.get("amount")
        company = update_amount_form.cleaned_data.get("company")
        update = Component.objects.get(marking=component.marking)
        if company == "ТРК":
            update.amount_trk += amount
            update.save()
            messages.success(
                request,
                f"Компонент {update.marking} обновлен! "
                f"Добавлено {amount} шт. "
                f"Текущее количество {update.amount_trk} шт. (ТРК)",
            )
            return redirect('components')
        if company == "ЭИС":
            update.amount_eis += amount
            update.save()
            messages.success(
                request,
                f"Компонент {update.marking} обновлен! "
                f"Добавлено {amount} шт. "
                f"Текущее количество {update.amount_eis} шт. (ЭИС)",
            )
            return redirect('components')
        if company == "ВТС":
            update.amount_vts += amount
            update.save()
            messages.success(
                request,
                f"Компонент {update.marking} обновлен! "
                f"Добавлено {amount} шт. "
                f"Текущее количество {update.amount_vts} шт. (ВТС)",
            )
            return redirect('components')
        messages.error(request, "Ошибка! Вероятно вы не указали компанию!")
        return redirect('components')


@login_required
def update_price(request):
    """ изменение цены компонента """
    if request.method != 'POST':
        return redirect('components')
    form = Update_price_form(request.POST)
    if not form.is_valid():
        return redirect('components')
    component = form.cleaned_data.get("component")
    price = form.cleaned_data.get("price")
    record = Component.objects.get(marking=component.marking)
    record.price = price
    record.save()
    messages.success(
        request, f"Цена обновлена! Текущая цена {record.price} рублей."
    )
    return redirect('components')


@login_required
def return_component(request, pk, block):
    """ вернуть компонент, списанный на блок """
    record_component = get_object_or_404(Record_component, pk=pk)
    component = record_component.component
    if record_component.company == "ЭИС":
        component.amount_eis += record_component.amount
        record_component.delete()
        component.save()
    if record_component.company == "ТРК":
        component.amount_trk += record_component.amount
        record_component.delete()
        component.save()
    if record_component.company == "ВТС":
        component.amount_vts += record_component.amount
        record_component.delete()
        component.save()
    messages.success(request, "Компонент возвращен, изменения сохранены.")
    return redirect("block_info", block)


def usage_components(request):
    components = Component.objects.all()
    usage_components = Record_component.objects.all()
    usage_filter = Record_components_filter(request.GET, queryset=usage_components)
    return render(request, 'usage_components.html', {'usage_filter': usage_filter, 'components':components})

# -----------------------------------------------------------------------------------------------------
# ------------------------------------ Заявки и заказы ------------------------------------------------


#def request_component(request):
#    """ просмотр заявок """
#    queryset = Request.objects.all()
#    context = {
#        'queryset': queryset,
#        'create_request_form': Create_request_form(),
#    }
#    return render(request, 'request_components.html', context)


#def create_request(request):
#    """ Создание заявки на компонент """
#    if request.method != 'POST':
#        return redirect('request_component')
#    form = Create_request_form(request.POST)
#    user = get_object_or_404(User, username=request.user)
#    if not form.is_valid():
#        return redirect('request_component')
#    create = form.save(commit=False)
#    component = form.cleaned_data.get("component")
#    request_component = Request.objects.filter(
#        user=user, component=component, status="ожидает"
#    ).exists()
#    if request_component:
#        messages.error(
#            request, 
#                f"Вы уже создали заявку на компонент <b>{component}</b>.<br>" +
#                f"Отредактируйте существующию заявку, либо дождитесь рассмотрения."
#            
#        )
#        return redirect('request_component')
#    create.user = user
#    form.save()
#    messages.success(
#        request, f"Заявка на компонент <b>{create.component}</b> создана!"
#    )
#    return redirect('request_component')


#def edit_request(request, pk):
#    """ Редактирование заявки """
#    get = get_object_or_404(Request, pk=pk)
#    form = Create_request_form(instance=get)
#    if get.user != request.user:
#        messages.error(request, 'Вы не являетесь автором заявки!')
#        return redirect('request_component')
#    if request.method != 'POST':
#        return render(request, 'edit_request.html', {'form':form})
#    form = Create_request_form(request.POST, instance=get)
#    if not form.is_valid():
#        return render(request, 'edit_request.html', {'form':form})
#    form.save()
#    messages.success(
#        request, 'Заявка отредактирована!'
#    )
#    return redirect('request_component')

