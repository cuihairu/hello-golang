# 请求处理机制
### 请求处理机制

#### 6.1 请求上下文 (Context)

Gin 使用 `gin.Context` 结构体来管理请求的生命周期。`Context` 提供了对请求和响应的访问，并携带了中间件之间的共享数据。

##### 6.1.1 Context 的基本结构

`gin.Context` 结构体包含了请求和响应的相关信息：

```go
type Context struct {
    Request  *http.Request
    Writer   http.ResponseWriter
    Params   Params
    Keys     map[string]interface{}
    Errors   errorMsgs
    // 其他字段...
}
```

##### 6.1.2 Context 的使用

在处理函数中使用 `Context` 获取请求数据和设置响应数据：

```go
func handler(c *gin.Context) {
    // 获取请求参数
    name := c.Query("name")
    
    // 设置响应状态码和响应数据
    c.JSON(200, gin.H{"message": "Hello " + name})
}
```

#### 6.2 请求数据的解析

Gin 提供了多种方式来解析 HTTP 请求中的数据，包括查询参数、表单参数、JSON 请求体等。

##### 6.2.1 解析查询参数

使用 `c.Query` 方法解析 URL 中的查询参数：

```go
func handler(c *gin.Context) {
    name := c.Query("name")
    c.String(200, "Hello %s", name)
}
```

##### 6.2.2 解析表单参数

使用 `c.PostForm` 方法解析表单参数：

```go
func handler(c *gin.Context) {
    name := c.PostForm("name")
    c.String(200, "Hello %s", name)
}
```

##### 6.2.3 解析 JSON 请求体

使用 `c.ShouldBindJSON` 方法解析 JSON 请求体：

```go
type Login struct {
    User     string `json:"user" binding:"required"`
    Password string `json:"password" binding:"required"`
}

func handler(c *gin.Context) {
    var json Login
    if err := c.ShouldBindJSON(&json); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }
    c.JSON(200, gin.H{"message": "Login successful"})
}
```

##### 6.2.4 解析路径参数

使用 `c.Param` 方法解析路径参数：

```go
func handler(c *gin.Context) {
    id := c.Param("id")
    c.String(200, "ID: %s", id)
}
```

#### 6.3 请求生命周期

每个请求在 Gin 中都有一个完整的生命周期，从接收到请求到返回响应。请求的生命周期通常包括以下几个阶段：

1. **接收请求**：Gin 接收到 HTTP 请求，并创建一个新的 `gin.Context` 实例。
2. **中间件处理**：按照注册顺序执行全局中间件和路由组中间件。
3. **路由匹配**：根据请求的路径和方法进行路由匹配，找到对应的处理函数。
4. **请求处理**：执行处理函数，解析请求数据并生成响应数据。
5. **中间件后处理**：在处理函数执行完毕后，中间件可以继续执行后续操作。
6. **发送响应**：Gin 将响应数据发送给客户端，完成请求的处理。

#### 6.4 流式处理

流式处理用于处理大文件上传、下载和实时数据传输等场景。

##### 6.4.1 文件上传

Gin 提供了对多文件上传的支持：

```go
func uploadHandler(c *gin.Context) {
    file, _ := c.FormFile("file")
    c.SaveUploadedFile(file, "/path/to/save/"+file.Filename)
    c.String(200, "File uploaded successfully")
}
```

##### 6.4.2 文件下载

使用 `c.File` 方法发送文件给客户端：

```go
func downloadHandler(c *gin.Context) {
    c.File("/path/to/file")
}
```

##### 6.4.3 SSE（Server-Sent Events）

Gin 支持 SSE，用于实时数据推送：

```go
func sseHandler(c *gin.Context) {
    c.Stream(func(w io.Writer) bool {
        c.SSEvent("message", "Hello world")
        return true
    })
}
```

### 总结

本章详细介绍了 Gin 的请求处理机制，包括请求上下文、请求数据的解析、请求生命周期和流式处理。理解这些机制有助于开发者更好地管理 HTTP 请求的处理过程，提高 Web 应用的性能和扩展性。