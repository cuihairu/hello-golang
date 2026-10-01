
## 安装 Go 语言

### 1. 从官网下载并安装 Go 语言

#### Windows
1. 打开 [Go 语言下载页面](https://golang.org/dl/)。
2. 选择适用于 Windows 的安装包并下载（例如：`go1.22.5.windows-amd64.msi`）。
3. 双击下载的 MSI 文件，按照安装向导完成安装。

#### Linux
1. 打开 [Go 语言下载页面](https://golang.org/dl/)。
2. 选择适用于 Linux 的安装包并下载（例如：`go1.22.5.linux-amd64.tar.gz`）。
3. 打开终端，运行以下命令解压并安装 Go：
   ```sh
   tar -C /usr/local -xzf go1.22.5.linux-amd64.tar.gz
   ```

#### macOS
1. 打开 [Go 语言下载页面](https://golang.org/dl/)。
2. 选择适用于 macOS 的安装包并下载（例如：`go1.22.5.darwin-amd64.pkg`）。
3. 双击下载的 PKG 文件，按照安装向导完成安装。

### 2. 设置环境变量

#### Windows
1. 打开“控制面板” -> “系统和安全” -> “系统” -> “高级系统设置”。
2. 在“系统属性”窗口中，点击“环境变量”。
3. 在“系统变量”部分，找到并选择“Path”变量，点击“编辑”。
4. 点击“新建”，添加 Go 的安装路径（默认路径是 `C:\Go\bin`），点击“确定”保存。

#### Linux
1. 打开终端，编辑你的 shell 配置文件（例如：`~/.bashrc` 或 `~/.profile` 或 `~/.zshrc`），添加以下行：
   ```sh
   export PATH=$PATH:/usr/local/go/bin
   ```
2. 保存文件并运行以下命令使更改生效：
   ```sh
   source ~/.bashrc  # 或者 source ~/.profile 或 source ~/.zshrc
   ```

#### macOS
1. 打开终端，编辑你的 shell 配置文件（例如：`~/.bash_profile` 或 `~/.zshrc`），添加以下行：
   ```sh
   export PATH=$PATH:/usr/local/go/bin
   ```
2. 保存文件并运行以下命令使更改生效：
   ```sh
   source ~/.bash_profile  # 或者 source ~/.zshrc
   ```

### 3. 验证安装
打开终端或命令提示符，运行以下命令验证 Go 安装是否成功：
```sh
go version
```

### 使用包管理工具安装 Go 语言

#### macOS 使用 Homebrew 安装
1. 打开终端，运行以下命令安装 Go：
   ```sh
   brew install go
   ```
2. 安装完成后，Homebrew 会自动将 Go 的路径添加到你的 PATH 变量中，可以直接验证安装：
   ```sh
   go version
   ```

#### Windows 使用 Scoop 安装
1. 打开 PowerShell 并运行以下命令安装 Scoop：
   ```sh
   iwr -useb get.scoop.sh | iex
   ```
2. 使用 Scoop 安装 Go：
   ```sh
   scoop install go
   ```
3. 验证安装：
   ```sh
   go version
   ```

通过以上步骤，您可以在 Windows、Linux 和 macOS 上成功安装 Go 语言并设置环境变量，使其在系统中可用。