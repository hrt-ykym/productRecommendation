from flask import Flask, jsonify
import requests
import random

class App:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/recommendations', methods=['GET'])
        def get_recommendations():
            response = requests.get('http://localhost:3000/products/api')
            products = response.json()
            recommended_products = random.sample(products, min(3, len(products)))
            return jsonify(recommended_products)

    def run(self):
        self.app.run(port=5000)
