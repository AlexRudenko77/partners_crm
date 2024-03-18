from django import forms
from django.contrib.auth.models import User
from django.db import models

from partners.models import Clients, CommentClient, CommentContract, Contracts, Partners


class SearchForm(forms.Form):
    SEARCH_FIELDS = (
        ('contract_number', 'Поиск по договору'),
        ('phone_number', 'Поиск по телефону'),
        ('address', 'Поиск по адресу'),
    )
    search_field = forms.ChoiceField(choices=SEARCH_FIELDS, label='Параметры поиска',
                                     widget=forms.Select(attrs={'class': 'form-select'}))
    search_term = forms.CharField(label='Введите значение')


class AddClientForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}), label='Комментарий')

    class Meta:
        model = Clients
        fields = ['client_phone_number', 'client_name', 'address', 'comment']


class AddClientFormOperator(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}), label='Комментарий')

    # who_is_partner = forms.ModelChoiceField(queryset=Partners.objects.all().order_by('partner_name'),
    #                                         label='Источник заявки')


    class Meta:
        model = Clients
        fields = ['client_phone_number', 'client_name', 'address', 'who_is_partner', 'comment']


class CommentClientForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True, label='')

    class Meta:
        model = CommentClient
        fields = ['text']


class EditClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['client_name', 'client_phone_number', 'address', 'call_result', 'callback_date']
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'client_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'call_result': forms.Select(attrs={'class': 'form-select'}),
            'callback_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
        }
