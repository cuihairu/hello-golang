# Coverage reconciliation gap table

Method: break the three kinds of sources into topics, search for each one across the repo's 368 pages (title, H1, body keywords), and map each row into one of the three tables below, with the result in three grades. "Covered" means there is a dedicated page; "partially covered" means it was mentioned in passing on another page; "gap" means no matching content was found.

Verification date 2026-10-08. The search used regex over file names, titles and body text; the files that hit are written in the tables, so it is reproducible.

## 1. Gaps and remediation (13 items, all filled)

| # | Gap | Source | Remediation page |
| --- | --- | --- | --- |
| 1 | Application scenario overview (official four categories) | `/solutions/use-cases` | `docs/zh/applications/Applications.md` |
| 2 | Cloud and network services, cloud-native ecosystem (CNCF 75%, Docker, Kubernetes) | `/solutions/cloud/` | `docs/zh/applications/CloudNative.md` |
| 3 | CLI scenarios (single binary, Cobra, Viper) | `/solutions/clis/` | `docs/zh/applications/CLI.md` |
| 4 | DevOps/SRE scenarios (Docker, Drone, etcd, Rend) | `/solutions/devops/` | `docs/zh/applications/DevOps.md` |
| 5 | Web development scenarios (HTTP/2, TLS 1.3, 64% less code) | `/solutions/webdev/` | `docs/zh/applications/Web.md` |
| 6 | Build constraints `//go:build` (regex search 0 hits) | `/pkg/go/build/`, `/pkg/cmd/go/` | `docs/zh/start/BuildConstraint.md` |
| 7 | Go memory model (only 1 mention on the home page) | `/ref/mem` | `docs/zh/gc/MemoryModel.md` |
| 8 | Profile-guided optimization (only 1 mention on the GC page) | `/doc/pgo` | `docs/zh/debug/PGO.md` |
| 9 | Native fuzzing (only the old go-fuzz toolchain content) | `/doc/fuzz/`, `/doc/tutorial/fuzz.html` | `docs/zh/test/Fuzz.md` |
| 10 | Effective Go guide (2 mentions, no body text) | `/doc/effective_go` | `docs/zh/idioms/EffectiveGo.md` |
| 11 | Release cadence and support policy (1 mention) | `/doc/devel/release`, `/dl/?mode=json` | `docs/zh/introduction/ReleaseNotes.md` |
| 12 | `encoding/json/v2` (0 hits) | `/doc/jsonv2-migration`, `/pkg/encoding/json/v2` | `docs/zh/encoding/JsonV2.md` |
| 13 | Official security stance and the `crypto` standard library (no `crypto/` content) | `/security/` | `docs/zh/security/Security.md` |

## 2. Official documentation sections

| Official topic | Repo location | Verdict |
| --- | --- | --- |
| Getting started / Hello World | `start/Hello.md`, `start/Build.md` | Covered |
| Official Create a module page | `mod/Init.md`, `mod/New.md` | Covered |
| Multi-module workspaces | `mod/Work.md` | Covered |
| Official RESTful API example | `gin/` 13 pages | Covered (finer coverage than the Go official RESTful API example) |
| Official generics docs | `generics/` 7 pages | Covered |
| Writing Web Applications | `gin/`, `net/` | Covered |
| Language specification `/ref/spec` | `syntax/`, `type/`, `func/` | Content covered, no spec citations |
| Effective Go | `idioms/` 8 pages | Partially covered -> gap 10 |
| FAQ | `generics/`, `oop/` | Partially covered |
| Standard library package docs | 42 directories grouped by package | Covered |
| Go Tour four-part structure | `start/` -> `oop/` -> `generics/` -> `concurrency/` | Covered |
| Language specification terminology (methods, interfaces, embedding) | `oop/` 8 pages | Covered |
| Module dependency management | `mod/` 9 pages (incl. `Vendor.md`, `Get.md`) | Covered |
| go.mod reference | `mod/Mod.md` | Covered |
| Module publishing and version numbers | `mod/Mod.md` mentions semantic versioning | Partially covered (this site has no module-publishing content, not filling) |
| Memory model | 1 mention on the home page | Gap 7 |
| GC guide | `gc/GC.md`, `alloc/GC.md` | Covered |
| Diagnostics | `debug/` 7 pages (Delve, GDB, pprof, expvar) | Covered |
| Coverage | `test/Cover.md` | Covered |
| PGO | 1 sentence in `gc/GC.md` | Gap 8 |
| Fuzzing | `test/Lib.md` (go-fuzz) | Gap 9 |
| json/v2 migration | 0 hits | Gap 12 |
| Build constraints | 0 hits | Gap 6 |
| Database access docs (connection, execution, prepared statements, transactions, cancellation, connection pools, injection prevention) | `db/` 19 pages (`Tx.md`, `ConnectPool.md`, `Security.md`, etc.) | Covered |
| Editors and gopls | `env/vscode.md`, `env/Goland.md`, `env/Vim.md` | Covered |
| Contribution guide `/doc/contribute` | -- | Not applicable (this site records Go development experience, it does not carry Go project contribution-guide content), not filling |
| Release history and support policy | 1 mention | Gap 11 |
| Security (vulnerability database, fuzzing, crypto libraries, FIPS 140-3) | 0 `crypto/` content | Gap 13 |
| gopls / goimports / godoc tool installation | `env/Tools.md`, `mod/Get.md` | Covered |

## 3. Comparable book chapter mapping

| Chapters books commonly have | Repo location | Verdict |
| --- | --- | --- |
| Syntax and data types | `syntax/` 12 pages, `type/` 26 pages | Covered |
| Functions, methods | `func/` 10 pages, `oop/` 8 pages | Covered |
| Interfaces and type assertions | `type/Interface.md`, `oop/InterfaceImpl.md`, `type/Assertion.md` | Covered |
| Packages and engineering | `mod/`, `start/Structure.md` | Covered |
| Testing (table-driven, benchmarks, fuzzing) | `test/` 9 pages, table-driven in `test/Practice.md` | Partially covered (fuzzing -> gap 9) |
| Concurrency (goroutine, channel, synchronization primitives) | `concurrency/` 13 pages + `sync/` 14 pages | Covered, highest density |
| Choice of and cost of concurrency primitives | `sync/Mutex.md`, `sync/RWMutex.md`, scattered | Partially covered (not filling, scattered coverage holds up) |
| Reflection and metaprogramming | `reflection/Reflection.md` 1 page | Partially covered (less depth than *Go: Design and Implementation*, not filling for now) |
| cgo and C interop | `cgo/CGO.md` 1 page | Partially covered |
| Assembly and low-level | `asm/Assembly.md` 1 page | Partially covered |
| Distributed systems and RPC (gRPC, Protobuf) | `distribution/Readme.md`, `middleware/` | Partially covered (`grpc.io` unreachable on this network, not filling a standalone page for now) |
| Performance profiling and tuning | `debug/Pprof.md`, `gc/GC.md` | Covered |
| Web frameworks | `gin/`, `middleware/` | Covered |
| CLI frameworks (Cobra, Viper) | `cmd/` covers flag, `gin/Config.md` mentions Viper | Partially covered -> gap 3 |
| Containers and orchestration (Docker, Kubernetes) | 17 scattered mentions, no body page | Partially covered -> gap 2 |

## 4. Application scenario mapping

| Scenario | Repo location | Verdict |
| --- | --- | --- |
| Cloud and network services | None | Gap 2 |
| CLI | `cmd/` 6 pages (design, flag, parsing) | Partially covered -> gap 3 |
| Web development | `gin/`, `net/`, `middleware/` | Partially covered -> gap 5 |
| DevOps/SRE | None | Gap 4 |
| Application scenario overview and company case studies | None | Gap 1 |
| Distributed systems | `distribution/Readme.md` 1 page | Partially covered (not filling, content is self-consistent) |
| Middleware (Kafka, message queues, Redis) | `middleware/`, `redis/` 11 pages | Covered |
| Log aggregation (fluentd) | `log/Aggregation.md` | Covered |

## 5. Issues found and fixed during reconciliation

| Location | Issue | Fix |
| --- | --- | --- |
| `env/Install.md`, `env/Goland.md`, `env/Vim.md`, `env/vscode.md` | 6 download links pointed to `https://golang.org/dl/`; the official download entry point has been consolidated onto `go.dev` | Changed to `https://go.dev/dl/` |
| `idioms/Idioms.md` | Effective Go link pointed to the old `golang.org/doc/effective_go.html` path | Changed to `https://go.dev/doc/effective_go` |
| Version statements | Needed to confirm whether the Go 1.25/1.26/1.27 mentioned in this repo matches the official release line | Official `go1.27.0` (2026-08-19) and `go1.27.1` (2026-09-01) are on the stable line; this repo's statements are kept |
| `docs/zh/research/README.md` | Draft link was misspelled as `Coverge.md` | Changed to `Coverage.md` |
| `SUMMARY.md` | `[Advanced applications](gin/Advanced.md)` case did not match the actual file `gin/advanced.md` | Changed to `gin/advanced.md` |
| `.vitepress/config.mts` | Comment said "49 top-level chapters", inconsistent with the 51 groups after adding research and application scenarios | Comment changed to 51 top-level groups |

## 6. The three items not filled, and why

1. **Contribution guide**: aimed at people submitting code to Go projects; this site has no Go project contribution workflow to organize from.
2. **Module publishing workflow**: this repo does not publish external modules; `mod/Mod.md` already covers semantic versioning and the major-version path, which is enough.
3. **Standalone gRPC page**: `grpc.io` and `protobuf.dev` are unreachable on this machine's network, and the official cloud scenario page only has one line of ecosystem mention, so a sourced technical page cannot be written.

## Sources

1. https://golang.google.cn/doc/ -- official documentation overview
2. https://golang.google.cn/doc/effective_go -- Effective Go table of contents
3. https://golang.google.cn/pkg/go/build/ -- build constraint definition
4. https://golang.google.cn/pkg/cmd/go/ -- Build constraints section
5. https://golang.google.cn/ref/mem -- memory model
6. https://golang.google.cn/doc/pgo -- PGO
7. https://golang.google.cn/doc/fuzz/ -- fuzzing
8. https://golang.google.cn/doc/jsonv2-migration -- json/v2
9. https://golang.google.cn/doc/devel/release -- release history and support policy
10. https://golang.google.cn/dl/?mode=json -- stable release go1.27.1
11. https://golang.google.cn/security/ -- official security page
12. https://golang.google.cn/solutions/use-cases -- the four scenarios
13. https://golang.google.cn/solutions/cloud/, `/clis/`, `/webdev/`, `/devops/` -- the four scenarios in detail
14. https://book.douban.com/tag/Go -- the reading list used for the book chapter mapping

<!-- BACKLINKS-AUTO -->
## Related pages

- [knowledge](/knowledge.md)
- [OfficialDocs](/research/OfficialDocs.md)
- [README](/research/README.md)