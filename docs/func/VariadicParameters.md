In Go, variadic parameters let a function accept an indefinite number of arguments: put `...` in front of the parameter type, and inside the function they are treated as a slice.

### Defining variadic parameters

The defining syntax for a variadic function is to use three dots `...` before the parameter type. Inside the function, the variadic parameters are handled as a slice.

#### Example: defining and using a variadic function

```go
package main

import "fmt"

// define a variadic function
func sum(nums ...int) int {
    total := 0
    for _, num := range nums {
        total += num
    }
    return total
}

func main() {
    fmt.Println(sum(1, 2, 3))    // prints: 6
    fmt.Println(sum(4, 5, 6, 7)) // prints: 22
    fmt.Println(sum())           // prints: 0
}
```

`nums` is handled as a slice inside the function, so a `range` loop is enough to add it up.

### Passing variadic arguments

When calling a variadic function, you can pass any number of arguments directly. You can also pass an existing slice to a variadic function, but you need to add `...` after the slice variable to expand the slice.

#### Example: passing a slice as variadic arguments

```go
package main

import "fmt"

func sum(nums ...int) int {
    total := 0
    for _, num := range nums {
        total += num
    }
    return total
}

func main() {
    numbers := []int{1, 2, 3, 4, 5}
    fmt.Println(sum(numbers...)) // prints: 15
}
```

`sum(numbers...)` expands the `numbers` slice into individual arguments passed to `sum`.

### Variadic and other parameters

In a function, variadic parameters can be used together with other fixed parameters. Note that the variadic parameter must be the last item in the parameter list.

#### Example: fixed and variadic parameters

```go
package main

import "fmt"

func greet(prefix string, names ...string) {
    for _, name := range names {
        fmt.Printf("%s %s\n", prefix, name)
    }
}

func main() {
    greet("Hello", "Alice", "Bob", "Charlie")
    // prints:
    // Hello Alice
    // Hello Bob
    // Hello Charlie
}
```

### Internal implementation

Inside the function, variadic parameters are handled as a slice, which means all of the slice's features and methods are available.

#### Example: accessing variadic arguments

```go
package main

import "fmt"

func printDetails(details ...string) {
    fmt.Println("Number of details:", len(details))
    for i, detail := range details {
        fmt.Printf("Detail %d: %s\n", i+1, detail)
    }
}

func main() {
    printDetails("Name: Alice", "Age: 30", "Country: Wonderland")
    // prints:
    // Number of details: 3
    // Detail 1: Name: Alice
    // Detail 2: Age: 30
    // Detail 3: Country: Wonderland
}
```

`details` is just a slice: use `len` for its length, and indexing to access a single element.

### Summary

Variadic parameters solve the problem of an indefinite number of arguments: at definition time, put `...` in front of the type; at call time, you can pass values directly, or use `slice...` to expand a slice into the call; inside the function you get a slice. There is only one restriction: it must be the last item in the parameter list.

## References

- [Language Spec · Function declarations](https://go.dev/ref/spec#Function_declarations)
- [Language Spec · Calls](https://go.dev/ref/spec#Calls)
- [Effective Go · Functions](https://go.dev/doc/effective_go#functions)
- [Language Spec · Function types (variadic)](https://go.dev/ref/spec#Function_types)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Arguments](/func/Arguments.md)
- [DefineAndCall](/func/DefineAndCall.md)
- [FuncValue](/func/FuncValue.md)
- [History](/func/History.md)
- [InnerFunc](/func/InnerFunc.md)
- [MultipleReturnValues](/func/MultipleReturnValues.md)
- [RecursiveFunction](/func/RecursiveFunction.md)
- [glossary](/glossary.md)
