import boto3
from boto3.session import Session
import json
from datetime import datetime, timedelta
import random

from strands.tools import tool

# Model configuration
MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"

# System prompt for the shopping assistant
SYSTEM_PROMPT = """You are a helpful and friendly shopping assistant for an e-commerce platform.
Your role is to:
- Help customers find products they're looking for
- Provide detailed product information and recommendations
- Assist with order tracking and status updates
- Offer personalized suggestions based on customer preferences
- Be enthusiastic about helping customers make great purchasing decisions
- Always offer additional assistance after answering questions

You have access to the following tools:
1. search_products() - Search for products by keywords or category
2. get_product_details() - Get detailed information about specific products
3. check_order_status() - Check order status and tracking information
4. get_recommendations() - Get personalized product recommendations

Always use the appropriate tool to get accurate, up-to-date information rather than making assumptions about products, prices, or availability.

Be conversational and helpful, and always try to understand what the customer is really looking for to provide the best assistance."""

@tool
def search_products(query: str, category: str = "all", max_results: int = 5) -> str:
    """
    Search for products in the catalog by keywords, category, or features.

    Args:
        query: Search keywords (e.g., 'wireless headphones', 'gaming laptop')
        category: Product category filter (e.g., 'electronics', 'clothing', 'books', 'all')
        max_results: Maximum number of results to return (default: 5)

    Returns:
        Formatted list of matching products with basic information
    """
    # Mock product catalog - in real implementation, this would query a product database
    products = [
        {
            "id": "PROD001",
            "name": "Wireless Bluetooth Headphones",
            "category": "electronics",
            "price": 89.99,
            "rating": 4.5,
            "in_stock": True,
            "keywords": ["wireless", "bluetooth", "headphones", "audio"]
        },
        {
            "id": "PROD002", 
            "name": "Gaming Laptop Pro",
            "category": "electronics",
            "price": 1299.99,
            "rating": 4.8,
            "in_stock": True,
            "keywords": ["gaming", "laptop", "computer", "nvidia"]
        },
        {
            "id": "PROD003",
            "name": "Smartphone Case",
            "category": "electronics", 
            "price": 24.99,
            "rating": 4.2,
            "in_stock": True,
            "keywords": ["phone", "case", "protection", "smartphone"]
        },
        {
            "id": "PROD004",
            "name": "Running Shoes",
            "category": "clothing",
            "price": 129.99,
            "rating": 4.6,
            "in_stock": False,
            "keywords": ["shoes", "running", "athletic", "sports"]
        },
        {
            "id": "PROD005",
            "name": "Programming Book: Python Mastery",
            "category": "books",
            "price": 39.99,
            "rating": 4.7,
            "in_stock": True,
            "keywords": ["python", "programming", "book", "coding"]
        }
    ]

    # Filter by category
    if category.lower() != "all":
        products = [p for p in products if p["category"].lower() == category.lower()]

    # Search by keywords
    query_words = query.lower().split()
    matching_products = []
    
    for product in products:
        name_match = any(word in product["name"].lower() for word in query_words)
        keyword_match = any(word in product["keywords"] for word in query_words)
        
        if name_match or keyword_match:
            matching_products.append(product)

    # Limit results
    matching_products = matching_products[:max_results]

    if not matching_products:
        return f"No products found matching '{query}' in category '{category}'. Try different keywords or browse all categories."

    result = f"Found {len(matching_products)} products matching '{query}':\n\n"
    for product in matching_products:
        stock_status = "✅ In Stock" if product["in_stock"] else "❌ Out of Stock"
        result += f"• {product['name']} (ID: {product['id']})\n"
        result += f"  Price: ${product['price']:.2f} | Rating: {product['rating']}/5 | {stock_status}\n\n"

    return result

@tool
def get_product_details(product_id: str) -> str:
    """
    Get detailed information about a specific product including specifications, pricing, and availability.

    Args:
        product_id: Unique product identifier (e.g., 'PROD001')

    Returns:
        Detailed product information including specs, pricing, and availability
    """
    # Mock detailed product database
    product_details = {
        "PROD001": {
            "name": "Wireless Bluetooth Headphones",
            "price": 89.99,
            "category": "Electronics",
            "brand": "AudioTech",
            "rating": 4.5,
            "reviews_count": 1247,
            "in_stock": True,
            "stock_quantity": 45,
            "specifications": {
                "Battery Life": "30 hours",
                "Connectivity": "Bluetooth 5.0",
                "Weight": "250g",
                "Noise Cancellation": "Active"
            },
            "shipping": "Free shipping on orders over $50",
            "warranty": "1 year manufacturer warranty"
        },
        "PROD002": {
            "name": "Gaming Laptop Pro",
            "price": 1299.99,
            "category": "Electronics",
            "brand": "GameForce",
            "rating": 4.8,
            "reviews_count": 892,
            "in_stock": True,
            "stock_quantity": 12,
            "specifications": {
                "Processor": "Intel i7-12700H",
                "Graphics": "NVIDIA RTX 4060",
                "RAM": "16GB DDR4",
                "Storage": "512GB SSD",
                "Display": "15.6\" 144Hz"
            },
            "shipping": "Free shipping",
            "warranty": "2 year manufacturer warranty"
        },
        "PROD003": {
            "name": "Smartphone Case",
            "price": 24.99,
            "category": "Electronics",
            "brand": "ProtectPro",
            "rating": 4.2,
            "reviews_count": 2156,
            "in_stock": True,
            "stock_quantity": 234,
            "specifications": {
                "Material": "TPU + PC",
                "Drop Protection": "6 feet",
                "Compatibility": "iPhone 15 Pro",
                "Wireless Charging": "Compatible"
            },
            "shipping": "$3.99 shipping",
            "warranty": "90 day warranty"
        }
    }

    product = product_details.get(product_id.upper())
    if not product:
        return f"Product with ID '{product_id}' not found. Please check the product ID and try again."

    stock_status = f"✅ {product['stock_quantity']} in stock" if product['in_stock'] else "❌ Out of stock"
    
    result = f"**{product['name']}** (ID: {product_id})\n\n"
    result += f"💰 **Price:** ${product['price']:.2f}\n"
    result += f"⭐ **Rating:** {product['rating']}/5 ({product['reviews_count']} reviews)\n"
    result += f"📦 **Availability:** {stock_status}\n"
    result += f"🏷️ **Brand:** {product['brand']}\n\n"
    
    result += "**Specifications:**\n"
    for spec, value in product['specifications'].items():
        result += f"• {spec}: {value}\n"
    
    result += f"\n🚚 **Shipping:** {product['shipping']}\n"
    result += f"🛡️ **Warranty:** {product['warranty']}"

    return result

@tool
def check_order_status(order_id: str, customer_email: str = None) -> str:
    """
    Check the status and tracking information for a customer order.

    Args:
        order_id: Order number or ID (e.g., 'ORD12345')
        customer_email: Customer email for verification (optional)

    Returns:
        Order status, tracking information, and delivery estimates
    """
    # Mock order database
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
        }
    }

    order = orders.get(order_id.upper())
    if not order:
        return f"Order '{order_id}' not found. Please check your order number and try again."

    # Email verification if provided
    if customer_email and order["customer_email"].lower() != customer_email.lower():
        return "Email address doesn't match our records for this order. Please verify your email."

    result = f"**Order Status: {order['status']}** 📦\n\n"
    result += f"**Order ID:** {order_id}\n"
    result += f"**Order Date:** {order['order_date']}\n"
    result += f"**Total:** ${order['total']:.2f}\n\n"

    result += "**Items Ordered:**\n"
    for item in order['items']:
        result += f"• {item['name']} (Qty: {item['quantity']}) - ${item['price']:.2f}\n"

    result += f"\n**Shipping Address:** {order['shipping_address']}\n"
    result += f"**Estimated Delivery:** {order['estimated_delivery']}\n"

    if order['tracking_number']:
        result += f"**Tracking Number:** {order['tracking_number']}\n"
        result += f"**Carrier:** {order['carrier']}\n"
        result += "\n📍 You can track your package on the carrier's website using the tracking number above."
    else:
        result += "\n⏳ Your order is being prepared for shipment. Tracking information will be available soon."

    return result

@tool
def get_recommendations(customer_preference: str, budget_range: str = "any") -> str:
    """
    Get personalized product recommendations based on customer preferences and budget.

    Args:
        customer_preference: Customer interests or needs (e.g., 'gaming', 'fitness', 'productivity')
        budget_range: Budget preference ('under_50', '50_200', '200_500', 'over_500', 'any')

    Returns:
        List of recommended products with explanations
    """
    # Mock recommendation engine
    recommendations_db = {
        "gaming": [
            {"id": "PROD002", "name": "Gaming Laptop Pro", "price": 1299.99, "reason": "High-performance gaming with RTX graphics"},
            {"id": "PROD006", "name": "Gaming Mouse RGB", "price": 79.99, "reason": "Precision gaming with customizable RGB"},
            {"id": "PROD007", "name": "Mechanical Keyboard", "price": 149.99, "reason": "Tactile feedback for competitive gaming"}
        ],
        "fitness": [
            {"id": "PROD004", "name": "Running Shoes", "price": 129.99, "reason": "Comfortable support for daily runs"},
            {"id": "PROD008", "name": "Fitness Tracker", "price": 199.99, "reason": "Track workouts and health metrics"},
            {"id": "PROD009", "name": "Wireless Earbuds", "price": 159.99, "reason": "Sweat-resistant for workout sessions"}
        ],
        "productivity": [
            {"id": "PROD002", "name": "Gaming Laptop Pro", "price": 1299.99, "reason": "Powerful performance for work tasks"},
            {"id": "PROD005", "name": "Programming Book: Python Mastery", "price": 39.99, "reason": "Enhance coding skills"},
            {"id": "PROD010", "name": "Ergonomic Office Chair", "price": 299.99, "reason": "Comfortable for long work sessions"}
        ],
        "audio": [
            {"id": "PROD001", "name": "Wireless Bluetooth Headphones", "price": 89.99, "reason": "High-quality audio with noise cancellation"},
            {"id": "PROD009", "name": "Wireless Earbuds", "price": 159.99, "reason": "Portable audio for on-the-go"},
            {"id": "PROD011", "name": "Bluetooth Speaker", "price": 119.99, "reason": "Room-filling sound for home"}
        ]
    }

    # Budget filters
    budget_filters = {
        "under_50": lambda price: price < 50,
        "50_200": lambda price: 50 <= price <= 200,
        "200_500": lambda price: 200 <= price <= 500,
        "over_500": lambda price: price > 500,
        "any": lambda price: True
    }

    # Find matching recommendations
    preference_key = customer_preference.lower()
    recommendations = []
    
    # Check for exact match first
    if preference_key in recommendations_db:
        recommendations = recommendations_db[preference_key]
    else:
        # Check for partial matches
        for key, products in recommendations_db.items():
            if preference_key in key or key in preference_key:
                recommendations.extend(products)
                break

    if not recommendations:
        # Default recommendations
        recommendations = [
            {"id": "PROD001", "name": "Wireless Bluetooth Headphones", "price": 89.99, "reason": "Popular choice with great reviews"},
            {"id": "PROD003", "name": "Smartphone Case", "price": 24.99, "reason": "Essential protection for your device"}
        ]

    # Apply budget filter
    budget_filter = budget_filters.get(budget_range, budget_filters["any"])
    filtered_recommendations = [r for r in recommendations if budget_filter(r["price"])]

    if not filtered_recommendations:
        return f"No recommendations found for '{customer_preference}' within budget range '{budget_range}'. Try adjusting your budget or preferences."

    result = f"**Recommendations for '{customer_preference}'** 🎯\n\n"
    if budget_range != "any":
        result += f"*Filtered by budget: {budget_range.replace('_', ' ')}*\n\n"

    for i, rec in enumerate(filtered_recommendations[:3], 1):
        result += f"{i}. **{rec['name']}** (ID: {rec['id']})\n"
        result += f"   💰 ${rec['price']:.2f}\n"
        result += f"   💡 {rec['reason']}\n\n"

    result += "Would you like more details about any of these products?"
    return result