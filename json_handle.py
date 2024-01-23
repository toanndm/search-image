import json
import requests
import csv
import os
from urllib.parse import urlparse
from shutil import copyfile

with open('output.json', 'r', encoding='utf-8') as file:
    datas = json.load(file)

output_folder = 'Data'

os.makedirs(output_folder, exist_ok=True)

for data in datas:
    image_path = data['file']
    product_id = data['publication']

    image_filename = os.path.join(output_folder, f'{product_id}.jpg')

    count = 1
    while os.path.exists(image_filename):
        image_filename = os.path.join(output_folder, f'{product_id}_{count}.jpg')
        count += 1

    if urlparse(image_path).scheme:
        response = requests.get(image_path)
        with open(image_filename, 'wb') as image_file:
            image_file.write(response.content)
    else:
        copyfile(image_path, image_filename)

print("Dữ liệu và ảnh đã được lưu vào output.csv và thư mục Data.")
