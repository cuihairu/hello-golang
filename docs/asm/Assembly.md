The Plan 9 assembler instruction set is relatively small but covers the basic operations. Below are some common Plan 9 instructions, with their usage and what they do.

### Data Transfer Instructions

#### The MOV instruction
- **MOVB src, dst**: move a byte
- **MOVW src, dst**: move a word
- **MOVL src, dst**: move a doubleword
- **MOVQ src, dst**: move a quadword

```assembly
MOVQ $10, AX       // move the immediate 10 into the AX register
MOVQ AX, 0x1000    // move the value of the AX register to memory address 0x1000
MOVQ 0x1000, BX    // move the value at memory address 0x1000 to the BX register
```

### Arithmetic Instructions

#### The ADD instruction
- **ADDB src, dst**: byte addition
- **ADDW src, dst**: word addition
- **ADDL src, dst**: doubleword addition
- **ADDQ src, dst**: quadword addition

```assembly
ADDQ AX, BX        // add the values of AX and BX, storing the result in BX
```

#### The SUB instruction
- **SUBB src, dst**: byte subtraction
- **SUBW src, dst**: word subtraction
- **SUBL src, dst**: doubleword subtraction
- **SUBQ src, dst**: quadword subtraction

```assembly
SUBQ AX, BX        // subtract the value of AX from BX, storing the result in BX
```

#### The MUL instruction
- **MULB src**: byte multiplication
- **MULW src**: word multiplication
- **MULL src**: doubleword multiplication
- **MULQ src**: quadword multiplication

```assembly
MULQ AX            // multiply AX by AX, storing the result in AX
```

#### The DIV instruction
- **DIVB src**: byte division
- **DIVW src**: word division
- **DIVL src**: doubleword division
- **DIVQ src**: quadword division

```assembly
DIVQ AX            // divide DX:AX by src, storing the result in AX (quotient) and DX (remainder)
```

### Logical Instructions

#### The AND instruction
- **ANDB src, dst**: byte AND
- **ANDW src, dst**: word AND
- **ANDL src, dst**: doubleword AND
- **ANDQ src, dst**: quadword AND

```assembly
ANDQ AX, BX        // bitwise AND of AX and BX, storing the result in BX
```

#### The OR instruction
- **ORB src, dst**: byte OR
- **ORW src, dst**: word OR
- **ORL src, dst**: doubleword OR
- **ORQ src, dst**: quadword OR

```assembly
ORQ AX, BX         // bitwise OR of AX and BX, storing the result in BX
```

#### The XOR instruction
- **XORB src, dst**: byte XOR
- **XORW src, dst**: word XOR
- **XORL src, dst**: doubleword XOR
- **XORQ src, dst**: quadword XOR

```assembly
XORQ AX, BX        // bitwise XOR of AX and BX, storing the result in BX
```

#### The NOT instruction
- **NOTB dst**: byte complement
- **NOTW dst**: word complement
- **NOTL dst**: doubleword complement
- **NOTQ dst**: quadword complement

```assembly
NOTQ AX            // flip every bit of AX
```

### Data Comparison Instructions

#### The CMP instruction
- **CMPB src, dst**: compare bytes
- **CMPW src, dst**: compare words
- **CMPL src, dst**: compare doublewords
- **CMPQ src, dst**: compare quadwords

```assembly
CMPQ AX, BX        // compare AX and BX, affecting the flags register
```

### Control Flow Instructions

#### The JMP instruction
- **JMP addr**: unconditional jump

```assembly
JMP 0x1000         // jump to address 0x1000
```

#### Conditional jump instructions
- **JE addr**: jump if equal
- **JNE addr**: jump if not equal
- **JG addr**: jump if greater
- **JGE addr**: jump if greater than or equal
- **JL addr**: jump if less
- **JLE addr**: jump if less than or equal

```assembly
CMPQ AX, BX        // compare AX and BX
JE 0x1000          // if AX == BX, jump to 0x1000
```

### Stack Instructions

#### The PUSH instruction
- **PUSHB src**: push a byte
- **PUSHW src**: push a word
- **PUSHL src**: push a doubleword
- **PUSHQ src**: push a quadword

```assembly
PUSHQ AX           // push AX onto the stack
```

#### The POP instruction
- **POPB dst**: pop a byte
- **POPW dst**: pop a word
- **POPL dst**: pop a doubleword
- **POPQ dst**: pop a quadword

```assembly
POPQ AX            // pop one quadword from the top of the stack into AX
```

### Function Call Instructions

#### The CALL instruction
- **CALL addr**: call a function

```assembly
CALL runtime·newproc(SB)  // call runtime's newproc function
```

#### The RET instruction
- **RET**: return

```assembly
RET                // return from the function
```

### Special Instructions

#### The NOP instruction
- **NOP**: no operation

```assembly
NOP                // no-op, usually used for alignment or delay
```

#### The HLT instruction
- **HLT**: halt the processor

```assembly
HLT                // halt the processor, usually used for debugging
```

### Others

#### The LEA instruction
- **LEAQ src, dst**: compute a memory address

```assembly
LEAQ 8(SP), BP     // store the result of SP plus 8 in BP
```

#### The PCDATA and FUNCDATA instructions
- **PCDATA** and **FUNCDATA**: used for debugging and stack traces

```assembly
PCDATA $0, $-2     // mark debugging info
FUNCDATA $1, info  // store function data
```

These instructions form the foundation of the Plan 9 assembler; once you are familiar with them, reading the output of `go build -gcflags="-S"` is more comfortable.

### Reading Go's internals in disassembly

Reading Go's low-level assembly shows you what function calls, stack frames, concurrency, and garbage collection look like at the machine level. Below I use a few small examples, compiled and then disassembled to verify.

#### Function calls and stack frames

In Go, every function call creates a new stack frame to hold the function's arguments, local variables, and return address. Stack frame management is handled automatically by the compiler and the runtime.

##### Example code

```go
package main

import "fmt"

func add(a, b int) int {
    return a + b
}

func main() {
    result := add(3, 4)
    fmt.Println(result)
}
```

Compile and disassemble the code above, and you can see how the function call and stack frame are managed:

```bash
go build -gcflags="-S" main.go
```

The generated assembly (partial; Go 1.27 / amd64 — output differs between versions) looks like this:

```assembly
	0x0000 00000 (main.go:5)	TEXT	main.add(SB), NOSPLIT|NOFRAME|ABIInternal, $0-16
	0x0000 00000 (main.go:5)	FUNCDATA	$0, gclocals·g5+hNtRBP6YXNjfog7aZjQ==(SB)
	0x0000 00000 (main.go:5)	FUNCDATA	$1, gclocals·g5+hNtRBP6YXNjfog7aZjQ==(SB)
	0x0000 00000 (main.go:5)	FUNCDATA	$5, main.add.arginfo1(SB)
	0x0000 00000 (main.go:5)	FUNCDATA	$6, main.add.argliveinfo(SB)
	0x0000 00000 (main.go:6)	ADDQ	BX, AX
	0x0003 00003 (main.go:6)	RET
```

You can see that since Go 1.17, function arguments and return values are passed through registers (on amd64 that is `AX`, `BX`, and so on), the stack cost for arguments is `$0-16`, and the function body is down to a single `ADDQ BX, AX`; earlier versions (Go 1.16 and before) instead show code storing and loading arguments at offsets from `SP`.

#### Concurrency

Go's concurrency model relies mainly on goroutines and channels. A goroutine is a lightweight thread managed by the Go runtime.

##### Creating a goroutine

```go
go func() {
    fmt.Println("Hello from goroutine")
}()
```

After compiling and disassembling, you can see that the `go` statement ultimately creates the goroutine by calling `runtime.newproc` in the runtime (the call site in user code):

```assembly
	0x0015 00021 (main.go:6)	CALL	runtime.newproc(SB)
```

`runtime.newproc` is implemented in `runtime/proc.go`; it is responsible for allocating the g struct, initializing the stack, and adding it to the run queue. You can inspect its implementation with `go tool objdump -s 'runtime.newproc' executable`.

#### Garbage collection

Go's garbage collection is automatic and uses a non-generational mark-and-sweep algorithm. The collector runs in a background thread, marking objects that are no longer used and freeing the memory they occupy.

##### Triggering garbage collection

```go
runtime.GC()
```

After compiling and disassembling, you can see that the `runtime.GC()` call lands on the `runtime.GC` entry point in the runtime (the call site in user code):

```assembly
	0x000a 00010 (main.go:6)	CALL	runtime.GC(SB)
```

The core GC logic (mark scheduling `gcStart`, concurrent marking, sweeping, and so on) lives in `runtime/mgc.go`; you can look further with `go tool objdump -s 'runtime\.GC$' executable` or by reading the source.

#### Summary

A function call compiles on amd64 to register arguments plus a single `ADDQ` and a `RET`; the `go` statement lands on `runtime.newproc`; `runtime.GC()` lands on the `runtime.GC` entry point. To go deeper, use `go tool objdump` together with the `runtime/proc.go` and `runtime/mgc.go` source to keep tracing down.

## References

- [Official · A Quick Guide to Go's Assembler](https://go.dev/doc/asm)

## Sibling pages

- [Program](/asm/Program.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Program](/asm/Program.md)
