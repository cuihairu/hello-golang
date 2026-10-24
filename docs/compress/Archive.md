### 3. The archive package

The `archive/tar` and `archive/zip` under the `archive` package handle reading and writing tar and zip respectively. Below are the packing and unpacking code.

#### 3.1 `archive/tar`

The `archive/tar` package provides reading and writing support for tar format files. The tar format is commonly used to bundle multiple files and directories into a single file.

##### 3.1.1 Basic usage

To use the `archive/tar` package, you need to import it and create a `tar.Writer` or `tar.Reader` to perform archiving and extraction.

```go
import (
    "archive/tar"
    "os"
    "io"
    "path/filepath"
)
```

##### 3.1.2 Creating and extracting tar files

**Creating a tar file:**

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

**Extracting a tar file:**

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

        // note: directory entries can't be created directly with os.Create, and file entries also need their parent directory to exist first
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

> Note: the code above uses the `path/filepath` package; make sure you imported `"path/filepath"`. The original implementation passed the file name straight to `os.MkdirAll`, which causes a `mkdir output/file1.txt: not a directory` style error when creating the file because a directory of the same name already exists.

##### 3.1.3 Practice case

Suppose we have two text files `file1.txt` and `file2.txt`, with the following content:

```plaintext
file1.txt:
Hello, this is file1.

file2.txt:
Hello, this is file2.
```

Use the functions above to pack them into `archive.tar`, then extract them into the `output` directory.

```go
func main() {
    files := []string{"file1.txt", "file2.txt"}
    tarFile := "archive.tar"
    outputDir := "output"

    // create the tar file
    err := createTar(tarFile, files)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Tar file created successfully")

    // extract the tar file
    err = extractTar(tarFile, outputDir)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Tar file extracted successfully")
}
```

Output when run:

```plaintext
Tar file created successfully
Tar file extracted successfully
```

And it generates `archive.tar` and an `output` directory in the current directory, containing `file1.txt` and `file2.txt`.

#### 3.2 `archive/zip`

The `archive/zip` package provides reading and writing support for zip format files. zip is a common compression and archive format.

##### 3.2.1 Basic usage

To use the `archive/zip` package, you need to import it and create a `zip.Writer` or `zip.Reader` to perform archiving and extraction.

```go
import (
    "archive/zip"
    "os"
    "io"
    "path/filepath"
)
```

##### 3.2.2 Creating and extracting zip files

**Creating a zip file:**

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

**Extracting a zip file:**

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

##### 3.2.3 Practice case

Use the functions above to pack `file1.txt` and `file2.txt` into `archive.zip`, then extract them into the `output` directory.

```go
func main() {
    files := []string{"file1.txt", "file2.txt"}
    zipFile := "archive.zip"
    outputDir := "output"

    // create the zip file
    err := createZip(zipFile, files)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Zip file created successfully")

    // extract the zip file
    err = extractZip(zipFile, outputDir)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Zip file extracted successfully")
}
```

Output when run:

```plaintext
Zip file created successfully
Zip file extracted successfully
```

And it generates `archive.zip` and an `output` directory in the current directory, containing `file1.txt` and `file2.txt`.

## References

- [compress/gzip standard library](https://pkg.go.dev/compress/gzip)
- [compress/flate standard library](https://pkg.go.dev/compress/flate)
- [archive/zip standard library](https://pkg.go.dev/archive/zip)
- [archive/tar standard library](https://pkg.go.dev/archive/tar)

## Sibling pages

- [Advanced](/compress/Advanced.md)
- [Composite](/compress/Composite.md)
- [Compress](/compress/Compress.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Advanced](/compress/Advanced.md)
- [Composite](/compress/Composite.md)
- [Compress](/compress/Compress.md)
- [ErrHandleAndTest](/compress/ErrHandleAndTest.md)
- [Readme](/compress/Readme.md)
