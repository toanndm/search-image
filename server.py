import numpy as np
from PIL import Image
from feature_extract import FeatureExtractor
from flask import Flask, request, jsonify
import psycopg2
import requests
from io import BytesIO
from flask_cors import CORS
from collections import OrderedDict

app = Flask(__name__)
CORS(app)

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS features (
    id SERIAL PRIMARY KEY,
    product_id INTEGER,
    image_url TEXT,
    feature_vector DOUBLE PRECISION[]
);
"""
INSERT_PRODUCT = "INSERT INTO features (product_id, image_url, feature_vector) VALUES (%s, %s, %s)"
SELECT_QUERY = "SELECT feature_vector, product_id FROM features;"

url = "postgres://oedhpqsz:JkxLZcGqBUV7mwYfiRu8AXQO7sWCW7rm@floppy.db.elephantsql.com/oedhpqsz"
connection = psycopg2.connect(url)


fe = FeatureExtractor()

@app.route('/api/create', methods=['POST'])
def create():
    data = request.get_json()
    image_url = data['file']
    product_id = data['id']
    response = requests.get(image_url)
    
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        feature = fe.extract(img=image).tolist()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(INSERT_PRODUCT, (product_id, image_url, feature))
                connection.commit()

        return {"success": "true"}, 201
    else:
        return {"error": "Failed to download image"}, 500

    
@app.route('/api/search', methods=['POST'])
def index():
    features = []
    product_ids = []

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TABLE)
            cursor.execute(SELECT_QUERY)
            results = cursor.fetchall()

            for result in results:
                feature_vector = result[0]
                product_id = result[1]
                feature_vector_np = np.array(feature_vector)

                features.append(feature_vector_np)
                product_ids.append(product_id)
    file = request.files['file']
    img = Image.open(file.stream)  # PIL image

    query = fe.extract(img)
    dists = np.linalg.norm(features - query, axis=1)  # L2 distances to features
    ids = np.argsort(dists)[:30]  # Top 30 results
    product_ids_res = [product_ids[id] for id in ids]
    set_ids_res = OrderedDict.fromkeys(product_ids_res)
    return jsonify({'product_ids': list(set_ids_res)})
    

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
S