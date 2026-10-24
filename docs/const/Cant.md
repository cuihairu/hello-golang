In Go, some things cannot be defined as constants:

1. **Interface types**: interface types in Go cannot be defined as constants. An interface is an abstract type that describes the behavior of an object without caring about its concrete type. Because an interface type is dynamic and its concrete value can't be determined at compile time, it cannot serve as a constant.

   ```go
   // you cannot define an interface type as a constant
   const myInterface error = MyError{}
   ```

2. **Function types**: function types cannot be defined as constants either. A function type is an abstract type that describes the signature and parameter list of a function rather than a concrete function implementation. So the value of a function type cannot be determined at compile time, and it cannot serve as a constant.

   ```go
   // you cannot define a function type as a constant
   const myFunc func(int) int = func(x int) int { return x + 1 }
   ```

3. **Dynamically computed values**: a constant's value must be determined at compile time and cannot depend on the result of a runtime computation. So any expression or function call whose value is only known at runtime cannot serve as a constant. Note that `time.Second` is itself a constant of type `time.Duration`, so defining a constant with it is legal; what is not legal is calling a function that can only be evaluated at runtime.

   ```go
   // you cannot define a dynamically computed expression as a constant
   const maxFileSize = 1024 * 1024  // OK, determinable at compile time
   const timeout = time.Second      // OK, time.Second is itself a constant
   const now = time.Now()           // not allowed, time.Now() is a runtime function call
   ```

4. **Values of reference types such as slices and maps**: a constant's type can only be a basic type (boolean, numeric, string). Composite values such as slices, maps, and structs that need runtime construction cannot be defined as constants.

   ```go
   // you cannot define a slice or a map as a constant
   const mySlice = []int{1, 2, 3}     // not allowed, a slice is not a constant type
   const myMap = map[string]int{"a": 1} // not allowed
   ```

5. **Taking the address of a constant**: a constant is a compile-time value and doesn't necessarily occupy runtime memory, so you cannot take its address.

   ```go
   const count = 10
   p := &count // not allowed, invalid operation: cannot take address of count
   ```

All of these restrictions point to the same thing: a constant's value must be determined at compile time and cannot depend on runtime context or dynamic computation.

## References

- [Language specification · Constant declarations](https://go.dev/ref/spec#Constant_declarations)
- [Official blog · Constants](https://go.dev/blog/constants)

## Sibling pages

- [Const](/const/Const.md)
- [TrueAndFalse](/const/TrueAndFalse.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Const](/const/Const.md)
- [TrueAndFalse](/const/TrueAndFalse.md)
- [glossary](/zh/glossary.md)
