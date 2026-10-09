# PGO：把生产环境的 CPU profile 喂回编译器

PGO（Profile-guided optimization，配置文件引导优化）也叫 FDO（反馈导向优化）：把有代表性的运行 profile 交给编译器，让下一次构建做更准的优化，比如对 profile 里频繁调用的函数更激进地内联。官方页面 `/doc/pgo` 抓取于 2026-10-08。

## 一、收益的官方数字

官方原文：以 Go 1.22 为基准，对一组有代表性的 Go 程序做基准测试，**带 PGO 构建的性能提升大约 2%-14%**，并且官方预期随版本迭代收益还会继续变大。这是文档里的基准结论，不是本仓测出来的数。

## 二、输入是什么

Go 编译器要的输入是 CPU pprof profile，来自 `runtime/pprof` 或 `net/http/pprof` 的运行时产物可以直接用，其他 profiling 系统的产物要先做转换。profile 必须能代表生产环境的行为，官方明确说：拿不具代表性的 profile 构建，生产环境可能一点收益都没有，所以**推荐直接从生产环境采集**。

推荐的迭代节奏：

1. 先出一版不带 PGO 的二进制。
2. 从生产环境采集 profile。
3. 下次发版时用最新源码加上生产 profile 构建。

PGO 对 profile 版本与构建版本之间的错位是稳健的，也允许拿已经优化过的二进制采集来的 profile，所以上面这个循环可以一直转下去。

## 三、怎么开

| 方式 | 用法 |
| --- | --- |
| 默认开 | 把 pprof CPU profile 命名为 `default.pgo`，放在被剖析程序的 main 包目录下，`go build` 自动检测并启用 |
| 显式指定 | `go build -pgo=/tmp/foo.pprof` |
| 关掉 | `go build -pgo=off` |
| 默认值 | `-pgo` 默认就是 `-pgo=auto`，即上面的 `default.pgo` 行为 |

官方建议把 profile 直接提交进源码仓库：profile 是构建输入，跟源码放一起，可复现的构建才同时可复现性能，拉下源码就不用再补步骤。

命令行工具这类发给最终用户、采不到生产 profile 的程序，可以改用有代表性的基准测试来采。官方同时给了个提醒：**微基准测试通常是差的 PGO 来源**，因为它只覆盖程序的一小块，套到整程序上收益很小。

## 四、在本仓的位置

| 相关内容 | 页面 |
| --- | --- |
| pprof 怎么采 | `docs/debug/Pprof.md` |
| 基准测试 | `docs/test/Benchmark.md` |
| GC 与内存行为 | `docs/gc/GC.md`、`docs/alloc/GC.md` |
| `net/http/pprof` 挂到服务上 | `docs/debug/Pprof.md` 的示例代码 |

先有 pprof 才有 PGO，本仓 `docs/debug/Pprof.md` 是这一页的前置。

## 来源

1. https://golang.google.cn/doc/pgo — Profile-guided optimization：2%-14% 收益、profile 来源、`default.pgo` 与 `-pgo` 三个取值、生产采集流程、微基准的反例（2026-10-08 抓取）
2. https://golang.google.cn/doc/ — References 板块下的 PGO 入口
