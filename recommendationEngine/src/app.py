from flask import Flask, jsonify
import requests
import random

class App:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/recommendations', methods=['GET'])
        def get_recommendations():
            response = requests.get('http://rails-service.haruotsu.svc.cluster.local:80/products/api')
            products = response.json()
            recommended_products = random.sample(products, min(3, len(products)))
            return jsonify(recommended_products)

    def run(self):
        self.app.run(host='0.0.0.0', port=5000)
