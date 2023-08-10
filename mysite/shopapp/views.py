from timeit import default_timer
from datetime import date
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def shop_index(request: HttpRequest):
    products = [
        ('laptop', 1999),
        ('desktop', 2999),
        ('smartphone', 999),
        ('monitor', 1200),
        ('printer', 1500),
    ]

    context = {
        "cur_date": date.today(),
        "time_running": default_timer(),
        "products": products,
        }

    return render(request, 'shopapp/shop-index.html', context=context)
