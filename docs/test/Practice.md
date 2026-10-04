### 测试最佳实践

测试保证改动没有把别处弄坏。Go 的测试写在 `_test.go` 文件里，用 `go test` 运行，下面按可维护性、覆盖率、策略、异常处理和 CI 五块讲。

#### 8.1 编写可维护的测试代码

1. **保持测试简洁**:
   - 测试代码不堆复杂逻辑。
   - 每个测试函数专注于一个特定功能或行为。

2. **使用表驱动测试**:
   - 通过表驱动测试（table-driven tests）组织测试用例，便于维护和扩展。
   - 定义一个结构体数组，描述各种输入和预期输出，然后循环执行测试。

   **示例**:
   ```go
   // example_test.go
   package example

   import "testing"

   func TestAdd(t *testing.T) {
       tests := []struct {
           a, b, expected int
       }{
           {1, 1, 2},
           {2, 2, 4},
           {2, 3, 5},
       }

       for _, test := range tests {
           result := Add(test.a, test.b)
           if result != test.expected {
               t.Errorf("Add(%d, %d) = %d; want %d", test.a, test.b, result, test.expected)
           }
       }
   }
   ```

3. **确保测试具有描述性**:
   - 测试函数名应清晰描述测试的目的和预期行为。
   - 使用 `t.Error` 或 `t.Errorf` 输出明确的错误信息，帮助快速定位问题。

4. **组织测试文件**:
   - 将测试代码放在与被测试代码相同的包中，并放在 `_test.go` 文件中。
   - 根据功能模块组织测试文件，保持代码结构清晰。

#### 8.2 测试覆盖率

1. **监控测试覆盖率**:
   - 使用 Go 的内置覆盖率工具来检查测试覆盖率，并确保重要代码路径被覆盖。
   - 定期查看覆盖率报告，识别未被测试的代码部分。

2. **不要过度追求高覆盖率**:
   - 高覆盖率并不等于高质量测试。确保测试用例覆盖实际业务逻辑和关键路径。

3. **结合其他测试类型**:
   - 除了单元测试，还应包括集成测试、端到端测试等，以确保全面的测试覆盖。

#### 8.3 高效的测试策略

1. **避免测试副作用**:
   - 测试应独立且无副作用，每个测试应在相同的初始状态下运行。
   - 使用 `setup` 和 `teardown` 函数来初始化和清理测试环境。

2. **使用 Mock 和 Stub**:
   - 使用模拟对象（mock）和桩（stub）来隔离测试，避免与外部系统的依赖（如数据库、网络服务）。
   - 常用的库是 `gomock` 和 `testify`。

3. **编写性能测试**:
   - 使用基准测试（Benchmarking）来评估代码的性能，并确保在性能方面满足需求。
   - 定期运行性能测试，以监控性能变化和优化代码。

   **示例**:
   ```go
   // example_benchmark_test.go
   package example

   import "testing"

   func BenchmarkAdd(b *testing.B) {
       for i := 0; i < b.N; i++ {
           Add(1, 2)
       }
   }
   ```

4. **并行测试**:
   - 利用 Go 的并发特性，通过 `t.Parallel()` 运行测试，缩短测试时间。
   - 确保测试代码线程安全，不会导致数据竞争。

   **示例**:
   ```go
   func TestParallel(t *testing.T) {
       t.Parallel()
       // 测试逻辑
   }
   ```

#### 8.4 异常处理和错误处理

1. **测试异常情况**:
   - 编写测试用例来验证函数在异常输入或错误条件下的行为。
   - 使用 `t.Errorf` 输出清晰的错误信息，帮助定位问题。

2. **验证错误返回值**:
   - 确保函数在处理错误时返回正确的错误信息，并对错误进行适当的处理。
   - 使用 `assert.Error` 等断言方法检查错误。

   **示例**:
   ```go
   func TestErrorHandling(t *testing.T) {
       _, err := Divide(1, 0)
       if err == nil {
           t.Errorf("Expected error, got nil")
       }
   }
   ```

#### 8.5 测试的自动化和持续集成

1. **自动化测试运行**:
   - 将测试集成到持续集成（CI）管道中，确保每次代码变更时都自动运行测试。
   - 使用 CI 工具（如 GitHub Actions、GitLab CI、Jenkins）自动执行测试并生成报告。

2. **测试报告和反馈**:
   - 配置 CI 工具生成测试报告，并在每次构建后查看测试结果。
   - 设置警报和通知，以便在测试失败时及时响应和修复问题。

#### 8.6 实践示例

```go
// example_test.go
package example

import (
    "testing"
)

// 被测试的函数
func Add(a, b int) int {
    return a + b
}

// 单元测试
func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d; want 5", result)
    }
}

// 并行测试
func TestAddParallel(t *testing.T) {
    t.Parallel()
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d; want 5", result)
    }
}

// 基准测试
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(2, 3)
    }
}
```

### 总结

表驱动测试、基准测试和 `t.Parallel()` 都是标准库 `testing` 自带的能力，覆盖率靠内置工具查，mock 和断言用 `gomock`、`testify`。把这些挂到 CI 上，每次提交自动跑一遍。