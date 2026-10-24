# Build constraints: `//go:build` and file-name rules

A build constraint (also called a build tag) decides whether a source file goes into a given build. This repo had no page covering it before; you can't get around it when cross-compiling or splitting files by platform. The content comes from the official `go/build` package docs and the Build constraints section of the `go` command, fetched 2026-10-08.

## 1. Where and how to write them

- A constraint is written as a single line comment starting with `//go:build`.
- It must appear near the top of the file: only blank lines and other comments may come before it, which in a Go file means it must be written before the `package` clause. To tell it apart from package documentation, a constraint must be followed by a blank line.
- More than one `//go:build` line in a single file is a compile error.
- Constraints also serve to lower the language version used to compile the file.

The expression is made up of tags and `||`, `&&`, `!`, and parentheses, with the operators meaning the same as in Go:

```go
//go:build (linux && 386) || (darwin && !cgo)
```

This line means: compile when the target is linux/386, or when the target is darwin and cgo is not available.

## 2. Which tags hold in this build

| Tag category | When it holds |
| --- | --- |
| Target OS | equals `runtime.GOOS`, set by the `GOOS` env var |
| Target architecture | equals `runtime.GOARCH`, set by the `GOARCH` env var |
| Architecture features | of the form `amd64.v2`, decided by vars like `GOAMD64`, `GOARM`, `GOARM64`, `GOMIPS`, `GOPPC64`, `GORISCV64`, `GOWASM` |
| `unix` | `GOOS` is a Unix or Unix-like system |
| Compiler | `gc` or `gccgo` |
| `cgo` | cgo is supported (see `CGO_ENABLED`) |
| Go version | one tag per major version from 1.1 on: `go1.1`, `go1.12`, ..., up to the current version |
| Custom | extra tags passed via `-tags` (see `go help build`) |

There are no beta or minor-version tags for major versions. Feature tags are cumulative: `GOAMD64=v2` satisfies both `amd64.v1` and `amd64.v2`, so to test for "this feature is absent" you write the negated condition:

```go
//go:build !amd64.v2
```

A few aliases are worth knowing: `GOOS=android` satisfies android in addition to the linux tag; `GOOS=illumos` satisfies illumos in addition to solaris; `GOOS=ios` satisfies ios in addition to darwin.

## 3. Constraints carried by the file name

Strip off the extension and any `_test` suffix; if the file name matches any of the patterns below, that acts as one more implicit constraint:

- `*_GOOS`, e.g. `dns_windows.go`
- `*_GOARCH`, e.g. `math_386.s`
- `*_GOOS_GOARCH`, e.g. `source_windows_amd64.go`

An implicit constraint and an explicit one written in the file are cumulative — both must hold for the file to be compiled in. A file named `dns_windows.go` only takes part when building the package for Windows.

## 4. A few conventions

- To keep a file out of every build: `//go:build ignore` (any other false word works too; `ignore` is the conventional spelling).
- Compile only when cgo is present and the OS is Linux or macOS: `//go:build cgo && (linux || darwin)`; write the negated condition in the paired file, so the two together cover every case.
- A package with an assembly implementation usually also ships a pure Go version, with the conventional tag `purego`.
- Go 1.16 and earlier used a different syntax with the `// +build` prefix; when `gofmt` meets the old form it adds an equivalent `//go:build` line.
- When the module's Go version is 1.21 or later, if a file's constraint contains a major-version tag, the language version used to compile that file is the minimum version that tag implies.

## 5. How this repo uses them

| Scenario | Approach |
| --- | --- |
| One codebase shipping Linux and Windows binaries | `GOOS=windows GOARCH=amd64 go build`, naming platform-specific files as `*_GOOS.go` |
| Splitting syscalls by platform | `syscall_unix.go` / `syscall_windows.go`, paired with the `x/sys/unix` example in `docs/zh/net/Advanced.md` |
| Two paths, assembly and non-assembly | switch with the `purego` tag, see `docs/zh/asm/Assembly.md` |
| A purely static build with cgo off | `CGO_ENABLED=0`, so the corresponding `cgo` tag does not hold |

## Sources

1. https://golang.google.cn/pkg/go/build/ — "Build constraints are given by a line comment that begins //go:build" plus the file-name constraint notes
2. https://golang.google.cn/pkg/cmd/go/ — Build constraints section: tag list, expression syntax, `ignore`, `purego`, the old `// +build` syntax, and the 1.21 language-version rule
3. https://golang.google.cn/doc/ — entry into the Commands section of the docs overview

All fetched 2026-10-08.

## References

- [Go Official Documentation · Getting started (external link)](https://go.dev/doc/tutorial/getting-started)
- [Go Official Documentation · Create a module (external link)](https://go.dev/doc/tutorial/create-module)
- [go/build · Build constraints](https://pkg.go.dev/go/build)
- [go/build/constraint](https://pkg.go.dev/go/build/constraint)

<!-- BACKLINKS-AUTO -->
## Related pages

- [knowledge](/zh/knowledge.md)
- [Build](/start/Build.md)
- [Embed](/start/Embed.md)
- [Hello](/start/Hello.md)
- [Run](/start/Run.md)
- [Starter](/start/Starter.md)
- [Structure](/start/Structure.md)
