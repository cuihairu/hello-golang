# Response handling
### Response handling

#### 7.1 JSON/XML/HTML responses

Gin provides several response formats, including JSON, XML, and HTML.

##### 7.1.1 JSON response

Use the `c.JSON` method to return a JSON response:

```go
func jsonResponse(c *gin.Context) {
    c.JSON(200, gin.H{"message": "Hello, world!"})
}
```

##### 7.1.2 XML response

Use the `c.XML` method to return an XML response:

```go
func xmlResponse(c *gin.Context) {
    c.XML(200, gin.H{"message": "Hello, world!"})
}
```

##### 7.1.3 HTML response

Use the `c.HTML` method to return an HTML response:

```go
func htmlResponse(c *gin.Context) {
    c.HTML(200, "index.html", gin.H{"title": "Hello, world!"})
}
```

#### 7.2 Setting the response status code

Gin lets you set the HTTP response status code in several ways.

##### 7.2.1 Basic status code

Use the `c.Status` method to set the status code:

```go
func statusCodeResponse(c *gin.Context) {
    c.Status(204)
}
```

##### 7.2.2 JSON response with a status code

You can set the status code at the same time as returning a JSON response:

```go
func jsonResponseWithStatus(c *gin.Context) {
    c.JSON(201, gin.H{"message": "Resource created"})
}
```

#### 7.3 File responses

Gin supports file responses, which is handy for file downloads and similar cases.

##### 7.3.1 Sending a file

Use the `c.File` method to send a file:

```go
func fileResponse(c *gin.Context) {
    c.File("/path/to/file")
}
```

##### 7.3.2 File attachment download

Use the `c.FileAttachment` method to download a file as an attachment:

```go
func fileAttachmentResponse(c *gin.Context) {
    c.FileAttachment("/path/to/file", "filename.pdf")
}
```

#### 7.4 Custom renderers

Gin lets you define custom renderers to support more response formats.

##### 7.4.1 Defining a renderer

A custom renderer has to implement the `render.Render` interface (`github.com/gin-gonic/gin/render`), which has two methods: `Render(http.ResponseWriter) error` and `WriteContentType(http.ResponseWriter)`:

```go
package main

import (
    "net/http"
)

type MyRenderer struct {
    Data string
}

func (r MyRenderer) Render(w http.ResponseWriter) error {
    // implement the rendering logic, writing the data into the response body
    _, err := w.Write([]byte("data: " + r.Data))
    return err
}

func (r MyRenderer) WriteContentType(w http.ResponseWriter) {
    w.Header().Set("Content-Type", "application/myformat")
}
```

##### 7.4.2 Using a custom renderer

Use `c.Render` with a custom renderer to return a response:

```go
func customRenderResponse(c *gin.Context) {
    c.Render(200, MyRenderer{Data: "Hello, custom render"})
}
```

### Summary

All of these exits are methods on `gin.Context`: use `c.JSON` for JSON, `c.XML` for XML, `c.HTML` for HTML, `c.File` and `c.FileAttachment` for file downloads, and implement the `render.Render` interface and hand it to `c.Render` for your own format.

## References

- [Gin Official Documentation](https://gin-gonic.com/en/docs/)
- [Gin · pkg.go.dev](https://pkg.go.dev/github.com/gin-gonic/gin)


## Sibling pages

- [Config](/gin/Config.md)
- [Debug](/gin/Debug.md)
- [Error](/gin/Error.md)
- [Request](/gin/Request.md)
- [Route](/gin/Route.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Request](/gin/Request.md)
- [Route](/gin/Route.md)
