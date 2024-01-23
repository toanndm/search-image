import requests
import json

def call_api_and_save_to_json(api_url, output_file):
    try:
        # Gọi API
        response = requests.get(api_url)

        # Kiểm tra xem yêu cầu có thành công không (status code 200)
        if response.status_code == 200:
            # Parse dữ liệu JSON từ nội dung trả về
            data = response.json()

            # Lưu dữ liệu vào file JSON
            with open(output_file, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=2)
            
            print(f"Dữ liệu đã được lưu vào {output_file}")
        else:
            print(f"Lỗi trong quá trình gọi API. Mã lỗi: {response.status_code}")

    except Exception as e:
        print(f"Có lỗi xảy ra: {str(e)}")

# Thay thế 'URL_API' bằng đường dẫn thực tế của API bạn muốn gọi
api_url = 'https://api-shopgear.onrender.com/api/attachments'
output_file = 'output.json'

call_api_and_save_to_json(api_url, output_file)
