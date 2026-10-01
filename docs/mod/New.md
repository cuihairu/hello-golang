发布自己的 Go 包，并将其公开在 GitHub 上，遵循版本规范，一般需要以下步骤：

### 1. 创建 GitHub 仓库

1. 登录 GitHub，点击右上角的 “+” 号，选择 “New repository”。
2. 填写仓库名称和描述，选择公开 (public) 仓库，点击 “Create repository”。

### 2. 初始化本地项目

1. 在本地创建一个新的 Go 项目目录：
   ```sh
   mkdir mypackage
   cd mypackage
   ```

2. 初始化 Go 模块：
   ```sh
   go mod init github.com/yourusername/mypackage
   ```

3. 创建 Go 源码文件，例如 `mypackage.go`：
   ```go
   // mypackage.go
   package mypackage

   import "fmt"

   // Hello prints a greeting message
   func Hello() {
       fmt.Println("Hello, world!")
   }
   ```

4. 创建 README 文件（可选，但推荐）：
   ```markdown
   # mypackage

   This is mypackage, a simple Go package for demonstration.

   ## Installation

   ```sh
   go get github.com/yourusername/mypackage
   ```

   ## Usage

   ```go
   package main

   import "github.com/yourusername/mypackage"

   func main() {
       mypackage.Hello()
   }
   ```
   ```

### 3. 提交代码到 GitHub

1. 初始化 Git 仓库：
   ```sh
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. 将本地仓库连接到 GitHub：
   ```sh
   git remote add origin https://github.com/yourusername/mypackage.git
   git push -u origin master
   ```

### 4. 版本管理

Go 包的版本管理遵循语义化版本 (Semantic Versioning, SemVer) 规范。版本号格式为 `vMAJOR.MINOR.PATCH`，例如 `v1.0.0`。

- **MAJOR** 版本：包含不兼容的 API 变更。
- **MINOR** 版本：添加功能，且与之前版本兼容。
- **PATCH** 版本：进行向下兼容的问题修正。

### 5. 创建版本标签

1. 在本地创建并推送标签，例如：
   ```sh
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. 在 GitHub 仓库的 “Releases” 页面，点击 “Draft a new release”，选择你刚创建的标签，填写发布说明，点击 “Publish release”。

### 6. 确保模块路径和版本兼容

1. 确保模块路径正确匹配：
   ```sh
   go mod tidy
   ```

2. 检查 `go.mod` 文件中的模块路径是否与 GitHub 仓库匹配。例如，`module github.com/yourusername/mypackage`。

### 示例

假设你发布的包在 `github.com/yourusername/mypackage` 下，并且创建了 `v1.0.0` 标签，用户可以通过以下命令安装并使用你的包：
```sh
go get github.com/yourusername/mypackage@v1.0.0
```

### 7. 更新包

当你对包进行更新时，修改代码并提交：
```sh
git commit -am "Add new feature"
```
创建新的版本标签并推送：
```sh
git tag v1.1.0
git push origin v1.1.0
```
发布新的版本到 GitHub Releases。

通过这些步骤，你可以轻松地在 GitHub 上发布并管理你的 Go 包，同时确保符合语义化版本规范。