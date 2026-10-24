# Configuration Management

#### 10.1 Overview of Configuration Options

The Gin framework does not ship with configuration management; you need to pair it with another library or write the code yourself. Configuration options, file formats, and loading methods are covered below.

##### 10.1.1 Common Configuration Options

Common configuration options are:
- Server port
- Log level
- Database connection information
- Cache configuration
- Third-party service interface information

##### 10.1.2 Configuration File Formats

Commonly used configuration file formats are:
- JSON
- YAML
- TOML
- INI

Which one to pick depends on project requirements and team conventions.

#### 10.2 Parsing Configuration Files

Gin is usually used together with other libraries such as Viper or Go's encoding/json to parse configuration files.

##### 10.2.1 Parsing Configuration with Viper

Viper supports configuration files in multiple formats, and can also watch for configuration changes to achieve dynamic configuration management.

```go
import (
    "github.com/spf13/viper"
)

type Config struct {
    Server struct {
        Port string
    }
    Database struct {
        Host     string
        Port     int
        Username string
        Password string
        Name     string
    }
}

func LoadConfig() (*Config, error) {
    viper.SetConfigName("config")
    viper.SetConfigType("yaml")
    viper.AddConfigPath(".")

    if err := viper.ReadInConfig(); err != nil {
        return nil, err
    }

    var config Config
    if err := viper.Unmarshal(&config); err != nil {
        return nil, err
    }

    return &config, nil
}
```

##### 10.2.2 Loading Configuration Files

Load the configuration file during application initialization:

```go
func main() {
    config, err := LoadConfig()
    if err != nil {
        log.Fatalf("Could not load config: %v", err)
    }

    r := gin.Default()
    r.Run(config.Server.Port)
}
```

#### 10.3 Dynamic Configuration Management

In some scenarios, an application needs to load or modify configuration dynamically; this can be done through file change watching or a configuration center.

##### 10.3.1 File Change Watching

Using Viper's file change watching feature, configuration can be reloaded automatically when a configuration file is modified:

```go
import (
    "log"

    "github.com/fsnotify/fsnotify"
    "github.com/spf13/viper"
)

func WatchConfig(config *Config) {
    viper.WatchConfig()
    viper.OnConfigChange(func(e fsnotify.Event) {
        log.Printf("Config file changed: %s", e.Name)
        if err := viper.Unmarshal(config); err != nil {
            log.Printf("Error reloading config: %v", err)
        }
    })
}

func main() {
    config, err := LoadConfig()
    if err != nil {
        log.Fatalf("Could not load config: %v", err)
    }

    WatchConfig(config)

    r := gin.Default()
    r.Run(config.Server.Port)
}
```

##### 10.3.2 Configuration Center

For large distributed systems, you can use a configuration center (such as Consul, Etcd, or Spring Cloud Config) to centrally manage configuration and achieve dynamic configuration updates.

```go
import (
    "context"
    "encoding/json"
    "time"

    "go.etcd.io/etcd/client/v3"
)

func LoadConfigFromEtcd() (*Config, error) {
    cli, err := clientv3.New(clientv3.Config{
        Endpoints: []string{"localhost:2379"},
        DialTimeout: 5 * time.Second,
    })
    if err != nil {
        return nil, err
    }
    defer cli.Close()

    ctx, cancel := context.WithTimeout(context.Background(), 5 * time.Second)
    resp, err := cli.Get(ctx, "/config/app")
    cancel()
    if err != nil {
        return nil, err
    }

    var config Config
    if err := json.Unmarshal(resp.Kvs[0].Value, &config); err != nil {
        return nil, err
    }

    return &config, nil
}
```

### Summary

Configuration options are centrally defined in a struct, and `LoadConfig` reads them in at startup; for hot reloading hook up `viper.WatchConfig`, and for multi-instance deployments move configuration into a configuration center like etcd.

## References

- [Gin Official Documentation](https://gin-gonic.com/en/docs/)
- [Gin · pkg.go.dev](https://pkg.go.dev/github.com/gin-gonic/gin)

## Sibling pages

- [Debug](/gin/Debug.md)
- [Error](/gin/Error.md)
- [Extend](/gin/Extend.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Debug](/gin/Debug.md)
- [Error](/gin/Error.md)
- [Extend](/gin/Extend.md)
- [Gin](/gin/Gin.md)
- [Middleware](/gin/Middleware.md)
- [Optimize](/gin/Optimize.md)
- [Request](/gin/Request.md)
- [Response](/gin/Response.md)
- [Route](/gin/Route.md)
- [Source](/gin/Source.md)
- [Use](/gin/Use.md)
- [advanced](/gin/advanced.md)
