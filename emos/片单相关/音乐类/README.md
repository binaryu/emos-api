# 音乐类

## 接口

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [歌单歌曲列表](<歌单歌曲列表.json>) | `GET` | `/api/watch/{{watch_id}}/music` |
| [搜索未加入歌单的歌曲](<搜索未加入歌单的歌曲.json>) | `GET` | `/api/watch/{{watch_id}}/music/search` |
| [更新歌单内歌曲](<更新歌单内歌曲.json>) | `POST` | `/api/watch/{{watch_id}}/music/{{music_song_id}}` |
| [删除歌单内歌曲](<删除歌单内歌曲.json>) | `DELETE` | `/api/watch/{{watch_id}}/music/{{music_song_id}}` |
| [清空歌单内歌曲](<清空歌单内歌曲.json>) | `DELETE` | `/api/watch/{{watch_id}}/music/empty` |

<!-- Postman 目录 ID: 53a27278-395a-43d0-ae5c-3c6b4eb8b619 -->
