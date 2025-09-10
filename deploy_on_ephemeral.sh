#!/bin/sh
set -e  # exit on any error

# 1) Receive parameters
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <API_KEY> <NAMESPACE>"
  exit 1
fi

API_KEY="$1"
NAMESPACE="$2"

echo "Using namespace: $NAMESPACE"

# 2) Create or update the secret
kubectl create secret generic custom-api-key \
  --from-literal=INFERENCE_API_KEY="$API_KEY" \
  -n "$NAMESPACE" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "✅ Secret 'custom-api-key' created or updated in namespace $NAMESPACE"

# 3) Deploy with bonfire
bonfire deploy {{cookiecutter.projectName}} --namespace="$NAMESPACE" --local-config-path bonfire-config.yaml

echo "✅ App {{cookiecutter.projectName}} deployed on Ephemeral cluster in namespace $NAMESPACE"