import json
import requests

# Đọc dữ liệu từ tệp JSON
with open('output.json', 'r') as file:
    data = json.load(file)

api_create_url = "http://127.0.0.1:5000/api/create"

for item in data:
    image_url = item["file"]
    product_id = item["publication"]

    # Tải hình từ đường link
    response = requests.get(image_url)

    if response.status_code == 200:
        # Gọi API create với dữ liệu và hình tải về
        create_data = {
            "file": image_url,
            "id": product_id
        }

        create_response = requests.post(api_create_url, json=create_data)

        if create_response.status_code == 201:
            print(f"Successfully created product with ID {product_id}")
        else:
            print(f"Failed to create product with ID {product_id}. API response: {create_response.text}")
    else:
        print(f"Failed to download image for product with ID {product_id}. HTTP status code: {response.status_code}")
