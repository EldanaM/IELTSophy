from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from ..models import UserProfile


def register(request):
    if request.method == 'POST':
        form =UserCreationForm(request.POST)
        if form.is_valid():
            user =form.save()
            UserProfile.objects.get_or_create(user=user)
            return redirect('login')
    else:
        form =UserCreationForm()
    return render(request, 'register.html', {'form': form})