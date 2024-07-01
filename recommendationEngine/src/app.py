from flask import Flask, jsonify
import logging
import requests
import random

class App:
    def __init__(self):
        self.app = Flask(__name__)

        # ロガーの設定
        logging.basicConfig(level=logging.DEBUG)

        @self.app.route('/recommendations', methods=['GET'])
        def get_recommendations():
            try:
                response = requests.get('http://rails-service.haruotsu.svc.cluster.local:80/products/api')
                response.raise_for_status()
                products = response.json()
                recommended_products = random.sample(products, min(3, len(products)))
                return jsonify(recommended_products)
            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed: {e}")
                return jsonify({"error": "Request to Rails service failed"}), 500

    def run(self):
        self.app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    app = App()
    app.run()
