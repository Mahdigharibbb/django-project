from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('products/<int:id>/', views.product_detail, name='product_list_in_id'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('like_post', views.like_post, name="like_post"),
    path('search/', views.search, name="search"),
    path('product/<int:product_id>/comment', views.product_comment, name="product_comment"),
    path('register_comment/', TemplateView.as_view(template_name="forms/register_comment.html"), name="register_comment"),
    path('ticket', views.ticket, name="ticket"),

]
