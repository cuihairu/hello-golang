# 原生 fuzzing：`FuzzXxx` 与 `go test -fuzz`

Go 从 **1.18** 起在标准工具链里内置 fuzzing，用覆盖率引导去走人想不到的输入分支。本仓 `docs/test/Lib.md` 讲的是 go-fuzz 这套外部工具链，原生写法此前没有页面。内容取自官方 `/doc/fuzz/` 与 fuzzing 教程，抓取于 2026-10-08。

## 一、它在解决什么问题

fuzzing 是持续变换程序输入、以找到 bug 的自动测试。官方给的理由是它能到达人容易漏掉的边界情况，所以在找安全漏洞上特别有价值。原生 fuzz 测试被 OSS-Fuzz 支持。

## 二、写法规则（官方 Requirements 一节）

- 测试函数必须形如 `FuzzXxx`，只接受一个 `*testing.F`，没有返回值。
- fuzz 测试必须放在 `_test.go` 文件里。
- fuzz 目标通过 `(*testing.F).Fuzz` 注册，第一个参数是 `*testing.T`，后面跟 fuzz 参数，没有返回值；每个 fuzz 测试只能有一个目标。
- 种子语料（seed corpus）的类型必须与 fuzz 参数完全一致、顺序一致，`(*testing.F).Add` 的调用与 `testdata/fuzz` 下的语料文件都算。
- 允许的参数类型只有：`string`、`[]byte`、各长度整型、`rune`、各长度无符号整型、`float32`、`float64`、`bool`。

官方给的建议：fuzz 目标要快、要确定性，这样引擎跑得动，新失败也能复现；目标会被多个 worker 并行、乱序调用，所以不要让状态跨调用残留，也不要依赖全局状态。

## 三、两种跑法

| 跑法 | 命令 | 行为 |
| --- | --- | --- |
| 当单元测试 | `go test` | 每条种子语料喂给目标跑一遍，有失败就报错退出 |
| 真做 fuzz | `go test -fuzz=FuzzTestName` | `-fuzz` 接一个正则，匹配到的那个 fuzz 测试开始持续变异输入 |

一个示例，对着 URL 解析做 fuzz：

```go
// fuzz_test.go
package example

import (
    "net/url"
    "testing"
)

func FuzzParse(f *testing.F) {
    f.Add("https://example.com/path?q=1")
    f.Fuzz(func(t *testing.T, raw string) {
        u, err := url.Parse(raw)
        if err != nil {
            t.Skip()
        }
        _ = u.String()
    })
}
```

种子语料用 `f.Add` 加，也可以放在 `testdata/fuzz/FuzzParse/` 下面。找到的失败输入会被写回语料目录，下一次 `go test` 直接复现。

## 四、和本仓其他页的关系

| 内容 | 页面 |
| --- | --- |
| 单元测试与子测试 | `docs/test/Test.md`、`docs/test/Advanced.md` |
| 表驱动测试 | `docs/test/Practice.md` |
| 基准测试 | `docs/test/Benchmark.md` |
| 覆盖率 | `docs/test/Cover.md` |
| go-fuzz 外部工具链 | `docs/test/Lib.md` |
| 安全侧的 fuzzing 定位 | `docs/security/Security.md` |

## 五、什么时候值得写

输入面由外部给的解析器（URL、JSON、模板、正则、协议解码）最划算，一行 `f.Add` 加一个目标就够；输入是固定枚举的内部函数，跑 fuzz 大概率只是烧 CPU，写表驱动测试更直接。

## 来源

1. https://golang.google.cn/doc/fuzz/ — Go Fuzzing：1.18 起内置、覆盖率引导、Requirements 与建议、两种运行方式、OSS-Fuzz（2026-10-08 抓取）
2. https://golang.google.cn/doc/tutorial/fuzz.html — fuzzing 教程
3. https://golang.google.cn/security/ — 安全页把 fuzzing 列为发现漏洞的手段
