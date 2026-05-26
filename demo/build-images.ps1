# Windows 可选脚本；macOS 请用 build-images.sh
# 离线调试：本地 tag + minikube image load（主路径见 docs/minikube实现预案.md §20）
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Demo = Join-Path $Root "demo-repo"

Write-Host "==> baseline (no tree) -> preview-demo:pr-41-base"
docker build -f (Join-Path $Demo "Dockerfile") -t preview-demo:pr-41-base $Demo
minikube image load preview-demo:pr-41-base

Write-Host "==> PR sample (with tree) -> preview-demo:pr-42-with-tree"
docker build -f (Join-Path $Demo "Dockerfile.with-tree") -t preview-demo:pr-42-with-tree $Demo
minikube image load preview-demo:pr-42-with-tree

Write-Host "Done. After Go operator is deployed, apply:"
Write-Host "  demo/demo-cr-baseline.yaml"
Write-Host "  demo/demo-cr.yaml"
Write-Host "See docs/operator-go设计.md"
