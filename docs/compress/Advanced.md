### 5. 高级应用

本节将探讨 Go 语言中更高级的压缩和归档技术，包括并行压缩和解压大文件的处理方法。我们将介绍如何使用 Goroutines 提高处理效率，以及处理大文件时的流式处理和内存管理技术。

#### 5.1 并行压缩和解压

在处理大量文件或大文件时，并行处理可以显著提高效率。我们可以利用 Go 的 Goroutines 实现并行压缩和解压。

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
    errChan := make(chan error, len(files))

    for _, file := range files {
        wg.Add(1)
        go func(filePath string) {
            defer wg.Done()
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

1. **优化 I/O 操作**：减少磁盘 I/O 操作的频率，如批量读取或写入数据。
2. **控制 Goroutines 数量**：使用有界的 Goroutines 池，避免因过多的 Goroutines 导致内存占用过高。
3. **缓存管理**：使用缓冲区来提高数据读取和写入的效率。

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

在处理大文件时，我们需要考虑内存管理和流式处理，以避免内存溢出和性能问题。

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
