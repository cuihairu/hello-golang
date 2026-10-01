### 2. Go 的正则表达式库

Go 语言中的正则表达式功能由 `regexp` 包提供。这个包实现了正则表达式的匹配、搜索、替换和分割等功能。以下是 `regexp` 包的详细介绍，包括主要功能和函数的使用。

#### 2.1 `regexp` 包介绍

**概述**
- `regexp` 包是 Go 语言标准库的一部分，提供了对正则表达式的支持。
- 包含功能：正则表达式的编译、匹配、替换和分割。

**导入**
```go
import "regexp"
```

**主要数据类型**
- `*regexp.Regexp`：表示编译后的正则表达式对象，可以用于匹配、替换和分割操作。

#### 2.2 匹配和搜索功能

**1. 编译正则表达式**
- 使用 `regexp.MustCompile` 函数编译正则表达式，并返回 `*regexp.Regexp` 对象。若正则表达式无效，将会触发 panic。
```go
re := regexp.MustCompile(`pattern`)
```

**2. 匹配完整字符串**
- **`MatchString`**：检查整个字符串是否匹配正则表达式。
```go
matched := re.MatchString("test string")
```

**3. 查找匹配**
- **`FindString`**：返回正则表达式匹配的第一个字符串。
```go
matched := re.FindString("test string")
```

- **`FindStringIndex`**：返回正则表达式匹配的第一个字符串的位置索引。
```go
index := re.FindStringIndex("test string")
```

- **`FindAllString`**：返回正则表达式匹配的所有字符串。
```go
matches := re.FindAllString("test string", -1)
```

- **`FindAllStringSubmatch`**：返回正则表达式匹配的所有字符串及其子串。
```go
matches := re.FindAllStringSubmatch("test string", -1)
```

#### 2.3 替换和分割功能

**1. 替换匹配的字符串**
- **`ReplaceAllString`**：用指定的字符串替换正则表达式匹配的所有部分。
```go
result := re.ReplaceAllString("test string", "replacement")
```

- **`ReplaceAllFunc`**：用函数返回的字符串替换正则表达式匹配的所有部分。
```go
result := re.ReplaceAllFunc([]byte("test string"), func(b []byte) []byte {
    return []byte("replacement")
})
```

**2. 分割字符串**
- **`Split`**：根据正则表达式分割字符串，返回分割后的子串。
```go
parts := re.Split("test string", -1)
```

#### 2.4 使用 `regexp` 包的主要函数

**1. 编译正则表达式**
- **`Compile`**：编译正则表达式并返回 `*regexp.Regexp` 对象，若正则表达式无效，则返回错误。
```go
re, err := regexp.Compile(`pattern`)
if err != nil {
    // 处理错误
}
```

- **`MustCompile`**：编译正则表达式并返回 `*regexp.Regexp` 对象，若正则表达式无效，则触发 panic。
```go
re := regexp.MustCompile(`pattern`)
```

**2. 检查匹配**
- **`MatchString`**：检查字符串是否匹配正则表达式。
```go
matched := re.MatchString("test string")
```

- **`Match`**：检查字节切片是否匹配正则表达式。
```go
matched := re.Match([]byte("test string"))
```

**3. 查找匹配**
- **`FindString`**：查找并返回正则表达式匹配的第一个字符串。
```go
result := re.FindString("test string")
```

- **`FindAllString`**：查找并返回正则表达式匹配的所有字符串。
```go
results := re.FindAllString("test string", -1)
```

- **`FindStringSubmatch`**：查找并返回正则表达式匹配的第一个字符串及其子串。
```go
matches := re.FindStringSubmatch("test string")
```

- **`FindAllStringSubmatch`**：查找并返回正则表达式匹配的所有字符串及其子串。
```go
matches := re.FindAllStringSubmatch("test string", -1)
```

**4. 替换匹配**
- **`ReplaceAllString`**：用指定的字符串替换正则表达式匹配的所有部分。
```go
result := re.ReplaceAllString("test string", "replacement")
```

- **`ReplaceAllFunc`**：用函数返回的字符串替换正则表达式匹配的所有部分。
```go
result := re.ReplaceAllFunc([]byte("test string"), func(b []byte) []byte {
    return []byte("replacement")
})
```

**5. 分割字符串**
- **`Split`**：根据正则表达式分割字符串，返回分割后的子串。
```go
parts := re.Split("test string", -1)
```

**6. 查找正则表达式的匹配位置**
- **`FindStringIndex`**：查找正则表达式匹配的第一个字符串的位置索引。
```go
index := re.FindStringIndex("test string")
```

通过这些函数，你可以在 Go 中灵活地使用正则表达式进行文本处理。