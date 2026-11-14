# 音乐

# 群星歌曲 `is_headless`

如果没有通过 `todb` 同步 而直接调用保存时会变成群星歌曲\
判断 `todb_music_music_id` 有没有值即可

## 子目录

- [歌词](<歌词/>)（3 个接口）
- [资源](<资源/>)（4 个接口）

## 接口

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [音乐搜索](<音乐搜索.json>) | `GET` | `/api/music/song/search` |
| [音乐列表](<音乐列表.json>) | `GET` | `/api/music/song/list` |
| [更新关联的视频ID](<更新关联的视频ID.json>) | `PUT` | `/api/music/song/{{music_song_id}}/updateVideoId` |
| [删除音乐](<删除音乐.json>) | `DELETE` | `/api/music/song/{{music_song_id}}/delete` |
| [通过hash批量判断资源是否存在](<通过hash批量判断资源是否存在.json>) | `POST` | `/api/music/song/batchHashExist` |

<!-- Postman 目录 ID: d417a21f-668e-4d78-a847-3daf93a2cf20 -->
