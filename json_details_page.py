import json

filename = "data/sandwich.json"

def write_json(data):
    with open(filename, "w", encoding='utf-8') as x:
        json.dump(data, x, ensure_ascii=False, indent=2)


def create_pizza_json(product_name, product_picture, dough_types, ingredients, ingredient_groups, price):
    with open(filename, "r+", encoding='utf-8') as json_file:
        data = json.load(json_file)
    pizza_data = {
        "product_name": product_name,
        "product_picture": product_picture,
        "price": price,
        "dough_types": dough_types,
        "ingredients": ingredients,
        "ingredient_groups": ingredient_groups
    }
    data += [pizza_data]
    write_json(data)


# # Example usage:
# product_name = "Deluxe Pizza"
# product_picture = "http://example.com/images/deluxe_pizza.jpg"
#
# dough_types = [
#     {
#         "type": "Regular",
#         "picture": "http://example.com/images/regular_dough.jpg",
#         "description": "Classic pizza dough made with high-quality flour",
#         "price": 9.99
#     },
#     {
#         "type": "Thin Crust",
#         "picture": "http://example.com/images/thin_crust_dough.jpg",
#         "description": "Thin and crispy crust for a lighter pizza experience",
#         "price": 10.99
#     },
#     {
#         "type": "Gluten-Free",
#         "picture": "http://example.com/images/gluten_free_dough.jpg",
#         "description": "Dough made without gluten, suitable for gluten-sensitive individuals",
#         "price": 12.99
#     }
# ]


# create_pizza_json(product_name='', product_picture='', dough_types='', ingredients='', ingredient_groups='')

'''
missing
ЧИК –ЧИ –РИК
Пеперони Класик
Шунка Класик
Пица Тон
Мастър Бургер пица
'''