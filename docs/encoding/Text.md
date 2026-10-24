###  Text Encoding

Text encoding solves the same problem: turn characters into byte sequences so they are easy to store and easy to transmit. Here I compare three encodings (ASCII, UTF-8, UTF-16) and how the Go standard library handles each.

#### 2.1 ASCII Encoding

**ASCII (American Standard Code for Information Interchange)** is an early character encoding standard that uses 7 bits to represent a character and defines 128 characters in total, including the basic Latin letters, digits, punctuation, and some control characters. Later extended character sets (such as Latin-1 and Windows-1252) use 8 bits to represent 256 characters, but they are not part of standard ASCII. ASCII encoding is simple and long-established, but its support for non-English characters is limited.

**Example code**:
```go
package main

import "fmt"

func main() {
    // ASCII encoding example
    text := "Hello, World!"
    fmt.Println("Text:", text)
}
```

In Go, strings are UTF-8 encoded by default, but ASCII strings can be handled too, because UTF-8 is backward compatible with ASCII.

#### 2.2 UTF-8 Encoding

**UTF-8 (8-bit Unicode Transformation Format)** is a variable-length encoding that uses 1 to 4 bytes to represent a Unicode character. UTF-8 is ASCII-compatible and supports characters from most languages around the world, making it the most commonly used text encoding in modern applications.

**Example code**:
```go
package main

import (
    "fmt"
    "unicode/utf8"
)

func main() {
    // UTF-8 encoding example
    text := "你好，世界！" // Chinese characters

    fmt.Println("Text:", text)
    fmt.Printf("Length: %d bytes\n", len(text))
    fmt.Printf("Rune count: %d\n", utf8.RuneCountInString(text))

    // iterate over each character (rune) in the string
    for i, c := range text {
        fmt.Printf("Character %d: %c (code point: %U)\n", i, c, c)
    }
}
```

In the example above, `utf8.RuneCountInString` counts the characters in a UTF-8 string, while `range` iterates over each character (rune) in the string.

#### 2.3 UTF-16 Encoding

**UTF-16 (16-bit Unicode Transformation Format)** is another Unicode encoding that uses 16 bits (two bytes) or 32 bits (four bytes) to represent a character. UTF-16 can represent all Unicode characters, but some characters use two 16-bit units (a surrogate pair).

In Go, UTF-16 encoding and decoding usually involves the `unicode/utf16` package. Here is an example of handling UTF-16:

**Example code**:
```go
package main

import (
    "fmt"
    "unicode/utf16"
)

func main() {
    // UTF-16 encoding example
    text := "こんにちは世界" // Japanese characters

    // convert UTF-8 to UTF-16
    utf16Codes := utf16.Encode([]rune(text))
    fmt.Println("UTF-16 Encoded:", utf16Codes)

    // convert UTF-16 back to UTF-8
    utf8Chars := utf16.Decode(utf16Codes)
    utf8Text := string(utf8Chars)
    fmt.Println("UTF-8 Decoded:", utf8Text)
}
```

In the example above, `utf16.Encode` and `utf16.Decode` convert between UTF-8 and UTF-16.

#### Summary

Here are the three main text encodings:

- **ASCII encoding**: the earliest character encoding standard, mainly for English text.
- **UTF-8 encoding**: a modern variable-length encoding, ASCII-compatible, and it supports characters from many languages.
- **UTF-16 encoding**: represents a character with 16 bits (two bytes) or 32 bits (four bytes, via surrogate pairs), supports all Unicode characters, and is commonly used on platforms such as Windows and Java.

In Go you meet all three at once: source code and string literals are already UTF-8, `len` counts bytes while `utf8.RuneCountInString` counts characters, and when you hit a UTF-16 boundary such as the Windows API or Java you switch with `unicode/utf16`. Remember that "bytes and characters are not the same thing" and you avoid most encoding pitfalls.

## References

- [encoding standard library family (json as the example)](https://pkg.go.dev/encoding/json)


## Sibling pages

- [JsonV2](/encoding/JsonV2.md)
- [Base64](/encoding/Base64.md)
- [Binary](/encoding/Binary.md)
- [TOML](/encoding/TOML.md)
- [Voice](/encoding/Voice.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [TOML](/encoding/TOML.md)
- [Voice](/encoding/Voice.md)
