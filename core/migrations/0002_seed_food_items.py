from django.db import migrations


MENU_ITEMS = [
    ("Cheese Pizza", "Fresh cheese pizza with toppings", "Pizza", "199.00", "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38"),
    ("Pepperoni Pizza", "Spicy pepperoni with cheese", "Pizza", "249.00", "https://images.unsplash.com/photo-1628840042765-356cda07f4ee"),
    ("Margherita Pizza", "Tomato, mozzarella and basil", "Pizza", "229.00", "https://images.unsplash.com/photo-1621996346565-411f89d04017"),
    ("Red Sauce Pasta", "Pasta in rich tomato sauce", "Pasta", "179.00", "https://images.unsplash.com/photo-1628294895950-9805252327bc"),
    ("Creamy Pasta", "White sauce with mushrooms", "Pasta", "189.00", "https://images.unsplash.com/photo-1612874742237-6526221fcf6f"),
    ("Classic Burger", "Cheesy burger with crispy patty", "Burger", "149.00", "https://images.unsplash.com/photo-1568901346375-23c9450c58cd"),
    ("Double Burger", "Double patty with extra cheese", "Burger", "199.00", "https://images.unsplash.com/photo-1550547990-87bcde18ba5e"),
    ("Grilled Chicken Sandwich", "Tender grilled chicken breast", "Other", "159.00", "https://images.unsplash.com/photo-1553979459-d2229ba7433b"),
    ("Veggie Burger", "Fresh vegetable patty with greens", "Burger", "129.00", "https://images.unsplash.com/photo-1562547256-d3ecad21a4e5"),
    ("Chicken Biryani", "Fragrant rice with tender chicken", "Biryani", "220.00", "https://images.unsplash.com/photo-1625938359305-2fedbf1a0da4"),
    ("Mutton Biryani", "Spicy biryani with tender mutton", "Biryani", "250.00", "https://images.unsplash.com/photo-1596040424166-b84c0d206410"),
    ("Veg Biryani", "Rice with mixed vegetables", "Biryani", "180.00", "https://images.unsplash.com/photo-1618184479302-1e8e6e773b72"),
    ("Butter Chicken", "Tender chicken in creamy sauce", "Indian", "210.00", "https://images.unsplash.com/photo-1601050690597-df0568f70950"),
    ("Chicken Tikka Masala", "Grilled chicken in spiced sauce", "Indian", "215.00", "https://images.unsplash.com/photo-1626082927389-6cd097cfd330"),
    ("Paneer Tikka Masala", "Cottage cheese in creamy sauce", "Indian", "195.00", "https://images.unsplash.com/photo-1625938359305-2fedbf1a0da4"),
    ("Chicken Curry", "Spiced chicken with rice", "Indian", "190.00", "https://images.unsplash.com/photo-1596040424166-b84c0d206410"),
]


def seed_food_items(apps, schema_editor):
    FoodItem = apps.get_model("core", "FoodItem")
    for name, description, category, price, image_url in MENU_ITEMS:
        FoodItem.objects.get_or_create(
            name=name,
            defaults={
                "description": description,
                "category": category,
                "price": price,
                "image_url": image_url,
                "is_available": True,
            },
        )


def remove_seed_food_items(apps, schema_editor):
    FoodItem = apps.get_model("core", "FoodItem")
    FoodItem.objects.filter(name__in=[item[0] for item in MENU_ITEMS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_food_items, remove_seed_food_items),
    ]
