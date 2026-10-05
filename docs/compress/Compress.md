### 2. compress 包

Go 标准库的 `compress` 包下有 `compress/gzip`、`compress/zlib` 和 `compress/bzip2` 三个子包，本节分别给出压缩和解压的代码示例。

#### 2.1 `compress/gzip`

`compress/gzip` 包提供了对 GNU zip (gzip) 格式文件的读写支持。gzip 是一种常用的压缩格式，具有较高的压缩率和快速的解压速度。

##### 2.1.1 基本使用

压缩用 `gzip.Writer`，解压用 `gzip.Reader`。

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

用上面的函数把 `example.txt` 压缩成 `example.txt.gz`，再解压回来。

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

输出：

```plaintext
File compressed successfully
File decompressed successfully
```

并且在当前目录下生成 `example.txt.gz` 和 `example_decompressed.txt` 文件。

#### 2.2 `compress/zlib`

`compress/zlib` 包提供了对 DEFLATE 压缩格式的读写支持。zlib 是一种广泛使用的压缩格式，通常用于网络传输和文件压缩。

##### 2.2.1 基本使用

压缩用 `zlib.Writer`，解压用 `zlib.Reader`。

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

用上面的函数把 `example.txt` 压缩成 `example.txt.zlib`，再解压回来。

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

输出：

```plaintext
File compressed successfully
File decompressed successfully
```

并且在当前目录下生成 `example.txt.zlib` 和 `example_decompressed_zlib.txt` 文件。

#### 2.3 `compress/bzip2`

`compress/bzip2` 包提供了对 bzip2 压缩格式的读取支持。bzip2 是一种压缩率较高的压缩算法，但压缩速度相对较慢。

##### 2.3.1 基本使用

`compress/bzip2` 只提供读取，解压用 `bzip2.Reader`。

```go
import (
    "compress/bzip2"
    "os"
    "io"
)
```

##### 2.3.2 解压 bzip2 文件

**从 bzip2 文件解压数据：**

```go
import (
    "compress/bzip2"
    "io"
    "os"
)

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

**实践案例：**标准库没有 bzip2 的写入端，这里预置一段压缩数据（原始内容是 `hello bzip2`），和上面的函数放进同一个包里编译：

```go
func main() {
    // 压缩后的数据，原始内容为 "hello bzip2\n"
    data := []byte{
        66, 90, 104, 57, 49, 65, 89, 38, 83, 89, 171, 107, 161, 241,
        0, 0, 2, 217, 128, 0, 16, 64, 0, 16, 0, 18, 100, 192, 16, 32,
        0, 49, 0, 211, 77, 4, 0, 30, 163, 239, 78, 81, 162, 7, 139, 185,
        34, 156, 40, 72, 85, 181, 208, 248, 128,
    }
    if err := os.WriteFile("example.bz2", data, 0644); err != nil {
        log.Fatal(err)
    }

    if err := decompressBzip2FromFile("example.bz2", "example_decompressed_bz2.txt"); err != nil {
        log.Fatal(err)
    }
    fmt.Println("File decompressed successfully")

    content, err := os.ReadFile("example_decompressed_bz2.txt")
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("解压内容: %s", content)
}
```

输出：

```plaintext
File decompressed successfully
解压内容: hello bzip2
```

并且在当前目录下生成 `example_decompressed_bz2.txt` 文件，内容为 `hello bzip2`。

---

`compress` 包的三个子包用法都在这里：gzip 和 zlib 读写对称，bzip2 只能读。
