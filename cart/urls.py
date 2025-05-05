from django.urls import path
from . import views

app_name = 'cart'


urlpatterns = [
    path('add/<int:product_id>', views.add_to_cart_in, name='add_to_cart_in'),
    # path('add/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('detail/', views.cart_detail, name='cart_detail'),
    path('cart_address/', views.cart_address, name='cart_address'),
    path('cart_payment_method/<int:product_id>/', views.cart_payment_method, name='cart_payment_method'),
    path('cart_complate_buy/', views.cart_complate_buy, name='cart_complate_buy'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('remove_item', views.remove_item, name='remove_item'),
]
