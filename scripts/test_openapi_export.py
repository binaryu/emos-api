"""不访问网络：校验 Postman 集合到 OpenAPI 3.0.3 的语义转换。"""
import copy
import json
import re
from pathlib import Path
import unittest

import openapi_export as export
HTTP_METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}
ROOT = Path(__file__).resolve().parent.parent
def url(path, query=None):
    if path is None: return None
    external = path.startswith(("http://", "https://"))
    path_only = re.sub(r"^[a-z]+://[^/]+", "", path) if external else path
    value = {"raw": path if external else "{{url}}" + path,
             "host": [] if external else ["{{url}}"],
             "path": [part for part in path_only.split("?")[0].split("/") if part]}
    if query is not None:
        value["query"] = query
        if query: value["raw"] += "?" + "&".join(str(f.get("key", "")) for f in query)
    return value
def req(name, request_id, method="GET", path="/api/example", *, body=None,
        query=None, headers=None, auth=None, responses=None):
    payload = {"method": method, "header": headers or [], "url": url(path, query)}
    if body is not None: payload["body"] = body
    if auth is not None: payload["auth"] = auth
    item = {"name": name, "id": request_id, "request": payload}
    if responses is not None: item["response"] = responses
    return item
def coll(*items, auth=None):
    value = {"info": {"name": "测试集合"}, "item": list(items)}
    if auth is not None: value["auth"] = auth
    return value
def ops(document):
    for path, item in document.get("paths", {}).items():
        for method, operation in item.items():
            if method.lower() in HTTP_METHODS and isinstance(operation, dict):
                yield path, method.lower(), operation
def op(document, path, method="GET"):
    for actual_path, actual_method, value in ops(document):
        if (actual_path, actual_method) == (path, method.lower()): return value
    raise AssertionError(f"missing operation {method.upper()} {path}")
def path_params(path, operation):
    declared = {p.get("name"): p for p in operation.get("parameters", []) if p.get("in") == "path"}
    return set(re.findall(r"\{([^{}]+)\}", path)), declared
def media_values(media):
    values = [media["example"]] if "example" in media else []
    values += [v.get("value") if isinstance(v, dict) and "value" in v else v
               for v in (media.get("examples") or {}).values()]
    return values
def examples(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "example": yield child
            else: yield from examples(child)
    elif isinstance(value, list):
        for child in value: yield from examples(child)
def source_requests(items):
    for item in items:
        if isinstance(item.get("item"), list): yield from source_requests(item["item"])
        elif isinstance(item.get("request"), dict): yield item

class OpenAPIExportTest(unittest.TestCase):
    def test_root_tags_auth_paths_operation_ids_and_external_server(self):
        collection = coll({
            "name": "parent", "item": [{"name": "child", "item": [
                req("创建条目", "create-item-1", "POST", "/api/items/{{item_id}}", responses=[]),
                req("旧接口", "legacy:item", path="/api/legacy/:id", responses=[]),
                req("外部", "external", "GET", "https://staging.example.test/api/external"),
                req("缺少地址", "missing-request", path=None)]}],
        }, auth={"type": "bearer"})
        original = copy.deepcopy(collection)
        document = export.build_openapi(collection)
        self.assertEqual(document, export.build_openapi(collection))
        self.assertEqual(collection, original)
        self.assertEqual(document["openapi"], "3.0.3")
        self.assertEqual([server.get("url") for server in document["servers"]],
                         ["https://emos.best", "https://api.emos.best"])
        schemes = document["components"]["securitySchemes"]
        bearer = {name for name, scheme in schemes.items()
                  if scheme.get("type") == "http" and scheme.get("scheme") == "bearer"}
        self.assertTrue(any(name in requirement for requirement in document["security"]
                            for name in bearer))
        current = op(document, "/api/items/{item_id}", "POST")
        self.assertEqual("/".join(current.get("tags", [])), "parent/child")
        self.assertEqual(current["operationId"], "request_create_item_1")
        for path, method in (("/api/items/{item_id}", "POST"), ("/api/legacy/{id}", "GET")):
            expected, declared = path_params(path, op(document, path, method))
            self.assertEqual(set(declared), expected)
            self.assertTrue(all(value["required"] for value in declared.values()))
        self.assertEqual(op(document, "/api/external")["servers"],
                         [{"url": "https://staging.example.test"}])
        self.assertNotIn("request_missing_request",
                         {value["operationId"] for _, _, value in ops(document)})
        unmapped = document["x-postman-unmapped-items"]
        self.assertEqual([item["id"] for item in unmapped], ["missing-request"])
        self.assertEqual(unmapped[0]["name"], "缺少地址")
        self.assertTrue(unmapped[0]["reason"])
    def test_raw_body_comments_trailing_commas_and_variables(self):
        raw = """{
    // 用户输入，未加引号的变量也应保留
    "name": "demo",
    "value": {{dynamic_value}},
    "items": [1, 2,],
}"""
        collection = coll(req("解析请求", "parse-body", "POST", "/api/parse", body={
            "mode": "raw", "raw": raw, "options": {"raw": {"language": "json"}}},
            responses=[]))
        operation = op(export.build_openapi(collection), "/api/parse", "POST")
        media = next(value for value in operation["requestBody"]["content"].values()
                     if value.get("x-postman-raw") == raw)
        self.assertEqual(media["x-postman-raw"], raw)
        properties = media["schema"]["properties"]
        self.assertEqual(properties["name"].get("type"), "string")
        self.assertNotIn(properties["value"].get("type"),
                         {"integer", "number", "boolean", "array", "object"})
        self.assertEqual(properties["items"].get("type"), "array")
        self.assertFalse(media["schema"].get("required"))
        self.assertTrue(any("{{dynamic_value}}" in json.dumps(example, ensure_ascii=False)
                            for example in examples(media)))
    def test_responses_defaults_examples_and_json_inference(self):
        first, second, callback = '{"kind": "first"}', '{"kind": "second"}', '{"ok": true}'
        collection = coll(
            req("多示例", "multi-response", "POST", "/api/multi", responses=[
                {"name": "第一个", "code": 200, "body": first, "header": [
                    {"key": "Content-Type", "value": "application/json; charset=utf-8"}]},
                {"name": "第二个", "code": 200, "body": second,
                 "_postman_previewlanguage": "json", "header": []},
                {"name": "回调", "body": callback, "header": []}]),
            req("无响应", "no-response", path="/api/no-response", responses=[]))
        document = export.build_openapi(collection)
        multi = op(document, "/api/multi", "POST")
        media = multi["responses"]["200"]["content"]["application/json"]
        for expected in (json.loads(first), json.loads(second)):
            self.assertTrue(any(value == expected for value in media_values(media)))
        self.assertGreaterEqual(len(media.get("examples") or {}), 2)
        self.assertEqual(len(media["examples"]), len(set(media["examples"])))
        self.assertIn("default", multi["responses"])
        default_media = multi["responses"]["default"]["content"]["application/json"]
        self.assertTrue(any(value == json.loads(callback)
                            for value in media_values(default_media)))
        self.assertIn("default", op(document, "/api/no-response")["responses"])
    def test_parameters_forms_binary_and_duplicate_query_array(self):
        collection = coll(
            req("参数", "parameters", path="/api/params/:id", query=[
                {"key": "q", "value": "词", "description": "搜索词"},
                {"key": "hidden", "value": "1", "disabled": True},
                {"key": "tag", "value": "a"}, {"key": "tag", "value": "b"}],
                headers=[{"key": "X-Trace", "value": "abc", "description": "追踪标识"},
                         {"key": "X-Skip", "disabled": True}], responses=[]),
            req("表单", "form-data", "POST", "/api/form", responses=[], body={
                "mode": "formdata", "formdata": [
                    {"key": "title", "value": "标题", "type": "text"},
                    {"key": "skip", "value": "忽略", "disabled": True}]}),
            req("文件", "binary-file", "POST", "/api/file", responses=[],
                body={"mode": "file", "file": {"src": "/tmp/avatar.jpg"}}))
        document = export.build_openapi(collection)
        by_location = {(p.get("in"), p.get("name")): p for p in
                       op(document, "/api/params/{id}").get("parameters", [])}
        self.assertEqual(by_location[("query", "q")]["description"], "搜索词")
        self.assertNotIn(("query", "hidden"), by_location)
        self.assertEqual(by_location[("header", "X-Trace")]["description"], "追踪标识")
        self.assertNotIn(("header", "X-Skip"), by_location)
        self.assertTrue(by_location[("path", "id")]["required"])
        duplicate = by_location[("query", "tag")]
        self.assertEqual(duplicate["schema"], {"type": "array", "items": {"type": "string"}})
        self.assertEqual(duplicate["example"], ["a", "b"])
        form = op(document, "/api/form", "POST")
        properties = form["requestBody"]["content"]["multipart/form-data"]["schema"]["properties"]
        self.assertIn("title", properties)
        self.assertNotIn("skip", properties)
        binary = op(document, "/api/file", "POST")
        media = binary["requestBody"]["content"]["application/octet-stream"]
        self.assertEqual((media["schema"]["type"], media["schema"]["format"]),
                         ("string", "binary"))
    def test_noauth_overrides_and_unknown_formats_raise(self):
        folder = {"name": "公开目录", "auth": {"type": "noauth"},
                  "item": [req("目录公开", "folder-noauth", path="/api/folder-public")]}
        collection = coll(folder, req("接口公开", "request-noauth",
                                     path="/api/request-public", auth={"type": "noauth"}),
                          auth={"type": "bearer"})
        document = export.build_openapi(collection)
        for path in ("/api/folder-public", "/api/request-public"):
            self.assertEqual(op(document, path).get("security"), [])
        with self.assertRaises(export.OpenAPIError):
            export.build_openapi(coll(req("未知认证", "unknown-auth",
                                         path="/api/unknown-auth", auth={"type": "mystery"})))
        with self.assertRaises(export.OpenAPIError):
            export.build_openapi(coll(req("未知请求体", "unknown-body", "POST",
                                         "/api/unknown-body", body={"mode": "mystery"})))

        with self.assertRaises(export.OpenAPIError):
            export.build_openapi(coll(req("手写鉴权", "auth-header", headers=[
                {"key": "Authorization", "value": "Bearer {{token}}"},
            ])))

    def test_duplicate_path_and_method_raise(self):
        for items in (
            (req("重复一", "duplicate-one", path="/api/duplicate"),
             req("重复二", "duplicate-two", path="/api/duplicate")),
            (req("重复三", "duplicate-three", path="/api/duplicate/:id"),
             req("重复四", "duplicate-four", path="/api/duplicate/{{id}}")),
            (req("等价路径一", "shape-one", path="/api/duplicate/{{id}}"),
             req("等价路径二", "shape-two", path="/api/duplicate/{{name}}")),
        ):
            with self.assertRaises(export.OpenAPIError):
                export.build_openapi(coll(*items))

    def test_real_collection_counts_are_derived_from_source(self):
        source = ROOT / "emos" / "apifox.json"
        self.assertTrue(source.is_file())
        collection = json.loads(source.read_text(encoding="utf-8"))
        original = copy.deepcopy(collection)
        requests = list(source_requests(collection.get("item") or []))
        mapped = [item for item in requests if item["request"].get("url")]
        missing = [item for item in requests if not item["request"].get("url")]
        document = export.build_openapi(collection)
        self.assertEqual(collection, original)
        self.assertEqual(sum(1 for _ in ops(document)), len(mapped))
        unmapped = document["x-postman-unmapped-items"]
        self.assertEqual(len(unmapped), len(missing))
        self.assertEqual({item["id"] for item in unmapped}, {item["id"] for item in missing})
        for item in unmapped:
            self.assertTrue({"id", "name", "reason"} <= set(item))
            self.assertTrue(item["reason"])
        path_parameter_count = 0
        for path, _, current in ops(document):
            self.assertNotIn("{{", path)
            self.assertNotIn(":", path)
            expected, declared = path_params(path, current)
            self.assertEqual(set(declared), expected, path)
            self.assertTrue(all(value["required"] for value in declared.values()), path)
            path_parameter_count += len(expected)
        self.assertGreater(path_parameter_count, 0)

if __name__ == "__main__":
    unittest.main()
