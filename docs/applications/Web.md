# Web 开发：标准库够用，框架是可选项

Web 开发是官方四类场景之一。本页是官方 Web 场景页的中文摘录与本仓导读，抓取于 2026-10-08。

## 一、官方给的能力清单

- 标准库自带易用、安全、高性能的 Web 服务器和模板库。
- 支持 HTTP/2、MySQL、MongoDB、Elasticsearch，以及 TLS 1.3 这类新的加密标准。
- 单个小体积二进制、零依赖，跨平台部署快；官方把这条放在「跨平台部署」标题下。
- 可以原生跑在 Google App Engine 与 Google Cloud Run 上，也可以跑在任何环境、云或操作系统上。

## 二、两个有出处的数字

一家公司（Hexact）CTO 列的五条换语言理由里有两条带数字：

1. goroutine 处理内部请求，资源占用比 Python 线程**便宜 10 倍**（10x cheaper in resources than Python Threads）。
2. 全部项目重写到 Go 之后，**代码量少了 64%**（64 percent less code）。

另外三条是静态链接成单二进制、静态类型系统适合大规模应用、多数场景不需要第三方框架。这五条来自官方页面引用的原话，不是本仓的测试结果。

## 三、官方列的项目

| 项目 | 说明 |
| --- | --- |
| Caddy 2 | 自动 HTTPS 的开源 Web 服务器，TLS 栈来自 Go 标准库 |
| Cloudflare | 压缩高延迟 HTTP 连接、整套 DNS 基础设施、SSL、压测 |
| gov.uk | 英国政府 HTTP 基础设施，选 Go 的理由是并发模型让 IO 密集应用的性能容易拿到 |
| Hugo | 静态站生成器 |
| Mattermost | 开源团队沟通平台，Go 加 React |
| Medium | 社交图、图片服务等辅助服务 |
| The Economist | 用 Go 服务支撑多渠道内容分发 |

## 四、和本仓的接法

| 需求 | 本仓页面 |
| --- | --- |
| 起 HTTP 服务 | `docs/net/Intro.md`、`docs/net/Socket.md` |
| 路由与中间件 | `docs/gin/Route.md`、`docs/gin/Middleware.md` |
| 请求与响应处理 | `docs/gin/Request.md`、`docs/gin/Response.md` |
| HTML 与文本模板 | `docs/type/HtmlTemplate.md`、`docs/type/Template.md` |
| JSON 编解码 | `docs/encoding/JSON.md`、`docs/encoding/JsonV2.md` |
| 并发压测 | `docs/test/Benchmark.md`、`docs/sync/` |
| 上游超时与取消 | `docs/sync/Context.md` |

标准库 `net/http` 写到什么程度再上框架，本仓 `docs/gin/` 13 页之前没有交代边界；官方页面的说法是多数场景不需要第三方框架，框架的价值在路由、参数绑定和中间件组织上。这个判断可以拿来当分界线。

## 来源

1. https://golang.google.cn/solutions/webdev/ — Go for Web Development（HTTP/2、TLS 1.3、10 倍、64%、项目清单，2026-10-08 抓取）
2. https://golang.google.cn/solutions/use-cases — 四类场景索引
3. https://golang.google.cn/doc/ — Getting Started 下的 Writing Web Applications 教程入口
