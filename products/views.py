from django.shortcuts import render
from .models import Product, Category
from django.core.paginator import Paginator


def view_products(request):
    """ A view to display products """

    products = Product.objects.all()
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    paginator = Paginator(products, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    template = 'products/products.html'
    context = {
        'products': products,
        'current_categories': categories,
        'page_obj': page_obj,
    }

    return render(request, template, context)
