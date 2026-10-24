# DevOps and SRE: scripts, CLIs and long-running services all use it

DevOps and SRE is one of the official four scenarios. This page is an excerpt from the official DevOps scenario page plus a guide into this repo, fetched 2026-10-08.

## 1. The official three-part argument

1. **Write small scripts**: the standard library covers HTTP, file I/O, time, regex, exec, JSON/CSV; with static typing and explicit error handling, scripts hold up to more change than dynamic-language scripts of the same length.
2. **Fast CLI release**: builds are fast, so a one-off script that grows into a tool used by dozens of people daily does not need to be rewritten. The official page's progression of forms is "one-off script -> CLI -> release management service".
3. **Big services stay maintainable**: garbage collection removes manual memory management, godoc generates documentation automatically, and the code carries its own explanation.

Operations tooling also has to face growing scale; the official page's supplementary reason is that concurrency and networking fit automating tools for cloud deployments.

## 2. Projects the official page lists

| Project | What it does | Source |
| --- | --- | --- |
| Docker | Container platform, officially described as driving large-scale safe automation and deployment, underpinning CI/CD | DevOps scenario page |
| Drone | A continuous delivery system running on containers, with one YAML file defining the pipeline | DevOps scenario page |
| etcd | A strongly consistent distributed key-value store, providing configuration and service discovery for distributed systems and clusters | DevOps scenario page |
| IBM | Uses Go through Docker, Kubernetes and a set of Go-written CI/CD tools | DevOps scenario page |
| Netflix | The Rend caching service, managing globally replicated personalized data | DevOps scenario page |
| Microsoft | Uses Go in the Azure Red Hat OpenShift service | DevOps scenario page |

The SRE practice originated at Google, aimed at making large-scale sites more reliable, more efficient and more scalable; the official page mentions that Amazon and Netflix later adopted the same practice.

## 3. How this connects to this repo

| Operations task | This repo's page |
| --- | --- |
| Parsing command-line arguments | `docs/zh/cmd/Flag.md`, `docs/zh/cmd/Parse.md` |
| Reading configuration files | `docs/zh/gin/Config.md`, `docs/zh/encoding/Ini.md`, `docs/zh/encoding/TOML.md` |
| Logging and log collection | `docs/zh/log/` 4 pages; the collection page covers fluentd |
| What to look at first when something breaks | `docs/zh/debug/`: Delve, GDB, pprof, expvar |
| Regression testing and coverage | `docs/zh/test/` 9 pages |
| Scheduling and timeout control | `docs/zh/time/TimerAndTicker.md`, `docs/zh/sync/Context.md` |
| Cross-compilation artifacts | `docs/zh/start/BuildConstraint.md` |

## 4. One trade-off

Whether an operations script should be Go depends on whether the script will live past three months. Glue logic that runs once and gets edited once is faster to write in Python; once you need to ship it to others, maintain it long term, or concurrently pull multiple pieces of state, Go's static typing and single binary start paying back. The form progression on the official page (a one-off script becoming the team's daily tool) is describing exactly that tipping point.

## Sources

1. https://golang.google.cn/solutions/devops/ -- Go for DevOps & Site Reliability Engineering (the three-part argument, Docker/Drone/etcd/IBM/Netflix/Microsoft, the SRE origin, fetched 2026-10-08)
2. https://golang.google.cn/solutions/use-cases -- the four-scenario index

## References

- [Go Official Documentation · Writing Web Applications (external link)](https://go.dev/doc/articles/wiki/)
- [net/http standard library](https://pkg.go.dev/net/http)

<!-- BACKLINKS-AUTO -->
## Related pages

- [knowledge](/knowledge.md)