### 4. Combined usage

Combine the `compress` and `archive` packages introduced earlier and you get composed operations like "archive first, then compress". This section covers creating and extracting `tar.gz` and `zip`.

#### 4.1 tar.gz archiving and compression

A `tar.gz` is produced by first archiving multiple files into a tar file with tar, then compressing that with gzip.

##### 4.1.1 Creating a tar.gz file

Creating has two steps: archive the files into tar first, then wrap that in a layer of gzip.

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

##### 4.1.2 Extracting a tar.gz file

Extracting a `tar.gz` file requires decompressing the gzip layer first, then unpacking the tar layer.

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

> Note: the code above uses the `path/filepath` package; make sure you imported `"path/filepath"`. Passing a file name straight to `os.MkdirAll` will cause a later `os.Create` to fail because a directory of the same name already exists.

##### 4.1.3 Practice case

Compile the functions from 4.1.1 and 4.1.2 together with the `main` in this block as one package. `main` first creates two input files itself, then packs them into `archive.tar.gz` and extracts into the `output` directory:

```go
func main() {
    // prepare the input files
    if err := os.WriteFile("file1.txt", []byte("hello tar.gz\n"), 0644); err != nil {
        log.Fatal(err)
    }
    if err := os.WriteFile("file2.txt", []byte("hello tar.gz again\n"), 0644); err != nil {
        log.Fatal(err)
    }

    files := []string{"file1.txt", "file2.txt"}
    tarGzFile := "archive.tar.gz"
    outputDir := "output"

    // create the tar.gz file
    err := createTarGz(tarGzFile, files)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Tar.gz file created successfully")

    // extract the tar.gz file
    err = extractTarGz(tarGzFile, outputDir)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Tar.gz file extracted successfully")
}
```

Output when run:

```plaintext
Tar.gz file created successfully
Tar.gz file extracted successfully
```

And it generates `archive.tar.gz` and an `output` directory in the current directory, containing `file1.txt` and `file2.txt`.

#### 4.2 zipping multiple files with zip

Packing multiple files into a zip and extracting uses `archive/zip`.

##### 4.2.1 Compressing multiple files into a zip file

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

##### 4.2.2 Extracting a zip file

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

##### 4.2.3 Practice case

Compile the functions from 4.2.1 and 4.2.2 together with the `main` in this block as one package. `main` first creates two input files, then packs them into `archive.zip` and extracts into the `output` directory:

```go
func main() {
    // prepare the input files
    if err := os.WriteFile("file1.txt", []byte("hello zip\n"), 0644); err != nil {
        log.Fatal(err)
    }
    if err := os.WriteFile("file2.txt", []byte("hello zip again\n"), 0644); err != nil {
        log.Fatal(err)
    }

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

## Sibling pages

- [Advanced](/compress/Advanced.md)
- [Archive](/compress/Archive.md)
- [Compress](/compress/Compress.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Advanced](/compress/Advanced.md)
- [Archive](/compress/Archive.md)
- [Compress](/compress/Compress.md)
- [ErrHandleAndTest](/compress/ErrHandleAndTest.md)
- [Readme](/compress/Readme.md)
