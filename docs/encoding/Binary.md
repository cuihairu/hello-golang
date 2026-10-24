### Binary Encoding

Binary encoding represents data in binary form and then converts it into other forms for storage and transmission. Common forms are Base64, Hex, and Go's own GOB.

#### 3.1 Base64 Encoding

**Base64** is an encoding that converts binary data into an ASCII string. By encoding every three bytes of binary data as four ASCII characters, it ensures the data can travel safely in text environments. Base64 encoding is widely used to represent binary data in email and URLs.

**Example code**:
```go
package main

import (
    "encoding/base64"
    "fmt"
)

func main() {
    // Base64 encoding example
    data := []byte("Hello, World!")
    encoded := base64.StdEncoding.EncodeToString(data)
    fmt.Println("Base64 Encoded:", encoded)

    // Base64 decoding example
    decoded, err := base64.StdEncoding.DecodeString(encoded)
    if err != nil {
        fmt.Println("Error decoding Base64:", err)
        return
    }
    fmt.Println("Base64 Decoded:", string(decoded))
}
```

In the example above, `base64.StdEncoding.EncodeToString` encodes byte data into a Base64 string, and `base64.StdEncoding.DecodeString` decodes a Base64 string back into the original byte data.

#### 3.2 Hex Encoding

**Hex (hexadecimal)** encoding represents binary data as a hexadecimal string. Each byte is represented by two hexadecimal characters. This encoding is mainly used for debugging and data representation.

**Example code**:
```go
package main

import (
    "encoding/hex"
    "fmt"
)

func main() {
    // Hex encoding example
    data := []byte("Hello, World!")
    encoded := hex.EncodeToString(data)
    fmt.Println("Hex Encoded:", encoded)

    // Hex decoding example
    decoded, err := hex.DecodeString(encoded)
    if err != nil {
        fmt.Println("Error decoding Hex:", err)
        return
    }
    fmt.Println("Hex Decoded:", string(decoded))
}
```

In the example above, `hex.EncodeToString` encodes byte data into a hexadecimal string, and `hex.DecodeString` decodes a hexadecimal string back into the original byte data.

#### 3.3 GOB Encoding

**GOB** is a Go-specific binary encoding used to encode and decode Go data structures. GOB encoding is well suited to data persistence and network transfer within Go applications. Unlike text encodings such as JSON and XML, GOB is mainly for efficient serialization and deserialization inside Go programs.

**Example code**:
```go
package main

import (
    "bytes"
    "encoding/gob"
    "fmt"
)

// define a data structure
type Person struct {
    Name string
    Age  int
}

func main() {
    // create a Person instance
    p1 := Person{Name: "Alice", Age: 30}

    // encode
    var buffer bytes.Buffer
    encoder := gob.NewEncoder(&buffer)
    err := encoder.Encode(p1)
    if err != nil {
        fmt.Println("Error encoding GOB:", err)
        return
    }
    encodedData := buffer.Bytes()
    fmt.Println("GOB Encoded Data:", encodedData)

    // decode
    var p2 Person
    decoder := gob.NewDecoder(bytes.NewReader(encodedData))
    err = decoder.Decode(&p2)
    if err != nil {
        fmt.Println("Error decoding GOB:", err)
        return
    }
    fmt.Println("GOB Decoded Data:", p2)
}
```

In the example above, `gob.NewEncoder` encodes a Go data structure into GOB format, and `gob.NewDecoder` decodes GOB data back into a Go data structure.

#### Summary

Here are some common binary encodings:

- **Base64 encoding**: encodes binary data as an ASCII string, for transmission and storage in text environments.
- **Hex encoding**: encodes binary data as a hexadecimal string, for debugging and data representation.
- **GOB encoding**: a Go-specific binary encoding for efficiently serializing and deserializing data between Go programs.

Which one to pick depends on where the data is going: Base64 for the text channel, Hex when you check bytes by eye, GOB when Go programs pass structs to each other.

## References

- [encoding standard library family (json as the example)](https://pkg.go.dev/encoding/json)
- [encoding/binary standard library](https://pkg.go.dev/encoding/binary)

## Sibling pages

- [JsonV2](/encoding/JsonV2.md)
- [Base64](/encoding/Base64.md)
- [CSV](/encoding/CSV.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Base64](/encoding/Base64.md)
- [CSV](/encoding/CSV.md)
- [Encoding](/encoding/Encoding.md)
- [Formats](/encoding/Formats.md)
- [Gob](/encoding/Gob.md)
- [Hex](/encoding/Hex.md)
- [Ini](/encoding/Ini.md)
- [JSON](/encoding/JSON.md)
- [TOML](/encoding/TOML.md)
- [Text](/encoding/Text.md)
- [Voice](/encoding/Voice.md)
- [XML](/encoding/XML.md)
