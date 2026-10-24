# Go's four application scenarios

The official page groups Go's uses into four categories; this page gives the criteria for those four and their counterparts in this repo. The four-way split comes from the official Go use-case index page, not from this repo's own invention.

## 1. The four scenarios and their criteria

| Scenario | Official rationale | Repo location |
| --- | --- | --- |
| Cloud and network services | Fast builds, built-in concurrency, low memory footprint; the dominant language in the container and orchestration ecosystem | `docs/zh/concurrency/`, `docs/zh/net/`, `docs/zh/middleware/` |
| Command-line interfaces | Compiles to a single self-contained binary, cross-architecture builds in seconds, startup close to C/C++ | `docs/zh/cmd/` |
| Web development | The standard library ships with an HTTP server and templates, supporting HTTP/2 and TLS 1.3 | `docs/zh/gin/`, `docs/zh/net/` |
| DevOps and SRE | Fast builds, lean syntax, built-in formatting and a documentation generator | `docs/zh/debug/`, `docs/zh/test/`, `docs/zh/cmd/` |

Beyond the four categories there is one implicit thread: Go projects usually start from "one runnable single binary" and get split into services once they grow, which is why concurrency and networking are the two biggest areas by page count in this repo (`docs/zh/concurrency/` 13 pages, `docs/zh/sync/` 14 pages, `docs/zh/net/` 7 pages).

## 2. Companies and projects the official pages name

| Company / project | What they use Go for | Source |
| --- | --- | --- |
| Google Cloud | Kubernetes, gVisor, Knative, Istio and Anthos are all Go | Cloud scenario page |
| Docker | Container engine and CI/CD automation | Cloud scenario page, DevOps scenario page |
| Kubernetes | A container orchestration system written in Go | Cloud scenario page |
| etcd | A strongly consistent distributed key-value store | DevOps scenario page |
| Cloudflare | Compression, DNS infrastructure, SSL, load testing | Web scenario page |
| MercadoLibre | Core user API at 8-10 million requests per minute, responses under 10 milliseconds | Official case page |
| PayPal | Rewrote a C++ NoSQL database in Go, 30% of clusters migrated | Official case page |
| American Express | Microservices on the payments and rewards networks | Official case page |
| Uber | AresDB real-time analytics, Geofence geofencing, Peloton resource scheduling | Cloud scenario page |
| Hugo | Single-binary static site generator | CLI scenario page |

## 3. Three questions to ask when picking Go

1. **Do you need single-binary distribution**: if yes, Go plus the `docs/zh/cmd/` set; the CLI scenario page gives the Cobra/Viper division of labor.
2. **Is the concurrency IO-bound or CPU-bound**: for IO-bound, goroutines plus channels, see `docs/zh/concurrency/`; for CPU-bound, look first at `docs/zh/debug/PGO.md` and `docs/zh/gc/GC.md`.
3. **Do you need to integrate with the container ecosystem**: if yes, read `docs/zh/applications/CloudNative.md`, which records the official wording on Docker and Kubernetes verbatim.

## Sources

1. https://golang.google.cn/solutions/use-cases -- the four-scenario index (fetched 2026-10-08)
2. https://golang.google.cn/solutions/cloud/ -- cloud and network services
3. https://golang.google.cn/solutions/clis/ -- command-line interfaces
4. https://golang.google.cn/solutions/webdev/ -- web development
5. https://golang.google.cn/solutions/devops/ -- DevOps/SRE
6. https://golang.google.cn/solutions/mercadolibre -- MercadoLibre case study
7. https://golang.google.cn/solutions/paypal -- PayPal case study

## References

- [Go Official Documentation · Writing Web Applications (external link)](https://go.dev/doc/articles/wiki/)
- [net/http standard library](https://pkg.go.dev/net/http)

<!-- BACKLINKS-AUTO -->
## Related pages

- [knowledge](/knowledge.md)