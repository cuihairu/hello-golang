### 2. The compress package

Under the `compress` package of the Go standard library there are three subpackages: `compress/gzip`, `compress/zlib`, and `compress/bzip2`. Below I record the compression and decompression code examples for each.

#### 2.1 `compress/gzip`

The `compress/gzip` package provides reading and writing support for GNU zip (gzip) format files. gzip is a commonly used compression format with a high compression ratio and fast decompression speed.

##### 2.1.1 Basic usage

Use `gzip.Writer` to compress, and `gzip.Reader` to decompress.

```go
import (
    "compress/gzip"
    "os"
    "io"
)
```

##### 2.1.2 Reading and writing gzip files

**Compressing data to a gzip file:**

```go
func compressToFile(inputFile, outputFile string) error {
    // open the input file
    inFile, err := os.Open(inputFile)
    if err != nil {
        return err
    }
    defer inFile.Close()

    // create the output file
    outFile, err := os.Create(outputFile)
    if err != nil {
        return err
    }
    defer outFile.Close()

    // create a gzip.Writer
    gzWriter := gzip.NewWriter(outFile)
    defer gzWriter.Close()

    // write the input file's data to the gzip.Writer
    _, err = io.Copy(gzWriter, inFile)
    return err
}
```

**Decompressing data from a gzip file:**

```go
func decompressFromFile(inputFile, outputFile string) error {
    // open the input file
    inFile, err := os.Open(inputFile)
    if err != nil {
        return err
    }
    defer inFile.Close()

    // create a gzip.Reader
    gzReader, err := gzip.NewReader(inFile)
    if err != nil {
        return err
    }
    defer gzReader.Close()

    // create the output file
    outFile, err := os.Create(outputFile)
    if err != nil {
        return err
    }
    defer outFile.Close()

    // write the gzip.Reader's data to the output file
    _, err = io.Copy(outFile, gzReader)
    return err
}
```

##### 2.1.3 Practice case

Suppose we have a text file `example.txt` with the following content:

```plaintext
Hello, Gopher!
This is a test file for gzip compression.
```

Use the functions above to compress `example.txt` into `example.txt.gz`, then decompress it back.

```go
func main() {
    inputFile := "example.txt"
    compressedFile := "example.txt.gz"
    decompressedFile := "example_decompressed.txt"

    // compress the file
    err := compressToFile(inputFile, compressedFile)
    if (err != nil) {
        log.Fatal(err)
    }
    fmt.Println("File compressed successfully")

    // decompress the file
    err = decompressFromFile(compressedFile, decompressedFile)
    if (err != nil) {
        log.Fatal(err)
    }
    fmt.Println("File decompressed successfully")
}
```

Output:

```plaintext
File compressed successfully
File decompressed successfully
```

And it generates `example.txt.gz` and `example_decompressed.txt` files in the current directory.

#### 2.2 `compress/zlib`

The `compress/zlib` package provides reading and writing support for the DEFLATE compression format. zlib is a widely used compression format, typically for network transfer and file compression.

##### 2.2.1 Basic usage

Use `zlib.Writer` to compress, and `zlib.Reader` to decompress.

```go
import (
    "compress/zlib"
    "os"
    "io"
)
```

##### 2.2.2 Reading and writing zlib data

**Compressing data to a zlib file:**

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

**Decompressing data from a zlib file:**

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

##### 2.2.3 Practice case

Use the functions above to compress `example.txt` into `example.txt.zlib`, then decompress it back.

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

Output:

```plaintext
File compressed successfully
File decompressed successfully
```

And it generates `example.txt.zlib` and `example_decompressed_zlib.txt` files in the current directory.

#### 2.3 `compress/bzip2`

The `compress/bzip2` package provides read support for the bzip2 compression format. bzip2 is a compression algorithm with a high compression ratio, but it compresses relatively slowly.

##### 2.3.1 Basic usage

`compress/bzip2` only supports reading; use `bzip2.Reader` to decompress.

```go
import (
    "compress/bzip2"
    "os"
    "io"
)
```

##### 2.3.2 Decompressing bzip2 files

**Decompressing data from a bzip2 file:**

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

**Practice case:** the standard library has no bzip2 writer, so here we preset a chunk of compressed data (the original content is `hello bzip2`); compile it in the same package as the function above:

```go
func main() {
    // the compressed data; the original content is "hello bzip2\n"
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

Output:

```plaintext
File decompressed successfully
解压内容: hello bzip2
```

And it generates `example_decompressed_bz2.txt` in the current directory, containing `hello bzip2`.

---

That covers all three subpackages of the `compress` package: gzip and zlib have symmetric read and write, bzip2 is read-only.

## References

- [compress/gzip standard library](https://pkg.go.dev/compress/gzip)
- [compress/flate standard library](https://pkg.go.dev/compress/flate)

## Sibling pages

- [Advanced](/compress/Advanced.md)
- [Archive](/compress/Archive.md)
- [Composite](/compress/Composite.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Advanced](/compress/Advanced.md)
- [Archive](/compress/Archive.md)
- [Composite](/compress/Composite.md)
- [ErrHandleAndTest](/compress/ErrHandleAndTest.md)
