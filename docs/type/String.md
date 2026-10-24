Go's `string` type is the basic data type for representing text. It is immutable — once created it cannot be modified — and it is encoded as UTF-8 internally, so it can hold characters from many languages.

### Declaration and initialization

You can declare and initialize a string in a number of ways:

```go
package main

import "fmt"

func main() {
    var s1 string           // declared but not initialized, default value is the empty string ""
    var s2 string = "Hello" // declared and initialized
    s3 := "World"           // short declaration and initialization
    fmt.Printf("s1: %q, s2: %s, s3: %s\n", s1, s2, s3) // s1: "", s2: Hello, s3: World
}
```

### String concatenation

You can concatenate two strings with the plus (`+`) operator:

```go
s2 := "Hello"
s3 := "World"
greeting := s2 + ", " + s3 + "!"
fmt.Println(greeting)  // prints: Hello, World!
```

### Multi-line strings

Use backticks (`) to declare a multi-line string. A backtick string is not escaped; its contents, including newline characters, are kept as they are:

```go
multiLine := `This is a
multi-line
string.`
fmt.Println(multiLine)
```

### String length

The `len` function returns a string's length, which is the number of bytes, not the number of characters:

```go
greeting := "Hello, World!"
length := len(greeting)
fmt.Println("Length of greeting:", length)  // prints: Length of greeting: 13
```

### String indexing and slicing

You can index into a string to access its bytes (note: bytes, not characters):

```go
greeting := "Hello, World!"
char := greeting[0]
fmt.Println("First character:", string(char))  // prints: First character: H
```

You can use the slice operator to get a substring:

```go
greeting := "Hello, World!"
substring := greeting[0:5]
fmt.Println("Substring:", substring)  // prints: Substring: Hello
```

### String comparison

You can compare strings with the comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`):

```go
s2 := "Hello"
if s2 == "Hello" {
    fmt.Println("s2 is Hello")
}
```

### Common string functions

Go provides many string-processing functions in the `strings` package:

```go
import (
    "fmt"
    "strings"
)

func main() {
    s := "Hello, World!"
    fmt.Println(strings.ToUpper(s))       // to uppercase: HELLO, WORLD!
    fmt.Println(strings.ToLower(s))       // to lowercase: hello, world!
    fmt.Println(strings.Contains(s, "Wo")) // contains: true
    fmt.Println(strings.ReplaceAll(s, "World", "Go")) // replace: Hello, Go!
    fmt.Println(strings.Split(s, ", "))   // split: [Hello World!]
}
```

### Iterating over a string

Use the `range` keyword to iterate over the characters of a string:

```go
s := "Hello"
for i, c := range s {
    fmt.Printf("Index: %d, Character: %c\n", i, c)
}
```

### Notes

1. **Immutability**: a string cannot be modified once it is created. If you need to concatenate strings heavily, use `strings.Builder` or `bytes.Buffer` for better performance.
2. **UTF-8 encoding**: Go strings are UTF-8 encoded, which means a single character can occupy multiple bytes. Be careful handling multi-byte characters when iterating over a string.

### Example code

Here is a complete example showing the declaration, initialization, manipulation, and iteration of a string:

```go
package main

import (
    "fmt"
    "strings"
)

func main() {
    var s1 string
    fmt.Printf("s1: %q\n", s1) // prints: s1: ""
    s2 := "Hello"
    s3 := "World"

    greeting := s2 + ", " + s3 + "!"
    fmt.Println(greeting)  // prints: Hello, World!

    multiLine := `This is a
multi-line
string.`
    fmt.Println(multiLine)

    fmt.Println("Length of greeting:", len(greeting))  // prints: Length of greeting: 13

    fmt.Println("First character:", string(greeting[0]))  // prints: First character: H

    substring := greeting[0:5]
    fmt.Println("Substring:", substring)  // prints: Substring: Hello

    if s2 == "Hello" {
        fmt.Println("s2 is Hello")
    }

    fmt.Println(strings.ToUpper(greeting))       // prints: HELLO, WORLD!
    fmt.Println(strings.ToLower(greeting))       // prints: hello, world!
    fmt.Println(strings.Contains(greeting, "Wo")) // prints: true
    fmt.Println(strings.ReplaceAll(greeting, "World", "Go")) // prints: Hello, Go!
    fmt.Println(strings.Split(greeting, ", "))   // prints: [Hello World!]

    for i, c := range greeting {
        fmt.Printf("Index: %d, Character: %c\n", i, c)
    }
}
```

Running through this example makes three things clear: `len` counts bytes, `range` iterates and yields characters, and the slice `[0:5]` cuts by bytes. When you hit a multi-byte character, these three results diverge.

## References

- [Language spec · Types](https://go.dev/ref/spec#Types)
- [Language spec · String types](https://go.dev/ref/spec#String_types)
- [Official blog · Strings, bytes, runes and characters in Go](https://go.dev/blog/strings)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [Slice](/type/Slice.md)
- [Struct](/type/Struct.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Struct](/type/Struct.md)
