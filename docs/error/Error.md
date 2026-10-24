Different programming languages have different error-handling mechanisms. Here are the error-handling approaches and their characteristics in some common languages:

### 1. **Go**

In Go, error handling relies on the `error` interface. Go uses explicit error return values to handle errors, letting programmers check and handle errors at the call site.

- **Error type**: the `error` interface, which defines an `Error()` method.
- **Creating errors**: use `errors.New` or `fmt.Errorf`.
- **Checking errors**: inspect whether the `error` return value from a function is `nil`.

**Example:**

```go
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}

func main() {
    result, err := divide(10, 0)
    if err != nil {
        fmt.Println("Error:", err)
    } else {
        fmt.Println("Result:", result)
    }
}
```

### 2. **Python**

Python uses an exception-handling mechanism to manage errors. Exceptions can be caught and handled so the program can keep running or respond to the error in a specific way.

- **Exception types**: a class-based exception hierarchy; every exception inherits from `BaseException`.
- **Raising exceptions**: use the `raise` statement.
- **Catching exceptions**: use `try`, `except`, `else`, and `finally` blocks.

**Example:**

```python
def divide(a, b):
    if b == 0:
        raise ValueError("division by zero")
    return a / b

try:
    result = divide(10, 0)
except ValueError as e:
    print("Error:", e)
else:
    print("Result:", result)
```

### 3. **Java**

Java uses an exception mechanism to handle errors. Exceptions in Java are split into checked exceptions and unchecked exceptions.

- **Exception types**: all exceptions inherit from the `Throwable` class. The main subclasses are `Exception` and `RuntimeException`.
- **Raising exceptions**: use the `throw` statement.
- **Catching exceptions**: use `try`, `catch`, and `finally` blocks.

**Example:**

```java
public class Main {
    public static void main(String[] args) {
        try {
            int result = divide(10, 0);
            System.out.println("Result: " + result);
        } catch (ArithmeticException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    public static int divide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("division by zero");
        }
        return a / b;
    }
}
```

### 4. **C++**

C++ uses an exception-handling mechanism to manage errors, but it also allows error handling through return values or error codes.

- **Exception types**: exceptions can be any `std::exception` or a class derived from it.
- **Raising exceptions**: use the `throw` statement.
- **Catching exceptions**: use `try` and `catch` blocks. C++ has no `finally` block; the idiom for releasing resources is RAII (the destructor releases them).

**Example:**

```cpp
#include <iostream>
#include <stdexcept>

int divide(int a, int b) {
    if (b == 0) {
        throw std::runtime_error("division by zero");
    }
    return a / b;
}

int main() {
    try {
        int result = divide(10, 0);
        std::cout << "Result: " << result << std::endl;
    } catch (const std::runtime_error& e) {
        std::cout << "Error: " << e.what() << std::endl;
    }
}
```

### 5. **JavaScript**

JavaScript uses an exception-handling mechanism to manage errors, much like Python. It uses `try...catch` statements to catch and handle exceptions.

- **Exception types**: exception objects can be of any type; the common ones are the `Error` object and its subclasses.
- **Raising exceptions**: use the `throw` statement.
- **Catching exceptions**: use `try`, `catch`, and `finally` blocks.

**Example:**

```javascript
function divide(a, b) {
    if (b === 0) {
        throw new Error("division by zero");
    }
    return a / b;
}

try {
    let result = divide(10, 0);
    console.log("Result:", result);
} catch (e) {
    console.log("Error:", e.message);
}
```

### 6. **C**

In C, error handling is done mainly through return values or global variables (such as `errno`). C has no built-in exception mechanism.

- **Error type**: an integer return value or `errno` is used to represent error state.
- **Creating errors**: return a specific error code or set `errno`.
- **Checking errors**: inspect the return value or `errno` to decide whether an operation succeeded.

**Example:**

```c
#include <stdio.h>
#include <errno.h>
#include <string.h>

int divide(int a, int b) {
    if (b == 0) {
        errno = EINVAL; // set the error code
        return -1;
    }
    return a / b;
}

int main() {
    int result = divide(10, 0);
    if (result == -1) {
        printf("Error: %s\n", strerror(errno));
    } else {
        printf("Result: %d\n", result);
    }
}
```

### Summary

- **Go**: uses the `error` interface and handles errors through return values.
- **Python**: uses an exception mechanism with `try`, `except`, `else`, and `finally` blocks.
- **Java**: uses an exception mechanism with `try`, `catch`, and `finally` blocks, split into checked and unchecked exceptions.
- **C++**: uses an exception mechanism with `try` and `catch` blocks; exceptions are based on `std::exception`; resource cleanup relies on RAII, with no `finally` block.
- **JavaScript**: uses an exception mechanism with `try`, `catch`, and `finally` blocks.
- **C**: uses return values or `errno` for error handling, with no built-in exception mechanism.

## References

- [Official blog · Error handling and Go](https://go.dev/blog/error-handling-and-go)
- [Official blog · Errors are values](https://go.dev/blog/errors-are-values)
- [errors standard library](https://pkg.go.dev/errors)
- [Effective Go · Errors](https://go.dev/doc/effective_go#errors)
- [Language spec · Errors (error built-in interface)](https://go.dev/ref/spec#Errors)

## Sibling pages

- [ErrorType](/error/ErrorType.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [ErrorType](/error/ErrorType.md)
- [glossary](/glossary.md)
