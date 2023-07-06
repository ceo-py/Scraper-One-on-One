from requests_html import HTML

file_path = "html_to_scrape/pizza_details.html"

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
    1: 'Сосове',
    2: 'Сирена',
    3: '',
    4: 'Меса',
    5: 'Зеленчуци',
    6: 'Подправки',
}


data_gather[pizza_title] = {x.attrs['alt']: {'Снимка големина': "https://www.dominos.bg" + x.attrs['src']} for x in sizes}


def get_dough_picture_and_size(item, item_pic, data):
    size = item.attrs['id'].split('_')[-1]

    for key in data.keys():
        if size in data[key]['Снимка големина']:
            data[key][item.attrs['title']] = {}
            data[key][item.attrs['title']]['Цена'] = item.attrs['price'].strip()
            data[key][item.attrs['title']]['Описание'] = item.attrs['description'].strip()
            data[key][item.attrs['title']]['Продукт Снимка'] = f"https://www.dominos.bg{item_pic.attrs['src']}"


for x in range(len(main_data)):
    get_dough_picture_and_size(main_data[x], dough_pic_url[x], data_gather[pizza_title])


data_gather[pizza_title]['Продукти'] = [x.text for x in products]
data_gather[pizza_title]['Продукт Снимка'] = pizza_picture

for key in data_gather:
    for key_l2 in data_gather[key]:
        print(key_l2)
        print(data_gather[key][key_l2])


for x in all_toppings_list:
    if x.attrs['t_type'] != 'hidden':
        print(f"{x.attrs['tname'].strip()} - {type_dict[int(x.attrs['t_type'].strip())]} {int(x.attrs['value'].strip())}")

print(product_price)

