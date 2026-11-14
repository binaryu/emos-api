# 视频相关

# 资源类型 `item_type`

- `vl` 视频列表

- `vs` 视频季

- `ve` 视频集

- `vp` 视频分段

- `vm` 视频资源

- `vt` 视频字幕

## 子目录

- [资源相关](<资源相关/>)（8 个接口）
- [字幕相关](<字幕相关/>)（3 个接口）
- [观影记录](<观影记录/>)（3 个接口）

## 接口

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [同步视频信息](<同步视频信息.json>) | `PATCH` | `/api/video/sync` |
| [搜索获取目录树](<搜索获取目录树.json>) | `GET` | `/api/video/tree` |
| [获取视频标识id](<获取视频标识id.json>) | `GET` | `/api/video/getVideoId` |
| [视频列表](<视频列表.json>) | `GET` | `/api/video/list` |
| [视频搜索 接口轮询用](<视频搜索 接口轮询用.json>) | `GET` | `/api/video/search` |
| [删除/恢复视频](<删除_恢复视频.json>) | `PUT` | `/api/video/{{video_id}}/delete` |
| [获取季列表](<获取季列表.json>) | `GET` | `/api/video/{{video_id}}/season` |
| [获取集列表](<获取集列表.json>) | `GET` | `/api/video/{{video_id}}/episode` |
| [获取演员列表](<获取演员列表.json>) | `GET` | `/api/video/persons` |

<!-- Postman 目录 ID: bbda4038-29b0-4802-86da-10100bc69c68 -->
