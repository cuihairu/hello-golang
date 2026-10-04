### Go 语言的命名规范

命名是 Go 代码风格里最常被 review 的部分：标识符怎么起名、大小写怎么定导出与否，规则不多但每条都有讲究。本章按标识符、包名、变量、常量、函数、类型、接口、文件名、目录名逐条给出规则和示例。

关键字、内建函数、内建类型和内建常量是预定义的，它们在任何代码中都有特殊的含义和用途。在编写 Go 代码时，我们应避免将这些关键字和内建名称用作标识符。以下是 Go 语言中的关键字、内建函数、内建类型和内建常量的详细列表。

#### 1. 标识符命名规则

在 Go 语言中，标识符是用来命名变量、常量、类型、函数、包等的名称。标识符可以包含字母、数字和下划线，但不能以数字开头。Go 的命名规则如下：

- 标识符区分大小写。
- 小写字母开头的标识符在包外不可见（包内私有）。
- 大写字母开头的标识符在包外可见（导出）。

#### 2. 包名

- 包名应尽量简短且有意义，通常是小写字母，不使用下划线或混合大小写。
- 包名通常与其所在的目录名相同。
- 避免使用通用名称，如 `common` 或 `util`。

示例：

```go
// greetings package
package greetings
```

#### 3. 变量名

- 变量名应简短但有意义。
- 局部变量通常使用较短的名字，如 `i`、`n`、`s` 等。
- 全局变量应使用更具描述性的名称。

示例：

```go
package main

import "fmt"

func main() {
    var count int        // global variable with descriptive name
    var i, j int         // local variables with short names
    count = 10
    i = 1
    j = 2
    fmt.Println(count, i, j)
}
```

#### 4. 常量名

- 常量名通常使用大写字母和下划线分隔词。
- 根据上下文可以使用驼峰式命名（CamelCase）。

示例：

```go
package main

import "fmt"

const Pi = 3.14             // CamelCase naming
const MaxRetries = 5        // CamelCase naming with multiple words
const MAX_BUFFER_SIZE = 1024 // ALL_CAPS with underscores

func main() {
    fmt.Println(Pi, MaxRetries, MAX_BUFFER_SIZE)
}
```

#### 5. 函数名

- 函数名应以动词开头，描述其功能。
- 如果函数是导出的（可从其他包访问），使用大写字母开头。
- 如果函数是包内私有的，使用小写字母开头。

示例：

```go
package main

import "fmt"

func CalculateTotal() int { // exported function
    return 100
}

func parseInput() { // unexported function
    fmt.Println("Parsing input")
}

func main() {
    total := CalculateTotal()
    fmt.Println("Total:", total)
    parseInput()
}
```

#### 6. 类型名

- 类型名应为名词，描述其表示的实体。
- 导出的类型名以大写字母开头，包内私有类型名以小写字母开头。

示例：

```go
package main

import "fmt"

type User struct { // exported type
    Name  string
    Email string
}

type config struct { // unexported type
    Port int
    Host string
}

func main() {
    u := User{Name: "Alice", Email: "alice@example.com"}
    fmt.Println(u)

    c := config{Port: 8080, Host: "localhost"}
    fmt.Println(c)
}
```

#### 7. 接口名

- 接口名通常以 `er` 结尾，表示实现该接口的类型所具备的行为。
- 短小的接口名可以省略 `er` 后缀。

示例：

```go
package main

import "fmt"

type Reader interface { // common interface name ending with 'er'
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type Stringer interface { // common interface name ending with 'er'
    String() string
}

func main() {
    // Example implementation of interfaces would go here
    fmt.Println("Interfaces defined")
}
```

#### 8. 文件名

- 文件名应全部小写，可以使用下划线分隔词。
- 文件名应描述文件的内容或功能。

示例：

```plaintext
main.go
greetings.go
user_service.go
```

#### 9. 目录名

- 目录名应全部小写，不使用下划线或混合大小写。
- 目录名应与包名相同，简短且有意义。

示例：

```plaintext
greetings/
user/
```

### 示例项目结构

以下是一个包含多个文件和包的项目结构示例：

```plaintext
my-go-project/
├── go.mod           # Go module file
├── go.sum           # Go module dependencies file
├── main.go          # Main program file
├── greetings/       # Custom package directory
│   └── greetings.go # Custom package source file
└── user/            # Another package directory
    ├── user.go      # Source file for the user package
    └── user_test.go # Test file for the user package
```

### 完整示例代码

#### `main.go`

```go
package main

import (
    "fmt"
    "my-go-project/greetings"
    "my-go-project/user"
)

func main() {
    message := greetings.Hello("Go")
    fmt.Println(message)

    u := user.NewUser("Alice", "alice@example.com")
    fmt.Println(u)
}
```

#### `greetings/greetings.go`

```go
package greetings

import "fmt"

// Hello returns a greeting for the named person.
func Hello(name string) string {
    return fmt.Sprintf("Hello, %s!", name)
}
```

#### `user/user.go`

```go
package user

import "fmt"

// User represents a user in the system.
type User struct {
    Name  string
    Email string
}

// NewUser creates a new User.
func NewUser(name, email string) User {
    return User{Name: name, Email: email}
}

// String returns a string representation of the User.
func (u User) String() string {
    return fmt.Sprintf("Name: %s, Email: %s", u.Name, u.Email)
}
```

上面这些规则可以压成一句：Go 的惯例是名字越短越好，作用域越大、生命周期越长的名字越要写得具体。团队里把规则写成一份约定并让 lint 工具把关，新代码就不会出现两种风格。