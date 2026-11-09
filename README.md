# loon-rules

Loon 用的分流规则集，自动同步自上游 Clash 规则。

## 规则

### Meta — `meta.list`

- 上游：[MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat)（`meta` 分支）— `geo/geosite/classical/meta.yaml`
- 内容：Meta 系域名（Facebook、WhatsApp、Threads、Meta AI / Muse、Oculus 等）
- 当前版本：556 条规则（DOMAIN 2、DOMAIN-SUFFIX 554），上游最后发布 2026-11-09

## 在 Loon 里用

```ini
[Remote Rule]
https://raw.githubusercontent.com/mgain/loon-rules/main/meta.list, policy=PROXY, tag=Meta, enabled=true
```

把 `policy=PROXY` 换成你自己的策略组名。

## 自动更新

`.github/workflows/sync.yml` 每天 03:00 UTC 自动拉一次上游：

1. 取上游 Clash yaml `meta.yaml`（`payload:` 格式）
2. 经 `scripts/convert.py` 转成 Loon `.list` 格式（去掉 `payload:` 和每行开头的 `- `，只保留规则行）
3. 有变化就自动提交，没变化就不提交

也可以在仓库 Actions 页点 `Run workflow` 手动立即同步一次。

## 文件

- `meta.list` — Loon 规则文件
- `scripts/convert.py` — Clash yaml → Loon `.list` 转换脚本
- `.github/workflows/sync.yml` — 每日自动同步
