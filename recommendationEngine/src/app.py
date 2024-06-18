from flask import Flask, jsonify
import random

class App:
    def __init__(self):
        self.app = Flask(__name__)

        # ダミーデータの作成
        self.products = [
            {"id": 1, "name": "Product 1", "description": "Description 1", "price": 10.0},
            {"id": 2, "name": "Product 2", "description": "Description 2", "price": 20.0},
            {"id": 3, "name": "Product 3", "description": "Description 3", "price": 30.0},
            {"id": 4, "name": "Product 4", "description": "Description 4", "price": 40.0},
            {"id": 5, "name": "Product 5", "description": "Description 5", "price": 50.0},
        ]

        @self.app.route('/recommendations', methods=['GET'])
        def get_recommendations():
            recommended_products = random.sample(self.products, 3)
            return jsonify(recommended_products)

    def run(self):
        self.app.run(port=5000)
