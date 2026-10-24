# Web development: the standard library is enough, frameworks are optional

Web development is one of the official four scenarios. This page is an excerpt from the official web scenario page plus a guide into this repo, fetched 2026-10-08.

## 1. The capability list the official page gives

- The standard library ships with an easy-to-use, safe and high-performance web server and template library.
- Supports HTTP/2, MySQL, MongoDB, Elasticsearch, and newer cryptographic standards such as TLS 1.3.
- A single small binary with zero dependencies means fast cross-platform deployment; the official page puts this point under a "cross-platform deployment" heading.
- Runs natively on Google App Engine and Google Cloud Run, and can also run in any environment, cloud or operating system.

## 2. Two numbers that have a source

Two of the five reasons for switching languages listed by a company's (Hexact) CTO carry numbers:

1. Goroutines handling internal requests are **10x cheaper in resources** than Python Threads.
2. After rewriting all projects to Go, **code volume dropped 64 percent**.

The other three are static linking into a single binary, a static type system suited to large applications, and no need for third-party frameworks in most scenarios. These five come from the official page's quotations of the original wording, not from this repo's tests.

## 3. Projects the official page lists

| Project | Description |
| --- | --- |
| Caddy 2 | An open-source web server with automatic HTTPS, its TLS stack from the Go standard library |
| Cloudflare | Compressing high-latency HTTP connections, the whole DNS infrastructure, SSL, load testing |
| gov.uk | The UK government's HTTP infrastructure; the reason for choosing Go is that the concurrency model makes IO-bound performance easy to get |
| Hugo | Static site generator |
| Mattermost | An open-source team communication platform, Go plus React |
| Medium | Supporting services such as the social graph and image service |
| The Economist | Multi-channel content distribution backed by Go services |

## 4. How this connects to this repo

| Need | This repo's page |
| --- | --- |
| Starting an HTTP service | `docs/zh/net/Intro.md`, `docs/zh/net/Socket.md` |
| Routing and middleware | `docs/zh/gin/Route.md`, `docs/zh/gin/Middleware.md` |
| Request and response handling | `docs/zh/gin/Request.md`, `docs/zh/gin/Response.md` |
| HTML and text templates | `docs/zh/type/HtmlTemplate.md`, `docs/zh/type/Template.md` |
| JSON encoding and decoding | `docs/zh/encoding/JSON.md`, `docs/zh/encoding/JsonV2.md` |
| Concurrent load testing | `docs/zh/test/Benchmark.md`, `docs/zh/sync/` |
| Upstream timeouts and cancellation | `docs/zh/sync/Context.md` |

Where the standard library's `net/http` needs to stop and a framework begin was not covered in this repo's 13 `docs/zh/gin/` pages; the official page's position is that third-party frameworks are not needed in most scenarios, and a framework's value lies in routing, parameter binding and organizing middleware. That judgment can serve as the dividing line.

## Sources

1. https://golang.google.cn/solutions/webdev/ -- Go for Web Development (HTTP/2, TLS 1.3, the 10x and 64% numbers, the project list, fetched 2026-10-08)
2. https://golang.google.cn/solutions/use-cases -- the four-scenario index
3. https://golang.google.cn/doc/ -- the Writing Web Applications page entry under Getting Started

## References

- [Go Official Documentation · Writing Web Applications (external link)](https://go.dev/doc/articles/wiki/)
- [net/http standard library](https://pkg.go.dev/net/http)

<!-- BACKLINKS-AUTO -->
## Related pages

- [knowledge](/knowledge.md)