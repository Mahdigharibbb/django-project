from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.decorators.http import require_POST
from shop.models import Product, DiscountCode
from .cart import Cart
from orders.forms import OrderCreateForm
from orders.models import Order, OrderItem
from django.http import JsonResponse
from django.contrib import messages
from account.models import Address
from account.forms import AddressForm
from django.utils import timezone
# Create your views here.


@require_POST
def add_to_cart_in(request, product_id):
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product)
        cart = request.session.get('cart', {})
        context = {
            'item_count': len(cart),
            'total_price': cart.get_total_price()
        }
        request.session['cart'] = cart
        return JsonResponse(context)
    except:
        return redirect(request.META.get('HTTP_REFERER'))


def cart_detail(request):
    cart = Cart(request)
    total_items = sum(item['quantity'] for item in cart.cart.values())
    return render(request, 'cart/detail.html', {'cart': cart, 'item_count': total_items})


def update_quantity(request):
    item_id = request.POST.get('item_id')
    action = request.POST.get('action')
    try:
        product = get_object_or_404(Product, id=item_id)
        cart = Cart(request)
        if action == 'add':
            cart.add(product)
        if action == 'decrease':
            cart.decrease(product)

        total_items = sum(item['quantity'] for item in cart.cart.values())

        context = {
            'item_count': total_items,
            'total_price': cart.get_total_price(),
            'quantity': cart.cart[item_id]['quantity'],
            'total': cart.cart[item_id]['quantity'] * cart.cart[item_id]['price'],
            'final_price': cart.get_final_price(),
            "off_price": cart.get_off_price(),
            'success': True
        }
        return JsonResponse(context)
    except:
        return JsonResponse({'success': False, 'error': 'item not found'})


def remove_item(request):
    item_id = request.POST.get('item_id')
    try:
        product = get_object_or_404(Product, id=item_id)
        cart = Cart(request)
        cart.remove(product)

        context = {
            'item_count': len(cart),
            'total_price': cart.get_total_price(),
            'final_price': cart.get_final_price(),
            'quantity': cart.cart[item_id]['quantity'],
            'total': cart.cart[item_id]['quantity'] * cart.cart[item_id]['price'],
            'off_price': cart.get_off_price(),
            'success': True

        }
        return JsonResponse(context)
    except:
        return JsonResponse({'success': False, 'error': 'item not found'})


def cart_address(request):
    addresses = Address.objects.filter(user=request.user)
    default_address = addresses.filter(is_default=True).first()
    cart = request.session.get('cart', {})
    product_ids = list(cart.keys())

    product = Product.objects.filter(id__in=product_ids).first() if product_ids else None

    if request.method == "POST":
        address_id = request.POST.get("address_id")

        if address_id:
            address = get_object_or_404(Address, id=address_id, user=request.user)
            form = AddressForm(request.POST, instance=address)
            form.set_user(request.user)
        else:
            form = AddressForm(request.POST)
            form.instance.user = request.user

        if form.is_valid():
            form.save()  # ذخیره آدرس
            if address_id:
                messages.success(request, "آدرس با موفقیت ویرایش شد!")
            else:
                messages.success(request, "آدرس با موفقیت ثبت شد!")
            # if product:
            #     return redirect(reverse('cart:cart_payment_method', kwargs={'product_id': product.id}))
            # else:
            #     messages.error(request, "سبد خرید شما خالی است!")
            #     return redirect('cart:cart_address')
        else:
            messages.error(request, "مشکلی در ذخیره آدرس وجود دارد. لطفاً فرم را بررسی کنید.")
            print(form.errors)

    else:
        form = AddressForm()
    context = {
        'addresses': addresses,
        'default_address': default_address,
        'form': form,
        'cart_products': Product.objects.filter(id__in=product_ids)
    }
    return render(request, 'cart/cart_address.html', context)


def cart_payment_method(request, product_id):
    cart = Cart(request)
    cart_items = [Product.objects.get(id=int(item_id)) for item_id in cart.cart.keys()]
    product = get_object_or_404(Product, id=product_id)
    product_data = [{'id': product.id, 'name': product.name, 'price': product.new_price} for product in cart_items]
    addresses = Address.objects.filter(user=request.user)
    default_address = addresses.filter(is_default=True).first()
    total_price_before_discount = cart.get_total_price()
    total_discount = 0

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        payment_method = request.POST.get('payment_method')
        address_id = request.POST.get('address_id')
        if address_id:
            address = get_object_or_404(Address, id=address_id, user=request.user)
        else:
            address = Address.objects.filter(user=request.user, is_default=True).first()
        if form.is_valid():
            print("✅ فرم معتبر بود")
            order = form.save(commit=False)
            order.buyer = request.user
            order.address = address
            order.payment_method = payment_method
            order.discount_amount = request.session.get('discount_amount', 0)
            order.final_price = request.session.get('final_price', cart.get_total_price())
            if order.final_price == cart.get_total_price():
                order.final_price = cart.get_total_price()
            order.paid = False
            order.save()
            discounted_product_id = request.session.get('discounted_product_id')
            discount_per_unit = request.session.get('discount_per_unit', 0)
            for item_id, item_data in cart.cart.items():
                print(item_data)
                if isinstance(item_data, dict) and 'product_id' in item_data:
                    try:
                        product = Product.objects.get(id=item_data['product_id'])
                        unit_price = item_data['new_price']

                        if str(product.id) == str(discounted_product_id):
                            unit_price = max(unit_price - discount_per_unit, 0)
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            price=unit_price,
                            quantity=item_data['quantity'],
                            weight=item_data['weight']
                        )
                    except Product.DoesNotExist:
                        print(f"❌ محصول با شناسه {item_data['product_id']} پیدا نشد.")
            cart.clear()
            del request.session['cart']
            request.session['order_id'] = order.id
            request.session.pop('discount_amount', None)
            request.session.pop('final_price', None)
            return redirect('cart:cart_complate_buy')
    else:
        form = OrderCreateForm()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        code = request.GET.get('code', '').strip().lower()

        if code:
            try:
                discount = DiscountCode.objects.get(code=code, active=True)
                valid_products = [product for product in cart_items if product == discount.product]

                if not valid_products:
                    return JsonResponse(
                        {'success': False, 'message': '❌ این کد تخفیف برای هیچ‌کدام از محصولات سبد خرید معتبر نیست.'})

                if discount.expiry_date and discount.expiry_date < timezone.now():
                    return JsonResponse({'success': False, 'message': 'کد تخفیف منقضی شده است.'})

                for item in valid_products:
                    quantity = cart.cart[str(item.id)]["quantity"]
                    discount_amount = discount.discount_amount * quantity
                    total_discount += discount_amount
                total_price_before_discount = sum(
                    product.new_price * cart.cart[str(product.id)]["quantity"] for product in cart_items
                )

                final_price = max(total_price_before_discount - total_discount, 0)
                request.session['discount_amount'] = total_discount
                request.session['final_price'] = final_price
                request.session['discounted_product_id'] = valid_products[0].id
                request.session['discount_per_unit'] = discount.discount_amount
                request.session.modified = True

                return JsonResponse({
                    'success': True,
                    'discount_amount': total_discount,
                    'final_price': final_price,
                    'original_price': total_price_before_discount,
                    'product_id': valid_products[0].id,
                    'product_name': valid_products[0].name,
                    'product_price': valid_products[0].new_price,
                })
            except DiscountCode.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'کد تخفیف نامعتبر است.'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'خطای غیرمنتظره: {str(e)}'})
        else:
            return JsonResponse({'success': False, 'message': 'کد تخفیف را وارد کنید.'})

    if 'final_price' in request.session:
        discount_amount = request.session.get('discount_amount', 0)
        final_price = request.session.get('final_price', cart.get_final_price())
    else:
        final_price = total_price_before_discount
        discount_amount = 0

    context = {
        'product': product,
        'discount_amount': discount_amount,
        'form': form,
        'cart': cart,
        'addresses': addresses,
        'default_address': default_address,
        'final_price': final_price,
        'total_discount': total_discount,
        'product_data': product_data
    }
    return render(request, 'cart/cart_payment_method.html', context)


def cart_complate_buy(request):
    return render(request, 'cart/cart_complate_buy.html')



