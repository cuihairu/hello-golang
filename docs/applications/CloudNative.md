# 云与网络服务：CNCF 里超过 75% 的项目用 Go

这一页抄的是官方云场景页的口径，日期 2019-10-04，抓取于 2026-10-08。引用那个 75% 的数字时要把页面日期一起带上，它是官方页面上的原话，不是本仓的估算。

## 一、官方给的三个理由

1. **开发周期与服务器性能之间不必二选一**：构建快，迭代快，内存与 CPU 占用低，服务器启动即用，官方特别点了 pay-as-you-go 和 serverless 这两种按量计费的部署形态。
2. **针对现代云的标准惯用 API**：标准库里 HTTP 服务端与客户端、JSON/XML 解析、SQL 数据库、加解密都在，运行时自带 race 检测、基准测试与 profiling、代码生成、静态分析。
3. **低延迟且不需要调参**：官方原话是 low-latency and "no knob" tuning。

## 二、生态清单

| 用途 | 官方列举的方案 |
| --- | --- |
| 云厂商 SDK | GCP、AWS、Azure 都有 Go API |
| API 工具 | Swagger |
| 传输 | protocol buffers、gRPC |
| 监控 | OpenCensus |
| ORM | gORM |
| 认证 | JWT |
| 服务框架 | Go Kit、Go Micro、Gizmo |
| Web 框架 | Echo、Flamingo、Gin、Gorilla |
| 路由 | net/http、httprouter、gorilla/mux、chi |
| 数据库 | database/sql、mongo-driver、go-elasticsearch、GORM、Bleve、CockroachDB |

## 三、容器两件套

官方页面对这两个项目的描述值得直接读：

- **Docker**：把软件、库和配置文件打包进容器，由 Docker Engine 托管，跑在同一个操作系统内核上，因此比虚拟机占的系统资源少。云上的 Go 开发者用 Docker 管理代码与多平台构建。
- **Kubernetes**：用 Go 写的容器编排系统，用来自动化 Web 应用的部署。云开发者靠它通过 API 管理容器，把规模上来后的复杂度收住。

本仓对应的实操内容在 `docs/start/Structure.md`（构建产物组织）和 `docs/net/`（服务间通信），Kubernetes 本身不在本仓范围内。

## 四、公司侧的数字

- 官方云场景页原话：CNCF 中**超过 75% 的项目用 Go 写成**。
- Google Cloud 的 Kubernetes、gVisor、Knative、Istio、Anthos 都是 Go 写的。
- Dropbox 在 2013 年决定把性能关键的后端从 Python 迁到 Go，如今公司大部分基础设施是 Go。
- Capital One 用 Go 做 Credit Offers API，工程团队在 serverless 架构上也选了 Go。
- Twitch 的直播与聊天系统用 Go，官方在这条下面挂的链接标题是 Go's march to low-latency GC。
- Uber 的实时分析引擎 AresDB、地理围栏服务 Geofence、资源调度器 Peloton 都用 Go。

## 五、和本仓的关系

写云上服务时，本仓这几页是直接的前置知识：

| 需求 | 读哪页 |
| --- | --- |
| 起 goroutine 与 channel | `docs/concurrency/` |
| 服务间长连接与多路复用 | `docs/net/Socket.md`、`docs/net/Netpoll.md` |
| 中间件与消息队列 | `docs/middleware/` |
| 内存上限怎么设 | `docs/alloc/GC.md`（`GOMEMLIMIT`） |
| 拿生产数据做优化 | `docs/debug/PGO.md` |

## 来源

1. https://golang.google.cn/solutions/cloud/ — Go for Cloud & Network Services，页面日期 2019-10-04，含 75% 占比、Docker、Kubernetes 与公司清单（2026-10-08 抓取）
2. https://golang.google.cn/solutions/use-cases — 四类场景索引
3. https://golang.google.cn/solutions/paypal — PayPal 迁移与 30% 集群数字
4. https://golang.google.cn/solutions/mercadolibre — MercadoLibre 请求量与响应时间
