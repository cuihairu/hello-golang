# Naming

Naming is the first-order factor in code readability. The Go community has a set of naming conventions: part of it is enforced by the compiler and toolchain, and the rest is the style recommended in the official documentation (such as [Effective Go](https://go.dev/doc/effective_go#names) and [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)). Here I collect the core rules and common conventions for naming in Go.

### Basic rules of naming

1. **Composition**: an identifier is made of letters, digits, and underscores, and cannot start with a digit. Go identifiers are theoretically Unicode-aware, but by convention only ASCII letters are used.
2. **Case decides visibility**: this is Go's biggest difference from other languages — **an identifier starting with an uppercase letter is exported (public), lowercase means unexported (private within the package)**. There are no `public` or `private` keywords.
3. **Cannot conflict with keywords**: the 25 keywords such as `break`, `func`, `interface` cannot be used as identifiers; some predeclared identifiers (such as `int`, `len`, `nil`) can be shadowed, but it is not recommended.

```go
package user

type Profile struct {  // exported type, usable by other packages
    Name    string     // exported field
    email   string     // unexported field, visible only within the package
}

func NewProfile() *Profile { ... }  // exported constructor
func validate() bool       { ... }  // unexported function
```

### Naming style conventions

#### Package names

- All lowercase, a single word, no underscores or camelCase: `strconv`, `httputil`, not `str_conv` or `httpUtil`.
- Use the plural form of a noun for collection packages: `bytes`, `errors`.
- Avoid clashing with standard library package names (don't name your own utility package `sync` or `time`).
- A package name should describe what the package "provides", not what it "contains": `net/http`, not `util` or `common`.

#### Variables and functions

- Use camelCase, no underscores: `parseRequest`, `maxRetryCount`.
- The longer the scope, the longer the name: local variables in a short scope can use short names like `i`, `n`, `buf`; an exported package-level identifier should describe its purpose in full.
- Avoid meaningless names: `data`, `info`, `temp`, `foo`.
- Function names use a verb or a verb-object phrase: `Read`, `ParseIP`, `NewServer`.

```go
// not recommended
func GetDataFromDBAndConvertIt() []byte { ... }

// recommended
func LoadConfig() []byte { ... }
```

#### Interfaces

- A single-method interface is usually named "method name + er": `Reader`, `Writer`, `Formatter`, `Clock`.
- A multi-method interface can use a noun describing its role: `Conn`, `Handler`.
- The standard library as a model: `io.Reader`, `io.Writer`, `fmt.Stringer` (method `String()`).

```go
type Stringer interface {
    String() string
}

type Speaker interface {
    Speak() string
}
```

#### Struct methods: avoid the Get prefix

By Go convention, **accessors don't use a `Get` prefix**: `obj.Name()`, not `obj.GetName()`; the corresponding setter uses `SetXxx`:

```go
type Counter struct {
    mu    sync.Mutex
    count int
}

func (c *Counter) Count() int { // read: use the field name directly
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.count
}

func (c *Counter) SetCount(n int) { // write: use the Set prefix
    c.mu.Lock()
    c.count = n
    c.mu.Unlock()
}
```

#### Error types and error variables

- Error types end in `Error`: `type ParseError struct { ... }`.
- Sentinel error variables start with `Err`: `var ErrNotFound = errors.New("not found")`.

```go
var ErrTimeout = errors.New("operation timed out")

type ParseError struct {
    Input string
}

func (e *ParseError) Error() string {
    return fmt.Sprintf("cannot parse %q", e.Input)
}
```

#### Acronyms

Acronyms keep a consistent case, following convention: `URL` → the `URL` in `ServeHTTP`, `id` (or `ID` — pick one and keep it consistent across the whole project), `HTTP`, `IP`. The standard library style is to write an uppercase acronym in full caps at an exported position (`File` in `ReadFile`, `JSON` in `MarshalJSON`).

```go
// recommended
type HTTPClient struct { ... }
func (c *HTTPClient) FetchURL(u string) error { ... }

// not recommended
type HttpClient struct { ... }
func (c *HttpClient) FetchUrl(u string) error { ... }
```

### Common anti-patterns

| Anti-pattern | Problem | Suggestion |
| ------ | ---- | ---- |
| `GetUser()` to read a field | Not idiomatic Go | `User()` |
| `userListArr` | Redundant suffix | `users` |
| `DoProcess()` | Uninformative verb | Name it after the actual action, e.g. `Parse`, `Sync` |
| Package named `utils`, `common`, `misc` | Catches everything, unclear responsibility | Split into packages named after their function |
| `myProject/internal2` | Meaningless numeric suffix | Name it by module |
| Interface named `IUser` | Hungarian prefix, not Go style | `User`, or name it by method such as `UserReader` |

### Tooling

- **gofmt / gofmt -s**: unify code formatting and end formatting arguments.
- **go vet**: check for suspicious naming-related issues, such as struct tag format (`structtag`).
- **staticcheck / revive / golangci-lint**: configurable naming style checks (such as an exported identifier missing a comment, or a package name that doesn't follow the convention).

```sh
go vet ./...
golangci-lint run
```

### Summary

The core principles of naming in Go are **short, accurate, consistent**. Visibility is decided by case, package names are short and not camelCase, variables adjust their length with the scope, interfaces end in "er", and errors use sentinel variables prefixed with `Err`. Follow these conventions and the code fits naturally into the Go ecosystem, letting collaborators "get it at a glance".

## References

- [Effective Go · Names](https://go.dev/doc/effective_go#names)
- [Official · CodeReviewComments](https://go.dev/wiki/CodeReviewComments)

## Sibling pages

- [IdentifierNamingRules](/naming/IdentifierNamingRules.md)
- [KeywordsAndReservedWords](/naming/KeywordsAndReservedWords.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [IdentifierNamingRules](/naming/IdentifierNamingRules.md)
- [KeywordsAndReservedWords](/naming/KeywordsAndReservedWords.md)
