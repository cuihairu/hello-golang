# PGO: feeding a production CPU profile back to the compiler

PGO (Profile-guided optimization) is also called FDO (feedback-directed optimization): you hand the compiler a representative runtime profile so the next build can optimize more accurately, for example by inlining functions the profile shows as frequently called more aggressively. The official page `/doc/pgo` was fetched 2026-10-08.

## 1. The official numbers on the gains

In the official words: benchmarked against Go 1.22 on a representative set of Go programs, **a PGO build improves performance by roughly 2%-14%**, and the official expectation is that the gains will keep growing as the version matures. This is the benchmark conclusion in the documentation, not a number measured in this repo.

## 2. What the input is

The input the Go compiler wants is a CPU pprof profile. Runtime output from `runtime/pprof` or `net/http/pprof` can be used directly; output from other profiling systems has to be converted first. The profile must represent production behavior, and the official docs say so explicitly: building with an unrepresentative profile may yield no benefit in production at all, so **collecting directly from production is recommended**.

The recommended iteration cadence:

1. Ship a binary without PGO first.
2. Collect a profile from production.
3. On the next release, build with the latest source plus the production profile.

PGO is robust to a mismatch between the profile version and the build version, and it also allows using a profile collected from an already-optimized binary, so the loop above can keep turning.

## 3. How to enable it

| Method | Usage |
| --- | --- |
| On by default | Name the pprof CPU profile `default.pgo` and place it in the main package directory of the profiled program; `go build` detects it and enables PGO automatically |
| Explicit | `go build -pgo=/tmp/foo.pprof` |
| Off | `go build -pgo=off` |
| Default value | `-pgo` defaults to `-pgo=auto`, i.e. the `default.pgo` behavior above |

The official advice is to commit the profile directly into the source repository: the profile is build input, so keeping it with the source makes a reproducible build also reproducible in performance, and anyone who pulls the source does not have to add a step.

For tools such as command-line utilities that ship to end users and cannot collect a production profile, collect one from a representative benchmark instead. The official docs also give a warning: **microbenchmarks are usually a poor source for PGO**, because they only cover a small part of the program, so applying them to the whole program yields little benefit.

## 4. Where this sits in this repo

| Related topic | Page |
| --- | --- |
| How pprof collects data | `docs/zh/debug/Pprof.md` |
| Benchmarks | `docs/zh/test/Benchmark.md` |
| GC and memory behavior | `docs/zh/gc/GC.md`, `docs/zh/alloc/GC.md` |
| Mounting `net/http/pprof` on a service | The example code in `docs/zh/debug/Pprof.md` |

You need pprof before you have PGO, so `docs/zh/debug/Pprof.md` in this repo is the prerequisite for this page.

## Sources

1. https://golang.google.cn/doc/pgo — Profile-guided optimization: the 2%-14% gains, where profiles come from, the three values of `default.pgo` and `-pgo`, the production collection flow, and the microbenchmark counterexample (fetched 2026-10-08)
2. https://golang.google.cn/doc/ — The PGO entry under the References section

## References

- [Official · Diagnostics](https://go.dev/doc/diagnostics)
- [runtime/pprof standard library](https://pkg.go.dev/runtime/pprof)
- [Official · Profile-guided optimization](https://go.dev/doc/pgo)
- [Official blog · PGO in Go 1.21](https://go.dev/blog/pgo)

## Sibling pages

- [Utils](/debug/Utils.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Debug](/debug/Debug.md)
- [Delve](/debug/Delve.md)
- [Expvar](/debug/Expvar.md)
- [GDB](/debug/GDB.md)
- [Utils](/debug/Utils.md)
- [glossary](/glossary.md)
- [knowledge](/knowledge.md)
