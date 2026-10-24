In Go, scope answers "where can this name be used", while lifetime answers "when does this memory get reclaimed". Both are determined by where the variable is declared.

### Variable scope

Scope is the region of a program where a variable can be referenced. Go has the following main kinds of variable scope:

1. **Package scope**:
   - Variables declared at package level can be accessed from all files in the same package.
   - Package-scope variables are usually declared at package level with the `var` keyword.
   - If a variable name starts with an uppercase letter, the variable is exported and can be accessed from other packages.

   For example:
   ```go
   // file1.go
   package main

   var PackageVar = "I am accessible throughout the package"

   func main() {
       fmt.Println(PackageVar)
   }

   // file2.go
   package main

   func anotherFunction() {
       fmt.Println(PackageVar) // can access PackageVar
   }
   ```

2. **Function scope**:
   - Variables declared inside a function can only be accessed within that function.
   - Function-scope variables include function parameters and variables declared inside a function with `var` or `:=`.

   For example:
   ```go
   func exampleFunction() {
       var functionVar = "I am only accessible within this function"
       fmt.Println(functionVar)
   }

   func anotherFunction() {
       // fmt.Println(functionVar) // cannot access functionVar
   }
   ```

3. **Block scope**:
   - Variables declared inside a code block (for example `if`, `for`, `switch`, etc.) can only be accessed within that code block.
   - Block-scope variables can be declared with `var` or `:=`.

   For example:
   ```go
   func exampleFunction() {
       if true {
           var blockVar = "I am only accessible within this block"
           fmt.Println(blockVar)
       }
       // fmt.Println(blockVar) // cannot access blockVar
   }
   ```

### Variable lifetime

Lifetime is the whole process from a variable's creation to its destruction. In Go, a variable's lifetime is mainly shaped by its scope:

1. **Package-level variables**:
   - Package-level variables are allocated when the program starts and freed when it ends.
   - Their lifetime spans the entire program run.

   For example:
   ```go
   var packageVar = "I live for the lifetime of the program"
   ```

2. **Local variables**:
   - Local variables are allocated when their enclosing function or code block is executed, and freed when that function or code block finishes.
   - Local variables usually have a short lifetime, confined to the execution of their function or code block.

   For example:
   ```go
   func exampleFunction() {
       var localVar = "I live for the lifetime of this function"
       fmt.Println(localVar)
   }
   ```

3. **Dynamically allocated variables**:
   - Variables allocated dynamically with `new` or `make` have a lifetime controlled by the program, and can continue to be used outside a function.
   - Dynamically allocated variables do not need to be freed manually; when they are no longer referenced, Go's garbage collector automatically reclaims the memory they occupy.

   For example:
   ```go
   func exampleFunction() {
       ptr := new(int)   // dynamic allocation
       *ptr = 100
       fmt.Println(*ptr) // dynamically allocated variables can continue to be used outside the function
   }
   ```

### Example code

Three scopes in a single program:

```go
package main

import "fmt"

// package-level variable
var packageVar = "I am a package-level variable"

func main() {
    fmt.Println(packageVar) // access the package-level variable

    // local variable
    var functionVar = "I am a function-level variable"
    fmt.Println(functionVar)

    if true {
        // block-level variable
        var blockVar = "I am a block-level variable"
        fmt.Println(blockVar)
    }
    // fmt.Println(blockVar) // cannot access blockVar

    anotherFunction()
}

func anotherFunction() {
    fmt.Println(packageVar) // access the package-level variable
    // fmt.Println(functionVar) // cannot access functionVar
}
```

### Summary

Package-level variables live for the whole process, local variables disappear when the function call ends, and memory allocated with `new`/`make` is reclaimed by the GC once it has no references. Scope and lifetime are two sides of the same thing: which block a declaration lives in decides where the name is visible, and how long the memory lasts.

## References

- [Language Spec · Variable declarations](https://go.dev/ref/spec#Variable_declarations)
- [Effective Go · Variables](https://go.dev/doc/effective_go#variables)
- [Language Spec · Declarations and scope](https://go.dev/ref/spec#Declarations_and_scope)

## Sibling pages

- [Segment](/var/Segment.md)
- [VarAndInit](/var/VarAndInit.md)
- [Assignment](/var/Assignment.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Assignment](/var/Assignment.md)
