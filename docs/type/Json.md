# Json
在 Go 语言中，处理 JSON 数据非常简单且高效。Go 提供了标准库 `encoding/json`，用于编码和解码 JSON 数据。下面是对 Go 中 JSON 处理的详细介绍，包括基本用法、结构体标签、常见操作和常见的陷阱。

### 1. 基本用法

#### JSON 编码（序列化）

将 Go 变量转换为 JSON 格式的字符串。

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
    
    // 将 person 序列化为 JSON 字符串
    jsonData, err := json.Marshal(person)
    if err != nil {
        fmt.Println(err)
        return
    }
    
    fmt.Println(string(jsonData)) // 输出: {"Name":"Alice","Age":30}
}
```

#### JSON 解码（反序列化）

将 JSON 格式的字符串转换为 Go 变量。

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
    
    // 将 JSON 字符串反序列化为 person
    err := json.Unmarshal([]byte(jsonString), &person)
    if err != nil {
        fmt.Println(err)
        return
    }
    
    fmt.Println(person) // 输出: {Alice 30}
}
```

### 2. 结构体标签

在结构体字段上使用标签可以控制 JSON 编码和解码的行为。例如，可以指定 JSON 字段名、忽略某个字段、指定字段的解码方式等。

```go
package main

import (
    "encoding/json"
    "fmt"
)

type Person struct {
    Name   string `json:"name"`             // JSON 字段名为 "name"
    Age    int    `json:"age"`              // JSON 字段名为 "age"
    Gender string `json:"gender,omitempty"` // 若为空则忽略该字段
}

func main() {
    person := Person{Name: "Alice", Age: 30, Gender: ""}
    
    jsonData, err := json.Marshal(person)
    if err != nil {
        fmt.Println(err)
        return
    }
    
    fmt.Println(string(jsonData)) // 输出: {"name":"Alice","age":30}
}
```

### 3. 常见操作

#### 处理嵌套结构体

可以处理包含嵌套结构体的 JSON 数据。

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
    
    fmt.Println(person) // 输出: {Alice 30 {New York USA}}
}
```

#### 处理动态 JSON

可以使用 `map[string]interface{}` 来处理未知结构的 JSON 数据。

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
    
    fmt.Println(data) // 输出: map[Name:Alice Age:30 Address:map[City:New York Country:USA]]
}
```

### 4. 常见陷阱

#### 大小写不匹配

JSON 字段名的大小写敏感，确保结构体标签与 JSON 字段名匹配。

```go
type Person struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}
```

#### 使用空接口类型

使用 `interface{}` 可以处理任意类型的数据，但需要进行类型断言。

```go
var data map[string]interface{}
json.Unmarshal([]byte(jsonString), &data)

name := data["Name"].(string)
age := data["Age"].(float64) // JSON 中的数字默认解析为 float64
```

#### 避免循环引用

Go 的 JSON 编码器不能处理包含循环引用的结构体。

### 5. 示例代码

下面是一个完整的示例代码，展示了 JSON 编码、解码和处理嵌套结构体：

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
    
    // JSON 编码
    jsonData, err := json.Marshal(person)
    if err != nil {
        fmt.Println(err)
        return
    }
    
    fmt.Println(string(jsonData)) // 输出: {"name":"Alice","age":30,"address":{"city":"New York","country":"USA"}}
    
    // JSON 解码
    jsonString := `{"name":"Bob","age":25,"address":{"city":"San Francisco","country":"USA"}}`
    var newPerson Person
    err = json.Unmarshal([]byte(jsonString), &newPerson)
    if err != nil {
        fmt.Println(err)
        return
    }
    
    fmt.Println(newPerson) // 输出: {Bob 25 {San Francisco USA}}
}
```

### 总结

Go 语言提供了强大且易用的 `encoding/json` 包，用于处理 JSON 数据。通过理解 JSON 编码和解码的基本用法、结构体标签的使用、常见操作以及常见陷阱，可以有效地在 Go 程序中处理 JSON 数据。