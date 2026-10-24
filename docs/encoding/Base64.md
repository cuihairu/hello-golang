### Base64 encoding

Base64 is an encoding scheme that converts binary data into ASCII strings. It is widely used in scenarios where binary data needs to be represented as text, such as in email, URLs, and data transmission. Base64 encoding works by converting every three bytes of binary data into four ASCII characters.

#### 1. How Base64 encoding works

The basic principle of Base64 encoding includes the following steps:

1. **Split the data into three-byte blocks**

   - Base64 encoding processes data in units of three bytes. If the input length is not a multiple of three, padding characters (`=`) are appended at the end to make it a multiple of three.

2. **Convert each three-byte block into 24 bits of binary data**

   - Each three-byte block totals 24 bits of binary data (3 × 8 = 24).

3. **Split the 24 bits of binary data into 4 blocks of 6 bits**

   - Each 6-bit block represents one Base64 character.

4. **Map each 6-bit block to the Base64 character set**

   - Base64 uses a fixed character set that includes uppercase letters (A-Z), lowercase letters (a-z), digits (0-9), plus sign (`+`), and slash (`/`).

5. **Handle blocks shorter than three bytes**

   - If the input length is not a multiple of three, one or two padding characters (`=`) are appended at the end to make up the required byte count.

#### 2. Base64 encoding example

Walking through encoding `"Man"`:

**Original data (ASCII)**:
```
"Man"
```

**Convert to binary**:
```
M  a  n
01001101 01100001 01101110
```

**Split into 6-bit blocks**:
```
010011 010110 000101 101110
```

**Map to the Base64 character set** (look up the decimal value of each 6-bit block):
```
010011 = 19 → T
010110 = 22 → W
000101 =  5 → F
101110 = 46 → u
```

**Result (Base64 encoded)**:
```
TWFu
```

#### 3. Base64 character set

The Base64 character set is as follows:
```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/
```

- `A-Z`: 0-25
- `a-z`: 26-51
- `0-9`: 52-61
- `+`: 62
- `/`: 63

#### 4. Base64 decoding

Base64 decoding is the reverse of Base64 encoding:

1. **Convert Base64 characters into 6-bit binary blocks**

   - Use the Base64 character set to map each character to its corresponding 6-bit binary data.

2. **Combine the 6-bit binary blocks into 24 bits of binary data**

   - Reassemble the 6-bit blocks into 24-bit binary data blocks.

3. **Split the 24 bits of binary data into 3 bytes**

   - Split the 24 bits of binary data into 3 bytes of 8 bits each.

4. **Handle padding characters**

   - If the Base64 encoding contains padding characters (`=`), ignore them during decoding.

#### 5. Base64 encoding and decoding examples (Go)

Go's `encoding/base64` package provides encoding and decoding functions.

**Base64 encoding example**:

```go
package main

import (
    "encoding/base64"
    "fmt"
)

func main() {
    // original data
    data := "Man"
    
    // encode as Base64
    encoded := base64.StdEncoding.EncodeToString([]byte(data))
    fmt.Println("Base64 编码:", encoded)
}
```

**Base64 decoding example**:

```go
package main

import (
    "encoding/base64"
    "fmt"
)

func main() {
    // Base64 encoded data
    encoded := "TWFu"
    
    // decode back to original data
    decoded, err := base64.StdEncoding.DecodeString(encoded)
    if err != nil {
        fmt.Println("解码错误:", err)
        return
    }
    fmt.Println("原始数据:", string(decoded))
}
```

#### 6. Base64 applications

1. **Data transmission**

   - Base64 encoding is commonly used to convert binary data into ASCII strings for easy transmission over text channels, such as email and HTTP requests.

2. **URL encoding**

   - Base64 encoding is used to embed binary data into URLs, ensuring the data is not accidentally modified or lost.

3. **Data storage**

   - Base64 encoding is used to store binary data in text-format files, such as configuration files and log files.

4. **Encryption and signing**

   - Base64 encoding is used to convert encrypted data and digital signatures into text format for easier storage and transmission.

#### 7. Pros and cons of Base64

**Pros**:

1. **Text-friendly**: Converts binary data into ASCII strings, making it easy to handle and transmit in text environments.
2. **Widely supported**: Base64 encoding is broadly supported and works across many programming languages and platforms.

**Cons**:

1. **Data expansion**: Base64 encoding inflates data by roughly 33% in size, adding overhead to storage and transmission.
2. **Not encryption**: Base64 encoding is only for data encoding and provides no encryption.

#### Summary

Base64 takes every 3 bytes, turns them into 4 six-bit groups, and maps those groups to ASCII characters via a lookup table. It costs about 33% extra size in exchange for letting binary data travel over text-only channels like email and HTTP. In Go, encoding is `base64.StdEncoding.EncodeToString` and decoding is `DecodeString`.

## References

- [encoding series standard library (json as an example)](https://pkg.go.dev/encoding/json)
- [encoding/base64 standard library](https://pkg.go.dev/encoding/base64)

## Sibling pages

- [JsonV2](/encoding/JsonV2.md)
- [Binary](/encoding/Binary.md)
- [CSV](/encoding/CSV.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Binary](/encoding/Binary.md)
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
