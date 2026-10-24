# Keywords and Reserved Words
In Go, keywords and reserved words are tokens with special meanings, used to define program structure and control flow. Below are the keywords and reserved words in Go:

### Keywords

Go has 25 keywords, used to define program structure and control flow:

1. **break**: terminates a loop or breaks out of a switch statement.
2. **case**: marks one branch of a switch statement.
3. **chan**: used to declare a channel.
4. **const**: used to declare a constant.
5. **continue**: skips the rest of the current loop iteration and moves on to the next iteration.
6. **default**: marks the default branch of a switch statement.
7. **defer**: postpones running a function until the surrounding function returns.
8. **else**: provides an alternative branch in an if statement.
9. **fallthrough**: in a switch statement, forces execution of the next case clause.
10. **for**: used to declare a loop.
11. **func**: used to declare a function.
12. **go**: starts a new goroutine.
13. **goto**: jumps to a given label.
14. **if**: used for conditional branching.
15. **import**: imports a package.
16. **interface**: used to declare an interface.
17. **map**: used to declare a map (hash table).
18. **package**: declares package-level code.
19. **range**: iterates over the elements of a collection.
20. **return**: returns from a function.
21. **select**: used to pick one of several communication operations.
22. **struct**: used to declare a struct.
23. **switch**: used to select a multi-way branch.
24. **type**: used to declare a new type.
25. **var**: used to declare a variable.

### Reserved words

Reserved words are words not currently used in Go but held for future use. These words cannot be used as identifiers in Go. Go doesn't have reserved words the way some other languages do, but it does have some special predefined identifiers and constants.

### Predeclared identifiers

Predeclared identifiers are identifiers predefined in Go, mainly for built-in functions and types. Although these identifiers can be redefined, doing so is generally not recommended.

1. **Built-in constants**:
    - **true**: the true value of the boolean type.
    - **false**: the false value of the boolean type.
    - **iota**: a constant generator, used for enumerations.
    - **nil**: stands for a zero value or empty value, and applies to pointer, channel, function, interface, map, and slice types.

2. **Built-in types**:
    - **int**: integer type.
    - **int8**: 8-bit integer type.
    - **int16**: 16-bit integer type.
    - **int32**: 32-bit integer type.
    - **int64**: 64-bit integer type.
    - **uint**: unsigned integer type.
    - **uint8**: 8-bit unsigned integer type.
    - **uint16**: 16-bit unsigned integer type.
    - **uint32**: 32-bit unsigned integer type.
    - **uint64**: 64-bit unsigned integer type.
    - **uintptr**: unsigned integer type, used for pointer arithmetic.
    - **float32**: 32-bit floating-point type.
    - **float64**: 64-bit floating-point type.
    - **complex64**: 64-bit complex number type.
    - **complex128**: 128-bit complex number type.
    - **bool**: boolean type.
    - **byte**: the same as the uint8 type.
    - **rune**: the same as the int32 type, representing a Unicode code point.
    - **string**: string type.
    - **error**: the built-in error interface type.

3. **Built-in functions**:
    - **append**: appends to a slice.
    - **cap**: returns the capacity.
    - **close**: closes a channel.
    - **complex**: constructs a complex number.
    - **copy**: copies a slice.
    - **delete**: deletes an element from a map.
    - **imag**: returns the imaginary part of a complex number.
    - **len**: returns the length.
    - **make**: allocates and initializes objects.
    - **new**: allocates memory.
    - **panic**: triggers a runtime error.
    - **print**: prints output.
    - **println**: prints output with a newline.
    - **real**: returns the real part of a complex number.
    - **recover**: recovers from a panic.

## References

- [Effective Go · Names](https://go.dev/doc/effective_go#names)
- [Official · CodeReviewComments](https://go.dev/wiki/CodeReviewComments)
- [Language spec · Keywords](https://go.dev/ref/spec#Keywords)

## Sibling pages

- [IdentifierNamingRules](/naming/IdentifierNamingRules.md)
- [Naming](/naming/Naming.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [IdentifierNamingRules](/naming/IdentifierNamingRules.md)
- [Naming](/naming/Naming.md)
