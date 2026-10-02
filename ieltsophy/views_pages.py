from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


def index(request):
    return render(request, 'index.html')


@method_decorator(login_required, name='dispatch')
class ProtectedView(TemplateView):
    pass