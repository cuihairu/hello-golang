# 模板
在 Go 语言中，`text/template` 包提供了创建和执行文本模板的功能。它允许我们将动态数据嵌入到静态文本中，广泛应用于生成配置文件、邮件内容、报告等。下面是对 Go 中 `text/template` 包的详细介绍，包括基本用法、模板语法、函数、自定义函数和常见的使用场景。

### 1. 基本用法

#### 创建并执行简单模板

```go
package main

import (
    "os"
    "text/template"
)

func main() {
    tmpl, err := template.New("example").Parse("Hello, {{.Name}}!")
    if err != nil {
        panic(err)
    }

    data := struct {
        Name string
    }{
        Name: "World",
    }

    err = tmpl.Execute(os.Stdout, data)
    if err != nil {
        panic(err)
    }
}
```

输出结果：
```
Hello, World!
```

### 2. 模板语法

#### 动态数据

使用 <code v-pre>{{.}}</code> 访问传入的数据。可以通过 <code v-pre>{{.Field}}</code> 访问结构体字段。

```go
tmpl, err := template.New("example").Parse("Name: {{.Name}}, Age: {{.Age}}")
```

#### 条件语句

使用 `if` 语句进行条件判断。

```go
tmpl, err := template.New("example").Parse(`{{if .Active}}User is active{{else}}User is inactive{{end}}`)
```

#### 循环语句

使用 `range` 语句进行循环。

```go
tmpl, err := template.New("example").Parse(`{{range .Items}}{{.}}, {{end}}`)
```

#### 管道（Pipe）

管道用于将一个命令的输出作为下一个命令的输入。

```go
tmpl, err := template.New("example").Parse(`{{.Name | printf "Hello, %s!"}}`)
```

### 3. 模板函数

`text/template` 包含一些内置函数，例如 `print`、`html` 等。可以使用这些函数来处理数据。

#### 使用内置函数

```go
tmpl, err := template.New("example").Parse(`{{printf "Hello, %s!" .Name}}`)
```

### 4. 自定义函数

可以向模板中添加自定义函数。

#### 定义并注册自定义函数

```go
package main

import (
    "os"
    "text/template"
)

func main() {
    tmpl, err := template.New("example").Funcs(template.FuncMap{
        "toUpperCase": func(s string) string {
            return strings.ToUpper(s)
        },
    }).Parse(`{{.Name | toUpperCase}}`)
    if err != nil {
        panic(err)
    }

    data := struct {
        Name string
    }{
        Name: "world",
    }

    err = tmpl.Execute(os.Stdout, data)
    if err != nil {
        panic(err)
    }
}
```

输出结果：
```
WORLD
```

### 5. 嵌套模板

可以将模板嵌套在一起，以实现模块化和复用。

#### 定义和执行嵌套模板

```go
package main

import (
    "os"
    "text/template"
)

func main() {
    tmpl, err := template.New("main").Parse(`
{{define "header"}}Header Content{{end}}
{{define "body"}}Body Content{{end}}

{{template "header"}}
{{template "body"}}
`)
    if err != nil {
        panic(err)
    }

    err = tmpl.Execute(os.Stdout, nil)
    if err != nil {
        panic(err)
    }
}
```

输出结果：
```
Header Content
Body Content
```

### 6. 常见使用场景

#### 生成配置文件

可以使用模板生成动态配置文件。

```go
package main

import (
    "os"
    "text/template"
)

func main() {
    tmpl, err := template.New("config").Parse(`
server {
    listen {{.Port}};
    server_name {{.ServerName}};
}
`)
    if err != nil {
        panic(err)
    }

    data := struct {
        Port       int
        ServerName string
    }{
        Port:       8080,
        ServerName: "localhost",
    }

    err = tmpl.Execute(os.Stdout, data)
    if err != nil {
        panic(err)
    }
}
```

输出结果：
```
server {
    listen 8080;
    server_name localhost;
}
```

#### 生成邮件内容

可以使用模板生成动态邮件内容。

```go
package main

import (
    "os"
    "text/template"
)

func main() {
    tmpl, err := template.New("email").Parse(`
Hello {{.Name}},

Thank you for your purchase!

Order details:
Product: {{.Product}}
Price: {{.Price}}
`)
    if err != nil {
        panic(err)
    }

    data := struct {
        Name    string
        Product string
        Price   float64
    }{
        Name:    "John",
        Product: "Go Programming Book",
        Price:   29.99,
    }

    err = tmpl.Execute(os.Stdout, data)
    if err != nil {
        panic(err)
    }
}
```

输出结果：
```
Hello John,

Thank you for your purchase!

Order details:
Product: Go Programming Book
Price: 29.99
```

### 总结

Go 语言中的 `text/template` 包提供了强大且灵活的模板功能，可以通过简单的语法将动态数据嵌入到静态文本中。通过理解基本用法、模板语法、内置和自定义函数以及常见的使用场景，可以有效地在 Go 程序中生成各种动态内容。