# Survey of comparable classic books

Conclusion first: this repo's knowledge organization is basically isomorphic with the chapter spine of *The Go Programming Language* (syntax -> types -> methods and interfaces -> packages -> testing -> concurrency -> reflection); what really doesn't line up is the low-level and engineering halves of *Go: Advanced Programming* (cgo, assembly, syntax trees, unsafe, RPC and cloud native), plus the "discipline of writing concurrency correctly" that concurrency books keep hammering -- this repo has pages for it but lacks one page that consolidates the methodology. All bibliographic data comes from Douban and Dangdang entries fetched on 2026-10-08.

## 1. Language bibles

| Title | Author / translator | Publisher · Year | Douban rating | Focus |
| --- | --- | --- | --- | --- |
| *The Go Programming Language* | Alan A. A. Donovan, Brian W. Kernighan | China Machine Press (Chinese edition); English edition Addison-Wesley Professional, 2015 | 8.6 | A web forum runs through the whole book, covering request handlers, templates, concurrency, testing and reflection; co-authored by one of the authors of *The C Programming Language*, known for terse prose |
| *Go Programming* | Chinese-edition entry | Douban entry | 7.1 | Language features only, covering memory management (heap and stack), error handling, OOP, concurrent programming |

The Douban entry for *The Go Programming Language* comes from a Sogou search aggregation of Douban and Dangdang pages: rating 8.6, the Dangdang entry lists the author as Alan A. A. Donovan and the publisher as China Machine Press. This book is the main alignment target for this repo's `docs/` chapters on syntax, types, methods, interfaces and concurrency.

## 2. Advanced and low-level

| Title | Author | Publisher · Year | Douban rating | Focus |
| --- | --- | --- | --- | --- |
| *Go: Advanced Programming (2nd edition)* | Chai Shushan, Cao Chunhui, Wang Min | Posts & Telecom Press · 2025-7 | Few reviews of the new edition (1st-edition entry 7.6) | 10 chapters covering low-level mechanisms, performance tuning, system programming and frontier applications; the 1st-edition short reviews recommend the reading order Go and Web, distributed systems, gRPC and Protobuf, language basics, CGO compilation |
| *Go: Design and Implementation* | Zuo Shuqi | Posts & Telecom Press · 2021-11 | 8.1 (144 ratings) | Print edition of the open-source ebook of the same name, ~200 full-color figures on compilation, runtime, scheduling and GC |
| *Go Expert Programming* | Ren Hongcai | Publishing House of Electronics Industry · 2020-7 | 8.9 (151 ratings) | Much content drawn from source-code analysis, covering internal implementation of common features |
| *Deep Dive into Go: Object Model and the Principles, Features and Applications of the Runtime* | Feng Youlin | Tsinghua University Press · 2022-8 | 8.5 (11 ratings) | Object model and runtime implementation |
| *The Path to Go Mastery: From Beginner to Expert* (vol. 1 and 2) | Bai Ming | China Machine Press · 2021-12 | Vol. 1: 8.7 (168 ratings), vol. 2: 8.2 (55 ratings) | Programming mindset and practical techniques, two dimensions, on writing code that follows Go conventions |
| *A Guide to Customizing Go* | Chai Shushan, Shi Bin, Ding Ernan | Posts & Telecom Press · 2022-2 | -- (10 ratings) | How syntax trees, `go fmt`, `go doc` and similar tools are built |

The low-level layer maps to this repo's `docs/zh/alloc/`, `docs/zh/gc/`, `docs/zh/asm/`, `docs/zh/cgo/`, `docs/zh/reflection/`, each with only 1-2 pages -- the thinnest areas of this repo.

## 3. Concurrency

| Title | Author | Publisher · Year | Douban rating | Focus |
| --- | --- | --- | --- | --- |
| *Understanding Go Concurrency in Depth* | Chao Yuepan | Publishing House of Electronics Industry · 2023-11 | 8.0 (13 ratings) | Part 1, 13 chapters, on synchronization primitives: Mutex, RWMutex and other standard-library primitives |
| *Concurrency in Go* | Katherine Cox-Buday | O'Reilly · 2017-08, 229 pages (English edition) | Chinese translation *The Way of Go Concurrency*, China Electric Power Press · 2018-12, 5.0 (83 ratings) | goroutine, synchronization primitives, pipeline patterns, data races, context |
| *Go Concurrent Programming in Practice* | Hao Lin | Posts & Telecom Press · 2015-1 | 6.2 (86 ratings) | Concurrent programming practice, published earlier |

The concurrency layer has 13 pages in this repo (CSP, Actor, goroutine implementation, channel implementation, select, WaitGroup, ErrorGroup, GMP scheduler) -- density is enough; what's missing is decision content that converges "when to use which primitive" into one page, already logged in the gap table.

## 4. Scenarios and project practice

| Title | Author | Publisher · Year | Douban rating | Focus |
| --- | --- | --- | --- | --- |
| *Build Your Own Docker* | Chen Xianlu, Wang Bingshen, Qin Yujia | Publishing House of Electronics Industry · 2017-7 | 7.3 (97 ratings) | Disassemble the tech stack Docker depends on, write a container engine in Go step by step |
| *A Go Programming Journey: Building Projects Together* | Chen Jianyu, Xu Xinhua | Publishing House of Electronics Industry · 2020-6 | 7.8 (67 ratings) | 6 chapters: command-line applications, HTTP applications, RPC applications, WebSocket applications, in-process cache |
| *Go Web Programming in Practice* | Liao Xiandong | Publishing House of Electronics Industry · 2021-4 | 6.8 (19 ratings) | Organized into four parts by web development topic |
| *Cloud Native Go* | Kevin Hoffman, Dan Nemeth | Publishing House of Electronics Industry · 2017-7 | 6.5 (15 ratings) | Cloud-native web applications and microservices with Go + React |
| *Enterprise-Grade Go Project Development in Practice* | Kong Lingfei | China Machine Press · 2023-1 | New book, few reviews | Enterprise-grade project end to end |
| *Go Core Programming* | Li Wenta | Publishing House of Electronics Industry · 2018-9 | 7.2 (69 ratings) | Basics plus the three major language features |

Scenario material maps to this repo's `docs/zh/gin/` (13 pages), `docs/zh/cmd/` (6 pages, flag and command-line design), `docs/zh/middleware/` (Kafka, message queues); `docs/zh/applications/` previously had no pages at all, the biggest blank spot in the gap table.

## 5. Introductory reads and English originals

| Title | Author | Publication info | Douban rating |
| --- | --- | --- | --- |
| *Head First Go* | Jay McGavren | O'Reilly · 2018-6-25 | 8.6 (38 ratings) |
| *Learning Go, 2nd Edition* | Jon Bodner | O'Reilly · 2024-2-27 | 16 ratings |
| *An Introduction to Programming in Go* | Caleb Doxsey | CreateSpace · 2012-9-3 | 7.6 (67 ratings) |
| *Go Programming: From Beginner to Advanced Practice* | Xu Bo | China Machine Press · 2018-6 | 6.6 (29 ratings) |

## 6. Three requirements the reading list places on this repo

1. The four low-level pages (alloc, gc, asm, cgo) should move toward the depth of *Go: Design and Implementation* and *Go Expert Programming*: explain data structures and source-code paths, not just conclusions.
2. The concurrency section should absorb the primitive-choice material from *Understanding Go Concurrency in Depth*: the applicable boundaries and costs of mutex, read-write lock, atomics and channels.
3. The scenario section should fill in the four application categories in official voice (cloud and network services, CLI, Web, DevOps); this repo's `docs/zh/applications/` is now built out accordingly.

## Sources

1. https://book.douban.com/tag/Go (pages 1-4, fetched 2026-10-08, providing authors, publishers, years and ratings for *Go: Advanced Programming (2nd edition)*, *Go: Design and Implementation*, *Go Expert Programming*, *The Path to Go Mastery*, *Understanding Go Concurrency in Depth*, *The Way of Go Concurrency*, *Build Your Own Docker* and others)
2. https://book.douban.com/tag/Go?start=25&type=T
3. https://book.douban.com/tag/Go?start=50&type=T
4. https://book.douban.com/tag/Go?start=75&type=T
5. Douban entries aggregated by Sogou search (*The Go Programming Language* rating 8.6, *Go Programming Design* 7.1, *Go Programming* 7.1)
6. Dangdang entries aggregated by Sogou search (*The Go Programming Language* author Alan A. A. Donovan, China Machine Press)
7. Douban entries aggregated by 360 Search (*Go Advanced Programming* rating 7.6, *The Go Programming Language* 8.6)
8. CSDN entries aggregated by 360 Search (*Concurrency in Go* O'Reilly August 2017, 229 pages)

<!-- BACKLINKS-AUTO -->
## Related pages

- [knowledge](/knowledge.md)
- [README](/research/README.md)