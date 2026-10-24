# Effective Go：16 节与本站页面对照

官方将 Effective Go 称为「任何新的 Go 程序员必读」，并建议先读 Tour 和语言规范。本仓 `docs/zh/idioms/`、`docs/zh/naming/` 里各提过一次链接，我把 16 节与本站页面的对应关系整理在下表，资料抓取于 2026-10-08。

## 一、16 节与本仓页面对照

| Effective Go 小节 | 讲什么 | 本仓页面 |
| --- | --- | --- |
| Introduction | Go 的设计取舍 | `docs/zh/introduction/Feature.md` |
| Formatting | `gofmt` 强制统一格式 | `docs/zh/naming/Naming.md`、`docs/zh/env/Tools.md` |
| Commentary | 包注释与 `godoc` | `docs/zh/mod/Package.md`、`docs/zh/env/Tools.md` |
| Names | 命名、MixedCaps、导出规则 | `docs/zh/naming/IdentifierNamingRules.md`、`docs/zh/idioms/Idioms.md` |
| Semicolons | 自动分号插入规则 | `docs/zh/syntax/` 控制流各页 |
| Control structures | if/for/switch、type switch | `docs/zh/syntax/Conditional.md`、`docs/zh/syntax/Loop.md`、`docs/zh/type/Switch.md` |
| Functions | 多返回值、命名返回值、defer | `docs/zh/func/MultipleReturnValues.md`、`docs/zh/func/Defer.md` |
| Data | 数组、切片、map、打印、append、常量、变量 | `docs/zh/type/` 与 `docs/zh/const/` 对应页 |
| Initialization | 初始化、`init` 函数、复合字面量 | `docs/zh/const/Const.md`、`docs/zh/var/VarAndInit.md` |
| Methods | 方法、指针与值接收者 | `docs/zh/oop/Methods.md`、`docs/zh/oop/PointerReceiver.md` |
| Interfaces and other types | 接口命名、断言、泛化 | `docs/zh/oop/InterfaceImpl.md`、`docs/zh/type/Assertion.md` |
| The blank identifier | 空标识符、多值赋值、导入副作用 | `docs/zh/idioms/BlankIdentifier.md` |
| Embedding | 嵌入扩展接口与结构体 | `docs/zh/oop/Embedding.md` |
| Concurrency | Share by communicating、goroutine、channel、并行化 | `docs/zh/concurrency/CSP.md`、`docs/zh/concurrency/Goroutine.md`、`docs/zh/concurrency/Chan.md` |
| Errors | panic、recover、错误值 | `docs/zh/error/Errors.md`、`docs/zh/error/PanicAndRecover.md` |
| A web server | 一个完整的 HTTP 服务器示例 | `docs/zh/net/Intro.md`、`docs/zh/gin/` |

40 个二级小节里，本仓有独立内容的重点是 `Defer`、`Allocation with make`、`Interfaces`、`Panic`、`Recover`、`MixedCaps`；讲得比 Effective Go 更细的是 `GMP 调度器`、`Channel 实现` 这两页，它们超出原文范围。

## 二、官方阅读建议与本站页面

官方的建议是 Tour → 语言规范 → Effective Go。按官方建议对照本站页面：

1. 基础语法与数据类型：`docs/zh/start/Hello.md`、`docs/zh/syntax/`、`docs/zh/type/`。
2. 方法、接口与包：`docs/zh/oop/`、`docs/zh/mod/`。
3. 测试：`docs/zh/test/`（Effective Go 没有专章讨论测试）。
4. 并发：`docs/zh/concurrency/`，对应 Concurrency 一节。
5. Effective Go 原文：本页作为对应索引。

## 三、两处官方自己的提醒

- 语言规范（`/ref/spec`）和 Tour 应该先读，Effective Go 是在它们之上的写法建议，不是语法定义。
- 官方对 A web server 那节的说法是：它展示的是一个小而完整的程序，重点在组织方式，不在于生产可用性。

## 来源

1. https://golang.google.cn/doc/effective_go — 16 个一级小节与 40 个二级小节目录，以及「a must read for any new Go programmer」的定位（2026-10-08 抓取）
2. https://golang.google.cn/doc/ — 文档总览中 Effective Go 的排序说明（先读 tour 与 spec）
3. https://golang.google.cn/tour/ — Tour 四段式结构

## 参考资料

- [Effective Go（官方）](https://go.dev/doc/effective_go)

<!-- BACKLINKS-AUTO -->
## 相关页面

- [BlankIdentifier](BlankIdentifier.md)
- [CommaOk](CommaOk.md)
- [Idioms](Idioms.md)
- [Labels](Labels.md)
- [Range](Range.md)
- [ShortVarDecl](ShortVarDecl.md)
- [knowledge](/zh/knowledge.md)
