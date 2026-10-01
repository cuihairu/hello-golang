### Go 的 `io` 包详细介绍

Go 的 `io` 包提供了基本的 I/O 原语和接口，用于处理输入和输出流。这个包定义了用于读写数据的基本接口，并提供了多种实现这些接口的工具和函数。

#### 1. `io` 包接口和类型

1. **`Reader` 接口**

   `Reader` 接口是所有读取操作的基础，它定义了一个方法 `Read`：

   ```go
   package io

   type Reader interface {
       Read(p []byte) (n int, err error)
   }
   ```

   `Read` 方法从数据源读取最多 len(p) 字节的数据到 p 中，并返回实际读取的字节数和可能的错误。

   **示例**：

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

2. **`Writer` 接口**

   `Writer` 接口定义了一个方法 `Write`：

   ```go
   package io

   type Writer interface {
       Write(p []byte) (n int, err error)
   }
   ```

   `Write` 方法将 p 中的数据写入到目标，并返回写入的字节数和可能的错误。

   **示例**：

   ```go
   package main

   import (
       "fmt"
       "strings"
       "io"
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

3. **`Closer` 接口**

   `Closer` 接口用于关闭资源，定义了一个方法 `Close`：

   ```go
   package io

   type Closer interface {
       Close() error
   }
   ```

   `Close` 方法关闭资源，并返回可能的错误。

4. **`ReadWriter` 接口**

   `ReadWriter` 接口结合了 `Reader` 和 `Writer` 接口，定义了两个方法：

   ```go
   package io

   type ReadWriter interface {
       Reader
       Writer
   }
   ```

   **示例**：

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

   `Pipe` 函数创建一对连接的 `Reader` 和 `Writer`，它们可以用于在不同的协程之间传递数据。

   ```go
   package io

   func Pipe() (*PipeReader, *PipeWriter) 
   ```

   **示例**：

   ```go
   package main

   import (
       "fmt"
       "io"
       "io/ioutil"
   )

   func main() {
       pr, pw := io.Pipe()

       go func() {
           defer pw.Close()
           pw.Write([]byte("Hello, Pipe!"))
       }()

       data, err := ioutil.ReadAll(pr)
       if err != nil {
           fmt.Println("Error reading from pipe:", err)
           return
       }
       fmt.Println("Read from pipe:", string(data))
   }
   ```

6. **`LimitedReader`**

   `LimitedReader` 限制 `Reader` 读取的字节数：

   ```go
   package io

   type LimitedReader struct {
       R Reader
       N int64
   }
   ```

   **示例**：

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

   `MultiReader` 连接多个 `Reader`，依次读取每个 `Reader` 直到第一个读取完毕。

   ```go
   package io

   type MultiReader struct {
       // contains filtered or unexported fields
   }
   ```

   **示例**：

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

8. **`PipeReader` 和 `PipeWriter`**

   `PipeReader` 和 `PipeWriter` 是 `Pipe` 函数返回的类型，它们用于在管道中进行读写操作。

   **示例**：

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

9. **` TeeReader`**

   `TeeReader` 同时将读取的数据写入另一个 `Writer` 并返回原始数据。

   ```go
   package io

   type TeeReader struct {
       R Reader
       W Writer
   }
   ```

   **示例**：

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

#### 2. 常用函数

1. **`io.Copy`**

   `io.Copy` 从一个 `Reader` 复制数据到一个 `Writer`。

   ```go
   package io

   func Copy(dst Writer, src Reader) (written int64, err error)
   ```

   **示例**：

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

   `io.ReadAll` 读取所有数据直到 EOF。

   ```go
   package io

   func ReadAll(r Reader) ([]byte, error)
   ```

   **示例**：

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

   `io.ReadFull` 读取指定长度的数据。

   ```go
   package io

   func ReadFull(r Reader, buf []byte) (n int, err error)
   ```

   **示例**：

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

4. **`io.Seek`**

   `io.Seek` 允许在 `Reader` 和 `Writer` 上设置当前位置（在实现了 `Seek` 接口的类型上使用）。

   **示例**：

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
           fmt.Println

("Error creating file:", err)
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

5. **`io.StringReader`**

   `io.StringReader` 允许将字符串视为 `Reader`。

   ```go
   package io

   func StringReader(s string) *strings.Reader
   ```

   **示例**：

   ```go
   package main

   import (
       "fmt"
       "io"
   )

   func main() {
       r := io.StringReader("Hello, StringReader!")
       data, _ := io.ReadAll(r)
       fmt.Println("Read from StringReader:", string(data))
   }
   ```

6. **`io.StringWriter`**

   `io.StringWriter` 允许将 `Writer` 转换为字符串。

   **示例**：

   ```go
   package main

   import (
       "fmt"
       "strings"
       "io"
   )

   func main() {
       var sb strings.Builder
       w := io.StringWriter(&sb)
       w.Write([]byte("Hello, StringWriter!"))
       fmt.Println("Written data:", sb.String())
   }
   ```

通过本章内容，你应该对 Go 的 `io` 包有了全面的了解。掌握这些接口、类型和函数，可以帮助你在处理输入输出流时更高效、更灵活。