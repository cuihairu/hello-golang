### 5. Advanced usage

This page records two approaches: compressing and decompressing multiple files in parallel with goroutines, and handling large files with streaming reads and writes so the whole file never has to be read into memory.

#### 5.1 Parallel compression and decompression

When there are many files, you can spin up multiple goroutines to compress and decompress them at the same time.

##### 5.1.1 Parallel processing with goroutines

**Compressing multiple files in parallel:**

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
    var mu sync.Mutex // note: zip.Writer is not concurrency-safe; writes must be serialized with a lock
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

func addFileToZip(zipWriter *zip.Writer, filePath string) error {
    f, err := os.Open(filePath)
    if err != nil {
        return err
    }
    defer f.Close()

    w, err := zipWriter.Create(filepath.Base(filePath))
    if err != nil {
        return err
    }

    _, err = io.Copy(w, f)
    return err
}
```

> Note: `zip.Writer` itself is not concurrency-safe; concurrent calls from multiple goroutines cause a data race (you can verify with `go run -race`). The implementation above uses a mutex to guarantee that only one goroutine writes at a time; if you want truly parallel compression, read and compress into memory in parallel first, then write to the `zip.Writer` serially.

**Decompressing multiple files in parallel:**

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

##### 5.1.2 Performance tuning

After parallelizing, three places are worth tuning: merge small chunk reads and writes into batched I/O to cut disk round trips; cap the number of goroutines so you don't open so many that memory usage balloons; and run reads and writes through buffers to reduce the overhead of small chunks.

##### 5.1.3 Practice case

Suppose we have several large files to compress in parallel into `archive.zip`, then extract into the `output` directory.

```go
func main() {
    files := []string{"file1.txt", "file2.txt", "file3.txt"}
    zipFile := "archive.zip"
    outputDir := "output"

    // create the zip file in parallel
    err := createZipParallel(zipFile, files)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Parallel zip file created successfully")

    // extract the zip file in parallel
    err = extractZipParallel(zipFile, outputDir)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Parallel zip file extracted successfully")
}
```

Running this code, we see the console output:

```plaintext
Parallel zip file created successfully
Parallel zip file extracted successfully
```

And it generates `archive.zip` and an `output` directory in the current directory, containing multiple files.

#### 5.2 Handling large files

The key to handling large files is not reading one into memory wholesale; streaming reads and writes combined with chunked processing is enough.

##### 5.2.1 Streaming large files

**Compressing a large file:**

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

**Decompressing a large file:**

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

##### 5.2.2 Memory management

When handling large files, keep the following memory management strategies in mind:

1. **Chunked processing**: read and write the file in chunks, avoiding loading the whole file at once.
2. **Use buffers**: use buffers to improve the efficiency of I/O operations.
3. **Memory reclamation**: run garbage collection periodically to release memory that is no longer in use.

##### 5.2.3 Practice case

We can use the functions above to compress a large file `largefile.txt` into `largefile.gz`, then decompress it back into `decompressed_largefile.txt`.

```go
func main() {
    inputFile := "largefile.txt"
    compressedFile := "largefile.gz"
    decompressedFile := "decompressed_largefile.txt"

    // compress the large file
    err := compressLargeFile(inputFile, compressedFile)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Large file compressed successfully")

    // decompress the large file
    err = decompressLargeFile(compressedFile, decompressedFile)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Large file decompressed successfully")
}
```

Running this code, we see the console output:

```plaintext
Large file compressed successfully
Large file decompressed successfully
```

And it generates `largefile.gz` and `decompressed_largefile.txt` files in the current directory.

## References

- [compress/gzip standard library](https://pkg.go.dev/compress/gzip)
- [compress/flate standard library](https://pkg.go.dev/compress/flate)

## Sibling pages

- [Archive](/compress/Archive.md)
- [Composite](/compress/Composite.md)
- [Compress](/compress/Compress.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Archive](/compress/Archive.md)
- [Composite](/compress/Composite.md)
- [Compress](/compress/Compress.md)
- [ErrHandleAndTest](/compress/ErrHandleAndTest.md)
- [Readme](/compress/Readme.md)
