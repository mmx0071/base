# PR 预览平台（Preview Operator）

基于 **Go** Kubernetes Operator 的 GitHub PR 动态预览环境：PR 打开/更新自动部署可访问实例，关闭自动回收。

> **本仓库当前为方案与 YAML 样例**，不含 Operator 源码；Go 实现见 [docs/operator-go设计.md](docs/operator-go设计.md)。

## 仓库结构

```text
pr_k8s/
├── docs/          # 方案与设计文档
├── templates/     # CRD、RBAC、NP、CR、Operator Deployment 等 YAML 骨架
└── demo/          # Minikube 演示：业务镜像、构建脚本、样例 CR
```

## 文档

| 文档 | 说明 |
| --- | --- |
| [docs/项目评审方案.md](docs/项目评审方案.md) | 生产架构、CRD、安全、GitHub 集成、验收 |
| [docs/operator-go设计.md](docs/operator-go设计.md) | **Go Operator** 技术选型、API、Reconcile、目录规划 |
| [docs/minikube实现预案.md](docs/minikube实现预案.md) | 本地 Minikube（**macOS 基底**）+ GitHub Webhook / image-ready + GHCR |

## 样例与演示

| 路径 | 说明 |
| --- | --- |
| [templates/](templates/) | CRD、RBAC、NP、CR、Operator Deployment 等 YAML 骨架 |
| [demo/](demo/) | 演示业务仓（含 Actions workflow）、手工 CR 调试样例 |

## 配置占位符（部署前由运维填写）

| 变量 | 说明 |
|------|------|
| `PREVIEW_DOMAIN` | 预览 Ingress 通配符域 |
| `REGISTRY` | 允许拉取的镜像仓库前缀 |
| `GITHUB_ORG` / `allowedRepos` | 允许接入的仓库 |
| `PREVIEW_NAMESPACE` | 固定预览 Namespace（默认 `preview`） |
| `INGRESS_CLASS` / `INGRESS_CONTROLLER_NS` | Ingress |
| `REGISTRY_EGRESS_CIDR` | NP 放行镜像仓库 |

## 非目标

- 禁止每 PR 独立 Namespace
- 禁止自动化执行 `kubectl delete namespace`
- Operator 不负责镜像构建（由 GitHub Actions 完成）
- 首期不支持 GitLab

## 相关仓库

K8s 集群运维笔记（Calico、Ingress 等）：`k8s_info`（与本文档仓分离）
