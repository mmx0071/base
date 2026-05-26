#!/usr/bin/env bash
# 离线调试：本地 tag + minikube image load（主路径为 GitHub Actions → GHCR，见 docs/minikube实现预案.md §20）
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEMO="${ROOT}/demo-repo"

echo "==> baseline (no tree) -> preview-demo:pr-41-base"
docker build -f "${DEMO}/Dockerfile" -t preview-demo:pr-41-base "${DEMO}"
minikube image load preview-demo:pr-41-base

echo "==> PR sample (with tree) -> preview-demo:pr-42-with-tree"
docker build -f "${DEMO}/Dockerfile.with-tree" -t preview-demo:pr-42-with-tree "${DEMO}"
minikube image load preview-demo:pr-42-with-tree

echo "Done (offline debug). Optional:"
echo "  kubectl apply -f demo/demo-cr-baseline.yaml"
echo "  kubectl apply -f demo/demo-cr.yaml"
echo "Production path: push demo-repo to GitHub + Webhook — see docs/minikube实现预案.md"
