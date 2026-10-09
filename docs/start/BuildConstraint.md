# 构建约束：`//go:build` 与文件名规则

构建约束（build constraint，也叫 build tag）决定一个源文件进不进这次编译。本仓此前没有任何页面讲它，交叉编译和按平台分文件时绕不开。内容取自官方 `go/build` 包文档与 `go` 命令的 Build constraints 小节，抓取于 2026-10-08。

## 一、写在哪、怎么写

- 约束写成一行以 `//go:build` 开头的行注释。
- 必须出现在文件靠前的位置：前面只能是空行和其他注释，在 Go 文件里也就是必须写在 `package` 子句之前。为了和包文档区分开，约束后面要跟一个空行。
- 一个文件里出现多于一行 `//go:build` 是编译错误。
- 约束也用于下调编译该文件使用的语言版本。

表达式由标签和 `||`、`&&`、`!` 以及括号组成，运算符含义与 Go 语言一致：

```go
//go:build (linux && 386) || (darwin && !cgo)
```

这行的意思是：目标为 linux/386 时编译，或者目标为 darwin 且没有 cgo 时编译。

## 二、这次构建里哪些标签成立

| 标签类别 | 成立条件 |
| --- | --- |
| 目标操作系统 | 等于 `runtime.GOOS`，由 `GOOS` 环境变量指定 |
| 目标架构 | 等于 `runtime.GOARCH`，由 `GOARCH` 环境变量指定 |
| 架构特性 | 形如 `amd64.v2`，由 `GOAMD64`、`GOARM`、`GOARM64`、`GOMIPS`、`GOPPC64`、`GORISCV64`、`GOWASM` 等变量决定 |
| `unix` | `GOOS` 是 Unix 或类 Unix 系统 |
| 编译器 | `gc` 或 `gccgo` |
| `cgo` | 支持 cgo 命令（见 `CGO_ENABLED`） |
| Go 版本 | 从 1.1 起每个大版本一个标签：`go1.1`、`go1.12`……一直到当前版本 |
| 自定义 | `-tags` 传入的额外标签（见 `go help build`） |

大版本没有 beta 或小版本标签。特性标签是累加的：`GOAMD64=v2` 同时满足 `amd64.v1` 与 `amd64.v2`，所以要判断「没有这个特性」得写反条件：

```go
//go:build !amd64.v2
```

几个别名要知道：`GOOS=android` 在 linux 标签之外额外满足 android；`GOOS=illumos` 在 solaris 之外额外满足 illumos；`GOOS=ios` 在 darwin 之外额外满足 ios。

## 三、文件名自带的约束

去掉扩展名和可能的 `_test` 后缀，文件名匹配下面任一模式，就等于多了一条隐式约束：

- `*_GOOS`，如 `dns_windows.go`
- `*_GOARCH`，如 `math_386.s`
- `*_GOOS_GOARCH`，如 `source_windows_amd64.go`

隐式约束与文件里写的显式约束是叠加关系，两者都要满足才会编译进去。命名 `dns_windows.go` 的文件只在为 Windows 构建这个包时参与编译。

## 四、几个约定

- 想让一个文件在任何构建里都不参与：`//go:build ignore`（其他不成立的词也行，`ignore` 是约定写法）。
- 只在有 cgo 且是 Linux 或 macOS 时编译：`//go:build cgo && (linux || darwin)`，配对文件写取反条件，两边合起来覆盖所有情况。
- 有汇编实现的包通常再给一个纯 Go 版本，约定标签是 `purego`。
- Go 1.16 及更早用的是 `// +build` 前缀的另一种写法，`gofmt` 遇到旧写法会补一行等价的 `//go:build`。
- 模块的 Go 版本是 1.21 及以上时，如果文件约束里带了大版本标签，编译该文件使用的语言版本就是这个标签隐含的最低版本。

## 五、本仓怎么用

| 场景 | 做法 |
| --- | --- |
| 一份代码同时发 Linux/Windows 二进制 | `GOOS=windows GOARCH=amd64 go build`，平台差异文件按 `*_GOOS.go` 命名 |
| 系统调用按平台分文件 | `syscall_unix.go` / `syscall_windows.go`，与 `docs/net/Advanced.md` 里 `x/sys/unix` 的例子配合 |
| 汇编与非汇编两条路径 | 用 `purego` 标签切换，参考 `docs/asm/Assembly.md` |
| 关掉 cgo 的纯静态构建 | `CGO_ENABLED=0`，对应标签 `cgo` 不成立 |

## 来源

1. https://golang.google.cn/pkg/go/build/ — 「Build constraints are given by a line comment that begins //go:build」与文件名约束说明
2. https://golang.google.cn/pkg/cmd/go/ — Build constraints 小节：标签清单、表达式语法、`ignore`、`purego`、`// +build` 旧语法与 1.21 语言版本规则
3. https://golang.google.cn/doc/ — 文档总览中 Commands 板块入口

以上抓取于 2026-10-08。
