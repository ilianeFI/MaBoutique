from django.shortcuts import render
from django.views import View
# Create your views here.

class Hello(View):
    def get(self, request):
        return render(request,'base/home.html',{})