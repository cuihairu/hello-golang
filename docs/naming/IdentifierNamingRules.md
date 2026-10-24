### Naming conventions for the Go language

Naming is the part of Go code style that gets reviewed most often: how to name identifiers, and how capitalization decides whether something is exported. There aren't many rules, but each one has its reasoning. Here I organize the rules and examples by identifier, package name, variable, constant, function, type, interface, file name, and directory name.

Keywords, built-in functions, built-in types, and built-in constants are predefined; they have special meaning and uses in any code. When writing Go code, we should avoid using these keywords and built-in names as identifiers. Below is a detailed list of the keywords, built-in functions, built-in types, and built-in constants in Go.

#### 1. Identifier naming rules

In Go, identifiers are the names used to name variables, constants, types, functions, packages, and so on. An identifier can contain letters, digits, and underscores, but cannot start with a digit. Go's naming rules are:

- Identifiers are case-sensitive.
- An identifier starting with a lowercase letter is not visible outside the package (private within the package).
- An identifier starting with an uppercase letter is visible outside the package (exported).

#### 2. Package names

- A package name should be short and meaningful, usually lowercase letters, with no underscores or mixed case.
- A package name is usually the same as the directory it lives in.
- Avoid generic names such as `common` or `util`.

Example:

```go
// greetings package
package greetings
```

#### 3. Variable names

- Variable names should be short but meaningful.
- Local variables usually use short names such as `i`, `n`, `s`.
- Global variables should use more descriptive names.

Example:

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

#### 4. Constant names

- Constant names usually use uppercase letters and underscores to separate words.
- CamelCase naming can be used depending on the context.

Example:

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

#### 5. Function names

- A function name should start with a verb describing what it does.
- If the function is exported (accessible from other packages), start it with an uppercase letter.
- If the function is private within the package, start it with a lowercase letter.

Example:

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

#### 6. Type names

- A type name should be a noun describing the entity it represents.
- An exported type name starts with an uppercase letter; a private one starts with a lowercase letter.

Example:

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

#### 7. Interface names

- An interface name usually ends in `er`, expressing the behavior the implementing type provides.
- A short interface name can drop the `er` suffix.

Example:

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

#### 8. File names

- File names should be all lowercase; underscores can be used to separate words.
- A file name should describe the file's contents or purpose.

Example:

```plaintext
main.go
greetings.go
user_service.go
```

#### 9. Directory names

- Directory names should be all lowercase, with no underscores or mixed case.
- A directory name should match the package name and be short and meaningful.

Example:

```plaintext
greetings/
user/
```

### Example project structure

Below is an example project structure with multiple files and packages:

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

### Complete example code

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

All of the rules above compress into one sentence: Go's convention is that the shorter a name, the better, and the wider the scope and the longer the lifetime, the more concrete the name should be. In a team, write the rules down as a single convention and let a linter enforce them, and new code won't end up with two styles.

## References

- [Effective Go · Names](https://go.dev/doc/effective_go#names)
- [Official · CodeReviewComments](https://go.dev/wiki/CodeReviewComments)
- [Effective Go · MixedCaps](https://go.dev/doc/effective_go#mixed-caps)

## Sibling pages

- [KeywordsAndReservedWords](/naming/KeywordsAndReservedWords.md)
- [Naming](/naming/Naming.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [KeywordsAndReservedWords](/naming/KeywordsAndReservedWords.md)
- [Naming](/naming/Naming.md)
