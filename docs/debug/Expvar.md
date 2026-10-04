`expvar` 是 Go 标准库的包，把程序运行时的变量和统计信息以 JSON 格式暴露出来，供监控和调试用。

### 主要功能

- **运行时统计**：请求计数、错误计数、内存使用这类数据随程序运行更新。
- **HTTP 暴露**：数据挂在 HTTP 服务上，访问 `/debug/vars` 就能拿到。

### 使用方法

#### 1. **导入 `expvar` 包**

```go
import (
    "expvar"
    "net/http"
)
```

#### 2. **定义和注册变量**

`expvar` 提供了 `Int`, `Float`, `String`, 和 `Map` 类型的变量，你可以用来记录各种统计数据。例如：

```go
var (
    requestCount = expvar.NewInt("request_count")
    errorCount   = expvar.NewInt("error_count")
    version      = expvar.NewString("version")
)

func main() {
    version.Set("1.0.0")  // 设置应用程序版本

    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        requestCount.Add(1) // 增加请求计数
        // 模拟处理请求
        w.Write([]byte("Hello, world!"))
    })

    http.ListenAndServe(":8080", nil)
}
```

#### 3. **使用 `Map` 类型**

`Map` 把多个相关的指标放在一起，创建后同样以 JSON 导出。例如：

```go
var metrics = expvar.NewMap("metrics")

func main() {
    metrics.Set("requests", expvar.NewInt("requests"))
    metrics.Set("errors", expvar.NewInt("errors"))

    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        metrics.Get("requests").(*expvar.Int).Add(1)
        // 模拟处理请求
        w.Write([]byte("Hello, world!"))
    })

    http.ListenAndServe(":8080", nil)
}
```

#### 4. **查看 `expvar` 数据**

运行你的应用程序后，可以通过访问 `http://localhost:8080/debug/vars` 来查看导出的变量。`expvar` 以 JSON 格式返回数据，例如：

```json
{
    "request_count": 100,
    "error_count": 5,
    "version": "1.0.0",
    "metrics": {
        "requests": 100,
        "errors": 5
    }
}
```

### 进阶使用

- **自定义类型**：实现 `expvar.Var` 接口，就能导出自己写的类型。

- **集成监控**：Prometheus 这类监控系统可以通过 HTTP 接口抓取 `expvar` 数据。

### 注意事项

- **安全性**：`expvar` 暴露的接口可能带敏感信息，生产环境要给 `debug/vars` 加访问控制。

- **性能**：适合低频统计；更新频率很高时换更专用的监控工具。

想给程序快速加几个运行时计数器，`expvar` 是标准库自带的现成方案，不用引第三方依赖。