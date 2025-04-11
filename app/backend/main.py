
from flask import Flask, request
import time
from prometheus_client import Counter, Summary, generate_latest, CONTENT_TYPE_LATEST
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# Initialize tracing and metrics
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "kubeobserve360-backend"})
    )
)
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

REQUEST_COUNT = Counter('http_requests_total', 'Total number of HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Summary('http_request_latency_seconds', 'Latency of HTTP requests in seconds')

@app.route("/")
@REQUEST_LATENCY.time()
def hello():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    with tracer.start_as_current_span("hello-span"):
        time.sleep(0.1)
        return "Hello from KubeObserve360!"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
