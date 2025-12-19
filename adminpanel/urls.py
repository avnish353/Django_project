from django.urls import path
from adminpanel.views import admin_login
from adminpanel import views

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('', admin_login, name="admin-login"),
    path('menu/', views.menu_items, name="menu-items"),
    path('menu/add/', views.menu_add, name="menu-add"),
    path('menu/edit/<int:pk>/', views.menu_edit, name="menu-edit"),
    path('menu/delete/<int:pk>/', views.menu_delete, name="menu-delete"),
    path('orders/', views.orders, name="orders"),
    path('admin/order/update/<int:order_id>/', views.update_order_status, name='update-order-status'),
    path('payments/', views.payments, name="payments"),
    path('announcements/', views.announcements, name="announcements"),
]

