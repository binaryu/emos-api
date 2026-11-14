# 邀请相关

在 `roless` 包含 `admin` 时 是无限发邀的
其余均使用 `invite_remaining` 剩余邀请次数判断

## 接口

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [邀请用户](<邀请用户.json>) | `POST` | `/api/invite` |
| [我的邀请信息](<我的邀请信息.json>) | `GET` | `/api/invite/info` |
| [邀请历史](<邀请历史.json>) | `GET` | `/api/invite/history` |
| [撤销邀请](<撤销邀请.json>) | `POST` | `/api/invite/revoke` |
| [退出邀请](<退出邀请.json>) | `POST` | `/api/invite/exit` |
| [邀请用户进入emps](<邀请用户进入emps.json>) | `POST` | `/api/invite/emps` |
| [修改邀请备注](<修改邀请备注.json>) | `PUT` | `/api/invite/remark` |
| [邀请关系树](<邀请关系树.json>) | `GET` | `/api/invite/tree` |

<!-- Postman 目录 ID: a667e632-0b89-466d-a78f-ea35b3a377d1 -->
