# EMOS 上游接口索引

源站地址：[emos.best](https://emos.best) · [api.emos.best](https://api.emos.best)（备用）

OpenAPI/Swagger：[openapi.json](<openapi.json>)（OpenAPI 3.0.3）。
链接导入：https://raw.githubusercontent.com/binaryu/emos-api/main/emos/openapi.json
在 Apifox 中选择“项目设置 → 导入数据 → OpenAPI/Swagger → URL 导入”。
OpenAPI 不包含缺少 URL 的请求；字段类型由示例推导，原始脚本和完整数据见 Postman 文件。

Apifox 导入：下载 [apifox.json](<apifox.json>)，在“项目设置 → 导入数据”中选择 **Postman**（Collection v2.1）。
导入时勾选对应环境，确认 `url`（默认 `https://emos.best`）并填写 `token`；备用地址为 `https://api.emos.best`。上游未填写 URL 的接口需自行补全。

> 由 `bash scripts/sync-emos-api.sh` 从上游 Postman 集合自动生成，请勿手工编辑。
> 上游集合：`api`（`6b2a25c4-59a6-4793-a958-01bbd27dec5c`）
> 来源：https://www.postman.com/_api/collection/51442337-6b2a25c4-59a6-4793-a958-01bbd27dec5c?populate=true&format=2.1.0

21 个模块 · 31 个子目录 · 191 个请求 · 204 个响应示例

目录说明见各目录的 `README.md`；公共配置见 [集合信息.json](<集合信息.json>)。

## 登录相关

目录 [登录相关/](<登录相关/>) · 2 个请求 · [README.md](<登录相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [link登录跳转](<登录相关/link登录跳转.json>) | `GET` | `/link` |
| [判断是否登录](<登录相关/判断是否登录.json>) | `GET` | `/api/sign/check` |

## 用户相关

目录 [用户相关/](<用户相关/>) · 13 个请求 · [README.md](<用户相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [简单的信息](<用户相关/简单的信息.json>) | `GET` | `/api/user/base` |
| [基本信息](<用户相关/基本信息.json>) | `GET` | `/api/user` |
| [更改是否显示空媒体库](<用户相关/更改是否显示空媒体库.json>) | `PUT` | `/api/user/showEmpty` |
| [更改是否显示成人内容](<用户相关/更改是否显示成人内容.json>) | `PUT` | `/api/user/showAdult` |
| [更改是否显示片单默认](<用户相关/更改是否显示片单默认.json>) | `GET` | `—` |
| [更新笔名](<用户相关/更新笔名.json>) | `PUT` | `/api/user/pseudonym` |
| [同意上传协议](<用户相关/同意上传协议.json>) | `PUT` | `/api/user/agreeUploadAgreement` |
| [签到](<用户相关/签到.json>) | `PUT` | `/api/user/sign` |
| [获取一次登录密码](<用户相关/获取一次登录密码.json>) | `GET` | `/api/user/passwordTemporary` |
| [重置永久登录密码](<用户相关/重置永久登录密码.json>) | `PUT` | `/api/user/passwordReset` |

### 我的服

目录 [用户相关/我的服/](<用户相关/我的服/>) · 2 个请求 · [README.md](<用户相关/我的服/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [视频服登录列表](<用户相关/我的服/视频服登录列表.json>) | `GET` | `/api/user/server/videoHistory` |
| [视频服登录退出](<用户相关/我的服/视频服登录退出.json>) | `POST` | `/api/user/server/videoLogout` |

### 统计

目录 [用户相关/统计/](<用户相关/统计/>) · 1 个请求 · [README.md](<用户相关/统计/README.md>)

#### 视频类

目录 [用户相关/统计/视频类/](<用户相关/统计/视频类/>) · 1 个请求 · [README.md](<用户相关/统计/视频类/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [观影记录](<用户相关/统计/视频类/观影记录.json>) | `GET` | `/api/user/stats/video/history` |

## 邀请相关

目录 [邀请相关/](<邀请相关/>) · 8 个请求 · [README.md](<邀请相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [邀请用户](<邀请相关/邀请用户.json>) | `POST` | `/api/invite` |
| [我的邀请信息](<邀请相关/我的邀请信息.json>) | `GET` | `/api/invite/info` |
| [邀请历史](<邀请相关/邀请历史.json>) | `GET` | `/api/invite/history` |
| [撤销邀请](<邀请相关/撤销邀请.json>) | `POST` | `/api/invite/revoke` |
| [退出邀请](<邀请相关/退出邀请.json>) | `POST` | `/api/invite/exit` |
| [邀请用户进入emps](<邀请相关/邀请用户进入emps.json>) | `POST` | `/api/invite/emps` |
| [修改邀请备注](<邀请相关/修改邀请备注.json>) | `PUT` | `/api/invite/remark` |
| [邀请关系树](<邀请相关/邀请关系树.json>) | `GET` | `/api/invite/tree` |

## 上传相关

目录 [上传相关/](<上传相关/>) · 17 个请求 · [README.md](<上传相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [获取上传token](<上传相关/获取上传token.json>) | `POST` | `/api/upload/getUploadToken` |

### 视频

目录 [上传相关/视频/](<上传相关/视频/>) · 4 个请求 · [README.md](<上传相关/视频/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [通过文件名识别视频](<上传相关/视频/通过文件名识别视频.json>) | `GET` | `/api/upload/video/recognize` |
| [获取基本信息](<上传相关/视频/获取基本信息.json>) | `GET` | `/api/upload/video/base` |
| [保存上传结果](<上传相关/视频/保存上传结果.json>) | `POST` | `/api/upload/video/save` |
| [内部入库](<上传相关/视频/内部入库.json>) | `POST` | `/api/upload/video/saveInternal` |

### 字幕

目录 [上传相关/字幕/](<上传相关/字幕/>) · 1 个请求 · [README.md](<上传相关/字幕/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [保存上传结果](<上传相关/字幕/保存上传结果.json>) | `POST` | `/api/upload/subtitle/save` |

### 图片

目录 [上传相关/图片/](<上传相关/图片/>) · 2 个请求 · [README.md](<上传相关/图片/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [上传列表](<上传相关/图片/上传列表.json>) | `GET` | `/api/upload/image/list` |
| [删除图片](<上传相关/图片/删除图片.json>) | `DELETE` | `/api/upload/image/delete` |

### 音乐

目录 [上传相关/音乐/](<上传相关/音乐/>) · 2 个请求 · [README.md](<上传相关/音乐/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [保存上传结果](<上传相关/音乐/保存上传结果.json>) | `POST` | `/api/upload/music/save` |
| [保存为群星版本](<上传相关/音乐/保存为群星版本.json>) | `POST` | `/api/upload/music/saveHeadless` |

### 分片上传

目录 [上传相关/分片上传/](<上传相关/分片上传/>) · 4 个请求 · [README.md](<上传相关/分片上传/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [获取分片上传凭证](<上传相关/分片上传/获取分片上传凭证.json>) | `POST` | `/api/upload/multipart/{{file_id}}/presign` |
| [客户端上传分片](<上传相关/分片上传/客户端上传分片.json>) | `PUT` | `/xxxx` |
| [分片合并](<上传相关/分片上传/分片合并.json>) | `POST` | `/api/upload/multipart/{{file_id}}/complete` |
| [取消上传](<上传相关/分片上传/取消上传.json>) | `DELETE` | `/api/upload/multipart/{{file_id}}/abort` |

### 储存

目录 [上传相关/储存/](<上传相关/储存/>) · 3 个请求 · [README.md](<上传相关/储存/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [可用储存列表](<上传相关/储存/可用储存列表.json>) | `GET` | `/api/upload/store/disk` |
| [暂存区文件](<上传相关/储存/暂存区文件.json>) | `GET` | `/api/upload/store/file` |
| [暂存区文件入库](<上传相关/储存/暂存区文件入库.json>) | `POST` | `/api/upload/store/archive` |

## 视频相关

目录 [视频相关/](<视频相关/>) · 23 个请求 · [README.md](<视频相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [同步视频信息](<视频相关/同步视频信息.json>) | `PATCH` | `/api/video/sync` |
| [搜索获取目录树](<视频相关/搜索获取目录树.json>) | `GET` | `/api/video/tree` |
| [获取视频标识id](<视频相关/获取视频标识id.json>) | `GET` | `/api/video/getVideoId` |
| [视频列表](<视频相关/视频列表.json>) | `GET` | `/api/video/list` |
| [视频搜索 接口轮询用](<视频相关/视频搜索 接口轮询用.json>) | `GET` | `/api/video/search` |
| [删除/恢复视频](<视频相关/删除_恢复视频.json>) | `PUT` | `/api/video/{{video_id}}/delete` |
| [获取季列表](<视频相关/获取季列表.json>) | `GET` | `/api/video/{{video_id}}/season` |
| [获取集列表](<视频相关/获取集列表.json>) | `GET` | `/api/video/{{video_id}}/episode` |
| [获取演员列表](<视频相关/获取演员列表.json>) | `GET` | `/api/video/persons` |

### 资源相关

目录 [视频相关/资源相关/](<视频相关/资源相关/>) · 8 个请求 · [README.md](<视频相关/资源相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [获取资源列表](<视频相关/资源相关/获取资源列表.json>) | `GET` | `/api/video/media/list` |
| [获取资源列表 分页](<视频相关/资源相关/获取资源列表 分页.json>) | `GET` | `/api/video/media/listAll` |
| [删除资源](<视频相关/资源相关/删除资源.json>) | `DELETE` | `/api/video/media/delete` |
| [恢复资源](<视频相关/资源相关/恢复资源.json>) | `PUT` | `/api/video/media/restore` |
| [移动资源](<视频相关/资源相关/移动资源.json>) | `PUT` | `/api/video/media/move` |
| [重命名资源](<视频相关/资源相关/重命名资源.json>) | `PUT` | `/api/video/media/rename` |
| [获取播放地址](<视频相关/资源相关/获取播放地址.json>) | `GET` | `/api/video/media/playUrl` |
| [重新同步metadata](<视频相关/资源相关/重新同步metadata.json>) | `PUT` | `/api/video/media/syncMetadata` |

### 字幕相关

目录 [视频相关/字幕相关/](<视频相关/字幕相关/>) · 3 个请求 · [README.md](<视频相关/字幕相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [获取字幕列表](<视频相关/字幕相关/获取字幕列表.json>) | `GET` | `/api/video/subtitle/list` |
| [删除字幕](<视频相关/字幕相关/删除字幕.json>) | `DELETE` | `/api/video/subtitle/delete` |
| [重命名字幕](<视频相关/字幕相关/重命名字幕.json>) | `PUT` | `/api/video/subtitle/rename` |

### 观影记录

目录 [视频相关/观影记录/](<视频相关/观影记录/>) · 3 个请求 · [README.md](<视频相关/观影记录/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [请求数](<视频相关/观影记录/请求数.json>) | `GET` | `/api/video/record/request` |
| [观影历史](<视频相关/观影记录/观影历史.json>) | `GET` | `/api/video/record/list` |
| [更新记录](<视频相关/观影记录/更新记录.json>) | `PUT` | `/api/video/record/change` |

## 片单相关

目录 [片单相关/](<片单相关/>) · 21 个请求 · [README.md](<片单相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [兑换新卡槽](<片单相关/兑换新卡槽.json>) | `POST` | `/api/watch/slot` |
| [列表](<片单相关/列表.json>) | `GET` | `/api/watch` |
| [新增或修改](<片单相关/新增或修改.json>) | `POST` | `/api/watch` |
| [更新维护者](<片单相关/更新维护者.json>) | `PUT` | `/api/watch/{{watch_id}}/maintainer` |
| [删除](<片单相关/删除.json>) | `DELETE` | `/api/watch/{{watch_id}}` |
| [对已订阅片单排序](<片单相关/对已订阅片单排序.json>) | `PUT` | `/api/watch/{{watch_id}}/sort` |
| [切换已订阅片单是否可见](<片单相关/切换已订阅片单是否可见.json>) | `PUT` | `/api/watch/{{watch_id}}/show` |
| [查看已订阅用户](<片单相关/查看已订阅用户.json>) | `GET` | `/api/watch/{{watch_id}}/user` |
| [订阅/取消订阅](<片单相关/订阅_取消订阅.json>) | `PUT` | `/api/watch/{{watch_id}}/subscribe` |
| [设置为动态抓取片单](<片单相关/设置为动态抓取片单.json>) | `PUT` | `/api/watch/{{watch_id}}/dynamic` |

### 视频类

目录 [片单相关/视频类/](<片单相关/视频类/>) · 6 个请求 · [README.md](<片单相关/视频类/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [片单视频列表](<片单相关/视频类/片单视频列表.json>) | `GET` | `/api/watch/{{watch_id}}/video` |
| [搜索未加入片单的视频](<片单相关/视频类/搜索未加入片单的视频.json>) | `GET` | `/api/watch/{{watch_id}}/video/search` |
| [更新片单内视频](<片单相关/视频类/更新片单内视频.json>) | `POST` | `/api/watch/{{watch_id}}/video/{{video_id}}` |
| [删除片单内视频](<片单相关/视频类/删除片单内视频.json>) | `DELETE` | `/api/watch/{{watch_id}}/video/{{video_id}}` |
| [清空片单内视频](<片单相关/视频类/清空片单内视频.json>) | `DELETE` | `/api/watch/{{watch_id}}/video/empty` |
| [批量设置片单内视频](<片单相关/视频类/批量设置片单内视频.json>) | `POST` | `/api/watch/{{watch_id}}/video/update` |

### 音乐类

目录 [片单相关/音乐类/](<片单相关/音乐类/>) · 5 个请求 · [README.md](<片单相关/音乐类/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [歌单歌曲列表](<片单相关/音乐类/歌单歌曲列表.json>) | `GET` | `/api/watch/{{watch_id}}/music` |
| [搜索未加入歌单的歌曲](<片单相关/音乐类/搜索未加入歌单的歌曲.json>) | `GET` | `/api/watch/{{watch_id}}/music/search` |
| [更新歌单内歌曲](<片单相关/音乐类/更新歌单内歌曲.json>) | `POST` | `/api/watch/{{watch_id}}/music/{{music_song_id}}` |
| [删除歌单内歌曲](<片单相关/音乐类/删除歌单内歌曲.json>) | `DELETE` | `/api/watch/{{watch_id}}/music/{{music_song_id}}` |
| [清空歌单内歌曲](<片单相关/音乐类/清空歌单内歌曲.json>) | `DELETE` | `/api/watch/{{watch_id}}/music/empty` |

## 反代相关

目录 [反代相关/](<反代相关/>) · 3 个请求 · [README.md](<反代相关/README.md>)

### 线路相关

目录 [反代相关/线路相关/](<反代相关/线路相关/>) · 3 个请求 · [README.md](<反代相关/线路相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [线路列表](<反代相关/线路相关/线路列表.json>) | `GET` | `/api/proxy/line` |
| [添加线路](<反代相关/线路相关/添加线路.json>) | `POST` | `/api/proxy/line` |
| [删除线路](<反代相关/线路相关/删除线路.json>) | `DELETE` | `/api/proxy/line` |

## 求片相关

目录 [求片相关/](<求片相关/>) · 7 个请求 · [README.md](<求片相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [求片列表](<求片相关/求片列表.json>) | `POST` | `/api/seek` |
| [最新求片 接口轮询用](<求片相关/最新求片 接口轮询用.json>) | `GET` | `/api/seek/poll` |
| [求片/取消求片](<求片相关/求片_取消求片.json>) | `PUT` | `/api/seek/apply` |
| [查询认领信息](<求片相关/查询认领信息.json>) | `GET` | `/api/seek/query` |
| [查询求片历史](<求片相关/查询求片历史.json>) | `GET` | `/api/seek/history` |
| [认领/取消认领](<求片相关/认领_取消认领.json>) | `PUT` | `/api/seek/claim` |
| [催上片](<求片相关/催上片.json>) | `PUT` | `/api/seek/urge` |

## 榜单相关

目录 [榜单相关/](<榜单相关/>) · 5 个请求 · [README.md](<榜单相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [萝卜排行榜](<榜单相关/萝卜排行榜.json>) | `GET` | `/api/rank/carrot` |
| [上传量排行榜](<榜单相关/上传量排行榜.json>) | `GET` | `/api/rank/upload` |
| [正在播放](<榜单相关/正在播放.json>) | `GET` | `/api/rank/userVideoRecordPlaying` |
| [正在播放-live](<榜单相关/正在播放-live.json>) | `GET` | `/api/rank/userLiveRecordPlaying` |
| [签到排行榜](<榜单相关/签到排行榜.json>) | `GET` | `/api/rank/sign` |

## 萝卜相关

目录 [萝卜相关/](<萝卜相关/>) · 3 个请求 · [README.md](<萝卜相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [可用萝卜](<萝卜相关/可用萝卜.json>) | `GET` | `/api/carrot/current` |
| [变化记录](<萝卜相关/变化记录.json>) | `GET` | `/api/carrot/history` |
| [转赠](<萝卜相关/转赠.json>) | `PUT` | `/api/carrot/transfer` |

## 直播相关

目录 [直播相关/](<直播相关/>) · 8 个请求 · [README.md](<直播相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [媒体库](<直播相关/媒体库.json>) | `GET` | `/api/live/library` |

### 列表相关

目录 [直播相关/列表相关/](<直播相关/列表相关/>) · 3 个请求 · [README.md](<直播相关/列表相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [列表](<直播相关/列表相关/列表.json>) | `GET` | `/api/live/list` |
| [新增或编辑](<直播相关/列表相关/新增或编辑.json>) | `POST` | `/api/live/list` |
| [删除](<直播相关/列表相关/删除.json>) | `DELETE` | `/api/live/list/{{live_list_id}}` |

### 资源相关

目录 [直播相关/资源相关/](<直播相关/资源相关/>) · 4 个请求 · [README.md](<直播相关/资源相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [媒体列表](<直播相关/资源相关/媒体列表.json>) | `GET` | `/api/live/media` |
| [新增直播源](<直播相关/资源相关/新增直播源.json>) | `POST` | `/api/live/media` |
| [删除直播源](<直播相关/资源相关/删除直播源.json>) | `DELETE` | `/api/live/media/{{live_media_id}}` |
| [批量更新直播源](<直播相关/资源相关/批量更新直播源.json>) | `POST` | `/api/live/media/update` |

## 支付相关

目录 [支付相关/](<支付相关/>) · 12 个请求 · [README.md](<支付相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [申请成为服务商](<支付相关/申请成为服务商.json>) | `POST` | `/api/pay/apply` |
| [服务商信息](<支付相关/服务商信息.json>) | `GET` | `/api/pay/base` |
| [更新服务商信息](<支付相关/更新服务商信息.json>) | `POST` | `/api/pay/update` |
| [转账给用户](<支付相关/转账给用户.json>) | `POST` | `/api/pay/transfer` |
| [创建订单](<支付相关/创建订单.json>) | `POST` | `/api/pay/create` |
| [查询订单](<支付相关/查询订单.json>) | `GET` | `/api/pay/query` |
| [关闭订单](<支付相关/关闭订单.json>) | `PUT` | `/api/pay/close` |
| [测试回调](<支付相关/测试回调.json>) | `POST` | `/api/pay/testNotify` |
| [查询用户可用萝卜](<支付相关/查询用户可用萝卜.json>) | `GET` | `/api/pay/getUserCarrot` |
| [查询用户信息](<支付相关/查询用户信息.json>) | `GET` | `/api/pay/getUserInfo` |
| [给用户发送邮件通知](<支付相关/给用户发送邮件通知.json>) | `POST` | `/api/pay/sendNotifyEmail` |
| [查询用户签到信息](<支付相关/查询用户签到信息.json>) | `GET` | `/api/pay/getUserSign` |

## 商城相关

目录 [商城相关/](<商城相关/>) · 24 个请求 · [README.md](<商城相关/README.md>)

### 商户

目录 [商城相关/商户/](<商城相关/商户/>) · 3 个请求 · [README.md](<商城相关/商户/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [基本信息](<商城相关/商户/基本信息.json>) | `GET` | `/api/shop/seller/base` |
| [更新信息](<商城相关/商户/更新信息.json>) | `POST` | `/api/shop/seller/update` |
| [申请成为商户](<商城相关/商户/申请成为商户.json>) | `POST` | `/api/shop/seller/apply` |

### 分类

目录 [商城相关/分类/](<商城相关/分类/>) · 4 个请求 · [README.md](<商城相关/分类/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [列表](<商城相关/分类/列表.json>) | `GET` | `/api/shop/category/list` |
| [新增](<商城相关/分类/新增.json>) | `POST` | `/api/shop/category/create` |
| [删除](<商城相关/分类/删除.json>) | `DELETE` | `/api/shop/category/delete` |
| [修改排序](<商城相关/分类/修改排序.json>) | `PUT` | `/api/shop/category/sort` |

### 商品

目录 [商城相关/商品/](<商城相关/商品/>) · 7 个请求 · [README.md](<商城相关/商品/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [商品列表](<商城相关/商品/商品列表.json>) | `GET` | `/api/shop/product/list` |
| [商品详情](<商城相关/商品/商品详情.json>) | `GET` | `/api/shop/product/info` |
| [新增或编辑商品](<商城相关/商品/新增或编辑商品.json>) | `POST` | `/api/shop/product/createOrUpdate` |
| [删除商品](<商城相关/商品/删除商品.json>) | `DELETE` | `/api/shop/product/delete` |
| [修改分类](<商城相关/商品/修改分类.json>) | `PUT` | `/api/shop/product/category` |
| [修改排序](<商城相关/商品/修改排序.json>) | `PUT` | `/api/shop/product/sort` |
| [上下架](<商城相关/商品/上下架.json>) | `PUT` | `/api/shop/product/up` |

### 订单

目录 [商城相关/订单/](<商城相关/订单/>) · 10 个请求 · [README.md](<商城相关/订单/README.md>)

#### 用户层面

目录 [商城相关/订单/用户层面/](<商城相关/订单/用户层面/>) · 6 个请求 · [README.md](<商城相关/订单/用户层面/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [下单](<商城相关/订单/用户层面/下单.json>) | `POST` | `/api/shop/order/user/create` |
| [支付](<商城相关/订单/用户层面/支付.json>) | `POST` | `/api/shop/order/user/pay` |
| [订单列表](<商城相关/订单/用户层面/订单列表.json>) | `GET` | `/api/shop/order/user/list` |
| [催发货](<商城相关/订单/用户层面/催发货.json>) | `PUT` | `/api/shop/order/user/urge` |
| [关闭订单](<商城相关/订单/用户层面/关闭订单.json>) | `POST` | `/api/shop/order/user/close` |
| [删除订单](<商城相关/订单/用户层面/删除订单.json>) | `DELETE` | `/api/shop/order/user/order` |

#### 商户层面

目录 [商城相关/订单/商户层面/](<商城相关/订单/商户层面/>) · 4 个请求 · [README.md](<商城相关/订单/商户层面/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [订单列表](<商城相关/订单/商户层面/订单列表.json>) | `GET` | `/api/shop/order/shop/order` |
| [更新发货状态](<商城相关/订单/商户层面/更新发货状态.json>) | `PUT` | `/api/shop/order/shop/delivery` |
| [更新备注](<商城相关/订单/商户层面/更新备注.json>) | `POST` | `/api/shop/order/shop/remark` |
| [删除订单](<商城相关/订单/商户层面/删除订单.json>) | `DELETE` | `/api/shop/order/shop/order` |

## 红包相关

目录 [红包相关/](<红包相关/>) · 3 个请求 · [README.md](<红包相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [发红包](<红包相关/发红包.json>) | `POST` | `/api/redPacket/create` |
| [红包领取记录](<红包相关/红包领取记录.json>) | `GET` | `/api/redPacket/receive` |
| [在 telegram 发 html 格式红包](<红包相关/在 telegram 发 html 格式红包.json>) | `POST` | `/api/redPacket/createTelegramHtml` |

## Telegram相关

目录 [Telegram相关/](<Telegram相关/>) · 2 个请求 · [README.md](<Telegram相关/README.md>)

### 投票

目录 [Telegram相关/投票/](<Telegram相关/投票/>) · 2 个请求 · [README.md](<Telegram相关/投票/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [创建投票](<Telegram相关/投票/创建投票.json>) | `POST` | `/api/telegram/vote/create` |
| [查看投票结果](<Telegram相关/投票/查看投票结果.json>) | `GET` | `/api/telegram/vote/result` |

## 抽奖相关

目录 [抽奖相关/](<抽奖相关/>) · 4 个请求 · [README.md](<抽奖相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [创建抽奖](<抽奖相关/创建抽奖.json>) | `POST` | `/api/lottery/create` |
| [查看中奖列表](<抽奖相关/查看中奖列表.json>) | `GET` | `/api/lottery/win` |
| [取消抽奖](<抽奖相关/取消抽奖.json>) | `PUT` | `/api/lottery/cancel` |
| [手动开奖](<抽奖相关/手动开奖.json>) | `PUT` | `/api/lottery/stop` |

## 封禁相关

目录 [封禁相关/](<封禁相关/>) · 2 个请求 · [README.md](<封禁相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [封禁列表](<封禁相关/封禁列表.json>) | `GET` | `/api/ban/list` |
| [更新状态](<封禁相关/更新状态.json>) | `PUT` | `/api/ban/change` |

## 音乐相关

目录 [音乐相关/](<音乐相关/>) · 20 个请求 · [README.md](<音乐相关/README.md>)

### 其他

目录 [音乐相关/其他/](<音乐相关/其他/>) · 4 个请求 · [README.md](<音乐相关/其他/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [收藏/取消收藏](<音乐相关/其他/收藏_取消收藏.json>) | `PUT` | `/api/music/favorite` |
| [评分](<音乐相关/其他/评分.json>) | `PUT` | `/api/music/rating` |
| [从todb同步数据](<音乐相关/其他/从todb同步数据.json>) | `PATCH` | `/api/music/sync` |
| [用spotify歌手去todb同步数据](<音乐相关/其他/用spotify歌手去todb同步数据.json>) | `PATCH` | `/api/music/syncSpotifyArtist` |

### 歌手

目录 [音乐相关/歌手/](<音乐相关/歌手/>) · 2 个请求 · [README.md](<音乐相关/歌手/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [歌手列表](<音乐相关/歌手/歌手列表.json>) | `GET` | `/api/music/person/list` |
| [歌手详情](<音乐相关/歌手/歌手详情.json>) | `GET` | `—` |

### 音乐

目录 [音乐相关/音乐/](<音乐相关/音乐/>) · 12 个请求 · [README.md](<音乐相关/音乐/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [音乐搜索](<音乐相关/音乐/音乐搜索.json>) | `GET` | `/api/music/song/search` |
| [音乐列表](<音乐相关/音乐/音乐列表.json>) | `GET` | `/api/music/song/list` |
| [更新关联的视频ID](<音乐相关/音乐/更新关联的视频ID.json>) | `PUT` | `/api/music/song/{{music_song_id}}/updateVideoId` |
| [删除音乐](<音乐相关/音乐/删除音乐.json>) | `DELETE` | `/api/music/song/{{music_song_id}}/delete` |
| [通过hash批量判断资源是否存在](<音乐相关/音乐/通过hash批量判断资源是否存在.json>) | `POST` | `/api/music/song/batchHashExist` |

#### 歌词

目录 [音乐相关/音乐/歌词/](<音乐相关/音乐/歌词/>) · 3 个请求 · [README.md](<音乐相关/音乐/歌词/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [歌词列表](<音乐相关/音乐/歌词/歌词列表.json>) | `GET` | `/api/music/song/{{music_song_id}}/lyric/list` |
| [创建歌词](<音乐相关/音乐/歌词/创建歌词.json>) | `POST` | `/api/music/song/{{music_song_id}}/lyric/create` |
| [删除歌词](<音乐相关/音乐/歌词/删除歌词.json>) | `DELETE` | `/api/music/song/{{music_song_id}}/lyric/delete` |

#### 资源

目录 [音乐相关/音乐/资源/](<音乐相关/音乐/资源/>) · 4 个请求 · [README.md](<音乐相关/音乐/资源/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [资源列表](<音乐相关/音乐/资源/资源列表.json>) | `GET` | `/api/music/song/{{music_song_id}}/media/list` |
| [删除资源](<音乐相关/音乐/资源/删除资源.json>) | `DELETE` | `/api/music/song/{{music_song_id}}/media/delete` |
| [获取播放地址](<音乐相关/音乐/资源/获取播放地址.json>) | `GET` | `/api/music/song/{{music_song_id}}/media/playUrl` |
| [移动资源](<音乐相关/音乐/资源/移动资源.json>) | `PUT` | `/api/music/song/{{music_song_id}}/media/move` |

### 专辑

目录 [音乐相关/专辑/](<音乐相关/专辑/>) · 2 个请求 · [README.md](<音乐相关/专辑/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [专辑列表](<音乐相关/专辑/专辑列表.json>) | `GET` | `/api/music/album/list` |
| [更新关联的视频ID](<音乐相关/专辑/更新关联的视频ID.json>) | `PUT` | `/api/music/album/{{music_alumb_id}}/updateVideoId` |

## 影院相关

目录 [影院相关/](<影院相关/>) · 6 个请求 · [README.md](<影院相关/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [随机影片](<影院相关/随机影片.json>) | `GET` | `/api/reel/rand` |
| [影片信息](<影院相关/影片信息.json>) | `GET` | `/api/reel/info/{{forge_reel_uuid}}` |
| [添加影片](<影院相关/添加影片.json>) | `POST` | `/api/reel/create` |
| [媒体列表](<影院相关/媒体列表.json>) | `GET` | `/api/reel/media` |
| [获取播放清单](<影院相关/获取播放清单.json>) | `POST` | `/api/reel/manifest` |
| [更新播放进度](<影院相关/更新播放进度.json>) | `POST` | `/api/reel/progress` |

## 基金相关

目录 [基金相关/](<基金相关/>) · 4 个请求 · [README.md](<基金相关/README.md>)

### 订单

目录 [基金相关/订单/](<基金相关/订单/>) · 4 个请求 · [README.md](<基金相关/订单/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [判断是否可以参与活动](<基金相关/订单/判断是否可以参与活动.json>) | `POST` | `/api/fund/order/check` |
| [订单列表](<基金相关/订单/订单列表.json>) | `GET` | `/api/fund/order/list` |
| [下单并支付](<基金相关/订单/下单并支付.json>) | `POST` | `/api/fund/order/create` |
| [提交报销凭证](<基金相关/订单/提交报销凭证.json>) | `POST` | `/api/fund/order/evidence` |

## 悄悄话

目录 [悄悄话/](<悄悄话/>) · 4 个请求 · [README.md](<悄悄话/README.md>)

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [发送](<悄悄话/发送.json>) | `POST` | `/api/whisper/create` |
| [发出的](<悄悄话/发出的.json>) | `GET` | `/api/whisper/sender` |
| [收到的](<悄悄话/收到的.json>) | `GET` | `/api/whisper/receiver` |
| [回复](<悄悄话/回复.json>) | `POST` | `/api/whisper/reply` |
