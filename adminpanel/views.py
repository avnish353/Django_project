from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Order,  PaymentLog, Announcement
from .forms import MenuItemForm, AnnouncementForm
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.db.models.signals import post_save
from django.dispatch import receiver


def superuser_required(view_func):
    return user_passes_test(lambda user: user.is_superuser)(view_func)


def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("dashboard")

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect("dashboard") 
                else:
                    messages.error(request, "You do not have admin access.")
                    return redirect("admin-login")

        messages.error(request, "Invalid username or password.")

    return render(request, "admin_login.html", {"form": form})


@login_required
def dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "Only admin can access this page.")
        return redirect("admin-login") 
    
    orders = Order.objects.count()
    menu_count = MenuItem.objects.count()
    sales = PaymentLog.objects.count()
    users = Order.objects.values("customer").distinct().count()

    context = {
        "orders": orders,
        "menu_count": menu_count,
        "sales": sales,
        "users": users,
    }
    
    return render(request, "dashboard.html", context)



@superuser_required
def menu_items(request):
    items = MenuItem.objects.all()
    return render(request, "menu_list.html", {"items": items})


@superuser_required
def menu_add(request):
    form = MenuItemForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("menu-items")
    return render(request, "menu_form.html", {"form": form})


@superuser_required
def menu_edit(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    form = MenuItemForm(request.POST or None, request.FILES or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect("menu-items")
    return render(request, "menu_form.html", {"form": form})


@superuser_required
def menu_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    item.delete()
    return redirect("menu-items")


@superuser_required
def orders(request):
    orders = Order.objects.all().order_by("-timestamp")
    return render(request, "orders.html", {"orders": orders})



def update_order_status(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get("status")
        if new_status in ["Pending", "Preparing", "Ready", "Picked Up"]:
            order.status = new_status
            order.save()
    return redirect("orders")


@superuser_required
def payments(request):
    logs = PaymentLog.objects.all().order_by("-timestamp")
    return render(request, "payments.html", {"logs": logs})


@superuser_required
def announcements(request):
    form = AnnouncementForm(request.POST or None)
    msgs = Announcement.objects.all().order_by("-created_at")

    if form.is_valid():
        form.save()
        return redirect("annonuncements")

    return render(request, "announcements.html", {"form": form, "msgs": msgs})
