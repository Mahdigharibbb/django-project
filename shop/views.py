from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Count
from .forms import *
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
# Create your views here.


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    products2 = Product.objects.order_by('?')[:5]
    products_clothing = Product.objects.filter(category__name__in=['شلوار', 'لباس', 'کفش'])
    products_likes = Product.objects.annotate(like_count=Count('likes')).filter(like_count__gt=0).order_by('-like_count')[:3]
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'products2': products2,
        'products_likes': products_likes,
        'products_clothing': products_clothing
    }
    return render(request, 'shop/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    products_similar = Product.objects.filter(category__name=product.category).exclude(id=product.id)
    comments = product.comments.filter(active=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 1)
    try:
        comments_page = paginator.page(page)
    except PageNotAnInteger:
        comments_page = paginator.page(1)
    except EmptyPage:
        return HttpResponse('')

    form = CommentForm()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'shop/list_ajax.html', {'comments': comments_page})
    context = {
        'product': product,
        'products_similar': products_similar,
        'form': form,
        'comments': comments_page,
    }
    return render(request, 'shop/detail.html', context)


@login_required
@require_POST
def like_post(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        if user in product.likes.all():
            product.likes.remove(user)
            liked = False
        else:
            product.likes.add(user)
            liked = True

        product.total_likes = product.likes.count()
        product_likes_count = product.total_likes
        product.save()

        response_data = {
            'liked': liked,
            'likes_count': product_likes_count,
        }
    else:
        response_data = {'error': 'Invalid post_id'}

    return JsonResponse(response_data)


def search(request):
    query = None
    categories = Category.objects.all()
    results = Product.objects.all()
    categories_clothing = categories.filter(name__in=['شلوار', 'لباس', 'کفش'])
    products_clothing = Product.objects.filter(category__name__in=['شلوار', 'لباس', 'کفش']).distinct()

    only_available = request.GET.get('available')
    min_price = int(request.GET.get('min_price', '0').replace(',', ''))
    max_price = int(request.GET.get('max_price', '5000000').replace(',', ''))
    selected_categories = request.GET.getlist('category')

    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results1 = results.annotate(similarity=TrigramSimilarity('name', query))\
                .filter(similarity__gt=0.15)
            results2 = results.annotate(similarity=TrigramSimilarity('description', query)) \
                .filter(similarity__gt=0.15)
            results3 = results.annotate(similarity=TrigramSimilarity('category__name', query)) \
                .filter(similarity__gt=0.15)
            results = (results1 | results2 | results3).order_by('-similarity')

    if only_available:
        results = results.filter(inventory__gt=0)

    if min_price and max_price:
        results = results.filter(new_price__gte=min_price, new_price__lte=max_price)

    if selected_categories:
        results = results.filter(category__name__in=selected_categories)
    if 'sort_by' in request.GET:
        sort_by = request.GET['sort_by']
        if sort_by == 'Most-Popular':
            results = results.order_by('-likes')
        elif sort_by == 'newest':
            results = results.order_by('-created')
        elif sort_by == 'cheapest':
            results = results.order_by('new_price')
        elif sort_by == 'most-expensive':
            results = results.order_by('-new_price')

    paginator = Paginator(results, 3)
    page_number = request.GET.get('page', 1)

    try:
        results = paginator.page(page_number)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        results = paginator.page(1)

    context = {
        'query': query,
        'results': results,
        'categories': categories,
        'categories_clothing': categories_clothing,
        'products_clothing': products_clothing,
        'only_available': only_available,
        'min_price': min_price,
        'max_price': max_price,
        'selected_categories': selected_categories,
        'sort_by': request.GET.get('sort_by', ''),
        'request': request,
    }

    return render(request, 'shop/search.html', context)


@require_http_methods(["GET", "POST"])
def product_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comment = None
    form = CommentForm(data=request.POST)
    referer = request.META.get('HTTP_REFERER', reverse('shop:product_list'))
    if request.method == "POST":
        form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.product = product
        comment.save()
        return redirect('shop:register_comment')
    context = {
        'product': product,
        'form': form,
        'comment': comment,
        'referer': referer
    }
    return render(request, "forms/comment.html", context)


def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(message=cd['message'], name=cd['name'], email=cd['email'],
                                  phone=cd['phone'], subject=cd['subject'])
            return redirect("shop:product_list")
    else:
        form = TicketForm()
    print(form.errors)
    return render(request, "forms/ticket.html", {'form': form})
