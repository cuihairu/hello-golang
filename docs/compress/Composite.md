### 4. 综合应用

在本节中，我们将展示如何将前面介绍的 `compress` 包和 `archive` 包结合使用，以实现更复杂的归档和压缩操作。我们将具体讲解 `tar.gz` 和 `zip` 的创建和解压方法，并提供实际的代码示例。

#### 4.1 tar.gz 归档和压缩

`tar.gz` 文件是通过先使用 tar 将多个文件归档成一个 tar 文件，然后使用 gzip 对 tar 文件进行压缩而生成的。

##### 4.1.1 创建 tar.gz 文件

要创建 `tar.gz` 文件，我们需要将文件先归档成 tar 文件，然后压缩成 gzip 文件。

```go
import (
    "compress/gzip"
    "archive/tar"
    "os"
    "io"
)

func createTarGz(outputFile string, files []string) error {
    outFile, err := os.Create(outputFile)
    if err != nil {
        return err
    }
    defer outFile.Close()

    gzipWriter := gzip.NewWriter(outFile)
    defer gzipWriter.Close()

    tarWriter := tar.NewWriter(gzipWriter)
    defer tarWriter.Close()

    for _, file := range files {
        err := addFileToTar(tarWriter, file)
        if err != nil {
            return err
        }
    }

    return nil
}
```

##### 4.1.2 解压 tar.gz 文件

解压 `tar.gz` 文件需要先解压 gzip 层，然后解压 tar 层。

```go
func extractTarGz(inputFile, outputDir string) error {
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

    tarReader := tar.NewReader(gzipReader)

    for {
        header, err := tarReader.Next()
        if err == io.EOF {
            break
        }
        if err != nil {
            return err
        }

        outputFile := outputDir + "/" + header.Name
        err = os.MkdirAll(outputDir+"/"+header.Name, os.FileMode(header.Mode))
        if err != nil {
            return err
        }

        if header.Typeflag == tar.TypeDir {
            continue
        }

        outFile, err := os.Create(outputFile)
        if err != nil {
            return err
        }
        defer outFile.Close()

        _, err = io.Copy(outFile, tarReader)
        if err != nil {
            return err
        }
    }

    return nil
}
```

##### 4.1.3 实践案例

我们可以使用上面的函数将 `file1.txt` 和 `file2.txt` 打包成 `archive.tar.gz`，然后再解压到 `output` 目录。

```go
func main() {
    files := []string{"file1.txt", "file2.txt"}
    tarGzFile := "archive.tar.gz"
    outputDir := "output"

    // 创建 tar.gz 文件
    err := createTarGz(tarGzFile, files)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Tar.gz file created successfully")

    // 解压 tar.gz 文件
    err = extractTarGz(tarGzFile, outputDir)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Tar.gz file extracted successfully")
}
```

运行此代码后，我们会看到控制台输出：

```plaintext
Tar.gz file created successfully
Tar.gz file extracted successfully
```

并且在当前目录下生成 `archive.tar.gz` 文件和 `output` 目录，其中包含 `file1.txt` 和 `file2.txt` 文件。

#### 4.2 zip 压缩多个文件

我们将展示如何将多个文件压缩成一个 zip 文件，并解压该 zip 文件。

##### 4.2.1 压缩多个文件到一个 zip 文件

```go
import (
    "archive/zip"
    "os"
    "io"
    "path/filepath"
)

func createZip(outputFile string, files []string) error {
    outFile, err := os.Create(outputFile)
    if err != nil {
        return err
    }
    defer outFile.Close()

    zipWriter := zip.NewWriter(outFile)
    defer zipWriter.Close()

    for _, file := range files {
        err := addFileToZip(zipWriter, file)
        if err != nil {
            return err
        }
    }

    return nil
}

func addFileToZip(zw *zip.Writer, filePath string) error {
    file, err := os.Open(filePath)
    if err != nil {
        return err
    }
    defer file.Close()

    stat, err := file.Stat()
    if err != nil {
        return err
    }

    header, err := zip.FileInfoHeader(stat)
    if err != nil {
        return err
    }

    header.Name = filepath.Base(filePath)
    header.Method = zip.Deflate

    writer, err := zw.CreateHeader(header)
    if err != nil {
        return err
    }

    _, err = io.Copy(writer, file)
    return err
}
```

##### 4.2.2 解压 zip 文件

```go
func extractZip(inputFile, outputDir string) error {
    zipReader, err := zip.OpenReader(inputFile)
    if err != nil {
        return err
    }
    defer zipReader.Close()

    for _, file := range zipReader.File {
        outputFile := filepath.Join(outputDir, file.Name)

        if file.FileInfo().IsDir() {
            os.MkdirAll(outputFile, os.ModePerm)
            continue
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
        if err != nil {
            return err
        }
    }

    return nil
}
```

##### 4.2.3 实践案例

我们可以使用上面的函数将 `file1.txt` 和 `file2.txt` 打包成 `archive.zip`，然后再解压到 `output` 目录。

```go
func main() {
    files := []string{"file1.txt", "file2.txt"}
    zipFile := "archive.zip"
    outputDir := "output"

    // 创建 zip 文件
    err := createZip(zipFile, files)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Zip file created successfully")

    // 解压 zip 文件
    err = extractZip(zipFile, outputDir)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Zip file extracted successfully")
}
```

运行此代码后，我们会看到控制台输出：

```plaintext
Zip file created successfully
Zip file extracted successfully
```

并且在当前目录下生成 `archive.zip` 文件和 `output` 目录，其中包含 `file1.txt` 和 `file2.txt` 文件。
