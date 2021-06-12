from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category


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

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    paginator = Paginator(products, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    template = 'products/products.html'
    context = {
        'products': products,
        'current_categories': categories,
        'search_term': query,
        'page_obj': page_obj,
    }

    return render(request, template, context)
