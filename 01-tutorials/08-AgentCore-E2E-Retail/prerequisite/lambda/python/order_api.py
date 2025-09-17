import json
from datetime import datetime, timedelta


def check_order_status(order_id, customer_email=None):
    """Check order status and tracking information"""
    orders = {
        "ORD12345": {
            "customer_email": "customer@example.com",
            "status": "Shipped",
            "tracking_number": "1Z999AA1234567890",
            "carrier": "UPS",
            "order_date": "2024-01-15",
            "estimated_delivery": "2024-01-18",
            "items": [
                {"name": "Wireless Bluetooth Headphones", "quantity": 1, "price": 89.99}
            ],
            "total": 89.99,
            "shipping_address": "123 Main St, Anytown, ST 12345"
        },
        "ORD12346": {
            "customer_email": "shopper@example.com",
            "status": "Processing",
            "tracking_number": None,
            "carrier": None,
            "order_date": "2024-01-16",
            "estimated_delivery": "2024-01-20",
            "items": [
                {"name": "Gaming Laptop Pro", "quantity": 1, "price": 1299.99}
            ],
            "total": 1299.99,
            "shipping_address": "456 Oak Ave, Another City, ST 67890"
        },
        "ORD12347": {
            "customer_email": "buyer@example.com",
            "status": "Delivered",
            "tracking_number": "1Z999BB9876543210",
            "carrier": "FedEx",
            "order_date": "2024-01-10",
            "estimated_delivery": "2024-01-13",
            "delivery_date": "2024-01-13",
            "items": [
                {"name": "Smartphone Case", "quantity": 2, "price": 24.99}
            ],
            "total": 49.98,
            "shipping_address": "789 Pine Rd, Some City, ST 11111"
        }
    }
    
    order = orders.get(order_id.upper())
    if not order:
        return None
        
    # Email verification if provided
    if customer_email and order["customer_email"].lower() != customer_email.lower():
        return {"error": "Email address doesn't match our records for this order"}
        
    return order


def create_order(customer_email, items, shipping_address):
    """Create a new order (mock implementation)"""
    import random
    import string
    
    # Generate order ID
    order_id = "ORD" + "".join(random.choices(string.digits, k=5))
    
    # Calculate total
    total = sum(item.get("price", 0) * item.get("quantity", 1) for item in items)
    
    # Create order
    order = {
        "order_id": order_id,
        "customer_email": customer_email,
        "status": "Processing",
        "tracking_number": None,
        "carrier": None,
        "order_date": datetime.now().strftime("%Y-%m-%d"),
        "estimated_delivery": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
        "items": items,
        "total": total,
        "shipping_address": shipping_address
    }
    
    return order


def get_order_history(customer_email, limit=10):
    """Get order history for a customer (mock implementation)"""
    # Mock order history - in real implementation, this would query a database
    all_orders = [
        {
            "order_id": "ORD12345",
            "customer_email": "customer@example.com",
            "status": "Shipped",
            "order_date": "2024-01-15",
            "total": 89.99,
            "items_count": 1
        },
        {
            "order_id": "ORD12346", 
            "customer_email": "shopper@example.com",
            "status": "Processing",
            "order_date": "2024-01-16",
            "total": 1299.99,
            "items_count": 1
        },
        {
            "order_id": "ORD12347",
            "customer_email": "buyer@example.com", 
            "status": "Delivered",
            "order_date": "2024-01-10",
            "total": 49.98,
            "items_count": 2
        }
    ]
    
    # Filter by customer email
    customer_orders = [
        order for order in all_orders 
        if order["customer_email"].lower() == customer_email.lower()
    ]
    
    return customer_orders[:limit]


def cancel_order(order_id, customer_email, reason=None):
    """Cancel an order (mock implementation)"""
    # Check if order exists and belongs to customer
    order = check_order_status(order_id, customer_email)
    
    if not order:
        return {"error": "Order not found or doesn't belong to this customer"}
        
    if order.get("error"):
        return order
        
    # Check if order can be cancelled
    if order["status"] in ["Shipped", "Delivered"]:
        return {"error": f"Cannot cancel order with status: {order['status']}"}
        
    # Mock cancellation
    return {
        "order_id": order_id,
        "status": "Cancelled",
        "cancellation_date": datetime.now().strftime("%Y-%m-%d"),
        "reason": reason or "Customer request",
        "refund_amount": order["total"],
        "refund_timeline": "3-5 business days"
    }