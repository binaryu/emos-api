#!/usr/bin/env python3
"""把上游 Postman Collection JSON 拆成 api/emos/ 下的小文件。

用法：python3 scripts/sync_emos_api.py <collection.json> <out_dir>

设计要点：
- 目录层级沿用上游（模块 → 子目录 → …），目录名做文件名安全化 + 去重。
- 每个请求一个 `<接口名称>.json`，保留完整请求对象（参数、请求体、响应示例、脚本）。
- 集合级配置写 `集合信息.json`；各目录的说明与接口列表写 `README.md`。
- 目录 ID 以注释保留，其他目录级配置写入 Markdown 中的 JSON 代码块。
- 完整集合写 `apifox.json`（Postman v2.1），补齐 url/token 默认变量。
- 同时生成 `openapi.json`（OpenAPI 3.0.3），供 OpenAPI/Swagger 链接导入。
- 输出完全确定：不写时间戳，保留上游 JSON 数组顺序，同一输入两次输出逐字节相同。
"""

from __future__ import annotations

import json
import os
import re
import sys

from openapi_export import OpenAPIError, build_openapi

COLLECTION_FILE = "集合信息.json"
IMPORT_FILE = "apifox.json"
OPENAPI_FILE = "openapi.json"
OPENAPI_URL = "https://raw.githubusercontent.com/binaryu/emos-api/main/emos/openapi.json"
POSTMAN_SCHEMA = "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
FOLDER_FILE = "README.md"
README_FILE = "README.md"
MAX_NAME_LEN = 80
# 上游唯一的纯英文接口名；只翻译文件名和索引，不改原始请求内容。
REQUEST_NAMES = {"tree": "邀请关系树"}

# Windows / POSIX 都不安全或会破坏 markdown 链接的字符
_UNSAFE_CHARS = re.compile(r'[\\/:*?"<>|\x00-\x1f\x7f]')
_BLANK_RUN = re.compile(r"\s+")
_REQ_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class SyncError(Exception):
    """可预期的失败：打印后人话退出，不动已有目录。"""


def write_json(path: str, payload) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, indent=2))
        fh.write("\n")


def apifox_collection(collection: dict) -> dict:
    """使用 Apifox 支持的 Postman v2.1 格式，不改写上游请求。"""
    variables = list(collection.get("variable") or [])
    keys = {variable.get("key") for variable in variables}
    for key, value in (("url", "https://emos.best"), ("token", "")):
        if key not in keys:
            variables.append({"key": key, "value": value, "type": "string"})
    return {
        **collection,
        "info": {**(collection.get("info") or {}), "schema": POSTMAN_SCHEMA},
        "variable": variables,
    }


def safe_name(name, fallback: str = "未命名") -> str:
    """把上游名称变成安全的单段文件名（不含分隔符、不留点尾）。"""
    text = _UNSAFE_CHARS.sub("_", str(name or ""))
    text = _BLANK_RUN.sub(" ", text).strip()
    text = text.rstrip(". ")
    if text in ("", ".", ".."):
        text = fallback
    return text[:MAX_NAME_LEN].rstrip(". ") or fallback


class NameAllocator:
    """同一目录下重名（或仅大小写不同）时追加 -2 / -3 …，保持稳定顺序。"""

    def __init__(self) -> None:
        self._used = {name.casefold() for name in (
            COLLECTION_FILE, IMPORT_FILE, OPENAPI_FILE, FOLDER_FILE, README_FILE,
        )}

    def take(self, name: str, extension: str = "") -> str:
        candidate = name + extension
        index = 2
        while candidate.casefold() in self._used:
            suffix = f"-{index}"
            candidate = name[: MAX_NAME_LEN - len(suffix)].rstrip(". ") + suffix + extension
            index += 1
        self._used.add(candidate.casefold())
        return candidate


def request_path(item: dict) -> str:
    """取请求的路径部分（去掉 host 与 query），拿不到就返回空串。"""
    request = item.get("request") or {}
    url = request.get("url")
    if not url:
        return ""

    if isinstance(url, str):
        return _path_from_raw(url)

    segments = url.get("path")
    if isinstance(segments, list):
        parts = [str(p) for p in segments if str(p) != ""]
        return "/" + "/".join(parts) if parts else ""

    raw = url.get("raw")
    return _path_from_raw(raw) if isinstance(raw, str) else ""


def _path_from_raw(raw: str) -> str:
    text = raw.split("#", 1)[0]
    host_prefix = re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://[^/?#]*", text)
    if host_prefix:
        text = text[host_prefix.end():]
    else:
        variable_prefix = re.match(r"^\{\{[^}]+\}\}", text)
        if variable_prefix:
            text = text[variable_prefix.end():]
    text = text.split("?", 1)[0]
    if not text:
        return ""
    return text if text.startswith("/") else "/" + text


def build_tree(items, rel_dir: str, stats: dict, seen_ids: dict, depth: int = 0):
    """把上游一层的 item 数组变成内部模型（不落盘）。"""
    allocator = NameAllocator()
    nodes = []

    for item in items:
        if not isinstance(item, dict):
            raise SyncError(f"{rel_dir or '.'} 下出现非对象的 item")
        raw_name = item.get("name")
        name = str(raw_name) if raw_name else ""

        if isinstance(item.get("item"), list):
            dir_name = allocator.take(safe_name(name, "未命名目录"))
            child_rel = f"{rel_dir}/{dir_name}" if rel_dir else dir_name
            node = {
                "kind": "folder",
                "name": name or "未命名目录",
                "dir": dir_name,
                "rel": child_rel,
                "meta": {k: v for k, v in item.items() if k != "item"},
            }
            node["children"] = build_tree(
                item["item"], child_rel, stats, seen_ids, depth=depth + 1
            )
            nodes.append(node)
            if depth > 0:  # 顶层模块单独计数，避免和「模块」重复
                stats["folders"] += 1
            continue

        request_id = item.get("id")
        if not isinstance(request_id, str) or not _REQ_ID.match(request_id):
            raise SyncError(
                f"请求缺少可用 id（{rel_dir or '.'} / {name or '未命名'}），无法校验请求唯一性"
            )
        if request_id in seen_ids:
            raise SyncError(
                f"请求 id 重复：{request_id}（{seen_ids[request_id]} 与 {rel_dir or '.'} / {name}）"
            )
        seen_ids[request_id] = f"{rel_dir or '.'} / {name}"

        display_name = REQUEST_NAMES.get(name, name) or "未命名请求"
        file_name = allocator.take(safe_name(display_name), ".json")
        request = item.get("request") or {}
        nodes.append(
            {
                "kind": "request",
                "name": display_name,
                "file": file_name,
                "rel": f"{rel_dir}/{file_name}" if rel_dir else file_name,
                "method": str(request.get("method") or "").upper(),
                "path": request_path(item),
                "meta": item,
            }
        )
        stats["requests"] += 1
        stats["responses"] += len(item.get("response") or [])

    return nodes


def write_tree(nodes, abs_dir: str) -> None:
    os.makedirs(abs_dir, exist_ok=True)
    for node in nodes:
        if node["kind"] == "folder":
            node["abs"] = os.path.join(abs_dir, node["dir"])
            os.makedirs(node["abs"], exist_ok=True)
            with open(os.path.join(node["abs"], FOLDER_FILE), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(render_folder_readme(node))
            write_tree(node["children"], node["abs"])
        else:
            write_json(os.path.join(abs_dir, node["file"]), node["meta"])


def count_requests(node) -> int:
    if node["kind"] == "request":
        return 1
    return sum(count_requests(child) for child in node["children"])


def _cell(text: str) -> str:
    return text.replace("|", "\\|")


def _link(label: str, target: str) -> str:
    # <> 包裹让含空格/中文的路径在 markdown 里也成立
    return f"[{_cell(label)}](<{target}>)"


def render_folder_readme(node) -> str:
    """目录正文直接展示说明和接口，只有实际配置才使用 JSON 代码块。"""
    meta = node["meta"]
    lines = [f"# {node['name']}", ""]
    description = meta.get("description")
    if isinstance(description, str) and description.strip():
        # 用反斜线保留 Markdown 硬换行，清除上游行尾空格。
        text = "\n".join(
            line.rstrip() + ("\\" if line.strip() and line.endswith("  ") else "")
            for line in description.rstrip().splitlines()
        )
        lines.extend([text, ""])

    folders = [child for child in node["children"] if child["kind"] == "folder"]
    if folders:
        lines.extend(["## 子目录", ""])
        for child in folders:
            lines.append(
                f"- {_link(child['name'], child['dir'] + '/')}（{count_requests(child)} 个接口）"
            )
        lines.append("")
    requests = render_requests(node["children"], local=True)
    if requests:
        lines.extend(["## 接口", "", *requests])

    config = {k: v for k, v in meta.items() if k not in ("name", "id")
              and not (k == "description" and isinstance(v, str))}
    if config:
        payload = json.dumps(config, ensure_ascii=False, indent=2)
        fence = "`" * (max([2] + [len(run) for run in re.findall(r"`+", payload)]) + 1)
        lines.extend(["## 目录配置", "", fence + "json", payload, fence, ""])
    if meta.get("id"):
        lines.append(f"<!-- Postman 目录 ID: {meta['id']} -->")
    return "\n".join(lines).rstrip() + "\n"


def render_index(modules, stats: dict, collection: dict, source_url: str) -> str:
    info = collection.get("info") or {}
    collection_name = str(info.get("name") or "api")
    collection_id = str(info.get("_postman_id") or "")

    lines = [
        "# EMOS 上游接口索引",
        "",
        "源站地址：[emos.best](https://emos.best) · [api.emos.best](https://api.emos.best)（备用）",
        "",
        f"OpenAPI/Swagger：{_link(OPENAPI_FILE, OPENAPI_FILE)}（OpenAPI 3.0.3）。",
        f"链接导入：{OPENAPI_URL}",
        "在 Apifox 中选择“项目设置 → 导入数据 → OpenAPI/Swagger → URL 导入”。",
        "OpenAPI 不包含缺少 URL 的请求；字段类型由示例推导，原始脚本和完整数据见 Postman 文件。",
        "",
        f"Apifox 导入：下载 {_link(IMPORT_FILE, IMPORT_FILE)}，"
        "在“项目设置 → 导入数据”中选择 **Postman**（Collection v2.1）。",
        "导入时勾选对应环境，确认 `url`（默认 `https://emos.best`）并填写 `token`；"
        "备用地址为 `https://api.emos.best`。上游未填写 URL 的接口需自行补全。",
        "",
        "> 由 `bash scripts/sync-emos-api.sh` 从上游 Postman 集合自动生成，请勿手工编辑。",
        f"> 上游集合：`{collection_name}`"
        + (f"（`{collection_id}`）" if collection_id else ""),
        *([f"> 来源：{source_url}"] if source_url else []),
        "",
        f"{stats['modules']} 个模块 · {stats['folders']} 个子目录 · "
        f"{stats['requests']} 个请求 · {stats['responses']} 个响应示例",
        "",
        f"目录说明见各目录的 `{FOLDER_FILE}`；"
        f"公共配置见 {_link(COLLECTION_FILE, COLLECTION_FILE)}。",
        "",
    ]

    for module in modules:
        lines.append(f"## {module['name']}")
        lines.append("")
        lines.append(render_folder_summary(module))
        lines.append("")
        lines.extend(render_requests(module["children"]))
        lines.extend(render_subfolders(module["children"], 3))

    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


def render_folder_summary(node) -> str:
    parts = [
        f"目录 {_link(node['rel'] + '/', node['rel'] + '/')}",
        f"{count_requests(node)} 个请求",
        _link(FOLDER_FILE, node["rel"] + "/" + FOLDER_FILE),
    ]
    return " · ".join(parts)


def render_requests(children, local: bool = False) -> list[str]:
    rows = [child for child in children if child["kind"] == "request"]
    if not rows:
        return []
    lines = ["| 请求 | 方法 | 路径 |", "| --- | --- | --- |"]
    for row in rows:
        method = row["method"] or "—"
        path = row["path"] or "—"
        lines.append(
            f"| {_link(row['name'], row['file'] if local else row['rel'])} | `{method}` | `{_cell(path)}` |"
        )
    lines.append("")
    return lines


def render_subfolders(children, heading_level: int) -> list[str]:
    lines: list[str] = []
    for child in children:
        if child["kind"] != "folder":
            continue
        lines.append("#" * min(heading_level, 6) + f" {child['name']}")
        lines.append("")
        lines.append(render_folder_summary(child))
        lines.append("")
        lines.extend(render_requests(child["children"]))
        lines.extend(render_subfolders(child["children"], heading_level + 1))
    return lines


def load_collection(raw: bytes) -> tuple[dict, list]:
    try:
        document = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SyncError(f"上游响应不是合法 JSON：{exc}") from exc

    if not isinstance(document, dict):
        raise SyncError("上游响应顶层不是对象")
    collection = document.get("data")
    if not isinstance(collection, dict):
        raise SyncError("上游响应里没有 .data 集合对象")
    items = collection.get("item")
    if items is None:
        raise SyncError("集合缺少 .data.item（检查是否漏了 populate=true）")
    if not isinstance(items, list):
        raise SyncError("集合 .data.item 不是数组")
    if not items:
        raise SyncError("集合 .data.item 为空")
    return collection, items


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("用法: sync_emos_api.py <collection.json> <out_dir>", file=sys.stderr)
        return 2

    source, out_dir = argv[1], os.path.abspath(argv[2])
    source_url = os.environ.get("EMOS_COLLECTION_URL", "")

    try:
        with open(source, "rb") as fh:
            collection, items = load_collection(fh.read())

        stats = {"modules": len(items), "folders": 0, "requests": 0, "responses": 0}
        seen_ids: dict[str, str] = {}
        modules = build_tree(items, "", stats, seen_ids)
        if stats["requests"] == 0:
            raise SyncError("集合里没有可拆出的请求")
        openapi = build_openapi(collection)
    except (SyncError, OpenAPIError) as exc:
        print(f"✗ {exc}", file=sys.stderr)
        return 1

    write_tree(modules, out_dir)
    write_json(
        os.path.join(out_dir, COLLECTION_FILE),
        {k: v for k, v in collection.items() if k != "item"},
    )
    write_json(os.path.join(out_dir, IMPORT_FILE), apifox_collection(collection))
    write_json(os.path.join(out_dir, OPENAPI_FILE), openapi)
    readme = render_index(modules, stats, collection, source_url)
    with open(os.path.join(out_dir, README_FILE), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(readme)

    # 兜底：确认所有产物都在输出目录内
    out_real = os.path.realpath(out_dir)
    for root, _dirs, files in os.walk(out_dir):
        for name in files:
            path = os.path.realpath(os.path.join(root, name))
            if os.path.commonpath([out_real, path]) != out_real:
                print(f"✗ 生成路径越界：{path}", file=sys.stderr)
                return 1

    print(
        f"✓ {stats['modules']} 个模块 / {stats['folders']} 个子目录 / "
        f"{stats['requests']} 个请求 / {stats['responses']} 个响应示例",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
