from django.shortcuts import render, get_object_or_404
from .models import Product

def products(request):
    pro = Product.objects.all()
    searchname = None
    searchdesc = None
    searchfrom = None
    searchto = None
    searchcheck = None
    if 'searchcheck' in request.GET:
        searchcheck = request.GET['searchcheck']
        if not searchcheck:
            searchcheck = 'off'

    if 'searchname' in request.GET:
        searchname = request.GET['searchname']
        if searchname:
            if searchcheck == 'on':
                pro = pro.filter(name__contains = searchname)
            else:
                pro = pro.filter(name__icontains = searchname)
    
    if 'searchdescription' in request.GET:
        searchdesc = request.GET['searchdescription']
        if searchdesc:
            if searchcheck == 'on':
                pro = pro.filter(description__contains = searchdesc)
            else:
                pro = pro.filter(description__icontains = searchdesc)
            

    if 'searchpricefrom' in request.GET and 'searchpriceto' in request.GET:
        searchfrom = request.GET['searchpricefrom']
        searchto = request.GET['searchpriceto']
        if searchfrom and searchto:
            if searchfrom.isdigit() and searchto.isdigit():
                pro = pro.filter(price__gte = searchfrom, price__lte = searchto)

    context = {
        'products': pro
    }
    return render(request, 'products/products.html', context)

def product(request, id_pro):
    context = {
        'product': get_object_or_404(Product, pk=id_pro)
    }
    return render(request, 'products/product.html', context)

def search(request):
    return render(request, 'products/search.html', {})

