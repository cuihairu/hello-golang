# DevOps 与 SRE：脚本、CLI 和长期运行的服务都用它

DevOps 与 SRE 是官方四类场景之一。本页是官方 DevOps 场景页的中文摘录与本仓导读，抓取于 2026-10-08。

## 一、官方的三段论

1. **写小脚本**：标准库覆盖 HTTP、文件 I/O、时间、正则、exec、JSON/CSV，静态类型加显式错误处理，脚本比同样长度的动态语言脚本更耐改。
2. **CLI 快速发布**：构建快，一次性脚本长成每天几十个人在用的工具时不用重写。官方举的形态演进是「一次性脚本 → CLI → 发布管理服务」。
3. **大服务好维护**：垃圾回收省掉手工内存管理，godoc 自动生成文档，代码自己带说明。

运维类工具还要面对规模增长，官方给的补充理由是并发与网络能力适合管理云上部署的自动化工具。

## 二、官方列的项目

| 项目 | 做什么 | 出处 |
| --- | --- | --- |
| Docker | 容器平台，官方描述为驱动大规模安全自动化与部署，支撑 CI/CD | DevOps 场景页 |
| Drone | 跑在容器上的持续交付系统，用一份 YAML 定义流水线 | DevOps 场景页 |
| etcd | 强一致的分布式键值存储，给分布式系统与集群提供配置与服务发现 | DevOps 场景页 |
| IBM | 通过 Docker、Kubernetes 和一批 Go 写的 CI/CD 工具使用 Go | DevOps 场景页 |
| Netflix | 缓存服务 Rend，管理全球复制的个性化数据 | DevOps 场景页 |
| Microsoft | Azure Red Hat OpenShift 服务里用 Go | DevOps 场景页 |

SRE 这套做法起源于 Google，目标是让大规模站点更可靠、更高效、更可扩展；官方页面提到 Amazon 与 Netflix 后来也采用了同样的实践。

## 三、和本仓的接法

| 运维任务 | 本仓页面 |
| --- | --- |
| 解析命令行参数 | `docs/cmd/Flag.md`、`docs/cmd/Parse.md` |
| 读配置文件 | `docs/gin/Config.md`、`docs/encoding/Ini.md`、`docs/encoding/TOML.md` |
| 打日志与日志采集 | `docs/log/` 4 页，采集那页讲 fluentd |
| 出问题先看什么 | `docs/debug/`：Delve、GDB、pprof、expvar |
| 回归测试与覆盖率 | `docs/test/` 9 页 |
| 定时与超时控制 | `docs/time/TimerAndTicker.md`、`docs/sync/Context.md` |
| 交叉编译产物 | `docs/start/BuildConstraint.md` |

## 四、一个取舍

运维脚本要不要 Go，取决于脚本会不会活过三个月。只会跑一次、改一次的粘合逻辑，写 Python 更快；一旦要发布给别人、要长期维护、要并发拉多份状态，Go 的静态类型和单二进制才开始回本。官方页面里的形态演进（一次性脚本变成团队日常工具）说的就是这个拐点。

## 来源

1. https://golang.google.cn/solutions/devops/ — Go for DevOps & Site Reliability Engineering（三段论、Docker/Drone/etcd/IBM/Netflix/Microsoft、SRE 起源，2026-10-08 抓取）
2. https://golang.google.cn/solutions/use-cases — 四类场景索引
