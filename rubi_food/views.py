from django.shortcuts import render,HttpResponseRedirect,reverse
from django.http import JsonResponse
from .models import *
# Create your views here.
def OrdHistory(userid):
    # should return order number, food bought,qty and total
    order_list=Order.objects.filter(ordered_by=userid).order_by('-order_timestamp')
    history_dictionary={}
    cummulative_total=0
    x=0
    for order in order_list:
        cummulative_total+=order.get_order_amount()
        item=Food.objects.get(pk=order.foodid_id)
        single_order=[order.ORD_No,str(item.food_name),order.quantity,str(order.get_order_amount()),str(cummulative_total)]
        history_dictionary[x]=single_order
        x+=1
    return history_dictionary

def history(request):
    if request.user.is_authenticated():# user has to be logged in to view their history
        user=request.user
        return JsonResponse(OrdHistory(user.id))
def dash(request):
    # statistical crunching,clearing orders, setting up offers and discounts
    #some graphing
    cumm_cleared,cumm_pending=0,0
    pending_orders=Order.objects.filter(status="PENDING").order_by('-order_timestamp')
    for single in pending_orders:
        cumm_pending+=single.get_order_amount()
    cleared_orders = Order.objects.filter(status="CLEARED").order_by('-order_timestamp')
    for single in cleared_orders:
        cumm_cleared+=single.get_order_amount()

    carts=Cart.objects.all()
        # .order_by('cart_status')
    user_count=User.objects.count()
    context={
        "pending":pending_orders,
        "c_pending":cumm_pending,
        "cleared":cleared_orders,
        "c_cleared":cumm_cleared,
        "carts":carts,
        "user_count":user_count,
    }
    return render(request,'rubi_food/dashboard.html',context=context)

def clear_cart(request,id):
    # get cart number, update cart status to cleared.
    # explode cart_no and update order status to cleared.
    cart=Cart.objects.get(id=id)
    cart.clear_cart()
    return HttpResponseRedirect(reverse('rubi_food:dashboard'))
