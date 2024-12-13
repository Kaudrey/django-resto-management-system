from django.shortcuts import render, redirect
from .forms import StaffMemberForm
from django.contrib.auth import authenticate,logout
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import StaffMember
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from reservations.models import CustomerReservation
from django.db.models import Sum, Count
from datetime import date
from django.db.models.functions import TruncDate
import json 

def admin_dashboard(request):
    # Get today's date
    today = date.today()

    # Fetch analytics data
    orders_today = Order.objects.filter(created_at__date=today).count()
    reservations_today = CustomerReservation.objects.filter(created_at__date=today).count()
    income_today = Order.objects.filter(created_at__date=today).aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Prepare data for the graph

    # Orders by date
    orders_by_date = (
        Order.objects.annotate(order_date=TruncDate('created_at'))  # Group by date, renamed annotation to avoid conflict
        .values('order_date')  # Extract the newly named 'order_date'
        .annotate(order_count=Count('id'))  # Count orders per date
        .order_by('order_date')  # Sort by 'order_date'
    )

    # Reservations by date
    reservations_by_date = (
        CustomerReservation.objects.annotate(reservation_date=TruncDate('created_at'))  # Group by date, renamed annotation
        .values('reservation_date')  # Extract the newly named 'reservation_date'
        .annotate(reservation_count=Count('id'))  # Count reservations per date
        .order_by('reservation_date')  # Sort by 'reservation_date'
    )

    # Ensure the data is JSON serializable (convert dates to strings)
    orders_by_date_serialized = [
        {'date': order['order_date'].strftime('%Y-%m-%d'), 'order_count': order['order_count']}
        for order in orders_by_date
    ]

    reservations_by_date_serialized = [
        {'date': reservation['reservation_date'].strftime('%Y-%m-%d'), 'reservation_count': reservation['reservation_count']}
        for reservation in reservations_by_date
    ]

    # Pass the data to the template
    return render(request, 'admin_dashboard/dashboard.html', {
        'orders_today': orders_today,
        'reservations_today': reservations_today,
        'income_today': income_today,
        'orders_by_date_json': json.dumps(orders_by_date_serialized),  # Safe JSON for JS
        'reservations_by_date_json': json.dumps(reservations_by_date_serialized),
    })




def add_staff_member(request):
    if request.method == 'POST':
        form = StaffMemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff member added successfully!")
            return redirect('view_staff')
    else:
        form = StaffMemberForm()
    return render(request, 'admin_dashboard/add_staff_member.html', {'form': form})

# @login_required
def view_staff(request):
    # if request.session.get('is_admin'):
    staff_members = StaffMember.objects.all()
    return render(request, 'admin_dashboard/view_staff_members.html', {'staff_members': staff_members})

# @login_required
def edit_staff_member(request, staff_id):
    staff = get_object_or_404(StaffMember, id=staff_id)
    
    if request.method == 'POST':
        form = StaffMemberForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff member updated successfully!")
            return redirect('view_staff')
        else:
            messages.error(request, "Error updating staff member. Please check the form.")
    else:
        form = StaffMemberForm(instance=staff)
    
    return render(request, 'admin_dashboard/edit_staff_member.html', {'form': form, 'staff': staff})

# Admin: Delete staff member
# @login_required
def delete_staff_member(request, staff_id):
    staff = get_object_or_404(StaffMember, id=staff_id)
    
    if request.method == 'POST':
        staff.delete()
        messages.success(request, "Staff member deleted successfully!")
        return redirect('view_staff')
    
    return render(request, 'admin_dashboard/delete_staff_member.html', {'staff': staff})



def admin_logout(request):
    logout(request)
    return redirect('/login')



