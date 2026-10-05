### 4. 综合应用

把前面介绍的 `compress` 包和 `archive` 包结合使用，就能做"先归档、再压缩"这类组合操作。这一节讲 `tar.gz` 和 `zip` 的创建与解压。

#### 4.1 tar.gz 归档和压缩

`tar.gz` 是先用 tar 把多个文件归档成一个 tar 文件，再用 gzip 压缩得到的。

##### 4.1.1 创建 tar.gz 文件

创建时分两步：先把文件归档成 tar，再套一层 gzip。

```go
import (
    "compress/gzip"
    "archive/tar"
    "os"
    "io"
    "path/filepath"
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

func addFileToTar(tw *tar.Writer, filePath string) error {
    file, err := os.Open(filePath)
    if err != nil {
        return err
    }
    defer file.Close()

    stat, err := file.Stat()
    if err != nil {
        return err
    }

    header, err := tar.FileInfoHeader(stat, stat.Name())
    if err != nil {
        return err
    }
    header.Name = filepath.Base(filePath)

    if err := tw.WriteHeader(header); err != nil {
        return err
    }
    _, err = io.Copy(tw, file)
    return err
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

        // 注意：目录条目不能用 os.Create 直接创建，文件条目也要先确保父目录存在
        target := filepath.Join(outputDir, header.Name)

        if header.Typeflag == tar.TypeDir {
            if err := os.MkdirAll(target, os.FileMode(header.Mode)); err != nil {
                return err
            }
            continue
        }

        if err := os.MkdirAll(filepath.Dir(target), 0755); err != nil {
            return err
        }

        outFile, err := os.Create(target)
        if err != nil {
            return err
        }

        _, err = io.Copy(outFile, tarReader)
        outFile.Close()
        if err != nil {
            return err
        }
    }

    return nil
}
```

> 注意：上面用到了 `path/filepath` 包，请确保 import 了 `"path/filepath"`。若把文件名直接传给 `os.MkdirAll`，会导致后续 `os.Create` 因同名目录已存在而失败。

##### 4.1.3 实践案例

把 4.1.1 与 4.1.2 的函数和本块的 `main` 放在同一个包里编译。`main` 先自己造出两个输入文件，再把它们打包成 `archive.tar.gz`，解压到 `output` 目录：

```go
func main() {
    // 准备输入文件
    if err := os.WriteFile("file1.txt", []byte("hello tar.gz\n"), 0644); err != nil {
        log.Fatal(err)
    }
    if err := os.WriteFile("file2.txt", []byte("hello tar.gz again\n"), 0644); err != nil {
        log.Fatal(err)
    }

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

运行输出：

```plaintext
Tar.gz file created successfully
Tar.gz file extracted successfully
```

并且在当前目录下生成 `archive.tar.gz` 文件和 `output` 目录，其中包含 `file1.txt` 和 `file2.txt` 文件。

#### 4.2 zip 压缩多个文件

把多个文件压进一个 zip 并解压，用的是 `archive/zip`。

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

把 4.2.1 与 4.2.2 的函数和本块的 `main` 放在同一个包里编译。`main` 先造出两个输入文件，再把它们打进 `archive.zip`，解压到 `output` 目录：

```go
func main() {
    // 准备输入文件
    if err := os.WriteFile("file1.txt", []byte("hello zip\n"), 0644); err != nil {
        log.Fatal(err)
    }
    if err := os.WriteFile("file2.txt", []byte("hello zip again\n"), 0644); err != nil {
        log.Fatal(err)
    }

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

运行输出：

```plaintext
Zip file created successfully
Zip file extracted successfully
```

并且在当前目录下生成 `archive.zip` 文件和 `output` 目录，其中包含 `file1.txt` 和 `file2.txt` 文件。
