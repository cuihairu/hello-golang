# Passing arguments

How Go passes arguments depends on the type: basic types are passed by copy, pointers pass an address, and slices and maps pass a handle to the underlying structure.

## 1. Passing by value

The most basic passing mechanism in Go is **passing by value**: the function receives a copy of the argument, so modifying the argument inside the function does not affect the original variable.

### Basic example

```go
package main

import "fmt"

func changeValue(x int) {
    x = 100
}

func main() {
    num := 5
    changeValue(num)
    fmt.Println("num:", num) // prints: num: 5, unchanged
}
```

### Key points
- **Integers, floating-point, booleans, strings** and other basic types are always passed by value
- Modifications inside the function do not affect the outer variable
- Every function call allocates a new stack frame, and the copy exists independently

## 2. Passing by pointer

To be able to modify the original variable inside a function, use **passing by pointer**. By passing a pointer, the function can access and modify the original value the pointer points to.

### Basic example

```go
package main

import "fmt"

func changePointer(x *int) {
    *x = 100
}

func main() {
    num := 5
    changePointer(&num)
    fmt.Println("num:", num) // prints: num: 100, modified
}
```

### Key points
- Use `&var` to get a variable's address as the argument
- Inside the function, use `*ptr` to access and modify the original value
- For large objects or cases where the original value needs to be modified, passing by pointer is recommended

## 3. The "passing behavior" of slices and maps

In Go, **slices** and **maps** are also passed by value, but the value passed is a **handle to the underlying data structure**, so modifications to a slice or map inside a function are reflected on the original.

### Slice passing example

```go
package main

import "fmt"

func modifyElements(s []int) {
    s[0] = 100 // modifying the element reflects back to the original slice
}

func appendValue(s []int) []int {
    return append(s, 4) // append may create a new underlying array, so the new slice must be returned
}

func main() {
    // approach 1: modify the element (no reallocation), no return value needed
    s1 := []int{1, 2, 3}
    modifyElements(s1)
    fmt.Println("after modifying the element:", s1) // prints: after modifying the element: [100 2 3]

    // approach 2: append may reallocate the underlying array, so the new slice must be returned
    s2 := []int{1, 2, 3}
    s3 := appendValue(s2)
    fmt.Println("original slice after append:", s2) // prints: original slice after append: [1 2 3]
    fmt.Println("new slice after append:", s3) // prints: new slice after append: [1 2 3 4]
}
```

### Map passing example

```go
package main

import "fmt"

func modifyMap(m map[string]int) {
    m["key"] = 100 // the modification reflects back on the original map
    // or add a new key
    m["new_key"] = 200
}

func main() {
    original := make(map[string]int)
    original["existing"] = 50
    modifyMap(original)
    fmt.Println("map:", original) // prints: map: map[existing:50 key:100 new_key:200]
}
```

### Key points
- **The values of slices and maps contain a reference to the underlying data structure**
- **Modifying slice elements or map contents** affects the original
- **Reassigning a slice** (e.g. `s = append(s, ...)`) may create a new underlying array, so the new slice reference must be returned
- **Key-value modifications on a map** are always reflected on the original map

## 4. Passing structs

Structs can be passed by value or by pointer. Passing by value copies the entire struct, while passing by pointer copies only the pointer (8 or 16 bytes).

### Passing a struct by value

```go
package main

import "fmt"

type Person struct {
    Name string
    Age  int
}

func setName(p Person) {
    p.Name = "Changed" // only the copy is modified, the original stays the same
}

func main() {
    p := Person{Name: "Alice"}
    setName(p)
    fmt.Println("Name:", p.Name) // prints: Name: Alice, unchanged
}
```

### Passing a struct by pointer

```go
package main

import "fmt"

type Person struct {
    Name string
    Age  int
}

func setNamePtr(p *Person) {
    p.Name = "Changed" // modify the original struct
}

func main() {
    p := Person{Name: "Alice"}
    setNamePtr(&p)
    fmt.Println("Name:", p.Name) // prints: Name: Changed, modified
}
```

### Choosing between them
- **Small structs** (e.g. with 1-2 int/string fields) can use **passing by value** to avoid the memory-copy overhead
- Use **passing by pointer** for **large structs** or when **the struct members need to be modified inside the function**
- Many functions in the Go standard library accept pointers

## 5. Recommended best practices

1. **For basic types** (int, float, bool, string): use passing by value, which is the default
2. **For large types or when modification is needed**: use passing by pointer, `*Type`
3. **For slices and maps**:
   - If you only need to modify the contents (no reallocation), pass directly and the modifications take effect
   - If reallocation or a return is needed, return the new slice/map
4. **Documentation comments**: clearly state in the function signature whether the argument is a value or a pointer, to help callers understand the behavior
5. **Consistency**: keep the same passing convention across related functions of the same type

When you are unsure which to use, look at two things: whether the original value needs to be modified inside the function, and how big the struct is. Modify or very large, use a pointer; otherwise passing by value is fine.

## References

- [Language Spec · Function declarations](https://go.dev/ref/spec#Function_declarations)
- [Language Spec · Calls](https://go.dev/ref/spec#Calls)
- [Effective Go · Functions](https://go.dev/doc/effective_go#functions)
- [Language Spec · Order of evaluation](https://go.dev/ref/spec#Order_of_evaluation)

## Sibling pages

- [AnonymousFunc](/func/AnonymousFunc.md)
- [Defer](/func/Defer.md)
- [VariadicParameters](/func/VariadicParameters.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [AnonymousFunc](/func/AnonymousFunc.md)
