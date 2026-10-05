### 6. 错误处理与测试

本节讲压缩和归档操作中的错误处理与测试：常见的错误类型、处理策略，以及怎么写测试用例和性能测试。

#### 6.1 错误处理

在进行压缩和归档操作时，可能会遇到各种错误：文件打不开、没有写权限、格式对不上。错误要在发生的那一刻返回给调用方，别让程序带着坏掉的文件继续往下跑。

##### 6.1.1 常见错误类型

1. **文件不存在**：尝试打开一个不存在的文件时会发生此错误。
2. **权限错误**：尝试访问一个没有权限的文件或目录时会发生此错误。
3. **I/O 错误**：读写文件时发生的输入输出错误。
4. **格式错误**：文件格式不符合预期时发生的错误，如读取 gzip 文件时发现其不是有效的 gzip 格式。

##### 6.1.2 错误处理策略

1. **检查错误并返回**：每次执行可能出错的操作后，都应检查错误并适当地返回或处理。
2. **包装错误**：使用 `fmt.Errorf`（标准库，配合 `%w` 动作符）或 `errors.Wrap`（来自第三方库 `github.com/pkg/errors`，不是标准库）包装错误，提供更多上下文信息。
3. **重试策略**：对于某些临时性错误，可以尝试重试操作。
4. **日志记录**：将错误记录到日志中，以便后续分析和排查。

示例代码：

```go
func compressFile(inputFile, outputFile string) error {
    inFile, err := os.Open(inputFile)
    if err != nil {
        return fmt.Errorf("failed to open input file: %w", err)
    }
    defer inFile.Close()

    outFile, err := os.Create(outputFile)
    if err != nil {
        return fmt.Errorf("failed to create output file: %w", err)
    }
    defer outFile.Close()

    gzipWriter := gzip.NewWriter(outFile)
    defer gzipWriter.Close()

    if _, err := io.Copy(gzipWriter, inFile); err != nil {
        return fmt.Errorf("failed to compress file: %w", err)
    }

    return nil
}
```

#### 6.2 测试压缩与归档

下面分别写单元测试和基准测试，验证压缩功能的正确性和性能。

##### 6.2.1 编写测试用例

使用 Go 的标准库 `testing` 包，可以编写单元测试和集成测试。

示例测试用例：

```go
import (
    "testing"
    "os"
    "io/ioutil"
)

func TestCompressFile(t *testing.T) {
    inputFile := "test_input.txt"
    outputFile := "test_output.gz"

    // 创建测试输入文件
    err := ioutil.WriteFile(inputFile, []byte("Hello, World!"), 0644)
    if err != nil {
        t.Fatalf("failed to create test input file: %v", err)
    }
    defer os.Remove(inputFile)
    defer os.Remove(outputFile)

    // 测试压缩函数
    err = compressFile(inputFile, outputFile)
    if err != nil {
        t.Fatalf("compressFile failed: %v", err)
    }

    // 检查输出文件是否存在
    if _, err := os.Stat(outputFile); os.IsNotExist(err) {
        t.Fatalf("output file does not exist")
    }
}
```

##### 6.2.2 性能测试

用 `testing` 包的 `Benchmark` 函数可以做性能测试，反复跑固定输入，得到每次调用的耗时。

示例性能测试：

```go
import (
    "testing"
    "os"
    "io/ioutil"
)

func BenchmarkCompressFile(b *testing.B) {
    inputFile := "benchmark_input.txt"
    outputFile := "benchmark_output.gz"

    // 创建基准测试输入文件
    err := ioutil.WriteFile(inputFile, []byte("Hello, World!"), 0644)
    if err != nil {
        b.Fatalf("failed to create benchmark input file: %v", err)
    }
    defer os.Remove(inputFile)
    defer os.Remove(outputFile)

    for i := 0; i < b.N; i++ {
        if err := compressFile(inputFile, outputFile); err != nil {
            b.Fatalf("compressFile failed: %v", err)
        }
    }
}
```

##### 6.2.3 实践案例

解压函数同样要测：先生成压缩过的测试文件，再解压，最后对比文件内容。

```go
import (
    "bytes"
    "compress/gzip"
    "io"
    "io/ioutil"
    "os"
    "testing"
)

// compressData 用 gzip 压缩数据，用来生成测试所需的压缩文件内容
func compressData(data []byte) []byte {
    var buf bytes.Buffer
    w := gzip.NewWriter(&buf)
    if _, err := w.Write(data); err != nil {
        panic(err)
    }
    if err := w.Close(); err != nil {
        panic(err)
    }
    return buf.Bytes()
}

// decompressFile 解压 gzip 文件
func decompressFile(inputFile, outputFile string) error {
    inFile, err := os.Open(inputFile)
    if err != nil {
        return err
    }
    defer inFile.Close()

    gzipReader, err := gzip.NewReader(inFile)
    if err != nil {
        return err
    }
    defer gzipReader.Close()

    outFile, err := os.Create(outputFile)
    if err != nil {
        return err
    }
    defer outFile.Close()

    _, err = io.Copy(outFile, gzipReader)
    return err
}

func TestDecompressFile(t *testing.T) {
    inputFile := "test_input.gz"
    outputFile := "test_output.txt"

    // 创建测试压缩文件
    err := ioutil.WriteFile(inputFile, compressData([]byte("Hello, World!")), 0644)
    if err != nil {
        t.Fatalf("failed to create test input file: %v", err)
    }
    defer os.Remove(inputFile)
    defer os.Remove(outputFile)

    // 测试解压函数
    err = decompressFile(inputFile, outputFile)
    if err != nil {
        t.Fatalf("decompressFile failed: %v", err)
    }

    // 检查输出文件内容
    content, err := ioutil.ReadFile(outputFile)
    if err != nil {
        t.Fatalf("failed to read output file: %v", err)
    }
    if string(content) != "Hello, World!" {
        t.Fatalf("unexpected content in output file: %s", content)
    }
}
```

压缩的测试检查输出文件是否存在，解压的测试检查内容是否和原文一致，两条都通过才算这两个函数可用。
