###  文本编码

文本编码解决的是同一个问题：把字符变成字节序列，好存储、好传输。这一章对比三种编码（ASCII、UTF-8、UTF-16）以及 Go 标准库处理它们的对应手段。

#### 2.1 ASCII 编码

**ASCII (American Standard Code for Information Interchange)** 是一种早期的字符编码标准，使用 7 位表示字符，共定义了 128 个字符，包括基本的拉丁字母、数字、标点符号以及一些控制字符。后来出现的扩展字符集（如 Latin-1、Windows-1252）用 8 位表示 256 个字符，但它们并不属于标准 ASCII。虽然 ASCII 编码简单且历史悠久，但其对非英文字符的支持有限。

**示例代码**：
```go
package main

import "fmt"

func main() {
    // ASCII 编码示例
    text := "Hello, World!"
    fmt.Println("Text:", text)
}
```

在 Go 中，字符串默认为 UTF-8 编码，但可以处理 ASCII 字符串，因为 UTF-8 向下兼容 ASCII。

#### 2.2 UTF-8 编码

**UTF-8 (8-bit Unicode Transformation Format)** 是一种变长编码方式，可以用 1 到 4 个字节表示一个 Unicode 字符。UTF-8 兼容 ASCII，且支持全球大多数语言的字符，是现代应用中最常用的文本编码方式。

**示例代码**：
```go
package main

import (
    "fmt"
    "unicode/utf8"
)

func main() {
    // UTF-8 编码示例
    text := "你好，世界！" // 中文字符

    fmt.Println("Text:", text)
    fmt.Printf("Length: %d bytes\n", len(text))
    fmt.Printf("Rune count: %d\n", utf8.RuneCountInString(text))

    // 遍历字符串中的每个字符（rune）
    for i, c := range text {
        fmt.Printf("Character %d: %c (code point: %U)\n", i, c, c)
    }
}
```

在上面的示例中，`utf8.RuneCountInString` 用于计算 UTF-8 字符串中的字符数量，而 `range` 用于遍历字符串中的每个字符（rune）。

#### 2.3 UTF-16 编码

**UTF-16 (16-bit Unicode Transformation Format)** 是另一种 Unicode 编码方式，使用 16 位（两个字节）或 32 位（四个字节）表示一个字符。UTF-16 可以表示所有 Unicode 字符，但对于某些字符使用两个 16 位单元（代理对）。

在 Go 语言中，UTF-16 编码和解码通常涉及到 `unicode/utf16` 包。以下是一个处理 UTF-16 的示例：

**示例代码**：
```go
package main

import (
    "fmt"
    "unicode/utf16"
)

func main() {
    // UTF-16 编码示例
    text := "こんにちは世界" // 日文字符

    // 将 UTF-8 转换为 UTF-16
    utf16Codes := utf16.Encode([]rune(text))
    fmt.Println("UTF-16 Encoded:", utf16Codes)

    // 将 UTF-16 转换回 UTF-8
    utf8Chars := utf16.Decode(utf16Codes)
    utf8Text := string(utf8Chars)
    fmt.Println("UTF-8 Decoded:", utf8Text)
}
```

在上面的示例中，`utf16.Encode` 和 `utf16.Decode` 用于在 UTF-8 和 UTF-16 之间转换。

#### 总结

本章介绍了三种主要的文本编码方式：

- **ASCII 编码**：最早的字符编码标准，主要用于英文文本。
- **UTF-8 编码**：现代的变长编码方式，兼容 ASCII，支持多语言字符。
- **UTF-16 编码**：用 16 位（两个字节）或 32 位（四个字节，通过代理对表示）表示一个字符的编码方式，支持所有 Unicode 字符，常用于 Windows 和 Java 等平台。

在 Go 里这三者会同时遇到：源码和字符串字面量本身就是 UTF-8，`len` 数的是字节、`utf8.RuneCountInString` 数的才是字符，碰到 Windows API 或 Java 这类以 UTF-16 为边界的场合再换 `unicode/utf16` 转码。记住"字节和字符不是一回事"，大部分编码坑就能避开。