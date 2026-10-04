# Go工具链
## Go 工具链简介

Go 工具链随安装包一起到位：编译 `go build`、运行 `go run`、测试 `go test`、检查 `go vet`、格式化 `go fmt`、性能分析 `go tool pprof`、调试 `dlv`，都在命令行里直接调。

### 1. `go` 命令

`go` 命令是工具链的入口，管理项目和依赖的子命令都挂在它名下：

- **构建与运行**

  - `go build`：编译包和依赖，但不安装结果。可以用于测试编译。

    ```sh
    go build
    ```

  - `go run`：编译并运行 Go 程序，适用于快速测试和开发阶段。

    ```sh
    go run main.go
    ```

- **测试**

  - `go test`：自动化测试工具，运行测试函数，并输出测试结果。

    ```sh
    go test ./...
    ```

- **安装**

  - `go install`：编译并安装包和依赖，将结果放在 `$GOPATH/bin` 目录下。

    ```sh
    go install
    ```

- **依赖管理**

  - `go mod`：管理模块和依赖关系，详细介绍见上一节。

    ```sh
    go mod init
    go mod tidy
    ```

- **格式化和文档**

  - `go fmt`：格式化代码，确保代码风格一致。

    ```sh
    go fmt ./...
    ```

  - `go doc`：显示包或符号的文档。

    ```sh
    go doc fmt.Println
    ```

### 2. `godoc` 工具

`godoc` 工具用于生成和浏览 Go 项目的文档。它可以启动一个本地的文档服务器，方便开发者查看代码的文档注释和 API 说明。

- 安装 `godoc`（它不随 Go 工具链一起分发）：

  ```sh
  go install golang.org/x/tools/cmd/godoc@latest
  ```

- 启动 `godoc` 服务器：

  ```sh
  godoc -http=:6060
  ```

  然后可以在浏览器中访问 `http://localhost:6060` 查看文档。

### 3. `go fmt` 工具

`go fmt` 是一个代码格式化工具，它根据官方的代码风格指南自动格式化 Go 代码，保持代码的一致性和可读性。

- 格式化当前包的所有 Go 文件：

  ```sh
  go fmt ./...
  ```

### 4. `go vet` 工具

`go vet` 是一个静态代码分析工具，用于发现代码中的潜在错误和问题。例如，它可以检测到未使用的变量、错误的格式化字符串等。

- 运行 `go vet`：

  ```sh
  go vet ./...
  ```

### 5. `golint` 工具

`golint` 是一个代码风格检查工具，它检查代码是否符合 Go 的编码规范和最佳实践。需要先通过 `go install` 安装：

- 安装 `golint`：

  ```sh
  go install golang.org/x/lint/golint@latest
  ```

- 运行 `golint`：

  ```sh
  golint ./...
  ```

### 6. `go tool pprof` 工具

`pprof` 是一个性能分析工具，用于分析 Go 程序的 CPU 和内存使用情况。通过 `go test` 或程序运行时生成的性能数据，`pprof` 可以帮助开发者优化程序性能。

- 启动 `pprof`：

  ```sh
  go tool pprof cpu.prof
  ```

### 7. `dlv` 工具

`dlv`（Delve）是 Go 的调试工具，支持设置断点、查看变量、单步执行等功能。需要先安装 `dlv`：

- 安装 `dlv`：

  ```sh
  go install github.com/go-delve/delve/cmd/dlv@latest
  ```

- 使用 `dlv` 调试：

  ```sh
  dlv debug main.go
  ```

### 8. `gofmt` 和 `goimports` 工具

`gofmt` 是一个格式化工具，而 `goimports` 不仅格式化代码，还会自动添加或移除 import 声明。

- 安装 `goimports`：

  ```sh
  go install golang.org/x/tools/cmd/goimports@latest
  ```

- 运行 `goimports`：

  ```sh
  goimports -w .
  ```

### 结论

一条命令对应一件事：`go build` 出二进制，`go test` 跑测试，`go vet` 做静态检查，`go tool pprof` 看 CPU 和内存，`dlv` 设断点单步。`go fmt` 和 `go vet` 适合挂在提交前的检查里。