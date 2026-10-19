# 结构改动内容复核（2026-10-19）

## 复核范围

按 `git log --oneline -4` 复核最近 4 个提交（`HEAD~4..HEAD`）：

| Commit | 内容 |
|---|---|
| `4f055f0` | Align site copy with notes voice（C：站点口径） |
| `edee3bf` | Clarify overlapping note scopes（B：重叠主题范围） |
| `5e9bf06` | Clarify navigation source（A：导航权威源及 SUMMARY 收敛） |
| `a3125cc` | Add docs structure audit（结构审计记录调整） |

这四个提交共改动 19 个文件，`HEAD~4..HEAD` 统计为 82 insertions、451 deletions；提交历史未改写。工作区起初干净，`git fetch origin && git pull --rebase origin main` 成功且显示已是最新。

## 四项核查

### 1. 内容丢失 — 未发现正文丢失

- `docs/SUMMARY.md:1-5`：旧版 414 行目录被替换为维护说明。配置 `docs/.vitepress/config.mts:18-20` 明确通过 `srcExclude` 排除 SUMMARY，且正文文件没有删除。此变更删的是第二份导航副本，不是内容性条目。
- 逐条对照 sidebar 删除的 13 个重复路由，目标页仍各有一次入口：例如旧 `/start/Build` 在 `docs/.vitepress/sidebar.json:74`，旧 `/concurrency/Select` 在其并发相关分组中保留。旧侧栏 402 个链接、389 个唯一目标；新侧栏 389 个链接、389 个唯一目标，重复数从 13 降至 0。
- B 合并的 `docs/alloc/GC.md`：旧 `### 基本原理：并发标记-清除` 下的两条解释被压成摘要，并在新 `docs/alloc/GC.md:11` 链到权威页 `docs/gc/GC.md`；分配器协作/调优内容继续保留。内容搬移目标存在。
- 前后对比：`docs/alloc/GC.md` 原有完整标记、清除两条说明；现为一段概述及“完整的标记、三色抽象与触发机制见 [GC 工作原理笔记](../gc/GC.md)”。未发现独有的分配器主题内容被删。

### 2. 表述改错、数字及技术含义 — 数字吻合；发现并修复审计文档陈述滞后

- `docs/.vitepress/config.mts:38-40` 声明 50 个顶层分组；人工计数 `sidebar.json` 顶层对象为 50。侧栏目标核对为 389 个链接、389 个唯一目标、0 重复、0 缺文件。
- README 两份改动各一行（`README.md:22`、`README.zh.md:22`），没有篇数、文件数或目录清单数字需要改。中文版从“Go 知识站点/覆盖……”改为“个人学习笔记、心得与开发经验……不是课程或学习教程”；没有把 Go 技术支持范围或能力从“不支持”反改为“支持”。英文版也只是改成个人开发笔记与游戏开发者视角，技术主题仍列语言细节、并发、算法、库和工程实践。
- `docs/index.md:6-7` 和 `config.mts:8,30` 的定位改写与 README 一致；“开发笔记”导航仍指向现存的 `start/Starter` 页面。
- 发现审计页旧分析段仍声称 SUMMARY 有 403 个当前链接、推荐 SUMMARY 作权威源并要求用户选择，和 A 收口的实际决定冲突。证据为复核前 `docs/review/structure-audit-2026-10-19.md` 第 103、113、129、135 行。已修正文案：将旧建议标作改动前状态、明确 sidebar JSON 已定为唯一源，并把构建死链状态改列“未核实”。修复提交：`6a354f4`。

### 3. 链接与导航 — 未发现错误目标

- 新增的 5 组范围说明交叉链接逐一核对文件主题及相对路径：数组语义↔数组数据结构、运行时接口↔接口概念、普通 switch↔类型 switch、赋值运算符↔变量赋值模式、官方安全↔IO/数据库安全；路径均存在且主题相符。
- sidebar 现存 389 个链接目标逐项映射文件，未缺失。移除的 13 个是重复路由，保留入口仍在对应主题分组（见第一项核查）。
- config 顶部导航 `/start/Starter`、`/type/CompositeType`、`/concurrency/Concurrency`、`/dp/DesignPatterns`、`/db/Readme`、`/gin/Gin` 均有对应页面。
- **未核实**：本轮没有安装依赖或运行 VitePress 全量构建；因此构建时的 dead-link 检查没有独立证据。此项不等同于报告已发现死链。

### 4. 其他明确结论

- SUMMARY 精简后的功能只是维护说明；其新内容说明 sidebar 权威源和 `srcExclude` 行为，与配置一致。
- B 对六组跨目录主题的范围说明与目标页面内容相符：只把 `gc/GC.md` 与 `alloc/GC.md` 的 GC 基础原理视为重复，其余五组保留不同视角；本次 diff 未删除这些 Markdown 页面。
- 未发现必须用户拍板的内容删并取舍；本轮实际合并的是重复导航路由，不是页面正文。

## 发现的问题清单

| # | 严重度 | 问题与证据 | 已修 | 修复 commit |
|---|---|---|---|---|
| 1 | 低（审计记录一致性） | 结构审计旧建议仍要求选择 SUMMARY/sidebar，和已经实施的唯一源决定矛盾；旧构建疑点表述也过时。 | 是 | `6a354f4` |

没有发现正文内容丢失、数字错误或链接指错。未核实项：VitePress 全量构建级链接检查（本轮未运行构建）。

## 结论

就本次逐项人工复核而言，A/B/C 结构改动未发现会导致内容丢失或错误导航的实质问题；审计记录中的滞后建议已修。**可视为内容与导航层面已验收，构建级死链状态仍未核实。**
