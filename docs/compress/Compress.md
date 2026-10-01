### 2. compress 包

在本节中，我们将详细介绍 Go 语言标准库中的 `compress` 包，包括 `compress/gzip`、`compress/zlib` 和 `compress/bzip2`。我们将展示如何使用这些包进行压缩和解压操作，并提供实际的代码示例。

#### 2.1 `compress/gzip`

`compress/gzip` 包提供了对 GNU zip (gzip) 格式文件的读写支持。gzip 是一种常用的压缩格式，具有较高的压缩率和快速的解压速度。

##### 2.1.1 基本使用

要使用 `compress/gzip` 包，需要导入该包并创建 `gzip.Writer` 或 `gzip.Reader` 来进行压缩和解压操作。

```go
import (
    "compress/gzip"
    "os"
    "io"
)
```

##### 2.1.2 读取和写入 gzip 文件

**压缩数据到 gzip 文件：**

```go
func compressToFile(inputFile, outputFile string) error {
    // 打开输入文件
    inFile, err := os.Open(inputFile)
    if err != nil {
        return err
    }
    defer inFile.Close()

    // 创建输出文件
    outFile, err := os.Create(outputFile)
    if err != nil {
        return err
    }
    defer outFile.Close()

    // 创建 gzip.Writer
    gzWriter := gzip.NewWriter(outFile)
    defer gzWriter.Close()

    // 将输入文件的数据写入 gzip.Writer
    _, err = io.Copy(gzWriter, inFile)
    return err
}
```

**从 gzip 文件解压数据：**

```go
func decompressFromFile(inputFile, outputFile string) error {
    // 打开输入文件
    inFile, err := os.Open(inputFile)
    if err != nil {
        return err
    }
    defer inFile.Close()

    // 创建 gzip.Reader
    gzReader, err := gzip.NewReader(inFile)
    if err != nil {
        return err
    }
    defer gzReader.Close()

    // 创建输出文件
    outFile, err := os.Create(outputFile)
    if err != nil {
        return err
    }
    defer outFile.Close()

    // 将 gzip.Reader 的数据写入输出文件
    _, err = io.Copy(outFile, gzReader)
    return err
}
```

##### 2.1.3 实践案例

假设我们有一个文本文件 `example.txt`，内容如下：

```plaintext
Hello, Gopher!
This is a test file for gzip compression.
```

我们可以使用上面的函数将其压缩成 `example.txt.gz`，然后再解压回来。

```go
func main() {
    inputFile := "example.txt"
    compressedFile := "example.txt.gz"
    decompressedFile := "example_decompressed.txt"

    // 压缩文件
    err := compressToFile(inputFile, compressedFile)
    if (err != nil) {
        log.Fatal(err)
    }
    fmt.Println("File compressed successfully")

    // 解压文件
    err = decompressFromFile(compressedFile, decompressedFile)
    if (err != nil) {
        log.Fatal(err)
    }
    fmt.Println("File decompressed successfully")
}
```

运行此代码后，我们会看到控制台输出：

```plaintext
File compressed successfully
File decompressed successfully
```

并且在当前目录下生成 `example.txt.gz` 和 `example_decompressed.txt` 文件。

#### 2.2 `compress/zlib`

`compress/zlib` 包提供了对 DEFLATE 压缩格式的读写支持。zlib 是一种广泛使用的压缩格式，通常用于网络传输和文件压缩。

##### 2.2.1 基本使用

要使用 `compress/zlib` 包，需要导入该包并创建 `zlib.Writer` 或 `zlib.Reader` 来进行压缩和解压操作。

```go
import (
    "compress/zlib"
    "os"
    "io"
)
```

##### 2.2.2 读取和写入 zlib 数据

**压缩数据到 zlib 文件：**

```go
func compressZlibToFile(inputFile, outputFile string) error {
    inFile, err := os.Open(inputFile)
    if err != nil {
        return err
    }
    defer inFile.Close()

    outFile, err := os.Create(outputFile)
    if err != nil {
        return err
    }
    defer outFile.Close()

    zlibWriter := zlib.NewWriter(outFile)
    defer zlibWriter.Close()

    _, err = io.Copy(zlibWriter, inFile)
    return err
}
```

**从 zlib 文件解压数据：**

```go
func decompressZlibFromFile(inputFile, outputFile string) error {
    inFile, err := os.Open(inputFile)
    if err != nil {
        return err
    }
    defer inFile.Close()

    zlibReader, err := zlib.NewReader(inFile)
    if err != nil {
        return err
    }
    defer zlibReader.Close()

    outFile, err := os.Create(outputFile)
    if err != nil {
        return err
    }
    defer outFile.Close()

    _, err = io.Copy(outFile, zlibReader)
    return err
}
```

##### 2.2.3 实践案例

我们可以使用上面的函数将 `example.txt` 压缩成 `example.txt.zlib`，然后再解压回来。

```go
func main() {
    inputFile := "example.txt"
    compressedFile := "example.txt.zlib"
    decompressedFile := "example_decompressed_zlib.txt"

    err := compressZlibToFile(inputFile, compressedFile)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("File compressed successfully")

    err = decompressZlibFromFile(compressedFile, decompressedFile)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("File decompressed successfully")
}
```

运行此代码后，我们会看到控制台输出：

```plaintext
File compressed successfully
File decompressed successfully
```

并且在当前目录下生成 `example.txt.zlib` 和 `example_decompressed_zlib.txt` 文件。

#### 2.3 `compress/bzip2`

`compress/bzip2` 包提供了对 bzip2 压缩格式的读取支持。bzip2 是一种压缩率较高的压缩算法，但压缩速度相对较慢。

##### 2.3.1 基本使用

要使用 `compress/bzip2` 包，需要导入该包并创建 `bzip2.Reader` 来进行解压操作。

```go
import (
    "compress/bzip2"
    "os"
    "io"
)
```

##### 2.3.2 读取和写入 bzip2 文件

**从 bzip2 文件解压数据：**

```go
func decompressBzip2FromFile(inputFile, outputFile string) error {
    inFile, err := os.Open(inputFile)
    if err != nil {
        return err
    }
    defer inFile.Close()

    bz2Reader := bzip2.NewReader(inFile)

    outFile, err := os.Create(outputFile)
    if err != nil {
        return err
    }
    defer outFile.Close()

    _, err = io.Copy(outFile, bz2Reader)
    return err
}
```

运行此代码后，我们会看到控制台输出：

```plaintext
File decompressed successfully
```

并且在当前目录下生成 `example_decompressed_bz2.txt` 文件。

---

以上是 `compress` 包的基本使用方法，包括 `compress/gzip`、`compress/zlib` 和 `compress/bzip2` 的详细介绍和实际代码示例。接下来，我们将介绍 `archive` 包，探讨如何在 Go 中进行归档操作。