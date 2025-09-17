from product_api import search_products, get_product_details, get_product_recommendations
from order_api import check_order_status, create_order, get_order_history, cancel_order


def get_named_parameter(event, name):
    if name not in event:
        return None
    return event.get(name)


def lambda_handler(event, context):
    print(f"Event: {event}")
    print(f"Context: {context}")

    extended_tool_name = context.client_context.custom["bedrockAgentCoreToolName"]
    resource = extended_tool_name.split("___")[1]

    print(resource)

    # Product API endpoints
    if resource == "search_products":
        query = get_named_parameter(event=event, name="query")
        category = get_named_parameter(event=event, name="category") or "all"
        max_results = get_named_parameter(event=event, name="max_results") or 5

        if not query:
            return {
                "statusCode": 400,
                "body": "❌ Please provide search query",
            }

        try:
            products = search_products(
                query=query, category=category, max_results=int(max_results)
            )
            
            if not products:
                return {
                    "statusCode": 200,
                    "body": f"No products found matching '{query}' in category '{category}'",
                }
                
            result = f"Found {len(products)} products:\\n"
            for product in products:
                stock_status = "✅ In Stock" if product["in_stock"] else "❌ Out of Stock"
                result += f"• {product['name']} (ID: {product['id']}) - ${product['price']:.2f} | {stock_status}\\n"
                
        except Exception as e:
            print(e)
            return {
                "statusCode": 400,
                "body": f"❌ {e}",
            }

        return {
            "statusCode": 200,
            "body": result,
        }

    elif resource == "get_product_details":
        product_id = get_named_parameter(event=event, name="product_id")

        if not product_id:
            return {
                "statusCode": 400,
                "body": "❌ Please provide product_id",
            }

        try:
            product = get_product_details(product_id=product_id)
            
            if not product:
                return {
                    "statusCode": 404,
                    "body": f"❌ Product with ID '{product_id}' not found",
                }
                
            stock_status = f"✅ {product['stock_quantity']} in stock" if product['in_stock'] else "❌ Out of stock"
            
            result = f"**{product['name']}** (ID: {product_id})\\n"
            result += f"💰 Price: ${product['price']:.2f}\\n"
            result += f"⭐ Rating: {product['rating']}/5 ({product['reviews_count']} reviews)\\n"
            result += f"📦 Availability: {stock_status}\\n"
            result += f"🏷️ Brand: {product['brand']}\\n\\n"
            result += "Specifications:\\n"
            for spec, value in product['specifications'].items():
                result += f"• {spec}: {value}\\n"
            result += f"\\n🚚 Shipping: {product['shipping']}\\n"
            result += f"🛡️ Warranty: {product['warranty']}"
                
        except Exception as e:
            print(e)
            return {
                "statusCode": 400,
                "body": f"❌ {e}",
            }

        return {
            "statusCode": 200,
            "body": result,
        }

    elif resource == "get_recommendations":
        customer_preference = get_named_parameter(event=event, name="customer_preference")
        budget_range = get_named_parameter(event=event, name="budget_range") or "any"

        if not customer_preference:
            return {
                "statusCode": 400,
                "body": "❌ Please provide customer_preference",
            }

        try:
            recommendations = get_product_recommendations(
                customer_preference=customer_preference, budget_range=budget_range
            )
            
            if not recommendations:
                return {
                    "statusCode": 200,
                    "body": f"No recommendations found for '{customer_preference}' within budget '{budget_range}'",
                }
                
            result = f"🎯 Recommendations for '{customer_preference}':\\n\\n"
            for i, rec in enumerate(recommendations, 1):
                result += f"{i}. {rec['name']} (ID: {rec['id']}) - ${rec['price']:.2f}\\n"
                result += f"   💡 {rec['reason']}\\n\\n"
                
        except Exception as e:
            print(e)
            return {
                "statusCode": 400,
                "body": f"❌ {e}",
            }

        return {
            "statusCode": 200,
            "body": result,
        }

    # Order API endpoints
    elif resource == "check_order_status":
        order_id = get_named_parameter(event=event, name="order_id")
        customer_email = get_named_parameter(event=event, name="customer_email")

        if not order_id:
            return {
                "statusCode": 400,
                "body": "❌ Please provide order_id",
            }

        try:
            order = check_order_status(order_id=order_id, customer_email=customer_email)
            
            if not order:
                return {
                    "statusCode": 404,
                    "body": f"❌ Order '{order_id}' not found",
                }
                
            if order.get("error"):
                return {
                    "statusCode": 400,
                    "body": f"❌ {order['error']}",
                }
                
            result = f"📦 Order Status: {order['status']}\\n\\n"
            result += f"Order ID: {order_id}\\n"
            result += f"Order Date: {order['order_date']}\\n"
            result += f"Total: ${order['total']:.2f}\\n\\n"
            result += "Items:\\n"
            for item in order['items']:
                result += f"• {item['name']} (Qty: {item['quantity']}) - ${item['price']:.2f}\\n"
            result += f"\\nShipping Address: {order['shipping_address']}\\n"
            result += f"Estimated Delivery: {order['estimated_delivery']}\\n"
            
            if order.get('delivery_date'):
                result += f"Delivered: {order['delivery_date']}\\n"
            elif order['tracking_number']:
                result += f"Tracking: {order['tracking_number']} ({order['carrier']})"
            else:
                result += "Tracking info will be available soon"
                
        except Exception as e:
            print(e)
            return {
                "statusCode": 400,
                "body": f"❌ {e}",
            }

        return {
            "statusCode": 200,
            "body": result,
        }

    elif resource == "get_order_history":
        customer_email = get_named_parameter(event=event, name="customer_email")
        limit = get_named_parameter(event=event, name="limit") or 10

        if not customer_email:
            return {
                "statusCode": 400,
                "body": "❌ Please provide customer_email",
            }

        try:
            orders = get_order_history(customer_email=customer_email, limit=int(limit))
            
            if not orders:
                return {
                    "statusCode": 200,
                    "body": f"No order history found for {customer_email}",
                }
                
            result = f"📋 Order History for {customer_email}:\\n\\n"
            for order in orders:
                result += f"• {order['order_id']} - {order['status']} - ${order['total']:.2f} ({order['order_date']})\\n"
                
        except Exception as e:
            print(e)
            return {
                "statusCode": 400,
                "body": f"❌ {e}",
            }

        return {
            "statusCode": 200,
            "body": result,
        }

    return {
        "statusCode": 400,
        "body": f"❌ Unknown toolname: {resource}",
    }