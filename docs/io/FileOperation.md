### Chapter 3 File operations

Here I note down opening and closing files, reading and writing, moving the pointer, and error handling.

#### 3.1 Opening and closing files

**Opening a file** is the first step of any file operation. First you pick an access mode:

- **Read-only mode**: Allows only reading the file content; the file cannot be modified.
- **Write-only mode**: Allows writing to the file; usually overwrites existing content.
- **Append mode**: Allows appending data to the end of the file without overwriting existing content.
- **Read-write mode**: Allows reading from and writing to the file at the same time.

**Closing a file** is the necessary step to release system resources once you're done. After a file is closed, all operations on it (such as reading or writing) become invalid.


In Go, you use the `os` package to open and close files.

**Example: opening and closing a file**

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // open the file (read-only mode)
    file, err := os.Open("example.txt")
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()  // make sure the file is closed when the function returns

    fmt.Println("File opened successfully")
}
```

In this example, we use `os.Open` to open a file, and then use `defer` to make sure the file is closed properly after the operations are done.

#### 3.2 Reading files

How you read a file depends on what you need. Common reading approaches include reading line by line and reading in blocks. Each method has a different range of applicability and performance characteristics.

**Reading line by line**: Well suited to text files; even a large file doesn't have to be loaded into memory all at once.

**Reading in blocks**: Well suited to binary files, or cases where you need to read a large chunk of data at once.

**Example: reading line by line**

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

In this example, we use `bufio.NewScanner` to read the file content line by line, and handle any errors that might occur while reading.

**Example: reading in blocks**

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

    buffer := make([]byte, 1024)  // read 1024 bytes
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

In this example, we use `file.Read` to read file data in blocks, and handle any errors that might occur while reading.

#### 3.3 Writing files

When writing to a file, you can either overwrite its content or append to the end of the existing content. Write operations can handle both text and binary data.

**Overwrite**: When writing data, the file's existing content is overwritten.

**Append**: Data is appended to the end of the file, preserving the existing content.

**Example: overwrite**

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    file, err := os.Create("example.txt")  // create the file or overwrite an existing one
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

In this example, we use `os.Create` to create a file and overwrite its existing content, then use `file.WriteString` to write data.

**Example: append**

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

In this example, we use `os.OpenFile` to open the file in append mode, and append data to the end of the file.


#### 3.4 File pointer and position

The file pointer indicates the current read/write position. You move it with the `Seek` method, and the three operations you'll use most are: get the current position, jump to a specified position, and return to the beginning.

**Example: getting the current position and setting the position**

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

    // get the current position
    pos, err := file.Seek(0, os.SEEK_CUR)
    if err != nil {
        fmt.Println("Error getting position:", err)
        return
    }
    fmt.Println("Current position:", pos)

    // set the file pointer to byte 10
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

In this example, we use `Seek` to move the file pointer to a specified position, and read the data at that position.


#### 3.5 Error handling and file operation exceptions

A file that won't open, a read/write error, a file that doesn't exist — all of these are handled by checking the returned `err`.

**Example: error handling**

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

In this example, we check whether the file open and write operations succeeded, and handle any errors that might occur.


#### Summary

All of Go's file operations live in the `os` package: `Open`/`Create`/`OpenFile` to open, `Read`/`WriteString` to read and write, `Seek` to move the pointer, and you check the returned `err` at every step. File locking, copying, and moving are advanced operations and are covered in the chapters that follow.

## References

- [io standard library](https://pkg.go.dev/io)
- [os standard library](https://pkg.go.dev/os)


## Sibling pages

- [Advanced](/io/Advanced.md)
- [CommonFormats](/io/CommonFormats.md)
- [EfficientIO](/io/EfficientIO.md)
- [FileAdvanced](/io/FileAdvanced.md)
- [IO](/io/IO.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [FileAdvanced](/io/FileAdvanced.md)
- [IO](/io/IO.md)
