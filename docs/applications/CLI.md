# Command-line tools: single binary plus Cobra and Viper

CLI is one of the official four scenarios. The official CLI page's rationale comes down to three points: fast builds, a single self-contained binary, and startup time close to C/C++. Fetched 2026-10-08.

## 1. Why Go

- From a single Windows or Mac laptop you can build programs for the dozens of architectures and operating systems Go supports in seconds, with no dedicated build farm needed. The official wording: no other compiled language builds this portably and this fast.
- The artifact is a single self-contained binary; installing the program means copying one file, with no dependency on existing libraries, runtimes or dependencies.
- Startup happens immediately, at a scale close to C/C++.

Cloud and infrastructure applications are naturally CLI-first, because scripting and remote operation are both convenient -- that is why the official pages single CLI out as its own category.

## 2. The division between Cobra and Viper

| Tool | Responsibility | Users named by the official page |
| --- | --- | --- |
| Cobra | Commands, subcommands, argument parsing, help and auto-completion; both a library and a code generator | CoreOS, Delve, Docker, Dropbox, Git LFS, Hugo, Kubernetes |
| Viper | Configuration: nested structures, files, environment variables; used with Cobra to form a complete solution | The scenario the official page gives is that sensitive data goes through environment variables, not into command-line history |

The official positioning of Cobra quotes Francesc Campoy of DGraph Labs: it is more of a framework than a library -- invoking the generated binary gives you a skeleton, and the rest is filling in code. Hugo author Bjørn Erik Pedersen's reason is that single-binary makes installation extremely simple.

This repo's `docs/zh/cmd/` covers the design and parsing of the standard-library `flag` package, enough for small-to-medium tools; move to Cobra once the command tree gets large, and `docs/zh/gin/Config.md` introduces Viper.

## 3. Official case studies

- **Comcast**: a Go CLI client for high-frequency site pub/sub, plus an open-sourced Go Apache Pulsar client library.
- **GitHub**: a CLI tool in Go that wraps git, used to extend extra functionality and commands.
- **Hugo**: a Go static site generator, listed by the official page as one of the most popular Go CLI applications, with single-binary installation the main reason.

## 4. Order of operations

1. Get commands and arguments working with the standard library first: `docs/zh/cmd/Flag.md`, `docs/zh/cmd/Parse.md`.
2. Need subcommands and generated help: move to Cobra, referring to the command design conventions in `docs/zh/cmd/Design.md`.
3. Multiple configuration sources (file, environment variable and command-line conflict): consolidate with Viper, see `docs/zh/gin/Config.md`.
4. Cross-compilation and release: `GOOS`/`GOARCH` combinations and build constraints are in `docs/zh/start/BuildConstraint.md`.

## Sources

1. https://golang.google.cn/solutions/clis/ -- Go for CLIs (single binary, cross-architecture builds in seconds, Cobra and Viper, Comcast/GitHub/Hugo case studies, fetched 2026-10-08)
2. https://golang.google.cn/solutions/use-cases -- the four-scenario index

## References

- [Go Official Documentation · Writing Web Applications (external link)](https://go.dev/doc/articles/wiki/)
- [net/http standard library](https://pkg.go.dev/net/http)

<!-- BACKLINKS-AUTO -->
## Related pages

- [knowledge](/knowledge.md)