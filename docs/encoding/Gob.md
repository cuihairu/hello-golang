# Gob encoding

Gob (Go binary) is a binary serialization format specific to Go, provided by the standard library `encoding/gob`. It can encode Go data structures into a compact binary stream and decode them back into values of the same structure on the other end. It is commonly used for RPC communication between Go programs and for data persistence. Compared with text formats such as JSON and XML, Gob has a smaller size, faster encoding and decoding, and natively supports Go types such as structs, slices, maps, and interfaces, but it only applies to Go-language environments.

## Basic usage

Use `gob.NewEncoder` to encode and `gob.NewDecoder` to decode. Both operate on an `io.Writer` / `io.Reader`:

```go
package main

import (
	"bytes"
	"encoding/gob"
	"fmt"
	"log"
)

type Address struct {
	City    string
	ZipCode string
}

type Person struct {
	Name    string
	Age     int
	Emails  []string
	Address Address
}

func main() {
	p := Person{
		Name:    "Alice",
		Age:     30,
		Emails:  []string{"alice@example.com", "a@work.com"},
		Address: Address{City: "Beijing", ZipCode: "100000"},
	}

	// encode to an in-memory buffer
	var buf bytes.Buffer
	if err := gob.NewEncoder(&buf).Encode(p); err != nil {
		log.Fatal("encoding failed:", err)
	}
	fmt.Printf("bytes after encoding: %d\n", buf.Len())

	// decode back to the struct
	var got Person
	if err := gob.NewDecoder(&buf).Decode(&got); err != nil {
		log.Fatal("decoding failed:", err)
	}
	fmt.Printf("%+v\n", got)
}
```

## Serializing to a file

Writing a struct to a file and then recovering it from the file is the simplest way to persist data:

```go
package main

import (
	"encoding/gob"
	"fmt"
	"log"
	"os"
)

type Config struct {
	Theme    string
	FontSize int
	Tags     []string
}

func main() {
	cfg := Config{Theme: "dark", FontSize: 14, Tags: []string{"go", "dev"}}

	// save
	f, err := os.Create("config.gob")
	if err != nil {
		log.Fatal(err)
	}
	if err := gob.NewEncoder(f).Encode(cfg); err != nil {
		f.Close()
		log.Fatal(err)
	}
	f.Close()

	// read
	r, err := os.Open("config.gob")
	if err != nil {
		log.Fatal(err)
	}
	defer r.Close()

	var loaded Config
	if err := gob.NewDecoder(r).Decode(&loaded); err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%+v\n", loaded)
}
```

## Registering concrete types for an interface

When the value being encoded is an interface type, gob transfers the concrete dynamic type, so you must use `gob.Register` to register all possible concrete types before encoding; otherwise decoding will report `gob: name not registered for interface`. Note that on the encoding side you must pass the interface variable by pointer (`Encode(&m)`); passing the concrete value directly will not receive an interface envelope, and the decoding end will report `local interface type ... can only be decoded from remote interface type`:

```go
package main

import (
	"bytes"
	"encoding/gob"
	"fmt"
	"log"
)

type Message interface{ Body() string }

type Text struct{ Content string }

func (t Text) Body() string { return t.Content }

type Image struct{ URL string }

func (i Image) Body() string { return "image: " + i.URL }

func main() {
	gob.Register(Text{})
	gob.Register(Image{})

	var buf bytes.Buffer
	enc := gob.NewEncoder(&buf)
	var m1 Message = Text{Content: "hello"}
	if err := enc.Encode(&m1); err != nil {
		log.Fatal(err)
	}
	var m2 Message = Image{URL: "https://example.com/a.png"}
	if err := enc.Encode(&m2); err != nil {
		log.Fatal(err)
	}

	dec := gob.NewDecoder(&buf)
	for i := 0; i < 2; i++ {
		var m Message
		if err := dec.Decode(&m); err != nil {
			log.Fatal(err)
		}
		fmt.Println(m.Body())
	}
}
```

Runtime output:

```text
hello
image: https://example.com/a.png
```

## Usage notes

- **Fields must be exported**: gob only encodes exported fields (uppercase first letter); unexported fields are ignored and remain at their zero value after decoding.
- **Struct tags**: The `gob:"name"` tag is supported to rename a field, and `gob:"-"` means to skip that field.
- **Zero-value omission**: gob omits fields whose value is the zero value to reduce size. Therefore unexported or zero-value fields will automatically be restored to the zero value on the decoding end, which requires the type structures on both encoding and decoding sides to be compatible.
- **Types on both ends must match**: Field names and types need to be consistent. Extra or missing fields are handled compatibly per gob's rules, but a type mismatch will return an error.
- **Not cross-language**: gob is a Go-only format. When you need to interact with general formats such as JSON or Protobuf, choose the latter.

## Summary

`encoding/gob` is a self-describing binary serialization format. For ordinary scenarios, use `Encode` / `Decode` directly; when interfaces are involved, use `gob.Register` to register the concrete types. It is suitable for internal communication between Go services and for local persistence. For cross-language scenarios, switch to JSON, XML, or Protobuf.

## References

- [encoding standard library series (json as an example)](https://pkg.go.dev/encoding/json)
- [encoding/gob standard library](https://pkg.go.dev/encoding/gob)


## Sibling pages

- [JsonV2](/encoding/JsonV2.md)
- [Base64](/encoding/Base64.md)
- [Binary](/encoding/Binary.md)
- [Formats](/encoding/Formats.md)
- [Hex](/encoding/Hex.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Formats](/encoding/Formats.md)
- [Hex](/encoding/Hex.md)
