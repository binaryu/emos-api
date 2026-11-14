# 分片上传

针对于 获取上传凭证返回的是 `multipart` 时使用

先基于上传凭凭证中的分片大小 本地判断要生成的分片数量
再获取上传凭证
客户都切片上传
最后调用合并分片

## 接口

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [获取分片上传凭证](<获取分片上传凭证.json>) | `POST` | `/api/upload/multipart/{{file_id}}/presign` |
| [客户端上传分片](<客户端上传分片.json>) | `PUT` | `/xxxx` |
| [分片合并](<分片合并.json>) | `POST` | `/api/upload/multipart/{{file_id}}/complete` |
| [取消上传](<取消上传.json>) | `DELETE` | `/api/upload/multipart/{{file_id}}/abort` |

<!-- Postman 目录 ID: 355be73c-abaf-4a26-9318-2415a9d9c857 -->
