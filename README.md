# py-trading-data-runner

公开 GitHub Actions runner 仓，用 public repo 的免费 runner 构建行情快照。

本仓故意不保存行情数据、manifest、universe 或私有源码。Workflow 运行时克隆 private 数据仓，在 runner 工作区构建快照，然后把 Release asset 和 manifest commit 发布回 private 数据仓。

## 必需 Secrets

启用定时任务前，需要在本仓配置这些 repository secrets：

- `PY_TRADING_DATA_REPO_TOKEN`：fine-grained token，只授权 `peilinok/py-trading-data`，权限为 `Contents: read and write`。
- `PY_TRADING_REPO_TOKEN`：fine-grained token，只授权 `peilinok/py-trading`，权限为 `Contents: read-only`。

两个 token 分开配置，避免读取 `py-trading` 的 token 同时拥有 Release/写入权限。

## Workflows

- `Publish A-share Snapshot`：构建 A 股后复权快照，并上传到 private `peilinok/py-trading-data` Release。
- `Publish US Snapshot`：构建美股 Yahoo adjusted-close 快照，并上传到 private `peilinok/py-trading-data` Release。
- `CN Security Master Admission Probe`：从 private 数据仓运行交易所证券主数据准入探针，只上传聚合计数、字段和 hash。

Workflow 支持 `dry_run=true`；dry run 只构建和校验，不发布 Release asset，也不提交 manifest 更新。

## 安全边界

本 public 仓不配置 pull request workflow，也不保存行情快照或原始交易所响应。证券主数据探针的原始响应只存在于 runner 临时目录，artifact 仅包含聚合审计报告。日志保持克制：不要打印生成后的 SQLite 内容、完整 manifest、完整 universe、token，或调试以外不必要的 Release asset URL。
