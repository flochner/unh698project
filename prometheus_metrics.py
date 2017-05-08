import time
from flask import request
from flask import Response
from prometheus_client import Summary, Counter, Histogram
from prometheus_client.exposition import generate_latest
from prometheus_client.core import  CollectorRegistry
from prometheus_client.multiprocess import MultiProcessCollector

_INF = float("inf")
# Create a metric to track time spent and requests made.
REQUEST_TIME = Histogram(
    'app:request_processing_seconds', 
    'Time spent processing request',
    ['method', 'endpoint'],
    buckets=tuple([0.0001, 0.001, .01, .1, 1, _INF])
)
REQUEST_COUNTER = Counter(
    'app:request_count', 
    'Total count of requests', 
    ['method', 'endpoint', 'http_status']
)

def setup_metrics(app):
    @app.before_request
    def before_request():
        request.start_time = time.time()

    @app.after_request
    def increment_request_count(response):
        request_latency = time.time() - request.start_time
        REQUEST_TIME.labels(request.method, request.path
            ).observe(request_latency)

        REQUEST_COUNTER.labels(request.method, request.path,
                response.status_code).inc()
        return response

    @app.route('/metrics')
    def metrics():
        return Response(generate_latest(), mimetype="text/plain")
