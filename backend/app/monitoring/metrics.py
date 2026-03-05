from prometheus_client import Counter, Histogram, Gauge
import time

predictions_total = Counter(
    'predictions_total',
    'Total number of predictions',
    ['model']
)

prediction_latency = Histogram(
    'prediction_latency_seconds',
    'Prediction latency in seconds',
    ['model']
)

model_inference_time = Histogram(
    'model_inference_seconds',
    'Model inference time in seconds',
    ['model']
)

active_requests = Gauge(
    'active_requests_total',
    'Number of active requests'
)

def track_prediction(model_name: str):
    predictions_total.labels(model=model_name).inc()

def track_inference_time(model_name: str, duration: float):
    model_inference_time.labels(model=model_name).observe(duration)
    prediction_latency.labels(model=model_name).observe(duration)

def increment_active_requests():
    active_requests.inc()

def decrement_active_requests():
    active_requests.dec()
