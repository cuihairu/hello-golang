### 6. Error handling and testing

This page records error handling and testing for compression and archiving operations: common error types, handling strategies, and how to write test cases and performance tests.

#### 6.1 Error handling

While doing compression and archiving operations, you may hit all kinds of errors: a file can't be opened, there's no write permission, the format doesn't match. Return an error to the caller the moment it occurs — don't let the program keep going with a broken file.

##### 6.1.1 Common error types

1. **File does not exist**: this error occurs when trying to open a file that doesn't exist.
2. **Permission error**: this error occurs when trying to access a file or directory you don't have permission for.
3. **I/O error**: an input/output error that occurs while reading from or writing to a file.
4. **Format error**: an error that occurs when a file's format doesn't match expectations, such as discovering while reading a gzip file that it is not a valid gzip format.

##### 6.1.2 Error handling strategies

1. **Check errors and return them**: after every operation that might fail, check for an error and return or handle it appropriately.
2. **Wrap errors**: use `fmt.Errorf` (standard library, with the `%w` verb) or `errors.Wrap` (from the third-party library `github.com/pkg/errors`, not part of the standard library) to wrap errors and provide more context.
3. **Retry strategy**: for some transient errors, you can try retrying the operation.
4. **Logging**: record errors in logs so you can analyze and diagnose them later.

Example code:

```go
func compressFile(inputFile, outputFile string) error {
    inFile, err := os.Open(inputFile)
    if err != nil {
        return fmt.Errorf("failed to open input file: %w", err)
    }
    defer inFile.Close()

    outFile, err := os.Create(outputFile)
    if err != nil {
        return fmt.Errorf("failed to create output file: %w", err)
    }
    defer outFile.Close()

    gzipWriter := gzip.NewWriter(outFile)
    defer gzipWriter.Close()

    if _, err := io.Copy(gzipWriter, inFile); err != nil {
        return fmt.Errorf("failed to compress file: %w", err)
    }

    return nil
}
```

#### 6.2 Testing compression and archiving

Below I write unit tests and benchmarks separately, to verify the correctness and performance of the compression functionality.

##### 6.2.1 Writing test cases

Using Go's standard `testing` package, you can write unit tests and integration tests.

Example test case:

```go
import (
    "testing"
    "os"
    "io/ioutil"
)

func TestCompressFile(t *testing.T) {
    inputFile := "test_input.txt"
    outputFile := "test_output.gz"

    // create the test input file
    err := ioutil.WriteFile(inputFile, []byte("Hello, World!"), 0644)
    if err != nil {
        t.Fatalf("failed to create test input file: %v", err)
    }
    defer os.Remove(inputFile)
    defer os.Remove(outputFile)

    // test the compression function
    err = compressFile(inputFile, outputFile)
    if err != nil {
        t.Fatalf("compressFile failed: %v", err)
    }

    // check that the output file exists
    if _, err := os.Stat(outputFile); os.IsNotExist(err) {
        t.Fatalf("output file does not exist")
    }
}
```

##### 6.2.2 Performance testing

Use the `Benchmark` function in the `testing` package for performance testing: run a fixed input repeatedly and get the time per call.

Example performance test:

```go
import (
    "testing"
    "os"
    "io/ioutil"
)

func BenchmarkCompressFile(b *testing.B) {
    inputFile := "benchmark_input.txt"
    outputFile := "benchmark_output.gz"

    // create the benchmark input file
    err := ioutil.WriteFile(inputFile, []byte("Hello, World!"), 0644)
    if err != nil {
        b.Fatalf("failed to create benchmark input file: %v", err)
    }
    defer os.Remove(inputFile)
    defer os.Remove(outputFile)

    for i := 0; i < b.N; i++ {
        if err := compressFile(inputFile, outputFile); err != nil {
            b.Fatalf("compressFile failed: %v", err)
        }
    }
}
```

##### 6.2.3 Practice case

The decompression function needs testing too: generate a compressed test file first, then decompress it, and finally compare the file contents.

```go
import (
    "bytes"
    "compress/gzip"
    "io"
    "io/ioutil"
    "os"
    "testing"
)

// compressData compresses data with gzip, used to produce the compressed file content the test needs
func compressData(data []byte) []byte {
    var buf bytes.Buffer
    w := gzip.NewWriter(&buf)
    if _, err := w.Write(data); err != nil {
        panic(err)
    }
    if err := w.Close(); err != nil {
        panic(err)
    }
    return buf.Bytes()
}

// decompressFile decompresses a gzip file
func decompressFile(inputFile, outputFile string) error {
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

func TestDecompressFile(t *testing.T) {
    inputFile := "test_input.gz"
    outputFile := "test_output.txt"

    // create the test compressed file
    err := ioutil.WriteFile(inputFile, compressData([]byte("Hello, World!")), 0644)
    if err != nil {
        t.Fatalf("failed to create test input file: %v", err)
    }
    defer os.Remove(inputFile)
    defer os.Remove(outputFile)

    // test the decompression function
    err = decompressFile(inputFile, outputFile)
    if err != nil {
        t.Fatalf("decompressFile failed: %v", err)
    }

    // check the output file contents
    content, err := ioutil.ReadFile(outputFile)
    if err != nil {
        t.Fatalf("failed to read output file: %v", err)
    }
    if string(content) != "Hello, World!" {
        t.Fatalf("unexpected content in output file: %s", content)
    }
}
```

The compression test checks that the output file exists, the decompression test checks that the content matches the original text — both have to pass for these two functions to be considered usable.

## References

- [compress/gzip standard library](https://pkg.go.dev/compress/gzip)
- [compress/flate standard library](https://pkg.go.dev/compress/flate)


## Sibling pages

- [Advanced](/compress/Advanced.md)
- [Archive](/compress/Archive.md)
- [Composite](/compress/Composite.md)
- [Compress](/compress/Compress.md)
- [Readme](/compress/Readme.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Readme](/compress/Readme.md)
