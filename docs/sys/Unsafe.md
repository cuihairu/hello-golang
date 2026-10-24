### unsafe unsafe operations

The `unsafe` package provides four capabilities that live outside compile-time safety checks: `Pointer` (a generic pointer), `Sizeof`/`Offsetof`/`Alignof` (type layout queries), `Add` (pointer stepping), and `Slice` (building a slice from a pointer and a length). It is used for interoperability with C, serialization, and performance-sensitive layout -- use it wrong and you get dangling pointers and data corruption.

### Pointer rules

`unsafe.Pointer` and `*T` can be converted freely. The official rules number six; the three you will use most:

- A pointer of any type can be converted to `unsafe.Pointer`, and converted back.
- `unsafe.Pointer` can be converted to and from `uintptr`, but `uintptr` is an integer -- if the GC moves or collects the object between converting out and converting back, you end up with a wrong address.
- An `unsafe.Pointer` inside an expression cannot be used for arithmetic; convert to `uintptr`, do the math, convert back, and make sure the pointer stays alive throughout.

### Type layout

A struct's memory layout can be determined exactly -- a required skill when working on binary protocols or aligning with C structs:

```go
package main

import (
	"fmt"
	"unsafe"
)

type T struct {
	a bool
	b int64
	c int32
}

func main() {
	var t T
	fmt.Println("size:", unsafe.Sizeof(t), "offset of b:", unsafe.Offsetof(t.b), "align of b:", unsafe.Alignof(t.b))
	// prints: size: 24 offset of b: 8 align of b: 8
	fmt.Println("string size:", unsafe.Sizeof("")) // prints: 16 (pointer + length)
}
```

An `int64` following a `bool` needs 7 bytes of padding for alignment, so `b`'s offset is 8 and the whole struct is 24 bytes. See the `unsafe` package documentation (golang.google.cn/pkg/unsafe) for the layout rules in detail.

### Interoperability with C

At the CGO boundary everything is bridged by `unsafe.Pointer`: a Go-side pointer is converted to `unsafe.Pointer` when passed to C, and C memory is mapped back to Go types the same way. See the pointer rules section of [How CGO works and its performance](/cgo/Internals.md) for the relevant constraints.

### In short

The four `unsafe` tools each have a job: pointers cross the type system boundary, layout queries serve binary interop, and arithmetic plus slicing serve zero-copy handling. Shared precondition: keep the pointer alive and the length in bounds.

## References

- [syscall standard library](https://pkg.go.dev/syscall)
- [os standard library](https://pkg.go.dev/os)
- [unsafe standard library](https://pkg.go.dev/unsafe)

## Sibling pages

- [Plugin](/sys/Plugin.md)
- [Sys](/sys/Sys.md)
- [Syscall](/sys/Syscall.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Plugin](/sys/Plugin.md)
- [Sys](/sys/Sys.md)
- [Syscall](/sys/Syscall.md)
