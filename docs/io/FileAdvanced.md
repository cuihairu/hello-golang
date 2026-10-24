###  Advanced file operations

Once file operations go beyond basic reading and writing, they also cover: locking, copying, moving, deleting, renaming, and, finally, file attributes and metadata.

#### 4.1 File locking

File locking is used to prevent multiple processes from modifying the same file at the same time, thereby avoiding data inconsistency and conflicts. File locks come in two flavors: shared and exclusive.

**Shared lock**: Allows multiple processes to read the file but forbids writing to it.

**Exclusive lock**: Prevents other processes from reading from or writing to the file, guaranteeing exclusive access.

##### 4.1.1 The basic concept of file locking
Introduces the basic principles and use cases of file locking.

##### 4.1.2 Using system calls to lock a file
Shows how to use system calls (such as `flock` or `fcntl`) to implement file locking.

##### 4.1.3 Cross-platform file locking
Discussions of how to make file locking compatible across different operating systems.

**Go example code**:
```go
package main

import (
    "fmt"
    "os"
    "syscall"
)

func lockFile(file *os.File) error {
    return syscall.Flock(int(file.Fd()), syscall.LOCK_EX)
}

func unlockFile(file *os.File) error {
    return syscall.Flock(int(file.Fd()), syscall.LOCK_UN)
}

func main() {
    file, err := os.OpenFile("example.txt", os.O_RDWR|os.O_CREATE, 0666)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    if err := lockFile(file); err != nil {
        fmt.Println("Error locking file:", err)
        return
    }
    fmt.Println("File locked successfully")

    // Perform file operations...

    if err := unlockFile(file); err != nil {
        fmt.Println("Error unlocking file:", err)
        return
    }
    fmt.Println("File unlocked successfully")
}
```

#### 4.2 Copying and moving files

Copying and moving files are common file operations. Copying a file involves copying the source file's content to a target file, while moving a file does so and then deletes the source.

##### 4.2.1 The basic concept of file copying
Introduces the principles and basic steps of file copying.

##### 4.2.2 Copying a file with standard library functions
Shows how to use standard library functions (such as `io.Copy` with `os.Create`) to copy a file.

##### 4.2.3 The basic concept of file moving
Introduces the principles and basic steps of file moving.

##### 4.2.4 Moving a file with standard library functions
Shows how to use standard library functions (such as `os.Rename`, or copying first and then deleting the source when crossing file systems) to move a file.

**Go example code**:
```go
package main

import (
    "fmt"
    "io"
    "os"
)

func copyFile(src, dst string) error {
    sourceFile, err := os.Open(src)
    if err != nil {
        return err
    }
    defer sourceFile.Close()

    destFile, err := os.Create(dst)
    if err != nil {
        return err
    }
    defer destFile.Close()

    _, err = io.Copy(destFile, sourceFile)
    return err
}

func moveFile(src, dst string) error {
    if err := copyFile(src, dst); err != nil {
        return err
    }
    return os.Remove(src)
}

func main() {
    if err := copyFile("source.txt", "destination.txt"); err != nil {
        fmt.Println("Error copying file:", err)
    } else {
        fmt.Println("File copied successfully")
    }

    if err := moveFile("source.txt", "new_destination.txt"); err != nil {
        fmt.Println("Error moving file:", err)
    } else {
        fmt.Println("File moved successfully")
    }
}
```

#### 4.3 Deleting and renaming files

Deleting a file removes it from the file system; renaming changes the file's name.

##### 4.3.1 The basic concept of file deletion
Introduces the principles and basic steps of file deletion.

##### 4.3.2 Deleting a file with standard library functions
Shows how to use standard library functions (such as `os.Remove`, which corresponds to the `unlink` system call) to delete a file.

##### 4.3.3 The basic concept of file renaming
Introduces the principles and basic steps of file renaming.

##### 4.3.4 Renaming a file with standard library functions
Shows how to use standard library functions (such as `os.Rename`) to rename a file.

**Go example code**:
```go
package main

import (
    "fmt"
    "os"
)

func deleteFile(filePath string) error {
    return os.Remove(filePath)
}

func renameFile(oldPath, newPath string) error {
    return os.Rename(oldPath, newPath)
}

func main() {
    if err := deleteFile("file_to_delete.txt"); err != nil {
        fmt.Println("Error deleting file:", err)
    } else {
        fmt.Println("File deleted successfully")
    }

    if err := renameFile("old_name.txt", "new_name.txt"); err != nil {
        fmt.Println("Error renaming file:", err)
    } else {
        fmt.Println("File renamed successfully")
    }
}
```

#### 4.4 File attributes and metadata

File attributes and metadata provide extra information about a file, such as its creation time, modification time, and size.

##### 4.4.1 The basic concept of file attributes
Introduces the principles and use cases of file attributes.

##### 4.4.2 Getting file attributes
Shows how to use system calls (such as `os.Stat`, which corresponds to the `stat` system call) to get file attributes.

##### 4.4.3 Modifying file attributes
Discusses how to modify file attributes, such as changing file permissions and timestamps.

##### 4.4.4 Managing file metadata
Introduces how to manage a file's metadata, including adding and reading custom metadata.

**Go example code**:
```go
package main

import (
    "fmt"
    "os"
)

func getFileAttributes(filePath string) (os.FileInfo, error) {
    return os.Stat(filePath)
}

func changeFilePermissions(filePath string, mode os.FileMode) error {
    return os.Chmod(filePath, mode)
}

func main() {
    fileInfo, err :=getFileAttributes("example.txt")
    if err != nil {
        fmt.Println("Error getting file attributes:", err)
        return
    }

    fmt.Printf("File size: %d bytes\n", fileInfo.Size())
    fmt.Printf("File permissions: %s\n", fileInfo.Mode().String())
    fmt.Printf("Last modified: %s\n", fileInfo.ModTime().String())

    if err := changeFilePermissions("example.txt", 0644); err != nil {
        fmt.Println("Error changing file permissions:", err)
    } else {
        fmt.Println("File permissions changed successfully")
    }
}
```

Locking goes through `syscall.Flock`; copying uses `io.Copy` with `os.Create`; moving and renaming use `os.Rename` (when crossing file systems, copy first and then delete the source); deleting is `os.Remove`; and attributes come from `os.Stat`. The examples here revolve around these calls.

## References

- [io standard library](https://pkg.go.dev/io)
- [os standard library](https://pkg.go.dev/os)


## Sibling pages

- [Advanced](/io/Advanced.md)
- [CommonFormats](/io/CommonFormats.md)
- [EfficientIO](/io/EfficientIO.md)
- [File](/io/File.md)
- [FileOperation](/io/FileOperation.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [File](/io/File.md)
- [FileOperation](/io/FileOperation.md)
