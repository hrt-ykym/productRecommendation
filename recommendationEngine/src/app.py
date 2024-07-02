# app.py
from flask import Flask, jsonify
import requests
import random
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

class App:
    def __init__(self):
        self.app = Flask(__name__)
        FlaskInstrumentor().instrument_app(self.app)

        @self.app.route('/recommendations', methods=['GET'])
        def get_recommendations():
            response = requests.get('http://rails-service.haruotsu.svc.cluster.local:80/products/api')
            products = response.json()
            recommended_products = random.sample(products, min(3, len(products)))
            return jsonify(recommended_products)

    def run(self):
        self.app.run(host='0.0.0.0', port=5000)

# OpenTelemetry configuration
resource = Resource(attributes={"service.name": "flask-app"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint="otel-collector-opentelemetry-collector.monitoring.svc.cluster.local:4318", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

if __name__ == '__main__':
    app_instance = App()
    app_instance.run()
