# Glossary

Chinese-English pairs, one-sentence definitions and authoritative sources for this repo's core terms. Sources are all official documentation, official blog posts, the language specification or original papers, and each is clickable; entries where no authoritative source could be found are labelled as such. Links to related pages point into this repo's body text.

## Concurrency and the runtime

### Goroutine
A lightweight unit of execution, scheduled by the Go runtime rather than by an OS thread, with a very small initial stack and the ability to coexist in large numbers.
**Source**: [Language spec · Go statements](https://go.dev/ref/spec#Go_statements), [Effective Go · Goroutines](https://go.dev/doc/effective_go#goroutines)
**Related page**: [Goroutine](/concurrency/Goroutine.md), [GoroutineImpl](/concurrency/GoroutineImpl.md)

### GMP scheduling model
The abstraction of the Go runtime scheduler: G (goroutine), M (machine thread), P (processor, which holds the queue of runnable Gs).
**Source**: [Official · Go scheduler design doc (golang.org/s/go11sched)](https://golang.org/s/go11sched)
**Related page**: [GMP](/concurrency/GMP.md), [Runtime](/sync/Runtime.md)

### Channel
A typed, concurrency-safe pipe for sending and receiving values between goroutines; an unbuffered channel synchronizes the sender and receiver.
**Source**: [Language spec · Channel types](https://go.dev/ref/spec#Channel_types), [Go memory model · channels](https://go.dev/ref/mem#chan), [Effective Go · Channels](https://go.dev/doc/effective_go#channels)
**Related page**: [Chan](/concurrency/Chan.md), [ChanImpl](/concurrency/ChanImpl.md)

### Select
A control structure that waits on multiple channel operations and, among the ready branches, picks one at random to execute.
**Source**: [Language spec · Select statements](https://go.dev/ref/spec#Select_statements)
**Related page**: [Select](/concurrency/Select.md)

### CSP (Communicating Sequential Processes)
The concurrency model proposed by Tony Hoare, the philosophical origin of Go's concurrency design: "Do not communicate by sharing memory; share memory by communicating."
**Source**: [Hoare 1978 original paper (CACM, DOI)](https://dl.acm.org/doi/10.1145/359576.359585), [CSP overview · Wikipedia](https://en.wikipedia.org/wiki/Communicating_sequential_processes)
**Related page**: [CSP](/concurrency/CSP.md), [Actor](/concurrency/Actor.md)

### Data race
Two goroutines concurrently access the same memory location, at least one is a write, and there is no synchronization between them -- the behavior is undefined.
**Source**: [Go memory model](https://go.dev/ref/mem), [Official blog · Introducing the Go Race Detector](https://go.dev/blog/race-detector)
**Related page**: [RaceCondition](/sync/RaceCondition.md)

### Go memory model
Specifies whether one goroutine can observe a value written by another goroutine; the core is the happens-before relation.
**Source**: [Go memory model](https://go.dev/ref/mem)
**Related page**: [MemoryModel](/gc/MemoryModel.md), [MemorySynchronization](/sync/MemorySynchronization.md)

### Happens-before
A partial order in the memory model: if A happens-before B, then A's write is visible to B.
**Source**: [Go memory model](https://go.dev/ref/mem)
**Related page**: [MemoryModel](/gc/MemoryModel.md)

### Mutex
A lock that guarantees only one goroutine at a time enters the critical section, `sync.Mutex`.
**Source**: [sync standard library](https://pkg.go.dev/sync)
**Related page**: [Mutex](/sync/Mutex.md)

### RWMutex
A lock that allows multiple readers and a single writer, with higher throughput in read-heavy/write-light scenarios, `sync.RWMutex`.
**Source**: [sync standard library](https://pkg.go.dev/sync)
**Related page**: [RWMutex](/sync/RWMutex.md)

### WaitGroup
A counting barrier that waits for a group of goroutines to finish, `sync.WaitGroup`.
**Source**: [sync standard library](https://pkg.go.dev/sync)
**Related page**: [WaitGroup](/concurrency/WaitGroup.md)

### Atomic
An indivisible low-level memory primitive, `sync/atomic`, the foundation of lock-free algorithms.
**Source**: [sync/atomic standard library](https://pkg.go.dev/sync/atomic), [Go memory model · atomics](https://go.dev/ref/mem#atomic)
**Related page**: [Atomic](/sync/Atomic.md)

### Critical section
A block of code that accesses a shared resource and requires mutual exclusion.
**Source**: [Go memory model · locks](https://go.dev/ref/mem#locks)
**Related page**: [CriticalSection](/sync/CriticalSection.md)

### Context
The standard carrier for passing cancellation signals, deadlines and request-scoped values across API boundaries, `context.Context`.
**Source**: [context standard library](https://pkg.go.dev/context), [Official blog · Go Concurrency Patterns: Context](https://go.dev/blog/context)
**Related page**: [Context](/sync/Context.md)

### errgroup
`golang.org/x/sync/errgroup`: goroutine group management with error propagation and cancellation.
**Source**: [golang.org/x/sync/errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup)
**Related page**: [ErrorGroup](/concurrency/ErrorGroup.md)

### Goroutine leak
A goroutine that cannot exit because it is blocked on a channel operation that never arrives, leaking memory as they accumulate.
**Source**: [Official blog · Goroutine Leak Profiles](https://go.dev/blog/goroutine-leak-profiles)
**Related page**: [GoroutineImpl](/concurrency/GoroutineImpl.md), [Pprof](/debug/Pprof.md)

### Race detector
A dynamic data-race detection tool based on ThreadSanitizer, `go test -race`.
**Source**: [Official blog · Introducing the Go Race Detector](https://go.dev/blog/race-detector)
**Related page**: [RaceCondition](/sync/RaceCondition.md), [Test](/test/Test.md)

## Memory and garbage collection

### GC
The Go runtime mechanism that automatically reclaims unreachable heap memory; concurrent, tri-color marking, low pause.
**Source**: [Official · A Guide to the Go Garbage Collector](https://go.dev/doc/gc-guide)
**Related page**: [GC](/gc/GC.md), [GC (memory allocation chapter)](/alloc/GC.md)

### Tri-color marking
The abstraction of GC reachability analysis: white (unvisited), gray (to be scanned), black (scanned).
**Source**: [Official GC guide · The GC cycle](https://go.dev/doc/gc-guide#The_GC_cycle)
**Related page**: [GC](/gc/GC.md)

### Hybrid write barrier
The write barrier strategy from Go 1.8 onward, reducing the time needed for a stack rescan to near zero.
**Source**: [Official blog · Go GC: Prioritizing low latency and simplicity](https://go.dev/blog/go15gc)
**Related page**: [GC](/gc/GC.md)

### GOGC
The environment variable / parameter controlling when GC is triggered: heap growth percentage.
**Source**: [Official GC guide · GOGC](https://go.dev/doc/gc-guide#GOGC)
**Related page**: [Practice](/alloc/Practice.md)

### GOMEMLIMIT
A soft ceiling on heap memory, the `GOMEMLIMIT` environment variable, preventing memory runaway.
**Source**: [Official GC guide · Memory limit](https://go.dev/doc/gc-guide#Memory_limit)
**Related page**: [Practice](/alloc/Practice.md)

### Escape analysis
The compiler's analysis of whether an object is allocated on the stack or the heap; objects that escape are managed by the GC.
**Source**: [Official GC guide · Escape analysis](https://go.dev/doc/gc-guide#Escape_analysis), [Official blog · Allocating on the Stack](https://go.dev/blog/allocation-optimizations)
**Related page**: [Segment](/var/Segment.md), [Alloc](/alloc/Alloc.md)

### Zero value
The default value of a declared variable that has not been explicitly assigned; Go guarantees every variable always has a definite initial value.
**Source**: [Language spec · The zero value](https://go.dev/ref/spec#The_zero_value)
**Related page**: [VarAndInit](/var/VarAndInit.md)

### nil
A predeclared identifier: the zero value of pointer, channel, map, slice, interface and function types.
**Source**: [Language spec · Predeclared identifiers](https://go.dev/ref/spec#Predeclared_identifiers)
**Related page**: [Nil](/const/Nil.md)

## Type system

### Slice
An abstraction over a backing array: pointer + length + capacity, and it can grow dynamically.
**Source**: [Language spec · Slice types](https://go.dev/ref/spec#Slice_types), [Official blog · Go Slices: usage and internals](https://go.dev/blog/slices-intro)
**Related page**: [Slice](/type/Slice.md)

### Append growth
`append` allocates a larger backing array and moves the elements when capacity is exceeded.
**Source**: [Official blog · How append works](https://go.dev/blog/slices)
**Related page**: [Slice](/type/Slice.md)

### Map
A key-value container implemented as a hash table, with deliberately randomized iteration order, `map[K]V`.
**Source**: [Language spec · Map types](https://go.dev/ref/spec#Map_types), [Official blog · Go maps in action](https://go.dev/blog/maps)
**Related page**: [Map](/type/Map.md)

### Interface
A set of method signatures; Go's implicit implementation (structural typing) differs from the nominal implementation of other languages.
**Source**: [Language spec · Interface types](https://go.dev/ref/spec#Interface_types), [Effective Go · Interfaces](https://go.dev/doc/effective_go#interfaces)
**Related page**: [Interface](/type/Interface.md), [Interface (OOP chapter)](/oop/Interface.md)

### Method set
The set of methods associated with a type, which determines interface satisfaction; value receivers and pointer receivers have different method sets.
**Source**: [Language spec · Method sets](https://go.dev/ref/spec#Method_sets)
**Related page**: [PointerReceiver](/oop/PointerReceiver.md)

### Type assertion
Extracting the concrete value of an interface value's dynamic type, `x.(T)`, optionally in comma-ok form.
**Source**: [Language spec · Type assertions](https://go.dev/ref/spec#Type_assertions)
**Related page**: [Assertion](/type/Assertion.md), [TypeAssertion](/oop/TypeAssertion.md)

### Type switch
`switch x.(type)`, which dispatches on the dynamic type of an interface value.
**Source**: [Language spec · Type switches](https://go.dev/ref/spec#Type_switches)
**Related page**: [Switch](/type/Switch.md)

### Reflection
The ability to inspect types and values at runtime, the `reflect` package; the official position is framed as "three laws".
**Source**: [Official blog · The Laws of Reflection](https://go.dev/blog/laws-of-reflection), [reflect standard library](https://pkg.go.dev/reflect)
**Related page**: [Reflection](/reflection/Reflection.md)

### Generics
Type parameterization, from Go 1.18 onward; functions and types can carry type parameters and constraints.
**Source**: [Official blog · An Introduction To Generics](https://go.dev/blog/intro-generics), [Language spec · Type parameter declarations](https://go.dev/ref/spec#Type_parameter_declarations)
**Related page**: [Generics](/generics/Generics.md)

### Constraint
The interface-like condition a type parameter must satisfy, expressible with approximate elements (`~T`) and unions (`A|B`).
**Source**: [Official blog · When To Use Generics](https://go.dev/blog/when-generics)
**Related page**: [Constraints](/generics/Constraints.md)

### Type inference
The compiler's mechanism for deriving type parameters from arguments, the core of generics' syntactic sugar.
**Source**: [Official blog · Type Inference](https://go.dev/blog/type-inference)
**Related page**: [TypeInference](/type/TypeInference.md)

### Embedding
Writing a named type into a struct/interface without a field name, gaining forwarding and composition, Go's substitute for inheritance.
**Source**: [Effective Go · Embedding](https://go.dev/doc/effective_go#embedding)
**Related page**: [Embedding](/oop/Embedding.md)

### Closure
A function literal that references outer variables; a `func` expression is a function value.
**Source**: [Language spec · Function literals](https://go.dev/ref/spec#Function_literals)
**Related page**: [AnonymousFunc](/func/AnonymousFunc.md)

### Variadic parameter
A `...T` parameter at the end of a parameter list, to which the caller may pass any number of arguments.
**Source**: [Language spec · Function types (variadic)](https://go.dev/ref/spec#Function_types)
**Related page**: [VariadicParameters](/func/VariadicParameters.md)

### Iota
A counter that increments inside constant declarations, used with constant expressions to generate enumerations.
**Source**: [Language spec · Iota](https://go.dev/ref/spec#Iota), [Official blog · Constants](https://go.dev/blog/constants)
**Related page**: [Iota](/const/Iota.md)

### Untyped constant
A constant not bound to a specific type, with unbounded precision and able to be implicitly adapted to many types.
**Source**: [Official blog · Constants](https://go.dev/blog/constants)
**Related page**: [Cant](/const/Cant.md)

### Struct tag
A metadata string on a struct field, the conventional carrier for encoding/decoding and mapping.
**Source**: [encoding/json standard library · tag conventions](https://pkg.go.dev/encoding/json), [Official blog · JSON and Go](https://go.dev/blog/json)
**Related page**: [StructTags](/idioms/StructTags.md)

## Error handling

### Error
The `error` built-in interface: non-nil means failure; Go errors are values, checked explicitly.
**Source**: [Language spec · Errors](https://go.dev/ref/spec#Errors), [Official blog · Error handling and Go](https://go.dev/blog/error-handling-and-go)
**Related page**: [Error](/error/Error.md)

### Error wrapping
`fmt.Errorf`'s `%w` verb and the `errors.Is/As/Unwrap` chain of checks.
**Source**: [errors standard library](https://pkg.go.dev/errors)
**Related page**: [Errors](/error/Errors.md)

### Defer
A call delayed until just before the function returns, stack-ordered LIFO, commonly paired with resource release.
**Source**: [Language spec · Defer statements](https://go.dev/ref/spec#Defer_statements), [Official blog · Defer, Panic, and Recover](https://go.dev/blog/defer-panic-and-recover)
**Related page**: [Defer](/func/Defer.md)

### Panic / Recover
The interruption mechanism for unrecoverable errors and the catching mechanism, appearing as a pair inside deferred calls.
**Source**: [Official blog · Defer, Panic, and Recover](https://go.dev/blog/defer-panic-and-recover), [Effective Go · Recover](https://go.dev/doc/effective_go#recover)
**Related page**: [PanicAndRecover](/error/PanicAndRecover.md)

## Engineering

### Module
A versioned set of packages, declared in `go.mod` with a path and dependencies, Go's unit of dependency.
**Source**: [Official · Go Modules usage guide](https://go.dev/doc/modules/), [Go Modules Reference](https://go.dev/ref/mod)
**Related page**: [Mod](/mod/Mod.md)

### go.mod
The declaration file at a module root: module path, Go version, require/exclude/retract.
**Source**: [Go Modules Reference](https://go.dev/ref/mod)
**Related page**: [Init](/mod/Init.md)

### MVS (minimal version selection)
Go's dependency resolution algorithm: pick the minimal (most conservative) version that satisfies every requirement for each dependency.
**Source**: [Go Modules Reference · minimal version selection](https://go.dev/ref/mod)
**Related page**: [Mod](/mod/Mod.md)

### Workspace
`go.work` aggregates several local modules for coordinated development without editing go.mod.
**Source**: [Go Official Documentation · Workspaces (external link)](https://go.dev/doc/tutorial/workspaces)
**Related page**: [Work](/mod/Work.md)

### Toolchain
The whole of the go command, compiler, standard library and related tools; supports multi-version install and automatic switching.
**Source**: [Official · Installing and managing the Go toolchain](https://go.dev/doc/manage-install)
**Related page**: [Env](/env/Env.md), [Install](/env/Install.md)

### Pprof
A runtime performance profiling toolset: CPU, heap, goroutines, locks, trace.
**Source**: [runtime/pprof standard library](https://pkg.go.dev/runtime/pprof), [Official blog · Profiling Go Programs](https://go.dev/blog/pprof)
**Related page**: [Pprof](/debug/Pprof.md)

### PGO (profile-guided optimization)
An optimization that feeds a production profile back into the compiler's inlining and layout decisions, from Go 1.21.
**Source**: [Official · Profile-guided optimization](https://go.dev/doc/pgo), [Official blog · PGO in Go 1.21](https://go.dev/blog/pgo)
**Related page**: [PGO](/debug/PGO.md)

### Fuzzing
Coverage-guided randomized testing, `FuzzXxx(*testing.F)`, built in from Go 1.18.
**Source**: [Official · Fuzzing](https://go.dev/doc/security/fuzz/)
**Related page**: [Fuzz](/zh/test/Fuzz.md)

### Deadlock
Multiple execution flows block forever, each waiting for a resource held by another. No authoritative single-page official source was found (to be verified); the runtime reports `fatal error: all goroutines are asleep` when all goroutines are unschedulable. The relevant standard-library position is in [sync standard library](https://pkg.go.dev/sync).
**Related page**: [CriticalSection](/sync/CriticalSection.md), [Chan](/concurrency/Chan.md)

## Algorithms and data structures

### Dynamic array
A variable-length array whose capacity doubles on demand; Go slices are its engineering form.
**Source**: [Dynamic array · Wikipedia](https://en.wikipedia.org/wiki/Dynamic_array), [Official blog · Go Slices](https://go.dev/blog/slices-intro)
**Related page**: [DynamicArray](/zh/algo/array/DynamicArray.md)

### Hash table
A key-value container with O(1) average access, whose performance shape depends on how collisions are handled.
**Source**: [Hash table · Wikipedia](https://en.wikipedia.org/wiki/Hash_table)
**Related page**: [Hash](/zh/algo/hash/Hash.md), [Map](/type/Map.md)

### Red-black tree
A self-balancing binary search tree with O(log n) insert/delete/lookup, one of the underlying structures of Go maps.
**Source**: [Red-black tree · Wikipedia](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree)
**Related page**: [RedBlackTree](/zh/algo/tree/RedBlackTree.md)

### Skip list
A multi-level linked list giving logarithmic lookup, the underlying implementation of Redis sorted sets.
**Source**: [Skip list · Wikipedia](https://en.wikipedia.org/wiki/Skip_list)
**Related page**: [SkipList](/zh/algo/list/SkipList.md)

---

**Maintenance rule**: any new entry must give a clickable authoritative source (official docs / spec / official blog / original paper / standard library); if none can be found, write "no authoritative source found (to be verified)". Do not fabricate links from memory.

<!-- BACKLINKS-AUTO -->
## Related pages

- [DynamicArray](/zh/algo/array/DynamicArray.md)
- [Hash](/zh/algo/hash/Hash.md)
- [SkipList](/zh/algo/list/SkipList.md)
- [RedBlackTree](/zh/algo/tree/RedBlackTree.md)
- [Alloc](/alloc/Alloc.md)
- [GC](/alloc/GC.md)
- [Practice](/alloc/Practice.md)
- [Actor](/concurrency/Actor.md)
- [CSP](/concurrency/CSP.md)
- [Chan](/concurrency/Chan.md)
- [ChanImpl](/concurrency/ChanImpl.md)
- [ErrorGroup](/concurrency/ErrorGroup.md)
- [GMP](/concurrency/GMP.md)
- [Goroutine](/concurrency/Goroutine.md)
- [GoroutineImpl](/concurrency/GoroutineImpl.md)
- [Select](/concurrency/Select.md)
- [WaitGroup](/concurrency/WaitGroup.md)
- [Cant](/const/Cant.md)
- [Iota](/const/Iota.md)
- [Nil](/const/Nil.md)
- [PGO](/debug/PGO.md)
- [Pprof](/debug/Pprof.md)
- [Env](/env/Env.md)
- [Install](/env/Install.md)
- [Error](/error/Error.md)
- [Errors](/error/Errors.md)
- [PanicAndRecover](/error/PanicAndRecover.md)
- [AnonymousFunc](/func/AnonymousFunc.md)
- [Defer](/func/Defer.md)
- [VariadicParameters](/func/VariadicParameters.md)
- [GC](/gc/GC.md)
- [MemoryModel](/gc/MemoryModel.md)
- [Constraints](/generics/Constraints.md)
- [Generics](/generics/Generics.md)
- [StructTags](/idioms/StructTags.md)
- [knowledge](/knowledge.md)
- [Init](/mod/Init.md)
- [Mod](/mod/Mod.md)
- [Work](/mod/Work.md)
- [Embedding](/oop/Embedding.md)
- [Interface](/oop/Interface.md)
- [PointerReceiver](/oop/PointerReceiver.md)
- [TypeAssertion](/oop/TypeAssertion.md)
- [Reflection](/reflection/Reflection.md)
- [Atomic](/sync/Atomic.md)
- [Context](/sync/Context.md)
- [CriticalSection](/sync/CriticalSection.md)
- [MemorySynchronization](/sync/MemorySynchronization.md)
- [Mutex](/sync/Mutex.md)
- [RWMutex](/sync/RWMutex.md)
- [RaceCondition](/sync/RaceCondition.md)
- [Runtime](/sync/Runtime.md)
- [Fuzz](/zh/test/Fuzz.md)
- [Test](/test/Test.md)
- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [Slice](/type/Slice.md)
- [Switch](/type/Switch.md)
- [TypeInference](/type/TypeInference.md)
- [Segment](/var/Segment.md)
- [VarAndInit](/var/VarAndInit.md)