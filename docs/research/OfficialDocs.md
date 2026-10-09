# 官方文档调研

官方文档入口是 https://go.dev/doc/，本机只能访问其中国大陆镜像 https://golang.google.cn/doc/（页脚仍标注 go.dev，正文一致）。下文按镜像抓取到的页面结构说明，日期 2026-10-08。

## 一、文档总览页列出的板块

抓取到的总览页把文档切成四块，每一块在本仓的对应位置如下：

| 官方板块 | 官方页面 | 本仓对应 |
| --- | --- | --- |
| Getting Started | 安装、Getting started 教程、Create a module、多模块工作区、用 Gin 写 RESTful API、泛型教程、fuzzing 教程 | `docs/env/`、`docs/start/`、`docs/mod/`、`docs/gin/`、`docs/generics/` |
| Writing Web Applications | 一个简单 Web 应用的完整教程 | `docs/gin/`、`docs/net/` |
| Using and understanding Go | Effective Go、FAQ、编辑器插件与 IDE、诊断、GC 指南、依赖管理、fuzzing、覆盖率、PGO、json/v2 迁移 | 部分有、部分缺，见 [Coverage.md](Coverage.md) |
| References | 标准库包文档、命令文档、语言规范、Go Modules 参考、go.mod 参考、内存模型、贡献指南、发布历史、数据库教程、模块开发与发布 | `docs/mod/` 有模块部分，内存模型、发布历史、贡献指南此前无页面 |

总览页对 Go 的定义是：表达力强、简洁、干净、高效；并发机制让程序吃满多核与网络机器；类型系统支持灵活的模块化构造；编译快、带垃圾回收和运行时反射；静态类型编译型语言，写起来像动态解释型语言。这段话是官方原话的中译，可作为本仓 `docs/introduction/` 的对照口径。

## 二、Effective Go

官方把 Effective Go 标为「任何新的 Go 程序员必读」，并且要求先读 Tour 和语言规范。抓取到的目录共 16 个一级小节：

1. Introduction
2. Formatting
3. Commentary
4. Names
5. Semicolons
6. Control structures
7. Functions
8. Data
9. Initialization
10. Methods
11. Interfaces and other types
12. The blank identifier
13. Embedding
14. Concurrency
15. Errors
16. A web server

其中 40 个二级小节（如 `MixedCaps`、`Defer`、`Allocation with make`、`Share by communicating`、`A leaky buffer`、`Panic`、`Recover`）在本仓大多有对应页面，但没有一页把 16 节串起来说明「读哪一页」。已补 `docs/idioms/EffectiveGo.md`。

## 三、规范、FAQ 与 Tour

- **语言规范**（`/ref/spec`，抓取 341 KB）是唯一的语法权威，本仓 `docs/syntax/`、`docs/type/` 的页面没有一条引用它；差异表记为「有内容、无引用」。
- **FAQ**（`/doc/faq`，133 KB）回答「Go 有没有泛型、为什么没有类、为什么错误用值返回」这类问题，本仓 `docs/generics/`、`docs/oop/` 覆盖了其中两个话题。
- **A Tour of Go**（`/tour/`，官方称四段式：基础语法与数据结构、方法与接口、泛型、并发，每段结尾有练习）与本仓章节顺序一致。

## 四、发布与版本

发布历史页 `/doc/devel/release` 给出两条硬事实：

- 支持策略：每个大版本支持到出现两个更新的大版本为止。原文举例 Go 1.5 支持到 Go 1.7 发布，Go 1.6 支持到 Go 1.8 发布；安全修复只发到最近两个大版本。
- 时间线：`go1.27.0` 发布于 2026-08-19，`go1.27.1` 发布于 2026-09-01；上一个大版本 `go1.26.0` 发布于 2026-02-10，1.26 系列的补丁版本一直发到 `go1.26.8`（2026-09-01）。半年一个大版本的节奏从这两个日期可以直接看出来。

`/dl/?mode=json` 返回的稳定版列表第一项是 `go1.27.1`，与本仓 `docs/asm/Assembly.md`、`docs/net/Netpoll.md` 提到的 Go 1.27 对得上。已补 `docs/introduction/ReleaseNotes.md`。

## 五、工具与周边文档

| 主题 | 官方页面 | 本仓状态 |
| --- | --- | --- |
| GC | `/doc/gc-guide`（A Guide to the Go Garbage Collector，103 KB） | `docs/gc/GC.md`、`docs/alloc/GC.md` 有内容 |
| 内存模型 | `/ref/mem`（The Go Memory Model） | 核对时只在首页出现过一次，已补 `docs/gc/MemoryModel.md` |
| PGO | `/doc/pgo` | 核对时只在 GC 页提了一句，已补 `docs/debug/PGO.md` |
| Fuzzing | `/doc/fuzz/`、`/doc/tutorial/fuzz.html`、`/security/fuzz` | 核对时只有 go-fuzz 老工具链内容，已补原生 fuzzing `docs/test/Fuzz.md` |
| 覆盖率 | `/doc/build-cover` | `docs/test/Cover.md` 已有 |
| json/v2 | `/doc/jsonv2-migration`、`/pkg/encoding/json/v2` | 核对时无正文页，已补 `docs/encoding/JsonV2.md` |
| 构建约束 | `/pkg/go/build/`、`/pkg/cmd/go/` 的 Build constraints 小节 | 核对时无正文页，已补 `docs/start/BuildConstraint.md` |
| 编辑器 | `/gopls`、`/doc/` 的编辑器插件页 | `docs/env/vscode.md`、`docs/env/Goland.md` 覆盖工具安装 |
| 贡献指南 | `/doc/contribute` | 不适用，本仓是教程仓不是 Go 项目仓库 |

## 六、原生 fuzzing 与 json/v2 的关键口径

- fuzzing：Go 从 **1.18** 起在标准工具链里内置 fuzzing，用覆盖率引导（coverage guidance）探索输入；测试函数写成 `FuzzXxx(*testing.F)`，跑法是默认当单元测试执行、需要真 fuzz 时加 `-fuzz=FuzzTestName`；参数类型只允许 `string`、`[]byte`、整型、浮点、`bool` 这几类；原生 fuzz 测试被 OSS-Fuzz 支持。
- json/v2：`encoding/json` 不会消失，受 Go 1 兼容性承诺保护，v1 与 v2 互相兼容；v2 更严格的默认值例如非法 UTF-8 在 v1 里被静默替换为替换字符，在 v2 里直接报错；Go 1.27 与 `encoding/json/v2` 一起引入的新结构体标签，`encoding/json` 同样支持。

两条都已按原文写进 `docs/test/Fuzz.md` 与 `docs/encoding/JsonV2.md`。

## 来源

1. https://golang.google.cn/doc/ — 文档总览（Getting Started、Writing Web Applications、Using and understanding Go、References 四块）
2. https://golang.google.cn/doc/effective_go — 16 个一级小节与 40 个二级小节目录
3. https://golang.google.cn/ref/spec — 语言规范（341 KB）
4. https://golang.google.cn/doc/faq — 官方 FAQ
5. https://golang.google.cn/doc/devel/release — 支持策略与 1.26/1.27 发布日期
6. https://golang.google.cn/dl/?mode=json — 稳定版 go1.27.1
7. https://golang.google.cn/doc/pgo — PGO 定义与 Go 1.22 起 2%-14% 的基准提升
8. https://golang.google.cn/doc/fuzz/ — fuzzing 要求与运行方式
9. https://golang.google.cn/ref/mem — 内存模型 DRF-SC 表述
10. https://golang.google.cn/pkg/go/build/ — `//go:build` 与文件名约束
11. https://golang.google.cn/pkg/cmd/go/ — Build constraints 小节全文
12. https://golang.google.cn/doc/jsonv2-migration — v2 迁移口径
13. https://golang.google.cn/gopls — 语言服务器
14. https://golang.google.cn/tour/ — 四段式 Tour
