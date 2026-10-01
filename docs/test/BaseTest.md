### 基本测试

在 Go 语言中，基本测试是确保代码功能正确的核心部分。通过编写和运行测试用例，我们可以验证代码的行为是否符合预期。以下是有关 Go 中基本测试的详细讲解，包括如何编写测试、运行测试以及使用常见的测试工具。

#### 2.1 测试文件和测试函数

##### 测试文件

在 Go 中，测试文件以 `_test.go` 结尾。例如，如果你正在测试 `math.go` 文件中的代码，那么相应的测试文件应命名为 `math_test.go`。这样，Go 工具链能够识别并运行这些测试文件。

##### 测试函数

测试函数的签名应为 `func TestXxx(t *testing.T)`，其中 `Xxx` 是测试的名称，`t` 是一个 `*testing.T` 类型的参数，用于管理测试的状态和记录结果。

**示例**:
```go
// math.go
package math

// Add 返回两个整数的和
func Add(a, b int) int {
    return a + b
}

// math_test.go
package math

import "testing"

// TestAdd 测试 Add 函数
func TestAdd(t *testing.T) {
    result := Add(2, 3)
    expected := 5

    if result != expected {
        t.Errorf("Add(2, 3) = %d; want %d", result, expected)
    }
}
```

在上述代码中：
- `Add` 是被测试的函数。
- `TestAdd` 是测试函数，用于验证 `Add` 函数是否返回预期的结果。
- 使用 `t.Errorf` 记录测试失败的详细信息。

#### 2.2 运行测试

使用 `go test` 命令可以运行测试。默认情况下，Go 会查找当前目录及其子目录中的所有 `_test.go` 文件并运行其中的测试。

**基本命令**:
```sh
go test
```

- `go test` 会编译测试代码和被测试的代码，然后执行所有的测试函数。
- 测试结果会显示在终端上。

**查看详细输出**:
```sh
go test -v
```

- `-v` 标志用于启用详细模式，会显示每个测试的输出和结果。

**运行特定测试**:
```sh
go test -run TestAdd
```

- `-run` 标志用于运行匹配指定模式的测试函数。上面的命令只运行 `TestAdd` 测试。

**运行测试并生成覆盖率报告**:
```sh
go test -cover
```

- `-cover` 标志用于显示测试覆盖率，即测试代码覆盖了多少百分比的源代码。

**生成覆盖率报告**:
```sh
go test -coverprofile=coverage.out
go tool cover -html=coverage.out
```

- `-coverprofile` 标志指定覆盖率数据的输出文件。
- `go tool cover` 用于生成覆盖率报告并以 HTML 格式查看。

#### 2.3 测试输出

测试函数可以使用 `t.Log` 和 `t.Logf` 方法来记录调试信息，这些信息仅在使用 `-v` 标志运行测试时显示。

**示例**:
```go
func TestAdd(t *testing.T) {
    result := Add(2, 3)
    expected := 5

    if result != expected {
        t.Logf("Testing Add(2, 3)")
        t.Errorf("Add(2, 3) = %d; want %d", result, expected)
    }
}
```

- `t.Logf` 用于记录调试信息，可以帮助诊断测试问题。

#### 2.4 测试错误处理

在测试中处理错误是确保测试可靠性的关键。通过适当的错误处理，可以捕捉到潜在的错误并进行调试。

**示例**:
```go
func TestDivide(t *testing.T) {
    result, err := Divide(4, 2)
    if err != nil {
        t.Fatalf("Divide(4, 2) failed: %v", err)
    }
    expected := 2
    if result != expected {
        t.Errorf("Divide(4, 2) = %d; want %d", result, expected)
    }
}
```

- `t.Fatalf` 用于在测试中遇到致命错误时停止测试并记录错误。

### 总结

基本测试是确保代码正确性和稳定性的基础。通过创建测试文件和测试函数，运行测试，记录和处理测试输出，可以有效地验证代码的功能是否符合预期。Go 的测试框架提供了简单而强大的工具来支持这些功能，使得编写和管理测试变得更加高效。