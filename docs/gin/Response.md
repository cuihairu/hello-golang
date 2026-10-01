# 响应处理机制
### 响应处理机制

#### 7.1 JSON/XML/HTML 响应

Gin 提供了多种响应格式，包括 JSON、XML 和 HTML。

##### 7.1.1 JSON 响应

使用 `c.JSON` 方法返回 JSON 格式的响应：

```go
func jsonResponse(c *gin.Context) {
    c.JSON(200, gin.H{"message": "Hello, world!"})
}
```

##### 7.1.2 XML 响应

使用 `c.XML` 方法返回 XML 格式的响应：

```go
func xmlResponse(c *gin.Context) {
    c.XML(200, gin.H{"message": "Hello, world!"})
}
```

##### 7.1.3 HTML 响应

使用 `c.HTML` 方法返回 HTML 格式的响应：

```go
func htmlResponse(c *gin.Context) {
    c.HTML(200, "index.html", gin.H{"title": "Hello, world!"})
}
```

#### 7.2 响应状态码设置

Gin 可以通过多种方法设置 HTTP 响应状态码。

##### 7.2.1 基本状态码设置

使用 `c.Status` 方法设置状态码：

```go
func statusCodeResponse(c *gin.Context) {
    c.Status(204)
}
```

##### 7.2.2 带状态码的 JSON 响应

在返回 JSON 响应时可以同时设置状态码：

```go
func jsonResponseWithStatus(c *gin.Context) {
    c.JSON(201, gin.H{"message": "Resource created"})
}
```

#### 7.3 文件响应

Gin 支持返回文件响应，方便处理文件下载等场景。

##### 7.3.1 发送文件

使用 `c.File` 方法发送文件：

```go
func fileResponse(c *gin.Context) {
    c.File("/path/to/file")
}
```

##### 7.3.2 文件附件下载

使用 `c.FileAttachment` 方法作为附件下载文件：

```go
func fileAttachmentResponse(c *gin.Context) {
    c.FileAttachment("/path/to/file", "filename.pdf")
}
```

#### 7.4 自定义渲染器

Gin 允许开发者定义自定义渲染器，以支持更多类型的响应格式。

##### 7.4.1 定义渲染器接口

自定义渲染器需要实现 `gin.Render` 接口：

```go
type MyRenderer struct {
    Data any
}

func (r MyRenderer) Render(w io.Writer) error {
    // 实现渲染逻辑
    return nil
}

func (r MyRenderer) WriteContentType(w http.ResponseWriter) {
    w.Header().Set("Content-Type", "application/myformat")
}
```

##### 7.4.2 使用自定义渲染器

使用自定义渲染器返回响应：

```go
func customRenderResponse(c *gin.Context) {
    c.Render(200, MyRenderer{Data: "Hello, custom render"})
}
```

### 总结

本章介绍了 Gin 的响应处理机制，包括 JSON、XML 和 HTML 响应，响应状态码设置，文件响应以及自定义渲染器。掌握这些技术，可以帮助开发者灵活地处理和返回不同格式的响应，提高 Web 应用的用户体验和功能多样性。