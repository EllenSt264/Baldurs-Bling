from django.shortcuts import render


def home(request):
    """ A view to render the homepage """
    return render(request, 'home/index.html')
