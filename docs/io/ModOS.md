### What the `os` package can do

Go's `os` package provides functionality for interacting with the operating system, including file system operations, environment variables, and process management.

#### 1. File operations

1. **The `File` type**

   The `File` type represents an open file and provides various file operation methods, such as reading, writing, and closing files.

   ```go
   package os

   type File struct {
       // contains filtered or unexported fields
   }
   ```

   - **Methods**:
     - `Read(p []byte) (n int, err error)`: read data from the file.
     - `Write(p []byte) (n int, err error)`: write data to the file.
     - `Close() error`: close the file.
     - `Seek(offset int64, whence int) (int64, error)`: set the current position in the file.
     - `Stat() (FileInfo, error)`: get file information.
     - `Truncate(size int64) error`: truncate the file.

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "os"
   )

   func main() {
       file, err := os.Create("example.txt")
       if err != nil {
           fmt.Println("Error creating file:", err)
           return
       }
       defer file.Close()

       file.Write([]byte("Hello, File!"))

       file.Seek(0, 0)
       buf := make([]byte, 12)
       file.Read(buf)
       fmt.Println("File contents:", string(buf))
   }
   ```

2. **File operation functions**

   - **`os.Create(name string) (*File, error)`**: create a new file, truncating it if it already exists.
   - **`os.Open(name string) (*File, error)`**: open a file for reading.
   - **`os.OpenFile(name string, flag int, perm FileMode) (*File, error)`**: open a file with more control options.
   - **`os.Remove(name string) error`**: delete a file.
   - **`os.Rename(oldpath, newpath string) error`**: rename or move a file.
   - **`os.Mkdir(name string, perm FileMode) error`**: create a directory.
   - **`os.MkdirAll(path string, perm FileMode) error`**: create directories recursively.
   - **`os.Remove(name string) error`**: delete a file or an empty directory (use `os.RemoveAll` for non-empty directories).

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "os"
   )

   func main() {
       // Create a file
       file, err := os.Create("example.txt")
       if err != nil {
           fmt.Println("Error creating file:", err)
           return
       }
       file.Close()

       // Remove the file
       err = os.Remove("example.txt")
       if err != nil {
           fmt.Println("Error removing file:", err)
           return
       }

       // Create a directory
       err = os.Mkdir("exampleDir", 0755)
       if err != nil {
           fmt.Println("Error creating directory:", err)
           return
       }

       // Remove the directory
       err = os.Remove("exampleDir")
       if err != nil {
           fmt.Println("Error removing directory:", err)
           return
       }
   }
   ```

#### 2. Environment variables

1. **`Getenv(key string) string`**

   Get the value of the specified environment variable.

   ```go
   package main

   import (
       "fmt"
       "os"
   )

   func main() {
       homeDir := os.Getenv("HOME")
       fmt.Println("HOME:", homeDir)
   }
   ```

2. **`Setenv(key, value string) error`**

   Set the value of an environment variable.

   ```go
   package main

   import (
       "fmt"
       "os"
   )

   func main() {
       err := os.Setenv("MY_VAR", "my_value")
       if err != nil {
           fmt.Println("Error setting environment variable:", err)
           return
       }

       value := os.Getenv("MY_VAR")
       fmt.Println("MY_VAR:", value)
   }
   ```

3. **`Unsetenv(key string) error`**

   Remove the specified environment variable.

   ```go
   package main

   import (
       "fmt"
       "os"
   )

   func main() {
       os.Setenv("MY_VAR", "my_value")
       os.Unsetenv("MY_VAR")

       value := os.Getenv("MY_VAR")
       fmt.Println("MY_VAR:", value)
   }
   ```

#### 3. Process management

1. **`exec.Command(name string, arg ...string) *Cmd`**

   Create a `Cmd` object for running a command (in the `os/exec` package).

   ```go
   package main

   import (
       "fmt"
       "os/exec"
   )

   func main() {
       cmd := exec.Command("echo", "Hello, World!")
       output, err := cmd.Output()
       if err != nil {
           fmt.Println("Error executing command:", err)
           return
       }
       fmt.Println(string(output))
   }
   ```

2. **The `Cmd` type**

   The `Cmd` type represents the execution of an external command and provides functionality for controlling external processes.

   ```go
   package exec

   type Cmd struct {
       // contains filtered or unexported fields
   }
   ```

   - **Methods**:
     - `Run() error`: run the command and wait for it to finish.
     - `Start() error`: start the command without waiting for it to finish.
     - `Wait() error`: wait for the command to finish.

3. **`Getpid() int`**

   Return the PID of the current process.

   ```go
   package main

   import (
       "fmt"
       "os"
   )

   func main() {
       fmt.Println("Current PID:", os.Getpid())
   }
   ```

4. **`Kill() error`**

   Send a signal to terminate a process (a method of `os.Process`).

   ```go
   package main

   import (
       "fmt"
       "os"
   )

   func main() {
       pid := os.Getpid()
       fmt.Println("Current PID:", pid)
       // To terminate a process, first get a *os.Process, then call its Kill method:
       // p, err := os.FindProcess(pid)
       // if err == nil {
       //     err = p.Kill()
       // }
   }
   ```

#### 4. File information

1. **The `FileInfo` interface**

   The `FileInfo` interface provides basic information about a file.

   ```go
   package os

   import "time"

   type FileMode uint32

   type FileInfo interface {
       Name() string
       Size() int64
       Mode() FileMode
       ModTime() time.Time
       IsDir() bool
       Sys() interface{}
   }
   ```

   - **Methods**:
     - `Name() string`: file name.
     - `Size() int64`: file size (bytes).
     - `Mode() FileMode`: file mode (permissions).
     - `ModTime() time.Time`: the file's last modification time.
     - `IsDir() bool`: whether it is a directory.
     - `Sys() interface{}`: system-related information.

2. **The `FileMode` type**

   `FileMode` represents the permissions and mode of a file.

   ```go
   package os

   type FileMode uint32
   ```

   - Common flag constants used when opening files (as the `flag` parameter of `os.OpenFile`, type int):
     - `os.O_RDONLY`: read-only mode.
     - `os.O_WRONLY`: write-only mode.
     - `os.O_RDWR`: read-write mode.
     - `os.O_CREATE`: create the file if it does not exist.
     - `os.O_TRUNC`: truncate the file.
     - `os.O_APPEND`: append when writing.

   - Common constants of `FileMode` itself:
     - `os.ModeDir`: directory.
     - `os.ModePerm`: Unix permission bit mask (0777).
     - `os.ModeSymlink`: symbolic link.

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "os"
   )

   func main() {
       file, err := os.Stat("example.txt")
       if err != nil {
           fmt.Println("Error getting file info:", err)
           return
       }
       fmt.Println("File Name:", file.Name())
       fmt.Println("File Size:", file.Size())
       fmt.Println("File Mode:", file.Mode())
       fmt.Println("Last Modified Time:", file.ModTime())
       fmt.Println("Is Directory:", file.IsDir())
   }
   ```

#### 5. File path handling

1. **`Join(elem ...string) string`**

   Join multiple path elements into a single path.

   ```go
   package path

   func Join(elem ...string) string
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "path"
   )

   func main() {
       fullPath := path.Join("folder", "subfolder", "file.txt")
       fmt.Println("Full Path:", fullPath)
   }
   ```

2. **`Abs(path string) (string, error)`**

   Get the absolute path (in the `path/filepath` package).

   ```go
   package filepath

   func Abs(path string) (string, error)
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "path/filepath"
   )

   func main() {
       absPath, err := filepath.Abs("example.txt")
       if err != nil {
           fmt.Println("Error getting absolute path:", err)
           return
       }
       fmt.Println("Absolute Path:", absPath)
   }
   ```

3. **`Base(path string) string`**

   Return the last element of the path (file name or directory name).

   ```go
   package path

   func Base(path string) string
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "path"
   )

   func main() {
       baseName := path.Base("/folder/subfolder/file.txt")
       fmt.Println("Base Name:", baseName)
   }
   ```

4. **`Dir(path string) string`**

   Return the directory part of the path.

   ```go
   package path

   func Dir(path string) string
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "path"
   )

   func main() {
       dirName := path.Dir("/folder/subfolder/file.txt")
       fmt.Println("Directory Name:", dirName)
   }
   ```

#### Summary

`os` splits its job into three parts: files use `File`'s `Read`, `Write`, `Close` plus the `os.Create` and `os.OpenFile` family of functions; environment variables are `Getenv`, `Setenv`, `Unsetenv`; processes are `exec.Command` and `os.Getpid`. Path joining belongs to `path` and `path/filepath`.

## References

- [io standard library](https://pkg.go.dev/io)
- [os standard library](https://pkg.go.dev/os)


## Sibling pages

- [Advanced](/io/Advanced.md)
- [CommonFormats](/io/CommonFormats.md)
- [EfficientIO](/io/EfficientIO.md)
- [ModIO](/io/ModIO.md)
- [ModPath](/io/ModPath.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [ModIO](/io/ModIO.md)
- [ModPath](/io/ModPath.md)
