# 入门
在Go环境搭建好之后，你可以通过以下步骤来创建一个Go项目。假设你已经安装并配置好了Go以及相关的工具。

### 1. 设置GOPATH和项目目录

首先，确保你已经设置好了`GOPATH`环境变量，这是Go工作空间的根目录。你可以在你的shell配置文件（如`.bashrc`或`.zshrc`）中添加以下行来设置`GOPATH`：

```sh
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
```

然后，创建项目目录。假设你要创建一个名为`myproject`的项目：

```sh
mkdir -p $GOPATH/src/github.com/yourusername/myproject
cd $GOPATH/src/github.com/yourusername/myproject
```

### 2. 初始化Go模块

Go模块是Go 1.11引入的一种依赖管理方式。通过模块，你可以轻松管理项目的依赖关系。在项目目录下运行以下命令来初始化一个新的Go模块：

```sh
go mod init github.com/yourusername/myproject
```

这将创建一个`go.mod`文件，记录项目的模块路径和依赖项。

### 3. 创建项目结构

一个典型的Go项目结构可能如下：

```
myproject/
├── go.mod
├── go.sum
├── cmd/
│   └── myproject/
│       └── main.go
├── pkg/
│   └── ...
└── internal/
    └── ...
```

- `cmd/`：存放项目的主应用程序入口。
- `pkg/`：存放可以被其他项目使用的库代码。
- `internal/`：存放只能被本项目使用的包。

创建这些目录和文件：

```sh
mkdir -p cmd/myproject
touch cmd/myproject/main.go
mkdir -p pkg
mkdir -p internal
```

### 4. 编写代码

在`cmd/myproject/main.go`中编写你的Go代码，例如一个简单的"Hello, World!"程序：

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

### 5. 构建和运行项目

你可以使用以下命令来构建和运行你的项目：

```sh
go build -o bin/myproject ./cmd/myproject
./bin/myproject
```

或者直接运行：

```sh
go run ./cmd/myproject
```

### 6. 添加依赖

如果你的项目需要使用外部包，可以使用`go get`命令。例如，要使用`gin`框架，你可以运行：

```sh
go get -u github.com/gin-gonic/gin
```

这将自动更新你的`go.mod`和`go.sum`文件以包含新的依赖项。

### 7. 管理依赖

当你添加或更新依赖时，`go mod tidy`命令可以帮助你清理和整理`go.mod`和`go.sum`文件：

```sh
go mod tidy
```

### 完整示例

```sh
# 设置项目目录
mkdir -p $GOPATH/src/github.com/yourusername/myproject
cd $GOPATH/src/github.com/yourusername/myproject

# 初始化Go模块
go mod init github.com/yourusername/myproject

# 创建项目结构
mkdir -p cmd/myproject
touch cmd/myproject/main.go
mkdir -p pkg
mkdir -p internal

# 编写代码
echo 'package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}' > cmd/myproject/main.go

# 构建和运行项目
go build -o bin/myproject ./cmd/myproject
./bin/myproject

# 或者直接运行
go run ./cmd/myproject

# 添加依赖
go get -u github.com/gin-gonic/gin

# 管理依赖
go mod tidy
```

通过以上步骤，你应该能够创建并运行一个基本的Go项目。你可以根据自己的需要进一步扩展和完善项目。