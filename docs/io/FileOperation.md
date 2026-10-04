### 第3章 文件操作

本章讲文件的打开关闭、读取写入、指针移动和错误处理。

#### 3.1 打开与关闭文件

**打开文件**是文件操作的第一步，先选访问模式：

- **只读模式**（Read-only）：仅允许读取文件内容，不允许修改文件。
- **写入模式**（Write-only）：允许写入文件内容，通常会覆盖现有内容。
- **追加模式**（Append）：允许将数据追加到文件末尾，而不会覆盖现有内容。
- **读写模式**（Read-write）：允许同时读取和写入文件。

**关闭文件**是在操作完成后释放系统资源的必要步骤。关闭文件后，所有对该文件的操作（如读取或写入）都将无效。


Go 里用 `os` 包打开和关闭文件。

**示例：打开与关闭文件**

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 打开文件（只读模式）
    file, err := os.Open("example.txt")
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()  // 确保文件在函数结束时关闭

    fmt.Println("File opened successfully")
}
```

在这个例子中，我们使用 `os.Open` 打开一个文件，并在操作完成后使用 `defer` 确保文件被正确关闭。

#### 3.2 读取文件

文件读取可以根据需要选择不同的方法，常见的读取方式包括逐行读取、按块读取等。每种方法的适用场景和性能特点不同。

**逐行读取**：适合文本文件，文件很大时也不必一次性读进内存。

**按块读取**：适合二进制文件，或一次要读一大块数据的场景。

**示例：逐行读取**

```go
package main

import (
    "bufio"
    "fmt"
    "os"
)

func main() {
    file, err := os.Open("example.txt")
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        fmt.Println(scanner.Text())
    }

    if err := scanner.Err(); err != nil {
        fmt.Println("Error reading file:", err)
    }
}
```

在这个例子中，我们使用 `bufio.NewScanner` 逐行读取文件内容，并处理可能发生的读取错误。

**示例：按块读取**

```go
package main

import (
    "fmt"
    "io"
    "os"
)

func main() {
    file, err := os.Open("example.txt")
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    buffer := make([]byte, 1024)  // 读取 1024 字节
    for {
        n, err := file.Read(buffer)
        if err == io.EOF {
            break
        }
        if err != nil {
            fmt.Println("Error reading file:", err)
            return
        }
        fmt.Print(string(buffer[:n]))
    }
}
```

在这个例子中，我们使用 `file.Read` 按块读取文件数据，并处理可能发生的读取错误。

#### 3.3 写入文件

写入文件可以选择覆盖文件内容或追加到现有内容的末尾。写入操作可以处理文本和二进制数据。

**覆盖写入**：写入数据时会覆盖文件的现有内容。

**追加写入**：将数据追加到文件末尾，保留现有内容。

**示例：覆盖写入**

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    file, err := os.Create("example.txt")  // 创建文件或覆盖现有文件
    if err != nil {
        fmt.Println("Error creating file:", err)
        return
    }
    defer file.Close()

    _, err = file.WriteString("This is a new line.\n")
    if err != nil {
        fmt.Println("Error writing to file:", err)
        return
    }

    fmt.Println("File written successfully")
}
```

在这个例子中，我们使用 `os.Create` 创建文件并覆盖现有内容，随后使用 `file.WriteString` 写入数据。

**示例：追加写入**

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    file, err := os.OpenFile("example.txt", os.O_APPEND|os.O_WRONLY, 0666)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    _, err = file.WriteString("This line is appended.\n")
    if err != nil {
        fmt.Println("Error writing to file:", err)
        return
    }

    fmt.Println("File appended successfully")
}
```

在这个例子中，我们使用 `os.OpenFile` 以追加模式打开文件，并将数据追加到文件末尾。


#### 3.4 文件指针与位置

文件指针指示当前的读写位置，移动它用 `Seek` 方法，常用的三种操作是：取当前位置、跳到指定位置、回到开头。

**示例：获取当前位置和设置位置**

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    file, err := os.OpenFile("example.txt", os.O_RDWR, 0666)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    // 获取当前位置
    pos, err := file.Seek(0, os.SEEK_CUR)
    if err != nil {
        fmt.Println("Error getting position:", err)
        return
    }
    fmt.Println("Current position:", pos)

    // 设置文件指针到第 10 字节
    _, err = file.Seek(10, os.SEEK_SET)
    if err != nil {
        fmt.Println("Error setting position:", err)
        return
    }

    buffer := make([]byte, 10)
    _, err = file.Read(buffer)
    if err != nil {
        fmt.Println("Error reading file:", err)
        return
    }
    fmt.Println("Data at position 10:", string(buffer))
}
```

在这个例子中，我们使用 `Seek` 移动文件指针到指定位置，并读取该位置的数据。


#### 3.5 错误处理与文件操作异常

文件打不开、读写出错、文件不存在，都是通过检查返回的 `err` 来处理的。

**示例：错误处理**

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    file, err := os.Open("example.txt")
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    _, err = file.WriteString("Trying to write")
    if err != nil {
        fmt.Println("Error writing to file:", err)
        return
    }

    fmt.Println("Operation completed successfully")
}
```

在这个例子中，我们检查文件打开和写入操作是否成功，并处理可能发生的错误。


#### 总结

Go 的文件操作都在 `os` 包里：`Open`/`Create`/`OpenFile` 打开，`Read`/`WriteString` 读写，`Seek` 移动指针，每一步都检查返回的 `err`。文件锁定、复制、移动属于进阶操作，后面章节会讲。