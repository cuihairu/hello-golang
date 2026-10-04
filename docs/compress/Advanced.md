### 5. 高级应用

本节讲两件事：用 Goroutine 并行压缩和解压多个文件，以及用流式读写处理大文件，避免把整个文件读进内存。

#### 5.1 并行压缩和解压

文件多的时候，可以起多个 goroutine 同时做压缩和解压。

##### 5.1.1 使用 Goroutines 进行并行处理

**并行压缩多个文件：**

```go
import (
    "archive/zip"
    "os"
    "io"
    "path/filepath"
    "sync"
)

func createZipParallel(outputFile string, files []string) error {
    outFile, err := os.Create(outputFile)
    if err != nil {
        return err
    }
    defer outFile.Close()

    zipWriter := zip.NewWriter(outFile)
    defer zipWriter.Close()

    var wg sync.WaitGroup
    var mu sync.Mutex // 注意：zip.Writer 不是并发安全的，写入必须用锁串行化
    errChan := make(chan error, len(files))

    for _, file := range files {
        wg.Add(1)
        go func(filePath string) {
            defer wg.Done()
            mu.Lock()
            defer mu.Unlock()
            if err := addFileToZip(zipWriter, filePath); err != nil {
                errChan <- err
            }
        }(file)
    }

    wg.Wait()
    close(errChan)

    if len(errChan) > 0 {
        return <-errChan
    }

    return nil
}
```

> 注意：`zip.Writer` 本身不是并发安全的，多个 goroutine 直接并发调用会产生数据竞争（可用 `go run -race` 验证）。上面的实现通过互斥锁保证同一时刻只有一个 goroutine 在写入；如需真正并行的压缩计算，可以先并行读取并压缩到内存，再串行写入 `zip.Writer`。

**并行解压多个文件：**

```go
func extractZipParallel(inputFile, outputDir string) error {
    zipReader, err := zip.OpenReader(inputFile)
    if err != nil {
        return err
    }
    defer zipReader.Close()

    var wg sync.WaitGroup
    errChan := make(chan error, len(zipReader.File))

    for _, file := range zipReader.File {
        wg.Add(1)
        go func(f *zip.File) {
            defer wg.Done()
            if err := extractFileFromZip(f, outputDir); err != nil {
                errChan <- err
            }
        }(file)
    }

    wg.Wait()
    close(errChan)

    if len(errChan) > 0 {
        return <-errChan
    }

    return nil
}

func extractFileFromZip(file *zip.File, outputDir string) error {
    outputFile := filepath.Join(outputDir, file.Name)

    if file.FileInfo().IsDir() {
        return os.MkdirAll(outputFile, os.ModePerm)
    }

    if err := os.MkdirAll(filepath.Dir(outputFile), os.ModePerm); err != nil {
        return err
    }

    outFile, err := os.OpenFile(outputFile, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, file.Mode())
    if err != nil {
        return err
    }
    defer outFile.Close()

    rc, err := file.Open()
    if err != nil {
        return err
    }
    defer rc.Close()

    _, err = io.Copy(outFile, rc)
    return err
}
```

##### 5.1.2 性能优化

并行化之后有三处值得调整：把小块读写合并成批量 I/O，减少磁盘往返；给 goroutine 的数量设上限，避免开太多导致内存占用过高；读写走缓冲区，降低小块数据带来的开销。

##### 5.1.3 实践案例

假设我们有多个大文件需要并行压缩成 `archive.zip`，然后解压到 `output` 目录。

```go
func main() {
    files := []string{"file1.txt", "file2.txt", "file3.txt"}
    zipFile := "archive.zip"
    outputDir := "output"

    // 并行创建 zip 文件
    err := createZipParallel(zipFile, files)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Parallel zip file created successfully")

    // 并行解压 zip 文件
    err = extractZipParallel(zipFile, outputDir)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Parallel zip file extracted successfully")
}
```

运行此代码后，我们会看到控制台输出：

```plaintext
Parallel zip file created successfully
Parallel zip file extracted successfully
```

并且在当前目录下生成 `archive.zip` 文件和 `output` 目录，其中包含多个文件。

#### 5.2 大文件处理

处理大文件的关键是不要一次性把它读进内存，流式读写配合分块处理即可。

##### 5.2.1 流式处理大文件

**压缩大文件：**

```go
import (
    "compress/gzip"
    "os"
    "io"
)

func compressLargeFile(inputFile, outputFile string) error {
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

    gzipWriter := gzip.NewWriter(outFile)
    defer gzipWriter.Close()

    _, err = io.Copy(gzipWriter, inFile)
    return err
}
```

**解压大文件：**

```go
func decompressLargeFile(inputFile, outputFile string) error {
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
```

##### 5.2.2 内存管理

在处理大文件时，应注意以下内存管理策略：

1. **分块处理**：将文件分块读取和写入，避免一次性加载整个文件。
2. **使用缓冲区**：利用缓冲区来提高 I/O 操作的效率。
3. **内存回收**：定期进行垃圾回收，释放不再使用的内存。

##### 5.2.3 实践案例

我们可以使用上面的函数将一个大文件 `largefile.txt` 压缩成 `largefile.gz`，然后再解压回 `decompressed_largefile.txt`。

```go
func main() {
    inputFile := "largefile.txt"
    compressedFile := "largefile.gz"
    decompressedFile := "decompressed_largefile.txt"

    // 压缩大文件
    err := compressLargeFile(inputFile, compressedFile)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Large file compressed successfully")

    // 解压大文件
    err = decompressLargeFile(compressedFile, decompressedFile)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Large file decompressed successfully")
}
```

运行此代码后，我们会看到控制台输出：

```plaintext
Large file compressed successfully
Large file decompressed successfully
```

并且在当前目录下生成 `largefile.gz` 文件和 `decompressed_largefile.txt` 文件。
