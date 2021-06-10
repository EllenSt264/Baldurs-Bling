from django.shortcuts import render


def view_products(request):
    """ A view to display products """

    return render(request, 'products/products.html')
