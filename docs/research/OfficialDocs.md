# Official documentation survey

The official documentation entry point is https://go.dev/doc/. From this machine only its mainland China mirror https://golang.google.cn/doc/ is reachable (the footer still says go.dev, and the body is identical). The following describes the page structure as fetched from the mirror; date 2026-10-08.

## 1. The sections the documentation overview page lists

The overview page I fetched cuts the documentation into four blocks. Each block's counterpart in this repo is below:

| Official section | Official pages | This repo's counterpart |
| --- | --- | --- |
| Getting Started | Installation, the Getting started page, Create a module, multi-module workspaces, writing a RESTful API with Gin, the official generics docs, the Fuzzing page (external link) | `docs/zh/env/`, `docs/zh/start/`, `docs/zh/mod/`, `docs/zh/gin/`, `docs/zh/generics/` |
| Writing Web Applications | A complete example of a simple web application | `docs/zh/gin/`, `docs/zh/net/` |
| Using and understanding Go | Effective Go, FAQ, editor plugins and IDEs, diagnostics, GC guide, dependency management, fuzzing, coverage, PGO, json/v2 migration | Partly present, partly missing; see [Coverage.md](/research/Coverage.md) |
| References | Standard library package docs, command docs, language specification, Go Modules reference, go.mod reference, memory model, contribution guide, release history, database access docs, module development and publishing | `docs/zh/mod/` has the module part; the memory model, release history and contribution guide had no pages before |

The overview page's definition of Go is: expressive, concise, clean and efficient; its concurrency mechanism lets programs saturate multicore and networked machines; its type system supports flexible modular construction; it compiles fast, with garbage collection and runtime reflection; a statically typed compiled language that reads like a dynamic interpreted language. This is a Chinese translation of the official wording, and it can serve as the reference wording for this repo's `docs/zh/introduction/`.

## 2. Effective Go

The official page labels Effective Go as "required reading for any new Go programmer", and asks you to read the Tour and the language specification first. The fetched table of contents has 16 top-level sections:

1. Introduction
2. Formatting
3. Commentary
4. Names
5. Semicolons
6. Control structures
7. Functions
8. Data
9. Initialization
10. Methods
11. Interfaces and other types
12. The blank identifier
13. Embedding
14. Concurrency
15. Errors
16. A web server

Of the 40 second-level sections (such as `MixedCaps`, `Defer`, `Allocation with make`, `Share by communicating`, `A leaky buffer`, `Panic`, `Recover`), most have a counterpart page in this repo, but there was previously no index mapping the 16 sections to this site's pages. That has now been filled in as `docs/zh/idioms/EffectiveGo.md`.

## 3. Specification, FAQ and Tour

- The **language specification** (`/ref/spec`, 341 KB fetched) is the sole grammatical authority; not a single page in this repo's `docs/zh/syntax/` or `docs/zh/type/` cites it. The gap table records this as "content present, no citations".
- The **FAQ** (`/doc/faq`, 133 KB) answers questions like "does Go have generics, why no classes, why errors are returned as values"; this repo's `docs/zh/generics/` and `docs/zh/oop/` cover two of those topics.
- **A Tour of Go** (`/tour/`, officially described as a four-part structure: basic syntax and data structures, methods and interfaces, generics, concurrency, each part ending in exercises) matches this repo's chapter order.

## 4. Releases and versions

The release history page `/doc/devel/release` gives two hard facts:

- Support policy: each major version is supported until two newer major versions have been released. The page's own example: Go 1.5 was supported until Go 1.7 shipped, Go 1.6 until Go 1.8 shipped; security fixes only go to the two most recent major versions.
- Timeline: `go1.27.0` released 2026-08-19, `go1.27.1` released 2026-09-01; the previous major, `go1.26.0`, released 2026-02-10, and patch releases for the 1.26 series ran through `go1.26.8` (2026-09-01). The half-yearly major-version cadence is visible straight from those two dates.

The first entry in the stable-release list returned by `/dl/?mode=json` is `go1.27.1`, which lines up with the Go 1.27 mentions in this repo's `docs/zh/asm/Assembly.md` and `docs/zh/net/Netpoll.md`. That gap has been filled with `docs/zh/introduction/ReleaseNotes.md`.

## 5. Tools and related documentation

| Topic | Official page | This repo's status |
| --- | --- | --- |
| GC | `/doc/gc-guide` (A Guide to the Go Garbage Collector, 103 KB) | `docs/zh/gc/GC.md`, `docs/zh/alloc/GC.md` have content |
| Memory model | `/ref/mem` (The Go Memory Model) | During reconciliation it appeared only once, on the home page; filled with `docs/zh/gc/MemoryModel.md` |
| PGO | `/doc/pgo` | During reconciliation it was mentioned in one sentence on the GC page; filled with `docs/zh/debug/PGO.md` |
| Fuzzing | `/doc/fuzz/`, `/doc/tutorial/fuzz.html`, `/security/fuzz` | During reconciliation there was only old go-fuzz toolchain content; native fuzzing filled with `docs/zh/test/Fuzz.md` |
| Coverage | `/doc/build-cover` | `docs/zh/test/Cover.md` already exists |
| json/v2 | `/doc/jsonv2-migration`, `/pkg/encoding/json/v2` | During reconciliation there was no body page; filled with `docs/zh/encoding/JsonV2.md` |
| Build constraints | `/pkg/go/build/`, the Build constraints section of `/pkg/cmd/go/` | During reconciliation there was no body page; filled with `docs/zh/start/BuildConstraint.md` |
| Editors | `/gopls`, the editor plugin page on `/doc/` | `docs/zh/env/vscode.md`, `docs/zh/env/Goland.md` cover tool installation |
| Contribution guide | `/doc/contribute` | Not applicable; this site records development experience, it is not a Go project repository |

## 6. Key points on native fuzzing and json/v2

- fuzzing: Go has built-in fuzzing in the standard toolchain since **1.18**, using coverage guidance to explore inputs. Test functions are written as `FuzzXxx(*testing.F)`; the invocation is run by default as a unit test, and add `-fuzz=FuzzTestName` when you want to actually fuzz. Parameter types are restricted to `string`, `[]byte`, integers, floating point and `bool`. Native fuzz tests are supported by OSS-Fuzz.
- json/v2: `encoding/json` is not going away, it is protected by the Go 1 compatibility commitment, and v1 and v2 are mutually compatible. v2 is stricter by default -- for example invalid UTF-8 is silently replaced with the replacement character in v1, but reports an error outright in v2. The new struct tags introduced together with `encoding/json/v2` in Go 1.27 are supported by `encoding/json` as well.

Both points have been written verbatim into `docs/zh/test/Fuzz.md` and `docs/zh/encoding/JsonV2.md`.

## Sources

1. https://golang.google.cn/doc/ -- documentation overview (Getting Started, Writing Web Applications, Using and understanding Go, References)
2. https://golang.google.cn/doc/effective_go -- 16 top-level and 40 second-level sections
3. https://golang.google.cn/ref/spec -- language specification (341 KB)
4. https://golang.google.cn/doc/faq -- official FAQ
5. https://golang.google.cn/doc/devel/release -- support policy and the 1.26/1.27 release dates
6. https://golang.google.cn/dl/?mode=json -- stable release go1.27.1
7. https://golang.google.cn/doc/pgo -- PGO definition and the 2%-14% benchmark improvement from Go 1.22
8. https://golang.google.cn/doc/fuzz/ -- fuzzing requirements and invocation
9. https://golang.google.cn/ref/mem -- memory model, DRF-SC wording
10. https://golang.google.cn/pkg/go/build/ -- `//go:build` and file-name constraints
11. https://golang.google.cn/pkg/cmd/go/ -- the full Build constraints section
12. https://golang.google.cn/doc/jsonv2-migration -- v2 migration position
13. https://golang.google.cn/gopls -- language server
14. https://golang.google.cn/tour/ -- the four-part Tour

<!-- BACKLINKS-AUTO -->
## Related pages

- [knowledge](/knowledge.md)
- [README](/research/README.md)