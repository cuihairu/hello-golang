# 包管理器
Go 用 `go mod` 管理依赖关系，`go.mod` 文件记录模块路径和依赖版本。下面按用途分组介绍常用命令：

### `go mod` 的基础概念

1. **模块（Module）**：模块是由 Go 源文件组成的目录树，其根目录包含一个 `go.mod` 文件。一个模块包含一个或多个包。
2. **包（Package）**：包是 Go 源文件的集合，它们都在同一个目录下，并且声明属于同一个包。
3. **依赖关系（Dependency）**：指项目所依赖的其他模块。

### `go mod` 命令详解

#### 初始化和创建模块

- `go mod init <module-path>`：初始化一个新的模块，并创建一个 `go.mod` 文件。`<module-path>` 是模块的路径，通常是项目的仓库地址。

```sh
go mod init github.com/user/project
```

#### 管理依赖

- `go get <package>`：添加或更新一个依赖包。可以指定特定版本，如 `@v1.2.3`。

```sh
go get github.com/sirupsen/logrus@v1.8.1
```

- `go mod tidy`：清理模块依赖。移除 `go.mod` 文件中未使用的依赖，并下载缺失的依赖。

```sh
go mod tidy
```

- `go mod vendor`：将依赖包复制到 `vendor` 目录。可以使用 `go build` 和 `go test` 时从 `vendor` 目录中读取依赖。

```sh
go mod vendor
```

#### 查看依赖

- `go list -m all`：列出所有的模块依赖。

```sh
go list -m all
```

- `go mod graph`：打印模块依赖图。

```sh
go mod graph
```

- `go mod why <package>`：解释为什么需要某个依赖包。

```sh
go mod why github.com/sirupsen/logrus
```

#### 版本管理

- `go mod edit`：手动编辑 `go.mod` 文件的工具，可以修改模块路径、版本等。

```sh
go mod edit -require=github.com/sirupsen/logrus@v1.8.1
```

#### 升级和降级依赖

- `go get -u`：升级所有依赖包到最新版本。

```sh
go get -u
```

- `go get <package>@latest`：升级指定包到最新版本。

```sh
go get github.com/sirupsen/logrus@latest
```

- `go get <package>@<version>`：将指定包降级或升级到特定版本。

```sh
go get github.com/sirupsen/logrus@v1.7.0
```

### 总结

`go mod` 是 Go 的依赖管理入口：`go mod init` 创建模块，`go get` 增删依赖，`go mod tidy` 清理未用到的条目，`go mod vendor` 把依赖复制进 `vendor` 目录。这几条命令配合 `go.mod` 记录的版本，让同一份代码在不同机器上构建时拉到同一套依赖。