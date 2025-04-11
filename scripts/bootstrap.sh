
#!/bin/bash

set -e

NAMESPACE_APP="app"
NAMESPACE_OBS="observability"
FRONTEND_CHART="./k8s-manifests/frontend"
BACKEND_CHART="./k8s-manifests/backend"
OTEL_VALUES="./k8s-manifests/observability-stack/otel-collector-values.yaml"

echo "Creating namespaces..."
kubectl create namespace $NAMESPACE_APP || true
kubectl create namespace $NAMESPACE_OBS || true

echo "Adding Helm repos..."
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

echo "Installing Prometheus..."
helm install prometheus prometheus-community/prometheus --namespace $NAMESPACE_OBS --create-namespace

echo "Installing Grafana..."
helm install grafana grafana/grafana --namespace $NAMESPACE_OBS --set adminPassword=admin123 --create-namespace

echo "Installing Loki..."
helm install loki grafana/loki --namespace $NAMESPACE_OBS --create-namespace

echo "Installing Jaeger..."
helm install jaeger bitnami/jaeger --namespace $NAMESPACE_OBS --create-namespace

echo "Installing Tempo..."
helm install tempo grafana/tempo --namespace $NAMESPACE_OBS --create-namespace

echo "Installing OpenTelemetry Collector..."
helm install otel-collector open-telemetry/opentelemetry-collector -f $OTEL_VALUES --namespace $NAMESPACE_OBS --create-namespace

echo "Deploying backend service..."
helm install backend $BACKEND_CHART --namespace $NAMESPACE_APP

echo "Deploying frontend service..."
helm install frontend $FRONTEND_CHART --namespace $NAMESPACE_APP

echo "Deployment complete!"
