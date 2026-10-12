from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, RefundRequest


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'order_list.html', context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    refunds = RefundRequest.objects.filter(order=order)

    context = {
        'order': order,
        'refunds': refunds,
        'refund_request': refunds.first(),
    }
    return render(request, 'order_detail.html', context)