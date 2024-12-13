from django.urls import path
from .views import  view_food_items,customer_food_items, add_food_item, edit_food_item,delete_food_item,admin_view_orders, place_order,customer_orders,edit_order,delete_order
urlpatterns = [
    # Common Views
    path('items/', view_food_items, name='view_food_items'),

    # Admin Views
    path('admin/add/',add_food_item, name='add_food_item'),
    path('admin/edit/<int:item_id>/', edit_food_item, name='edit_food_item'),
    path('admin/delete/<int:item_id>/', delete_food_item, name='delete_food_item'),
    path('admin/orders/', admin_view_orders, name='admin_view_orders'),

    # Customer Views
    path('all_items/',customer_food_items, name='customer_food_items'),
    path('order/', place_order, name='place_order'),
    path('customer/orders/', customer_orders, name='customer_orders'),
    path('customer/edit_order/<int:order_id>/', edit_order, name='edit_order'),
    path('customer/delete_order/<int:order_id>/', delete_order, name='delete_order'),
    ]
