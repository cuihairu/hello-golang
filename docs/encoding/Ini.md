### INI file format

An INI file is a simple text format used for configuration and settings. Microsoft designed it for the Windows operating system in the 1980s, and programs commonly store their configuration data in this format: it is simple and readable directly by eye.

#### 1. INI file format

The INI file format has some basic structures and conventions:

1. **File structure**:

   - An INI file is made up of multiple parts, including sections, key-value pairs, and comments.

2. **Sections**:

   - A section is wrapped in square brackets (`[]`) and represents a configuration area. For example:
     ```
     [SectionName]
     ```

3. **Key-value pairs**:

   - Each section contains multiple key-value pairs, with the key and value separated by an equals sign (`=`). For example:
     ```
     key1=value1
     key2=value2
     ```

4. **Comments**:

   - Comments start with a semicolon (`;`), and the comment content is ignored. For example:
     ```
     ; This is a comment
     key=value
     ```

5. **Blank lines**:

   - Blank lines are ignored and do not affect parsing.

#### 2. INI file example

A complete INI file looks like this:

```ini
; This is an example INI file

[General]
name=John Doe
age=30
city=New York

[Settings]
theme=dark
autosave=true

[Paths]
data_path=C:\data
log_path=C:\logs
```

- **[General]**: section name, representing general settings.
- **name=John Doe**: a key-value pair, where `name` is the key and `John Doe` is the value.
- **[Settings]**: another section name, representing setting-related options.
- **theme=dark**: a key-value pair that sets the theme to "dark".
- **[Paths]**: a section used for path settings.

#### 3. Pros and cons of INI files

The pros are a simple format, read/write support everywhere, plain text you can edit directly, and well suited for simple configuration. The cons are limited expressiveness: no nested structures or arrays, only one type (strings); the basic structure is universal, but there is no strict standard, so implementations differ in the details.

#### 4. Applications of INI files

Program runtime parameters, user personalization settings, and system configuration for operating systems and various tools can all live in an INI file.

#### 5. INI file processing example (Go)

In Go, use the third-party library `gopkg.in/ini.v1` (the original `github.com/go-ini/ini` project) to handle INI files, installed via `go get gopkg.in/ini.v1`. Reading and writing look like this:

**Reading an INI file**:

Reading requires a `config.ini` in the current directory; you can run the writing example below first to generate one, or hand-write one, for example:

```ini
[General]
name = John Doe
age = 30
city = New York
```

```go
package main

import (
    "fmt"
    "log"

    "gopkg.in/ini.v1"
)

func main() {
    // read the INI file
    cfg, err := ini.Load("config.ini")
    if err != nil {
        log.Fatalf("Failed to read file: %v", err)
    }

    // read the section
    generalSection := cfg.Section("General")

    // read key-value pairs
    name := generalSection.Key("name").String()
    age := generalSection.Key("age").MustInt()
    city := generalSection.Key("city").String()

    fmt.Printf("Name: %s\n", name)
    fmt.Printf("Age: %d\n", age)
    fmt.Printf("City: %s\n", city)
}
```

Output:

```plaintext
Name: John Doe
Age: 30
City: New York
```

**Writing an INI file**:

```go
package main

import (
    "log"

    "gopkg.in/ini.v1"
)

func main() {
    // create the INI file
    cfg := ini.Empty()

    // add the section and key-value pairs
    section, err := cfg.NewSection("General")
    if err != nil {
        log.Fatalf("Failed to create section: %v", err)
    }
    section.Key("name").SetValue("John Doe")
    section.Key("age").SetValue("30")
    section.Key("city").SetValue("New York")

    // save the INI file
    err = cfg.SaveTo("config.ini")
    if err != nil {
        log.Fatalf("Failed to save file: %v", err)
    }

    log.Println("INI 文件保存成功")
}
```

#### 6. Common issues in INI file handling

1. **Key uniqueness**:

   - Keys within each section of an INI file should be unique. If duplicated, a later value may overwrite an earlier one.

2. **Correct parsing of sections**:

   - Ensure section names have no spaces inside the square brackets and contain no special characters.

3. **Data type handling**:

   - Since INI files only support string values, you need to convert when handling other data types (such as converting a string to an integer or boolean).

4. **Use of comments**:

   - Ensure comment lines start with a semicolon and that comments do not interfere with parsing key-value pairs.

#### Summary

Square brackets delimit sections, equals signs join keys and values, and semicolons start comments — those three things are the entire INI syntax. The functionality is limited, but in exchange any text editor can edit it and nearly every language has a ready-made library. In Go, read it with `ini.Load` and write it with `cfg.SaveTo`.

## References

- [encoding series standard library (json as an example)](https://pkg.go.dev/encoding/json)


## Sibling pages

- [JsonV2](/encoding/JsonV2.md)
- [Base64](/encoding/Base64.md)
- [Binary](/encoding/Binary.md)
- [Hex](/encoding/Hex.md)
- [JSON](/encoding/JSON.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Hex](/encoding/Hex.md)
- [JSON](/encoding/JSON.md)
