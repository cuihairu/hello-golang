# 测试与调试
### 测试与调试

#### 11.1 Gin 的测试方法

Gin 的测试大多不用真的起 HTTP 服务：构造路由，用 `httptest.NewRecorder()` 记录响应，再比对状态码和响应体。

##### 11.1.1 单元测试

单元测试关注于测试应用中的单个组件或函数，确保它们按照预期工作。

```go
import (
    "net/http"
    "net/http/httptest"
    "testing"
    "github.com/gin-gonic/gin"
)

func TestHelloWorld(t *testing.T) {
    // 创建一个新的 Gin 路由
    r := gin.Default()
    r.GET("/hello", func(c *gin.Context) {
        c.String(http.StatusOK, "Hello, World!")
    })

    // 创建一个 HTTP 请求
    req, err := http.NewRequest(http.MethodGet, "/hello", nil)
    if err != nil {
        t.Fatalf("Failed to create request: %v", err)
    }

    // 记录响应
    resp := httptest.NewRecorder()
    r.ServeHTTP(resp, req)

    // 验证响应状态码
    if resp.Code != http.StatusOK {
        t.Errorf("Expected status code %d but got %d", http.StatusOK, resp.Code)
    }

    // 验证响应内容
    expectedBody := "Hello, World!"
    if resp.Body.String() != expectedBody {
        t.Errorf("Expected body %q but got %q", expectedBody, resp.Body.String())
    }
}
```

##### 11.1.2 集成测试

集成测试关注于测试应用的多个组件之间的交互，通常涉及到完整的应用环境和真实的请求/响应。

```go
import (
    "net/http"
    "net/http/httptest"
    "testing"
    "github.com/gin-gonic/gin"
)

func TestIntegration(t *testing.T) {
    r := gin.Default()
    r.GET("/greet/:name", func(c *gin.Context) {
        name := c.Param("name")
        c.JSON(http.StatusOK, gin.H{"greeting": "Hello, " + name})
    })

    req, err := http.NewRequest(http.MethodGet, "/greet/John", nil)
    if err != nil {
        t.Fatalf("Failed to create request: %v", err)
    }

    resp := httptest.NewRecorder()
    r.ServeHTTP(resp, req)

    if resp.Code != http.StatusOK {
        t.Errorf("Expected status code %d but got %d", http.StatusOK, resp.Code)
    }

    expectedBody := `{"greeting":"Hello, John"}`
    if resp.Body.String() != expectedBody {
        t.Errorf("Expected body %q but got %q", expectedBody, resp.Body.String())
    }
}
```

##### 11.1.3 性能测试

性能测试用 `testing.B` 衡量单个请求处理的耗时。

```go
import (
    "testing"
    "github.com/gin-gonic/gin"
    "net/http"
    "net/http/httptest"
)

func BenchmarkHelloWorld(b *testing.B) {
    r := gin.Default()
    r.GET("/hello", func(c *gin.Context) {
        c.String(http.StatusOK, "Hello, World!")
    })

    req, _ := http.NewRequest(http.MethodGet, "/hello", nil)
    resp := httptest.NewRecorder()

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        r.ServeHTTP(resp, req)
    }
}
```

#### 11.2 单元测试与集成测试

##### 11.2.1 单元测试

单元测试是对代码中的单个函数或方法进行的测试。它们通常是自动化的，并且应该快速执行，重点是测试代码的功能是否符合预期。

- **测试函数**：编写专门的测试函数来验证各个处理函数的逻辑。
- **Mock 数据**：使用 Mock 或假数据来测试函数在不同输入下的行为。

##### 11.2.2 集成测试

集成测试关注于系统的多个部分如何协同工作，通常包括与数据库、缓存或其他服务的交互。

- **测试整个路由**：包括多个处理函数和中间件的集成测试。
- **模拟服务**：使用模拟服务来替代真实服务，进行端到端测试。

#### 11.3 常见问题调试

排查问题时，最直接的手段是把请求和响应记录下来。

##### 11.3.1 调试请求和响应

使用 Gin 的内置日志功能或者自定义日志中间件来记录请求和响应，以便排查问题。

```go
func debugLogger() gin.HandlerFunc {
    return func(c *gin.Context) {
        log.Printf("Request: %s %s", c.Request.Method, c.Request.URL.Path)
        c.Next()
        log.Printf("Response: %d", c.Writer.Status())
    }
}
```

注意：`c.Writer` 是 `gin.ResponseWriter` 接口，它只暴露 `Status()`、`Size()`、`Written()`、`Header()` 等方法，并没有 `Body` 字段，无法直接读取响应体。如果确实需要记录响应体，可以自定义一个包装了 `http.ResponseWriter` 的类型，在 `Write` 时把内容缓存下来再通过中间件输出。

func main() {
    r := gin.Default()
    r.Use(debugLogger())
    r.GET("/debug", func(c *gin.Context) {
        c.String(http.StatusOK, "Debug Info")
    })
    r.Run()
}
```

##### 11.3.2 处理错误信息

在错误处理中提供详细的错误信息，以便于定位问题源。

```go
func errorHandling() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()
        if len(c.Errors) > 0 {
            for _, e := range c.Errors {
                log.Printf("Error: %v", e.Err)
            }
            c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal Server Error"})
        }
    }
}
```

##### 11.3.3 使用调试工具

利用 Go 的调试工具（如 `delve`）进行深入的调试，设置断点，查看变量值和调用栈。

```bash
dlv debug main.go
```

### 总结

Gin 的测试用 `httptest` 就能做，单元测试、集成测试、基准测试都不需要起真实端口；调试先看日志中间件里的请求方法、路径和响应状态码，再不够就用 `dlv` 打断点查变量和调用栈。