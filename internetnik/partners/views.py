from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from partners.models import Clients, Partners, CommentClient, Contracts, Operators, CommentContract, OperatorSchedule

from partners.forms import AddClientFormOperator, SearchForm, CommentClientForm, EditClientForm, AddClientForm


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
        'title': 'Личный кабинет оператора',
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

            # Создание нового комментария
            comment = CommentClient(client=client, user=request.user, text=form.cleaned_data['comment'])
            comment.save()

        return HttpResponseRedirect(reverse('home'))
    else:
        form = AddClientForm()
    data = {
        'title': 'Отправить нового клиента',
        'form': form
    }

    return render(request, 'partners/add_client.html', data)

    
@login_required
def add_client_operator(request):
    searchform = SearchForm()
    if request.method == 'POST':
        form = AddClientFormOperator(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()

            # Создание нового комментария
            comment = CommentClient(client=client, user=request.user, text=form.cleaned_data['comment'])
            comment.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = AddClientFormOperator()
        
    data = {
        'title': 'Создание нового клиента',
        'form': form,
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
    data_db_clients = Clients.objects.filter(who_is_operator=current_user, callback_date__lte=today).order_by(
        '-time_create')

    data = {
        'title': 'Звонки в работе',
        'clients': data_db_clients
    }
    return render(request, 'partners/calls_in_work.html', context=data)
        
        
@login_required(login_url='/users/login/')
def check_contract(request):
    current_user = Operators.objects.get(user=request.user)
    today = timezone.now().date()  # получаем текущую дату
    data_db_connect = Contracts.objects.filter(who_is_operator=current_user, contract_status='FIX',
                                               connection_date__lte=today).order_by('-time_create')

    data = {
        'title': 'Заявки на проверке подключения',
        'contracts': data_db_connect
    }
    return render(request, 'partners/check_contract.html', context=data)
    
    
@login_required(login_url='/users/login/')
def all_clients(request):
    current_user = Operators.objects.get(user=request.user)
    data_db_clients = Clients.objects.filter(who_is_operator=current_user).order_by('-time_create')
    data = {
        'title': 'Список всех клиентов',
        'clients': data_db_clients,
    }
    return render(request, 'partners/all_clients.html', context=data)
    

@login_required(login_url='/users/login/')
def all_contracts(request):
    current_user = Operators.objects.get(user=request.user)
    data_db_connect = Contracts.objects.filter(who_is_operator=current_user).order_by(
        '-time_create')

    data = {
        'title': 'Список всех заявок',
        'contracts': data_db_connect
    }
    return render(request, 'partners/all_contracts.html', context=data)  
    

@login_required
def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_field = form.cleaned_data['search_field']
            search_term = form.cleaned_data['search_term']
            clients = Clients.objects.none()
            contracts = Contracts.objects.none()
            if search_field == 'phone_number':
                clients = Clients.objects.filter(client_phone_number__icontains=search_term)
                contracts = Contracts.objects.filter(client_phone_number__icontains=search_term)
            elif search_field == 'address':
                clients = Clients.objects.filter(address__icontains=search_term)
                contracts = Contracts.objects.filter(address__icontains=search_term)
            elif search_field == 'contract_number':
                contracts = Contracts.objects.filter(contract_number__icontains=search_term)
            return render(request, 'partners/search_results.html', {'clients': clients, 'contracts': contracts})
    else:
        form = SearchForm()
    return render(request, 'partners/search_results.html', {'form': form})    
    

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
            }
            return render(request, 'partners/edit_client.html', context)
        else:
            return HttpResponseNotFound("<h1>Доступ запрещен</h1>")
    else:
        return HttpResponseNotFound("<h1>Доступ запрещен</h1>")

        
