#!/usr/bin/env bash
# 发布新版本：scripts/release.sh 0.3.1
# 更新 VERSION 单源并打 git tag，服务器端用 scripts/upgrade.sh 拉取升级
set -euo pipefail
cd "$(dirname "$0")/.."

new="${1:-}"
if [[ ! "$new" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "用法: scripts/release.sh <x.y.z>（当前 $(cat VERSION 2>/dev/null || echo 无）)" >&2
  exit 1
fi

echo "$new" > VERSION
git add VERSION
git commit -m "release: v$new"
git tag "v$new"
echo "已发布 v$new。推送代码与标签：git push && git push origin v$new"
