from django.db import migrations


IMAGE_URLS = {
    "Cheese Pizza": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=700&q=80",
    "Pepperoni Pizza": "https://images.unsplash.com/photo-1628840042765-356cda07f4ee?auto=format&fit=crop&w=700&q=80",
    "Margherita Pizza": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=700&q=80",
    "Red Sauce Pasta": "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?auto=format&fit=crop&w=700&q=80",
    "Creamy Pasta": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=700&q=80",
    "Classic Burger": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=700&q=80",
    "Double Burger": "https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=700&q=80",
    "Grilled Chicken Sandwich": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=700&q=80",
    "Veggie Burger": "https://images.unsplash.com/photo-1520072959219-c595dc870360?auto=format&fit=crop&w=700&q=80",
    "Chicken Biryani": "https://images.unsplash.com/photo-1563379091339-03246963d7d3?auto=format&fit=crop&w=700&q=80",
    "Mutton Biryani": "https://images.unsplash.com/photo-1633945274309-2c16c9682a8c?auto=format&fit=crop&w=700&q=80",
    "Veg Biryani": "https://images.unsplash.com/photo-1596797038530-2c107229654b?auto=format&fit=crop&w=700&q=80",
    "Butter Chicken": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=700&q=80",
    "Chicken Tikka Masala": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=700&q=80",
    "Paneer Tikka Masala": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=700&q=80",
    "Chicken Curry": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?auto=format&fit=crop&w=700&q=80",
}


def refresh_food_images(apps, schema_editor):
    FoodItem = apps.get_model("core", "FoodItem")
    for name, image_url in IMAGE_URLS.items():
        FoodItem.objects.filter(name=name).update(image_url=image_url)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_seed_food_items"),
    ]

    operations = [
        migrations.RunPython(refresh_food_images, migrations.RunPython.noop),
    ]
