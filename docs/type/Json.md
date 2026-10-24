# Json
The standard library `encoding/json` handles JSON with two functions: `Marshal` encodes a struct into bytes, and `Unmarshal` decodes bytes back into a struct. Here I cover the basics, struct tags, nested and dynamic JSON, and the common pitfalls.

### 1. Basic usage

#### JSON encoding (serialization)

Convert a Go value into a JSON string.

```go
package main

import (
    "encoding/json"
    "fmt"
)

type Person struct {
    Name string
    Age  int
}

func main() {
    person := Person{Name: "Alice", Age: 30}
    
    // serialize person into a JSON string
    jsonData, err := json.Marshal(person)
    if err != nil {
        fmt.Println(err)
        return
    }
    
    fmt.Println(string(jsonData)) // prints: {"Name":"Alice","Age":30}
}
```

#### JSON decoding (deserialization)

Convert a JSON string into a Go value.

```go
package main

import (
    "encoding/json"
    "fmt"
)

type Person struct {
    Name string
    Age  int
}

func main() {
    jsonString := `{"Name":"Alice","Age":30}`
    
    var person Person
    
    // deserialize the JSON string back into person
    err := json.Unmarshal([]byte(jsonString), &person)
    if err != nil {
        fmt.Println(err)
        return
    }
    
    fmt.Println(person) // prints: {Alice 30}
}
```

### 2. Struct tags

Tags on struct fields control JSON encoding and decoding behavior. For example, you can specify the JSON field name, skip a field, or control how a field is decoded.

```go
package main

import (
    "encoding/json"
    "fmt"
)

type Person struct {
    Name   string `json:"name"`             // JSON field name is "name"
    Age    int    `json:"age"`              // JSON field name is "age"
    Gender string `json:"gender,omitempty"` // skip the field if it is empty
}

func main() {
    person := Person{Name: "Alice", Age: 30, Gender: ""}
    
    jsonData, err := json.Marshal(person)
    if err != nil {
        fmt.Println(err)
        return
    }
    
    fmt.Println(string(jsonData)) // prints: {"name":"Alice","age":30}
}
```

### 3. Common operations

#### Handling nested structs

You can handle JSON data that contains nested structs.

```go
package main

import (
    "encoding/json"
    "fmt"
)

type Address struct {
    City    string
    Country string
}

type Person struct {
    Name    string
    Age     int
    Address Address
}

func main() {
    jsonString := `{"Name":"Alice","Age":30,"Address":{"City":"New York","Country":"USA"}}`
    
    var person Person
    err := json.Unmarshal([]byte(jsonString), &person)
    if err != nil {
        fmt.Println(err)
        return
    }
    
    fmt.Println(person) // prints: {Alice 30 {New York USA}}
}
```

#### Handling dynamic JSON

You can use `map[string]interface{}` to handle JSON data whose structure is unknown.

```go
package main

import (
    "encoding/json"
    "fmt"
)

func main() {
    jsonString := `{"Name":"Alice","Age":30,"Address":{"City":"New York","Country":"USA"}}`
    
    var data map[string]interface{}
    err := json.Unmarshal([]byte(jsonString), &data)
    if err != nil {
        fmt.Println(err)
        return
    }
    
    fmt.Println(data) // prints: map[Name:Alice Age:30 Address:map[City:New York Country:USA]]
}
```

### 4. Common pitfalls

#### Case mismatch

JSON field names are case-sensitive, so make sure struct tags match the JSON field names.

```go
type Person struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}
```

#### Using the empty interface type

`interface{}` can handle data of any type, but you need type assertions to get the value back.

```go
package main

import (
    "encoding/json"
    "fmt"
)

func main() {
    jsonString := `{"Name":"Alice","Age":30}`

    var data map[string]interface{}
    json.Unmarshal([]byte(jsonString), &data)

    name := data["Name"].(string)
    age := data["Age"].(float64) // numbers in JSON are parsed as float64 by default
    fmt.Println(name, age)
}
```

#### Avoid circular references

Go's JSON encoder can't handle structs that contain circular references.

### 5. Example code

Here's a complete example showing JSON encoding, decoding, and handling nested structs:

```go
package main

import (
    "encoding/json"
    "fmt"
)

type Address struct {
    City    string `json:"city"`
    Country string `json:"country"`
}

type Person struct {
    Name    string  `json:"name"`
    Age     int     `json:"age"`
    Address Address `json:"address"`
}

func main() {
    person := Person{
        Name: "Alice",
        Age:  30,
        Address: Address{
            City:    "New York",
            Country: "USA",
        },
    }
    
    // JSON encoding
    jsonData, err := json.Marshal(person)
    if err != nil {
        fmt.Println(err)
        return
    }
    
    fmt.Println(string(jsonData)) // prints: {"name":"Alice","age":30,"address":{"city":"New York","country":"USA"}}
    
    // JSON decoding
    jsonString := `{"name":"Bob","age":25,"address":{"city":"San Francisco","country":"USA"}}`
    var newPerson Person
    err = json.Unmarshal([]byte(jsonString), &newPerson)
    if err != nil {
        fmt.Println(err)
        return
    }
    
    fmt.Println(newPerson) // prints: {Bob 25 {San Francisco USA}}
}
```

### Summary

Four things are enough: field names line up through `json:"..."` tags, and without a tag the field name is used as-is; `omitempty` makes zero-value fields disappear from the output; when the structure is unknown, fall back on `map[string]interface{}`, but remember that numbers in JSON all arrive as `float64` on the Go side; and a struct with circular references will make encoding fail.

## References

- [Language Spec · Types](https://go.dev/ref/spec#Types)
- [encoding/json standard library](https://pkg.go.dev/encoding/json)
- [Official Blog · JSON and Go](https://go.dev/blog/json)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [LinkedList](/type/LinkedList.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [LinkedList](/type/LinkedList.md)
