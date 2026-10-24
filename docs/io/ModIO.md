### What the `io` package can do

Go's `io` package provides the basic primitives and interfaces for I/O: interfaces like `Reader` and `Writer` define read and write actions, while functions like `Copy` and `Pipe` bridge them together.

#### 1. Interfaces and types in the `io` package

1. **`Reader` interface**

   The `Reader` interface is the foundation of all read operations. It defines a single method, `Read`:

   ```go
   package io

   type Reader interface {
       Read(p []byte) (n int, err error)
   }
   ```

   The `Read` method reads up to len(p) bytes from the data source into p, and returns the number of bytes actually read and any error.

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "strings"
       "io"
   )

   func main() {
       r := strings.NewReader("Hello, Go!")
       buf := make([]byte, 4)

       for {
           n, err := r.Read(buf)
           if err == io.EOF {
               break
           }
           if err != nil {
               fmt.Println("Error reading:", err)
               break
           }
           fmt.Printf("Read %d bytes: %s\n", n, string(buf[:n]))
       }
   }
   ```

2. **`Writer` interface**

   The `Writer` interface defines a single method, `Write`:

   ```go
   package io

   type Writer interface {
       Write(p []byte) (n int, err error)
   }
   ```

   The `Write` method writes the data in p to the destination, and returns the number of bytes written and any error.

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "strings"
   )

   func main() {
       var w strings.Builder
       n, err := w.Write([]byte("Hello, Go!"))
       if err != nil {
           fmt.Println("Error writing:", err)
           return
       }
       fmt.Printf("Wrote %d bytes: %s\n", n, w.String())
   }
   ```

3. **`Closer` interface**

   The `Closer` interface is used to close a resource. It defines a single method, `Close`:

   ```go
   package io

   type Closer interface {
       Close() error
   }
   ```

   The `Close` method closes the resource and returns any error.

4. **`ReadWriter` interface**

   The `ReadWriter` interface combines the `Reader` and `Writer` interfaces, defining two methods:

   ```go
   package io

   type Reader interface {
       Read(p []byte) (n int, err error)
   }

   type Writer interface {
       Write(p []byte) (n int, err error)
   }

   type ReadWriter interface {
       Reader
       Writer
   }
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "io"
       "os"
   )

   func main() {
       file, err := os.Create("example.txt")
       if err != nil {
           fmt.Println("Error creating file:", err)
           return
       }
       defer file.Close()

       rw := io.Writer(file)
       rw.Write([]byte("Hello, File!"))
   }
   ```

5. **`Pipe`**

   The `Pipe` function creates a connected pair of `Reader` and `Writer`, which can be used to pass data between different goroutines.

   ```go
   package io

   type PipeReader struct {
       // contains filtered or unexported fields
   }

   type PipeWriter struct {
       // contains filtered or unexported fields
   }

   func Pipe() (*PipeReader, *PipeWriter)
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "io"
   )

   func main() {
       pr, pw := io.Pipe()

       go func() {
           defer pw.Close()
           pw.Write([]byte("Hello, Pipe!"))
       }()

       data, err := io.ReadAll(pr)
       if err != nil {
           fmt.Println("Error reading from pipe:", err)
           return
       }
       fmt.Println("Read from pipe:", string(data))
   }
   ```

6. **`LimitedReader`**

   `LimitedReader` limits the number of bytes a `Reader` reads:

   ```go
   package io

   type Reader interface {
       Read(p []byte) (n int, err error)
   }

   type LimitedReader struct {
       R Reader
       N int64
   }
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "io"
       "strings"
   )

   func main() {
       r := io.LimitReader(strings.NewReader("Hello, Go!"), 5)
       data, _ := io.ReadAll(r)
       fmt.Println("Limited read:", string(data))
   }
   ```

7. **`MultiReader`**

   `MultiReader` chains multiple `Reader`s: it reads each `Reader` in turn, and moves on to the next one only after the previous one is exhausted (returns EOF).

   ```go
   package io

   type MultiReader struct {
       // contains filtered or unexported fields
   }
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "io"
       "strings"
   )

   func main() {
       r1 := strings.NewReader("Hello, ")
       r2 := strings.NewReader("World!")
       mr := io.MultiReader(r1, r2)

       data, _ := io.ReadAll(mr)
       fmt.Println("Multi-read:", string(data))
   }
   ```

8. **`PipeReader` and `PipeWriter`**

   `PipeReader` and `PipeWriter` are the types returned by the `Pipe` function, and they are used to read from and write to the pipe.

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "io"
   )

   func main() {
       pr, pw := io.Pipe()

       go func() {
           defer pw.Close()
           pw.Write([]byte("Hello, Pipe!"))
       }()

       data, err := io.ReadAll(pr)
       if err != nil {
           fmt.Println("Error reading from pipe:", err)
           return
       }
       fmt.Println("Read from pipe:", string(data))
   }
   ```

9. **`TeeReader`**

   `TeeReader` writes the data it reads to another `Writer` while also returning the original data.

   ```go
   package io

   type Reader interface {
       Read(p []byte) (n int, err error)
   }

   type Writer interface {
       Write(p []byte) (n int, err error)
   }

   func TeeReader(r Reader, w Writer) Reader
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "io"
       "strings"
   )

   func main() {
       var output strings.Builder
       r := io.TeeReader(strings.NewReader("Hello, TeeReader!"), &output)

       data, _ := io.ReadAll(r)
       fmt.Println("Read data:", string(data))
       fmt.Println("Written to output:", output.String())
   }
   ```

#### 2. Common functions

1. **`io.Copy`**

   `io.Copy` copies data from a `Reader` to a `Writer`.

   ```go
   package io

   type Reader interface {
       Read(p []byte) (n int, err error)
   }

   type Writer interface {
       Write(p []byte) (n int, err error)
   }

   func Copy(dst Writer, src Reader) (written int64, err error)
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "io"
       "strings"
   )

   func main() {
       src := strings.NewReader("Hello, Copy!")
       var dst strings.Builder
       _, err := io.Copy(&dst, src)
       if err != nil {
           fmt.Println("Error copying:", err)
           return
       }
       fmt.Println("Copied data:", dst.String())
   }
   ```

2. **`io.ReadAll`**

   `io.ReadAll` reads all data until EOF.

   ```go
   package io

   type Reader interface {
       Read(p []byte) (n int, err error)
   }

   func ReadAll(r Reader) ([]byte, error)
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "io"
       "strings"
   )

   func main() {
       r := strings.NewReader("Hello, ReadAll!")
       data, err := io.ReadAll(r)
       if err != nil {
           fmt.Println("Error reading:", err)
           return
       }
       fmt.Println("Read all data:", string(data))
   }
   ```

3. **`io.ReadFull`**

   `io.ReadFull` reads an exact number of bytes.

   ```go
   package io

   type Reader interface {
       Read(p []byte) (n int, err error)
   }

   func ReadFull(r Reader, buf []byte) (n int, err error)
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "io"
       "strings"
   )

   func main() {
       r := strings.NewReader("Hello, ReadFull!")
       buf := make([]byte, 5)
       n, err := io.ReadFull(r, buf)
       if err != nil {
           fmt.Println("Error reading full data:", err)
           return
       }
       fmt.Printf("Read %d bytes: %s\n", n, string(buf))
   }
   ```

4. **`io.Seeker` interface and constants like `io.SeekStart`**

   The `io.Seeker` interface wraps the ability to set the current position in a stream (such as `*os.File`); `io.SeekStart`, `io.SeekCurrent`, and `io.SeekEnd` are the reference-point constants used by the `Seek` method.

   ```go
   package io

   type Seeker interface {
       Seek(offset int64, whence int) (int64, error)
   }

   const (
       SeekStart   = 0 // relative to the start of the file
       SeekCurrent = 1 // relative to the current position
       SeekEnd     = 2 // relative to the end of the file
   )
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "io"
       "os"
   )

   func main() {
       file, err := os.Create("example.txt")
       if err != nil {
           fmt.Println("Error creating file:", err)
           return
       }
       defer file.Close()

       file.Write([]byte("Hello, Seek!"))

       file.Seek(0, io.SeekStart)
       buf := make([]byte, 5)
       file.Read(buf)
       fmt.Println("Seeked data:", string(buf))
   }
   ```

5. **`strings.NewReader`**

   Go's `io` package has no function that turns a string into a `Reader` directly; you usually use `NewReader` from the `strings` package.

   ```go
   package strings

   // Reader is a simplified excerpt of the standard library strings.Reader
   type Reader struct {
       s string
       i int
   }

   func NewReader(s string) *Reader
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "io"
       "strings"
   )

   func main() {
       r := strings.NewReader("Hello, StringReader!")
       data, _ := io.ReadAll(r)
       fmt.Println("Read from StringReader:", string(data))
   }
   ```

6. **`io.StringWriter`**

   `io.StringWriter` is an interface for a `Writer` that supports writing a whole string in one call (such as `*strings.Builder`).

   ```go
   package io

   type StringWriter interface {
       WriteString(s string) (n int, err error)
   }
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "io"
       "strings"
   )

   func main() {
       var sb strings.Builder
       var w io.StringWriter = &sb
       w.WriteString("Hello, StringWriter!")
       fmt.Println("Written data:", sb.String())
   }
   ```

`Reader` and `Writer` are the two most-referenced interfaces in Go's I/O system, and `Copy`, `ReadAll`, and `ReadFull` cover most data-moving scenarios. Write a function to accept an `io.Reader` and it can take data from both files and memory.

## References

- [io standard library](https://pkg.go.dev/io)
- [os standard library](https://pkg.go.dev/os)


## Sibling pages

- [Advanced](/io/Advanced.md)
- [CommonFormats](/io/CommonFormats.md)
- [EfficientIO](/io/EfficientIO.md)
- [InputOutput](/io/InputOutput.md)
- [ModOS](/io/ModOS.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [InputOutput](/io/InputOutput.md)
- [ModOS](/io/ModOS.md)
