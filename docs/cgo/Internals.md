### How It Works

CGO's compilation chain has two stages: `go build` first uses the cgo tool to read the C code in the comment above `import "C"` and generates stub files such as `_cgo_gotypes.go` and `_cgo_export.c`; then the C compiler compiles the C part, and finally the Go toolchain links the two sides together. To see the full set of steps use `go build -x` — the cgo invocation shows up in the output.

**Go calling C**: `runtime.cgocall` takes over the call — the current M enters syscall state (the same semantics as being blocked in a syscall), and only after the C code finishes does it return to the Go stack and continue. So a cross-boundary call costs more than an ordinary function call, and the cost is the scheduler stepping in plus the stack switch.

**C calling Go**: mark a Go function with `//export` and cgo generates a C-side export bridge for it; C code can call back using the corresponding `extern` declaration. The callback runs on whichever C thread made the call — it is not guaranteed to be the same thread as the previous caller.

### Performance

- A cross-boundary call has fixed overhead: entering/leaving syscall state and saving context. A single call isn't worth optimizing; on a hot path, move the boundary out of the loop — one call, a batch of data.
- String conversion has an allocation cost: `C.CString` mallocs on the C heap every time, and you must `C.free` afterwards; for bulk data pass an `unsafe.Pointer` with a length instead of converting element by element.
- For high-frequency small calls, plan for the long term: turn the C side into a service (interprocess communication), or move the whole hot loop over to run on the C side.

### Pointer Rules (Safety and Limits)

cgo has explicit rules for passing pointers; violating them is an error at run time:

1. A Go pointer can be passed to C as an argument during the call, but the C side must not keep holding it after the call returns.
2. Go memory may store C pointers; C memory must not store Go pointers.
3. When a Go pointer into the Go heap is passed to C, the Go side must ensure that memory is not moved during that call — the current GC does not move heap objects, but the rule is part of the language contract, so have it in mind when writing `unsafe` code.

Checks: `GODEBUG=cgocheck=1` (on by default, catches violations of rules 2 and 3) and `GODEBUG=cgocheck=2` (stricter, also catches C still using a Go pointer after it has returned; higher overhead, use it while debugging). `go vet` also flags common CGO pointer misuse.

### Concurrency

While a CGO call is in progress the goroutine is blocked in a syscall; the P is yielded to other goroutines and no thread is held. When C code calls back into Go, the callback goroutine runs on the C thread, and after it finishes it can be scheduled onto any M — do not assume the callback and the original goroutine share a thread; any shared data locked in the callback should be protected with the `sync` package.

### Debugging

- `gdb` / `lldb` can show both the Go stack and the C stack; use `bt` to see the full call chain across the boundary.
- `go tool nm <binary>` lets you verify that the `//export` symbols were generated.
- To track down pointer violations, start by running tests under `GODEBUG=cgocheck=2`; clear the boundary problems first, then tune performance or concurrency.

Cross-reading: [CGO Call Records](/cgo/CGO.md) covers the call steps, type conversion and common pitfalls; the [command documentation](https://golang.google.cn/cmd/cgo/) has the pointer rules in the original wording.

## References

- [cgo command documentation](https://pkg.go.dev/cmd/cgo)
- [Official · A Quick Guide to Go's Assembler](https://go.dev/doc/asm)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Unsafe](/sys/Unsafe.md)
