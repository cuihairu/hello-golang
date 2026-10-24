# Loop statements

Loop statements are used to execute a block of code repeatedly. Go has only one loop statement — `for` — but by omitting some of its parts, it can cover every case: `while`, `do-while`, infinite loops, and so on.

## The three-part `for`

The most common form consists of an initialization statement, a condition expression, and a post statement, separated by semicolons:

```go
package main

import "fmt"

func main() {
    sum := 0
    for i := 1; i <= 100; i++ {
        sum += i
    }
    fmt.Println("sum of 1 to 100:", sum)
}
```

Both the initialization and the post statement can be omitted, and once they are the semicolons can be dropped too — at that point it is equivalent to `while`:

```go
package main

import "fmt"

func main() {
    n := 1
    for n < 100 {
        n *= 2
    }
    fmt.Println(n)
}
```

Omitting all three parts gives an infinite loop, which needs `break`, `return`, or `panic` to exit:

```go
package main

import "fmt"

func main() {
    count := 0
    for {
        count++
        if count%2 == 0 {
            continue
        }
        if count > 5 {
            break
        }
        fmt.Println(count)
    }
}
```

## Iteration with `for range`

`range` is used to iterate over arrays, slices, strings, maps, and channels. Different collections return different iteration variables:

| Collection type | First value | Second value |
| --- | --- | --- |
| array, slice, string | index | element copy |
| map | key | value |
| channel | element | - |
| integer (Go 1.22+) | 0..n-1 | - |

```go
package main

import "fmt"

func main() {
    nums := []int{10, 20, 30}
    for i, v := range nums {
        fmt.Println(i, v)
    }

    // only the index or key is needed
    for i := range nums {
        fmt.Println(i)
    }

    // only the value is needed, so the index is discarded with the blank identifier
    sum := 0
    for _, v := range nums {
        sum += v
    }
    fmt.Println(sum)

    m := map[string]int{"a": 1, "b": 2}
    for k, v := range m {
        fmt.Println(k, v)
    }

    // iterating over a string goes code point by code point in UTF-8
    for i, r := range "Go语言" {
        fmt.Printf("%d %q\n", i, r)
    }
}
```

## The scope of the loop variable

Before Go 1.22, the loop variable shared a single instance across the whole loop, so referencing it directly inside closures and goroutines gave unexpected results; from Go 1.22 on, a new variable instance is created on every iteration. The cross-version-compatible way to write it is to copy explicitly inside the loop body:

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    var wg sync.WaitGroup
    for i := 0; i < 3; i++ {
        wg.Add(1)
        i := i // copy the loop variable so this works on all versions
        go func() {
            defer wg.Done()
            fmt.Println(i)
        }()
    }
    wg.Wait()
}
```

## Loops with `break` and `continue`

`break` terminates the enclosing loop immediately, and `continue` skips the rest of the current iteration and goes straight to the next one. Both can take a label, so that they act on an outer loop:

```go
package main

import "fmt"

func main() {
outer:
    for i := 1; i <= 3; i++ {
        for j := 1; j <= 3; j++ {
            if j > i {
                continue outer // start the next iteration of the outer loop
            }
            if i*j == 6 {
                break outer // end the outer loop
            }
            fmt.Printf("%d*%d=%d ", i, j, i*j)
        }
        fmt.Println()
    }
}
```

For detailed explanations, see [for](/syntax/For.md), [break](/syntax/Break.md), and [continue](/syntax/Continue.md).

## References

- [Language Specification · Statements](https://go.dev/ref/spec#Statements)
- [Effective Go · Control Structures](https://go.dev/doc/effective_go#control-structures)
- [Language Specification · For statements](https://go.dev/ref/spec#For_statements)


## Sibling pages

- [Break](/syntax/Break.md)
- [Continue](/syntax/Continue.md)
- [For](/syntax/For.md)
- [Jump](/syntax/Jump.md)
- [Switch](/syntax/Switch.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Jump](/syntax/Jump.md)
