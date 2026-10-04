Go 的错误处理以 `error` 返回值为主，`panic`/`recover` 只留给真正恢复不了的情况，标准库 `errors` 再补上比较、解包、取根因这几个动作。常见做法如下：

### 1. 返回 `error` 类型

Go 的标准错误处理方式是通过函数返回值返回一个 `error` 类型。`error` 是一个内置的接口类型，用于表示错误信息。

#### 示例

```go
package main

import (
    "fmt"
    "errors"
)

// 函数返回错误
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

func main() {
    result, err := divide(10, 0)
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    fmt.Println("Result:", result)
}
```

在这个示例中，`divide` 函数返回两个值：结果和一个 `error`。如果出现错误（如除数为零），函数返回一个非 `nil` 的 `error` 值，调用方可以检查这个错误值并作出相应处理。

### 2. 自定义错误类型

除了使用 `errors.New` 创建简单的错误外，可以创建自定义错误类型以提供更多上下文信息。自定义错误类型通常实现了 `error` 接口。

#### 示例

```go
package main

import (
    "fmt"
)

// CustomError 自定义错误类型
type CustomError struct {
    Code    int
    Message string
}

func (e *CustomError) Error() string {
    return fmt.Sprintf("Code %d: %s", e.Code, e.Message)
}

// 函数返回自定义错误
func doSomething() error {
    return &CustomError{Code: 404, Message: "Not Found"}
}

func main() {
    err := doSomething()
    if err != nil {
        fmt.Println("Error:", err)
    }
}
```

在这个示例中，自定义错误类型 `CustomError` 包含了错误代码和消息，并实现了 `Error` 方法。

### 3. `errors` 包

Go 的 `errors` 包提供了几个实用函数来创建和处理错误。`errors` 包中的一些函数包括：

- `errors.New`: 创建一个基本的错误。
- `errors.Is`: 判断错误链中是否存在与目标错误相等的错误（通常配合哨兵错误变量使用）。
- `errors.As`: 将错误转换为特定的错误类型。
- `errors.Unwrap`: 获取封装的底层错误。

#### 示例

注意：`errors.Is` 通过比较错误值（指针相等）来判断，因此目标必须是哨兵错误变量，不能是每次新建的 `&CustomError{}`。

```go
package main

import (
    "errors"
    "fmt"
)

// CustomError 自定义错误类型
type CustomError struct {
    Code    int
    Message string
}

func (e *CustomError) Error() string {
    return fmt.Sprintf("Code %d: %s", e.Code, e.Message)
}

// ErrNotFound 哨兵错误
var ErrNotFound = &CustomError{Code: 404, Message: "Not Found"}

func doSomething() error {
    return ErrNotFound
}

func main() {
    err := doSomething()

    if errors.Is(err, ErrNotFound) {
        fmt.Println("CustomError detected")
    }

    var customErr *CustomError
    if errors.As(err, &customErr) {
        fmt.Printf("CustomError with code %d\n", customErr.Code)
    }
}
```

### 4. 错误包装

错误包装是指在返回错误时附加更多上下文信息。Go 1.13 引入了错误包装功能，通过 `fmt.Errorf` 使用 `%w` 动作符进行错误包装。

#### 示例

```go
package main

import (
    "fmt"
    "errors"
)

// errOriginal 哨兵错误，供 errors.Is 比较
var errOriginal = errors.New("original error")

func doSomething() error {
    return fmt.Errorf("failed to do something: %w", errOriginal)
}

func main() {
    err := doSomething()
    if err != nil {
        fmt.Println("Error:", err)
        if errors.Is(err, errOriginal) {
            fmt.Println("The error is the original error")
        }
    }
}
```

### 5. 错误处理的最佳实践

- **提前返回**：对于错误处理，通常使用提前返回（early return）来简化代码逻辑。
  
  ```go
  func process() error {
      if err := doSomething(); err != nil {
          return err
      }
      // 继续处理
      return nil
  }
  ```

- **封装错误**：将错误封装到更高层次的函数中，并提供额外的上下文信息，以帮助调试和理解错误发生的原因。

  ```go
  func main() {
      if err := process(); err != nil {
          fmt.Printf("Error occurred: %v\n", err)
      }
  }
  ```

### 总结

- **返回 `error` 类型**：Go 的标准错误处理方式，通过返回 `error` 类型的值来处理函数中的错误。
- **自定义错误类型**：创建自定义的错误类型以提供更多的上下文信息。
- **`errors` 包**：提供了实用的错误创建和处理函数。
- **错误包装**：使用 `fmt.Errorf` 和 `%w` 动作符来包装错误，附加更多上下文信息。
- **最佳实践**：使用提前返回和错误封装来简化错误处理和提高代码的可维护性。

选哪一种取决于调用方要不要拿到错误细节：只是判等用 `errors.Is`，要取字段用 `errors.As`，要给排错加线索就用 `%w` 包装。