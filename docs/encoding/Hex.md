# Hex encoding

Hex (hexadecimal) encoding represents binary data as a hexadecimal string. Each byte is expressed with two hex characters (`0-9`, `a-f`), so the encoded length is twice the original. Hex encoding is mainly used for debugging, data display, and binary representation in protocols — for example, printing memory contents, or showing hash values and digests.

The Go standard library `encoding/hex` provides Hex encoding and decoding.

## Basic usage

`hex.EncodeToString` encodes a byte slice into a hex string, and `hex.DecodeString` does the reverse:

```go
package main

import (
	"encoding/hex"
	"fmt"
)

func main() {
	data := []byte("Hello, Go!")

	// encode as a hex string
	encoded := hex.EncodeToString(data)
	fmt.Println("编码结果:", encoded)

	// decode back to the original data
	decoded, err := hex.DecodeString(encoded)
	if err != nil {
		fmt.Println("解码失败:", err)
		return
	}
	fmt.Println("解码结果:", string(decoded))
}
```

Output:

```
编码结果: 48656c6c6f2c20476f21
解码结果: Hello, Go!
```

Note that the encoded result uses lowercase letters by default. If you need uppercase, call `strings.ToUpper` on the result, or build it byte by byte with `fmt.Sprintf("%02X", b)`.

## Streaming encoding and decoding

For larger data, use the streaming interfaces that implement `io.Reader` / `io.Writer`:

```go
package main

import (
	"bytes"
	"encoding/hex"
	"fmt"
	"io"
	"strings"
)

func main() {
	// streaming encoding: bytes written to the encoder are written to buf in hex form
	var buf bytes.Buffer
	enc := hex.NewEncoder(&buf)
	if _, err := enc.Write([]byte("stream data")); err != nil {
		fmt.Println("编码失败:", err)
		return
	}
	fmt.Println("流式编码:", buf.String())

	// streaming decoding: reconstruct the original bytes from hex text
	dec := hex.NewDecoder(strings.NewReader(buf.String()))
	out, err := io.ReadAll(dec)
	if err != nil {
		fmt.Println("解码失败:", err)
		return
	}
	fmt.Println("流式解码:", string(out))
}
```

`hex.NewEncoder(w io.Writer) io.Writer` writes bytes written into it to `w` in hex form; `hex.NewDecoder(r io.Reader) io.Reader` reads hex text from `r` and restores it to bytes.

## Error handling on decode

`hex.DecodeString` requires the input length to be even and to contain only valid hex characters, otherwise it returns `hex.InvalidByteError` or a length error:

```go
package main

import (
	"encoding/hex"
	"fmt"
)

func main() {
	if _, err := hex.DecodeString("abc"); err != nil {
		fmt.Println("长度错误:", err) // encoded length must be even
	}
	if _, err := hex.DecodeString("zz"); err != nil {
		fmt.Printf("非法字符: %v\n", err)
	}
}
```

## Comparison with Base64

- Hex expands each byte into exactly 2 characters, so data grows by 100%; Base64 grows by about 33% on average and is more space-efficient.
- Hex has a simpler character set and is more readable, so it is commonly used in logs, debugging, and hash value display; Base64 is better suited for carrying larger binary payloads inside text protocols.
- Neither is encryption — both are only encoding, and neither protects data confidentiality.

## Summary

Hex is the least-effort way to represent binary as text. `encoding/hex`'s `EncodeToString` / `DecodeString` handle one-shot conversion, and the streaming `NewEncoder` / `NewDecoder` handle read-as-you-go conversion. Reach for Hex first when you need to display or debug binary content; if you need to carry a large binary payload over a text protocol, switch to Base64 to cut the size.

## References

- [encoding series standard library (json as an example)](https://pkg.go.dev/encoding/json)
- [encoding/hex standard library](https://pkg.go.dev/encoding/hex)


## Sibling pages

- [JsonV2](/encoding/JsonV2.md)
- [Base64](/encoding/Base64.md)
- [Binary](/encoding/Binary.md)
- [Gob](/encoding/Gob.md)
- [Ini](/encoding/Ini.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Gob](/encoding/Gob.md)
- [Ini](/encoding/Ini.md)
