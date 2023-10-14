from main import db,EatenItems,FoodItems

items = FoodItems.query.with_entities(FoodItems.item).all()
print(items)
a = [(item[0],item[0]) for item in items]
print(a)