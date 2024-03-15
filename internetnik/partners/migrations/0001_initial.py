# Generated by Django 4.1.10 on 2023-12-21 17:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата поступления')),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('client_phone_number', models.CharField(max_length=12, verbose_name='Номер телефона клиента')),
                ('client_name', models.CharField(blank=True, max_length=50, verbose_name='ФИО клиента')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Адрес клиента')),
                ('call_result', models.CharField(choices=[('AG', 'Заявка'), ('NO', 'Отказ'), ('PR', 'Думает'), ('NA', 'Недозвон'), ('NEW', 'Новый клиент')], default='NEW', max_length=3, verbose_name='Результат звонка')),
                ('callback_date', models.DateField(blank=True, null=True, verbose_name='Дата повторного звонка')),
                ('is_contract_created', models.BooleanField(default=False, verbose_name='Заключен договор д/н')),
            ],
            options={
                'verbose_name': 'Клиенты',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Partners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner_city', models.CharField(blank=True, max_length=50)),
                ('partner_phone_number', models.CharField(blank=True, max_length=12)),
                ('partner_name', models.CharField(blank=True, max_length=50)),
                ('partner_motivation', models.CharField(blank=True, max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Риелторы',
                'verbose_name_plural': 'Риелторы',
            },
        ),
        migrations.CreateModel(
            name='Operators',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operator_phone_number', models.CharField(blank=True, max_length=12)),
                ('operator_name', models.CharField(blank=True, max_length=50)),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность оператора')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Операторы',
                'verbose_name_plural': 'Операторы',
            },
        ),
        migrations.CreateModel(
            name='Contracts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заявки')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('client_phone_number', models.CharField(max_length=12, verbose_name='Номер телефона клиента')),
                ('client_name', models.CharField(blank=True, max_length=80, verbose_name='ФИО клиента')),
                ('client_info', models.TextField(blank=True, verbose_name='Данные для заявки (дата рождения, паспорт...')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Адрес клиента')),
                ('provider', models.CharField(blank=True, choices=[('EG', 'Электронный город'), ('SS', 'Cибирские сети'), ('MTS', 'МТС'), ('DRU', 'ДомРУ'), ('RTKSpir', 'РТК Спиридонов'), ('RTKRud', 'РТК Руденко'), ('RTKKuz', 'РТК Кузнецов'), ('TTK', 'ТТК'), ('BL', 'Билайн'), ('RK', ' Русская компания')], max_length=7, null=True, verbose_name='Провайдер')),
                ('contract_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Номер договора')),
                ('tariff', models.CharField(blank=True, max_length=80, null=True, verbose_name='Тариф')),
                ('arpu', models.CharField(blank=True, max_length=50, null=True, verbose_name='стоимость тарифа')),
                ('equipment', models.CharField(blank=True, max_length=50, null=True, verbose_name='Оборудование')),
                ('contract_status', models.CharField(blank=True, choices=[('DIS', 'Согласование визита'), ('FIX', 'Назначен визит'), ('VRF', 'Подключен - проверка оплаты'), ('FIN', 'Подключен - абон.плата внесена'), ('FAIL', 'Отказ')], max_length=4, null=True, verbose_name='Статус подключения')),
                ('connection_date', models.DateField(blank=True, null=True, verbose_name='Дата подключения')),
                ('partners_motivation', models.CharField(blank=True, max_length=4, null=True, verbose_name='Размер бонуса')),
                ('is_paid_to_partner', models.BooleanField(default=False, verbose_name='Выплачен ли бонус риелтору')),
                ('operators_motivation', models.CharField(default=0, max_length=4, verbose_name='Бонус оператора')),
                ('is_paid_to_operator', models.BooleanField(default=False, verbose_name='Выплачен ли бонус оператору')),
                ('salary_sum', models.CharField(blank=True, max_length=6, null=True, verbose_name='ЗП за заявку')),
                ('is_paid_by_provider', models.BooleanField(default=False, verbose_name='Оплата провайдером')),
                ('who_is_client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='partners.clients', verbose_name='ID клиента')),
                ('who_is_operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='partners.operators', verbose_name='Ответственный оператор')),
                ('who_is_partner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='partners.partners', verbose_name='Источник заявки')),
            ],
            options={
                'verbose_name': 'Заявки',
                'verbose_name_plural': 'Заявки',
            },
        ),
        migrations.CreateModel(
            name='CommentContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='partners.contracts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='CommentClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='partners.clients')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.AddField(
            model_name='clients',
            name='who_is_operator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='partners.operators', verbose_name='Ответственный оператор'),
        ),
        migrations.AddField(
            model_name='clients',
            name='who_is_partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='partners.partners', verbose_name='Источник заявки'),
        ),
    ]
