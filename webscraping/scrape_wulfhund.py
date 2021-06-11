"""
* Attribution:

* To fix UnicodeEncodeError when writing to JSON file:
'https://stackoverflow.com/questions/44391671/python3-unicodeencodeerror-charmap-codec-cant-encode-characters-in-position'

"""

import re
import requests
from bs4 import BeautifulSoup

product_skus = [] 
product_prices = []
product_names = []
product_links = []
product_images = []
product_image_names = []
product_sizes = []
product_descriptions = []

product_count = 0

all_lists = [
    product_skus, product_prices,
    product_names, product_links,
    product_images, product_image_names,
    product_sizes, product_descriptions
]


def get_product_information():
    """ Get product information functions """

    for products in soup.select('.products-list .product-inn'):

        def get_catalogue_num():
            """ Get product catalogue number for sku """
            for product in products.select('.product-section.product-details'):
                for item in product.select('span', {'class': 'value'})[1]:
                    product_sku = item
                    product_skus.append(product_sku)

        def get_product_name_and_link():
            """ Get product name """
            for product in products.select('h3', {'class': 'product-title'}):
                product_name = product.text
                if '"' in product_name:
                    product_name = product_name.replace('"', '')
                regex = re.compile(r"[\n\r\t]")
                text = regex.sub(" ", product_name)
                product_names.append(text)

            """ Get product link """
            for a in product.select('a'):
                link = a.attrs['href']
                product_link = f'https://www.wulflund.com/{link}'
                product_links.append(product_link)

        get_catalogue_num()
        get_product_name_and_link()

    def individual_products_page():
        url_list = product_links

        for url in url_list:
            source = requests.get(url)
            soup = BeautifulSoup(source.text, 'html.parser')

            def get_product_price():
                """ Get product price """
                for product in soup.select('.price'):
                    price = product.text
                    regex = re.compile(r"[\n\r\t]")
                    product_price = regex.sub("", price)
                    product_price = product_price.replace(
                        '£', '').replace('€', '').replace(
                            '$', '').replace(',', '.').replace(' ', '')
                    product_prices.append(product_price)

            def get_product_images():
                """ Get product images """
                images = []
                image_names = []
                if soup.select('.product-images'):
                    for product in soup.select('.product-images'):
                        for img in product.findAll('img'):
                            img = img['src']

                            img_name = img.split('/')
                            for i in range(len(img_name)):
                                if i == len(img_name) - 1:
                                    image_names.append(img_name[i])

                            image = f'https:{img}'
                            images.append(image)
                else:
                    for product in soup.select('.img-wrap'):
                        for img in product.select('img'):
                            img = img['src']

                            img_name = img.split('/')
                            for i in range(len(img_name)):
                                if i == len(img_name) - 1:
                                    image_names.append(img_name[i])

                            image = f'https:{img}'
                            images.append(image)

                product_images.append(images)
                product_image_names.append(image_names)

            def get_product_sizes():
                """ Get product sizes """
                sizes = []
                if soup.select('.custom-select'):
                    for product in soup.select('form', {'class': 'koupit'}):
                        for i in product.select('fieldset', {'class': 'xsmall-mb-15'}):
                            for li in i.select('.custom-select option'):
                                options = [i for i in li]
                                if 'Choose' not in options:
                                    for x in options:
                                        regex = re.compile(r"[\n\r\t]")
                                        text = regex.sub(" ", x)
                                        text = text.replace(' ', '').replace('\xa0€', '').replace(',','.')
                                        sizes.append(text)
                else:                               
                    sizes.append('no sizes')

                product_sizes.append(sizes)

            def get_product_description():
                """ Get product description """
                if soup.select('#prod-tab-description'):
                    for product in soup.select('#prod-tab-description'):
                        for desc in product.select('.product-description'):
                            description = desc.text
                            if '"' in description:
                                description = description.replace('"', '')
                            regex = re.compile(r"[\n\r\t]")
                            text = regex.sub(" ", description)
                            product_descriptions.append(text)
                else:
                    product_descriptions.append('no desc')

            get_product_price()
            get_product_images()
            get_product_sizes()
            get_product_description()

    individual_products_page()


def reset_lists():
    global product_count
    if any(all_lists):
        for lis in all_lists:
            lis.clear()


def stringfy_list(mylist):
    mylist = str(mylist)
    mylist = mylist.replace("[", "").replace("]", "").replace("'", "")

    return mylist


def scrape_rings():
    global page_num
    global soup
    global product_count

    page_attrs = '?strana='
    page_num = 1
    all_pages = []

    """ Silver Rings - 4 pages """
    url = 'https://www.wulflund.com/jewellery/silver-jewels/fantasy-silver-jewels/'

    while page_num <= 4:
        new_url = url + page_attrs + str(page_num)
        page_num += 1
        all_pages.append(new_url)

    for url in all_pages:
        source = requests.get(url)
        soup = BeautifulSoup(source.text, 'html.parser')

        get_product_information()

    product_count = len(product_names)

    def writeToJS():
        file = open('webscraping/test.json', 'w', encoding='utf-8')

        file.write('[\n\t')

        for i in range(len(product_names)):
            file.write(
                '{\n\t\t'
                f'"pk": {i+1},\n\t\t'
                '"model": "products.product",\n\t\t'
                '"fields": {\n\t\t\t'
                f'"sku": "{product_skus[i].lower()}",\n\t\t\t'
                f'"name": "{product_names[i]}",\n\t\t\t'
                f'"description": "{product_descriptions[i]}",\n\t\t\t'
                f'"price": {product_prices[i]},\n\t\t\t'
                f'"size": "{stringfy_list(product_sizes[i])}",\n\t\t\t'
                '"category": 1,\n\t\t\t'
                f'"image_url": "{product_images[i][0]}",\n\t\t\t'
                f'"image": "{product_image_names[i][0]}",\n\t\t\t'
                f'"more_images_url": "{stringfy_list(product_images[i])}",\n\t\t\t'
                f'"more_images": "{stringfy_list(product_image_names[i])}"\n\t\t'
                '}'
                '\n\t},\n\t'
            )

    writeToJS()


def scrape_necklaces():
    global page_num
    global soup
    global product_count

    page_attrs = '?strana='
    page_num = 1
    all_pages = []

    """ Silver Necklaces - 2 pages """
    url = 'https://www.wulflund.com/jewellery/silver-jewels/torcs-necklaces-silver/'

    while page_num <= 2:
        new_url = url + page_attrs + str(page_num)
        page_num += 1
        all_pages.append(new_url)

    for url in all_pages:
        source = requests.get(url)
        soup = BeautifulSoup(source.text, 'html.parser')

        get_product_information()

        last_product_count = product_count

    def writeToJS():
        file = open('webscraping/test.json', 'a', encoding='utf-8')

        y = last_product_count
        for i in range(len(product_names)):
            file.write(
                '{\n\t\t'
                f'"pk": {y+1},\n\t\t'
                '"model": "products.product",\n\t\t'
                '"fields": {\n\t\t\t'
                f'"sku": "{product_skus[i].lower()}",\n\t\t\t'
                f'"name": "{product_names[i]}",\n\t\t\t'
                f'"description": "{product_descriptions[i]}",\n\t\t\t'
                f'"price": {product_prices[i]},\n\t\t\t'
                f'"size": "{stringfy_list(product_sizes[i])}",\n\t\t\t'
                '"category": 2,\n\t\t\t'
                f'"image_url": "{product_images[i][0]}",\n\t\t\t'
                f'"image": "{product_image_names[i][0]}",\n\t\t\t'
                f'"more_images_url": "{stringfy_list(product_images[i])}",\n\t\t\t'
                f'"more_images": "{stringfy_list(product_image_names[i])}"\n\t\t'
                '}'
                '\n\t},\n\t'
            )
            y += 1

    writeToJS()

    product_count += len(product_names)


def scrape_braclets():
    global page_num
    global soup
    global product_count

    page_attrs = '?strana='
    page_num = 1
    all_pages = []

    """ Silver Braclets - 2 pages """
    url = 'https://www.wulflund.com/jewellery/silver-jewels/bracelets-historical-jewelry/'

    while page_num <= 2:
        new_url = url + page_attrs + str(page_num)
        page_num += 1
        all_pages.append(new_url)

    for url in all_pages:
        source = requests.get(url)
        soup = BeautifulSoup(source.text, 'html.parser')

        get_product_information()

        last_product_count = product_count

    def writeToJS():
        file = open('webscraping/test.json', 'a', encoding='utf-8')

        y = last_product_count
        for i in range(len(product_names)):
            file.write(
                '{\n\t\t'
                f'"pk": {y+1},\n\t\t'
                '"model": "products.product",\n\t\t'
                '"fields": {\n\t\t\t'
                f'"sku": "{product_skus[i].lower()}",\n\t\t\t'
                f'"name": "{product_names[i]}",\n\t\t\t'
                f'"description": "{product_descriptions[i]}",\n\t\t\t'
                f'"price": {product_prices[i]},\n\t\t\t'
                f'"size": "{stringfy_list(product_sizes[i])}",\n\t\t\t'
                '"category": 3,\n\t\t\t'
                f'"image_url": "{product_images[i][0]}",\n\t\t\t'
                f'"image": "{product_image_names[i][0]}",\n\t\t\t'
                f'"more_images_url": "{stringfy_list(product_images[i])}",\n\t\t\t'
                f'"more_images": "{stringfy_list(product_image_names[i])}"\n\t\t'
                '}'
                '\n\t},\n\t'
            )
            y += 1

    writeToJS()

    product_count += len(product_names)


def scrape_earrings():
    global page_num
    global soup
    global product_count

    page_attrs = '?strana='
    page_num = 1
    all_pages = []

    """ Silver Earrings - 3 pages """
    url = 'https://www.wulflund.com/jewellery/silver-jewels/historical-jewelry-silver-earrings/'

    while page_num <= 3:
        new_url = url + page_attrs + str(page_num)
        page_num += 1
        all_pages.append(new_url)

    for url in all_pages:
        source = requests.get(url)
        soup = BeautifulSoup(source.text, 'html.parser')

        get_product_information()

        last_product_count = product_count

    def writeToJS():
        file = open('webscraping/test.json', 'a', encoding='utf-8')

        y = last_product_count
        for i in range(len(product_names)):
            file.write(
                '{\n\t\t'
                f'"pk": {y+1},\n\t\t'
                '"model": "products.product",\n\t\t'
                '"fields": {\n\t\t\t'
                f'"sku": "{product_skus[i].lower()}",\n\t\t\t'
                f'"name": "{product_names[i]}",\n\t\t\t'
                f'"description": "{product_descriptions[i]}",\n\t\t\t'
                f'"price": {product_prices[i]},\n\t\t\t'
                f'"size": "{stringfy_list(product_sizes[i])}",\n\t\t\t'
                '"category": 4,\n\t\t\t'
                f'"image_url": "{product_images[i][0]}",\n\t\t\t'
                f'"image": "{product_image_names[i][0]}",\n\t\t\t'
                f'"more_images_url": "{stringfy_list(product_images[i])}",\n\t\t\t'
                f'"more_images": "{stringfy_list(product_image_names[i])}"\n\t\t'
                '}'
                '\n\t},\n\t'
            )
            y += 1

    writeToJS()

    product_count += len(product_names)


def scrape_brooches():
    global page_num
    global soup
    global product_count

    """ Silver Brooches - 1 page """
    url = 'https://www.wulflund.com/jewellery/silver-jewels/historical-brooches-silver/'

    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'html.parser')

    get_product_information()

    last_product_count = product_count

    def writeToJS():
        file = open('webscraping/test.json', 'a', encoding='utf-8')

        y = last_product_count
        for i in range(len(product_names)):
            file.write(
                '{\n\t\t'
                f'"pk": {y+1},\n\t\t'
                '"model": "products.product",\n\t\t'
                '"fields": {\n\t\t\t'
                f'"sku": "{product_skus[i].lower()}",\n\t\t\t'
                f'"name": "{product_names[i]}",\n\t\t\t'
                f'"description": "{product_descriptions[i]}",\n\t\t\t'
                f'"price": {product_prices[i]},\n\t\t\t'
                f'"size": "{stringfy_list(product_sizes[i])}",\n\t\t\t'
                '"category": 5,\n\t\t\t'
                f'"image_url": "{product_images[i][0]}",\n\t\t\t'
                f'"image": "{product_image_names[i][0]}",\n\t\t\t'
                f'"more_images_url": "{stringfy_list(product_images[i])}",\n\t\t\t'
                f'"more_images": "{stringfy_list(product_image_names[i])}"\n\t\t'
                '}'
                '\n\t},\n\t'
            )
            y += 1

    writeToJS()

    product_count += len(product_names)


def scrape_axes_and_polearms():
    global page_num
    global soup
    global product_count

    page_attrs = '?strana='
    page_num = 1
    all_pages = []

    """ Axes and Polearms - 9 pages """
    url = 'https://www.wulflund.com/weapons/axes-poleweapons/'

    while page_num <= 3:
        new_url = url + page_attrs + str(page_num)
        page_num += 1
        all_pages.append(new_url)

    for url in all_pages:
        source = requests.get(url)
        soup = BeautifulSoup(source.text, 'html.parser')

        get_product_information()

        last_product_count = product_count

    def writeToJS():
        file = open('webscraping/test.json', 'a', encoding='utf-8')

        y = last_product_count
        for i in range(len(product_names)):
            file.write(
                '{\n\t\t'
                f'"pk": {y+1},\n\t\t'
                '"model": "products.product",\n\t\t'
                '"fields": {\n\t\t\t'
                f'"sku": "{product_skus[i].lower()}",\n\t\t\t'
                f'"name": "{product_names[i]}",\n\t\t\t'
                f'"description": "{product_descriptions[i]}",\n\t\t\t'
                f'"price": {product_prices[i]},\n\t\t\t'
                f'"size": "{stringfy_list(product_sizes[i])}",\n\t\t\t'
                '"category": 6,\n\t\t\t'
                f'"image_url": "{product_images[i][0]}",\n\t\t\t'
                f'"image": "{product_image_names[i][0]}",\n\t\t\t'
                f'"more_images_url": "{stringfy_list(product_images[i])}",\n\t\t\t'
                f'"more_images": "{stringfy_list(product_image_names[i])}"\n\t\t'
                '}'
                '\n\t},\n\t'
            )
            y += 1

    writeToJS()

    product_count += len(product_names)


def scrape_swords():
    global page_num
    global soup
    global product_count

    page_attrs = '?strana='
    page_num = 1
    all_pages = []

    """ Swords - 22 pages """
    url = 'https://www.wulflund.com/weapons/swords/'

    while page_num <= 3:
        new_url = url + page_attrs + str(page_num)
        page_num += 1
        all_pages.append(new_url)

    for url in all_pages:
        source = requests.get(url)
        soup = BeautifulSoup(source.text, 'html.parser')

        get_product_information()

        last_product_count = product_count

    def writeToJS():
        file = open('webscraping/test.json', 'a', encoding='utf-8')

        y = last_product_count
        for i in range(len(product_names)):
            file.write(
                '{\n\t\t'
                f'"pk": {y+1},\n\t\t'
                '"model": "products.product",\n\t\t'
                '"fields": {\n\t\t\t'
                f'"sku": "{product_skus[i].lower()}",\n\t\t\t'
                f'"name": "{product_names[i]}",\n\t\t\t'
                f'"description": "{product_descriptions[i]}",\n\t\t\t'
                f'"price": {product_prices[i]},\n\t\t\t'
                f'"size": "{stringfy_list(product_sizes[i])}",\n\t\t\t'
                '"category": 7,\n\t\t\t'
                f'"image_url": "{product_images[i][0]}",\n\t\t\t'
                f'"image": "{product_image_names[i][0]}",\n\t\t\t'
                f'"more_images_url": "{stringfy_list(product_images[i])}",\n\t\t\t'
                f'"more_images": "{stringfy_list(product_image_names[i])}"\n\t\t'
                '}'
                '\n\t},\n\t'
            )
            y += 1

    writeToJS()

    product_count += len(product_names)


def scrape_maces_and_warhammers():
    global page_num
    global soup
    global product_count

    page_attrs = '?strana='
    page_num = 1
    all_pages = []

    """ Maces and Warhammers - 2 pages """
    url = 'https://www.wulflund.com/weapons/maces-war-hammers/'

    while page_num <= 2:
        new_url = url + page_attrs + str(page_num)
        page_num += 1
        all_pages.append(new_url)

    for url in all_pages:
        source = requests.get(url)
        soup = BeautifulSoup(source.text, 'html.parser')

        get_product_information()

        last_product_count = product_count

    def writeToJS():
        file = open('webscraping/test.json', 'a', encoding='utf-8')

        y = last_product_count
        for i in range(len(product_names)):
            file.write(
                '{\n\t\t'
                f'"pk": {y+1},\n\t\t'
                '"model": "products.product",\n\t\t'
                '"fields": {\n\t\t\t'
                f'"sku": "{product_skus[i].lower()}",\n\t\t\t'
                f'"name": "{product_names[i]}",\n\t\t\t'
                f'"description": "{product_descriptions[i]}",\n\t\t\t'
                f'"price": {product_prices[i]},\n\t\t\t'
                f'"size": "{stringfy_list(product_sizes[i])}",\n\t\t\t'
                '"category": 8,\n\t\t\t'
                f'"image_url": "{product_images[i][0]}",\n\t\t\t'
                f'"image": "{product_image_names[i][0]}",\n\t\t\t'
                f'"more_images_url": "{stringfy_list(product_images[i])}",\n\t\t\t'
                f'"more_images": "{stringfy_list(product_image_names[i])}"\n\t\t'
                '}'
                '\n\t},\n\t'
            )
            y += 1

    writeToJS()

    product_count += len(product_names)


def scrape_daggers():
    global page_num
    global soup
    global product_count

    page_attrs = '?strana='
    page_num = 1
    all_pages = []

    """ Daggers - 4 pages """
    url = 'https://www.wulflund.com/weapons/daggers/'

    while page_num <= 2:
        new_url = url + page_attrs + str(page_num)
        page_num += 1
        all_pages.append(new_url)

    for url in all_pages:
        source = requests.get(url)
        soup = BeautifulSoup(source.text, 'html.parser')

        get_product_information()

        last_product_count = product_count

    def writeToJS():
        file = open('webscraping/test.json', 'a', encoding='utf-8')

        y = last_product_count
        for i in range(len(product_names)):
            file.write(
                '{\n\t\t'
                f'"pk": {y+1},\n\t\t'
                '"model": "products.product",\n\t\t'
                '"fields": {\n\t\t\t'
                f'"sku": "{product_skus[i].lower()}",\n\t\t\t'
                f'"name": "{product_names[i]}",\n\t\t\t'
                f'"description": "{product_descriptions[i]}",\n\t\t\t'
                f'"price": {product_prices[i]},\n\t\t\t'
                f'"size": "{stringfy_list(product_sizes[i])}",\n\t\t\t'
                '"category": 9,\n\t\t\t'
                f'"image_url": "{product_images[i][0]}",\n\t\t\t'
                f'"image": "{product_image_names[i][0]}",\n\t\t\t'
                f'"more_images_url": "{stringfy_list(product_images[i])}",\n\t\t\t'
                f'"more_images": "{stringfy_list(product_image_names[i])}"\n\t\t'
                '}'
                '\n\t},\n\t'
            )
            y += 1

    writeToJS()

    product_count += len(product_names)


def scrape_horns():
    global page_num
    global soup
    global product_count

    page_attrs = '?strana='
    page_num = 1
    all_pages = []

    """ Horns - 10 pages """
    url = 'https://www.wulflund.com/horn-products/drinking-horns/'

    while page_num <= 4:
        new_url = url + page_attrs + str(page_num)
        page_num += 1
        all_pages.append(new_url)

    for url in all_pages:
        source = requests.get(url)
        soup = BeautifulSoup(source.text, 'html.parser')

        get_product_information()

        last_product_count = product_count

    def writeToJS():
        file = open('webscraping/test.json', 'a', encoding='utf-8')

        y = last_product_count
        for i in range(len(product_names)):
            file.write(
                '{\n\t\t'
                f'"pk": {y+1},\n\t\t'
                '"model": "products.product",\n\t\t'
                '"fields": {\n\t\t\t'
                f'"sku": "{product_skus[i].lower()}",\n\t\t\t'
                f'"name": "{product_names[i]}",\n\t\t\t'
                f'"description": "{product_descriptions[i]}",\n\t\t\t'
                f'"price": {product_prices[i]},\n\t\t\t'
                f'"size": "{stringfy_list(product_sizes[i])}",\n\t\t\t'
                '"category": 10,\n\t\t\t'
                f'"image_url": "{product_images[i][0]}",\n\t\t\t'
                f'"image": "{product_image_names[i][0]}",\n\t\t\t'
                f'"more_images_url": "{stringfy_list(product_images[i])}",\n\t\t\t'
                f'"more_images": "{stringfy_list(product_image_names[i])}"\n\t\t'
                '}'
                '\n\t},\n\t'
            )
            y += 1

    writeToJS()

    product_count += len(product_names)


def scrape_mead():
    global page_num
    global soup
    global product_count

    """ Mead - 1 page """
    url = 'https://www.wulflund.com/food-and-drinking/mead/'

    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'html.parser')

    get_product_information()

    last_product_count = product_count

    def writeToJS():
        file = open('webscraping/test.json', 'a', encoding='utf-8')

        y = last_product_count
        for i in range(len(product_names)):
            file.write(
                '{\n\t\t'
                f'"pk": {y+1},\n\t\t'
                '"model": "products.product",\n\t\t'
                '"fields": {\n\t\t\t'
                f'"sku": "{product_skus[i].lower()}",\n\t\t\t'
                f'"name": "{product_names[i]}",\n\t\t\t'
                f'"description": "{product_descriptions[i]}",\n\t\t\t'
                f'"price": {product_prices[i]},\n\t\t\t'
                f'"size": "{stringfy_list(product_sizes[i])}",\n\t\t\t'
                '"category": 11,\n\t\t\t'
                f'"image_url": "{product_images[i][0]}",\n\t\t\t'
                f'"image": "{product_image_names[i][0]}",\n\t\t\t'
                f'"more_images_url": "{stringfy_list(product_images[i])}",\n\t\t\t'
                f'"more_images": "{stringfy_list(product_image_names[i])}"\n\t\t'
                '}'
                '\n\t},\n\t'
            )
            y += 1

    writeToJS()

    product_count += len(product_names)


def scrape_tshirts():
    global page_num
    global soup
    global product_count

    page_attrs = '?strana='
    page_num = 1
    all_pages = []

    """ T-Shirts - 24 pages """
    url = 'https://www.wulflund.com/leather-fashion-t-shirts/viking-t-shirts/'

    while page_num <= 8:
        new_url = url + page_attrs + str(page_num)
        page_num += 1
        all_pages.append(new_url)

    for url in all_pages:
        source = requests.get(url)
        soup = BeautifulSoup(source.text, 'html.parser')

        get_product_information()

        last_product_count = product_count

    def writeToJS():
        file = open('webscraping/test.json', 'a', encoding='utf-8')

        y = last_product_count
        for i in range(len(product_names)):
            file.write(
                '{\n\t\t'
                f'"pk": {y+1},\n\t\t'
                '"model": "products.product",\n\t\t'
                '"fields": {\n\t\t\t'
                f'"sku": "{product_skus[i].lower()}",\n\t\t\t'
                f'"name": "{product_names[i]}",\n\t\t\t'
                f'"description": "{product_descriptions[i]}",\n\t\t\t'
                f'"price": {product_prices[i]},\n\t\t\t'
                f'"size": "{stringfy_list(product_sizes[i])}",\n\t\t\t'
                '"category": 12,\n\t\t\t'
                f'"image_url": "{product_images[i][0]}",\n\t\t\t'
                f'"image": "{product_image_names[i][0]}",\n\t\t\t'
                f'"more_images_url": "{stringfy_list(product_images[i])}",\n\t\t\t'
                f'"more_images": "{stringfy_list(product_image_names[i])}"\n\t\t'
                '}'
                '\n\t},\n\t'
            )
            y += 1

    writeToJS()

    product_count += len(product_names)


def scrape_fashion_leather():
    global page_num
    global soup
    global product_count

    page_attrs = '?strana='
    page_num = 1
    all_pages = []

    """ Fashion Leather - 3 pages """
    url = 'https://www.wulflund.com/leather-fashion-t-shirts/fashion---leather-t-shirts/'

    while page_num <= 2:
        new_url = url + page_attrs + str(page_num)
        page_num += 1
        all_pages.append(new_url)

    for url in all_pages:
        source = requests.get(url)
        soup = BeautifulSoup(source.text, 'html.parser')

        get_product_information()

        last_product_count = product_count

    def writeToJS():
        file = open('webscraping/test.json', 'a', encoding='utf-8')

        y = last_product_count
        for i in range(len(product_names)):
            file.write(
                '{\n\t\t'
                f'"pk": {y+1},\n\t\t'
                '"model": "products.product",\n\t\t'
                '"fields": {\n\t\t\t'
                f'"sku": "{product_skus[i].lower()}",\n\t\t\t'
                f'"name": "{product_names[i]}",\n\t\t\t'
                f'"description": "{product_descriptions[i]}",\n\t\t\t'
                f'"price": {product_prices[i]},\n\t\t\t'
                f'"size": "{stringfy_list(product_sizes[i])}",\n\t\t\t'
                '"category": 13,\n\t\t\t'
                f'"image_url": "{product_images[i][0]}",\n\t\t\t'
                f'"image": "{product_image_names[i][0]}",\n\t\t\t'
                f'"more_images_url": "{stringfy_list(product_images[i])}",\n\t\t\t'
                f'"more_images": "{stringfy_list(product_image_names[i])}"\n\t\t'
                '}'
                '\n\t},\n\t'
            )
            y += 1

    writeToJS()

    product_count += len(product_names)


def scrape_boardgames():
    global page_num
    global soup
    global product_count

    """ Board Games - 1 page """
    url = 'https://www.wulflund.com/historical-board-games/'

    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'html.parser')

    get_product_information()
    
    last_product_count = product_count

    def writeToJS():
        file = open('webscraping/test.json', 'a', encoding='utf-8')

        y = last_product_count
        for i in range(len(product_names)):
            if i != len(product_names) - 1:
                file.write(
                    '{\n\t\t'
                    f'"pk": {y+1},\n\t\t'
                    '"model": "products.product",\n\t\t'
                    '"fields": {\n\t\t\t'
                    f'"sku": "{product_skus[i].lower()}",\n\t\t\t'
                    f'"name": "{product_names[i]}",\n\t\t\t'
                    f'"description": "{product_descriptions[i]}",\n\t\t\t'
                    f'"price": {product_prices[i]},\n\t\t\t'
                    f'"size": "{stringfy_list(product_sizes[i])}",\n\t\t\t'
                    '"category": 14,\n\t\t\t'
                    f'"image_url": "{product_images[i][0]}",\n\t\t\t'
                    f'"image": "{product_image_names[i][0]}",\n\t\t\t'
                    f'"more_images_url": "{stringfy_list(product_images[i])}",\n\t\t\t'
                    f'"more_images": "{stringfy_list(product_image_names[i])}"\n\t\t'
                    '}'
                    '\n\t},\n\t'
                )
            else:
                file.write(
                    '{\n\t\t'
                    f'"pk": "{i+1}",\n\t\t'
                    '"model": "products.product",\n\t\t'
                    '"fields": {\n\t\t\t'
                    f'"sku": "{product_skus[i].lower()}",\n\t\t\t'
                    f'"name": "{product_names[i]}",\n\t\t\t'
                    f'"description": "{product_descriptions[i]}",\n\t\t\t'
                    f'"price": {product_prices[i]},\n\t\t\t'
                    f'"size": "{stringfy_list(product_sizes[i])}",\n\t\t\t'
                    '"category": 14,\n\t\t\t'
                    f'"image_url": "{product_images[i][0]}",\n\t\t\t'
                    f'"image": "{product_image_names[i][0]}",\n\t\t\t'
                    f'"more_images_url": "{stringfy_list(product_images[i])}",\n\t\t\t'
                    f'"more_images": "{stringfy_list(product_image_names[i])}"\n\t\t'
                    '}'
                    '\n\t'
                )
            y += 1
        
        file.write('}\n]')

    writeToJS()

    product_count += len(product_names)


scrape_rings()

if not any(all_lists):
    scrape_necklaces()
else:
    reset_lists()
    scrape_necklaces()

if not any(all_lists):
    scrape_braclets()
else:
    reset_lists()
    scrape_braclets()

if not any(all_lists):
    scrape_earrings()
else:
    reset_lists()
    scrape_earrings()

if not any(all_lists):
    scrape_brooches()
else:
    reset_lists()
    scrape_brooches()

if not any(all_lists):
    scrape_axes_and_polearms()
else:
    reset_lists()
    scrape_axes_and_polearms()

if not any(all_lists):
    scrape_swords()
else:
    reset_lists()
    scrape_swords()

if not any(all_lists):
    scrape_maces_and_warhammers()
else:
    reset_lists()
    scrape_maces_and_warhammers()

if not any(all_lists):
    scrape_daggers()
else:
    reset_lists()
    scrape_daggers()

if not any(all_lists):
    scrape_horns()
else:
    reset_lists()
    scrape_horns()

if not any(all_lists):
    scrape_mead()
else:
    reset_lists()
    scrape_mead()

if not any(all_lists):
    scrape_tshirts()
else:
    reset_lists()
    scrape_tshirts()

if not any(all_lists):
    scrape_fashion_leather()
else:
    reset_lists()
    scrape_fashion_leather()

if not any(all_lists):
    scrape_boardgames()
else:
    reset_lists()
    scrape_boardgames()
