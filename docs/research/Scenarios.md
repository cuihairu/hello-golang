# Application scenario survey

The official page groups Go's uses into four categories; the index page is `/solutions/use-cases`: **cloud and network services, command-line interfaces (CLI), web development, DevOps and SRE**. This repo previously had no page at all covering these four scenarios -- only scattered technical content (`docs/zh/gin/` for web frameworks, `docs/zh/cmd/` for flag, `docs/zh/middleware/` for message queues). This page records the official position and numbers for the four scenarios; the gaps have been filled as five pages under `docs/zh/applications/`.

Fetched 2026-10-08, all from the `golang.google.cn` mirror.

## 1. Cloud and network services

The official page is titled Go for Cloud & Network Services, with a page date of 2019-10-04. Key points:

- The official wording: **over 75 percent of projects in the Cloud Native Computing Foundation are written in Go**. This is the hardest cloud-native share number this repo can cite; cite it together with the page date.
- Fast startup and low memory footprint; the official page ties this to the cost of pay-as-you-go and serverless deployments.
- Ecosystem list: all three major cloud vendors (GCP, AWS, Azure) have Go APIs; API tooling uses Swagger, the transport layer uses protocol buffers and gRPC, monitoring uses OpenCensus, the ORM is gORM, authentication uses JWT; service frameworks include Go Kit, Go Micro, Gizmo.
- The toolchain ships with race detection, benchmarking and profiling, code generation, and static analysis.
- The two container projects the official page names: **Docker** (packages software, libraries and configuration into containers, run by Docker Engine, sharing a single operating-system kernel, which saves resources compared with virtual machines) and **Kubernetes** (a container orchestration system written in Go).
- Users listed on the page: Google Cloud (Kubernetes, gVisor, Knative, Istio, Anthos are all Go), Capital One (the Credit Offers API; the quote is "never planned to go serverless without Go"), Dropbox (migrated performance-critical backends from Python to Go starting in 2013, and most of the infrastructure is Go today), The New York Times (backend services and the open-source toolchain Gizmo), Twitch (live streaming and chat systems, citing the low-latency GC), Uber (the real-time analytics engine AresDB, the geofencing service Geofence, the resource scheduler Peloton).

## 2. Command-line interfaces

The official page is titled Go for CLIs. Key points:

- Compiles to a **single self-contained binary**, depending on no existing libraries, runtime or dependencies; startup time is close to C/C++.
- From a single Windows or Mac laptop you can build programs for the dozens of architectures and operating systems Go supports in a few seconds; the official wording is "no other compiled language builds this portably and this fast".
- Framework layer: **Cobra** is both a library and a code generator, and the official page lists its users as CoreOS, Delve, Docker, Git LFS, Hugo, Kubernetes; **Viper** handles configuration, supporting nested structures and environment variables, and the two are used together.
- Case studies: Comcast wrote a CLI client for high-frequency site pub/sub in Go and open-sourced a Go Apache Pulsar client library; GitHub wrote a CLI tool in Go that wraps git; Hugo is a static site generator written in Go, and single-binary installation is one of the reasons it is popular.

## 3. Web development

The official page is titled Go for Web Development. Key points:

- The standard library ships with an HTTP server and a template library, supporting HTTP/2, MySQL/MongoDB/Elasticsearch, and TLS 1.3.
- The cross-platform deployment speed that comes from a single binary with zero dependencies; third-party frameworks are not required in most scenarios.
- Five reasons from a company's (Hexact) CTO include concrete numbers: goroutines handling internal requests are **10 times cheaper** in resources than Python threads; after rewriting in Go, **code volume dropped 64 percent**.
- Projects: Caddy 2 (a web server with automatic HTTPS, its TLS stack from the Go standard library), Cloudflare (compression, DNS infrastructure, SSL, load testing), the UK government's gov.uk HTTP infrastructure, Hugo, Mattermost, Medium (social graph, image service), The Economist.

## 4. DevOps and SRE

The official page is titled Go for DevOps & Site Reliability Engineering. Key points:

- SRE originated at Google, aimed at making large-scale sites more reliable, more efficient and more scalable; Amazon and Netflix later adopted the same practice.
- The standard library covers HTTP, file I/O, time, regex, exec, JSON/CSV, so small scripts go straight into business logic; static typing plus explicit error handling makes scripts more durable.
- godoc generates documentation automatically, lowering maintenance cost.
- Projects: **Docker** (automation and deployment underpinning CI/CD), **Drone** (a continuous delivery system running on containers), **etcd** (a strongly consistent distributed key-value store), IBM (uses Go through Docker and Kubernetes), Netflix (the Rend caching service manages globally replicated personalized data), Microsoft (the Azure Red Hat OpenShift service).

## 5. Numbers from three official case studies

| Company | Page date | Key fact |
| --- | --- | --- |
| American Express | 2019-12-19 | Payments and rewards networks both in Go; the engineering director's point is the low cognitive load, fast ramp-up on new codebases, and most Go code looking much the same |
| PayPal | 2020-06-01 | Rewrote a C++ NoSQL database in Go; the team spent six months learning Go and rewriting, and **30 percent of clusters have moved to the new database**; the reason given is that goroutines and channels rein in multithreading complexity |
| MercadoLibre | -- | The largest e-commerce ecosystem in Latin America, spanning 18 countries; migrated from Groovy/Grails to Go starting in 2015; the core user API averages **8 to 10 million requests per minute**, with response times **under 10 milliseconds** |

## 6. What the four scenarios mean for this repo

1. Cloud and network services map to `docs/zh/concurrency/`, `docs/zh/net/`, `docs/zh/middleware/`; one page was missing to connect the background -- Docker, Kubernetes, the CNCF share -- and that has been filled as `docs/zh/applications/CloudNative.md`.
2. CLI maps to `docs/zh/cmd/` (flag and command-line design); what was missing was a scenario account of the Cobra/Viper split and single-binary traits, now filled as `docs/zh/applications/CLI.md`.
3. Web maps to `docs/zh/gin/`, `docs/zh/net/`; filled as `docs/zh/applications/Web.md`.
4. DevOps/SRE had no corresponding directory; filled as `docs/zh/applications/DevOps.md`.

## Sources

1. https://golang.google.cn/solutions/use-cases -- the four-scenario index
2. https://golang.google.cn/solutions/cloud/ -- cloud and network services (incl. CNCF 75%, Docker, Kubernetes, Dropbox, Uber)
3. https://golang.google.cn/solutions/clis/ -- CLI scenario (single binary, Cobra, Viper, Hugo, GitHub CLI)
4. https://golang.google.cn/solutions/webdev/ -- web development (HTTP/2, TLS 1.3, the 10x and 64% numbers)
5. https://golang.google.cn/solutions/devops/ -- DevOps/SRE (Docker, Drone, etcd, Netflix Rend)
6. https://golang.google.cn/solutions/americanexpress -- American Express case study
7. https://golang.google.cn/solutions/paypal -- PayPal case study (six months, 30% of clusters)
8. https://golang.google.cn/solutions/mercadolibre -- MercadoLibre case study (18 countries, 8-10 million requests per minute, 10 milliseconds)
9. https://golang.google.cn/security/ -- official security page (vulnerability database, fuzzing, crypto libraries, FIPS 140-3)

<!-- BACKLINKS-AUTO -->
## Related pages

- [knowledge](/knowledge.md)
- [README](/research/README.md)