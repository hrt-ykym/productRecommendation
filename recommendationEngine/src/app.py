from flask import Flask, jsonify
import requests
import random

class App:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/recommendations', methods=['GET'])
        def get_recommendations():
            try:
                response = requests.get('http://localhost:8888/products/api')
                print(response.json())
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
            products = response.json()
            recommended_products = random.sample(products, min(3, len(products)))
            return jsonify(recommended_products)

    def run(self):
        self.app.run(host='0.0.0.0', port=5000)
