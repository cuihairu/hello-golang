# 应用场景调研

官方把 Go 的用途归成四类，索引页是 `/solutions/use-cases`：**云与网络服务、命令行界面（CLI）、Web 开发、DevOps 与 SRE**。本仓此前没有任何一页讲这四类场景，只有散落的技术内容（`docs/gin/` 讲 Web 框架、`docs/cmd/` 讲 flag、`docs/middleware/` 讲消息队列）。本篇把四类场景的官方口径与数字抄下来，缺口部分已建成 `docs/applications/` 下的五页。

抓取日期 2026-10-08，全部来自 `golang.google.cn` 镜像。

## 一、云与网络服务

官方页面标题是 Go for Cloud & Network Services，页面标注日期 2019 年 10 月 4 日。要点：

- 官方原话：**CNCF 中超过 75% 的项目用 Go 写成**（over 75 percent of projects in the Cloud Native Computing Foundation are written in Go）。这是本仓可以引用的最硬的云原生占比数字，引用时要带上页面日期。
- 快速启动与低内存占用，官方把它对到 pay-as-you-go 和 serverless 部署的成本上。
- 生态清单：三大云厂商（GCP、AWS、Azure）都有 Go API；API 工具用 Swagger，传输层用 protocol buffers 与 gRPC，监控用 OpenCensus，ORM 用 gORM，认证用 JWT；服务框架有 Go Kit、Go Micro、Gizmo。
- 工具链里自带 race 检测、基准测试与 profiling、代码生成、静态分析。
- 官方点名的两个容器项目：**Docker**（把软件、库、配置打包进容器，由 Docker Engine 运行，共享一个操作系统内核，比虚拟机省资源）与 **Kubernetes**（用 Go 写的容器编排系统）。
- 页面列出的用户：Google Cloud（Kubernetes、gVisor、Knative、Istio、Anthos 都在用 Go）、Capital One（Credit Offers API，原话是「没打算在没有 Go 的情况下上 serverless」）、Dropbox（2013 年起把性能关键后端从 Python 迁到 Go，如今大部分基础设施是 Go）、纽约时报（后端服务与开源工具集 Gizmo）、Twitch（直播与聊天系统，引用了低延迟 GC）、Uber（实时分析引擎 AresDB、地理围栏 Geofence、资源调度 Peloton）。

## 二、命令行界面

官方页面标题 Go for CLIs。要点：

- 编译成**单个自包含二进制**，不依赖任何已有库、运行时或依赖；启动时间接近 C/C++。
- 从一台 Windows 或 Mac 笔记本出发，几秒钟就能构建出 Go 支持的几十种架构与操作系统上的程序，官方原话是「没有别的编译型语言能构建得这么可移植、这么快」。
- 框架层：**Cobra** 既是库也是代码生成器，官方列出用它的项目有 CoreOS、Delve、Docker、Git LFS、Hugo、Kubernetes；**Viper** 管配置，支持嵌套结构与环境变量，两者配套使用。
- 案例：Comcast 用 Go 写高频站点发布订阅的 CLI 客户端与 Apache Pulsar 客户端库；GitHub 用 Go 写命令行工具包装 git；Hugo 是用 Go 写的静态站生成器，单二进制安装是它流行的原因之一。

## 三、Web 开发

官方页面标题 Go for Web Development。要点：

- 标准库自带 HTTP 服务器与模板库，支持 HTTP/2、MySQL/MongoDB/Elasticsearch、TLS 1.3。
- 单二进制、零依赖带来的跨平台部署速度；第三方框架在多数场景不是必需。
- 一家公司（Hexact）CTO 的五条理由里有具体数字：goroutine 处理内部请求，资源占用比 Python 线程**便宜 10 倍**；重写到 Go 后**代码量少了 64%**。
- 项目：Caddy 2（自动 HTTPS 的 Web 服务器，TLS 栈来自 Go 标准库）、Cloudflare（压缩、DNS 基础设施、SSL、压测）、英国政府 gov.uk 的 HTTP 基础设施、Hugo、Mattermost、Medium（社交图、图片服务）、The Economist。

## 四、DevOps 与 SRE

官方页面标题 Go for DevOps & Site Reliability Engineering。要点：

- SRE 起源于 Google，目标是让大规模站点更可靠、更高效、更可扩展；Amazon、Netflix 后来也采用了这套实践。
- 标准库覆盖 HTTP、文件 I/O、时间、正则、exec、JSON/CSV，写小脚本就直接进业务逻辑；静态类型加显式错误处理让脚本更皮实。
- godoc 自动生成文档，降低维护成本。
- 项目：**Docker**（支撑 CI/CD 的自动化与部署）、**Drone**（容器上的持续交付系统）、**etcd**（强一致的分布式键值存储）、IBM（通过 Docker 与 Kubernetes 使用 Go）、Netflix（缓存服务 Rend 管理全球复制的个性化数据）、Microsoft（Azure Red Hat OpenShift 服务）。

## 五、三则官方案例的数字

| 公司 | 页面日期 | 关键事实 |
| --- | --- | --- |
| American Express | 2019-12-19 | 支付与积分两条网络用 Go；工程总监的说法是认知负担低，新代码库上手快，多数 Go 代码长得差不多 |
| PayPal | 2020-06-01 | 把 C++ 写的 NoSQL 数据库用 Go 重写，团队花六个月学习 Go 并重写，**30% 的集群已迁到新数据库**；理由是 goroutine 与 channel 把多线程的复杂度收住了 |
| MercadoLibre | — | 拉美最大的电商生态，覆盖 18 个国家；2015 年起从 Groovy/Grails 迁到 Go；核心用户 API 平均**每分钟 800 万至 1000 万次请求**（原文 eight to ten million requests per minute），响应时间**不到 10 毫秒**（原文 less than ten milliseconds） |

## 六、四类场景对本仓的意义

1. 云与网络服务对应 `docs/concurrency/`、`docs/net/`、`docs/middleware/`，缺一页把 Docker、Kubernetes、CNCF 占比这些背景接起来，已补 `docs/applications/CloudNative.md`。
2. CLI 对应 `docs/cmd/`（flag 与命令行设计），缺 Cobra/Viper 与单二进制特性的场景说明，已补 `docs/applications/CLI.md`。
3. Web 对应 `docs/gin/`、`docs/net/`，已补 `docs/applications/Web.md`。
4. DevOps/SRE 无对应目录，已补 `docs/applications/DevOps.md`。

## 来源

1. https://golang.google.cn/solutions/use-cases — 四类场景索引
2. https://golang.google.cn/solutions/cloud/ — 云与网络服务（含 CNCF 75%、Docker、Kubernetes、Dropbox、Uber 等）
3. https://golang.google.cn/solutions/clis/ — CLI 场景（单二进制、Cobra、Viper、Hugo、GitHub CLI）
4. https://golang.google.cn/solutions/webdev/ — Web 开发（HTTP/2、TLS 1.3、10 倍与 64% 两个数字）
5. https://golang.google.cn/solutions/devops/ — DevOps/SRE（Docker、Drone、etcd、Netflix Rend）
6. https://golang.google.cn/solutions/americanexpress — American Express 案例
7. https://golang.google.cn/solutions/paypal — PayPal 案例（六个月、30% 集群）
8. https://golang.google.cn/solutions/mercadolibre — MercadoLibre 案例（18 国、每分钟 800 万至 1000 万请求、10 毫秒）
9. https://golang.google.cn/security/ — 官方安全页（漏洞库、fuzzing、加密库、FIPS 140-3）
