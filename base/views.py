import datetime
import os
from django.http import FileResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from .models import Defect_statement, Post, Record_block, Type_block, Component, User, Record_component, Maker, Order
from .filters import Block_filter, Components_filter, Order_filter, Record_components_filter, Maker_filter
from .forms_block import Defect_statement_form, Record_block_form, Repair_block_form, Type_block_form, Unit_form, Send_block_form, MakerForm, Return_maker_block_form
from .forms_components import (
    New_component_form,
    Edit_component_form, Update_amount_form, Update_price_form
)
from .forms_order import Create_request_form, Invoice_number_form, Confirmation_form
from users.permissions import employee_permission, admin_permission
from .utils import calculate_component, create_statement, create_repair_maker


@login_required
def index(request):
    """ главная страница с информацией """
    queryset = Post.objects.all()
    context = {
        'posts': queryset,
    }
    return render(request, 'index.html', context)


@login_required
def viewing_block(request):
    """ учет блоков. Информация о блоках в центре """
    if "one_block_filter" in request.GET:
        block = get_object_or_404(Record_block, pk=request.GET['number_block'])
        return redirect('block_info', block.pk)
    queryset = Record_block.objects.all()
    data_filter = Block_filter(request.GET, queryset=queryset)
    cnt = data_filter.qs.count()
    paginator = Paginator(data_filter.qs, 200)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(
        request,
        "block template/viewing-block.html",
        {   "page": page,
            'paginator': paginator,
            "data_filter": data_filter,
            "cnt": cnt,
        },
    )


@login_required
@employee_permission
def records_block(request):
    """ управление блоками """
    today = datetime.date.today()
    last_mounth = today - datetime.timedelta(days=30)
    if "one_block_filter" in request.GET:
        block = get_object_or_404(Record_block, pk=request.GET['number_block'])
        return redirect('block_info', block.pk)
    queryset = Record_block.objects.all()
    data_filter = Block_filter(request.GET, queryset=queryset)
    cnt = data_filter.qs.count()
    paginator = Paginator(data_filter.qs, 200)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(
        request,
        "block template/records-block.html",
        {
            "page": page,
            'paginator': paginator,
            "data_filter": data_filter,
            "cnt": cnt,
            "type_block_form": Type_block_form(),
            "unit_form": Unit_form(),
            "record_block_form": Record_block_form(),
        },
    )


@login_required
@employee_permission
def add_new_record_block(request):
    """ добавляем новый блок в ремонт """
    if request.method != "POST":
        return redirect("records_block")
    record_block_form = Record_block_form(request.POST)
    if not record_block_form.is_valid():
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
@employee_permission
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
@employee_permission
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
@employee_permission
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
        "block template/send_block.html",
        {
            "data_filter": data_filter,
            "cnt": cnt,
            'send_block': Send_block_form(),
        },
    )


@login_required
@employee_permission
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
        if block.status != 'забракован':
            block.status = 'выдан'
        block.save()
    messages.success(request, "Блоки выданы!")
    return redirect("records_block")


@login_required
@employee_permission
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
    return render(request, 'block template/block_info.html', context)


@login_required
@employee_permission
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
@employee_permission
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
        status = "забракован"
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
        record_check = Component.objects.filter(
            marking__in=marking
        ).exists()
        if not record_check:
            messages.error(
            request, (
                    f"Компонент <b>{component}</b> не существует! Возможно вы оставили поле пустым?"
                )
            )
            return redirect("block_info", pk)
        record = Component.objects.get(
            marking__in=marking,
        )
        result = calculate_component(
            record.amount_trk,
            record.amount_eis,
            record.amount_vts,
            int(amount),
        )
        if result["spent_trk"] == 0 and result["spent_eis"] == 0 and result["spent_vts"] == 0:
            messages.error(
                    request,
                    f"Склад с компонентом {record.marking} пуст! Вы не можете его списать! ",
                    )
            return redirect("block_info", pk)
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
@employee_permission
def edit_record_block(request, pk):
    """ редактирования записанного блока """
    block = get_object_or_404(Record_block, pk=pk)
    context = {
        'form': Record_block_form(instance=block),
        'block': block,
    }
    if request.method != "POST":
        return render(request, 'block template/edit_record_block.html', context)
    form = Record_block_form(request.POST, instance=block)
    if not form.is_valid():
        messages.error(
            request, f'{form.errors}'
        )
        return render(request, 'block template/edit_record_block.html', context)
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
    return render(request, 'block template/defect_statement.html', context)


@login_required
@employee_permission
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
    if block.status == 'выдан':
        messages.error(
            request,
            'Блок уже выдан! Вы не можете...'
        )
        return redirect('block_info', pk)
    defect_form = Defect_statement_form(request.POST)
    if not defect_form.is_valid():
        messages.error(
            request, "Что-то пошло не так! Форма не прошла проверку!"
        )
        return redirect('block_info', pk)
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    block.status = 'забракован'
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


@login_required
@employee_permission    
def view_block_maker(request):
    queryset = Maker.objects.all()
    data_filter = Maker_filter(request.GET, queryset=queryset)
    paginator = Paginator(data_filter.qs, 100)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    cnt = data_filter.qs.count()
    context = {
        'data_filter': data_filter,
        'cnt':cnt,
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'block template/view_block_maker.html', context)


def return_block_maker(request):
    """ промежуточная страница блоков производителей """
    number_id = request.GET.getlist("checkbox")
    if not number_id:
        messages.error(request, "Выберите блоки!")
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
    elif 'create_maker_xlsx' in request.GET:
        status_block = 'create_maker_xlsx'

    return render(
        request,
        "block template/return_block_maker.html",
        {
            "data_filter": data_filter,
            "page": data_filter.qs,
            "cnt": cnt,
            'return_block': Return_maker_block_form(),
            'status_block': status_block
        },
    )


@login_required
@employee_permission
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
            return_block.status = 'производителю'
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
            return_block.status = 'забракован'
            return_block.note = 'Забракован производителем'
            return_block.date_repair = date_shipment
            return_block.save()
            block.save()
        messages.success(request, "Блоки возвращены!")
        return redirect("view_block_maker")
    if "create_maker_xlsx" in request.POST:
        qs = Maker.objects.filter(block__pk__in=number_id)
        create_repair_maker(qs)
        try:
            dest_filename = "repair_maker.xlsx"
            path_open = os.path.join(
                os.getcwd(),
                "base/Maker/{}".format(
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
                'Ошибка! Файл поврежден!'
            )
            return redirect("view_block_maker")

@login_required
@employee_permission
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
    block.status = 'производителю'
    block.save()
    messages.success(
        request,
        'Блок добавлен в список отправки!'
    )
    return redirect('block_info', pk)


@login_required
@employee_permission
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


@login_required
@employee_permission
def view_components(request):
    """ страница с информацие о компонентах и расходе за 30 дней. """
    components = Component.objects.annotate(
        summ=Sum("amount_trk") + Sum("amount_eis") + Sum("amount_vts")
    ).order_by("summ", "type_component", "marking")
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
        "new_component_form": New_component_form(initial={'amount_vts': 0, 'amount_eis': 0, 'amount_trk': 0,}),
        "edit_component_form": Edit_component_form(),
        "update_amount_form": Update_amount_form(),
        "update_price_form": Update_price_form(),
    }
    return render(request, 'component template/view_components.html', context)


@login_required
@employee_permission
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


def edit_component(request, pk):
    """ Редикатирование компонента """
    component = get_object_or_404(Component, pk=pk)
    form = Edit_component_form(instance=component)
    if request.method != 'POST':
        return render(
            request, 'component template/edit_component.html', {'form': form}
        )
    form = Edit_component_form(request.POST, instance=component)
    if not form.is_valid():
        return render(
            request, 'component template/edit_component.html', {'form': form}
        )
    form.save()
    messages.success(
        request, f'Компонент "{component}" изменен успешно!'
    )
    return redirect('components')
    

@login_required
@employee_permission
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
@employee_permission
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
@employee_permission
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


@login_required
@employee_permission
def usage_components(request):
    components = Component.objects.all()
    usage_components = Record_component.objects.all()
    usage_filter = Record_components_filter(request.GET, queryset=usage_components)
    return render(request, 'component template/usage_components.html', {'usage_filter': usage_filter, 'components':components})

# -----------------------------------------------------------------------------------------------------
# ------------------------------------ Заявки и заказы ------------------------------------------------


@login_required
@employee_permission
def view_order(request):
    """ просмотр заявок """
    data_filter = Order_filter(
        request.GET,
        queryset=Order.objects.all()
    ).qs
    today = datetime.datetime.today()
    cnt = data_filter.count()
    paginator = Paginator(data_filter, 50)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    context = {
        'data_filter': data_filter,
        'cnt': cnt,
        'paginator': paginator,
        'page': page,
        'today': today,
        'data_filter_form': Order_filter(),
        'create_request_form': Create_request_form(),
        'processing_order_form': Create_request_form(),
        'invoice_number_form': Invoice_number_form(),
        'incomplete_commit_order': Invoice_number_form(),
    }
    return render(request, 'order template/view_order.html', context)


@login_required
@employee_permission
def create_request(request):
    """ Создание заявки на компонент """
    if request.method != 'POST':
        return redirect('view_order')
    form = Create_request_form(request.POST)
    user = get_object_or_404(User, username=request.user)
    if not form.is_valid():
        return redirect('view_order')
    create = form.save(commit=False)
    date = datetime.datetime.today()
    component = form.cleaned_data.get("component")
    order_exists = Order.objects.filter(
        component=component,
        status='ожидает'
    )
    for i in order_exists:
        if user.last_name in i.user.split(', '):
            messages.error(
                request, 
                    f"Вы уже создали заявку на компонент {component}"
            )
            return redirect('view_order')

    if order_exists.exists():
        order = get_object_or_404(Order,
            component=component,
            status='ожидает'
        )
        amount = form.cleaned_data.get("amount")
        order.amount += amount
        order.user += f', {user.last_name}'
        order.save()
        messages.success(
            request, 
            f"Заявка на компонент <b>{create.component}</b> уже существует!" +
            f"Вы были присоеденены к заявке!"
        )
        return redirect('view_order')
        
    create.user = user.last_name
    create.date_created = date
    form.save()
    messages.success(
        request, f"Заявка на компонент <b>{create.component}</b> создана!"
    )
    return redirect('view_order')


@login_required
@employee_permission
def processing_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method != 'POST':
        context = {
            'processing_order_form': Create_request_form(instance=order),
            'order': order,
        }
        return render(request, 'order template/processing_order.html', context)
    form = Create_request_form(request.POST, instance=order)
    if not form.is_valid():
        context = {
            'processing_order_form': Create_request_form(instance=order),
            'order': order,
        }
        return render(request, 'order template/processing_order.html', context)
    form = form.save(commit=False)
    date = datetime.datetime.today()
    form.date_processing = date
    form.status = 'обработан'
    form.save()
    context = {
        'processing_order_form': Create_request_form(instance=order)
    }
    return redirect('view_order')


@login_required
@employee_permission
def commit_order(request):
    number_id = request.POST.getlist("checkbox")
    if not number_id:
        messages.error(request, "Выберите заказы!")
        return redirect("view_order")
    error = []
    order_date_commit = datetime.datetime.today()
    for pk in number_id:
        order = get_object_or_404(Order, pk=pk)
        component = get_object_or_404(
            Component, pk=order.component.pk

        )
        if order.status == 'оплачен':
            order.date_commit = order_date_commit
            order.amount_commit = order.amount_order
            order.status = "получен"
            if order.payer == 'ЭИС':
                component.amount_eis += order.amount_order
            elif order.payer == 'ТРК':
                component.amount_trk += order.amount_order
            elif order.payer == 'ВТС':
                component.amount_vts += order.amount_order
            order.save()
            component.save()
        else:
            error.append(order.pk)
    if error:
        messages.error(
            request,
            f'Заявки {error} не могут быть обработаны! Проверьте их статус!'
        )
        return redirect("view_order")
    messages.success(
        request,
        'Заявки успешно получены!'
    )
    return redirect("view_order")


@login_required
@employee_permission
def order_components(request):
    number_id = request.POST.getlist("checkbox")
    if 'commit_order' in request.POST:
        commit_order(request)
        return redirect("view_order")
    if not number_id:
        messages.error(request, "Выберите заказы!")
        return redirect("view_order")
    if request.method != 'POST':
        return redirect("view_order")
    form = Invoice_number_form(request.POST)
    if not form.is_valid():
        return redirect("view_order")
    invoice_number = form.cleaned_data['number']
    invoice_amount = form.cleaned_data['invoice_amount']
    if not invoice_number:
        messages.error(request, "Заполните поле 'Номер счета'")
        return redirect("view_order")
    if not invoice_amount:
        if not invoice_amount == 0:
            messages.error(request, "Заполните поле 'Сумма счета'")
            return redirect("view_order")
    payer = form.cleaned_data['payer']
    provider = form.cleaned_data['provider']
    delivery_time = form.cleaned_data['delivery_time']
    date_order = datetime.datetime.today()
    error = []
    for pk in number_id:
        order = get_object_or_404(Order, pk=pk)
        if order.status == 'обработан':
            order.date_order = date_order
            order.invoice_number = invoice_number
            order.invoice_amount = invoice_amount
            order.payer = payer
            order.provider = provider
            order.delivery_time = delivery_time
            order.status = "заказан"
            order.save()
        else:
            error.append(order.pk)
    if error:
        messages.error(
            request,
            f'Заявки {error} не могут быть обработаны! Проверьте их статус!'
        )
        return redirect("view_order")
    messages.success(
        request,
        'Заявки успешно заказаны!'
    )
    return redirect("view_order")


@login_required
@employee_permission
def incomplete_commit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method != 'POST':
        context = {
            'incomplete_commit_order': Create_request_form(instance=order),
            'order': order,
        }
        return render(request, 'order template/incomplete_commit_order.html', context)
    form = Create_request_form(request.POST, instance=order)
    date = datetime.datetime.today()
    if not form.is_valid():
        context = {
            'incomplete_commit_order': Create_request_form(instance=order),
            'order': order,
        }
        return render(request, 'order template/incomplete_commit_order.html', context)
    form = form.save(commit=False)
    if form.amount_commit > form.amount_order:
        messages.error(
        request,
        'Вы не можете получить больше, чем заказали!'
        )
        return redirect('view_order')
    if form.amount_commit < form.amount_order:
        Order.objects.create(
            component=form.component,
            amount=form.amount,
            amount_order=form.amount_order - form.amount_commit,
            date_created=form.date_created,
            date_processing=form.date_processing,
            date_order=date,
            delivery_time=form.delivery_time,
            provider=form.provider,
            invoice_number=form.invoice_number,
            invoice_amount=form.invoice_amount,
            payer=form.payer,
            user=form.user,
            status='недопоставка'
        )
    component = get_object_or_404(
        Component, pk=order.component.pk

    )
    if order.payer == 'ЭИС':
        component.amount_eis += form.amount_commit
    elif order.payer == 'ТРК':
        component.amount_trk += form.amount_commit
    elif order.payer == 'ВТС':
        component.amount_vts += form.amount_commit
    form.date_commit = date
    form.status = 'получен'
    component.save()
    form.save()
    messages.success(
        request,
        'Заявка обработана! Компонент успешно получен!'
    )
    return redirect('view_order')
        

@login_required
@employee_permission
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method != 'POST':
        context = {
            'order': order,
        }
        return render(request, 'order template/cancel_order.html', context)
    order.amount_commit = 0
    order.status = 'отменен'
    Order.objects.create(
        component=order.component,
        amount=order.amount,
        status='ожидает',
        date_created=order.date_created,
        user=order.user,
        note=order.note,
    )
    order.save()
    messages.warning(
            request,
            'Заявка отменена!'
    )
    return redirect('view_order')

def edit_order(request, pk):
    """ Редактирование заявки """
    get = get_object_or_404(Order, pk=pk)
    form = Create_request_form(instance=get)
    if request.method != 'POST':
        return render(request, 'order template/edit_order.html', {'form':form})
    form = Create_request_form(request.POST, instance=get)
    if not form.is_valid():
        return render(request, 'order template/edit_order.html', {'form':form})
    form.save()
    messages.success(
        request, 'Заявка отредактирована!'
    )
    return redirect('view_order')


def order_confirmation(request):
    if 'cancel' in request.GET:
        cancel = True
    else:
        cancel = False
    if request.method != 'POST':
        form = Confirmation_form()
        return render(request, 'order template/order_confirmation_form.html', {'form': form, 'cancel': cancel})
    form = Confirmation_form(request.POST)
    if not form.is_valid():
        return render(request, 'order template/order_confirmation_form.html', {'form': form, 'cancel': cancel})
    invoice_number = form.cleaned_data['invoice_number']
    order = Order.objects.filter(invoice_number=invoice_number, status='заказан')
    if not order.exists():
        order = Order.objects.filter(invoice_number=invoice_number, status='оплачен')
    cnt = order.count()
    return render(request, 'order template/order_confirmation_commit.html', {'page':order, 'cnt':cnt, 'cancel': cancel})


def confirmation_commit(request):
    number_id = request.POST.getlist("checkbox")
    if not number_id:
        messages.error(
        request, 'На странице подтвеждения оплаты не были выбраны позиции!'
        )
        return redirect('view_order')
    if 'cancel' in request.POST:
        for pk in number_id:
            order = get_object_or_404(Order, pk=pk)
            order.status = 'отменен'
            Order.objects.create(
                component=order.component,
                amount=order.amount,
                status='ожидает',
                date_created=order.date_created,
                user=order.user,
                note=order.note,
            )
            order.save()
        messages.warning(
            request,
            'Позиции успешно изменили статус на "отменен"! Заявки пересозданы!'
        )   
    else:
        for pk in number_id:
            order = get_object_or_404(Order, pk=pk)
            if order.status != 'заказан':
                messages.error(
                    request, 'Статус одного из заказов не прошел проверку! Статус должен быть "заказан"!'
                )
                return redirect('view_order')
            order.status = 'оплачен'
            order.save()
        messages.success(
            request,
            'Позиции успешно изменили статус на "оплачено"!'
        )
    return redirect('view_order')

