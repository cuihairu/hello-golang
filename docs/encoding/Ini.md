### INI 文件格式

INI 文件是一种用于配置和设置的简单文本格式。Microsoft 在 1980 年代为 Windows 操作系统设计了它，程序的配置数据常用这种格式存放：格式简单，肉眼能直接读。

#### 1. INI 文件格式

INI 文件格式有一些基本的结构和约定：

1. **文件结构**：

   - INI 文件由多个部分组成，包括节（Section）、键值对（Key-Value Pairs），和注释（Comments）。

2. **节（Section）**：

   - 节以方括号（`[]`）括起来，表示一个配置区域。例如：
     ```
     [SectionName]
     ```

3. **键值对（Key-Value Pair）**：

   - 每个节包含多个键值对，键和值之间用等号（`=`）分隔。例如：
     ```
     key1=value1
     key2=value2
     ```

4. **注释（Comments）**：

   - 注释以分号（`;`）开头，注释内容会被忽略。例如：
     ```
     ; This is a comment
     key=value
     ```

5. **空白行**：

   - 空白行会被忽略，不会影响解析。

#### 2. INI 文件的示例

一个完整的 INI 文件长这样：

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

- **[General]**：节名，表示通用的设置。
- **name=John Doe**：键值对，其中 `name` 是键，`John Doe` 是值。
- **[Settings]**：另一个节名，表示设置相关的选项。
- **theme=dark**：键值对，设置主题为“dark”。
- **[Paths]**：一个节，用于指定路径设置。

#### 3. INI 文件的优点和缺点

优点是格式简单、到处都能读写，纯文本打开就能改，适合存简单配置。缺点是表达力有限：不支持嵌套结构和数组，只有字符串一种类型；基本结构虽通用，却没有严格标准，各实现的细节存在差异。

#### 4. INI 文件的应用

程序的运行参数、用户的个性化设置、操作系统和各类工具的系统配置，都可以放在 INI 文件里。

#### 5. INI 文件处理示例（Go 语言）

在 Go 语言中，用第三方库 `gopkg.in/ini.v1`（即原 `github.com/go-ini/ini` 项目）处理 INI 文件，安装方式为 `go get gopkg.in/ini.v1`。读取和写入分别如下：

**读取 INI 文件示例**：

```go
package main

import (
    "fmt"
    "log"

    "gopkg.in/ini.v1"
)

func main() {
    // 读取 INI 文件
    cfg, err := ini.Load("config.ini")
    if err != nil {
        log.Fatalf("Failed to read file: %v", err)
    }

    // 读取节
    generalSection := cfg.Section("General")

    // 读取键值对
    name := generalSection.Key("name").String()
    age := generalSection.Key("age").MustInt()
    city := generalSection.Key("city").String()

    fmt.Printf("Name: %s\n", name)
    fmt.Printf("Age: %d\n", age)
    fmt.Printf("City: %s\n", city)
}
```

**写入 INI 文件示例**：

```go
package main

import (
    "log"

    "gopkg.in/ini.v1"
)

func main() {
    // 创建 INI 文件
    cfg := ini.Empty()

    // 添加节和键值对
    section, err := cfg.NewSection("General")
    if err != nil {
        log.Fatalf("Failed to create section: %v", err)
    }
    section.Key("name").SetValue("John Doe")
    section.Key("age").SetValue("30")
    section.Key("city").SetValue("New York")

    // 保存 INI 文件
    err = cfg.SaveTo("config.ini")
    if err != nil {
        log.Fatalf("Failed to save file: %v", err)
    }

    log.Println("INI 文件保存成功")
}
```

#### 6. INI 文件处理中的常见问题

1. **键的唯一性**：

   - INI 文件中的每个节中的键应该是唯一的。如果重复，后面的值可能会覆盖前面的值。

2. **节的正确解析**：

   - 确保节名在方括号中没有空格，并且节名不包含特殊字符。

3. **数据类型的处理**：

   - 由于 INI 文件只支持字符串值，处理其他数据类型时需要进行转换（如将字符串转换为整数或布尔值）。

4. **注释的使用**：

   - 确保注释行以分号开头，并且注释不会干扰键值对的解析。

#### 总结

方括号分节、等号连键值、分号起注释，三样就构成了 INI 的全部语法。功能有限，换来的是任何文本编辑器都能改、几乎每种语言都有现成的库。Go 里读它用 `ini.Load`，写它用 `cfg.SaveTo`。