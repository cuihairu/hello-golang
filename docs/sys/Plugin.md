### plugin plugins

The `plugin` package lets a program load a compiled shared library (`.so`) at runtime, look up symbols by name, assert them to a function or variable, and call them. It is the standard form of a "plugin system" in Go, and dynamic patching (hot-reload logic) goes down this path.

### Basic usage

On the plugin side it is an ordinary package that exports functions or variables:

```go
package main

// Greet returns a greeting, exported for plugin consumers
func Greet(name string) string {
	return "Hello, " + name
}
```

Build it into a shared library with `-buildmode=plugin`:

```sh
go build -buildmode=plugin -o greet.so greet.go
```

On the host side, use `plugin.Open` to load and `Lookup` to look up symbols by name:

```go
package main

import (
	"fmt"
	"plugin"
)

func main() {
	p, err := plugin.Open("greet.so")
	if err != nil {
		panic(err)
	}
	sym, err := p.Lookup("Greet")
	if err != nil {
		panic(err)
	}
	greet := sym.(func(string) string)
	fmt.Println(greet("Go")) // prints: Hello, Go
}
```

### Limitations

- Platform-limited: `-buildmode=plugin` is only available on Linux, macOS, and FreeBSD; Windows is not supported.
- Load only: once a plugin is `Open`ed it cannot be unloaded; no unload function exists.
- Same path loads once: repeatedly `Open`ing the same path returns the same plugin instance.
- Version-sensitive: the plugin and host must be compiled with the same toolchain and dependencies; a mismatch produces an error like `plugin was built with a different version` at `Open` time.
- Types are an assertion away: `Lookup` returns a `Symbol` (`any`); you assert the signature yourself, and a wrong one panics at runtime.

### The reality of dynamic patching

Doing hot reloads with plugin means the flow "edit code -> rebuild the `.so` -> `Open` a different path". Because you cannot unload, the old version's code and data stay in memory indefinitely, so a long-running hot-reload process has to manage things as "one filename per version" to avoid loading the same file twice. In most scenarios a steadier path is to put the changing part in a subprocess or drive it with data (configuration, rule engines), and leave plugin for genuine native extension points.

Cross-reading: for the security boundary of loading external code, see [the official security stance](/security/Security.md).

## References

- [syscall standard library](https://pkg.go.dev/syscall)
- [os standard library](https://pkg.go.dev/os)
- [plugin standard library](https://pkg.go.dev/plugin)

## Sibling pages

- [Sys](/sys/Sys.md)
- [Syscall](/sys/Syscall.md)
- [Unsafe](/sys/Unsafe.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Sys](/sys/Sys.md)
- [Syscall](/sys/Syscall.md)
- [Unsafe](/sys/Unsafe.md)
