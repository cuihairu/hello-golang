# Extend
### Extending Gin

There are two ways to extend Gin: install a ready-made community plugin, or write your own for your needs. This page collects Gin's plugin mechanism, common plugins, and how to build custom ones.

#### 14.1 Plugin mechanism

##### 14.1.1 Overview of the plugin mechanism

- **What plugins are and what they do**: a plugin in Gin is usually a module that hangs off the engine, filling in what Gin doesn't do itself.
- **Installing and configuring plugins**: pull the package with `go get`, mount it with `r.Use(...)`, and keep the configuration in your own code.

##### 14.1.2 Gin's plugin architecture

- **Plugin lifecycle**: loaded when the package is imported, taking effect once registered in `main`, and ending when the process exits.
- **Plugin interface**: middleware is just a function that returns a `gin.HandlerFunc`.

##### 14.1.3 Common plugin types

- **Middleware plugins**: extend Gin's middleware capabilities.
- **Routing plugins**: provide custom routing.
- **Data-processing plugins**: handle data validation, conversion, and the like.

#### 14.2 Common community plugins

##### 14.2.1 Middleware plugins

- **Gin CORS**: a CORS (cross-origin resource sharing) plugin that lets you configure cross-origin requests.
  - **Install**:
    ```shell
    go get -u github.com/gin-contrib/cors
    ```
  - **Usage**:
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

- **Gin Logger**: a logging plugin for recording HTTP request logs.
  - **Install**:
    ```shell
    go get -u github.com/gin-contrib/logger
    ```
  - **Usage**:
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

##### 14.2.2 Routing plugins

- **Gin Swagger**: a plugin that generates API documentation automatically.
  - **Install**:
    ```shell
    go get -u github.com/swaggo/gin-swagger
    ```
  - **Usage**:
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

    Note: `ginSwagger.WrapHandler` depends on the static assets provided by `github.com/swaggo/files`, so both imports are required; you also need to run `swag init` to generate the docs and import the generated docs package with a blank import (`_ "your-module/docs"`), otherwise `/swagger/index.html` will report that no documentation was found.

##### 14.2.3 Data-processing plugins

- **Gin Validator**: a data-validation plugin for validating request data.
  - **Install**:
    ```shell
    go get -u github.com/go-playground/validator/v10
    ```
  - **Usage**:
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

#### 14.3 Writing your own plugins

##### 14.3.1 Plugin development overview

- **What custom plugins are for**: wrap a piece of pre- or post-request logic in a `gin.HandlerFunc`, put it in its own package, and import it in whichever project needs it.
- **Plugin structure and design**: a function returns the handler, and after its own work it calls `c.Next()` to hand off to what follows.

##### 14.3.2 Custom middleware plugins

- **Creating a custom middleware**:
  ```go
  package middleware
  
  import "github.com/gin-gonic/gin"
  
  func CustomMiddleware() gin.HandlerFunc {
      return func(c *gin.Context) {
          // handle the request
          c.Next()
      }
  }
  ```

- **Using the custom middleware**:
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

##### 14.3.3 Custom routing plugins

- **Creating a custom routing plugin**:
  ```go
  package routes
  
  import "github.com/gin-gonic/gin"
  
  func RegisterRoutes(r *gin.Engine) {
      r.GET("/custom", func(c *gin.Context) {
          c.String(200, "Custom Route")
      })
  }
  ```

- **Using the custom routing plugin**:
  ```go
  func main() {
      r := gin.Default()
      routes.RegisterRoutes(r)
      r.Run()
  }
  ```

##### 14.3.4 Custom data-processing plugins

- **Creating a custom data-processing plugin**:
  ```go
  package processor
  
  import "github.com/gin-gonic/gin"
  
  func ProcessData(c *gin.Context) {
      // data processing logic
      c.Next()
  }
  ```

- **Using the custom data-processing plugin**:
  ```go
  func main() {
      r := gin.Default()
      r.POST("/process", processor.ProcessData)
      r.Run()
  }
  ```

##### 14.3.5 Publishing and sharing plugins

- **Publishing plugins**: how to release a custom plugin to the open-source community or share it internally at your company.
- **Plugin docs and examples**: how to write documentation and example code for a custom plugin, so users can understand and use it.

Community plugins already cover the common needs: CORS, logging, Swagger docs, and parameter validation. Write your own logic as a `gin.HandlerFunc`, mount it as middleware with `r.Use(...)`, or register it on its own the way routes are.

## References

- [Gin Official Documentation](https://gin-gonic.com/en/docs/)
- [Gin · pkg.go.dev](https://pkg.go.dev/github.com/gin-gonic/gin)

## Sibling pages

- [Config](/gin/Config.md)
- [Debug](/gin/Debug.md)
- [Error](/gin/Error.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Config](/gin/Config.md)
- [Debug](/gin/Debug.md)
- [Error](/gin/Error.md)
- [Gin](/gin/Gin.md)
