from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse

from item.models import Category, Item

from .forms import SignupForm

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

def contact(request):
    return render(request, 'core/contact.html')

def about(request):
    return render(request, 'core/about.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })

def health_check(request):
    """
    Health check endpoint for Kubernetes liveness and readiness probes
    """
    return JsonResponse({'status': 'healthy'}, status=200)