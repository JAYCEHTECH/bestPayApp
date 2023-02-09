from django.shortcuts import redirect, render

from bestPayApp import models


def products(request):
    if models.Product.objects.filter(status=0):
        all_products = models.Product.objects.all()
        context = {'products': all_products}
        return render(request, 'shop/product/products.html', context=context)
    else:
        return render(request, 'shop/product/products.html')


def product_detail(request, product_name):
    if models.Product.objects.filter(name=product_name, status=0):
        product = models.Product.objects.filter(name=product_name).first()
        context = {'product': product}
        return render(request, 'shop/product/product-detail.html', context=context)












