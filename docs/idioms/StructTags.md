In Go, struct tags are a way to attach extra information to struct fields, usually for data serialization and deserialization. For example, struct tags are used extensively in JSON, XML, and database work.

### 1. Basic usage

A struct tag is a backtick-quoted string written after a struct field. The most common use is providing tags for JSON serialization and deserialization.

#### Example: JSON tags

```go
package main

import (
    "encoding/json"
    "fmt"
)

type Person struct {
    Name  string `json:"name"`
    Age   int    `json:"age"`
    Email string `json:"email,omitempty"`
}

func main() {
    p := Person{Name: "Alice", Age: 30}
    jsonData, _ := json.Marshal(p)
    fmt.Println(string(jsonData)) // prints: {"name":"Alice","age":30}
}
```

In this example:
- The `Name` field's tag is `json:"name"`, meaning `"name"` should be used as the field name when encoding to JSON.
- The `Age` field's tag is `json:"age"`, meaning `"age"` should be used as the field name when encoding to JSON.
- The `Email` field's tag is `json:"email,omitempty"`, meaning that if `Email` is empty (empty string, zero value, or nil), the field is omitted when encoding to JSON.

### 2. Reading struct tags

Reading struct tags requires Go's reflection mechanism. Here is an example of reading struct tags.

#### Example: reading struct tags

```go
package main

import (
    "fmt"
    "reflect"
)

type Person struct {
    Name  string `json:"name"`
    Age   int    `json:"age"`
    Email string `json:"email,omitempty"`
}

func main() {
    p := Person{Name: "Alice", Age: 30}
    t := reflect.TypeOf(p)

    for i := 0; i < t.NumField(); i++ {
        field := t.Field(i)
        fmt.Printf("Field: %s, Tag: %s\n", field.Name, field.Tag)
    }
}
```

Output:

```
Field: Name, Tag: json:"name"
Field: Age, Tag: json:"age"
Field: Email, Tag: json:"email,omitempty"
```

In this example, the reflection package `reflect` is used to read the struct fields' tags:
- `reflect.TypeOf(p)` gets the type information of the `Person` struct.
- `t.NumField()` gets the number of fields in the struct.
- `t.Field(i)` fetches each field's information one by one, printing the field name and tag.

### Common uses of struct tags

1. **JSON tags**
    - `json:"name"`: specify the field name used for JSON encoding/decoding.
    - `json:"name,omitempty"`: omit the field if its value is empty.
    - `json:"-"`: ignore the field entirely, no encoding/decoding.

2. **XML tags**
    - `xml:"name"`: specify the field name used for XML encoding/decoding.
    - `xml:"name,attr"`: emit the field as an XML attribute.
    - `xml:",chardata"`: emit the field as XML character data.

3. **Database tags (e.g. gorm)**
    - `gorm:"column:name"`: specify the database column name.
    - `gorm:"primaryKey"`: mark the field as the primary key.

### Summary

Struct tags hang a field's metadata on a backtick-quoted string, and `encoding/json`, `encoding/xml`, and gorm all rely on them to decide how to treat each field. A tag is just a string; to read it yourself you have to go through `reflect`.

## References

- [Effective Go (official)](https://go.dev/doc/effective_go)
- [encoding/json · Struct tags](https://pkg.go.dev/encoding/json)
- [Official blog · JSON and Go](https://go.dev/blog/json)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
- [BlankIdentifier](/idioms/BlankIdentifier.md)
- [CommaOk](/idioms/CommaOk.md)
- [Idioms](/idioms/Idioms.md)
- [Labels](/idioms/Labels.md)
- [Range](/idioms/Range.md)
- [ShortVarDecl](/idioms/ShortVarDecl.md)
