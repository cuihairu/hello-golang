# 覆盖核对差异表

比对方法：把三类来源拆成主题，逐个在本仓 368 个页面里检索（标题、H1、正文关键词），逐条映射写在下面三张表里，结果分三档。已覆盖指有专门页面，部分覆盖指只在别的页面里提过一句，缺口指检索不到对应内容。

核对日期 2026-10-08。检索用的是文件名、标题与正文正则，命中文件写在表里，可复现。

## 一、缺口与处置（13 项，全部已补）

| # | 缺口 | 来源 | 处置页 |
| --- | --- | --- | --- |
| 1 | 应用场景总览（官方四类） | `/solutions/use-cases` | `docs/applications/Applications.md` |
| 2 | 云与网络服务、云原生生态（CNCF 75%、Docker、Kubernetes） | `/solutions/cloud/` | `docs/applications/CloudNative.md` |
| 3 | CLI 场景（单二进制、Cobra、Viper） | `/solutions/clis/` | `docs/applications/CLI.md` |
| 4 | DevOps/SRE 场景（Docker、Drone、etcd、Rend） | `/solutions/devops/` | `docs/applications/DevOps.md` |
| 5 | Web 开发场景（HTTP/2、TLS 1.3、64% 代码量） | `/solutions/webdev/` | `docs/applications/Web.md` |
| 6 | 构建约束 `//go:build`（正则检索 0 命中） | `/pkg/go/build/`、`/pkg/cmd/go/` | `docs/start/BuildConstraint.md` |
| 7 | Go 内存模型（仅首页 1 处提及） | `/ref/mem` | `docs/gc/MemoryModel.md` |
| 8 | Profile-guided optimization（仅 GC 页 1 处提及） | `/doc/pgo` | `docs/debug/PGO.md` |
| 9 | 原生 fuzzing（只有 go-fuzz 老工具链内容） | `/doc/fuzz/`、`/doc/tutorial/fuzz.html` | `docs/test/Fuzz.md` |
| 10 | Effective Go 导读（2 处提及，无正文） | `/doc/effective_go` | `docs/idioms/EffectiveGo.md` |
| 11 | 版本发布与支持策略（1 处提及） | `/doc/devel/release`、`/dl/?mode=json` | `docs/introduction/ReleaseNotes.md` |
| 12 | `encoding/json/v2`（0 命中） | `/doc/jsonv2-migration`、`/pkg/encoding/json/v2` | `docs/encoding/JsonV2.md` |
| 13 | 官方安全口径与 `crypto` 标准库（无 `crypto/` 内容） | `/security/` | `docs/security/Security.md` |

## 二、官方文档板块对照

| 官方主题 | 本仓位置 | 判定 |
| --- | --- | --- |
| Getting started / Hello World | `start/Hello.md`、`start/Build.md` | 已覆盖 |
| Create a module 教程 | `mod/Init.md`、`mod/New.md` | 已覆盖 |
| 多模块工作区 | `mod/Work.md` | 已覆盖 |
| 用 Gin 写 RESTful API 教程 | `gin/` 13 页 | 已覆盖（比官方教程更细） |
| 泛型教程 | `generics/` 7 页 | 已覆盖 |
| Writing Web Applications | `gin/`、`net/` | 已覆盖 |
| 语言规范 `/ref/spec` | `syntax/`、`type/`、`func/` | 已覆盖内容，无规范引用 |
| Effective Go | `idioms/` 8 页 | 部分覆盖 → 缺口 10 |
| FAQ | `generics/`、`oop/` | 部分覆盖 |
| 标准库包文档 | 42 个目录按包分类 | 已覆盖 |
| Go Tour 四段式 | `start/` → `oop/` → `generics/` → `concurrency/` | 已覆盖 |
| 语言规范术语（方法、接口、嵌入） | `oop/` 8 页 | 已覆盖 |
| 模块依赖管理 | `mod/` 9 页（含 `Vendor.md`、`Get.md`） | 已覆盖 |
| go.mod 参考 | `mod/Mod.md` | 已覆盖 |
| 模块发布与版本号 | `mod/Mod.md` 提了语义化版本 | 部分覆盖（教程仓不发布模块，不补） |
| 内存模型 | 首页 1 处 | 缺口 7 |
| GC 指南 | `gc/GC.md`、`alloc/GC.md` | 已覆盖 |
| 诊断 diagnostics | `debug/` 7 页（Delve、GDB、pprof、expvar） | 已覆盖 |
| 覆盖率 | `test/Cover.md` | 已覆盖 |
| PGO | `gc/GC.md` 1 句 | 缺口 8 |
| Fuzzing | `test/Lib.md`（go-fuzz） | 缺口 9 |
| json/v2 迁移 | 0 命中 | 缺口 12 |
| 构建约束 | 0 命中 | 缺口 6 |
| 数据库教程（连接、执行、预处理、事务、取消、连接池、防注入） | `db/` 19 页（`Tx.md`、`ConnectPool.md`、`Security.md` 等） | 已覆盖 |
| 编辑器与 gopls | `env/vscode.md`、`env/Goland.md`、`env/Vim.md` | 已覆盖 |
| 贡献指南 `/doc/contribute` | — | 不适用（本仓是教程仓，不向 Go 项目提交代码），不补 |
| 发布历史与支持策略 | 1 处提及 | 缺口 11 |
| 安全（漏洞库、fuzzing、加密库、FIPS 140-3） | 0 处 `crypto/` 内容 | 缺口 13 |
| gopls / goimports / godoc 工具安装 | `env/Tools.md`、`mod/Get.md` | 已覆盖 |

## 三、同类书籍章节对照

| 书里常设的章节 | 本仓位置 | 判定 |
| --- | --- | --- |
| 语法与数据类型 | `syntax/` 12 页、`type/` 26 页 | 已覆盖 |
| 函数、方法 | `func/` 10 页、`oop/` 8 页 | 已覆盖 |
| 接口与类型断言 | `type/Interface.md`、`oop/InterfaceImpl.md`、`type/Assertion.md` | 已覆盖 |
| 包与工程 | `mod/`、`start/Structure.md` | 已覆盖 |
| 测试（表驱动、基准、模糊） | `test/` 9 页，表驱动在 `test/Practice.md` | 部分覆盖（fuzzing → 缺口 9） |
| 并发（goroutine、channel、同步原语） | `concurrency/` 13 页 + `sync/` 14 页 | 已覆盖，密度最高 |
| 并发原语的选择与代价 | `sync/Mutex.md`、`sync/RWMutex.md` 分散讲 | 部分覆盖（不补，分散讲也成立） |
| 反射与元编程 | `reflection/Reflection.md` 1 页 | 部分覆盖（深度不如《Go语言设计与实现》，暂不补） |
| cgo 与 C 互操作 | `cgo/CGO.md` 1 页 | 部分覆盖 |
| 汇编与底层 | `asm/Assembly.md` 1 页 | 部分覆盖 |
| 分布式与 RPC（gRPC、Protobuf） | `distribution/Readme.md`、`middleware/` | 部分覆盖（`grpc.io` 网络不可达，暂不补独立页） |
| 性能剖析与调优 | `debug/Pprof.md`、`gc/GC.md` | 已覆盖 |
| Web 框架 | `gin/`、`middleware/` | 已覆盖 |
| CLI 框架（Cobra、Viper） | `cmd/` 讲 flag，`gin/Config.md` 提了 Viper | 部分覆盖 → 缺口 3 |
| 容器与编排（Docker、Kubernetes） | 17 处散落提及，无正文页 | 部分覆盖 → 缺口 2 |

## 四、应用场景对照

| 场景 | 本仓位置 | 判定 |
| --- | --- | --- |
| 云与网络服务 | 无 | 缺口 2 |
| CLI | `cmd/` 6 页（设计、flag、解析） | 部分覆盖 → 缺口 3 |
| Web 开发 | `gin/`、`net/`、`middleware/` | 部分覆盖 → 缺口 5 |
| DevOps/SRE | 无 | 缺口 4 |
| 应用场景总览与公司案例 | 无 | 缺口 1 |
| 分布式系统 | `distribution/Readme.md` 1 页 | 部分覆盖（不补，内容自洽） |
| 中间件（Kafka、消息队列、Redis） | `middleware/`、`redis/` 11 页 | 已覆盖 |
| 日志聚合（fluentd） | `log/Aggregation.md` | 已覆盖 |

## 五、核对中发现并修订的问题

| 位置 | 问题 | 处置 |
| --- | --- | --- |
| `env/Install.md`、`env/Goland.md`、`env/Vim.md`、`env/vscode.md` | 6 处下载链接指向 `https://golang.org/dl/`，官方下载入口已统一为 `go.dev` | 改为 `https://go.dev/dl/` |
| `idioms/Idioms.md` | Effective Go 链接指向 `golang.org/doc/effective_go.html` 旧路径 | 改为 `https://go.dev/doc/effective_go` |
| 版本表述 | 需要确认本仓提到的 Go 1.25/1.26/1.27 是否与官方发布线一致 | 官方 `go1.27.0`（2026-08-19）、`go1.27.1`（2026-09-01）在稳定线上，本仓表述保留 |
| `docs/research/README.md` | 目录初稿链接写错为 `Coverge.md` | 改为 `Coverage.md` |
| `SUMMARY.md` | `[高级应用](gin/Advanced.md)` 大小写与实际文件 `gin/advanced.md` 不符 | 改为 `gin/advanced.md` |
| `.vitepress/config.mts` | 注释写「49 个顶层章节」，与加完调研与应用场景后的 51 个分组不符 | 注释改为 51 个顶层分组 |

## 六、不补的三项及理由

1. **贡献指南**：面向向 Go 项目提交代码的人，本仓是教程仓，写不出有依据的内容。
2. **模块发布工作流**：本仓不发布对外模块，`mod/Mod.md` 已提到语义化版本与 major 版本路径，够用。
3. **gRPC 独立页**：`grpc.io`、`protobuf.dev` 在本机网络不可达，官方云场景页只有一句生态提及，写不出带来源的技术页。

## 来源

1. https://golang.google.cn/doc/ — 官方文档总览
2. https://golang.google.cn/doc/effective_go — Effective Go 目录
3. https://golang.google.cn/pkg/go/build/ — 构建约束定义
4. https://golang.google.cn/pkg/cmd/go/ — Build constraints 小节
5. https://golang.google.cn/ref/mem — 内存模型
6. https://golang.google.cn/doc/pgo — PGO
7. https://golang.google.cn/doc/fuzz/ — fuzzing
8. https://golang.google.cn/doc/jsonv2-migration — json/v2
9. https://golang.google.cn/doc/devel/release — 发布历史与支持策略
10. https://golang.google.cn/dl/?mode=json — 稳定版 go1.27.1
11. https://golang.google.cn/security/ — 官方安全页
12. https://golang.google.cn/solutions/use-cases — 四类场景
13. https://golang.google.cn/solutions/cloud/ 、`/clis/`、`/webdev/`、`/devops/` — 四类场景详情
14. https://book.douban.com/tag/Go — 书籍章节对照所用书单
