import urllib.request
import json

image_urls = []
image_names = []

nested_more_images_url = []
nested_more_images_names = []

with open('webscraping/products.json', 'r', encoding='utf-8') as data:
    test = json.load(data)
    for i in test:
        fields = i['fields']
        for x, v in fields.items():
            if x == 'image_url':
                image_urls.append(v)
            if x == "image":
                image_names.append(v)
            if x == 'more_images_url':
                v = v.replace('[', '').replace(']', '').replace(
                    "'", '').replace(' ', '')
                img_arr = v.split(',')
                nested_more_images_url.append(img_arr)
            if x == 'more_images':
                v = v.replace('[', '').replace(']', '').replace(
                    "'", '').replace(' ', '')
                img_arr = v.split(',')
                nested_more_images_names.append(img_arr)

for i, x in zip(image_urls, image_names):
    urllib.request.urlretrieve(i, f'media/{x}')

for i, x in zip(nested_more_images_url, nested_more_images_names):
    for i1, x1 in zip(i, x):
        urllib.request.urlretrieve(i1, f'media/{x1}')
