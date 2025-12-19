from django.urls import path,include
from canteen import views

urlpatterns = [
    path('',views.homepage, name='homepage'),
    path('menu/', views.menu, name='menu'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.customer_orders, name='customer_orders'),
    path('reorder/<int:order_id>/', views.reorder, name='reorder'),
    path("contact/", views.contact, name="contact"),
    path('my-account/', views.my_account, name='my_account'),
    path("search/", views.search_food, name="search_food"),
    path("payment/", views.payment_page, name="payment_page"),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('download-receipt', views.download_receipt, name="download_receipt"),
]
