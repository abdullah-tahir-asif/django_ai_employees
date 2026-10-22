from django.utils import timezone

from orders.models import Order, RefundRequest
from . tracking_data import DELIVERY_DATA

def get_order_details(order_id):
    try:
        order = Order.objects.get(id=order_id)
        return {
            'id': order.id,
            'product_name': order.product_name,
            'amount': str(order.amount),
            'status': order.status,
            'carrier': order.carrier,
            'tracking_number': order.tracking_number,
            'delivery_address': order.delivery,
            'ordered_on': order.created_at.strftime('%d %b %Y'),
            'days_since_ordered': (timezone.now() - order.created_at).days,
        }
    except Order.DoesNotExist:
        return {"error": f"Order # {order_id} not found."}




def get_refund_history(order_id):
    refunds = RefundRequest.objects.filter(id=order_id).order_by('-created_at')
    history = []
    for refund in refunds:
        history.append({
            "order_id": refund.order.id,
            "product": refund.order.product_name,
            "reason": refund.reason,
            "status": refund.status,
            "requested_on": refund.created_at.strftime("%d %b %Y"),
        })

    return {
        "total_refund_requests": len(history),
        "history": history
    }


def check_delivery_status(tracking_number, carrier):
    default_response = {
        "status": "Unknown",
        "last_location": "Tracking info unavailable",
        "last_update": "N/A",
        "estimated_delivery": "contact carrier directly",
        "delay_reason": "No updates from carrier",
    }
    delivery_info = DELIVERY_DATA.get(tracking_number, default_response)

    result =DELIVERY_DATA.get(tracking_number, default_response)
    result['carrier'] = carrier
    result['tracking_number'] = tracking_number
    return result