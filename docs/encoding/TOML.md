### TOML (Tom's Obvious, Minimal Language)

TOML (Tom's Obvious, Minimal Language) is a configuration file format designed to be readable at a glance and easy to write and parse. Its syntax derives from INI files, but supports more complex structures and has stricter grammar rules.

#### 1. TOML file format

The basic components of the TOML file format include:

1. **Key-value pairs**:

   - TOML files use key-value pairs to represent data. The key and value are separated by an equals sign (`=`). For example:
     ```toml
     key = "value"
     ```

2. **Tables**:

   - TOML files use tables to organize configuration data, with tables represented by square brackets (`[]`). For example:
     ```toml
     [section]
     key = "value"
     ```

3. **Subtables**:

   - TOML supports nested tables, allowing you to define subtables within a table. For example:
     ```toml
     [parent]
     key = "value"

     [parent.child]
     key = "value"
     ```

4. **Arrays**:

   - TOML supports one-dimensional and multi-dimensional arrays. For example:
     ```toml
     array = [1, 2, 3]
     ```

5. **Date and time**:

   - TOML supports dates and times in ISO 8601 format. For example:
     ```toml
     date = 2024-07-25
     datetime = 2024-07-25T14:30:00
     ```

6. **Comments**:

   - Comments start with a hash sign (`#`), and the comment content is ignored. For example:
     ```toml
     # This is a comment
     key = "value"
     ```

7. **Multiline strings**:

   - TOML supports multiline strings, wrapped in three double quotes (`"""`). For example:
     ```toml
     multiline_string = """
     This is a
     multiline string
     """
     ```

#### 2. TOML file example

Here is an example TOML file showing the various features:

```toml
# This is a TOML file example

[server]
host = "localhost"
port = 8080

[database]
user = "admin"
password = "secret"
dbname = "example_db"

[features]
enabled = true
version = 1.0

[paths]
data = "/path/to/data"
logs = "/path/to/logs"

[servers]
[servers.alpha]
ip = "192.168.1.1"
port = 9000

[servers.beta]
ip = "192.168.1.2"
port = 9001

[[items]]
name = "Item1"
value = 10

[[items]]
name = "Item2"
value = 20
```

- **[server]**: table name, used to define server configuration.
- **[database]**: table name, used to define database configuration.
- **[features]**: table name, used to define feature toggles and version.
- **[paths]**: table name, used to define path configuration.
- **[servers]**: table name containing the subtables `alpha` and `beta`, used to define multiple server configurations.
- **[[items]]**: array table, where each array element represents an item.

#### 3. Pros and cons of TOML

**Pros**:

1. **Human-readable**:

   - Plain text format, easy to read and edit.

2. **Supports complex data structures**:

   - TOML supports nested tables, arrays, and multiline strings, making it suitable for expressing complex configuration data.

3. **Strict grammar rules**:

   - The rules are clear, parsing has little ambiguity, and the chance of errors is small.

**Cons**:

1. **Limited tooling support**:

   - Although TOML has gained some support, compared with more common formats such as JSON and YAML, there are relatively fewer supporting tools and libraries.

2. **No custom data types**:

   - TOML does not support custom data types or structures, only basic types (strings, integers, floats, booleans, dates, etc.).

#### 4. Applications of TOML files

TOML is most commonly used for application configuration, to define program parameters and options; it is also often used for system settings, service configuration, and development environment configuration — anywhere the data is structured.

#### 5. TOML file processing example (Go)

In Go, use a third-party library (such as `github.com/pelletier/go-toml`) to handle TOML files. Here is an example showing how to read and write TOML files.

**Reading a TOML file**:

Reading requires a `config.toml` in the current directory; you can run the writing example below first to generate one, or hand-write one, for example:

```toml
[server]
host = "localhost"
port = 8080
```

```go
package main

import (
    "fmt"
    "log"

    "github.com/pelletier/go-toml"
)

func main() {
    // read the TOML file
    data, err := toml.LoadFile("config.toml")
    if err != nil {
        log.Fatalf("Failed to read file: %v", err)
    }

    // read the table
    server := data.Get("server").(*toml.Tree)

    // read key-value pairs; note that integers in TOML are parsed as int64
    host := server.Get("host").(string)
    port := server.Get("port").(int64)

    fmt.Printf("Host: %s\n", host)
    fmt.Printf("Port: %d\n", port)
}
```

Output:

```plaintext
Host: localhost
Port: 8080
```

**Writing a TOML file**:

```go
package main

import (
    "log"
    "os"

    "github.com/pelletier/go-toml"
)

func main() {
    // build a TOML tree from a map via TreeFromMap
    data, err := toml.TreeFromMap(map[string]interface{}{
        "server": map[string]interface{}{
            "host": "localhost",
            "port": 8080,
        },
        "database": map[string]interface{}{
            "user":     "admin",
            "password": "secret",
        },
    })
    if err != nil {
        log.Fatalf("Failed to build tree: %v", err)
    }

    // write the TOML tree to a file via WriteTo
    file, err := os.Create("config.toml")
    if err != nil {
        log.Fatalf("Failed to create file: %v", err)
    }
    defer file.Close()
    if _, err := data.WriteTo(file); err != nil {
        log.Fatalf("Failed to save file: %v", err)
    }

    log.Println("TOML 文件保存成功")
}
```

#### 6. Common issues in TOML file handling

1. **Table naming**:

   - Ensure table names conform to TOML syntax requirements, with no illegal characters or spaces.

2. **Data type conversion**:

   - TOML supports basic data types, but you need to handle type conversion correctly when reading and writing.

3. **File encoding**:

   - Ensure the TOML file uses UTF-8 encoding to avoid character encoding issues.

4. **Array handling**:

   - When handling arrays, ensure the double-bracket (`[[...]]`) syntax is used correctly, and handle array element ordering and duplication issues.

#### Summary

TOML has clear grammar rules and can express tables, arrays, and dates, so a library like `github.com/pelletier/go-toml` is enough to read and write it on the Go side. Tooling and library support is not as widespread as JSON or YAML, but for the configuration file use case it is adequate.

## References

- [encoding series standard library (json as an example)](https://pkg.go.dev/encoding/json)


## Sibling pages

- [JsonV2](/encoding/JsonV2.md)
- [Base64](/encoding/Base64.md)
- [Binary](/encoding/Binary.md)
- [Text](/encoding/Text.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Text](/encoding/Text.md)
