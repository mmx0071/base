# preview-demo（GitHub 演示业务仓）

用 **Ubuntu 基线镜像** 做 PR 预览演示：默认 **没有** `tree`，PR 在 `Dockerfile` 增加 `apt install tree` 后，预览 URL 的 JSON 可区分环境。

控制面由 **preview-webhook**（建 CR / 写镜像）与 **preview-operator**（Reconcile 工作负载）完成；本目录仅提供**业务容器**与 **Actions workflow**。

## 文件

| 文件 | 说明 |
| --- | --- |
| `Dockerfile` | 基线（main）：`python3`，无 `tree` |
| `Dockerfile.with-tree` | 参考：PR 改 `Dockerfile` 增加 `tree` 即可 |
| `serve.py` | `:8080` 返回 `{"tree":{"installed":...}}` |
| `.github/workflows/preview-build.yml` | 推 GHCR + `image-ready` |

## 推到 GitHub

```bash
# 在 demo-repo 目录初始化并推送（示例）
git init
git remote add origin git@github.com:myorg/preview-demo.git
git add .
git commit -m "init preview demo"
git push -u origin main
```

仓库 Secrets（Settings → Secrets and variables → Actions）：

| Secret | 示例 |
| --- | --- |
| `PREVIEW_CALLBACK_URL` | `https://<ngrok>.ngrok-free.app/api/v1/preview/image-ready` |
| `PREVIEW_CALLBACK_TOKEN` | 与集群 `preview-webhook-secrets.image-ready-token` 一致 |

GitHub 仓库 Webhook：`https://<ngrok>.ngrok-free.app/webhook/github`，事件 **Pull requests**，Secret 与 `github-webhook-secret` 一致。

## 验收 PR 建议

1. **基线 PR**：不改 `Dockerfile` → `curl` 预览 URL → `"installed": false`
2. **功能 PR**：`Dockerfile` 增加 `tree` → `"installed": true`

镜像 tag：`ghcr.io/<owner>/preview-demo:pr-{n}-{shortSHA}`（由 workflow 生成）。

详见 [docs/minikube实现预案.md](../../docs/minikube实现预案.md)。

## 离线调试（非主路径）

见上级 [demo/build-images.sh](../build-images.sh) 与 [demo/demo-cr.yaml](../demo-cr.yaml)。
