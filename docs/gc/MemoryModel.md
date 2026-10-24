# Go Memory Model: when one goroutine is guaranteed to see another's write

The memory model answers one specific question: goroutine A changed a variable, and goroutine B is guaranteed to read the new value when. The official document `/ref/mem` is the only authority; this repo had only mentioned the term on the home page before. The content below comes from the official page, fetched 2026-10-08.

## 1. The three pieces of advice at the start of the spec

The Advice section of the original spec is very direct:

1. Data modified by multiple goroutines at the same time must be accessed serially, protected by channel operations or the synchronization primitives in `sync` or `sync/atomic`.
2. If you have to read the rest of this document to understand what your program does, you are overthinking it. The exact words are: If you must read the rest of this document to understand the behavior of your program, you are being too clever. Don't be clever.

My conclusion: share mutable data with no synchronization and you might read anything; add synchronization, then judge by the rules below.

## 2. A few definitions

- **Data race**: a write to one memory location happens at the same time as another read or write to the same location, unless all accesses are the atomic ones provided by `sync/atomic`.
- **DRF-SC**: a Go program with no data race behaves as if all its goroutines run in order on a single processor. This property is called: data-race-free programs execute in a sequentially consistent manner.
- **The floor the implementation promises**: the implementation may report a race and terminate the program at any time; beyond that, every read of a single-word or subword memory location must observe a value that was actually written and has not been overwritten since. The spec describes this level of constraint as "closer to Java or JavaScript than to C/C++", because a racing program in C/C++ is completely undefined.

## 3. The synchronization rules (the original Happens-before rules)

| Situation | Guarantee |
| --- | --- |
| Package initialization | All `init` functions in `q` have finished before any `init` function in a package `p` that imports `q` begins; all `init` functions have finished before `main.main` begins |
| Starting a goroutine | the `go` statement happens before the goroutine's execution begins |
| Goroutine exit | **no guarantee at all**. The counterexample the spec gives: assigning to a global variable just before exit — other goroutines are not guaranteed to see it, and an aggressive compiler might even delete the whole `go` statement |
| Channel send | a given send happens before the corresponding receive completes |
| Channel close | the close happens before the receive that returns the zero value because the channel was closed |
| Receive on an unbuffered channel | that receive happens before the corresponding send completes |
| Buffered channel | for a channel of capacity C, the k-th receive happens before the (k+C)-th send completes (a counting semaphore can be modeled this way) |
| Locks | for any `sync.Mutex` or `sync.RWMutex` variable `l` and `n < m`, the n-th `l.Unlock()` happens before the m-th `l.Lock()` returns |
| `sync.Once` | the execution of `f` inside `once.Do(f)` completes before any `once.Do(f)` returns |

The "the receiver reads after the sender finished writing" claim in `docs/zh/concurrency/Chan.md` rests on exactly those three channel rows; and the "goroutine exit gives no guarantee" row is the reason every "wait for the goroutine to finish, then read the result" pattern in `docs/zh/concurrency/` has to be written the way it is.

## 4. The skeleton of the formal definition

The official formal definition follows the line of Boehm and Adve's 2008 PLDI paper "Foundations of the C++ Concurrency Memory Model". Three requirements:

1. The memory operations inside each goroutine must correspond to one correct sequential execution of that goroutine, consistent with the sequenced-before relations the control-flow structures of the language spec define.
2. Restricting that mapping to synchronization operations, it must be explainable by some implicit total order of the synchronization operations, and that total order must be consistent with program order and with the values read and written.
3. The write `w` read by a plain read `r` must be visible to it: `w` happens before `r`, and there is no other write `w'` that happens before `r` and which `w` also happens before — in other words, take the most recent visible write.

Read-class operations include read, atomic read, mutex lock, and channel receive; write-class operations include write, atomic write, mutex unlock, and channel send and close; both sides of an atomic compare-and-swap count as both.

## 5. When you need to read this page

- You wrote a lock-free singleton, lazy initialization, or state machine without `sync/atomic` or `sync.Once`.
- You used goroutine exit as your "it's done" signal, with no channel or `WaitGroup` to wait on.
- You use a buffered channel as a queue and assume "I received, so the other side has finished writing memory".

The first two are wrong straight from the table; the third depends on capacity — the k-th receive only guarantees happening before the (k+C)-th send.

## Sources

1. https://golang.google.cn/ref/mem — The Go Memory Model: the Advice, Informal Overview, and Synchronization sections and the three Requirements (fetched 2026-10-08)
2. https://golang.google.cn/ref/spec — expression evaluation order in the language spec (cited by Requirement 1)

## References

- [Official · A Guide to the Go Garbage Collector](https://go.dev/doc/gc-guide)
- [Official blog · Go GC: Prioritizing low latency and simplicity](https://go.dev/blog/go15gc)
- [The Go Memory Model](https://go.dev/ref/mem)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
- [knowledge](/knowledge.md)
