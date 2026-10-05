# Html模板
在 Go 语言中，`html/template` 包创建和执行 HTML 模板。它与 `text/template` 包类似，多出来的是针对 HTML 安全的功能：插值前自动转义特殊字符，防止跨站脚本（XSS）攻击。处理 HTML 就用这个包。

### 1. 基本用法

#### 创建并执行简单模板

```go
package main

import (
    "html/template"
    "os"
)

func main() {
    tmpl, err := template.New("example").Parse("<h1>Hello, {{.Name}}!</h1>")
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
```html
<h1>Hello, World!</h1>
```

### 2. 模板语法

#### 动态数据

使用 <code v-pre>{{.}}</code> 访问传入的数据。可以通过 <code v-pre>{{.Field}}</code> 访问结构体字段。

```go
package main

import (
    "html/template"
    "os"
)

func main() {
    data := struct {
        Name string
        Age  int
    }{Name: "Tom", Age: 18}

    tmpl, err := template.New("example").Parse("<p>Name: {{.Name}}, Age: {{.Age}}</p>")
    if err != nil {
        panic(err)
    }
    tmpl.Execute(os.Stdout, data)
}
```

#### 条件语句

使用 `if` 语句进行条件判断。

```go
package main

import (
    "html/template"
    "os"
)

func main() {
    data := struct{ Active bool }{Active: true}

    tmpl, err := template.New("example").Parse(`{{if .Active}}<p>User is active</p>{{else}}<p>User is inactive</p>{{end}}`)
    if err != nil {
        panic(err)
    }
    tmpl.Execute(os.Stdout, data)
}
```

#### 循环语句

使用 `range` 语句进行循环。

```go
package main

import (
    "html/template"
    "os"
)

func main() {
    data := struct{ Items []string }{Items: []string{"Go", "Rust", "Python"}}

    tmpl, err := template.New("example").Parse(`<ul>{{range .Items}}<li>{{.}}</li>{{end}}</ul>`)
    if err != nil {
        panic(err)
    }
    tmpl.Execute(os.Stdout, data)
}
```

#### 管道（Pipe）

管道用于将一个命令的输出作为下一个命令的输入。

```go
package main

import (
    "html/template"
    "os"
)

func main() {
    data := struct{ Name string }{Name: "World"}

    tmpl, err := template.New("example").Parse(`<p>{{.Name | printf "Hello, %s!"}}</p>`)
    if err != nil {
        panic(err)
    }
    tmpl.Execute(os.Stdout, data)
}
```

### 3. 自定义函数

可以向模板中添加自定义函数。

#### 定义并注册自定义函数

```go
package main

import (
    "html/template"
    "os"
    "strings"
)

func main() {
    tmpl, err := template.New("example").Funcs(template.FuncMap{
        "toUpperCase": func(s string) string {
            return strings.ToUpper(s)
        },
    }).Parse(`<p>{{.Name | toUpperCase}}</p>`)
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
```html
<p>WORLD</p>
```

### 4. 嵌套模板

可以将模板嵌套在一起，以实现模块化和复用。

#### 定义和执行嵌套模板

```go
package main

import (
    "html/template"
    "os"
)

func main() {
    tmpl, err := template.New("main").Parse(`
{{define "header"}}<header>Header Content</header>{{end}}
{{define "body"}}<main>Body Content</main>{{end}}

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
```html
<header>Header Content</header>
<main>Body Content</main>
```

### 5. 常见使用场景

#### 生成 HTML 页面

可以使用模板生成动态 HTML 页面。

```go
package main

import (
    "html/template"
    "os"
)

type User struct {
    Name  string
    Email string
}

func main() {
    tmpl, err := template.New("email").Parse(`
<!DOCTYPE html>
<html>
<head>
    <title>User Info</title>
</head>
<body>
    <h1>Hello, {{.Name}}</h1>
    <p>Your email is {{.Email}}</p>
</body>
</html>
`)
    if err != nil {
        panic(err)
    }

    user := User{Name: "John", Email: "john@example.com"}

    err = tmpl.Execute(os.Stdout, user)
    if err != nil {
        panic(err)
    }
}
```

输出结果：
```html
<!DOCTYPE html>
<html>
<head>
    <title>User Info</title>
</head>
<body>
    <h1>Hello, John</h1>
    <p>Your email is john@example.com</p>
</body>
</html>
```

### 6. 常见陷阱

#### 自动转义

`html/template` 包会自动转义 HTML 中的特殊字符，确保生成的 HTML 内容是安全的。

```go
package main

import (
    "html/template"
    "os"
)

func main() {
    tmpl, err := template.New("example").Parse("<p>{{.Content}}</p>")
    if err != nil {
        panic(err)
    }

    data := struct {
        Content string
    }{
        Content: "<script>alert('XSS');</script>",
    }

    err = tmpl.Execute(os.Stdout, data)
    if err != nil {
        panic(err)
    }
}
```

输出结果：
```html
<p>&lt;script&gt;alert('XSS');&lt;/script&gt;</p>
```

#### 安全模板实践

- 避免直接使用 `text/template` 处理 HTML 内容，使用 `html/template` 以确保安全。
- 自定义函数返回 HTML 安全类型时，使用 `template.HTML` 类型来标记已安全处理的 HTML。

### 示例代码

把前面几节合起来：创建模板、绑定数据、调用自定义函数，一次跑完。

```go
package main

import (
    "html/template"
    "os"
    "strings"
)

func main() {
    tmpl, err := template.New("example").Funcs(template.FuncMap{
        "toUpperCase": func(s string) string {
            return strings.ToUpper(s)
        },
    }).Parse(`
<!DOCTYPE html>
<html>
<head>
    <title>{{.Title}}</title>
</head>
<body>
    <h1>{{.Header}}</h1>
    <p>{{.Content | toUpperCase}}</p>
</body>
</html>
`)
    if err != nil {
        panic(err)
    }

    data := struct {
        Title   string
        Header  string
        Content string
    }{
        Title:   "Go HTML Template",
        Header:  "Welcome",
        Content: "This is a sample content.",
    }

    err = tmpl.Execute(os.Stdout, data)
    if err != nil {
        panic(err)
    }
}
```

输出结果：
```html
<!DOCTYPE html>
<html>
<head>
    <title>Go HTML Template</title>
</head>
<body>
    <h1>Welcome</h1>
    <p>THIS IS A SAMPLE CONTENT.</p>
</body>
</html>
```

### 总结

`html/template` 的几个语法点：<code v-pre>{{.Field}}</code> 取数据，`if`、`range` 管分支和循环，`|` 把左边结果传给下一个函数，<code v-pre>{{define}}</code> 加 <code v-pre>{{template}}</code> 拆模块。安全上记住一条：输出自动转义，`text/template` 不做这层，HTML 场景别用它。
