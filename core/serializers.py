def serialize_food(food):
    return {
        "id": food.id,
        "name": food.name,
        "description": food.description,
        "category": food.category,
        "price": float(food.price),
        "image_url": food.image_url,
        "is_available": food.is_available,
    }


def serialize_order(order):
    return {
        "id": order.id,
        "customer": order.user.get_full_name() or order.user.username,
        "status": order.status,
        "total_amount": float(order.total_amount),
        "delivery_address": order.delivery_address,
        "created_at": order.created_at.isoformat(),
        "items": [
            {
                "food": item.food_item.name,
                "quantity": item.quantity,
                "price": float(item.price),
                "subtotal": float(item.subtotal),
            }
            for item in order.items.select_related("food_item")
        ],
    }
