### 3. archive 包

在本节中，我们将详细介绍 Go 语言标准库中的 `archive` 包，包括 `archive/tar` 和 `archive/zip`。我们将展示如何使用这些包进行归档和解压操作，并提供实际的代码示例。

#### 3.1 `archive/tar`

`archive/tar` 包提供了对 tar 格式文件的读写支持。tar 格式常用于将多个文件和目录打包成一个文件。

##### 3.1.1 基本使用

要使用 `archive/tar` 包，需要导入该包并创建 `tar.Writer` 或 `tar.Reader` 来进行归档和解压操作。

```go
import (
    "archive/tar"
    "os"
    "io"
)
```

##### 3.1.2 创建和解压 tar 文件

**创建 tar 文件：**

```go
func createTar(outputFile string, files []string) error {
    outFile, err := os.Create(outputFile)
    if err != nil {
        return err
    }
    defer outFile.Close()

    tarWriter := tar.NewWriter(outFile)
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

    header := &tar.Header{
        Name: filePath,
        Size: stat.Size(),
        Mode: int64(stat.Mode()),
        ModTime: stat.ModTime(),
    }
    err = tw.WriteHeader(header)
    if err != nil {
        return err
    }

    _, err = io.Copy(tw, file)
    return err
}
```

**解压 tar 文件：**

```go
func extractTar(inputFile, outputDir string) error {
    inFile, err := os.Open(inputFile)
    if err != nil {
        return err
    }
    defer inFile.Close()

    tarReader := tar.NewReader(inFile)

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

##### 3.1.3 实践案例

假设我们有两个文本文件 `file1.txt` 和 `file2.txt`，内容如下：

```plaintext
file1.txt:
Hello, this is file1.

file2.txt:
Hello, this is file2.
```

我们可以使用上面的函数将它们打包成 `archive.tar`，然后再解压到 `output` 目录。

```go
func main() {
    files := []string{"file1.txt", "file2.txt"}
    tarFile := "archive.tar"
    outputDir := "output"

    // 创建 tar 文件
    err := createTar(tarFile, files)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Tar file created successfully")

    // 解压 tar 文件
    err = extractTar(tarFile, outputDir)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Tar file extracted successfully")
}
```

运行此代码后，我们会看到控制台输出：

```plaintext
Tar file created successfully
Tar file extracted successfully
```

并且在当前目录下生成 `archive.tar` 文件和 `output` 目录，其中包含 `file1.txt` 和 `file2.txt` 文件。

#### 3.2 `archive/zip`

`archive/zip` 包提供了对 zip 格式文件的读写支持。zip 格式是一种常见的压缩和归档格式。

##### 3.2.1 基本使用

要使用 `archive/zip` 包，需要导入该包并创建 `zip.Writer` 或 `zip.Reader` 来进行归档和解压操作。

```go
import (
    "archive/zip"
    "os"
    "io"
    "path/filepath"
)
```

##### 3.2.2 创建和解压 zip 文件

**创建 zip 文件：**

```go
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

**解压 zip 文件：**

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

##### 3.2.3 实践案例

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

