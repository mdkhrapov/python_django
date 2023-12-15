from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


# Create your views here.
class StartIndex(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'start_index/start_index.html')