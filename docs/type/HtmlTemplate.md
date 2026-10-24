# Html templates
In Go, the `html/template` package creates and executes HTML templates. It's similar to the `text/template` package, with one addition aimed at HTML safety: special characters are escaped automatically before interpolation, which prevents cross-site scripting (XSS) attacks. Use this package for anything involving HTML.

### 1. Basic usage

#### Creating and executing a simple template

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

Output:
```html
<h1>Hello, World!</h1>
```

### 2. Template syntax

#### Dynamic data

Use <code v-pre>{{.}}</code> to access the passed-in data. You can use <code v-pre>{{.Field}}</code> to access struct fields.

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

#### Conditional statements

Use `if` for conditional branching.

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

#### Loop statements

Use `range` to loop.

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

#### Pipes

A pipe uses one command's output as the next command's input.

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

### 3. Custom functions

You can add custom functions to a template.

#### Defining and registering a custom function

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

Output:
```html
<p>WORLD</p>
```

### 4. Nested templates

You can nest templates together to achieve modularity and reuse.

#### Defining and executing nested templates

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

Output:
```html
<header>Header Content</header>
<main>Body Content</main>
```

### 5. Common use cases

#### Generating HTML pages

You can use templates to generate dynamic HTML pages.

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

Output:
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

### 6. Common pitfalls

#### Automatic escaping

The `html/template` package escapes special characters in HTML automatically, making sure the generated HTML content is safe.

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

Output:
```html
<p>&lt;script&gt;alert('XSS');&lt;/script&gt;</p>
```

#### Safe template practices

- Avoid using `text/template` directly for HTML content; use `html/template` to stay safe.
- When a custom function returns an HTML-safe type, use the `template.HTML` type to mark HTML that has already been sanitized.

### Example code

Everything from the sections above put together: create a template, bind data, call a custom function, run it in one go.

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

Output:
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

### Summary

A few syntax points from `html/template`: <code v-pre>{{.Field}}</code> pulls data, `if` and `range` handle branching and loops, `|` passes the left-hand result to the next function, and <code v-pre>{{define}}</code> plus <code v-pre>{{template}}</code> split things into modules. On safety, remember one thing: output is escaped automatically, `text/template` doesn't do that layer, so don't use it for HTML.

## References

- [Language Spec · Types](https://go.dev/ref/spec#Types)
- [html/template standard library](https://pkg.go.dev/html/template)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [Float](/type/Float.md)
- [Int](/type/Int.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Float](/type/Float.md)
- [Int](/type/Int.md)
