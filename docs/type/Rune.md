In Go, the `rune` type is an alias for `int32`, representing a 32-bit signed integer. The `rune` type is specifically used to represent Unicode code points, which makes handling multi-byte characters easier. Strings in Go are UTF-8 encoded, and `rune` helps process Unicode characters correctly.

### Declaration and initialization

You can declare and initialize a `rune` variable in the following ways:

```go
func main() {
    var r rune           // declared but not initialized, default value is 0
    var r1 rune = 'A'    // declared and initialized to the character 'A'
    r2 := '世'           // short declaration, initialized to the character '世'
    fmt.Println(r, r1, r2)
}
```

### Usage and examples

#### Representing characters

The `rune` type is commonly used to represent characters, including ASCII and non-ASCII characters:

```go
func main() {
    var char rune = 'A'
    fmt.Println(char)          // prints: 65 (the Unicode code point of 'A')
    fmt.Printf("%c\n", char)   // prints: A

    var chineseChar rune = '世'
    fmt.Println(chineseChar)          // prints: 19990 (the Unicode code point of '世')
    fmt.Printf("%c\n", chineseChar)   // prints: 世
}
```

#### Unicode characters in strings

In Go, strings are UTF-8 encoded, so a single character can occupy multiple bytes. Using `rune` lets you handle these characters correctly:

```go
s := "Hello, 世界"
for i, r := range s {
    fmt.Printf("Index: %d, Character: %c, Unicode: %U\n", i, r, r)
}
```

Output:
```
Index: 0, Character: H, Unicode: U+0048
Index: 1, Character: e, Unicode: U+0065
Index: 2, Character: l, Unicode: U+006C
Index: 3, Character: l, Unicode: U+006C
Index: 4, Character: o, Unicode: U+006F
Index: 5, Character: ,, Unicode: U+002C
Index: 6, Character:  , Unicode: U+0020
Index: 7, Character: 世, Unicode: U+4E16
Index: 10, Character: 界, Unicode: U+754C
```

### Converting between strings and `[]rune`

You can convert a string to `[]rune` so that each character can be processed independently:

```go
s := "Hello, 世界"
runes := []rune(s)
for _, r := range runes {
    fmt.Printf("%c ", r)
}
// prints: H e l l o ,   世 界
```

You can also convert `[]rune` back to a string:

```go
runes := []rune("Hello, 世界")
s2 := string(runes)
fmt.Println(s2)  // prints: Hello, 世界
```

### Operations on `rune`

`rune` is an alias for `int32`, so all integer arithmetic works on it:

```go
r := 'A'
fmt.Println(r + 1)        // prints: 66
fmt.Printf("%c\n", r+1)   // prints: B
```

### Notes

1. **Multi-byte characters**: When handling multi-byte characters, using `rune` directly avoids character-truncation issues.
2. **Indexing and slicing**: String indexing operates on bytes; to get characters, convert the string to `[]rune` first.

### Example code

Here is a complete example showing the declaration, initialization, manipulation, and string processing of `rune`:

```go
package main

import (
    "fmt"
)

func main() {
    // declaration and initialization
    var r rune = 'A'
    fmt.Println(r)          // prints: 65
    fmt.Printf("%c\n", r)   // prints: A

    var chineseChar rune = '世'
    fmt.Println(chineseChar)          // prints: 19990
    fmt.Printf("%c\n", chineseChar)   // prints: 世

    // Unicode characters in a string
    s := "Hello, 世界"
    for i, r := range s {
        fmt.Printf("Index: %d, Character: %c, Unicode: %U\n", i, r, r)
    }

    // converting between string and []rune
    runes := []rune(s)
    for _, r := range runes {
        fmt.Printf("%c ", r)
    }
    fmt.Println()

    s2 := string(runes)
    fmt.Println(s2)  // prints: Hello, 世界

    // rune arithmetic
    r2 := 'A'
    fmt.Println(r2 + 1)        // prints: 66
    fmt.Printf("%c\n", r2+1)   // prints: B
}
```

`rune` is `int32`, so it can be printed as a character (`%c`) and also used in integer arithmetic. Indexing a string by bytes cuts through multi-byte characters; to process it character by character, convert to `[]rune` first.

## References

- [Language spec · Types](https://go.dev/ref/spec#Types)
- [Official blog · Strings, bytes, runes and characters in Go](https://go.dev/blog/strings)
- [unicode/utf8 standard library](https://pkg.go.dev/unicode/utf8)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [Ring](/type/Ring.md)
- [Slice](/type/Slice.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Ring](/type/Ring.md)
