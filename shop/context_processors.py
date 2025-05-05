from shop.models import *
from cart.cart import Cart


def header_product(request):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'products': products,
        'category': category,
        'categories': categories,
    }
    return context


def cart(request):
    return {'cart': Cart(request)}
