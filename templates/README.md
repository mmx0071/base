# YAML 样例模板

部署前请替换占位符（域名、Registry、镜像等）。与 [docs/operator-go设计.md](../docs/operator-go设计.md) §4 对齐。

| 文件 | 说明 |
| --- | --- |
| `crd-previewenvironment.yaml` | `PreviewEnvironment` CRD 骨架 |
| `rbac-operator.yaml` | Operator ClusterRole / Role@preview |
| `networkpolicy-isolate.yaml` | `preview` NS 默认隔离 NP |
| `operator-deployment.yaml` | Operator Deployment 样例 |
| `webhook-deployment.yaml` | Webhook Deployment + Service（Minikube/生产同构） |
| `preview-environment-cr.yaml` | 生产向 CR 样例 |
| `preview-environment-cr-minikube.yaml` | 手工调试 CR（与 `demo/demo-cr.yaml` 同步；主路径为 Webhook 建 CR） |
| `preview-environment-cr-minikube-baseline.yaml` | 手工调试基线 CR |
| `github-actions-snippet.yml` | Actions 构建与 `image-ready` 片段 |
