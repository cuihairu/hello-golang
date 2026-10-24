# Jump statements

Jump statements change the order in which the program executes. Go provides three jump statements — `break`, `continue`, and `goto` — and they can be combined with labels for finer control.

## `break`

`break` is used to immediately terminate the enclosing `for` loop, `switch`, or `select` statement. Note: in a `switch`/`select` nested inside a `for`, an unlabeled `break` only jumps out of the `switch`/`select` itself.

```go
package main

import "fmt"

func main() {
    for i := 0; i < 10; i++ {
        if i == 5 {
            break
        }
        fmt.Println(i)
    }
}
```

With a label, you can jump out of several levels of loops at once:

```go
package main

import "fmt"

func main() {
outer:
    for i := 0; i < 3; i++ {
        for j := 0; j < 3; j++ {
            if i == 1 && j == 1 {
                break outer
            }
            fmt.Println(i, j)
        }
    }
    fmt.Println("end")
}
```

See [break](/syntax/Break.md) for details.

## `continue`

`continue` is used to skip the remaining statements of the current loop iteration and go straight to the next one. It also supports labels:

```go
package main

import "fmt"

func main() {
    for i := 0; i < 5; i++ {
        if i%2 == 0 {
            continue
        }
        fmt.Println(i)
    }
}
```

See [continue](/syntax/Continue.md) for details.

## `goto`

`goto` jumps unconditionally to a label within the same function. Go imposes two hard restrictions on `goto`:

- You cannot jump to another function, and you cannot jump across functions.
- You cannot jump over a variable declaration that comes before the label, or you get a compile error "jumps over declaration".

```go
package main

import "fmt"

func main() {
    i := 0
loop:
    if i < 3 {
        fmt.Println(i)
        i++
        goto loop
    }
    fmt.Println("end")
}
```

`goto` makes control flow hard to follow. In everyday code, prefer `break`, `continue`, or `return`, and consider it only in the few cases where you need to centralize error cleanup logic.

See [goto](/syntax/Goto.md) for details.

## Labels

A label is an identifier followed directly by a colon, used to mark the position of a statement and referenced by `break`, `continue`, and `goto`. A label is only valid within the function that defines it, and labels that are never referenced are ignored by the compiler (`go vet` will flag them).

```go
package main

import "fmt"

func main() {
done:
    for i := 0; i < 3; i++ {
        fmt.Println(i)
        if i == 1 {
            break done
        }
    }
}
```

## References

- [Language Specification · Statements](https://go.dev/ref/spec#Statements)
- [Effective Go · Control Structures](https://go.dev/doc/effective_go#control-structures)
- [Language Specification · Break/Continue/Goto](https://go.dev/ref/spec#Break_statements)


## Sibling pages

- [Break](/syntax/Break.md)
- [Continue](/syntax/Continue.md)
- [For](/syntax/For.md)
- [If](/syntax/If.md)
- [Loop](/syntax/Loop.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Loop](/syntax/Loop.md)
