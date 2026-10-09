# `encoding/json/v2`：要不要迁移，官方给了明确答案

`encoding/json/v2` 是 Go 1.27 随新结构体标签一起推出的新 JSON 包，官方专门写了迁移指南。本仓 `docs/encoding/JSON.md` 讲的是 v1，v2 此前没有页面。内容取自官方迁移指南与包文档，抓取于 2026-10-08。

## 一、先说结论：不必迁

官方迁移指南的第一句回答是「First things first: you don't have to!」：

- `encoding/json` 永远不会消失，受 Go 1 兼容性承诺保护，用 v1 的代码会一直能跑。
- v1 与 v2 互相兼容。类型实现了 `encoding/json/v2.MarshalerTo`，通过 `encoding/json.Marshal` 调用时同样会走这个自定义 marshal。
- Go 1.27 引入的新结构体标签，`encoding/json` 也支持。

所以这是「想要更好的默认值和更好用的 API 时再迁」，不是版本压迫。

## 二、v2 改在哪

| 方面 | v1 | v2 |
| --- | --- | --- |
| 写出到 writer | 要用 `encoding/json.Encoder` | `encoding/json/v2.MarshalWrite` 直接写 `io.Writer` |
| 覆盖特定类型的序列化行为 | 只能改类型本身 | `encoding/json/v2.Marshalers` 可以覆盖你并不拥有的类型 |
| 字段名大小写匹配 | 固定行为 | `encoding/json/v2.MatchCaseInsenstiveNames` 控制是否忽略大小写 |
| 字符串里的非法 UTF-8 | 静默替换成替换字符 | 直接报错 |
| 默认值取向 | 宽松 | 更严格、互操作性更好 |

最后一条是官方说的迁移理由里最重的一条：v2 选了更严格、更可互操作的默认值。非法 UTF-8 那行是文档给的第一个对照例子。

## 三、对本仓的含义

| 场景 | 怎么办 |
| --- | --- |
| 已有服务，v1 跑得稳 | 不动，兼容性有官方承诺撑着 |
| 新写的接口要严格校验输入 | 新代码用 v2，非法 UTF-8 会在编解码处报错而不是被悄悄改写 |
| 需要按字段名忽略大小写匹配 | v1 做不到的用 v2 的开关 |
| 混用 v1/v2 | 可行，自定义 marshal 与新结构体标签两边都认 |

相关页面：`docs/encoding/JSON.md`（v1 语法与用法）、`docs/type/Json.md`（结构体标签）、`docs/gin/Request.md`（请求体绑定）。

## 四、查包文档

v2 的包文档在标准库 `encoding/json/v2` 分组下，`golang.google.cn/pkg/` 与 pkg.go.dev 都能打开；迁移指南在 `/doc/jsonv2-migration`，两处都是这次调研实际抓取过的页面。

## 来源

1. https://golang.google.cn/doc/jsonv2-migration — 迁移指南：不必迁的三条理由、v1/v2 兼容、四个 API 与默认值差异、Go 1.27 新标签两边都支持（2026-10-08 抓取）
2. https://golang.google.cn/pkg/encoding/json/v2 — 包文档入口
3. https://golang.google.cn/doc/ — 文档总览 References 板块列出的 json/v2 迁移指南条目
