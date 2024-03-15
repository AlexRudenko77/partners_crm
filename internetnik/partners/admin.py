from django.contrib import admin
from .models import Partners, Clients, Contracts, Operators, OperatorSchedule

# Register your models here.

admin.site.register(Operators)


class ClientsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'time_create', 'address', 'client_phone_number', 'call_result', 'callback_date', 'who_is_partner',
        'who_is_operator')
    list_display_links = ('id', 'address')
    ordering = ['-time_create']


admin.site.register(Clients, ClientsAdmin)


class ContractsAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_create', 'address', 'contract_status', 'who_is_operator', 'who_is_partner')
    list_filter = ('contract_status',)
    list_display_links = ('id', 'address')
    ordering = ['-time_create']


admin.site.register(Contracts, ContractsAdmin)


class PartnersAdmin(admin.ModelAdmin):
    list_display = ('partner_name', 'partner_city', 'partner_phone_number')
    list_display_links = ('partner_name',)


admin.site.register(Partners, PartnersAdmin)


class OperatorScheduleAdmin(admin.ModelAdmin):
    list_display = ('date', 'operator')
    ordering = ['date']
    list_filter = ('operator',)


admin.site.register(OperatorSchedule, OperatorScheduleAdmin)
