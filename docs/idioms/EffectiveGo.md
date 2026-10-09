# Effective Go 导读：16 节各对应本仓哪一页

Effective Go 是官方文档里被标成「任何新的 Go 程序员必读」的那一篇，官方还要求先读 Tour 和语言规范再读它。本仓 `docs/idioms/`、`docs/naming/` 里各提过一次链接，但没有一页说明这 16 节怎么对照本仓来读。抓取于 2026-10-08。

## 一、16 节与本仓页面对照

| Effective Go 小节 | 讲什么 | 本仓页面 |
| --- | --- | --- |
| Introduction | Go 的设计取舍 | `docs/introduction/Feature.md` |
| Formatting | `gofmt` 强制统一格式 | `docs/naming/Naming.md`、`docs/env/Tools.md` |
| Commentary | 包注释与 `godoc` | `docs/mod/Package.md`、`docs/env/Tools.md` |
| Names | 命名、MixedCaps、导出规则 | `docs/naming/IdentifierNamingRules.md`、`docs/idioms/Idioms.md` |
| Semicolons | 自动分号插入规则 | `docs/syntax/` 控制流各页 |
| Control structures | if/for/switch、type switch | `docs/syntax/Conditional.md`、`docs/syntax/Loop.md`、`docs/type/Switch.md` |
| Functions | 多返回值、命名返回值、defer | `docs/func/MultipleReturnValues.md`、`docs/func/Defer.md` |
| Data | 数组、切片、map、打印、append、常量、变量 | `docs/type/` 与 `docs/const/` 对应页 |
| Initialization | 初始化、`init` 函数、复合字面量 | `docs/const/Const.md`、`docs/var/VarAndInit.md` |
| Methods | 方法、指针与值接收者 | `docs/oop/Methods.md`、`docs/oop/PointerReceiver.md` |
| Interfaces and other types | 接口命名、断言、泛化 | `docs/oop/InterfaceImpl.md`、`docs/type/Assertion.md` |
| The blank identifier | 空标识符、多值赋值、导入副作用 | `docs/idioms/BlankIdentifier.md` |
| Embedding | 嵌入扩展接口与结构体 | `docs/oop/Embedding.md` |
| Concurrency | Share by communicating、goroutine、channel、并行化 | `docs/concurrency/CSP.md`、`docs/concurrency/Goroutine.md`、`docs/concurrency/Chan.md` |
| Errors | panic、recover、错误值 | `docs/error/Errors.md`、`docs/error/PanicAndRecover.md` |
| A web server | 一个完整的 HTTP 服务器示例 | `docs/net/Intro.md`、`docs/gin/` |

40 个二级小节里，本仓有独立内容的重点是 `Defer`、`Allocation with make`、`Interfaces`、`Panic`、`Recover`、`MixedCaps`；讲得比 Effective Go 更细的是 `GMP 调度器`、`Channel 实现` 这两页，它们超出原文范围。

## 二、读的顺序

官方的建议是 Tour → 语言规范 → Effective Go。本仓对应顺序：

1. `docs/start/Hello.md` 起步，走完 `docs/syntax/`、`docs/type/`。
2. `docs/oop/` 的方法与接口、`docs/mod/` 的包。
3. `docs/test/`，Effective Go 没有专章讲测试，本仓这块比它全。
4. `docs/concurrency/`，对应 Concurrency 那一节。
5. 最后读 Effective Go 原文对照，本页当索引用。

## 三、两处官方自己的提醒

- 语言规范（`/ref/spec`）和 Tour 应该先读，Effective Go 是在它们之上的写法建议，不是语法定义。
- 官方对 A web server 那节的说法是：它展示的是一个小而完整的程序，重点在组织方式，不在于生产可用性。

## 来源

1. https://golang.google.cn/doc/effective_go — 16 个一级小节与 40 个二级小节目录，以及「a must read for any new Go programmer」的定位（2026-10-08 抓取）
2. https://golang.google.cn/doc/ — 文档总览中 Effective Go 的排序说明（先读 tour 与 spec）
3. https://golang.google.cn/tour/ — Tour 四段式结构
