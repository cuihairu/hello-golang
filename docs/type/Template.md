# Templates
In Go, the `text/template` package embeds dynamic data into static text, commonly used to generate configuration files, email content, and reports.

### 1. Basic usage

#### Creating and executing a simple template

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

Output:
```
Hello, World!
```

### 2. Template syntax

#### Dynamic data

Use <code v-pre>{{.}}</code> to access the passed-in data. You can use <code v-pre>{{.Field}}</code> to access struct fields.

```go
package main

import "text/template"

func main() {
    tmpl, err := template.New("example").Parse("Name: {{.Name}}, Age: {{.Age}}")
    _ = tmpl
    _ = err
}
```

#### Conditional statements

Use `if` for conditional branching.

```go
package main

import "text/template"

func main() {
    tmpl, err := template.New("example").Parse(`{{if .Active}}User is active{{else}}User is inactive{{end}}`)
    _ = tmpl
    _ = err
}
```

#### Loop statements

Use `range` to loop.

```go
package main

import "text/template"

func main() {
    tmpl, err := template.New("example").Parse(`{{range .Items}}{{.}}, {{end}}`)
    _ = tmpl
    _ = err
}
```

#### Pipes

A pipe uses one command's output as the next command's input.

```go
package main

import "text/template"

func main() {
    tmpl, err := template.New("example").Parse(`{{.Name | printf "Hello, %s!"}}`)
    _ = tmpl
    _ = err
}
```

### 3. Template functions

`text/template` ships with a few built-in functions, such as `print` and `html`. You can use them to process data.

#### Using built-in functions

```go
package main

import "text/template"

func main() {
    tmpl, err := template.New("example").Parse(`{{printf "Hello, %s!" .Name}}`)
    _ = tmpl
    _ = err
}
```

### 4. Custom functions

You can add custom functions to a template.

#### Defining and registering a custom function

```go
package main

import (
    "os"
    "strings"
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

Output:
```
WORLD
```

### 5. Nested templates

You can nest templates together to achieve modularity and reuse.

#### Defining and executing nested templates

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

Output:
```
Header Content
Body Content
```

### 6. Common use cases

#### Generating configuration files

You can use templates to generate dynamic configuration files.

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

Output:
```
server {
    listen 8080;
    server_name localhost;
}
```

#### Generating email content

You can use templates to generate dynamic email content.

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

Output:
```
Hello John,

Thank you for your purchase!

Order details:
Product: Go Programming Book
Price: 29.99
```

### Summary

`text/template` has just these pieces of syntax: <code v-pre>{{.Field}}</code> reads a value, <code v-pre>{{if}}</code> and <code v-pre>{{range}}</code> control flow, `|` connects pipes, `Funcs` registers custom functions, and <code v-pre>{{define}}</code> and <code v-pre>{{template}}</code> split templates apart. For generating repetitive text like configs and emails, these are enough.

## References

- [Language Spec · Types](https://go.dev/ref/spec#Types)
- [text/template standard library](https://pkg.go.dev/text/template)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [Switch](/type/Switch.md)
- [Type](/type/Type.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Type](/type/Type.md)
