from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FoodItem, Order, OrderItem
from .forms import FoodItemForm
from customers.models import Customer
from django.contrib import messages
from django.conf import settings


# @login_required
def view_food_items(request):
    food_items = FoodItem.objects.all()
    return render(request, 'orders/view_food_items.html', {'food_items': food_items})

def customer_food_items(request):
    food_items = FoodItem.objects.all()
    return render(request, 'orders/customer_food_items.html', {'food_items': food_items})


# @login_required
def add_food_item(request):
    
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Food item added successfully!")
            return redirect('view_food_items')
    else:
        form = FoodItemForm()
    return render(request, 'orders/add_food_item.html', {'form': form})

# @login_required
def edit_food_item(request, item_id):
    # if not request.session.get('is_admin'):
        # return HttpResponseForbidden("You are not authorized to access this page.")
    
    food_item = get_object_or_404(FoodItem, id=item_id)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Food item updated successfully!")
            return redirect('view_food_items')
    else:
        form = FoodItemForm(instance=food_item)
    return render(request, 'orders/edit_food_item.html', {'form': form})

# @login_required
def delete_food_item(request, item_id):
    # if not request.session.get('is_admin'):
        # return HttpResponseForbidden("You are not authorized to access this page.")
    
    food_item = get_object_or_404(FoodItem, id=item_id)
    food_item.delete()
    messages.success(request, "Food item deleted successfully!")
    return redirect('view_food_items')

# @login_required
def admin_view_orders(request):

    # if not request.session.get('is_admin'):
        # return HttpResponseForbidden("You are not authorized to access this page.")
    
    orders = Order.objects.all()
    # print(orders.all())
    customers = {}
    for order in orders:
        # print(order.customer)
        customers[order.id] = order.customer
    
    print(customers.values())
    return render(request, 'orders/order_list.html', {'orders': orders})




# ---------- Customer Views ----------

# @login_required
def place_order(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity'))
        food_item = get_object_or_404(FoodItem, id=item_id)

        # Create new order
        order = Order.objects.create(customer=request.user, total_price=food_item.price * quantity)
        OrderItem.objects.create(order=order, food_item=food_item, quantity=quantity)
        messages.success(request, "Order placed successfully!")
        return redirect('customer_orders')

    food_items = FoodItem.objects.all() 
    return render(request, 'orders/customer_orders.html', {'food_items': food_items})

@login_required
def customer_orders(request):
    """Customer can view only their own orders."""
    orders = Order.objects.filter(customer_id=request.user.id)
    return render(request, 'orders/customer_orders.html', {'orders': orders})


@login_required
def edit_order(request, order_id):
    """Customer can edit their existing orders."""
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if quantity > 0:
            order_item = order.orderitem_set.first()
            order_item.quantity = quantity
            order_item.save()
            order.total_price = order_item.food_item.price * quantity
            order.save()
            messages.success(request, "Order updated successfully!")
        else:
            messages.error(request, "Quantity must be greater than zero.")
        return redirect('customer_orders')

    return render(request, 'orders/order_edit.html', {'order': order})

@login_required
def delete_order(request, order_id):

    order = get_object_or_404(Order, id=order_id, customer=request.user)
    order.delete()
    messages.success(request, "Order deleted successfully!")
    return redirect('/orders')
