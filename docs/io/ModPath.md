### Go's `path` package in detail

Go's `path` package handles path strings, managing operations like joining, splitting, and parsing. It only recognizes Unix-style paths (separated by `/`).

In addition, Go provides the `path/filepath` package, which extends `path` to handle platform-specific paths (including Windows-style paths, separated by `\`).

#### 1. What the `path` package does

The `path` package mainly provides the following functionality:

- **Path joining**: combine multiple path elements into one path.
- **Path splitting**: extract the file name or directory name from a path.
- **Path normalization**: reduce a path to its simplest form.

#### 2. Functions in detail

1. **`Join(elem ...string) string`**

   The `Join` function joins multiple path elements into one path, handling path separators automatically.

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

   **Output**:

   ```
   Full Path: folder/subfolder/file.txt
   ```

   This function automatically inserts `/` between path elements and handles extra separators.

2. **`Base(path string) string`**

   The `Base` function returns the last element of a path, that is, the file name or directory name.

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

   **Output**:

   ```
   Base Name: file.txt
   ```

   This function returns the last part of the path, not including the part before the path separator.

3. **`Dir(path string) string`**

   The `Dir` function returns the directory part of a path, that is, the part after removing the last path element.

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

   **Output**:

   ```
   Directory Name: /folder/subfolder
   ```

   This function strips the last element from the path and returns the rest.

4. **`Split(path string) (string, string)`**

   The `Split` function divides a path into two parts: directory and file name.

   ```go
   package path

   func Split(path string) (dir, file string)
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "path"
   )

   func main() {
       dir, file := path.Split("/folder/subfolder/file.txt")
       fmt.Println("Directory:", dir)
       fmt.Println("File:", file)
   }
   ```

   **Output**:

   ```
   Directory: /folder/subfolder/
   File: file.txt
   ```

   This function splits the path into a directory part and a file name part, where the directory part includes the trailing `/`.

5. **`Clean(path string) string`**

   The `Clean` function returns a normalized version of the path, eliminating extra path separators and parent-directory references (`..`).

   ```go
   package path

   func Clean(path string) string
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "path"
   )

   func main() {
       cleanPath := path.Clean("/folder/./subfolder/../file.txt")
       fmt.Println("Clean Path:", cleanPath)
   }
   ```

   **Output**:

   ```
   Clean Path: /folder/file.txt
   ```

   This function normalizes the path, resolving `.` (current directory) and `..` (parent directory) into the corresponding path.

6. **`IsAbs(path string) bool`**

   The `IsAbs` function checks whether a path is absolute.

   ```go
   package path

   func IsAbs(path string) bool
   ```

   **Example**:

   ```go
   package main

   import (
       "fmt"
       "path"
   )

   func main() {
       fmt.Println("Is Absolute Path:", path.IsAbs("/folder/file.txt"))
       fmt.Println("Is Absolute Path:", path.IsAbs("folder/file.txt"))
   }
   ```

   **Output**:

   ```
   Is Absolute Path: true
   Is Absolute Path: false
   ```

   This function checks whether the path starts with the root directory. In Unix-style paths, a path beginning with `/` is absolute.

#### 3. The difference between the `path` and `path/filepath` packages

- **`path` package**: handles Unix-style `/` paths, with rules that are platform-independent and no awareness of Windows separators.
- **`path/filepath` package**: handles paths according to the current operating system, and also supports Windows's `\`.

**Example**:

```go
package main

import (
    "fmt"
    "path/filepath"
)

func main() {
    // Join paths using filepath package
    fullPath := filepath.Join("folder", "subfolder", "file.txt")
    fmt.Println("Full Path:", fullPath)

    // Get base name and directory using filepath package
    baseName := filepath.Base("/folder/subfolder/file.txt")
    dirName := filepath.Dir("/folder/subfolder/file.txt")
    fmt.Println("Base Name:", baseName)
    fmt.Println("Directory Name:", dirName)

    // Clean path using filepath package
    cleanPath := filepath.Clean("/folder/./subfolder/../file.txt")
    fmt.Println("Clean Path:", cleanPath)

    // Check if path is absolute
    fmt.Println("Is Absolute Path:", filepath.IsAbs("/folder/file.txt"))
    fmt.Println("Is Absolute Path:", filepath.IsAbs("folder/file.txt"))
}
```

#### Summary

The `path` package has exactly the six functions above: `Join` for joining, `Base` for the file name, `Dir` for the directory, `Split` for dividing into two, `Clean` for normalization, and `IsAbs` for checking absolute paths, all handled in Unix style. When paths may contain `\` or drive letters, switch to `path/filepath`.

## References

- [io standard library](https://pkg.go.dev/io)
- [os standard library](https://pkg.go.dev/os)
- [path/filepath standard library](https://pkg.go.dev/path/filepath)


## Sibling pages

- [Advanced](/io/Advanced.md)
- [CommonFormats](/io/CommonFormats.md)
- [EfficientIO](/io/EfficientIO.md)
- [ModOS](/io/ModOS.md)
- [Security](/io/Security.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [ModOS](/io/ModOS.md)
- [Security](/io/Security.md)
