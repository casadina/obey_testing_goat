from django.shortcuts import render
from lists.forms import ExistingListItemForm, ItemForm
from lists.models import Item, List
from django.shortcuts import redirect


def home_page(request):
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=our_list)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=our_list, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(our_list)
    return render(request, "list.html", {"list": our_list, "form": form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        our_list = List.objects.create()
        form.save(for_list=our_list)
        return redirect(our_list)
    else:
        return render(request, "home.html", {"form": form})


def my_lists(request, email):
    return render(request, "my_lists.html")
