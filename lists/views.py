from django.shortcuts import render
from lists.forms import ItemForm
from lists.models import Item, List
from django.shortcuts import redirect
from django.core.exceptions import ValidationError


def home_page(request):
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == "POST":
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST["text"], list=our_list)
            return redirect(our_list)
    return render(request, "list.html", {"list": our_list, "form": form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        our_list = List.objects.create()
        Item.objects.create(text=request.POST["text"], list=our_list)
        return redirect(f'/lists/{our_list.id}/')
    else:
        return render(request, "home.html", {"form": form})
