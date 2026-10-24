# Features

Most of Go's features land directly in the syntax and the toolchain, and every one of them is verifiable. Listed one at a time below.

### 1. Concise syntax

Go deliberately keeps the syntax to an extremely small set. There are only 25 keywords, no header files, no macros, no enum types, and no classes and inheritance in the traditional sense. Loops come in just one form, `for`, yet it covers everything C's `while` and `do-while` can do.

```go
package main

import "fmt"

func main() {
    // the only loop keyword in Go
    sum := 0
    for i := 1; i <= 10; i++ {
        sum += i
    }
    fmt.Println("sum of 1 to 10:", sum) // prints: sum of 1 to 10: 55
}
```

Concise syntax lowers the bar for reading other people's code, and it makes Go code style highly uniform (`gofmt` enforces one formatting).

### 2. Built-in concurrency

Go provides concurrency primitives at the language level: `goroutine` and `channel`.

- **goroutine**: a lightweight thread scheduled by the Go runtime, starting with a stack of only about 2 KB; creating tens of thousands of goroutines costs far less than creating OS threads.
- **channel**: a type-safe pipe for communication between goroutines; combined with the `select` statement it enables flexible concurrent control.

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    var wg sync.WaitGroup
    results := make(chan int, 5)

    for i := 1; i <= 5; i++ {
        wg.Add(1)
        go func(n int) {
            defer wg.Done()
            results <- n * n
        }(i)
    }

    wg.Wait()
    close(results)

    for r := range results {
        fmt.Println(r)
    }
}
```

### 3. Static typing and compilation

Go is a statically typed, compiled language that compiles to native machine code, with no virtual machine layer. It also supports type inference, so an explicit type can be left out when declaring a variable:

```go
x := 10           // compiler infers int
name := "Go"      // compiler infers string
fmt.Println(x, name)
```

This keeps the safety of compile-time type checking while preserving a writing experience close to a dynamic language.

### 4. Automatic garbage collection

Go ships with a garbage collector, so developers don't have to manage memory by hand. Go's GC is a concurrent mark-and-sweep collector, with pauses typically in the sub-millisecond range, which suits latency-sensitive services.

```go
func createData() []int {
    data := make([]int, 1000)
    for i := range data {
        data[i] = i
    }
    return data
    // once data is no longer referenced, the garbage collector reclaims it automatically, no free needed
}
```

### 5. Fast compilation

Go's compiler treats fast compilation as a design goal: dependency analysis is precise, and there is a package-level compilation cache, so even large projects build in seconds.

### 6. Standard library

Go's standard library covers the areas used most often in development:

- **Networking**: `net`, `net/http` (you can build a production-grade HTTP service directly)
- **Encoding**: `encoding/json`, `encoding/xml`
- **Cryptography**: `crypto/*`
- **Testing**: a built-in `testing` framework, so unit tests and benchmarks can be written without a third-party test library

```go
package main

import (
    "fmt"
    "net/http"
)

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintln(w, "Hello, Go!")
    })
    http.ListenAndServe(":8080", nil)
}
```

### 7. Static linking and cross-compilation

By default Go statically links the runtime and dependencies into a single executable, so no extra runtime needs to be installed on deployment. By setting the `GOOS` and `GOARCH` environment variables, cross-compilation is done in one command:

```sh
GOOS=linux GOARCH=amd64 go build -o myapp
GOOS=windows GOARCH=amd64 go build -o myapp.exe
```

### Summary

Each of these seven features has a fact behind it: 25 keywords, a 2 KB initial stack, sub-millisecond GC pauses, second-scale builds, a single static binary. Large infrastructure software such as Docker and Kubernetes is written in Go, which lines up directly with the above.

## References

- [Official documentation overview](https://go.dev/doc/)
- [Release history and support policy](https://go.dev/doc/devel/release)
- [Official FAQ](https://go.dev/doc/faq)
- [Effective Go (official)](https://go.dev/doc/effective_go)

## Sibling pages

- [ReleaseNotes](/introduction/ReleaseNotes.md)
- [Introduction](/introduction/Introduction.md)
- [Lineage](/introduction/Lineage.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Introduction](/introduction/Introduction.md)
- [Lineage](/introduction/Lineage.md)
