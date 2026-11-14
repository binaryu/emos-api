# 视频类

## 接口

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [片单视频列表](<片单视频列表.json>) | `GET` | `/api/watch/{{watch_id}}/video` |
| [搜索未加入片单的视频](<搜索未加入片单的视频.json>) | `GET` | `/api/watch/{{watch_id}}/video/search` |
| [更新片单内视频](<更新片单内视频.json>) | `POST` | `/api/watch/{{watch_id}}/video/{{video_id}}` |
| [删除片单内视频](<删除片单内视频.json>) | `DELETE` | `/api/watch/{{watch_id}}/video/{{video_id}}` |
| [清空片单内视频](<清空片单内视频.json>) | `DELETE` | `/api/watch/{{watch_id}}/video/empty` |
| [批量设置片单内视频](<批量设置片单内视频.json>) | `POST` | `/api/watch/{{watch_id}}/video/update` |

<!-- Postman 目录 ID: d2973dd0-bc8c-458d-94f4-f4da6d8bcd82 -->
