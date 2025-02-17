from django.urls import path
from library_app.views import *

# --- URL Configuration ---
urlpatterns = [
    path('', home, name='home'),
    path('books/', book_list, name='book_list'),
    path('books/create/', book_create, name='book_create'),
    path('books/update/<int:pk>/', book_update, name='book_update'),
    path('books/delete/<int:pk>/', book_delete, name='book_delete'),

    path('members/', member_list, name='member_list'),
    path('members/create/', member_create, name='member_create'),
    path('members/update/<int:pk>/', member_update, name='member_update'),
    path('members/delete/<int:pk>/', member_delete, name='member_delete'),

    path('transactions/', transaction_list, name='transaction_list'),
    path('transactions/create/', transaction_create, name='transaction_create'),
    path('transactions/update/<int:pk>/', transaction_update, name='transaction_update'),
    path('transactions/delete/<int:pk>/', transaction_delete, name='transaction_delete'),

    path('staff/', staff_list, name='staff_list'),
    path('staff/create/', staff_create, name='staff_create'),
    path('staff/update/<int:pk>/', staff_update, name='staff_update'),
    path('staff/delete/<int:pk>/', staff_delete, name='staff_delete'),
]