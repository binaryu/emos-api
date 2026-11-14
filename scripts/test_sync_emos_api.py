"""不访问网络：校验中文命名、冲突处理和确定性输出。"""

import copy
import json
import re
from pathlib import Path
import tempfile
import unittest

import sync_emos_api as sync


def request(name, request_id):
    return {"name": name, "id": request_id, "request": {"method": "GET"}}


def build(items):
    stats = dict(modules=len(items), folders=0, requests=0, responses=0)
    return sync.build_tree(items, "", stats, {}), stats


class ChineseNamesTest(unittest.TestCase):
    def test_names_and_collisions_preserve_requests(self):
        items = [
            request("判断是否登录", "one"),
            request("判断是否登录", "two"),
            request("删除/恢复视频", "three"),
            request("目录信息", "four"),
            request("集合信息", "five"),
            request("tree", "six"),
            request("", "seven"),
            {"name": "接口.json", "item": []},
            request("接口", "eight"),
            request("接口-2", "nine"),
            request("接口", "ten"),
        ]
        original = copy.deepcopy(items)
        nodes, stats = build(items)
        self.assertEqual([n.get("file", n.get("dir")) for n in nodes], [
            "判断是否登录.json", "判断是否登录-2.json", "删除_恢复视频.json",
            "目录信息.json", "集合信息-2.json", "邀请关系树.json",
            "未命名请求.json", "接口.json", "接口-2.json", "接口-2-2.json", "接口-3.json",
        ])
        self.assertEqual(items, original)
        self.assertEqual(stats["requests"], 10)
        for node in nodes:
            if node["kind"] == "request":
                self.assertIn(node["meta"], original)

    def test_safe_names_and_case_insensitive_conflicts(self):
        allocator = sync.NameAllocator()
        self.assertEqual(allocator.take("README.md"), "README.md-2")
        self.assertEqual(allocator.take("apifox", ".json"), "apifox-2.json")
        self.assertEqual(allocator.take("openapi", ".json"), "openapi-2.json")
        self.assertEqual(allocator.take("ABC", ".json"), "ABC.json")
        self.assertEqual(allocator.take("abc", ".json"), "abc-2.json")
        self.assertEqual(sync.safe_name("../../测试/接口. "), ".._.._测试_接口")
        self.assertEqual(sync.safe_name("..."), "未命名")
        name = "长" * sync.MAX_NAME_LEN
        allocator.take(name, ".json")
        self.assertEqual(len(allocator.take(name, ".json")), sync.MAX_NAME_LEN + 5)

    def test_output_is_deterministic_and_links_exist(self):
        items = [{"name": "登录相关", "item": [request("判断是否登录", "one")]}]
        collection = {"info": {"name": "测试"}, "item": items}
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source.json"
            source.write_text(json.dumps({"data": collection}), encoding="utf-8")
            outputs = []
            for name in ("first", "second"):
                out = Path(tmp) / name
                self.assertEqual(sync.main(["sync", str(source), str(out)]), 0)
                outputs.append({p.relative_to(out).as_posix(): p.read_bytes()
                                for p in out.rglob("*") if p.is_file()})
            self.assertEqual(*outputs)
            self.assertEqual(set(outputs[0]), {
                "README.md", "集合信息.json", "apifox.json", "openapi.json", "登录相关/README.md",
                "登录相关/判断是否登录.json",
            })
            index = outputs[0]["README.md"].decode()
            self.assertIn("源站地址：[emos.best](https://emos.best)", index)
            self.assertIn("[api.emos.best](https://api.emos.best)（备用）", index)
            self.assertIn("(<登录相关/判断是否登录.json>)", index)
            self.assertIn("(<判断是否登录.json>)", outputs[0]["登录相关/README.md"].decode())
            self.assertIn("(<apifox.json>)", index)
            self.assertIn("(<openapi.json>)", index)
            self.assertIn(sync.OPENAPI_URL, index)
            self.assertEqual(json.loads(outputs[0]["openapi.json"])["openapi"], "3.0.3")
            exported = json.loads(outputs[0]["apifox.json"])
            self.assertEqual(exported["item"], collection["item"])
            self.assertEqual(exported["info"]["schema"], sync.POSTMAN_SCHEMA)
            self.assertEqual({v["key"]: v["value"] for v in exported["variable"]}, {
                "url": "https://emos.best", "token": "",
            })

    def test_apifox_export_preserves_existing_data_and_variables(self):
        collection = {
            "info": {"name": "测试", "description": "集合说明"},
            "variable": [{"key": "url", "value": "https://custom.example"},
                         {"key": "token", "value": "{{external_token}}"}],
            "auth": {"type": "bearer"},
            "event": [{"listen": "prerequest", "script": {"exec": ["// script"]}}],
            "item": [{**request("接口", "one"), "response": [{"name": "示例"}]}],
        }
        original = copy.deepcopy(collection)
        exported = sync.apifox_collection(collection)
        self.assertEqual(collection, original)
        for key in ("item", "auth", "event", "variable"):
            self.assertEqual(exported[key], original[key])
        self.assertEqual(exported["info"], {**original["info"], "schema": sync.POSTMAN_SCHEMA})

    def test_folder_markdown_preserves_description_id_and_config(self):
        folder = {
            "name": "投票", "id": "folder-id", "description": "只允许内部使用。",
            "auth": {"type": "bearer"},
            "event": [{"script": {"exec": ["const fence = '```';"]}}],
            "item": [request("创建投票", "vote"), {"name": "结果", "item": []}],
        }
        nodes, _ = build([folder])
        markdown = sync.render_folder_readme(nodes[0])
        self.assertIn("# 投票\n", markdown)
        self.assertIn(folder["description"], markdown)
        self.assertIn("<!-- Postman 目录 ID: folder-id -->", markdown)
        self.assertIn("(<创建投票.json>)", markdown)
        self.assertIn("(<结果/>)", markdown)
        self.assertNotIn("投票/创建投票.json", markdown)
        match = re.search(r"\n(`{3,})json\n(.*?)\n\1\n", markdown, re.S)
        self.assertIsNotNone(match)
        self.assertEqual(json.loads(match[2]), {"auth": folder["auth"], "event": folder["event"]})

    def test_description_whitespace_preserves_markdown_hard_breaks(self):
        nodes, _ = build([{
            "name": "目录", "description": "正文  \n下一行 \n    \n末行\n", "item": [],
        }])
        markdown = sync.render_folder_readme(nodes[0])
        self.assertIn("正文\\\n下一行\n\n末行", markdown)
        self.assertTrue(all(line == line.rstrip() for line in markdown.splitlines()))

    def test_structured_description_is_not_discarded(self):
        description = {"content": "说明正文", "type": "text/markdown"}
        nodes, _ = build([{"name": "目录", "description": description, "item": []}])
        markdown = sync.render_folder_readme(nodes[0])
        match = re.search(r"```json\n(.*?)\n```", markdown, re.S)
        self.assertEqual(json.loads(match[1]), {"description": description})

    def test_openapi_failure_preserves_existing_output(self):
        collection = {"info": {"name": "测试"}, "item": [{
            **request("未知鉴权", "one"),
            "request": {"method": "GET", "url": "https://emos.best/api/test",
                        "auth": {"type": "unknown"}},
        }]}
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source.json"
            source.write_text(json.dumps({"data": collection}), encoding="utf-8")
            out = Path(tmp) / "out"
            out.mkdir()
            (out / "keep.txt").write_text("原数据", encoding="utf-8")
            self.assertEqual(sync.main(["sync", str(source), str(out)]), 1)
            self.assertEqual([p.name for p in out.iterdir()], ["keep.txt"])
            self.assertEqual((out / "keep.txt").read_text(encoding="utf-8"), "原数据")

    def test_duplicate_ids_fail_before_writing(self):
        with self.assertRaises(sync.SyncError):
            build([request("接口一", "duplicate"), request("接口二", "duplicate")])


if __name__ == "__main__":
    unittest.main()
