from flask import Flask, jsonify
import requests
import random
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# トレーサーの設定
resource = Resource(attributes={
    "service.name": "flask-service"
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint="http://tempo.observability.svc.cluster.local:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

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
