from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self .cart = cart

    @property
    def item_count(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product):
        product_id = str(product.id)
        if product.inventory > 0:
            if product_id not in self.cart:
                self.cart[product_id] = {'product_id': product.id, 'quantity': 1, 'price': product.price, 'new_price': product.new_price, 'weight': product.weight, 'off': product.off}
            else:
                # if self.cart[product_id]['quantity'] < product.inventory + 1:
                self.cart[product_id]['quantity'] += 1

            product.inventory -= 1
            product.save()

            self.save()

    def decrease(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] > 1:
                self.cart[product_id]['quantity'] -= 1
                product.inventory += 1

            product.save()
            self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            product.inventory += self.cart[product_id]['quantity']
            del self.cart[product_id]
            product.save()

        self.save()

    def clear(self):
        del self.session['cart']
        self.session.modified = True
        self.save()

    def get_post_price(self):
        weight = sum(item['weight'] * item['quantity'] for item in self.cart.values())
        if weight <= 1000:
            return 20000
        elif 1000 <= weight < 2000:
            return 30000
        else:
            return 50000

    def get_total_price(self):
        price = sum(item['price'] * item['quantity'] for item in self.cart.values())
        return price

    def get_final_price(self):
        total_price = sum(item['new_price'] * item['quantity'] for item in self.cart.values())

        discount = self.session.get('discount_fixed', 0)

        return int(total_price - discount)
    # :
    #     return self.get_total_price()
    #     # + self.get_post_price()

    def get_off_price(self):
        off = sum(item['off'] * item['quantity'] for item in self.cart.values())
        return off

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_dict = self.cart.copy()
        for product in products:
            cart_dict[str(product.id)]['product'] = product
        for item in cart_dict.values():
            item['total'] = item['price'] * item['quantity']
            yield item

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True
