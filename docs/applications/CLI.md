# 命令行工具：单二进制加 Cobra 与 Viper

CLI 是官方四类场景之一。官方 CLI 页给的理由集中在三条：编译快、单个自包含二进制、启动时间接近 C/C++。抓取于 2026-10-08。

## 一、为什么是 Go

- 从一台 Windows 或 Mac 笔记本出发，几秒钟能构建出 Go 支持的几十种架构与操作系统上的程序，不需要专门的构建农场。官方原话：没有别的编译型语言能构建得这么可移植、这么快。
- 产物是单个自包含二进制，装这个程序就是拷一个文件，不依赖已有库、运行时或依赖。
- 启动立即发生，量级接近 C/C++。

云与基础设施类应用天然以 CLI 为主，因为脚本化和远程操作都方便，这也是官方把 CLI 单列一类的原因。

## 二、Cobra 与 Viper 的分工

| 工具 | 职责 | 官方点名的使用方 |
| --- | --- | --- |
| Cobra | 命令、子命令、参数解析、帮助与自动补全；既是库也是代码生成器 | CoreOS、Delve、Docker、Dropbox、Git LFS、Hugo、Kubernetes |
| Viper | 配置：嵌套结构、文件、环境变量，配合 Cobra 组成完整方案 | 官方页面给出的场景是敏感数据走环境变量，不留在命令行历史里 |

官方对 Cobra 的定位引用的是 DGraph Labs 的 Francesc Campoy：它更像框架而不是库，调用生成出来的二进制就有了骨架，剩下往里填代码。Hugo 作者 Bjørn Erik Pedersen 给的理由是单二进制让安装变得极简单。

本仓 `docs/cmd/` 讲的是标准库 `flag` 的设计与解析，够写中小型工具；命令树大了再上 Cobra，`docs/gin/Config.md` 里对 Viper 有介绍。

## 三、官方案例

- **Comcast**：用 Go 写高频站点发布订阅的 CLI 客户端，并开源了 Go 写的 Apache Pulsar 客户端库。
- **GitHub**：命令行工具用 Go 包装 git，用来扩展额外功能与命令。
- **Hugo**：Go 写的静态站生成器，官方把它列为最流行的 Go CLI 应用之一，单二进制安装是主因。

## 四、动手顺序

1. 先用标准库把命令与参数跑通：`docs/cmd/Flag.md`、`docs/cmd/Parse.md`。
2. 需要子命令与帮助生成：上 Cobra，参考 `docs/cmd/Design.md` 里的命令设计约定。
3. 配置来源多（文件、环境变量、命令行三处会冲突）：用 Viper 收口，见 `docs/gin/Config.md`。
4. 交叉编译发布：`GOOS`/`GOARCH` 组合与构建约束见 `docs/start/BuildConstraint.md`。

## 来源

1. https://golang.google.cn/solutions/clis/ — Go for CLIs（单二进制、几秒跨架构构建、Cobra 与 Viper、Comcast/GitHub/Hugo 案例，2026-10-08 抓取）
2. https://golang.google.cn/solutions/use-cases — 四类场景索引
