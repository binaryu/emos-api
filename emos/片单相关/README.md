# 片单相关

权限分为 `创建者` `维护者`

对于 `创建者` 可以修改片单元信息 如 `简介` `每周所需萝卜` 等\
对于 `维护者` 只可以编辑视频内的视频列表

# 片单类型

- `video` 片单
- `music` 歌单

## 子目录

- [视频类](<视频类/>)（6 个接口）
- [音乐类](<音乐类/>)（5 个接口）

## 接口

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [兑换新卡槽](<兑换新卡槽.json>) | `POST` | `/api/watch/slot` |
| [列表](<列表.json>) | `GET` | `/api/watch` |
| [新增或修改](<新增或修改.json>) | `POST` | `/api/watch` |
| [更新维护者](<更新维护者.json>) | `PUT` | `/api/watch/{{watch_id}}/maintainer` |
| [删除](<删除.json>) | `DELETE` | `/api/watch/{{watch_id}}` |
| [对已订阅片单排序](<对已订阅片单排序.json>) | `PUT` | `/api/watch/{{watch_id}}/sort` |
| [切换已订阅片单是否可见](<切换已订阅片单是否可见.json>) | `PUT` | `/api/watch/{{watch_id}}/show` |
| [查看已订阅用户](<查看已订阅用户.json>) | `GET` | `/api/watch/{{watch_id}}/user` |
| [订阅/取消订阅](<订阅_取消订阅.json>) | `PUT` | `/api/watch/{{watch_id}}/subscribe` |
| [设置为动态抓取片单](<设置为动态抓取片单.json>) | `PUT` | `/api/watch/{{watch_id}}/dynamic` |

<!-- Postman 目录 ID: 36e1715a-9b8e-4fec-a9ae-d484b84cd073 -->
