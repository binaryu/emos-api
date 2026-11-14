#!/usr/bin/env bash
# 同步 EMOS 上游 Postman 集合并拆成 emos/ 下的小文件。
#
#   bash scripts/sync-emos-api.sh              # 更新 emos/
#   bash scripts/sync-emos-api.sh /tmp/preview # 生成到别处（预览/对比用）
#   EMOS_COLLECTION_URL=file:///tmp/x.json bash scripts/sync-emos-api.sh /tmp/t
#                                              # 换数据源（自测用，同时写进 README）
#
# 仓库保留拆分文档、Postman 集合和 OpenAPI 规范；上游原始响应仅作临时文件。
# 只有下载、校验、拆分全部成功才会替换目标目录；任一步失败都保留上一次的结果。
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-${OUT_DIR:-$REPO_ROOT/emos}}"
OUT_DIR="${OUT_DIR%/}"

COLLECTION_URL="${EMOS_COLLECTION_URL:-https://www.postman.com/_api/collection/51442337-6b2a25c4-59a6-4793-a958-01bbd27dec5c?populate=true&format=2.1.0}"

RAW_JSON="$(mktemp -t emos-collection.XXXXXX.json)"
STAGE="$(dirname "$OUT_DIR")/.$(basename "$OUT_DIR").staging.$$"

cleanup() {
  rm -rf "$RAW_JSON" "$STAGE"
}
trap cleanup EXIT

mkdir -p "$(dirname "$OUT_DIR")"
rm -rf "$STAGE"

echo "→ 拉取上游集合"
if ! curl -fsS --retry 3 --retry-delay 2 \
  -H 'User-Agent: Mozilla/5.0' \
  -H 'Accept: application/json' \
  "$COLLECTION_URL" -o "$RAW_JSON"; then
  echo "✗ 下载失败，保留原目录：$OUT_DIR" >&2
  exit 1
fi

echo "→ 拆分到临时目录"
if ! EMOS_COLLECTION_URL="$COLLECTION_URL" \
  python3 "$REPO_ROOT/scripts/sync_emos_api.py" "$RAW_JSON" "$STAGE"; then
  echo "✗ 生成失败，保留原目录：$OUT_DIR" >&2
  exit 1
fi

# 全部成功才替换：上游删掉的请求对应文件会一起消失，git 里表现为删除。
rm -rf "$OUT_DIR"
mv "$STAGE" "$OUT_DIR"

echo "✓ 已更新 $OUT_DIR"
