from requests_html import HTMLSession, HTML

from json_details_page import create_pizza_json

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


def open_web_site(URL, timer=5):
    s = HTMLSession()
    r_html = s.get(URL)
    r_html.html.render(sleep=timer)

    return r_html.html


def only_html(html_content):
    return HTML(html=html_content)


def scrape_general_information(r_html):
    title = r_html.find('.menu-title')
    description = r_html.find('.menu-desc')
    tag_container = r_html.find('.menu-tag-container')
    images = r_html.find('.menu-img')

    for x in range(len(title)):

        title_text = title[x].text.strip().split('\n')[-1]
        print(title_text)

        if description:
            description_text = description[x].text.strip()
            print(description_text)

        images_link = images[x].attrs['style'].split('"')[1].strip()
        print(images_link)

        additional_info = HTML(html=tag_container[x].html).find('.menu-tag')

        print('\n'.join(
            [f"{x.attrs['data-original-title'].strip()} - {x.attrs['src'].strip()}" for x in additional_info]))

        print()


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


def scrape_product_details(r_html):
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
    price = float(r_html.find('.Price_Sum')[0].text)


    data_gather[pizza_title] = {x.attrs['alt']: {'Снимка големина': "https://www.dominos.bg" + x.attrs['src']} for x in
                                sizes}
    dough_info = []
    for x in range(len(main_data)):
        dough_info.append(get_dough_picture_and_size(main_data[x], dough_pic_url[x], data_gather[pizza_title]))

    show_details(data_gather, pizza_title, all_toppings_list, products, pizza_picture, product_price, dough_info,
                 all_toppings_list, price)


def toppings(all_toppings_list):
    data = ingredient()
    for x in all_toppings_list:
        if x.attrs['t_type'] != 'hidden':
            data[type_dict[int(x.attrs['t_type'].strip())]] += [x.attrs['tname'].strip()]
    return data


def show_details(data_gather, pizza_title, all_toppings_list, products, pizza_picture, product_price, dough_info,
                 toppings_data, price):
    data_gather[pizza_title]['Продукти'] = [x.text for x in products]
    data_gather[pizza_title]['Продукт Снимка'] = pizza_picture

    for key in data_gather:
        for key_l2 in data_gather[key]:
            print(key_l2)
            print(data_gather[key][key_l2])

    for x in all_toppings_list:
        if x.attrs['t_type'] != 'hidden':
            print(f"{x.attrs['tname'].strip()} - {type_dict[int(x.attrs['t_type'].strip())]}")

    print(product_price)
    print(toppings(toppings_data))
    create_pizza_json(
        product_name=pizza_title.strip(),
        product_picture=pizza_picture, dough_types=dough_info,
        ingredients=[x.text for x in products],
        ingredient_groups=toppings(toppings_data),
        price=price)

# scrape_general_information(open_web_site(URL))

# scrape_product_details(open_web_site(URL))
