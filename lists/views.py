from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from textwrap import dedent

from lists.models import Item, List
from lists.forms import ItemForm
from django.contrib.auth import get_user_model
User = get_user_model()


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    item = Item(list=list_)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(instance=item, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)

    return render(request, 'list.html', {'list': list_, 'form': form})


def new_list(request):
    list_ = List.objects.create()
    item = Item(list=list_)
    form = ItemForm(instance=item, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(list_)
    else:
        list_.delete()
        return render(request, 'home.html', {'form': form})


def my_lists(request, user_email):
    owner = User.objects.get(email=user_email)
    return render(request, 'my_lists.html', {'owner': owner})
