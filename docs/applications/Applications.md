# Go 的四类应用场景

官方把 Go 的用途归成四类，本页给出这四类的判据与本仓对应章节。四类的划分来自 Go 官方的用例索引页，不是本仓自己编的分类。

## 一、四类场景与判据

| 场景 | 官方给的理由 | 本仓章节 |
| --- | --- | --- |
| 云与网络服务 | 快速构建、内置并发、低内存占用，容器与编排生态的主力语言 | `docs/concurrency/`、`docs/net/`、`docs/middleware/` |
| 命令行界面 | 编译成单个自包含二进制，跨架构构建只要几秒，启动接近 C/C++ | `docs/cmd/` |
| Web 开发 | 标准库自带 HTTP 服务器与模板，支持 HTTP/2 与 TLS 1.3 | `docs/gin/`、`docs/net/` |
| DevOps 与 SRE | 构建快、语法精简、自带格式化与文档生成器 | `docs/debug/`、`docs/test/`、`docs/cmd/` |

四类之外还有一条隐含线索：Go 的项目多半从「一个能跑的单二进制」起步，规模上来以后再拆成服务，所以并发与网络这两块在本仓页数最多（`docs/concurrency/` 13 页、`docs/sync/` 14 页、`docs/net/` 7 页）。

## 二、官方点名的公司与项目

| 公司 / 项目 | 用 Go 做什么 | 出处 |
| --- | --- | --- |
| Google Cloud | Kubernetes、gVisor、Knative、Istio、Anthos 全部用 Go | 云场景页 |
| Docker | 容器引擎与 CI/CD 自动化 | 云场景页、DevOps 场景页 |
| Kubernetes | 用 Go 写的容器编排系统 | 云场景页 |
| etcd | 强一致的分布式键值存储 | DevOps 场景页 |
| Cloudflare | 压缩、DNS 基础设施、SSL、压测 | Web 场景页 |
| MercadoLibre | 核心用户 API 每分钟 800 万至 1000 万次请求，响应不到 10 毫秒 | 官方案例页 |
| PayPal | 用 Go 重写 C++ 的 NoSQL 数据库，30% 集群已迁移 | 官方案例页 |
| American Express | 支付与积分两条网络的微服务 | 官方案例页 |
| Uber | AresDB 实时分析、Geofence 地理围栏、Peloton 资源调度 | 云场景页 |
| Hugo | 单二进制静态站生成器 | CLI 场景页 |

## 三、选型时该问的三个问题

1. **要不要单二进制分发**：要，就 Go 加 `docs/cmd/` 这套；CLI 场景页给了 Cobra 与 Viper 的分工。
2. **并发是 IO 密集还是 CPU 密集**：IO 密集用 goroutine 加 channel，见 `docs/concurrency/`；CPU 密集要先看 `docs/debug/PGO.md` 和 `docs/gc/GC.md`。
3. **要不要对接容器生态**：要，读 `docs/applications/CloudNative.md`，里面抄了官方对 Docker 与 Kubernetes 的原话。

## 来源

1. https://golang.google.cn/solutions/use-cases — 四类场景索引（2026-10-08 抓取）
2. https://golang.google.cn/solutions/cloud/ — 云与网络服务
3. https://golang.google.cn/solutions/clis/ — 命令行界面
4. https://golang.google.cn/solutions/webdev/ — Web 开发
5. https://golang.google.cn/solutions/devops/ — DevOps/SRE
6. https://golang.google.cn/solutions/mercadolibre — MercadoLibre 案例
7. https://golang.google.cn/solutions/paypal — PayPal 案例
