# hello-golang 文档结构审计（2026-10-19）

范围：只读检查仓库文档组织、VitePress 侧边栏、仓库根目录与本地链接。报告新增于 `docs/zh/review/structure-audit-2026-10-19.md`；没有改动其他文档或配置。行数按 LF 分行统计，包含空行。

## 量化事实

### `docs/` 一级目录下 Markdown 数量与行数

| 一级目录 | .md 数 | 总行数 |
|---|---:|---:|
| algo | 49 | 6,906 |
| alloc | 3 | 476 |
| applications | 5 | 292 |
| asm | 2 | 385 |
| cgo | 2 | 435 |
| cmd | 6 | 1,416 |
| compress | 6 | 1,583 |
| concurrency | 11 | 1,925 |
| const | 5 | 478 |
| db | 19 | 3,817 |
| debug | 7 | 1,014 |
| distribution | 1 | 199 |
| dp | 29 | 3,822 |
| encoding | 14 | 2,311 |
| env | 9 | 1,184 |
| error | 4 | 923 |
| func | 10 | 1,741 |
| gc | 2 | 208 |
| generics | 7 | 1,154 |
| gin | 13 | 2,674 |
| idioms | 8 | 979 |
| introduction | 4 | 357 |
| io | 14 | 3,922 |
| log | 4 | 939 |
| math | 8 | 1,707 |
| middleware | 3 | 209 |
| mod | 9 | 1,240 |
| naming | 3 | 537 |
| net | 7 | 1,617 |
| oop | 8 | 1,460 |
| operator | 11 | 1,603 |
| redis | 11 | 1,820 |
| reflection | 2 | 370 |
| regex | 6 | 1,052 |
| research | 5 | 449 |
| security | 1 | 58 |
| start | 7 | 1,016 |
| sync | 11 | 1,741 |
| syntax | 10 | 1,670 |
| sys | 4 | 296 |
| test | 9 | 1,286 |
| time | 7 | 982 |
| type | 26 | 4,677 |
| var | 5 | 831 |
| **合计（内容目录）** | **391** | **64,701** |

目录统计递归计算。`docs/.vitepress` 为配置/构建目录（0 篇 md），`docs/public` 为静态资源目录（0 篇 md），不计入内容目录合计。`docs/` 根下另有 `SUMMARY.md`（414 行）、`glossary.md`（379 行）、`index.md`（25 行）、`knowledge.md`（122 行），合计 4 篇、940 行。

### 组织轴清点

| 组织轴/机制 | 条目数 | 命名规律 | 编号 | 连续性 |
|---|---:|---|---|---|
| 主题目录（主存储轴） | 44 个内容目录、391 篇 | 多为英文短主题目录，目录内英文主题文件名；如 `docs/zh/concurrency/Chan.md` | 无 | 不适用 |
| 导航章节顺序（`SUMMARY.md` → `sidebar.json`） | SUMMARY 403 个链接；sidebar 389 个唯一页面引用 | 以中文章节名组织，链接落到主题目录；由 `config.mts` 导入 sidebar | 无显式数字编号 | 不适用；不是编号体系 |
| 指南/入门路径（嵌入主题导航） | 未设独立 `guide` 目录；入门章节 7 篇，环境章节 9 篇 | `docs/zh/start/`、`docs/zh/env/`，分别作为主题目录和导航分组 | 无 | 不适用 |
| API 目录轴 | 0 个名为 API 的一级目录；API 内容散落在主题目录（条目未按专门 API 清单计） | 按语言/库主题归档 | 无 | 不适用 |
| history/历史轴 | 1 个文件名含 History：`docs/zh/func/History.md` | 文件级主题/历史标签，不是独立目录或稳定体系 | 无 | 不适用 |
| 数字前缀章节轴 | 0 篇文件 basename 以数字前缀命名 | 未发现 `01-`、`1.` 等数字前缀文件 | 无条目 | 无断档/跳号/重复可报；全量数字前缀排序结果为空 |

结论口径：**3 套实际起作用的组织方式**（主题目录、导航章节顺序、嵌入式指南路径）。API 与 history 是内容类型/单文件现象，不构成独立组织轴；数字章节编号轴不存在。`SUMMARY.md` 与侧边栏是同一导航结构的底稿和运行配置，不重复计为两套。

### 侧边栏对账

读取 `docs/.vitepress/config.mts` 与导入的 `docs/.vitepress/sidebar.json`。配置页面链接 389 个唯一值：

| 分组 | 数量 | 前 10 条 |
|---|---:|---|
| 配置了但目标文件不存在 | 0 | 无 |
| 文件存在但未进侧边栏 | 2 | `docs/zh/index.md`、`docs/SUMMARY.md` |

`SUMMARY.md` 在 `config.mts` 的 `srcExclude: ['**/SUMMARY.md']` 中明确排除；`index.md` 是站点根页面，通常由 VitePress 首页路由承载，不作为侧边栏条目属于合理配置。侧边栏检查不把目录页面/别名重复计数。

### 编号、命名、分布与根目录

- **数字前缀**：对 391 篇内容 Markdown 的 basename 全量抽取，匹配 `数字 + 可选分隔符 + 名称` 的结果为 0。没有可以列出的断档、跳号或重复编号；不应为此人为补编号。
- **同主题/相近主题多处**（相同 basename 是可复核的代理证据，不表示内容必然重复）：`Array` 位于 `docs/zh/type/Array.md`、`docs/zh/algo/array/Array.md`；`GC` 位于 `docs/zh/gc/GC.md`、`docs/zh/alloc/GC.md`；`Interface` 位于 `docs/zh/type/Interface.md`、`docs/zh/oop/Interface.md`；`Security` 位于 `docs/zh/security/Security.md`、`docs/zh/io/Security.md`、`docs/zh/db/Security.md`；`Switch` 位于 `docs/zh/syntax/Switch.md`、`docs/zh/type/Switch.md`；`Assignment` 位于 `docs/zh/operator/Assignment.md`、`docs/zh/var/Assignment.md`。分别代表不同语境可能合理，需看正文后才能判定是否重复。
- **命名风格**：主题目录为小写英文（如 `docs/zh/redis/`），文件名同时出现 PascalCase（`docs/zh/env/Goland.md`）、小写（`docs/zh/env/ide.md`、`docs/zh/gin/advanced.md`）、缩写/词界风格（`docs/zh/encoding/JSON.md`、`docs/zh/io/ModOS.md`）；`Readme.md` 与 `README.md` 并存，8 个 basename 大小写不统一的 README 变体，具体有 `docs/zh/cmd/Readme.md`、`docs/zh/db/Readme.md`、`docs/zh/distribution/Readme.md`、`docs/zh/middleware/Readme.md`、`docs/zh/redis/Readme.md`、`docs/zh/regex/Readme.md`、`docs/zh/research/README.md`、`docs/zh/compress/Readme.md`。大小写差异会影响大小写敏感链接和检索一致性。
- **交叉入口**：`docs/SUMMARY.md` 的“惯用法”章节重复链接到 `func/MultipleReturnValues.md`、`func/Defer.md`、`syntax/Switch.md`、`concurrency/Select.md` 等主题页；这是多入口导航，不足以单独证明正文重复。
- **导航映射底稿差异**：`docs/SUMMARY.md` 有 403 个 Markdown 链接，当前文件均存在；VitePress sidebar 为 389 个唯一引用。SUMMARY 中重复链接解释了部分差值。`docs/.vitepress/config.mts` 注释说明 sidebar 由 SUMMARY 映射生成；两者内容看起来同步，但映射脚本未在本次核查中执行（`未核实`）。
- **根目录杂散文件**：仓库根有 `BUGS.md`、`README.md`、`README.zh.md`、`LICENSE`、`package.json`、`package-lock.json`；未发现根目录临时文件。`BUGS.md` 是维护记录，README 双语是有意区分，不属于重复 README。`docs/` 有上表 4 篇入口/辅助 Markdown，属文档站内容，不算仓库根杂散文件。

### 链接/构建检查

- `npm run docs:build` **未能运行**：`sh: 1: vitepress: not found`；`package.json` 有构建脚本，但当前环境没有已安装的本地 VitePress 可执行文件。完整构建级死链检查因此为 **未核实**。
- 对 sidebar 页面引用做文件映射核对：0 个缺失。
- 对 Markdown 内链做了简易扫描，但扫描器会把代码围栏/行内代码里的括号误识为链接，产生 18 条假阳性（如 `docs/zh/generics/Constraints.md:14` 的代码参数）。不能据此宣称有 18 个死链。对照 `docs/SUMMARY.md:396` 与 `docs/zh/gin/advanced.md`，当前 SUMMARY 的大小写引用一致；`docs/zh/research/Coverage.md:100` 只是审计表格中保留的旧问题记录，并非链接，不能据此报当前死链。

## 问题清单与严重度

| # | 问题/判断 | 严重度 | 证据与理由 |
|---|---|---|---|
| 1 | 构建级死链状态未知 | 未核实 | 本次收口执行记录有本地链接扫描结果，但本记录最初的 VitePress 构建仍未运行。此前大小写疑点已确认是旧问题记录，不是当前链接。 |
| 2 | SUMMARY 与侧栏是双份维护数据，可能发生漂移 | 已处理 | 收口执行记录已选定 `docs/.vitepress/sidebar.json` 为唯一权威源；`docs/SUMMARY.md` 现为维护说明并被 `srcExclude` 排除。旧的 403/389 对账仅描述改动前状态，不代表当前数据。 |
| 3 | 文件命名大小写/词界不一致，README 变体尤其明显 | 低 | 上述 8 个 `Readme.md`/`README.md` 路径；`docs/zh/env/ide.md` 与 `docs/zh/env/Goland.md`、`docs/zh/gin/advanced.md` 并列。主要影响检索、链接跨平台和维护一致性，不构成组织失效。 |
| 4 | 相同 basename 的主题页分布多处，容易误判重复或产生检索歧义 | 低 | `docs/zh/type/Array.md` 与 `docs/zh/algo/array/Array.md`；`docs/zh/gc/GC.md` 与 `docs/zh/alloc/GC.md`；更多见“同主题/相近主题多处”。语境可能有意区分，不建议仅凭文件名合并。 |
| 5 | 编号断档/重复 | 无问题 | 全部内容文件数字前缀计数为 0；当前体系不是编号章节，不应视作缺陷。 |
| 6 | Sidebar 配置孤儿/未入栏页面 | 低/无阻塞 | 配置缺文件 0；未入栏 2，其中 SUMMARY 被显式排除，index 为根首页。没有需要修复的导航断链。 |

## 判断与推荐

目前的主骨架是**主题目录 + 一套章节导航**，结构本身可理解，目录名大体覆盖 Go 语言、标准库、工程实践、算法和生态主题。改动前的导航底稿双维护风险已在收口时处理；仍需关注文件命名细节，以及相邻概念页是否有清楚的语境提示；“太乱”并不适用于所有部分。

改动前的结构建议曾倾向 SUMMARY 为导航源；该建议已由下方“收口执行记录”取代。当前实际方案是 `docs/.vitepress/sidebar.json` 为唯一权威源，SUMMARY 仅保留维护说明，不存在 403/389 链接差异需要继续处理。

**其实不乱、不用动的部分**

- 主题目录作为主归档方式合理；`db/`、`redis/`、`gin/` 等主题边界清楚，数量多本身不是混乱证据。
- VitePress sidebar 目前 389 个引用全部命中文件；没有配置死链接。
- `docs/SUMMARY.md` 被显式排除、`docs/zh/index.md` 不在 sidebar 中符合常见站点路由设计。
- `README.md` 与 `README.zh.md` 是语言版本，不是重复文件；`BUGS.md` 是仓库级维护记录。
- 相同名称如 `Array`、`Interface`、`Security` 可能在不同领域有不同讲解目标；先保留并改善交叉链接，不做无证据合并。
- 当前没有数字章节编号，也无编号跳号问题，不需要补号或重排。

## 三期收口方案

| 期次 | 动作清单 | 影响范围 | 风险（链接/搜索/外链） | 用户拍板 |
|---|---|---|---|---|
| 一期：机械整理，目标 1 小时内 | 统一明显拼写/大小写命名的候选清单（先做链接全仓替换与大小写核验）；为同名跨主题页补一行范围说明/交叉链接；确认疑似 `Advanced.md` 路径。只有在逐条更新所有站内引用并跑构建成功后才重命名。 | 少量文件名与链接，README 变体候选；不改目录架构。 | 原地大小写重命名可能伤及大小写敏感路径、外链与搜索索引；纯补范围说明风险低。重命名必须同步站内链接。 | **拍板** README 统一目标名；重命名公开 URL 是否接受；跨主题页是否保留现名。 |
| 二期：导航权威源与重定向 | **导航权威源选择已完成**：以 sidebar JSON 为唯一源；检查 `docs/zh/knowledge.md` 等页面是否有合理入口；未来若迁移路径，再评估旧 URL 重定向并做构建链接检查。 | sidebar JSON、少量导航和可能的重定向配置。 | 变更导航顺序会影响可发现性；页面路径迁移可能影响外链和搜索收录。保留旧地址重定向可降低风险，但需维护。 | 权威源已定；未来路径迁移和重定向策略按具体变更评估。 |
| 三期：章节删并的深度重构 | 对相同 basename/重复主题做正文对比、定义受众与边界；决定合并、拆分或保留；维护别名/重定向、更新站内链接和搜索；以构建与人工抽样验证。 | 多主题文档，可能触及几十篇正文、导航与历史 URL。 | 最高：删除/合并会影响深链、搜索排名、引用与读者书签；重定向只能缓解，语义合并也可能损失差异内容。 | **必须逐项拍板** 内容删除/并入目标、旧 URL 去留、导航层级及外链兼容策略。 |

## 最该先做的三件事

1. 在装好依赖的环境运行 `npm ci && npm run docs:build`，解决并记录真实构建/死链结果；记录构建输出并处理构建实际报告的死链。
2. 导航权威源已收敛为 sidebar JSON；后续只维护该文件，并确认目标 Markdown 文件存在。
3. 先为同名/相近主题页标明范围与交叉入口，再讨论重命名或合并；暂不碰编号或大规模迁移。

## 收口执行记录（2026-10-19）

### A. 导航唯一真源

- 权威源定为 `docs/.vitepress/sidebar.json`：`docs/.vitepress/config.mts:2,40` 直接导入并配置该文件。
- `docs/SUMMARY.md:1-5` 保留为维护说明：说明 sidebar 是唯一可编辑源、SUMMARY 是 mdbook 遗留底稿且被 `srcExclude` 排除；手工修改 SUMMARY 不生效。
- 侧栏树原有 13 个重复路由（402 个链接值、389 个唯一值）。重复项已收敛到首次入口；重复父级若含独立子页面则保留分组但移除重复父级链接，避免丢失子页面入口。现为 389 个链接值、389 个唯一值、0 重复。不同分组中的页面复用属于导航入口复用，未跨侧栏删除。

### B. 跨轴重复逐组判定

| 页面组 | 判定 | 正文对照证据 | 处理 |
|---|---|---|---|
| `type/Array.md` / `algo/array/Array.md` | 不同角度 | 前者首段“数组固定长度、元素类型相同，切片可以变长”，并讲 Go 的数组/切片和值传递；后者首段“线性数据结构……连续的内存”，重点为随机访问 O(1)、连续存储与复杂度。 | 保留，互链并标注语言语义/数据结构视角。 |
| `gc/GC.md` / `alloc/GC.md` | 真重复（GC 基本原理） | 前者“Go 的垃圾回收器是并发的标记-清除回收器”，后者“Go 的 GC 是并发三色标记-清除回收器”；两页都解释从根标记、清除不可达对象。 | `gc/GC.md` 为原理权威页；`alloc/GC.md:11-13` 改为摘要与完整链接，分配器协作、观察和调优仍留在该页。 |
| `type/Interface.md` / `oop/Interface.md` | 不同角度 | `type/Interface.md` 开篇以 `iface`、`itab` 和反射关系为重点；`oop/Interface.md` 从“类型描述数据长什么样，接口描述对象能做什么”展开类型/接口定义与实现。 | 保留，互链并标注运行时/概念实现视角。 |
| `syntax/Switch.md` / `type/Switch.md` | 不同角度 | 前者开篇涉及默认退出、`fallthrough`、普通 switch；后者首段明确是按接口值动态类型分支的类型 switch。 | 保留，互链并标注控制流/动态类型分派视角。 |
| `operator/Assignment.md` / `var/Assignment.md` | 不同角度 | 前者首段讨论 `=` 与复合赋值运算符；后者首段称“常见的写法有十种”，覆盖短声明、多重赋值、空白标识符、指针和结构体等模式。 | 保留，互链并标注运算符/变量使用模式视角。 |
| `security/Security.md` / `io/Security.md` / `db/Security.md` | 不同角度 | 官方页讲 Go 漏洞库、修复范围、fuzzing 和 crypto；IO 页标题为“文件与 IO 的安全性”；DB 页从数据库安全与 SQL 注入展开。 | 三页均保留并互链，标注官方口径、文件 IO、数据库安全视角。 |

合并真重复 **1 组**；保留不同角度 **5 组**。未删除 Markdown，也未把不同心得硬并。

### C. 口径与死项

- `README.md:22`、`README.zh.md:22` 改为个人笔记与游戏开发者分享口径；两份 README 没有硬编码篇数或目录清单，无需改计数/清单。
- `docs/zh/index.md:6-7` 与 `docs/.vitepress/config.mts:6,24` 的站点文案改为个人开发笔记口径。
- `docs/.vitepress/config.mts:38-40` 的“50 个顶层分组”与 sidebar 实际 50 项一致，保留；未发现目标文件不存在的 sidebar 页面条目。
- `docs/zh/knowledge.md` 已在“调研”侧栏分组中，重要总览页已入栏。

### 验收快照

- `pnpm docs:build` 通过（VitePress 1.6.4；页面构建完成）。输出含 assembly/gdb 高亮回退和大 chunk 警告，不影响构建。
- 可复算等价检查：Markdown 本地链接扫描跳过代码围栏与行内代码，并将 `/...` 路由按 docs 根目录解析；检查 **2782** 条本地 Markdown 链接，缺失 **0**。sidebar 389 个链接目标均存在，缺失 **0**；侧栏重复路由 **0**。
- Markdown 删除数：**0**（收口提交期间未删除任何 `.md`）。
