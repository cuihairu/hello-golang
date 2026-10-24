# Advanced Applications
### Advanced Applications

This page records four advanced scenarios for Gin: integrating GORM to work with a database, JWT authentication, WebSocket real-time communication, and deployment and operations.

#### 13.1 Integrating Gin with GORM

GORM is a commonly used ORM library in Go. Once a Gin project is wired up to it, route handlers can query and write to the database directly.

##### 13.1.1 Introduction to GORM

GORM maps database tables to Go structs (models); `gorm.Open` establishes the connection and returns `*gorm.DB`, which the whole application shares as a single instance.

##### 13.1.2 Steps to Integrate Gin with GORM

- **Configure the GORM database connection**:
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

- **Use GORM in Gin**:
  ```go
  import "github.com/gin-gonic/gin"

  // the User model corresponds to the users table in the database
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

##### 13.1.3 Common Issues and Debugging

- **Database connection problems**: when a connection fails, first look at the err returned by `gorm.Open`; usually the DSN is wrong or the database is not started.
- **Performance optimization**: when queries are slow, first check whether indexes are missing, and avoid querying row by row inside a loop.

#### 13.2 JWT Authentication with Gin

JWT (JSON Web Token) is a common authentication mechanism: the server issues a token, the client carries it with the request, and the server only lets it through once the signature verifies.

##### 13.2.1 Introduction to JWT

- **Basic JWT concepts**: a token is made of three parts — header, payload, and signature — and issuing and verifying use the same set of keys.
- **Installing and configuring JWT**: use `github.com/golang-jwt/jwt/v5`, the community successor branch of the unmaintained `github.com/dgrijalva/jwt-go`.

##### 13.2.2 Implementing JWT Authentication in Gin

- **Generate a JWT**:
  ```go
  import "github.com/golang-jwt/jwt/v5"

  func GenerateToken(username string) (string, error) {
      token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
          "username": username,
      })
      return token.SignedString([]byte("secret"))
  }
  ```

- **Parse a JWT**:
  ```go
  import "github.com/golang-jwt/jwt/v5"

  func ParseToken(tokenStr string) (*jwt.Token, error) {
      return jwt.Parse(tokenStr, func(token *jwt.Token) (interface{}, error) {
          return []byte("secret"), nil
      })
  }
  ```

- **Use a JWT authentication middleware in Gin**:
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

##### 13.2.3 Common Issues and Debugging

- **Invalid token**: most of the time the issuing and verifying keys do not match; compare the keys in `GenerateToken` and `ParseToken`.
- **Security considerations**: the key in the example is the hardcoded `secret`; in a real project read it from configuration or environment variables, and never commit it to the code repository.

#### 13.3 Gin with WebSocket

WebSocket is used for real-time communication: first the protocol is upgraded over HTTP, and afterwards both sides can send messages proactively. It suits scenarios like chat and push notifications.

##### 13.3.1 Introduction to WebSocket

- **Basic WebSocket concepts**: once the connection upgrade is established, the long-lived connection stays open and the client no longer needs to poll.
- **Installing and configuring WebSocket**: use `github.com/gorilla/websocket`.

##### 13.3.2 Implementing WebSocket in Gin

- **Create a WebSocket handler**:
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

##### 13.3.3 Common Issues and Debugging

- **Connection problems**: when `upgrader.Upgrade` returns an err, check whether the request headers meet the upgrade conditions and whether `CheckOrigin` lets the origin through.
- **Performance optimization**: `ReadMessage` in the example blocks, so when there are many connections keep an eye on the number of server goroutines.

#### 13.4 Deployment and Operations for Gin

##### 13.4.1 Deployment Strategies

- **Containerized deployment**: build an image with Docker and run the Gin application.
- **Cloud deployment**: deploy to cloud platforms such as AWS, GCP, and Azure.

##### 13.4.2 Monitoring and Logging

- **Application monitoring**: use Prometheus and Grafana to watch a Gin application's performance and health.
- **Log management**: configure and manage the logging of a Gin application.

##### 13.4.3 Performance Optimization

- **Performance tuning**: first use a profiling tool to find the hot spots, then optimize those specifically.
- **Caching and load balancing**: put hot data into a cache and spread traffic with load balancing; response speed and availability both improve.

##### 13.4.4 Common Operations Issues

- **Troubleshooting**: use logs and monitoring metrics to diagnose common problems in a Gin application.
- **Upgrades and maintenance**: upgrading and maintaining the application keeps the system stable and secure.

## References

- [Gin Official Documentation](https://gin-gonic.com/en/docs/)
- [Gin · pkg.go.dev](https://pkg.go.dev/github.com/gin-gonic/gin)


## Sibling pages

- [Config](/gin/Config.md)
- [Debug](/gin/Debug.md)
- [Error](/gin/Error.md)
- [Use](/gin/Use.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Use](/gin/Use.md)
