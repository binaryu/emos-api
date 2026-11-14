# 支付相关

成为服务商后 会获得萝卜的利息

也可以让用户支付萝卜获得您的服务

# 订单状态

- `default` 默认
- `await` 支付中
- `success` 支付成功
- `cancel` 取消支付
- `close` 关闭订单

## 接口

| 请求 | 方法 | 路径 |
| --- | --- | --- |
| [申请成为服务商](<申请成为服务商.json>) | `POST` | `/api/pay/apply` |
| [服务商信息](<服务商信息.json>) | `GET` | `/api/pay/base` |
| [更新服务商信息](<更新服务商信息.json>) | `POST` | `/api/pay/update` |
| [转账给用户](<转账给用户.json>) | `POST` | `/api/pay/transfer` |
| [创建订单](<创建订单.json>) | `POST` | `/api/pay/create` |
| [查询订单](<查询订单.json>) | `GET` | `/api/pay/query` |
| [关闭订单](<关闭订单.json>) | `PUT` | `/api/pay/close` |
| [测试回调](<测试回调.json>) | `POST` | `/api/pay/testNotify` |
| [查询用户可用萝卜](<查询用户可用萝卜.json>) | `GET` | `/api/pay/getUserCarrot` |
| [查询用户信息](<查询用户信息.json>) | `GET` | `/api/pay/getUserInfo` |
| [给用户发送邮件通知](<给用户发送邮件通知.json>) | `POST` | `/api/pay/sendNotifyEmail` |
| [查询用户签到信息](<查询用户签到信息.json>) | `GET` | `/api/pay/getUserSign` |

<!-- Postman 目录 ID: a3af5d4c-d749-4c60-94b6-aab345c323e5 -->
