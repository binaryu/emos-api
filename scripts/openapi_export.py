"""将本仓库使用的 Postman 请求转换为 OpenAPI 3.0，不依赖第三方包。"""

from __future__ import annotations

import json
import re
from urllib.parse import parse_qsl, urlsplit


class OpenAPIError(ValueError):
    """不能安全表示的数据应中止生成，而不是静默覆盖或去掉鉴权。"""


# 字符串整体匹配，避免把 URL 中的 // 或字符串中的逗号误当作 JSONC 语法。
_JSON_TOKENS = re.compile(r'"(?:\\.|[^"\\])*"|//[^\r\n]*|/\*[\s\S]*?\*/|\{\{[^{}]+\}\}')
_TRAILING_COMMAS = re.compile(r'"(?:\\.|[^"\\])*"|,\s*(?=[}\]])')
_METHODS = {"get", "put", "post", "delete", "patch", "head", "options", "trace"}


def _parse_json(text):
    def replace(match):
        token = match.group()
        if token.startswith('"'):
            return token
        if token.startswith("{{"):
            return json.dumps(token)
        return "\n"  # 保留注释分隔，避免相邻 token 意外拼接。

    text = _JSON_TOKENS.sub(replace, text)
    text = _TRAILING_COMMAS.sub(lambda m: m.group() if m.group().startswith('"') else "", text)
    return json.loads(text)


def _description(value):
    if isinstance(value, dict):
        value = value.get("content")
    return value if isinstance(value, str) else ""


def _merge_schemas(schemas):
    unique = {json.dumps(schema, sort_keys=True): schema for schema in schemas}
    if not unique:
        return {}
    values = list(unique.values())
    return values[0] if len(values) == 1 else {"anyOf": values}


def _schema(value):
    if value is None:
        return {"nullable": True}
    if isinstance(value, bool):
        return {"type": "boolean"}
    if isinstance(value, int):
        return {"type": "integer"}
    if isinstance(value, float):
        return {"type": "number"}
    if isinstance(value, str):
        return {} if "{{" in value else {"type": "string"}
    if isinstance(value, list):
        return {"type": "array", "items": _merge_schemas([_schema(item) for item in value])}
    return {"type": "object", "properties": {key: _schema(item) for key, item in value.items()}}


def _media(raw, content_type):
    media = {"schema": {}}
    if "json" in content_type:
        try:
            example = _parse_json(raw)
            media.update(schema=_schema(example), example=example)
        except (ValueError, TypeError) as exc:
            # 不把无法解析的 JSON 原文伪装成合法 JSON 字符串示例。
            media["x-postman-parse-error"] = str(exc)
        media["x-postman-raw"] = raw
    else:
        media.update(schema={"type": "string"}, example=raw)
    return media


def _content_type(headers, raw, json_hint=False):
    for header in headers or []:
        if not header.get("disabled") and str(header.get("key", "")).lower() == "content-type":
            return str(header.get("value") or "text/plain").split(";", 1)[0].strip().lower()
    return "application/json" if json_hint or raw.lstrip().startswith(("{", "[")) else "text/plain"


def _url_parts(url):
    if isinstance(url, str):
        raw, segments = url, None
    else:
        raw, segments = url.get("raw") or "", url.get("path")
    # Postman 的前置 URL 变量不是 OpenAPI 路径参数。
    parsed = urlsplit(re.sub(r"^\{\{[^{}]+\}\}", "", raw))
    if isinstance(segments, list):
        path = "/" + "/".join(str(part) for part in segments)
    elif isinstance(segments, str):
        path = segments
    else:
        path = parsed.path or "/"
    path = re.sub(r"\{\{([^{}]+)\}\}", r"{\1}", path)
    path = re.sub(r"(?<=/):([^/]+)", r"{\1}", path)
    server = f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else None
    return path if path.startswith("/") else "/" + path, server, parsed.query


def _parameters(request, url, path, raw_query):
    definitions = {v.get("key"): v for v in url.get("variable", [])} if isinstance(url, dict) else {}
    parameters = []
    for name in dict.fromkeys(re.findall(r"\{([^{}]+)\}", path)):
        definition = definitions.get(name, {})
        parameter = {"name": name, "in": "path", "required": True, "schema": {"type": "string"}}
        if definition.get("value") is not None:
            parameter["example"] = str(definition["value"])
        if definition.get("description"):
            parameter["description"] = _description(definition["description"])
        parameters.append(parameter)

    query = url.get("query") if isinstance(url, dict) else None
    if query is None:
        query = [{"key": key, "value": value} for key, value in parse_qsl(raw_query, keep_blank_values=True)]
    for location, fields in (("query", query), ("header", request.get("header") or [])):
        for field in fields:
            name = str(field.get("key") or "")
            if not name or field.get("disabled"):
                continue
            if location == "header" and name.lower() == "authorization":
                raise OpenAPIError("存在手写 Authorization 请求头，需明确转换为 OpenAPI 鉴权配置")
            if location == "header" and name.lower() in {"content-type", "accept"}:
                continue
            parameter = {"name": name, "in": location, "required": bool(field.get("required")),
                         "schema": {"type": "string"}}
            if field.get("value") is not None:
                parameter["example"] = str(field["value"])
            if field.get("description"):
                parameter["description"] = _description(field["description"])
            existing = next((p for p in parameters if p["in"] == location and
                             (p["name"].lower() if location == "header" else p["name"]) ==
                             (name.lower() if location == "header" else name)), None)
            if existing:
                existing["schema"] = {"type": "array", "items": {"type": "string"}}
                previous = existing.get("example", [])
                existing["example"] = (previous if isinstance(previous, list) else [previous]) + [str(field.get("value") or "")]
            else:
                parameters.append(parameter)
    return parameters


def _request_body(request):
    body = request.get("body") or {}
    mode = body.get("mode")
    if not mode:
        return None
    if mode == "raw":
        raw = body.get("raw") or ""
        hint = ((body.get("options") or {}).get("raw") or {}).get("language") == "json"
        kind = _content_type(request.get("header"), raw, hint)
        return {"content": {kind: _media(raw, kind)}}
    if mode == "file":
        kind = _content_type(request.get("header"), "")
        if kind == "text/plain":
            kind = "application/octet-stream"
        return {"content": {kind: {"schema": {"type": "string", "format": "binary"}}}}
    if mode not in {"formdata", "urlencoded"}:
        raise OpenAPIError(f"不支持的 Postman 请求体格式：{mode}")
    properties, required = {}, []
    for field in body.get(mode) or []:
        if field.get("disabled") or not field.get("key"):
            continue
        name = str(field["key"])
        if name in properties:
            raise OpenAPIError(f"表单字段重复，需要人工确认数组定义：{name}")
        schema = {"type": "string"}
        if field.get("type") == "file":
            schema["format"] = "binary"
        elif field.get("value") is not None:
            schema["example"] = str(field["value"])
        if field.get("description"):
            schema["description"] = _description(field["description"])
        properties[name] = schema
        if field.get("required"):
            required.append(name)
    schema = {"type": "object", "properties": properties}
    if required:
        schema["required"] = required
    kind = "multipart/form-data" if mode == "formdata" else "application/x-www-form-urlencoded"
    return {"content": {kind: {"schema": schema}}}


def _responses(examples):
    responses = {}
    for index, example in enumerate(examples or [], 1):
        code = str(example.get("code") or "default")
        if code != "default" and not re.fullmatch(r"[1-5][0-9]{2}", code):
            raise OpenAPIError(f"响应状态码不合法：{code}")
        response = responses.setdefault(code, {"description": str(example.get("status") or example.get("name") or "响应")})
        headers = response.setdefault("headers", {})
        for header in example.get("header") or []:
            if str(header.get("key", "")).lower() != "content-type" and header.get("key"):
                headers[header["key"]] = {"schema": {"type": "string"}, "example": str(header.get("value") or "")}
        if not headers:
            response.pop("headers", None)
        raw = example.get("body")
        if raw is None or raw == "" or code == "204":
            continue
        kind = _content_type(example.get("header"), raw, example.get("_postman_previewlanguage") == "json")
        media = _media(raw, kind)
        content = response.setdefault("content", {})
        target = content.setdefault(kind, {"schema": media["schema"], "examples": {}})
        target["schema"] = _merge_schemas([target["schema"], media["schema"]])
        sample = {"summary": str(example.get("name") or f"示例 {index}")}
        if "example" in media:
            sample["value"] = media["example"]
        if "x-postman-raw" in media:
            sample["x-postman-raw"] = raw
        if "x-postman-parse-error" in media:
            sample["description"] = "上游示例不是可解析的 JSON，原文保留在 x-postman-raw 中。"
            sample["x-postman-parse-error"] = media["x-postman-parse-error"]
        target["examples"][f"example_{index}"] = sample
    return responses or {"default": {"description": "上游未提供响应示例"}}


def _security(auth, schemes):
    if not auth or auth.get("type") == "noauth":
        return []
    kind = auth.get("type")
    if kind not in {"bearer", "basic"}:
        raise OpenAPIError(f"不支持的 Postman 鉴权格式：{kind}，不会静默去掉鉴权")
    name = kind + "Auth"
    schemes[name] = {"type": "http", "scheme": kind}
    return [{name: []}]


def build_openapi(collection: dict) -> dict:
    """只映射已知语义；缺 URL 的请求显式记录，原始数据继续保留在 apifox.json。"""
    info = collection.get("info") or {}
    document = {
        "openapi": "3.0.3",
        "info": {
            "title": "EMOS API",
            "version": info.get("version") if isinstance(info.get("version"), str) else "snapshot",
            "description": "由 Postman 快照生成。字段类型来自示例，不代表完整业务约束；未猜测必填字段。"
                           "Postman 脚本请使用 apifox.json。\n\n" + _description(info.get("description")),
        },
        "servers": [{"url": "https://emos.best", "description": "主站"},
                    {"url": "https://api.emos.best", "description": "备用"}],
        "tags": [], "paths": {}, "components": {"securitySchemes": {}},
        "x-postman-unmapped-items": [],
    }
    schemes = document["components"]["securitySchemes"]
    root_auth = collection.get("auth")
    document["security"] = _security(root_auth, schemes)
    path_shapes = {}

    def walk(items, folders, inherited_auth):
        for item in items:
            if isinstance(item.get("item"), list):
                names = [*folders, str(item.get("name") or "未命名目录")]
                tag = {"name": "/".join(names)}
                if item.get("description"):
                    tag["description"] = _description(item["description"])
                if tag["name"] not in {t["name"] for t in document["tags"]}:
                    document["tags"].append(tag)
                walk(item["item"], names, item.get("auth") or inherited_auth)
                continue
            request = item.get("request") or {}
            if isinstance(request, str):
                request = {"method": "GET", "url": request}
            url = request.get("url")
            if not url:
                document["x-postman-unmapped-items"].append({
                    "id": item.get("id"), "name": item.get("name"),
                    "folder": "/".join(folders), "reason": "missing_url",
                })
                continue
            path, server, query = _url_parts(url)
            shape = re.sub(r"\{[^{}]+\}", "{}", path)
            previous = path_shapes.setdefault(shape, path)
            if previous != path:
                raise OpenAPIError(f"路径模板等价但参数名不同，需要人工统一：{previous} 与 {path}")
            method = str(request.get("method") or "GET").lower()
            if method not in _METHODS:
                raise OpenAPIError(f"OpenAPI 不支持请求方法：{method}")
            paths = document["paths"].setdefault(path, {})
            if method in paths:
                raise OpenAPIError(f"方法与路径重复，不能覆盖已有接口：{method.upper()} {path}")
            operation = {
                "summary": str(item.get("name") or "未命名请求"),
                "operationId": "request_" + str(item["id"]).replace("-", "_"),
                "tags": ["/".join(folders) or "其他"],
                "parameters": _parameters(request, url, path, query),
                "responses": _responses(item.get("response")),
            }
            if request.get("description"):
                operation["description"] = _description(request["description"])
            auth = request.get("auth") or inherited_auth
            if auth != root_auth:
                operation["security"] = _security(auth, schemes)
            body = _request_body(request)
            if body:
                operation["requestBody"] = body
            if server and server not in {entry["url"] for entry in document["servers"]}:
                operation["servers"] = [{"url": server}]
            paths[method] = operation

    walk(collection.get("item") or [], [], root_auth)
    return document
