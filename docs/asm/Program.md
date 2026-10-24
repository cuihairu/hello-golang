### Writing Plan 9 Programs

For the instruction set reference see [Plan 9 Assembly Instructions](/asm/Assembly.md); this page is about writing assembly that the Go toolchain can link: pseudoregisters, function declarations, and one complete runnable example.

### Pseudoregisters

These four in Plan 9 assembly are not real registers — they are linker notations:

| Notation | Meaning |
| --- | --- |
| `SB` | Static base, the anchor for all global symbols; written as `symbol(SB)` |
| `FP` | Frame pointer, used to access the arguments and return values passed in by the caller; written as `a+0(FP)` |
| `SP` | Pseudo stack pointer, pointing at the current frame's local variable area (not the same thing as the hardware SP) |
| `PC` | Program counter, used for jump addressing |

The `·` (middle dot) inside a symbol name separates the package name from the function name: `·Add(SB)` becomes `main.Add` after linking.

### Function Declarations

Every assembly function is declared with `TEXT`, and the frame size is written as `$frame bytes - argument plus return value bytes`:

```assembly
#include "textflag.h"

// func Add(a, b int64) int64
TEXT ·Add(SB), NOSPLIT, $0-24
    MOVQ a+0(FP), AX
    ADDQ b+8(FP), AX
    MOVQ AX, ret+16(FP)
    RET
```

`$0-24` means this function claims no local stack space, and arguments plus return value total 24 bytes (two int64 arguments plus one int64 return value). `NOSPLIT` means no stack growth check is inserted — only appropriate for small functions where you are sure you will not exceed the stack, and it requires `#include "textflag.h"` to supply that macro.

On the Go side you only declare the function signature (no body), and the linker finds the assembly implementation:

```go
package main

import "fmt"

// Add is implemented in Plan 9 assembly in add.s
func Add(a, b int64) int64

func main() {
	fmt.Println(Add(2, 3)) // prints: 5
}
```

Put the `.s` file in the same package directory as the `.go` file, and `go build` compiles them together automatically.

### Generating Assembly from Go

Before you write assembly by hand, look at what the compiler generates. `go build -gcflags=-S` prints the assembly for every function (the call site for the example above):

```assembly
0x0020 00032 (main.go:9)	CALL	main.Add(SB)
0x0025 00037 (main.go:9)	XORPS	X15, X15
0x0029 00041 (main.go:9)	MOVQ	(TLS), R14
```

The flow for writing a performance-sensitive function: first write a correct version in Go, use `-gcflags=-S` to look at what the compiler produces, and only decide whether to hand-write a replacement once you have confirmed the hot spot. `go tool objdump binary` disassembles an already-compiled artifact; compare the two side by side.

### Summary

The pseudoregisters (`SB`/`FP`/`SP`/`PC`) are the linker's language, and the frame size in a `TEXT` declaration reveals the argument layout; declare the signature on the Go side and supply the implementation in assembly, and the same directory gets linked. Before you start writing, look at the assembly the compiler generates — for most hot spots it has already arranged things quite well.

## References

- [Official · A Quick Guide to Go's Assembler](https://go.dev/doc/asm)

## Sibling pages

- [Assembly](/asm/Assembly.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Assembly](/asm/Assembly.md)
