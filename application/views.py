from django.shortcuts import render
from .models import Photo

# Create your views here.


def  index(request):
    return render(request , 'index.html')
def  navbar(request):
    return render(request , 'navbar.html')
def  footer(request):
    return render(request , 'footer.html')
def  login(request):
    return render(request , 'login.html')
def  signup(request):
    return render(request , 'signup.html')

def  photo(request):
    pictures = Photo.objects.all()
    ctx = {'pictures':pictures}
    return render(request , 'picture.html' , ctx)    
