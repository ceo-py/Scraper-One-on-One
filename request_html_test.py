from requests_html import HTMLSession, HTML

type_dict = {
    1: 'Сосове',
    2: 'Сирена',
    3: '',
    4: 'Меса',
    5: 'Зеленчуци',
    6: 'Подправки',
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

    for key in data.keys():
        if size in data[key]['Снимка големина']:
            data[key][item.attrs['title']] = {}
            data[key][item.attrs['title']]['Цена'] = item.attrs['price'].strip()
            data[key][item.attrs['title']]['Описание'] = item.attrs['description'].strip()
            data[key][item.attrs['title']]['Продукт Снимка'] = f"https://www.dominos.bg{item_pic.attrs['src']}"


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

    data_gather[pizza_title] = {x.attrs['alt']: {'Снимка големина': "https://www.dominos.bg" + x.attrs['src']} for x in
                                sizes}

    for x in range(len(main_data)):
        get_dough_picture_and_size(main_data[x], dough_pic_url[x], data_gather[pizza_title])

    show_details(data_gather, pizza_title, all_toppings_list, products, pizza_picture, product_price)


def show_details(data_gather, pizza_title, all_toppings_list, products, pizza_picture, product_price):
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


# scrape_general_information(open_web_site(URL))

# scrape_product_details(open_web_site(URL))
