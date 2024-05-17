from django.db.models import Q
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
import datetime

from partners.models import Clients, Partners, CommentClient, Contracts, Operators, CommentContract, OperatorSchedule

from partners.forms import AddClientFormOperator, SearchForm, CommentClientForm, EditClientForm, AddClientForm, \
    CommentContractForm, EditContractForm
from django.core.serializers import serialize


# Create your views here.


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


@login_required(login_url='/users/login/')
def index_check_user_type(request):
    if Operators.objects.filter(user=request.user).exists():
        return index_operator(request)
    else:
        return index(request)


@login_required(login_url='/users/login/')
def index(request):
    current_user = Partners.objects.get(user=request.user)
    data_db_clients = Clients.objects.filter(who_is_partner=current_user).order_by('-time_create')
    data = {
        'clients': data_db_clients,
    }
    return render(request, 'partners/index.html', context=data)


@login_required(login_url='/users/login/')
def index_operator(request):
    current_user = Operators.objects.get(user=request.user)
    today = timezone.now().date()  # получаем текущую дату
    calls_in_work_count = Clients.objects.filter(who_is_operator=current_user, callback_date__lte=today).count()
    check_connect_count = Contracts.objects.filter(who_is_operator=current_user, contract_status='FIX',
                                                   connection_date__lte=today).count()
    coordinate_count = Contracts.objects.filter(who_is_operator=current_user, contract_status='DIS').count()

    searchform = SearchForm()
    data = {
        'title': 'Личный кабинет',
        'calls_in_work_count': calls_in_work_count,
        'check_connect_count': check_connect_count,
        'coordinate_count': coordinate_count,
        'searchform': searchform
    }
    return render(request, 'partners/index_operator.html', context=data)


@login_required(login_url='/users/login/')
def add_client_check_user_type(request):
    if Operators.objects.filter(user=request.user).exists():
        return add_client_operator(request)
    else:
        return add_client(request)


def get_current_operator():
    today = timezone.now().date()
    try:
        # Поиск оператора, работающего сегодня
        operator_schedule = OperatorSchedule.objects.get(date=today)
        return operator_schedule.operator
    except OperatorSchedule.DoesNotExist:
        return None


@login_required
def add_client(request):
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.who_is_partner = request.user.partners
            client.callback_date = timezone.now().date()
            operator = get_current_operator()  # определяем оператора, работающего сегодня
            client.who_is_operator = operator
            client.save()

            # Проверяем, что поле комментария не пустое
            if form.cleaned_data['comment'].strip():  # Используем strip() для удаления пробелов в начале и конце
                # Создание нового комментария только если комментарий не пустой
                comment = CommentClient(client=client, user=request.user, text=form.cleaned_data['comment'])
                comment.save()

        return HttpResponseRedirect(reverse('show_client', args=[client.id]))
    else:
        form = AddClientForm()
    data = {
        'title': 'Отправить нового клиента',
        'form': form
    }

    return render(request, 'partners/add_client.html', data)


@login_required
def add_client_operator(request):
    partners = Partners.objects.all().order_by('partner_name')
    searchform = SearchForm()
    if request.method == 'POST':
        form = AddClientFormOperator(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.callback_date = timezone.now()
            operator = Operators.objects.get(user=request.user)
            client.who_is_operator = operator
            client.save()

            # Проверяем, что поле комментария не пустое
            if form.cleaned_data['comment'].strip():  # Используем strip() для удаления пробелов в начале и конце
                # Создание нового комментария только если комментарий не пустой
                comment = CommentClient(client=client, user=request.user, text=form.cleaned_data['comment'])
                comment.save()

        return HttpResponseRedirect(reverse('show_client', args=[client.id]))

    else:
        form = AddClientFormOperator()

    data = {
        'title': 'Создание нового клиента',
        'form': form,
        'partners': partners,
        'searchform': searchform
    }

    return render(request, 'partners/add_client_operator.html', data)


@login_required(login_url='/users/login/')
def show_new_clients(request):
    current_user = Operators.objects.get(user=request.user)
    searchform = SearchForm()
    data_db_clients = Clients.objects.filter(who_is_operator=current_user, call_result='NEW').order_by(
        '-time_create')

    data = {
        'title': 'Новые клиенты',
        'clients': data_db_clients,
        'searchform': searchform
    }
    return render(request, 'partners/show_new_clients.html', context=data)


@login_required(login_url='/users/login/')
def calls_in_work(request):
    current_user = Operators.objects.get(user=request.user)
    today = timezone.now().date()  # получаем текущую дату
    end_of_today = datetime.datetime.combine(today, datetime.time.max)  # конец текущего дня
    data_db_clients = Clients.objects.filter(who_is_operator=current_user, callback_date__lte=end_of_today).order_by(
        '-time_create')
    searchform = SearchForm()

    data = {
        'title': 'Позвонить сегодня',
        'clients': data_db_clients,
        'searchform': searchform,

    }
    return render(request, 'partners/calls_in_work.html', context=data)


@login_required(login_url='/users/login/')
def check_contract(request):
    current_user = Operators.objects.get(user=request.user)
    today = timezone.now().date()  # получаем текущую дату
    data_db_connect = Contracts.objects.filter(who_is_operator=current_user, contract_status='FIX',
                                               connection_date__lte=today).order_by('-time_create')
    searchform = SearchForm()
    data = {
        'title': 'Заявки на проверке подключения',
        'contracts': data_db_connect,
        'searchform': searchform,

    }
    return render(request, 'partners/check_contract.html', context=data)


@login_required(login_url='/users/login/')
def all_clients(request):
    current_user = Operators.objects.get(user=request.user)
    data_db_clients = Clients.objects.filter(who_is_operator=current_user).order_by('-time_create')
    searchform = SearchForm()
    data = {
        'title': 'Список всех клиентов',
        'clients': data_db_clients,
        'searchform': searchform,
    }
    return render(request, 'partners/all_clients.html', context=data)


@login_required(login_url='/users/login/')
def all_contracts(request):
    current_user = Operators.objects.get(user=request.user)
    data_db_connect = Contracts.objects.filter(who_is_operator=current_user).order_by(
        '-time_create')
    searchform = SearchForm()
    data = {
        'title': 'Список всех заявок',
        'contracts': data_db_connect,
        'searchform': searchform,
    }
    return render(request, 'partners/all_contracts.html', context=data)


@login_required
def search(request):
    if request.method == 'POST':
        searchform = SearchForm(request.POST)
        if searchform.is_valid():
            search_field = searchform.cleaned_data['search_field']
            search_term = searchform.cleaned_data['search_term']
            clients = Clients.objects.none()
            contracts = Contracts.objects.none()
            if search_field == 'phone_number':
                clients = Clients.objects.filter(Q(client_phone_number__icontains=search_term) | Q(second_phone_number__icontains=search_term))
                contracts = Contracts.objects.filter(Q(client_phone_number__icontains=search_term) | Q(second_phone_number__icontains=search_term))
            elif search_field == 'address':
                clients = Clients.objects.filter(address__icontains=search_term)
                contracts = Contracts.objects.filter(address__icontains=search_term)
            elif search_field == 'contract_number':
                contracts = Contracts.objects.filter(contract_number__icontains=search_term)
            return render(request, 'partners/search_results.html', {'clients': clients, 'contracts': contracts, 'searchform': searchform})
    else:
        searchform = SearchForm()
    return render(request, 'partners/search_results.html', {'searchform': searchform})


@login_required(login_url='/users/login/')
def show_client_check_user_type(request, client_id):
    if Operators.objects.filter(user=request.user).exists():
        return show_client_operator(request, client_id)
    else:
        return show_client(request, client_id)


@login_required(login_url='/users/login/')
def show_client(request, client_id):
    client = get_object_or_404(Clients, id=client_id)
    contracts = Contracts.objects.filter(who_is_client=client.id)
    comments = CommentClient.objects.filter(client=client).order_by('-created_at')
    current_partner = Partners.objects.get(user=request.user)

    if client.who_is_partner == current_partner:
        if request.method == 'POST':
            comment_form = CommentClientForm(request.POST)
            if comment_form.is_valid():
                new_comment = CommentClient(text=comment_form.cleaned_data['text'],
                                            client=client, user=request.user)
                new_comment.save()
                return redirect('show_client', client_id=client_id)
        else:
            comment_form = CommentClientForm()

        context = {
            'client': client,
            'comments': comments,
            'comment_form': comment_form,
            'contracts': contracts,

        }
        return render(request, 'partners/show_client.html', context)
    else:
        return HttpResponseNotFound("<h1>Доступ запрещен</h1>")


@login_required(login_url='/users/login/')
def show_client_operator(request, client_id):
    client = get_object_or_404(Clients, id=client_id)
    contracts = Contracts.objects.filter(who_is_client=client.id)
    searchform = SearchForm()

    comments = CommentClient.objects.filter(client=client).order_by('-created_at')
    current_operator = Operators.objects.get(user=request.user)

    if client.who_is_operator == current_operator:
        if request.method == 'POST':
            comment_form = CommentClientForm(request.POST)
            if comment_form.is_valid():
                new_comment = CommentClient(text=comment_form.cleaned_data['text'], client=client, user=request.user)
                new_comment.save()
                return redirect('show_client', client_id=client_id)
        else:
            comment_form = CommentClientForm()

        context = {
            'client': client,
            'comments': comments,
            'comment_form': comment_form,
            'contracts': contracts,
            'is_operator': Operators.objects.filter(user=request.user).exists(),
            'searchform': searchform,
            'title': 'Новый клиент',
        }
        return render(request, 'partners/show_client_operator.html', context)
    else:
        return HttpResponseNotFound("<h1>Доступ запрещен</h1>")


@login_required(login_url='/users/login/')
def edit_client(request, client_id):
    client = get_object_or_404(Clients, id=client_id)
    searchform = SearchForm()

    if Operators.objects.filter(user=request.user).exists():
        current_operator = Operators.objects.get(user=request.user)
        if client.who_is_operator == current_operator:
            if request.method == 'POST':
                form = EditClientForm(request.POST, instance=client)

                if form.is_valid():
                    form.save()
                    return redirect('show_client', client_id=client_id)
            else:
                form = EditClientForm(instance=client)

            comments = CommentClient.objects.filter(client=client).order_by('-created_at')

            context = {
                'client': client,
                'form': form,
                'comments': comments,
                'searchform': searchform,
                'title': 'Редактирование клиента',
            }
            return render(request, 'partners/edit_client.html', context)
        else:
            return HttpResponseNotFound("<h1>Доступ запрещен</h1>")
    else:
        return HttpResponseNotFound("<h1>Доступ запрещен</h1>")


@login_required(login_url='/users/login/')
def show_contract_check_user_type(request, contract_id):
    if Operators.objects.filter(user=request.user).exists():
        return show_contract_operator(request, contract_id)
    else:
        return show_contract(request, contract_id)


@login_required
def show_contract(request, contract_id):
    contract = get_object_or_404(Contracts, id=contract_id)
    comments = CommentContract.objects.filter(contract=contract).order_by('-created_at')
    current_partner = Partners.objects.get(user=request.user)
    client = getattr(contract, 'who_is_client')

    if contract.who_is_partner == current_partner:
        if request.method == 'POST':
            comment_form = CommentContractForm(request.POST)
            if comment_form.is_valid():
                new_comment = CommentContract(text=comment_form.cleaned_data['text'],
                                              contract=contract, user=request.user)
                new_comment.save()
                return redirect('show_contract', contract_id=contract_id)
        else:
            comment_form = CommentContractForm()

        context = {
            'contract': contract,
            'comments': comments,
            'comment_form': comment_form,
            'client': client,
        }
        return render(request, 'partners/show_contract.html', context)
    else:
        return HttpResponseNotFound("<h1>Доступ запрещен</h1>")


@login_required
def show_contract_operator(request, contract_id):
    contract = get_object_or_404(Contracts, id=contract_id)
    client = getattr(contract, 'who_is_client')
    searchform = SearchForm()
    comments = CommentContract.objects.filter(contract=contract).order_by('-created_at')
    current_operator = Operators.objects.get(user=request.user)

    if contract.who_is_operator == current_operator:
        if request.method == 'POST':
            comment_form = CommentContractForm(request.POST)
            if comment_form.is_valid():
                new_comment = CommentContract(text=comment_form.cleaned_data['text'],
                                              contract=contract, user=request.user)
                new_comment.save()
                return redirect('show_contract', contract_id=contract_id)
        else:
            comment_form = CommentContractForm()

        context = {
            'title': 'Информация по заявке',
            'contract': contract,
            'comments': comments,
            'comment_form': comment_form,
            'client': client,
            'searchform': searchform,
        }
        return render(request, 'partners/show_contract_operator.html', context)
    else:
        return HttpResponseNotFound("<h1>Доступ запрещен</h1>")


@login_required
def edit_contract(request, contract_id):
    contract = get_object_or_404(Contracts, id=contract_id)
    searchform = SearchForm()

    if Operators.objects.filter(user=request.user).exists():
        if request.method == 'POST':
            form = EditContractForm(request.POST, instance=contract)
            if form.is_valid():
                form.save()
                return redirect('show_contract', contract_id=contract_id)
            else:
                form = EditContractForm(instance=contract)
        else:
            form = EditContractForm(instance=contract)
        comments = CommentContract.objects.filter(contract=contract).order_by('-created_at')
        context = {
            'title': 'Редактирование заявки',
            'contract': contract,
            'form': form,
            'comments': comments,
            'searchform': searchform,
        }
        return render(request, 'partners/edit_contract.html', context)
    else:
        return HttpResponseNotFound('<h1>Доступ запрещен</h1>')