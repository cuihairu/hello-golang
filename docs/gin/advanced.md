# 高级应用
### 高级应用

本章讲 Gin 的四个进阶场景：集成 GORM 操作数据库、JWT 认证、WebSocket 实时通信，以及部署和运维。

#### 13.1 Gin 与 GORM 集成

GORM 是 Go 语言里常用的 ORM 库。Gin 项目接上它之后，路由处理函数里可以直接查库、写库。

##### 13.1.1 GORM 简介

GORM 把数据库表映射成 Go 结构体（模型），`gorm.Open` 建立连接后返回 `*gorm.DB`，整个应用共用这一个实例。

##### 13.1.2 Gin 与 GORM 的集成步骤

- **配置 GORM 数据库连接**：
  ```go
  import (
      "gorm.io/driver/mysql"
      "gorm.io/gorm"
  )
  
  func SetupDatabase() *gorm.DB {
      dsn := "user:password@tcp(127.0.0.1:3306)/dbname"
      db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
      if err != nil {
          panic("failed to connect database")
      }
      return db
  }
  ```

- **在 Gin 中使用 GORM**：
  ```go
  import "github.com/gin-gonic/gin"

  // User 模型与数据库中的 users 表对应
  type User struct {
      ID   uint   `json:"id"`
      Name string `json:"name"`
  }

  func main() {
      r := gin.Default()
      db := SetupDatabase()
      r.GET("/users", func(c *gin.Context) {
          var users []User
          db.Find(&users)
          c.JSON(200, users)
      })
      r.Run()
  }
  ```

##### 13.1.3 常见问题和调试

- **数据库连接问题**：连接失败先看 `gorm.Open` 返回的 err，多数是 DSN 写错或数据库没启动。
- **性能优化**：查询慢先查缺不缺索引，避免在循环里逐条查询。

#### 13.2 Gin 与 JWT 认证

JWT（JSON Web Token）是一种常用的认证机制：服务端签发 token，客户端随请求携带，服务端验签通过才放行。

##### 13.2.1 JWT 简介

- **JWT 基本概念**：token 由头部、负载、签名三部分组成，签发和验证用同一套密钥。
- **JWT 的安装和配置**：使用 `github.com/golang-jwt/jwt/v5`，它是已停止维护的 `github.com/dgrijalva/jwt-go` 的社区继任分支。

##### 13.2.2 Gin 中实现 JWT 认证

- **生成 JWT**：
  ```go
  import "github.com/golang-jwt/jwt/v5"

  func GenerateToken(username string) (string, error) {
      token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
          "username": username,
      })
      return token.SignedString([]byte("secret"))
  }
  ```

- **解析 JWT**：
  ```go
  func ParseToken(tokenStr string) (*jwt.Token, error) {
      return jwt.Parse(tokenStr, func(token *jwt.Token) (interface{}, error) {
          return []byte("secret"), nil
      })
  }
  ```

- **在 Gin 中使用 JWT 认证中间件**：
  ```go
  func AuthMiddleware() gin.HandlerFunc {
      return func(c *gin.Context) {
          tokenStr := c.GetHeader("Authorization")
          _, err := ParseToken(tokenStr)
          if err != nil {
              c.JSON(401, gin.H{"message": "Unauthorized"})
              c.Abort()
              return
          }
          c.Next()
      }
  }
  
  func main() {
      r := gin.Default()
      r.Use(AuthMiddleware())
      r.GET("/protected", func(c *gin.Context) {
          c.JSON(200, gin.H{"message": "Welcome"})
      })
      r.Run()
  }
  ```

##### 13.2.3 常见问题和调试

- **Token 无效**：多半是签发和验证用的密钥不一致，对比 `GenerateToken` 和 `ParseToken` 里的密钥。
- **安全性考虑**：示例中的密钥是写死的 `secret`，实际项目要从配置或环境变量读取，不要提交到代码仓库。

#### 13.3 Gin 与 WebSocket

WebSocket 用于实时通信：先通过 HTTP 完成协议升级，之后双方都能主动发消息，适合聊天、推送这类场景。

##### 13.3.1 WebSocket 简介

- **WebSocket 基本概念**：连接升级建立后保持长连接，不再需要客户端轮询。
- **WebSocket 的安装和配置**：使用 `github.com/gorilla/websocket`。

##### 13.3.2 Gin 中实现 WebSocket

- **创建 WebSocket 处理器**：
  ```go
  import (
      "net/http"

      "github.com/gin-gonic/gin"
      "github.com/gorilla/websocket"
  )

  var upgrader = websocket.Upgrader{
      CheckOrigin: func(r *http.Request) bool {
          return true
      },
  }
  
  func WebSocketHandler(c *gin.Context) {
      conn, err := upgrader.Upgrade(c.Writer, c.Request, nil)
      if err != nil {
          c.JSON(500, gin.H{"message": "Failed to upgrade connection"})
          return
      }
      defer conn.Close()
      for {
          msgType, msg, err := conn.ReadMessage()
          if err != nil {
              break
          }
          conn.WriteMessage(msgType, msg)
      }
  }
  
  func main() {
      r := gin.Default()
      r.GET("/ws", WebSocketHandler)
      r.Run()
  }
  ```

##### 13.3.3 常见问题和调试

- **连接问题**：`upgrader.Upgrade` 返回 err 时，检查请求头是否满足升级条件、`CheckOrigin` 是否放行。
- **性能优化**：示例中 `ReadMessage` 是阻塞的，连接数多时注意服务端的 goroutine 数量。

#### 13.4 Gin 的部署与运维

##### 13.4.1 部署策略

- **容器化部署**：用 Docker 打镜像，跑 Gin 应用。
- **云服务部署**：部署到 AWS、GCP、Azure 这类云平台。

##### 13.4.2 监控和日志

- **应用监控**：用 Prometheus、Grafana 看 Gin 应用的性能和健康状况。
- **日志管理**：配置并管理 Gin 应用的日志记录。

##### 13.4.3 性能优化

- **性能调优**：先用性能分析工具找到热点，再针对性优化。
- **缓存和负载均衡**：热点数据进缓存，流量用负载均衡分摊，响应速度和可用性都跟着上来。

##### 13.4.4 常见运维问题

- **故障排除**：按日志和监控指标排查 Gin 应用的常见问题。
- **升级和维护**：应用的升级和维护，保证系统稳定和安全。