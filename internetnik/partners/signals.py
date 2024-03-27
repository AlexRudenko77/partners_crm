from django.contrib.auth.models import User
import requests

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse

from .models import Clients, Contracts, Partners
from django.core.exceptions import ObjectDoesNotExist
from internetnik.settings import bot_config
import phonenumbers


@receiver(post_save, sender=Clients)
def create_contract(sender, instance, created, **kwargs):
    if instance.call_result == 'AG' and instance.is_contract_created == False:

        contract = Contracts.objects.create()
        for field_name in ['client_phone_number', 'client_name', 'address', 'who_is_partner',
                           'who_is_operator']:
            setattr(contract, field_name, getattr(instance, field_name))
        contract.who_is_client = instance
        contract.save()


@receiver(post_save, sender=Clients)
def update_is_contract_created(sender, instance, **kwargs):
    if instance.call_result == 'AG' and not instance.is_contract_created:
        instance.is_contract_created = True
        instance.save()


@receiver(pre_save, sender=Clients)
def set_callback_date_to_null(sender, instance, **kwargs):
    if instance.is_contract_created or instance.call_result == 'NO':
        instance.callback_date = None


@receiver(post_save, sender=User)
def create_partners_profile(sender, instance, created, **kwargs):
    if created:
        # Используйте get_full_name() для получения полного имени пользователя
        partner_name = instance.get_full_name()
        # Создайте объект Partners с полученным именем
        Partners.objects.create(user=instance, partner_name=partner_name)


@receiver(post_save, sender=User)
def save_partners_profile(sender, instance, **kwargs):
    try:
        instance.partners
    except ObjectDoesNotExist:
        # Создайте объект partners, если он не существует
        Partners.objects.create(user=instance, partner_name=instance.get_full_name())
    else:
        # Обновите поле partner_name объекта partners
        instance.partners.partner_name = instance.get_full_name()
        instance.partners.save()


@receiver(post_save, sender=Clients)
def notify_operator_new_client_added(sender, instance, created, **kwargs):
    if created:
        if instance.who_is_operator and instance.who_is_operator.telegram_id:
            TOKEN = bot_config.tg_bot.token
            chat_id = instance.who_is_operator.telegram_id  # Используем telegram_id оператора
            client_edit_url = f"https://bonus-internet.ru{reverse('edit_client', kwargs={'client_id': instance.id})}"
            partner_name = instance.who_is_partner.partner_name if instance.who_is_partner else "Не указан"

            # Преобразование номера телефона
            phone_number = phonenumbers.parse(instance.client_phone_number, "RU")
            formatted_phone_number = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)

            message = f"Новый клиент. Возьмите в работу.\n\nИмя: {instance.client_name}\nАдрес: {instance.address}\nТелефон: {formatted_phone_number}\nКто риелтор: {partner_name} "
            inline_keyboard = [
                [
                    {
                        "text": "Открыть карточку клиента",
                        "url": client_edit_url
                    }
                ]
            ]
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'Markdown',
                'reply_markup': {
                    'inline_keyboard': inline_keyboard
                }
            }
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            response = requests.post(url, json=payload)
            print(response.json())