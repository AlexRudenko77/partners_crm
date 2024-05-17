from django import forms
from django.contrib.auth.models import User
from django.db import models

from partners.models import Clients, CommentClient, CommentContract, Contracts, Partners


class SearchForm(forms.Form):
    SEARCH_FIELDS = (
        ('phone_number', 'Поиск по телефону'),
        ('address', 'Поиск по адресу'),
        ('contract_number', 'Поиск по договору'),
    )
    search_field = forms.ChoiceField(choices=SEARCH_FIELDS, label='Параметры поиска',
                                     widget=forms.Select(attrs={'class': 'form-select'}))
    search_term = forms.CharField(label='Введите значение')


class AddClientForm(forms.ModelForm):
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}), label='Комментарий')

    class Meta:
        model = Clients
        fields = ['client_phone_number', 'client_name', 'address', 'comment', 'second_phone_number']


class AddClientFormOperator(forms.ModelForm):
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}), label='Комментарий')

    class Meta:
        model = Clients
        fields = ['client_phone_number', 'client_name', 'address', 'who_is_partner', 'comment', 'second_phone_number']


class CommentClientForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True, label='')

    class Meta:
        model = CommentClient
        fields = ['text']


class EditClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['client_name', 'client_phone_number', 'address', 'call_result', 'callback_date', 'second_phone_number']
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'client_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'second_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'call_result': forms.Select(attrs={'class': 'form-select'}),
            'callback_date': forms.DateTimeInput(format='%Y-%m-%d %H:%M',
                                                 attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class CommentContractForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True, label='')

    class Meta:
        model = CommentContract
        fields = ['text']


class EditContractForm(forms.ModelForm):
    class Meta:
        model = Contracts
        fields = ['client_name', 'client_phone_number', 'address', 'provider',
                  'contract_number', 'tariff', 'arpu', 'equipment', 'contract_status', 'connection_date', 'client_info',
                  'second_phone_number']
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'client_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'client_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'second_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'contract_status': forms.Select(attrs={'class': 'form-select'}),
            'contract_number': forms.TextInput(attrs={'class': 'form-control'}),
            'tariff': forms.TextInput(attrs={'class': 'form-control'}),
            'arpu': forms.TextInput(attrs={'class': 'form-control'}),
            'provider': forms.Select(attrs={'class': 'form-select'}),
            'equipment': forms.TextInput(attrs={'class': 'form-control'}),
            'connection_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
        }
