# Cloud and network services: over 75% of CNCF projects are Go

This page records the position of the official cloud scenario page, dated 2019-10-04, fetched 2026-10-08. When citing that 75% number, carry the page date with it -- it is the official page's own wording, not this repo's estimate.

## 1. The three reasons the official page gives

1. **You do not have to choose between development cycle and server performance**: builds are fast, iteration is fast, memory and CPU footprint are low, servers are ready to use on boot. The official page specifically calls out the two pay-as-you-go and serverless billing deployment forms.
2. **Standard idiomatic APIs aimed at the modern cloud**: the standard library has HTTP server and client, JSON/XML parsing, SQL databases, encryption and decryption; the runtime ships with race detection, benchmarking and profiling, code generation, and static analysis.
3. **Low latency with no tuning knobs**: the official wording is low-latency and "no knob" tuning.

## 2. Ecosystem list

| Use | Options the official page lists |
| --- | --- |
| Cloud vendor SDKs | GCP, AWS and Azure all have Go APIs |
| API tooling | Swagger |
| Transport | protocol buffers, gRPC |
| Monitoring | OpenCensus |
| ORM | gORM |
| Authentication | JWT |
| Service frameworks | Go Kit, Go Micro, Gizmo |
| Web frameworks | Echo, Flamingo, Gin, Gorilla |
| Routing | net/http, httprouter, gorilla/mux, chi |
| Databases | database/sql, mongo-driver, go-elasticsearch, GORM, Bleve, CockroachDB |

## 3. The two container tools

The official page's descriptions of these two projects are worth reading directly:

- **Docker**: packages software, libraries and configuration files into containers, hosted by Docker Engine, running on a single operating-system kernel, and therefore using fewer system resources than virtual machines. Go developers in the cloud use Docker to manage code and multi-platform builds.
- **Kubernetes**: a container orchestration system written in Go, used to automate web application deployment. Cloud developers rely on it to manage containers through APIs and rein in the complexity that comes with scale.

The corresponding hands-on content in this repo is in `docs/zh/start/Structure.md` (organizing build artifacts) and `docs/zh/net/` (inter-service communication); Kubernetes itself is outside this repo's scope.

## 4. The company-side numbers

- The official cloud scenario page's own wording: **over 75% of CNCF projects are written in Go**.
- Google Cloud's Kubernetes, gVisor, Knative, Istio and Anthos are all written in Go.
- Dropbox decided in 2013 to migrate performance-critical backends from Python to Go; most of the company's infrastructure is Go today.
- Capital One used Go for the Credit Offers API, and the engineering team chose Go for the serverless architecture as well.
- Twitch's live streaming and chat systems use Go; the link title the official page hangs under this point is Go's march to low-latency GC.
- Uber's real-time analytics engine AresDB, its geofencing service Geofence and its resource scheduler Peloton are all Go.

## 5. How this connects to this repo

When writing cloud services, these pages in this repo are the direct prerequisite knowledge:

| Need | Which page to read |
| --- | --- |
| Starting goroutines and channels | `docs/zh/concurrency/` |
| Long-lived inter-service connections and multiplexing | `docs/zh/net/Socket.md`, `docs/zh/net/Netpoll.md` |
| Middleware and message queues | `docs/zh/middleware/` |
| How to set the memory ceiling | `docs/zh/alloc/GC.md` (`GOMEMLIMIT`) |
| Optimizing from production data | `docs/zh/debug/PGO.md` |

## Sources

1. https://golang.google.cn/solutions/cloud/ -- Go for Cloud & Network Services, page date 2019-10-04, including the 75% share, Docker, Kubernetes and the company list (fetched 2026-10-08)
2. https://golang.google.cn/solutions/use-cases -- the four-scenario index
3. https://golang.google.cn/solutions/paypal -- PayPal migration and the 30% cluster number
4. https://golang.google.cn/solutions/mercadolibre -- MercadoLibre request volume and response time

## References

- [Go Official Documentation · Writing Web Applications (external link)](https://go.dev/doc/articles/wiki/)
- [net/http standard library](https://pkg.go.dev/net/http)

<!-- BACKLINKS-AUTO -->
## Related pages

- [knowledge](/knowledge.md)