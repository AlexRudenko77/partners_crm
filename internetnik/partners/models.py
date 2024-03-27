from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Partners(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    partner_city = models.CharField(max_length=50, blank=True)  # город риелтора
    partner_phone_number = models.CharField(max_length=12, blank=True)  # Номер телефона риелтор
    partner_name = models.CharField(max_length=50, blank=True)  # имя риелтора
    partner_motivation = models.CharField(max_length=50, blank=True)  # мотивация риелтора текстом
    telegram_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID в Telegram')

    class Meta:
        verbose_name = "Риелторы"
        verbose_name_plural = "Риелторы"

    def __str__(self):
        return self.partner_name


class Operators(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    operator_phone_number = models.CharField(max_length=12, blank=True)  # Номер телефона оператора
    operator_name = models.CharField(max_length=50, blank=True)  # имя
    is_active = models.BooleanField(default=True, verbose_name='Активность оператора')
    telegram_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID в Telegram')

    class Meta:
        verbose_name = "Операторы"
        verbose_name_plural = "Операторы"

    def __str__(self):
        return self.operator_name


class ContractStatus(models.TextChoices):
    DISCUSS = 'DIS', 'Согласование визита'
    FIXED = 'FIX', 'Назначен визит'
    VERIFY = 'VRF', 'Подключен - проверка оплаты'
    FINISHED = 'FIN', 'Подключен - абон.плата внесена'
    FAILED = 'FAIL', 'Отказ'


class Providers(models.TextChoices):
    ELGOR = 'EG', 'Электронный город'
    SIBSET = 'SS', 'Cибирские сети'
    MTS = 'MTS', 'МТС'
    DOMRU = 'DRU', 'ДомРУ'
    RTK_Spir = 'RTKSpir', 'РТК Спиридонов'
    RTK_Rud = 'RTKRud', 'РТК Руденко'
    RTK_Kuz = 'RTKKuz', 'РТК Кузнецов'
    TTK = 'TTK', 'ТТК'
    BEELINE = 'BL', 'Билайн'
    RUS_KOM = 'RK', ' Русская компания'


class CallResultChoices(models.TextChoices):
    AGREED = 'AG', 'Заявка'
    NOT_AGREED = 'NO', 'Отказ'
    IN_PROCESS = 'PR', 'Думает'
    NO_ANSWER = 'NA', 'Недозвон'
    NEW = 'NEW', 'Новый клиент'


class Clients(models.Model):
    objects = models.Manager()

    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата поступления')  # дата поступления клиента
    time_update = models.DateTimeField(auto_now=True)  # дата обновления
    client_phone_number = models.CharField(max_length=12, blank=False, verbose_name='Номер телефона клиента')
    client_name = models.CharField(max_length=50, blank=True, verbose_name='ФИО клиента')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес клиента')
    call_result = models.CharField(max_length=3, choices=CallResultChoices.choices,
                                   verbose_name='Результат звонка', default='NEW')
    callback_date = models.DateField(null=True, blank=True, verbose_name='Дата повторного звонка')
    is_contract_created = models.BooleanField(default=False, verbose_name='Заключен договор д/н')
    who_is_partner = models.ForeignKey('Partners', on_delete=models.CASCADE, verbose_name='Источник заявки',
                                       null=True, blank=True)
    who_is_operator = models.ForeignKey('Operators', on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name='Ответственный оператор')

    class Meta:
        verbose_name = "Клиенты"
        verbose_name_plural = "Клиенты"


class Contracts(models.Model):
    objects = models.Manager()

    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заявки')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    who_is_client = models.ForeignKey(Clients, on_delete=models.CASCADE, verbose_name='ID клиента', null=True)
    client_phone_number = models.CharField(max_length=12, blank=False, verbose_name='Номер телефона клиента')
    client_name = models.CharField(max_length=80, blank=True, verbose_name='ФИО клиента')
    client_info = models.TextField(blank=True, verbose_name='Данные для заявки (дата рождения, паспорт...')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес клиента')

    who_is_partner = models.ForeignKey('Partners', on_delete=models.CASCADE, verbose_name='Источник заявки', null=True,
                                       blank=True)
    who_is_operator = models.ForeignKey('Operators', on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name='Ответственный оператор')

    provider = models.CharField(null=True, max_length=7, choices=Providers.choices, blank=True,
                                verbose_name='Провайдер')
    contract_number = models.CharField(null=True, max_length=50, blank=True, verbose_name='Номер договора')
    tariff = models.CharField(null=True, max_length=80, blank=True, verbose_name='Тариф')
    arpu = models.CharField(null=True, max_length=50, blank=True, verbose_name='стоимость тарифа')
    equipment = models.CharField(null=True, max_length=50, blank=True, verbose_name='Оборудование')
    contract_status = models.CharField(null=True, max_length=4, choices=ContractStatus.choices, blank=True,
                                       verbose_name='Статус подключения')
    connection_date = models.DateField(null=True, blank=True, verbose_name='Дата подключения')
    partners_motivation = models.CharField(max_length=4, null=True, blank=True,
                                           verbose_name='Размер бонуса')  # Мотивация партнера
    is_paid_to_partner = models.BooleanField(default=False, verbose_name='Выплачен ли бонус риелтору')
    operators_motivation = models.CharField(max_length=4, default=0,
                                            verbose_name='Бонус оператора')  # Мотивация оператора
    is_paid_to_operator = models.BooleanField(default=False, verbose_name='Выплачен ли бонус оператору')
    salary_sum = models.CharField(max_length=6, blank=True, null=True, verbose_name='ЗП за заявку')
    is_paid_by_provider = models.BooleanField(default=False, verbose_name='Оплата провайдером')

    class Meta:
        verbose_name = "Заявки"
        verbose_name_plural = "Заявки"


class CommentClient(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return 'Comment {} by {}'.format(self.text, self.user.username)


class CommentContract(models.Model):
    contract = models.ForeignKey(Contracts, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return 'Comment {} by {}'.format(self.text, self.user.username)


class OperatorSchedule(models.Model):
    objects = models.Manager()
    date = models.DateField(verbose_name='Дата')
    operator = models.ForeignKey(Operators, on_delete=models.CASCADE, verbose_name='Оператор')

    class Meta:
        unique_together = ('operator', 'date')
        verbose_name = "График"
        verbose_name_plural = "График"
