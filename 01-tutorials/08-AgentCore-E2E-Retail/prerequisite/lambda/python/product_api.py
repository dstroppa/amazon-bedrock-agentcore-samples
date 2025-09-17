import json
from datetime import datetime


def search_products(query, category="all", max_results=5):
    """Search for products in the catalog"""
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

    return matching_products[:max_results]


def get_product_details(product_id):
    """Get detailed product information"""
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
    
    return product_details.get(product_id.upper())


def get_product_recommendations(customer_preference, budget_range="any"):
    """Get personalized product recommendations"""
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
        "audio": [
            {"id": "PROD001", "name": "Wireless Bluetooth Headphones", "price": 89.99, "reason": "High-quality audio with noise cancellation"},
            {"id": "PROD009", "name": "Wireless Earbuds", "price": 159.99, "reason": "Portable audio for on-the-go"},
            {"id": "PROD011", "name": "Bluetooth Speaker", "price": 119.99, "reason": "Room-filling sound for home"}
        ]
    }

    budget_filters = {
        "under_50": lambda price: price < 50,
        "50_200": lambda price: 50 <= price <= 200,
        "200_500": lambda price: 200 <= price <= 500,
        "over_500": lambda price: price > 500,
        "any": lambda price: True
    }

    preference_key = customer_preference.lower()
    recommendations = recommendations_db.get(preference_key, [])
    
    if not recommendations:
        # Default recommendations
        recommendations = [
            {"id": "PROD001", "name": "Wireless Bluetooth Headphones", "price": 89.99, "reason": "Popular choice with great reviews"},
            {"id": "PROD003", "name": "Smartphone Case", "price": 24.99, "reason": "Essential protection for your device"}
        ]

    # Apply budget filter
    budget_filter = budget_filters.get(budget_range, budget_filters["any"])
    filtered_recommendations = [r for r in recommendations if budget_filter(r["price"])]

    return filtered_recommendations[:3]