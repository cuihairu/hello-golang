In Go, the `byte` type is an alias for `uint8`, used to represent an 8-bit unsigned integer with a range of 0 to 255. The `byte` type is typically used to handle and manipulate raw byte data, especially in file I/O and network I/O.

### Declaration and Initialization

You can declare and initialize a `byte` variable just like other basic types:

```go
func main() {
    var b byte = 255
    fmt.Println(b)  // prints: 255

    b2 := byte(100)
    fmt.Println(b2) // prints: 100
}
```

### Arrays and Slices of the `byte` Type

In practice, the `byte` type typically appears as arrays or slices, used to represent a sequence of bytes:

```go
data := []byte{72, 101, 108, 108, 111}
fmt.Println(data)        // prints: [72 101 108 108 111]
fmt.Println(string(data)) // prints: Hello
```

### Converting Between Strings and Bytes

In Go, you can conveniently convert between `string` and `[]byte` in both directions:

```go
// convert string to []byte
s := "Hello"
b := []byte(s)
fmt.Println(b)  // prints: [72 101 108 108 111]

// convert []byte to string
s2 := string(b)
fmt.Println(s2) // prints: Hello
```

Going back and forth between text and binary data relies on exactly this pair of conversions.

### Reading and Writing Files

The `byte` type is very common in file I/O operations. For example, reading and writing files typically uses `[]byte`:

```go
import (
    "fmt"
    "io/ioutil"
    "log"
)

func main() {
    // write to the file
    data := []byte("Hello, World!")
    err := ioutil.WriteFile("example.txt", data, 0644)
    if err != nil {
        log.Fatal(err)
    }

    // read the file
    readData, err := ioutil.ReadFile("example.txt")
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(string(readData))  // prints: Hello, World!
}
```

### Network Communication

In network communication, the `byte` type is also widely used to represent transmitted data. For example, when making a TCP connection with the `net` package, read and write operations on data are typically based on `[]byte`:

```go
import (
    "fmt"
    "net"
    "log"
)

func main() {
    conn, err := net.Dial("tcp", "example.com:80")
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    // send the request
    request := "GET / HTTP/1.0\r\n\r\n"
    _, err = conn.Write([]byte(request))
    if err != nil {
        log.Fatal(err)
    }

    // read the response
    buffer := make([]byte, 1024)
    n, err := conn.Read(buffer)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(string(buffer[:n]))
}
```

### String Processing

When you take a single byte out of a string by index, what you get is a `byte`:

```go
s := "Hello"
for i := 0; i < len(s); i++ {
    fmt.Printf("Character: %c, Byte: %d\n", s[i], s[i])
}
// prints:
// Character: H, Byte: 72
// Character: e, Byte: 101
// Character: l, Byte: 108
// Character: l, Byte: 108
// Character: o, Byte: 111
```

### Notes

1. **Immutability**: although `byte` is mutable, strings in Go are immutable. So converting a `string` to `[]byte` lets you operate on the string's contents, but you need to create a new string afterwards.
2. **UTF-8 encoding**: the `byte` type handles raw byte data; for multi-byte characters (such as UTF-8 encoded Unicode characters), you need to pay special attention to the integrity of characters.

File I/O, network I/O, and processing strings byte by byte — everywhere you turn you run into `byte`. Keep one thing in mind when using it: it is just an 8-bit unsigned number, and character-level semantics (UTF-8 decoding) have to come from `rune` and the methods of `string`.

## References

- [Language Specification · Types](https://go.dev/ref/spec#Types)
- [Language Specification · Numeric Types](https://go.dev/ref/spec#Numeric_types)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [Bool](/type/Bool.md)
- [Complex](/type/Complex.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Bool](/type/Bool.md)
- [Complex](/type/Complex.md)
