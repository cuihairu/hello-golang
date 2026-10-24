
> Perspective: this page collects assignment patterns by variable-usage scenario; for the operator taxonomy (`=`, `+=`, etc.) see [assignment operator notes](/zh/operator/Assignment.md).
In Go, assignment hands a value to a variable. There are ten common forms.

### 1. Simple assignment

This is the most basic assignment pattern, used to assign a value to a variable.

```go
var x int
x = 10
```

### 2. Declare and assign

You can assign a value at the same time you declare the variable.

```go
var x int = 10
// or use type inference
var y = 20
```

### 3. Short variable declaration (:=)

Inside a function, you can use `:=` for a short variable declaration and assignment.

```go
x := 10
y, z := 20, 30
```

### 4. Multiple assignment

You can assign to multiple variables at once, or swap the values of variables.

```go
a, b, c := 1, 2, 3
a, b = b, a  // swap the values of a and b
```

### 5. Blank identifier (_)

The blank identifier `_` can be used to discard values you don't need in an assignment; it is commonly used to ignore unwanted values when a function returns several.

```go
_, b := someFunction()
_, x, y := anotherFunction()
```

### 6. Pointer assignment

You can assign to or read a variable's value through a pointer.

```go
var x int = 10
var p *int = &x // p points to the address of x
*p = 20         // modify the value p points to; x also becomes 20
```

### 7. Struct assignment

You can assign to a struct's fields, or assign a whole struct at once.

```go
type Person struct {
    Name string
    Age  int
}

// field assignment
var p Person
p.Name = "Alice"
p.Age = 30

// struct assignment
p = Person{"Bob", 25}
```

### 8. Slice assignment

A slice can be assigned through its index, or directly through a slice literal.

```go
var s []int
s = make([]int, 5)
s[0] = 10

// slice literal assignment
s = []int{1, 2, 3, 4, 5}
```

### 9. Map assignment

A map can be assigned through its key.

```go
m := make(map[string]int)
m["a"] = 10
m["b"] = 20

// map literal assignment
m = map[string]int{"a": 10, "b": 20}
```

### 10. Assigning function return values

A function can return multiple values, which you can assign directly to multiple variables.

```go
func someFunction() (int, int) {
    return 1, 2
}

a, b := someFunction()
```

### Example code

```go
package main

import "fmt"

func someFunction() (int, int) {
    return 1, 2
}

type Person struct {
    Name string
    Age  int
}

func main() {
    // simple assignment
    var x int
    x = 10
    fmt.Println(x)

    // declare and assign
    var y int = 20
    var z = 30
    fmt.Println(y, z)

    // short variable declaration
    a := 40
    b, c := 50, 60
    fmt.Println(a, b, c)

    // multiple assignment
    d, e, f := 1, 2, 3
    d, e = e, d // swap the values of d and e
    fmt.Println(d, e, f)

    // blank identifier
    _, g := someFunction()
    h, i := someFunction()
    fmt.Println(g, h, i)

    // pointer assignment
    var j int = 70
    var p *int = &j
    *p = 80
    fmt.Println(j)

    // struct assignment
    var person Person
    person.Name = "Alice"
    person.Age = 30
    fmt.Println(person)

    person = Person{"Bob", 25}
    fmt.Println(person)

    // slice assignment
    var s []int
    s = make([]int, 5)
    s[0] = 10
    fmt.Println(s)

    s = []int{1, 2, 3, 4, 5}
    fmt.Println(s)

    // map assignment
    m := make(map[string]int)
    m["a"] = 10
    m["b"] = 20
    fmt.Println(m)

    m = map[string]int{"a": 10, "b": 20}
    fmt.Println(m)

    // assigning function return values
    k, l := someFunction()
    fmt.Println(k, l)
}
```

### Summary

`:=` is a short declaration inside a function, while `var` lets you declare first and assign later; `_` throws away return values you don't need; `a, b = b, a` swaps in a single step; and structs, slices, and maps can all be assigned as a whole, as well as field-by-field, by index, or by key.

## References

- [Language Spec · Variable declarations](https://go.dev/ref/spec#Variable_declarations)
- [Effective Go · Variables](https://go.dev/doc/effective_go#variables)
- [Language Spec · Assignment](https://go.dev/ref/spec#Assignment)

## Sibling pages

- [Segment](/var/Segment.md)
- [VarAndInit](/var/VarAndInit.md)
- [ScopeAndLifetime](/var/ScopeAndLifetime.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [ScopeAndLifetime](/var/ScopeAndLifetime.md)
- [Variable](/var/Variable.md)
