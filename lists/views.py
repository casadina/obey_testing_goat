from django.shortcuts import render
from lists.forms import ExistingListItemForm, ItemForm
from lists.models import List
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()


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
        list_ = List()
        if request.user.is_authenticated:
            list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, "home.html", {"form": form})


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, "my_lists.html", {'owner': owner})
