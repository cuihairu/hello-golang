# Survey overview

This directory records an external knowledge survey performed against this repo: first gather three kinds of material -- comparable classic books, the Go official documentation, and the officially published application scenarios -- then break those three kinds of material into checkable topics, compare them one by one against the 368 pages already under this repo's `docs/`, and finally turn the gaps into new pages.

Fetch and verification date: 2026-10-08.

## How the three kinds of material were obtained

- **Official documentation**: `go.dev` is unreachable from this machine's network, so the official mainland China mirror `golang.google.cn` was used instead; the page footer still says `go.dev`, and the content matches the main site. The text retrieved includes the documentation overview, Effective Go, the language specification, release history, PGO, fuzzing, the memory model, `go` command docs, the security page, the four application scenario pages, and three company case studies.
- **Comparable books**: the 4 pages of listings under the `Go` tag on Douban Books (100 entries in total) were taken, then entries aggregated by Sogou and 360 search from Douban and Dangdang were used to fill in books like *The Go Programming Language* that are not on the tag's front page. Book titles, authors, publishers, publication dates and Douban ratings all come from the fetched page text; nothing was filled in from memory.
- **Application scenarios**: all taken from the official `solutions/` pages (cloud and network services, CLI, web development, DevOps/SRE) and the three official case studies (American Express, PayPal, MercadoLibre); every number and quotation can be located in the original text.

## The four body pages

| Document | Content |
| --- | --- |
| [Books.md](/research/Books.md) | Layered reading list of comparable classic books, with authors, publishers, years, ratings and focus |
| [OfficialDocs.md](/research/OfficialDocs.md) | The official documentation's section structure and what each section means for this repo |
| [Scenarios.md](/research/Scenarios.md) | The official four application scenarios and company case numbers |
| [Coverage.md](/research/Coverage.md) | The coverage reconciliation gap table: source topic -> repo page -> verdict -> remediation |

The 13 items judged as "gap" in the gap table have each been filled in as a body page, spread across `docs/zh/applications/`, `docs/zh/start/`, `docs/zh/gc/`, `docs/zh/debug/`, `docs/zh/test/`, `docs/zh/idioms/`, `docs/zh/introduction/`, `docs/zh/encoding/`, `docs/zh/security/`.

## Three facts to state up front

1. The official current stable release is **go1.27.1** (`go1.27.0` released 2026-08-19, `go1.27.1` released 2026-09-01); this repo's version-related statements line up with it.
2. The official support policy is **each major version is supported until two newer major versions appear** (verbatim from the Release Policy), so 1.26 and 1.27 remain supported after 1.28 ships.
3. This repo's pages are complete by topic (directories for syntax, types, concurrency, sync, testing, database, Gin, etc. -- 42 on the verification date, 44 after adding application scenarios and the survey directory) -- there is no shortage of language knowledge; what was missing was **official-documentation-entry pages** (memory model, PGO, fuzzing, build constraints, json/v2, security) and **application scenario pages** (not one of the four scenarios existed before).

## Source list

1. https://golang.google.cn/doc/ -- official documentation overview
2. https://golang.google.cn/doc/effective_go -- Effective Go
3. https://golang.google.cn/ref/spec -- Go language specification
4. https://golang.google.cn/doc/faq -- official FAQ
5. https://golang.google.cn/doc/devel/release -- release history and support policy
6. https://golang.google.cn/dl/?mode=json -- current stable release list
7. https://golang.google.cn/doc/pgo -- profile-guided optimization
8. https://golang.google.cn/doc/fuzz/ -- Go native fuzzing
9. https://golang.google.cn/ref/mem -- Go memory model
10. https://golang.google.cn/pkg/go/build/ -- build constraints
11. https://golang.google.cn/pkg/cmd/go/ -- the `go` command and the `Build constraints` section
12. https://golang.google.cn/doc/jsonv2-migration -- encoding/json/v2 migration guide
13. https://golang.google.cn/security/ -- official security page
14. https://golang.google.cn/solutions/use-cases -- the four application scenarios index
15. https://golang.google.cn/solutions/cloud/ -- cloud and network services scenario
16. https://golang.google.cn/solutions/clis/ -- CLI scenario
17. https://golang.google.cn/solutions/webdev/ -- web development scenario
18. https://golang.google.cn/solutions/devops/ -- DevOps/SRE scenario
19. https://golang.google.cn/solutions/americanexpress -- American Express case study
20. https://golang.google.cn/solutions/paypal -- PayPal case study
21. https://golang.google.cn/solutions/mercadolibre -- MercadoLibre case study
22. https://golang.google.cn/tour/ -- A Tour of Go
23. https://golang.google.cn/doc/code -- How to write Go code
24. https://golang.google.cn/gopls -- gopls editor language server
25. https://book.douban.com/tag/Go -- Douban Books Go tag (pages 1-4)
26. Douban and Dangdang entries aggregated by Sogou and 360 search (bibliographic info for books like *The Go Programming Language*)

Note: `go.dev`, `pkg.go.dev`, `github.com`, `grpc.io` and `kubernetes.io` all fail to establish TLS connections from this machine's network, so every citation in this directory points to a mirror or mainland site that can be reproducibly fetched; where bibliographic information could not be fetched from a mirror, the entry it was aggregated from is named.

<!-- BACKLINKS-AUTO -->
## Related pages

- [knowledge](/knowledge.md)