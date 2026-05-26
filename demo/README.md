# Minikube 演示

通过 **GitHub PR + preview-webhook + Actions（GHCR + image-ready）** 验证「不同 PR → 不同镜像 → 不同预览 URL」。

| 路径 | 说明 |
| --- | --- |
| [demo-repo/](demo-repo/) | 推送到 GitHub 的业务仓（Ubuntu + `tree` 演示） |
| [demo-repo/.github/workflows/preview-build.yml](demo-repo/.github/workflows/preview-build.yml) | 构建推 GHCR + 回调 `image-ready` |
| [demo-cr.yaml](demo-cr.yaml) | **仅手工调试**（Webhook 未就绪时）；非验收主路径 |
| [demo-cr-baseline.yaml](demo-cr-baseline.yaml) | 同上 |
| [build-images.sh](build-images.sh) | **仅离线调试**（本地 tag + `minikube image load`） |

完整流程见 [docs/minikube实现预案.md](../docs/minikube实现预案.md)（阶段 0→B）。

## 主路径（GitHub）

1. 将 `demo-repo/` 推到 GitHub（如 `myorg/preview-demo`）。
2. 按预案 §10–§11 部署 Operator/Webhook，配置 ngrok 与 GitHub Webhook。
3. 配置仓库 Secrets：`PREVIEW_CALLBACK_URL`、`PREVIEW_CALLBACK_TOKEN`。
4. 开 PR（基线无 `tree` / PR 改 `Dockerfile` 安装 `tree`）→ Actions → `curl` 预览 URL。

## 附录（手工调试）

```bash
chmod +x demo/build-images.sh
./demo/build-images.sh
kubectl apply -f demo/demo-cr-baseline.yaml
kubectl apply -f demo/demo-cr.yaml
```
