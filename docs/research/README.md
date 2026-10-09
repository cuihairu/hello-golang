# 调研总览

本目录记录一次针对本仓的外部知识调查：先取同类经典书籍、Go 官方文档、官方公布的应用场景三类材料，再把三类材料拆成可核对的主题，逐条比对本仓 `docs/` 下已有的 368 个页面，最后把缺口写成新页面。

抓取与核对日期：2026-10-08。

## 三类材料怎么取的

- **官方文档**：`go.dev` 在本机网络不可达，改走官方中国大陆镜像 `golang.google.cn`，页面页脚仍标注 `go.dev`，内容与主站一致。取回的原文包括文档总览、Effective Go、语言规范、发布历史、PGO、fuzzing、内存模型、`go` 命令文档、安全页、四类应用场景页与三则公司案例。
- **同类书籍**：取豆瓣读书 `Go` 标签的 4 页列表（共 100 条条目），再用搜狗、360 搜索聚合的豆瓣与当当条目补《Go程序设计语言》这类不在标签首页的书。书名、作者、出版社、出版时间、豆瓣评分全部来自抓取到的页面原文，没有凭记忆填。
- **应用场景**：全部取自官方 `solutions/` 页面（云与网络服务、CLI、Web 开发、DevOps/SRE）和三则官方案例（American Express、PayPal、MercadoLibre），数字与引语都能在原文里找到。

## 四篇正文

| 文档 | 内容 |
| --- | --- |
| [Books.md](Books.md) | 同类经典书籍分层书单，附作者、出版社、年份、评分、侧重点 |
| [OfficialDocs.md](OfficialDocs.md) | 官方文档的板块结构与各板块对本仓的意义 |
| [Scenarios.md](Scenarios.md) | 官方口径的四类应用场景与公司案例数字 |
| [Coverage.md](Coverage.md) | 覆盖核对差异表：来源主题 → 本仓页面 → 判定 → 处置 |

差异表里判定为「缺口」的 13 项，已各自补成正文页，分布在 `docs/applications/`、`docs/start/`、`docs/gc/`、`docs/debug/`、`docs/test/`、`docs/idioms/`、`docs/introduction/`、`docs/encoding/`、`docs/security/`。

## 三个先说清的事实

1. 官方当前稳定版是 **go1.27.1**（`go1.27.0` 于 2026-08-19 发布，`go1.27.1` 于 2026-09-01 发布），本仓版本相关的表述与此对得上。
2. 官方支持策略是**每个大版本支持到出现两个更新的大版本为止**（Release Policy 原文），所以 1.26、1.27 在 1.28 发布后仍受支持。
3. 本仓页面按主题分类齐全（语法、类型、并发、同步、测试、数据库、Gin 等目录，核对日 42 个，补完应用场景与调研目录后 44 个）——语言知识不缺，缺的是**官方文档入口类页面**（内存模型、PGO、fuzzing、构建约束、json/v2、安全）和**应用场景类页面**（四类场景此前一个都没有）。

## 来源清单

1. https://golang.google.cn/doc/ — 官方文档总览
2. https://golang.google.cn/doc/effective_go — Effective Go
3. https://golang.google.cn/ref/spec — Go 语言规范
4. https://golang.google.cn/doc/faq — 官方 FAQ
5. https://golang.google.cn/doc/devel/release — 发布历史与支持策略
6. https://golang.google.cn/dl/?mode=json — 当前稳定版列表
7. https://golang.google.cn/doc/pgo — Profile-guided optimization
8. https://golang.google.cn/doc/fuzz/ — Go 原生 fuzzing
9. https://golang.google.cn/ref/mem — Go 内存模型
10. https://golang.google.cn/pkg/go/build/ — 构建约束说明
11. https://golang.google.cn/pkg/cmd/go/ — `go` 命令与 `Build constraints` 小节
12. https://golang.google.cn/doc/jsonv2-migration — encoding/json/v2 迁移指南
13. https://golang.google.cn/security/ — 官方安全页
14. https://golang.google.cn/solutions/use-cases — 四类应用场景索引
15. https://golang.google.cn/solutions/cloud/ — 云与网络服务场景
16. https://golang.google.cn/solutions/clis/ — CLI 场景
17. https://golang.google.cn/solutions/webdev/ — Web 开发场景
18. https://golang.google.cn/solutions/devops/ — DevOps/SRE 场景
19. https://golang.google.cn/solutions/americanexpress — American Express 案例
20. https://golang.google.cn/solutions/paypal — PayPal 案例
21. https://golang.google.cn/solutions/mercadolibre — MercadoLibre 案例
22. https://golang.google.cn/tour/ — A Tour of Go
23. https://golang.google.cn/doc/code — How to write Go code
24. https://golang.google.cn/gopls — gopls 编辑器语言服务器
25. https://book.douban.com/tag/Go — 豆瓣读书 Go 标签（第 1-4 页）
26. 搜狗搜索、360 搜索聚合的豆瓣与当当条目（《Go程序设计语言》等书目信息）

注意：`go.dev`、`pkg.go.dev`、`github.com`、`grpc.io`、`kubernetes.io` 在本机网络均无法建立 TLS 连接，因此本目录所有引用都指向可复现抓取的镜像或国内站点；镜像取不到的书目信息，标注了它来自搜索引擎聚合的哪一家条目。
