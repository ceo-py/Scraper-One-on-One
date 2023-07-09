from requests_html import HTML

from json_details_page import create_pizza_json

file_path = "pizza_details.html"

with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

r_html = HTML(html=html_content)

### product main info
pizza_title = r_html.find('.decoration-title', first=True).text
pizza_picture = r_html.find('.product-img', first=True).attrs['style'].split('//')[-1][:-2]
data_gather = {pizza_title: {'product picture': pizza_picture}}
### product details
main_data = r_html.find('.col-md-4 input')[1:]
pic_url = r_html.find('.col-md-4 label img')[1:]
dough_pic_url = r_html.find('.col-md-4 img')[1:]
products = r_html.find('.toppings span')
sizes = r_html.find('.Sizes img')
### all toppings
all_toppings_category = r_html.find('.col-xs-12 h3')
del all_toppings_category[2]
del all_toppings_category[-1]
product_price = r_html.find('.product-total-price', first=True).text
all_toppings_list = r_html.find('.white-txt li .single-topping')
extra = r_html.find('.white-txt li .double input')

type_dict = {
    1: 'sauce',
    2: 'cheese',
    3: '',
    4: 'meats',
    5: 'vegetables',
    6: 'spices',
}


def ingredient():
    return {
        "spices": [],
        "meats": [],
        "vegetables": [],
        "cheese": [],
        "sauce": []
    }


data_gather[pizza_title] = {x.attrs['alt']: {'Снимка големина': "https://www.dominos.bg" + x.attrs['src']} for x in
                            sizes}


def get_dough_picture_and_size(item, item_pic, data):
    size = item.attrs['id'].split('_')[-1]
    return_data = []
    for key in data.keys():
        if size in data[key]['Снимка големина']:
            return_data.append({
                "type": key,
                "picture": f"https://www.dominos.bg{item_pic.attrs['src']}",
                "description": item.attrs['description'].strip(),
                "price": float(item.attrs['price'].strip())
            })

            return return_data


def get_dough():
    data = []
    for x in range(len(main_data)):
        data.append(get_dough_picture_and_size(main_data[x], dough_pic_url[x], data_gather[pizza_title]))
    return data


data_gather[pizza_title]['Продукти'] = [x.text for x in products]
data_gather[pizza_title]['Продукт Снимка'] = pizza_picture


def toppings():
    data = ingredient()
    for x in all_toppings_list:
        if x.attrs['t_type'] != 'hidden':
            data[type_dict[int(x.attrs['t_type'].strip())]] += [x.attrs['tname'].strip()]
    return data


def list_all_topings(data):
    return [value for sublist in data.values() for value in sublist]


def create_json():
    create_pizza_json(
        product_name=pizza_title.strip(),
        product_picture=pizza_picture, dough_types=get_dough(),
        ingredients=[x.text for x in products],
        ingredient_groups=toppings())


create_json()
