### Gin 框架概述

#### 1 Gin 是什么
Gin 是一个用 Go 编写的轻量级 Web 框架，API 短、路由快，常用来写 RESTful API 和微服务的 HTTP 层。

#### 2 Gin 的特点
- **路由快**：路由建立在 HTTP 路由树上，按路径逐段匹配。
- **API 短**：注册路由、取参数、回响应都收在 `*gin.Context` 上，代码量小。
- **中间件**：请求处理链可以插入自定义中间件。
- **内置中间件**：自带日志与恢复（panic 后返回 500 而不是崩掉进程）。
- **错误响应**：`c.JSON`/`c.String` 等方法直接控制状态码和响应体。

#### 3 Gin 的应用场景
- RESTful API 服务：路由加中间件已经覆盖大部分需求。
- 微服务架构：每个服务的 HTTP 层都用同一套 Gin 写法。
- 快速原型：几个路由就能把接口跑起来，适合 MVP 验证。

#### 4 Gin 的安装和快速入门

##### 4.1 安装 Gin
在你的 Go 环境中，可以通过以下命令安装 Gin：
```sh
go get -u github.com/gin-gonic/gin
```

##### 4.2 快速入门示例
一个最简的 HTTP 服务器：

```go
package main

import (
    "github.com/gin-gonic/gin"
)

func main() {
    // 创建一个默认的 Gin 路由器
    r := gin.Default()

    // 定义一个简单的 GET 路由
    r.GET("/ping", func(c *gin.Context) {
        c.JSON(200, gin.H{
            "message": "pong",
        })
    })

    // 启动 HTTP 服务器，监听 8080 端口
    r.Run(":8080")
}
```

运行后访问 `http://localhost:8080/ping`，响应是：
```json
{
    "message": "pong"
}
```

##### 4.3 路由和请求处理
路由匹配走 HTTP 路由树，多写几个路由看看取参：

```go
package main

import (
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()

    // 定义一个简单的 GET 路由
    r.GET("/hello", func(c *gin.Context) {
        name := c.Query("name")
        if name == "" {
            name = "World"
        }
        c.JSON(200, gin.H{
            "message": "Hello " + name,
        })
    })

    // 定义一个带参数的 GET 路由
    r.GET("/user/:name", func(c *gin.Context) {
        name := c.Param("name")
        c.JSON(200, gin.H{
            "message": "Hello " + name,
        })
    })

    // 启动 HTTP 服务器
    r.Run(":8080")
}
```

在这个示例中，`/hello` 路由返回一个带有 `name` 参数的 JSON 响应，而 `/user/:name` 路由则返回一个带有 URL 参数 `name` 的 JSON 响应。

### 总结
这一章装好了 Gin，写出了 `/ping` 和带参数的 `/user/:name` 两类路由。中间件、参数绑定、分组路由这些功能在后面的章节逐个展开。