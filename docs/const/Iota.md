Go doesn't offer an explicit enum type the way other languages do, but you can get the same effect with a few techniques and conventions. Among them, `iota` is a special predefined identifier that is commonly used to give incrementing values to a group of enum constants.

### Implementing enum types

The pattern is to define a group of constants with `const` and let `iota` make them increment in sequence.

#### Defining enums with `iota`

```go
package main

import "fmt"

// define the enum type
type Weekday int

const (
    Sunday Weekday = iota
    Monday
    Tuesday
    Wednesday
    Thursday
    Friday
    Saturday
)

func (d Weekday) String() string {
    return [...]string{"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"}[d]
}

func main() {
    fmt.Println(Sunday)     // prints: Sunday (Weekday implements String(), so the name is printed)
    fmt.Println(Monday)     // prints: Monday
    fmt.Println(Tuesday)    // prints: Tuesday
    fmt.Println(Wednesday)  // prints: Wednesday
    fmt.Println(Thursday)   // prints: Thursday
    fmt.Println(Friday)     // prints: Friday
    fmt.Println(Saturday)   // prints: Saturday

    // to print the corresponding integer values, do an explicit conversion
    fmt.Println(int(Sunday), int(Saturday)) // prints: 0 6

    // use the enum type
    today := Wednesday
    fmt.Printf("Today is %s\n", today) // prints: Today is Wednesday
}
```

### Using `iota`

- **Automatic incrementing**: inside a `const` group, `iota` starts at 0 and increments automatically, and it resets to 0 each time a new `const` keyword is encountered.
- **Skipping values**: you can use the blank identifier `_` to skip over some values.

#### Example

```go
package main

import "fmt"

// define the enum type
type FilePermission uint

const (
    ReadPermission FilePermission = 1 << iota
    WritePermission
    ExecutePermission
)

func main() {
    var p FilePermission = ReadPermission | WritePermission

    fmt.Printf("Permission: %b\n", p) // prints: Permission: 11
    fmt.Println("Has Read permission?", p&ReadPermission == ReadPermission)
    fmt.Println("Has Write permission?", p&WritePermission == WritePermission)
    fmt.Println("Has Execute permission?", p&ExecutePermission == ExecutePermission)
}
```

### Where to use it

- **Defining status codes**: a finite set of values such as HTTP status codes or file permissions.
- **Options and flags**: combined with `1 << iota` to build bit masks.

### Things to watch

- `iota` is only valid inside a `const` group, and it resets every time a new `const` keyword is encountered.

### Summary

For a group of related constants like status codes or permission bits, define them with `const` plus `iota`: values increment automatically from 0 inside the constant group, and when you want to skip a value, use `_` as a placeholder.

## References

- [Language specification · Constant declarations](https://go.dev/ref/spec#Constant_declarations)
- [Official blog · Constants](https://go.dev/blog/constants)
- [Language specification · Iota](https://go.dev/ref/spec#Iota)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Const](/const/Const.md)
- [TrueAndFalse](/const/TrueAndFalse.md)
- [glossary](/glossary.md)
