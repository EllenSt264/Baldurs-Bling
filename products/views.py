from django.shortcuts import render
from .models import Product, Category
from django.db.models import Q


def view_products(request):
    """ A view to display products """

    products = Product.objects.all()
    categories = None
    query = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    template = 'products/products.html'
    context = {
        'products': products,
        'current_categories': categories,
    }

    return render(request, template, context)
