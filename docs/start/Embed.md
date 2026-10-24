### Embedding with the embed package

`embed` (Go 1.16+) bakes static assets into the binary: templates, config, frontend build output all ship with the program, so deployment no longer drags along a pile of loose files. The idiom is a package-level variable with a `//go:embed` comment; the variable's type decides the embedded form — `string`/`[]byte` for a single file, `embed.FS` for a file tree.

### Basic usage

```go
package main

import (
	"embed"
	"fmt"
)

//go:embed hello.txt
var hello string

//go:embed hello.txt
var helloBytes []byte

//go:embed static
var static embed.FS

func main() {
	fmt.Print(hello)                    // prints: hello embed
	fmt.Println("bytes:", len(helloBytes)) // prints: bytes: 12
	data, err := static.ReadFile("static/config.json")
	fmt.Println(string(data), err)      // prints: {"mode":"test"} <nil>
}
```

The same file can be embedded into several variables; paths inside an `embed.FS` are counted from where the embed sits in the module, so they carry the directory prefix. `ReadDir` lists a directory, and `fs.WalkDir` traverses one.

### Serving static files

`embed.FS` implements the `fs.FS` interface, so wrapping it in `http.FS` mounts it straight onto a file server (snippet, where `static` is the variable defined above):

```go
mux := http.NewServeMux()
mux.Handle("/", http.FileServer(http.FS(static)))
http.ListenAndServe(":8080", mux)
```

### Limits and caveats

- A pattern can only match the package's own directory and its subdirectories; writing `..` is a compile error: `pattern ../outside.txt: invalid pattern syntax`.
- Paths inside a pattern use forward slashes, on Windows too.
- The variable must be declared at package level; a local variable inside a function won't do. An unused embedded variable needs to be received with `_`.
- `go:generate` and build constraints both work alongside embedding: put a build constraint on platform-specific assets, see [Build constraints](/start/BuildConstraint.md).

### Summary

The rule of thumb for embedding: a comment declares the pattern, the variable decides the type, and `embed.FS` takes the file tree. Once assets are inside the binary, the release artifact is a single executable — the tradeoff being that changing an asset requires recompiling.

## References

- [Go Official Documentation · Getting started (external link)](https://go.dev/doc/tutorial/getting-started)
- [Go Official Documentation · Create a module (external link)](https://go.dev/doc/tutorial/create-module)
- [embed standard library](https://pkg.go.dev/embed)

## Sibling pages

- [BuildConstraint](/start/BuildConstraint.md)
- [Build](/start/Build.md)
- [Hello](/start/Hello.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Build](/start/Build.md)
- [Hello](/start/Hello.md)
- [Run](/start/Run.md)
- [Starter](/start/Starter.md)
- [Structure](/start/Structure.md)
