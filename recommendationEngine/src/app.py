from flask import Flask, jsonify
import requests
import random
import os

class App:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/recommendations', methods=['GET'])
        def get_recommendations():
            rails_service_url = os.getenv('RAILS_SERVICE_URL', 'http://localhost:3000')
            response = requests.get(f'{rails_service_url}/products/api')
            products = response.json()
            recommended_products = random.sample(products, min(3, len(products)))
            return jsonify(recommended_products)

    def run(self):
        self.app.run(host='0.0.0.0', port=5000)
