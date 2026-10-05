# 错误处理机制
### 错误处理机制

#### 8.1 内置错误处理

Gin 提供了内置的错误处理机制，方便开发者捕获和处理请求过程中的错误。

##### 8.1.1 `c.Error` 方法

使用 `c.Error` 方法可以在处理函数中记录错误：

```go
// someFunction 代表任一可能出错的业务调用
func someFunction() error {
    return errors.New("something went wrong")
}

func handler(c *gin.Context) {
    err := someFunction()
    if err != nil {
        c.Error(err)  // 记录错误
        c.JSON(500, gin.H{"error": err.Error()})
        return
    }
    c.JSON(200, gin.H{"message": "Success"})
}
```

##### 8.1.2 错误收集与处理

Gin 会自动收集所有通过 `c.Error` 记录的错误，并可以在中间件或处理函数中统一处理：

```go
func errorHandlingMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()  // 先执行其他处理函数

        // 检查是否有错误发生
        if len(c.Errors) > 0 {
            c.JSON(500, gin.H{"errors": c.Errors})
        }
    }
}
```

#### 8.2 自定义错误处理

内置的收发方式覆盖不了的场景，就自己定义错误类型和处理中间件。

##### 8.2.1 自定义错误类型

把状态码和消息打包成一个类型，响应时一次带出：

```go
type AppError struct {
    Code    int    `json:"code"`
    Message string `json:"message"`
}

func (e AppError) Error() string {
    return e.Message
}
```

##### 8.2.2 全局错误处理

通过中间件实现全局错误处理：

```go
func customErrorHandler() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()

        // 检查是否有错误发生
        if len(c.Errors) > 0 {
            err := c.Errors[0].Err
            if appErr, ok := err.(AppError); ok {
                c.JSON(appErr.Code, appErr)
            } else {
                c.JSON(500, gin.H{"error": "Internal Server Error"})
            }
        }
    }
}
```

##### 8.2.3 处理特定类型的错误

根据错误类型进行特定处理：

```go
// ValidationError 业务自定义的校验错误类型
type ValidationError struct {
    Field string
}

func (e ValidationError) Error() string {
    return "invalid field: " + e.Field
}

// someFunction 返回一个业务错误，这里以校验错误为例
func someFunction() error {
    return ValidationError{Field: "age"}
}

func handler(c *gin.Context) {
    err := someFunction()
    if err != nil {
        if validationErr, ok := err.(ValidationError); ok {
            c.JSON(400, gin.H{"error": validationErr.Error()})
        } else {
            c.Error(err)
            c.JSON(500, gin.H{"error": "Internal Server Error"})
        }
        return
    }
    c.JSON(200, gin.H{"message": "Success"})
}
```

#### 8.3 错误日志记录

错误挂到 `c.Errors` 上只是记在了请求里，要事后能查，还得落到日志。

##### 8.3.1 使用内置日志记录器

Gin 内置的日志记录器可以记录请求和错误信息：

```go
func main() {
    r := gin.Default()

    // 使用 Gin 默认的日志中间件
    r.Use(gin.Logger())

    r.GET("/example", func(c *gin.Context) {
        c.String(200, "example")
    })

    r.Run()
}
```

##### 8.3.2 自定义日志记录器

可以实现自定义的日志记录逻辑：

```go
func customLogger() gin.HandlerFunc {
    return func(c *gin.Context) {
        // 记录请求信息
        log.Printf("Request: %s %s", c.Request.Method, c.Request.URL.Path)

        c.Next()

        // 记录错误信息
        if len(c.Errors) > 0 {
            log.Printf("Errors: %v", c.Errors)
        }
    }
}

func main() {
    r := gin.New()

    // 使用自定义日志中间件
    r.Use(customLogger())

    r.GET("/example", func(c *gin.Context) {
        c.String(200, "example")
    })

    r.Run()
}
```

### 总结

Gin 的错误分三步走：`c.Error(err)` 把错误挂到当前请求上，中间件在 `c.Next()` 之后读 `c.Errors`，按 `AppError` 这类类型分派状态码，剩下的统一回 500。日志用内置的 `gin.Logger()` 起步，需要额外字段再换自定义中间件。