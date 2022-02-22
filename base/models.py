from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL

User = get_user_model()


class Post(models.Model):
    """
    Новости и информация центра
    """
    title = models.CharField(
        max_length=50,
        verbose_name='Заголовок',)
    image = models.ImageField(
        upload_to="posts/", blank=True, null=True, verbose_name="Изображение"
    )
    text = models.TextField(
        verbose_name="Текст",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Новости"
        verbose_name = "Новость"
        ordering = ["-pub_date"]


class Maker_company(models.Model):
    """ модель компаний производетелей. Записываются названия компаний. """
    name = models.CharField(
        max_length=50,
        verbose_name="Наименование",
    )

    class Meta:
        verbose_name_plural = "Производители"
        verbose_name = "Производитель"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Component(models.Model):
    """ Модель для записи информации о компонентах. Тип компонента, маркировка
    примечание, количество в разных компаниях и средняя цена """
    id = models.AutoField(
        primary_key=True,
        verbose_name="id",
    )
    type_component = models.CharField(
        max_length=100,
        verbose_name="Тип компонента",
    )
    marking = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Маркировка",
    )
    note = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Корпус",
    )
    amount_eis = models.IntegerField(
        validators=[validators.MinValueValidator(0)],
        verbose_name="Количество ЭИС",
    )
    amount_trk = models.IntegerField(
        validators=[validators.MinValueValidator(0)],
        verbose_name="Количество ТРК",
    )
    amount_vts = models.IntegerField(
        validators=[validators.MinValueValidator(0)],
        verbose_name="Количество ВТС",
    )
    price = models.IntegerField(
        validators=[validators.MinValueValidator(0)],
        verbose_name="Цена/шт",
    )

    def __str__(self):
        return "%s %s %s" % (self.type_component, self.marking, self.note)

    class Meta:
        verbose_name_plural = "Компоненты"
        verbose_name = "Компонент"
        ordering = ["type_component"]


class Type_block(models.Model):
    """ Модель создания типа блока. Указываются наименование блока, а так же привязываются
    компонента. Множество блоков имеют множество компонентов """
    name_block = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Наименование блока",
    )
    components = models.ManyToManyField(
        Component,
        related_name='block_components',
        verbose_name='Компоненты блока',
        blank=True,
    )
    maker = models.ForeignKey(
        Maker_company,
        related_name='block_maker',
        verbose_name='Производитель',
        on_delete=SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name_block

    class Meta:
        verbose_name_plural = "Типы блоков"
        verbose_name = "Тип блока"
        ordering = ["name_block"]


class Unit(models.Model):
    """ Модель регионов. Добавляем новые участки. """
    region = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Подразделение",
    )

    def __str__(self):
        return self.region

    class Meta:
        verbose_name_plural = "Подразделения"
        verbose_name = "Подразделение"
        ordering = ["region"]


class Record_block(models.Model):
    """ Модель учета блоков в центре. По сути главная модель, в которой содержится
    вся информация о учтенном блоке. Учетный номер, наименвоание, участок, статус, ФИО водителя. """
    wait = "принят"
    ready = "готов"
    ship = "выдан"
    red = "забракован"
    maker = "производителю"
    CHOICE = [
        (wait, "принят"),
        (ready, "готов"),
        (ship, "выдан"),
        (red, "забракован"),
        (maker, "производителю"),
    ]
    number_block = models.IntegerField(
        primary_key=True,
        verbose_name="Номер блока",
    )
    name_block = models.ForeignKey(
        Type_block,
        on_delete=models.CASCADE,
        verbose_name="Тип блока",
        related_name="record_type_block",
    )
    serial_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Заводской_номер",
    )
    region = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        verbose_name="Подразделение",
        related_name="unit",
    )
    date_add = models.DateField(
        verbose_name="Дата приема",
    )
    date_repair = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата ремонта",
    )
    date_shipment = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата отправки",
    )
    FIO = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name="ФИО",
    )
    status = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        choices=CHOICE,
        default=wait,
        verbose_name="Состояние",
    )
    note = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Примечание",
    )
    passed = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        verbose_name="Передан ФИО",
    )

    def __str__(self):
        return "%s | %s" % (self.number_block, self.name_block)

    class Meta:
        verbose_name_plural = "Блоки в центре"
        verbose_name = "Блок в центре"
        ordering = ["-number_block"]


class Record_component(models.Model):
    """ модель учета компонентов. """
    component = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        verbose_name="Компонент",
        related_name="record_component",
    )
    block = models.ForeignKey(
        Record_block,
        on_delete=models.CASCADE,
        verbose_name="Номер блока",
        related_name="record_block",
    )
    company = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="Компания",
    )
    amount = models.IntegerField(
        validators=[validators.MinValueValidator(1)],
        verbose_name="Количество",
    )
    date_add = models.DateField(
        auto_now_add=True,
        verbose_name="Дата учета",
    )

    class Meta:
        verbose_name_plural = "Учет компонентов"
        verbose_name = "Учет"
        ordering = ["-id"]


class Maker(models.Model):
    """ модель учета блоков, отправленных на ремонт производителю. """
    wait = "ожидает"
    ready = "возвращен"
    ship = "отправлен"
    red = "забракован"
    CHOICE = [
        (wait, "ожидает"),
        (ship, "отправлен"),
        (ready, "возвращен"),
        (red, "забракован"),
    ]
    id = models.AutoField(primary_key=True, verbose_name="id")
    block = models.ForeignKey(
        Record_block,
        on_delete=models.CASCADE,
        verbose_name="Блок",
    )
    number_block = models.PositiveIntegerField(
        verbose_name='Номер блока'
    )
    name_block = models.CharField(
        max_length=150,
        verbose_name="Тип блока",
    )
    serial_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Заводской_номер",
    )
    maker = models.ForeignKey(
        Maker_company,
        on_delete=models.CASCADE,
        verbose_name='Производитель',
    )
    date_shipment_maker = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата отправки производителю",
    )
    date_add_maker = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата возврата",
    )
    maker_status = models.CharField(
        max_length=15,
        choices=CHOICE,
        default=ship,
        verbose_name="Состояние",
    )
    reason = models.CharField(
        max_length=65,
        blank=True,
        null=True,
        verbose_name="Причина отправки",
    )
    note_maker = models.CharField(
        max_length=65,
        blank=True,
        null=True,
        verbose_name="Примечание",
    )

    class Meta:
        verbose_name_plural = "Ремонты Производителей"
        verbose_name = "Ремон производителя"
        ordering = ["-id"]


class Order(models.Model):
    wait = "ожидает"
    processing = "обработан"
    order = "заказан"
    paid = "оплачен"
    commit = "получен"
    under = "недопоставка"
    cancel = "отменен"
    trk = "ТРК"
    vts = "ВТС"
    eis = "ЭИС"
    default = "--------"
    CHOICE = [
        (wait, "ожидает"),
        (processing, "обработан"),
        (order, "заказан"),
        (paid, "оплачен"),
        (commit, "получен"),
        (cancel, "отменен"),
        (under, "недопоставка"),
    ]
    CHOICE_COMPANY = [
        (trk, "ТРК"),
        (vts, "ВТС"),
        (eis, "ЭИС"),
        (default, "--------")
    ]
    component = models.ForeignKey(
        Component,
        on_delete=SET_NULL,
        verbose_name='Наименование компонента',
        related_name='component_request',
        null=True,
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
    )
    amount_order = models.PositiveIntegerField(
        verbose_name='Заказано',
        blank=True,
        null=True,
    )
    amount_commit = models.PositiveIntegerField(
        verbose_name='Получено',
        blank=True,
        null=True,
    )
    date_created = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата заявки',
    )
    date_processing = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата обработки',
    )
    date_order = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата заказа',
    )
    date_commit = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата получения',
    )
    delivery_time = models.CharField(
        max_length=15,
        verbose_name='Срок поставки',
        blank=True,
        null=True,
    )
    provider = models.CharField(
        max_length=100,
        verbose_name='Поставщик',
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=25,
        verbose_name='Статус заявки',
        null=True,
        choices=CHOICE,
        default=wait,
    )
    invoice_number = models.CharField(
        max_length=100,
        verbose_name='Номер счета',
        blank=True,
        null=True,
    )
    invoice_amount = models.FloatField(
        verbose_name='Сумма счета',
        blank=True,
        null=True,
    )
    payer = models.CharField(
        max_length=25,
        verbose_name='Плательщик',
        blank=True,
        null=True,
        choices=CHOICE_COMPANY,
        default=default,
    )
    user = models.CharField(
        max_length=180,
        verbose_name='ФИО',
        blank=True,
        null=True,
    )
    note = models.CharField(
        max_length=100,
        verbose_name='Примечание',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.component}'

    class Meta:
        verbose_name_plural = "Заказы"
        verbose_name = "Заказ"
        ordering = ["-pk"]


class Defect_statement(models.Model):
    """ модель учета дефектных блоков. """
    id = models.AutoField(
        primary_key=True,
        verbose_name="id",
    )
    block = models.ForeignKey(
        Record_block,
        on_delete=models.CASCADE,
        verbose_name="Блок",
        related_name="defect_block",
    )
    region = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        verbose_name="Подразделение",
        related_name="unit_statement",
    )
    date_add = models.DateField(
        verbose_name="Дата",
    )
    defect_1 = models.CharField(
        max_length=100,
        verbose_name="Неисправность 1",
    )
    defect_2 = models.CharField(
        max_length=100,
        verbose_name="Неисправность 2",
        blank=True,
        null=True,
    )
    defect_3 = models.CharField(
        max_length=100,
        verbose_name="Неисправность 3",
        blank=True,
        null=True,
    )
    result = models.CharField(
        max_length=100,
        verbose_name="Заключение",
    )

    class Meta:
        verbose_name_plural = "Дефектные ведомости"
        verbose_name = "Деектная ведомость"
        ordering = ["block"]