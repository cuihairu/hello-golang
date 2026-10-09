# 版本发布与支持策略

Go 的版本节奏和支撑策略决定你该追哪个版本、什么时候升级。本仓此前只有一处提到发布说明。内容取自官方发布历史页与下载接口，抓取于 2026-10-08。

## 一、两条硬规则

1. **支持到落后两个大版本**：官方原话是每个大版本支持到出现两个更新的大版本为止。文档给的例子是 Go 1.5 支持到 Go 1.7 发布，Go 1.6 支持到 Go 1.8 发布。
2. **安全修复只覆盖最近两个大版本**：官方安全页用的也是同一条口径，所以留在老版本上等于不再收到安全补丁。

补丁版本（minor revision）按需发布，用于修关键问题、包括关键安全问题。

## 二、当前的版本线

| 版本 | 发布日期 | 说明 |
| --- | --- | --- |
| `go1.27.0` | 2026-08-19 | 当前大版本 |
| `go1.27.1` | 2026-09-01 | 修 cgo、编译器、运行时、`go fix`、`database/sql`、`debug/elf`、`encoding/json`、`net/http`、`os`、`simd` 等 |
| `go1.26.0` | 2026-02-10 | 上一个大版本 |
| `go1.26.1` - `go1.26.8` | 2026-03-05 至 2026-09-01 | 含多批安全修复（`crypto/x509`、`crypto/tls`、`html/template`、`net/url`、`net/http` 等） |

从 2026-02-10 和 2026-08-19 两个日期能直接看出节奏：**半年一个大版本**。`/dl/?mode=json` 返回的稳定版列表第一项是 `go1.27.1`，与本页一致。

## 三、实际怎么选

| 场景 | 建议 |
| --- | --- |
| 新项目 | 直接用当前稳定版，本页抓取时是 `go1.27.1` |
| 生产在跑 | 跟住当前大版本的最新补丁版本，安全修复集中在这里 |
| 依赖要求的最低版本更高 | 看依赖的 `go.mod`，必要时按 `docs/env/Tools.md` 里的 toolchain 用法升级 |
| 想用新语言特性 | 大版本标签从 1.1 起每年累积两个，见 `docs/start/BuildConstraint.md` 的 `go1.N` 标签 |

`go.mod` 里的 `go` 指令决定可用的语言版本，本仓 `docs/mod/Mod.md` 讲过；构建约束里带大版本标签时，语言版本取标签隐含的最低版本，规则在 `docs/start/BuildConstraint.md`。

## 四、本仓页面里的版本表述核对

这次核对把本仓提到的版本与官方发布线对了一遍：

| 页面 | 表述 | 核对结果 |
| --- | --- | --- |
| `docs/concurrency/WaitGroup.md` | Go 1.25 起 `sync.WaitGroup` 有 `Go` 方法 | 1.25 在支持线内 |
| `docs/net/Netpoll.md` | 提到 Go 1.26、1.27 | 与 `go1.26.0`、`go1.27.0` 对得上 |
| `docs/asm/Assembly.md` | 用 Go 1.27 生成的汇编举例 | 与当前稳定线一致 |
| `docs/alloc/GC.md` | `GOMEMLIMIT` 是 Go 1.19 引入 | 与发布历史一致 |
| `docs/debug/Utils.md` | `log/slog` 是 Go 1.21 引入 | 与发布历史一致 |

## 来源

1. https://golang.google.cn/doc/devel/release — Release History：支持策略、`go1.27.0`（2026-08-19）、`go1.27.1`（2026-09-01）、`go1.26.0`（2026-02-10）及各补丁版本日期
2. https://golang.google.cn/dl/?mode=json — 稳定版列表，第一项 `go1.27.1`
3. https://golang.google.cn/security/ — 「我们对最近两个大版本发布安全修复」
4. https://golang.google.cn/doc/ — 文档总览中的 Release Notes 入口
