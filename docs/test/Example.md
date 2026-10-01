### 示例测试

示例测试（Example Tests）是 Go 测试框架的一种特殊形式，旨在通过提供具体的示例和预期结果来验证代码的行为。与常规测试和基准测试不同，示例测试通常用于展示函数的用法和验证示例输出是否符合预期。

#### 4.1 示例测试的定义

示例测试是以 `ExampleXxx` 为名称的函数，其中 `Xxx` 是示例名称，`Example` 是前缀。示例测试的签名为 `func ExampleXxx()`, 并且没有参数和返回值。示例测试通常会通过标准输出（`fmt.Println`）打印预期的结果。

**示例**:
```go
// math.go
package math

import "fmt"

// Add 返回两个整数的和
func Add(a, b int) int {
    return a + b
}

// math_test.go
package math

import "fmt"

// ExampleAdd 展示 Add 函数的用法
func ExampleAdd() {
    result := Add(2, 3)
    fmt.Println(result)
    // Output: 5
}
```

在上述代码中：
- `ExampleAdd` 是示例测试函数，展示了 `Add` 函数的用法。
- `fmt.Println(result)` 打印出函数的结果。
- 注释 `// Output: 5` 指定了期望的输出结果。

#### 4.2 运行示例测试

示例测试可以通过 `go test` 命令运行。当运行测试时，Go 测试框架会执行所有的示例测试，并检查其输出是否与注释中的期望结果匹配。

**基本命令**:
```sh
go test
```

- `go test` 会自动运行所有的示例测试，并检查实际输出与预期输出是否匹配。

#### 4.3 示例测试的输出

示例测试的输出被用来验证示例代码的正确性。在测试执行过程中，Go 测试框架会比较实际输出和预期输出。如果输出不匹配，测试将失败，并显示错误信息。

**示例输出**:
```sh
go test
```
```
--- FAIL: ExampleAdd (0.00s)
    math_test.go:12: example output does not match expectation:
        got: 6
        want: 5
```

- `--- FAIL` 表示测试失败。
- 错误信息显示实际输出与期望输出不匹配。

#### 4.4 示例测试的用途

1. **文档化**：示例测试可以作为代码的文档，展示函数的用法和预期行为。
2. **验证示例**：确保代码示例在文档中是正确的，并且随着代码的变更不会破坏示例的正确性。
3. **教学**：帮助新手理解如何使用特定的函数或方法，通过实际示例展示函数的行为。

#### 4.5 编写示例测试的最佳实践

1. **明确预期输出**：确保示例测试的注释中包含明确的预期输出，以便正确验证结果。
2. **简洁明了**：编写简洁的示例代码，专注于展示函数的基本用法和预期行为。
3. **覆盖边界条件**：考虑添加示例测试来展示函数在不同输入条件下的行为。

**示例**:
```go
// ExampleAddNegative 展示 Add 函数处理负数的用法
func ExampleAddNegative() {
    result := Add(-2, -3)
    fmt.Println(result)
    // Output: -5
}

// ExampleAddZero 展示 Add 函数处理零的用法
func ExampleAddZero() {
    result := Add(0, 5)
    fmt.Println(result)
    // Output: 5
}
```

### 总结

示例测试在 Go 语言中提供了一种验证代码示例的有效方法。通过编写示例测试，可以展示函数的用法，确保示例代码的正确性，并作为文档的一部分来帮助理解函数的行为。示例测试不仅对开发者有帮助，还可以在团队协作中作为清晰的代码示例和文档支持。