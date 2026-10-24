# Go knowledge-point index

I have organized the books, official documentation and application scenarios I consulted on 2026-10-08 into this knowledge-point index. The survey drafts and sources are in `docs/zh/research/`; this page summarizes the main findings and the entry points to the pages.

Source-labelling rule: official content was fetched from the `golang.google.cn` mirror (the footer says go.dev, the body matches the main site, fetch date 2026-10-08); books come from Douban Books and Dangdang entries (same-day fetch); the survey's own judgments are marked "survey conclusion". As of the writing date (2026-10-10), this document contains no unsupported entries; later additions without a source will be marked "source unverified" in place.

## 1. Language and core concepts

1. **Official positioning**: the official documentation overview defines Go as expressive, concise, clean and efficient; its concurrency mechanism lets programs saturate multicore and networked machines; its type system supports flexible modular construction; it compiles fast, with garbage collection and runtime reflection; a statically typed compiled language that reads like a dynamic interpreted language. This is a Chinese translation of the official wording; see [OfficialDocs.md](/research/OfficialDocs.md).

2. **CSP concurrency model**: Go's concurrency follows CSP; the core line is share by communicating -- not communicating through shared memory, but sharing memory through communication (Effective Go section 14; the official page labels Effective Go "required reading for new Go programmers"). A goroutine is a lightweight unit of execution scheduled by the runtime, and a channel is a typed communication pipe. This repo's `concurrency/` 13 pages plus `sync/` 14 pages are the densest part of the whole repo; see [EffectiveGo.md](/idioms/EffectiveGo.md) for the guide.

3. **Memory model and happens before**: the official memory model (The Go Memory Model) only guarantees for synchronization primitives -- channel send/receive, locks, `sync.Once`, goroutine launch and the other rules listed in the documentation establish happens before; a program with no data race behaves sequentially consistently (DRF-SC), and the proof route is the same as Boehm and Adve's 2008 PLDI paper. Reads and writes without synchronization protection may be reordered by both compiler and processor. Source [`/ref/mem`](https://golang.google.cn/ref/mem); body page [MemoryModel.md](/gc/MemoryModel.md).

4. **Type system**: interfaces are implicitly implemented, so a type need not declare what it implements; composition goes through embedding; generics (type parameters) are now part of the language. The language specification ([`/ref/spec`](https://golang.google.cn/ref/spec), 341 KB fetched) is the sole grammatical authority; this repo's `syntax/`, `type/` and `func/` have corresponding content but do not cite the specification text, so the gap table records it as "content present, no citations"; see table 2 in [Coverage.md](/research/Coverage.md).

5. **GC and runtime**: the official GC guide ([`/doc/gc-guide`](https://golang.google.cn/doc/gc-guide), 103 KB) is the official source for tuning GOGC and GOMEMLIMIT, and GC frequency is controlled by those two variables; low-latency GC is the reason Twitch names when citing Go. This repo's `gc/` and `alloc/` each have only 2 pages, shallower than *Go: Design and Implementation*; the gap table marks it "partially covered"; see 2 in [Books.md](/research/Books.md).

## 2. Toolchain and engineering practice

6. **Build constraints**: `//go:build` is the recommended syntax from Go 1.17 onward; the old `// +build` form is kept in sync automatically by gofmt. From Go 1.21 build constraints can reference a language version (for example `go1.21`). File-name suffixes (`_linux`, `_amd64`) are implicit constraints. Sources [`/pkg/go/build/`](https://golang.google.cn/pkg/go/build/) and [`/pkg/cmd/go/`](https://golang.google.cn/pkg/cmd/go/); body page [BuildConstraint.md](/start/BuildConstraint.md).

7. **Native fuzzing**: built in from Go 1.18, using coverage guidance to explore inputs. Test functions are written as `FuzzXxx(*testing.F)`; they run as unit tests by default, and add `-fuzz=FuzzTestName` to actually fuzz. Parameter types are restricted to `string`, `[]byte`, integers, floating point and `bool`. Supported by OSS-Fuzz. Seed corpora use `f.Add` or go in `testdata/fuzz/`. Source [`/doc/fuzz/`](https://golang.google.cn/doc/fuzz/); body page [Fuzz.md](/zh/test/Fuzz.md).

8. **PGO**: profile-guided optimization has been available since Go 1.20; the official benchmarks say CPU-bound programs gain 2%-14% (data from Go 1.22 onward). The official page also states plainly: microbenchmarks are usually a bad profiling source; only a pprof profile taken under real traffic is representative. Source [`/doc/pgo`](https://golang.google.cn/doc/pgo); body page [PGO.md](/debug/PGO.md).

9. **json/v2**: `encoding/json` is not going away, it is protected by the Go 1 compatibility commitment, and v1 and v2 are mutually compatible. The new struct tags introduced together with `encoding/json/v2` in Go 1.27 are supported by `encoding/json` as well. The real difference is default strictness: invalid UTF-8 is silently replaced with the replacement character in v1, but reports an error outright in v2. Source [`/doc/jsonv2-migration`](https://golang.google.cn/doc/jsonv2-migration); body page [JsonV2.md](/encoding/JsonV2.md).

10. **The testing three-piece set**: table-driven tests, benchmarks (`testing.B`) and coverage ([`/doc/build-cover`](https://golang.google.cn/doc/build-cover), this repo's `test/Cover.md`) are the usual three, and native fuzzing from 1.18 becomes the fourth. The table-driven style is in `test/Practice.md`. Sources in table 2 of [Coverage.md](/research/Coverage.md).

11. **Versions and support policy**: each major version is supported until two newer major versions appear, and security fixes only go to the two most recent major versions; a major version every half year, `go1.26.0` released 2026-02-10, `go1.27.0` released 2026-08-19, `go1.27.1` released 2026-09-01. Sources [`/doc/devel/release`](https://golang.google.cn/doc/devel/release) and [`/dl/?mode=json`](https://golang.google.cn/dl/?mode=json); body page [ReleaseNotes.md](/introduction/ReleaseNotes.md).

12. **Official security position**: the official security page ([`/security/`](https://golang.google.cn/security/)) maintains a vulnerability database and provides accompanying checking tools; use `crypto/rand` for cryptographic randomness, `math/rand` cannot take that role; the standard library has FIPS 140-3 compliance machinery. The full original text on the vulnerability response process was not retrieved during the survey, and the body page notes that faithfully; see [Security.md](/security/Security.md).

## 3. Application scenarios

13. **Four-scenario overview**: the official page groups Go's uses into four categories -- cloud and network services, command-line interfaces (CLI), web development, DevOps and SRE, index page [`/solutions/use-cases`](https://golang.google.cn/solutions/use-cases). This repo previously had not one scenario page; after the survey, five pages were built under `docs/zh/applications/`, overview at [Applications.md](/applications/Applications.md), drafts at [Scenarios.md](/research/Scenarios.md).

14. **Cloud and network services**: the hardest citable number is that over 75% of CNCF projects are written in Go (the official page is dated 2019-10-04, so cite it with the date). Both Docker and Kubernetes are Go projects; Dropbox began migrating performance-critical backends from Python to Go in 2013, and most of its infrastructure is Go today; Uber has the real-time analytics engine AresDB, the geofencing service Geofence and the resource scheduler Peloton. The standard ecosystem is Swagger, protocol buffers, gRPC. Source [`/solutions/cloud/`](https://golang.google.cn/solutions/cloud/); body page [CloudNative.md](/applications/CloudNative.md).

15. **CLI**: compiles to a single self-contained binary, depends on no runtime, startup time close to C/C++; the official wording is that no other compiled language builds this portably and this fast. Cobra is both a library and a code generator, used by CoreOS, Docker, Hugo and Kubernetes; Viper handles configuration, and the two go together; single-binary installation accounts for some of Hugo's popularity. Source [`/solutions/clis/`](https://golang.google.cn/solutions/clis/); body page [CLI.md](/applications/CLI.md).

16. **Web development**: the standard library ships with an HTTP server and template library, supporting HTTP/2 and TLS 1.3; third-party frameworks are not required in most scenarios. Two numbers from Hexact's CTO: goroutines handling internal requests are 10x cheaper in resources than Python threads, and code volume dropped 64% after the rewrite (quotations on the official page, not this repo's test results). Caddy 2's automatic HTTPS uses the standard library TLS stack. Source [`/solutions/webdev/`](https://golang.google.cn/solutions/webdev/); body page [Web.md](/applications/Web.md).

17. **DevOps and SRE**: SRE originated at Google, and Amazon and Netflix later adopted it; Docker (CI/CD automation and deployment), Drone (continuous delivery on containers), etcd (strongly consistent distributed key-value store) and Netflix's Rend caching service are all Go. The standard library covers HTTP, file I/O, time, regex, exec and JSON, so operations scripts go straight into business logic. Source [`/solutions/devops/`](https://golang.google.cn/solutions/devops/); body page [DevOps.md](/applications/DevOps.md).

18. **Numbers from three official case studies**: American Express (page date 2019-12-19) runs both its payments and rewards networks on Go, and the engineering director's point is the low cognitive load, with most Go code looking much the same; PayPal (2020-06-01) rewrote its C++ NoSQL database in Go, with six months of learning and migration, and 30% of clusters switched; MercadoLibre spans 18 countries, migrated from Groovy/Grails starting in 2015, and its core user API averages 8 to 10 million requests per minute with response times under 10 milliseconds. Sources [`/solutions/americanexpress`](https://golang.google.cn/solutions/americanexpress), [`/solutions/paypal`](https://golang.google.cn/solutions/paypal), [`/solutions/mercadolibre`](https://golang.google.cn/solutions/mercadolibre).

## 4. Key points from authoritative books

All bibliographic data comes from Douban and Dangdang entries fetched on 2026-10-08; the full reading list, ratings and fetch sources are in [Books.md](/research/Books.md).

19. ***The Go Programming Language***, Alan A. A. Donovan, Brian W. Kernighan, China Machine Press Chinese edition (English edition Addison-Wesley 2015, Douban 8.6). Corresponding knowledge points: the full spine of syntax, types, methods and interfaces, packages, testing, concurrency and reflection, threaded with a web forum case study. Survey conclusion: this repo's chapter spine is basically isomorphic with it.

20. ***Go: Design and Implementation***, Zuo Shuqi, Posts & Telecom Press 2021-11 (Douban 8.1). Corresponding knowledge points: source-level implementation of the compiler, runtime, GMP scheduling and GC; a print edition of the open-source ebook, with nearly 200 figures. An advanced reference for this repo's `alloc/`, `gc/`.

21. ***Go Expert Programming***, Ren Hongcai, Publishing House of Electronics Industry 2020-7 (Douban 8.9). Corresponding knowledge points: internal implementation of common features, much content drawn from source-code analysis.

22. ***Concurrency in Go***, Katherine Cox-Buday, O'Reilly 2017-08 (Chinese translation *The Way of Go Concurrency*, China Electric Power Press 2018-12). Corresponding knowledge points: goroutine, synchronization primitives, pipeline patterns, data races, context, and the decision discipline of "which primitive when". Survey conclusion: this repo's concurrency pages have enough density; what was missing is exactly the page that synthesizes them, and the gap is logged.

23. ***Understanding Go Concurrency in Depth***, Chao Yuepan, Publishing House of Electronics Industry 2023-11 (Douban 8.0). Corresponding knowledge points: implementation and choice boundaries of standard-library synchronization primitives such as Mutex and RWMutex.

24. ***Go: Advanced Programming (2nd edition)***, Chai Shushan, Cao Chunhui, Wang Min, Posts & Telecom Press 2025-7. Corresponding knowledge points: cgo, assembly, syntax trees, unsafe, gRPC and cloud native. An advanced reference for this repo's four low-level pages (`alloc/`, `gc/`, `asm/`, `cgo/`, each 1-2 pages).

25. ***The Path to Go Mastery*** (vol. 1 and 2), Bai Ming, China Machine Press 2021-12 (vol. 1 Douban 8.7). Corresponding knowledge points: writing code that follows Go conventions, along the two lines of programming mindset and practical technique.

26. ***Build Your Own Docker***, Chen Xianlu, Wang Bingshen, Qin Yujia, Publishing House of Electronics Industry 2017-7 (Douban 7.3). Corresponding knowledge points: disassembling the container tech stack, implementing the engine in Go step by step.

27. Quick look at the remaining titles (one line each, ratings and authors per the Douban entries):

| Book | Author | Corresponding knowledge points |
| --- | --- | --- |
| *Deep Dive into Go* | Feng Youlin (Tsinghua 2022-8, 8.5) | Object model and runtime implementation |
| *A Guide to Customizing Go* | Chai Shushan, Shi Bin, Ding Ernan (Posts & Telecom 2022-2) | Syntax trees, `go fmt`, `go doc` tool construction |
| *Go Core Programming* | Li Wenta (Publishing House of Electronics Industry 2018-9, 7.2) | Basics plus the three major language features |
| *A Go Programming Journey* | Chen Jianyu, Xu Xinhua (Publishing House of Electronics Industry 2020-6, 7.8) | Five projects: command line, HTTP, RPC, WebSocket, cache |
| *Cloud Native Go* | Kevin Hoffman, Dan Nemeth (Publishing House of Electronics Industry 2017-7) | Cloud-native web and microservices |
| *Enterprise-Grade Go Project Development in Practice* | Kong Lingfei (China Machine Press 2023-1) | Enterprise-grade project end to end |
| *Go Web Programming in Practice* | Liao Xiandong (Publishing House of Electronics Industry 2021-4) | Four-part web development structure |
| *Go Concurrent Programming in Practice* | Hao Lin (Posts & Telecom 2015-1, 6.2) | Concurrency practice, published earlier |
| *Head First Go* | Jay McGavren (O'Reilly 2018, 8.6) | Basics |
| *Learning Go, 2nd Edition* | Jon Bodner (O'Reilly 2024) | Basics and intermediate content |
| *An Introduction to Programming in Go* | Caleb Doxsey (CreateSpace 2012, 7.6) | Basics |
| *Go Programming: From Beginner to Advanced Practice* | Xu Bo (China Machine Press 2018-6) | Project work from basics to advanced |

## 5. Common pitfalls and misconceptions

28. **The old `golang.org` domain**: the download page and documentation entry points have been consolidated onto `go.dev`, and old `golang.org` links no longer work. Reconciliation record: 6 dead `golang.org/dl/` links across the four `env/` pages in this repo, and the old `effective_go.html` path in `Idioms.md`, all corrected. Cite official resources with `go.dev` or the `golang.google.cn` mirror. See 5 in [Coverage.md](/research/Coverage.md).

29. **File-name case**: macOS and Windows file systems are case-insensitive, Linux is case-sensitive. Record: `SUMMARY.md` wrote `gin/Advanced.md` while the file on disk is `gin/advanced.md`, which looked fine locally but broke the link on a Linux build (or CI). Links must match the actual file name from `ls` character for character.

30. **Misreading json v1/v2 compatibility**: v2 and v1 coexist, `encoding/json` is not going away, and the two are interoperable; the behavioral difference is default strictness, typically invalid UTF-8 (v1 replaces silently, v2 errors). Treating it as "swapping in a new library" misjudges the migration cost. Source [`/doc/jsonv2-migration`](https://golang.google.cn/doc/jsonv2-migration); see point 9 above.

31. **Choosing the wrong profiling source for PGO**: using a microbenchmark profile for PGO is the bad practice the official page names; only a profile taken under real load on the application is valid. The 2%-14% figure is the official documentation's benchmark conclusion, not a measurement by this repo; cite it with the source. See point 8 above.

32. **The fuzz parameter type whitelist**: `FuzzXxx` parameters are restricted to `string`, `[]byte`, integers, floating point and `bool`; you cannot fuzz a struct or map directly. Serialize complex inputs to `[]byte` first, then pass them into the fuzz function. Source [`/doc/fuzz/`](https://golang.google.cn/doc/fuzz/); see point 7 above.

33. **The sequential intuition for the memory model**: reads and writes without synchronization protection may be reordered by both compiler and processor; the basis for judgment is happens before, and the order of lines in code says nothing about it. "Surely this must happen" does not hold outside channels, locks and `sync.Once`. Source [`/ref/mem`](https://golang.google.cn/ref/mem); see point 3 above.

34. **Hard-coded counts going stale**: writing fixed numbers like "8 pages" or "47 directories" into the docs becomes untrue as soon as the directory moves. Reconciliation record: `test/` went from 8 to 9 pages, and there are 42 topic directories in fact. Either carry a verification date with a number, or give a recomputable basis. See 5 in [Coverage.md](/research/Coverage.md).

## 6. Sources and navigation

Survey drafts (fetch methods, per-item sources, full comparison tables):

- [research/README.md](/research/README.md) -- survey overview and the three facts stated up front
- [research/Books.md](/research/Books.md) -- full reading list and fetch sources
- [research/OfficialDocs.md](/research/OfficialDocs.md) -- official documentation section structure and links
- [research/Scenarios.md](/research/Scenarios.md) -- the four scenarios and case numbers
- [research/Coverage.md](/research/Coverage.md) -- coverage reconciliation gap table and fix record

Body pages produced from the survey gaps (13 in all):

- Application scenarios: [Applications.md](/applications/Applications.md), [CloudNative.md](/applications/CloudNative.md), [CLI.md](/applications/CLI.md), [DevOps.md](/applications/DevOps.md), [Web.md](/applications/Web.md)
- Official documentation entry points: [MemoryModel.md](/gc/MemoryModel.md), [PGO.md](/debug/PGO.md), [Fuzz.md](/zh/test/Fuzz.md), [BuildConstraint.md](/start/BuildConstraint.md), [JsonV2.md](/encoding/JsonV2.md), [ReleaseNotes.md](/introduction/ReleaseNotes.md), [EffectiveGo.md](/idioms/EffectiveGo.md), [Security.md](/security/Security.md)

Term lookup: [glossary](/glossary.md) (Chinese-English pairs, one-sentence definitions, authoritative sources and related pages).

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)