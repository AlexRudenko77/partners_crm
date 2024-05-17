from django.urls import path, register_converter

from users.views import logout_user
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")


urlpatterns = [
    path('', views.index_check_user_type, name='home'),    # bonus-internet.ru
    path('add_client/', views.add_client_check_user_type, name='add_client'),
    path('show_new_clients/', views.show_new_clients, name='show_new_clients'),
    path('client/<int:client_id>/', views.show_client_check_user_type, name='show_client'),
    path('clients/<int:client_id>/edit/', views.edit_client, name='edit_client'),
    path('calls_in_work/', views.calls_in_work, name='calls_in_work'),
    path('check_contract/', views.check_contract, name='check_contract'),
    path('all_contracts/', views.all_contracts, name='all_contracts'),
    path('all_clients/', views.all_clients, name='all_clients'),
    path('search_results/', views.search, name='search'),
    path('show_contract/<int:contract_id>/', views.show_contract_check_user_type, name='show_contract'),
    path('contracts/<int:contract_id>/edit/', views.edit_contract, name='edit_contract'),


    # path('create_contract/<int:client_id>/', views.create_contract, name='create_contract'),
    #
    # path('contracts_to_coordinate/', views.contracts_to_coordinate, name='contracts_to_coordinate'),

]