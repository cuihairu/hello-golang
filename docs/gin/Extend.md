# 扩展
### Gin 的扩展

Gin 的扩展有两条路：装社区现成的插件，或者按需求写自己的插件。本章讲插件机制、常用插件和自定义插件的做法。

#### 14.1 插件机制

##### 14.1.1 插件机制概述

- **插件的定义和作用**：Gin 里说的插件，一般是能挂到引擎上的模块，用来补 Gin 没做的功能。
- **插件的安装和配置**：`go get` 拉包，`r.Use(...)` 挂载，配置写在自己的代码里。

##### 14.1.2 Gin 的插件架构

- **插件的生命周期**：随包导入加载，在 `main` 里注册后生效，进程退出即结束。
- **插件的接口**：中间件就是一个返回 `gin.HandlerFunc` 的函数。

##### 14.1.3 常见插件类型

- **中间件插件**：扩展 Gin 的中间件功能。
- **路由插件**：提供自定义路由功能。
- **数据处理插件**：处理数据验证、转换等功能。

#### 14.2 社区常用插件介绍

##### 14.2.1 中间件插件

- **Gin CORS**：跨域资源共享插件，允许配置跨域请求。
  - **安装**：
    ```shell
    go get -u github.com/gin-contrib/cors
    ```
  - **使用**：
    ```go
    import (
        "github.com/gin-contrib/cors"
        "github.com/gin-gonic/gin"
    )

    func main() {
        r := gin.Default()
        r.Use(cors.Default())
        r.Run()
    }
    ```

- **Gin Logger**：日志记录插件，用于记录 HTTP 请求日志。
  - **安装**：
    ```shell
    go get -u github.com/gin-contrib/logger
    ```
  - **使用**：
    ```go
    import (
        "github.com/gin-contrib/logger"
        "github.com/gin-gonic/gin"
    )

    func main() {
        r := gin.Default()
        r.Use(logger.SetLogger())
        r.Run()
    }
    ```

##### 14.2.2 路由插件

- **Gin Swagger**：自动生成 API 文档插件。
  - **安装**：
    ```shell
    go get -u github.com/swaggo/gin-swagger
    ```
  - **使用**：
    ```go
    import (
        "github.com/gin-gonic/gin"
        "github.com/swaggo/files"
        ginSwagger "github.com/swaggo/gin-swagger"
    )

    func main() {
        r := gin.Default()
        r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))
        r.Run()
    }
    ```

    注意：`ginSwagger.WrapHandler` 依赖 `github.com/swaggo/files` 提供的静态资源，两处导入缺一不可；另外还需要用 `swag init` 生成文档，并在代码中以空白导入的方式引入生成的 docs 包（`_ "your-module/docs"`），否则访问 `/swagger/index.html` 会提示找不到文档。

##### 14.2.3 数据处理插件

- **Gin Validator**：数据验证插件，用于验证请求数据。
  - **安装**：
    ```shell
    go get -u github.com/go-playground/validator/v10
    ```
  - **使用**：
    ```go
    import (
        "github.com/gin-gonic/gin"
        "github.com/go-playground/validator/v10"
    )

    type MyData struct {
        Name  string `json:"name" validate:"required"`
        Email string `json:"email" validate:"required,email"`
    }

    func main() {
        r := gin.Default()
        v := validator.New()
        r.POST("/validate", func(c *gin.Context) {
            var data MyData
            if err := c.ShouldBindJSON(&data); err != nil {
                c.JSON(400, gin.H{"error": err.Error()})
                return
            }
            if err := v.Struct(data); err != nil {
                c.JSON(400, gin.H{"error": err.Error()})
                return
            }
            c.JSON(200, gin.H{"message": "Valid"})
        })
        r.Run()
    }
    ```

#### 14.3 自定义插件开发

##### 14.3.1 插件开发概述

- **自定义插件的定义和用途**：把一段请求前后的逻辑包成 `gin.HandlerFunc`，放在独立的包里，哪个项目要就引哪个。
- **插件的结构和设计**：一个函数返回 handler，内部处理完调用 `c.Next()` 交给后续逻辑。

##### 14.3.2 自定义中间件插件

- **创建自定义中间件**：
  ```go
  package middleware
  
  import "github.com/gin-gonic/gin"
  
  func CustomMiddleware() gin.HandlerFunc {
      return func(c *gin.Context) {
          // 处理请求
          c.Next()
      }
  }
  ```

- **使用自定义中间件**：
  ```go
  func main() {
      r := gin.Default()
      r.Use(middleware.CustomMiddleware())
      r.GET("/", func(c *gin.Context) {
          c.String(200, "Hello, World!")
      })
      r.Run()
  }
  ```

##### 14.3.3 自定义路由插件

- **创建自定义路由插件**：
  ```go
  package routes
  
  import "github.com/gin-gonic/gin"
  
  func RegisterRoutes(r *gin.Engine) {
      r.GET("/custom", func(c *gin.Context) {
          c.String(200, "Custom Route")
      })
  }
  ```

- **使用自定义路由插件**：
  ```go
  func main() {
      r := gin.Default()
      routes.RegisterRoutes(r)
      r.Run()
  }
  ```

##### 14.3.4 自定义数据处理插件

- **创建自定义数据处理插件**：
  ```go
  package processor
  
  import "github.com/gin-gonic/gin"
  
  func ProcessData(c *gin.Context) {
      // 数据处理逻辑
      c.Next()
  }
  ```

- **使用自定义数据处理插件**：
  ```go
  func main() {
      r := gin.Default()
      r.POST("/process", processor.ProcessData)
      r.Run()
  }
  ```

##### 14.3.5 插件的发布与共享

- **发布插件**：如何将自定义插件发布到开源社区或公司内部共享。
- **插件的文档和示例**：如何为自定义插件编写文档和示例代码，帮助用户理解和使用插件。

社区插件已经覆盖了常见需求：CORS、日志、Swagger 文档、参数校验。自己的逻辑写成 `gin.HandlerFunc`，用 `r.Use(...)` 挂成中间件，或者像路由那样单独注册。