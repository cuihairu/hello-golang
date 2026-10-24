# Effective Go: the 16 sections mapped to this site's pages

The official docs call Effective Go "a must read for any new Go programmer" and suggest reading the Tour and the language spec first. This repo links to it once each in `docs/zh/idioms/` and `docs/zh/naming/`. I've laid out the correspondence between the 16 sections and this site's pages in the table below. References fetched 2026-10-08.

## 1. The 16 sections mapped to this repo's pages

| Effective Go section | What it covers | This repo's pages |
| --- | --- | --- |
| Introduction | Go's design trade-offs | `docs/zh/introduction/Feature.md` |
| Formatting | `gofmt` enforces uniform formatting | `docs/zh/naming/Naming.md`, `docs/zh/env/Tools.md` |
| Commentary | package comments and `godoc` | `docs/zh/mod/Package.md`, `docs/zh/env/Tools.md` |
| Names | naming, MixedCaps, export rules | `docs/zh/naming/IdentifierNamingRules.md`, `docs/zh/idioms/Idioms.md` |
| Semicolons | automatic semicolon insertion rules | the control flow pages in `docs/zh/syntax/` |
| Control structures | if/for/switch, type switch | `docs/zh/syntax/Conditional.md`, `docs/zh/syntax/Loop.md`, `docs/zh/type/Switch.md` |
| Functions | multiple return values, named return values, defer | `docs/zh/func/MultipleReturnValues.md`, `docs/zh/func/Defer.md` |
| Data | arrays, slices, maps, printing, append, constants, variables | the corresponding pages in `docs/zh/type/` and `docs/zh/const/` |
| Initialization | initialization, the `init` function, composite literals | `docs/zh/const/Const.md`, `docs/zh/var/VarAndInit.md` |
| Methods | methods, pointer and value receivers | `docs/zh/oop/Methods.md`, `docs/zh/oop/PointerReceiver.md` |
| Interfaces and other types | interface naming, assertions, generalization | `docs/zh/oop/InterfaceImpl.md`, `docs/zh/type/Assertion.md` |
| The blank identifier | the blank identifier, multi-value assignment, import side effects | `docs/zh/idioms/BlankIdentifier.md` |
| Embedding | embedding to extend interfaces and structs | `docs/zh/oop/Embedding.md` |
| Concurrency | share by communicating, goroutines, channels, parallelization | `docs/zh/concurrency/CSP.md`, `docs/zh/concurrency/Goroutine.md`, `docs/zh/concurrency/Chan.md` |
| Errors | panic, recover, error values | `docs/zh/error/Errors.md`, `docs/zh/error/PanicAndRecover.md` |
| A web server | a complete HTTP server example | `docs/zh/net/Intro.md`, `docs/zh/gin/` |

Of the 40 second-level subsections, the ones where this repo has standalone content are `Defer`, `Allocation with make`, `Interfaces`, `Panic`, `Recover`, and `MixedCaps`. The two pages that go finer than Effective Go are `GMP scheduler` and `Channel implementation`; they go beyond the original's scope.

## 2. Official reading suggestions and this site's pages

The official recommendation is Tour → language spec → Effective Go. Following that recommendation, this site's pages:

1. Basic syntax and data types: `docs/zh/start/Hello.md`, `docs/zh/syntax/`, `docs/zh/type/`.
2. Methods, interfaces and packages: `docs/zh/oop/`, `docs/zh/mod/`.
3. Testing: `docs/zh/test/` (Effective Go has no dedicated chapter on testing).
4. Concurrency: `docs/zh/concurrency/`, corresponding to the Concurrency section.
5. The Effective Go original: this page serves as the corresponding index.

## 3. Two reminders from the official docs

- The language spec (`/ref/spec`) and the Tour should be read first; Effective Go is writing advice on top of them, not a grammar definition.
- On the A web server section, the official docs say: it shows a small but complete program, focused on the way it's organized, not on production readiness.

## Sources

1. https://golang.google.cn/doc/effective_go — the 16 top-level sections and 40 second-level subsections outline, and the "a must read for any new Go programmer" positioning (fetched 2026-10-08)
2. https://golang.google.cn/doc/ — the Effective Go ordering note in the docs overview (read tour and spec first)
3. https://golang.google.cn/tour/ — the Tour's four-part structure

## References

- [Effective Go (official)](https://go.dev/doc/effective_go)

<!-- BACKLINKS-AUTO -->
## Related pages

- [BlankIdentifier](/idioms/BlankIdentifier.md)
- [CommaOk](/idioms/CommaOk.md)
- [Idioms](/idioms/Idioms.md)
- [Labels](/idioms/Labels.md)
- [Range](/idioms/Range.md)
- [ShortVarDecl](/idioms/ShortVarDecl.md)
- [knowledge](/knowledge.md)
