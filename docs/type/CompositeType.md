Composite types in programming are data structures built by combining multiple primitive types or other composite types. They exist mainly to solve the following problems:

### 1. Data organization and management

Composite types bundle related pieces of data together, so the structure mirrors the relationships in the actual problem.

For example, in a social network app, a user's profile might include a username, age, and a friends list. Putting them together in a struct lets anyone reading the code see at a glance which fields the user data has.

```go
type User struct {
    Username string
    Age      int
    Friends  []string
}
```

### 2. Data access and operations

Composite types define more than data — they also define how you access and manipulate that data. Methods (struct methods, interface methods) pin down the create/update/delete/read conventions, so callers don't have to worry about the internal structure.

```go
// define the struct and its methods
type User struct {
    Username string
    Age      int
    Friends  []string
}

func (u *User) AddFriend(friend string) {
    u.Friends = append(u.Friends, friend)
}

func (u *User) RemoveFriend(friend string) {
    for i, f := range u.Friends {
        if f == friend {
            u.Friends = append(u.Friends[:i], u.Friends[i+1:]...)
            return
        }
    }
}

// usage example
func main() {
    user := User{
        Username: "Alice",
        Age:      30,
        Friends:  []string{"Bob", "Charlie"},
    }

    user.AddFriend("David")
    fmt.Println(user.Friends)  // prints: [Bob Charlie David]

    user.RemoveFriend("Charlie")
    fmt.Println(user.Friends)  // prints: [Bob David]
}
```

### 3. Memory allocation and performance optimization

At the implementation level, different parts of a composite type can be placed in different regions of memory. A slice, as an implementation of a dynamic array, adjusts its length and capacity automatically, without the fixed-length constraint of a regular array.

```go
// a slice as a dynamic array
func main() {
    // start with an empty int slice
    var numbers []int

    // add elements
    numbers = append(numbers, 1)
    numbers = append(numbers, 2, 3, 4)

    // print the slice contents
    fmt.Println(numbers)  // prints: [1 2 3 4]
}
```

### Summary

Composite types do three things: structs bundle related fields together, methods specify how data is operated on, and slices grow or shrink capacity on demand. Any shape a single primitive type can't express, they piece together.

## References

- [Language spec · Types](https://go.dev/ref/spec#Types)
- [Language spec · Composite literals](https://go.dev/ref/spec#Composite_literals)


## Sibling pages

- [Assertion](/zh/type/Assertion.md)
- [Interface](/zh/type/Interface.md)
- [Map](/zh/type/Map.md)
- [Complex](/zh/type/Complex.md)
- [Conv](/zh/type/Conv.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Complex](/zh/type/Complex.md)
- [Conv](/zh/type/Conv.md)
