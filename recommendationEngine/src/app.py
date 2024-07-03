from flask import Flask, jsonify, request
import requests
import random
import os
import logging
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
import time

class App:
    def __init__(self):
        self.app = Flask(__name__)

        # OpenTelemetryの初期化
        resource = Resource(attributes={"service.name": "flask-app"})
        provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(provider)
        exporter = OTLPSpanExporter(endpoint="http://otel-collector-opentelemetry-collector.monitoring.svc.cluster.local:4317", insecure=True)
        span_processor = BatchSpanProcessor(exporter)
        provider.add_span_processor(span_processor)

        # FlaskとRequestsの自動計装
        FlaskInstrumentor().instrument_app(self.app)
        RequestsInstrumentor().instrument()

        @self.app.route('/recommendations', methods=['GET'])
        def get_recommendations():
            rails_service_url = os.getenv('RAILS_SERVICE_URL', 'http://localhost:3000')
            try:
                response = requests.get(f'{rails_service_url}/products/api', timeout=5)
                response.raise_for_status()  # HTTPエラーが発生した場合に例外をスロー
                products = response.json()


                # 重ーーーい計算を仕込んでやったぜ！！！！！！
                # 二度とやるなよ
                # heavy_computation()


                recommended_products = random.sample(products, min(3, len(products)))
                return jsonify(recommended_products)
            except requests.RequestException as e:
                logging.error(f"Error fetching recommendations: {e}")
                return jsonify({"error": "Unable to fetch recommendations"}), 500

    def run(self):
        self.app.run(host='0.0.0.0', port=5000)

def heavy_computation():
    # Simulate heavy computation
    start_time = time.time()
    time.sleep(6)  # Sleep for 6 seconds to simulate heavy computation
    end_time = time.time()
    print(f"Heavy computation took {end_time - start_time} seconds")

if __name__ == "__main__":
    app_instance = App()
    app_instance.run()
