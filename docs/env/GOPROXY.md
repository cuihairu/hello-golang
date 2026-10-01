`GOPROXY` 是 Go 语言中用于配置模块代理的环境变量。模块代理可以缓存和加速 Go 模块的下载，尤其对于中国大陆的用户，由于网络环境的限制，访问官方的 `proxy.golang.org` 可能会遇到较慢的下载速度。使用国内的 Go 模块代理可以显著提高下载和构建速度。

### 常用的国内 Go 模块代理

1. **GOPROXY.cn**
   - 地址: `https://goproxy.cn`
   - 这是由七牛云提供的免费的 Go 模块代理服务，速度快且稳定。

2. **goproxy.io**
   - 地址: `https://goproxy.io`
   - 这是一个由业界开发者提供的 Go 模块代理服务，主要面向全球用户，但在中国大陆也有不错的速度。

3. **Aliyun Go 镜像**
   - 地址: `https://mirrors.aliyun.com/goproxy/`
   - 这是由阿里云提供的 Go 模块代理服务，适合在中国大陆使用。

### 配置 GOPROXY

可以通过以下步骤在终端中配置 `GOPROXY` 环境变量：

```sh
export GOPROXY=https://goproxy.cn
```

或将其添加到你的 `~/.bashrc` 或 `~/.zshrc` 文件中，使其在每次打开终端时自动生效：

```sh
echo "export GOPROXY=https://goproxy.cn" >> ~/.bashrc
source ~/.bashrc
```

对于 `zsh` 用户：

```sh
echo "export GOPROXY=https://goproxy.cn" >> ~/.zshrc
source ~/.zshrc
```

### 设置多个代理

`GOPROXY` 支持配置多个代理服务器，以逗号分隔。如果第一个代理不可用，Go 工具链将自动尝试下一个。例如：

```sh
export GOPROXY=https://goproxy.cn,https://proxy.golang.org,direct
```

这将会首先尝试 `goproxy.cn`，如果失败，则尝试 `proxy.golang.org`，最后直接从源代码库获取模块。

### 验证配置

你可以通过以下命令来验证你的 `GOPROXY` 配置是否生效：

```sh
go env GOPROXY
```

这将输出当前配置的 `GOPROXY` 值。

### 总结

通过配置合适的 `GOPROXY`，特别是使用国内的 Go 模块代理，可以显著提高在中国大陆的 Go 模块下载和构建速度。`GOPROXY.cn`、`goproxy.io` 和 阿里云的 Go 镜像都是非常好的选择。

### 搭建局域网代理

搭建一个局域网内的 Go 模块代理（GOPROXY）可以帮助团队内的开发者更快地下载和使用 Go 模块，特别是在无法访问外部网络或外部网络速度较慢的情况下。以下是搭建局域网内的 GOPROXY 的步骤：

### 使用 goproxy.io 的代理服务

[goproxy.io](https://github.com/goproxyio/goproxy) 提供了一个开源的 Go 模块代理服务器，你可以在局域网内运行它。

#### 1. 安装 goproxy

首先，你需要在服务器上安装 `goproxy`。确保你的 Go 环境已经安装并配置好，然后运行以下命令：

```sh
go install github.com/goproxyio/goproxy/cmd/goproxy@latest
```

#### 2. 启动 goproxy

安装完成后，可以使用以下命令启动 `goproxy`：

```sh
goproxy -listen=0.0.0.0:8080
```

这会在所有网络接口上监听 `8080` 端口，你可以根据需要更改端口号。

#### 3. 配置缓存目录（可选）

你可以配置一个缓存目录来存储下载的模块，避免重复下载。启动命令如下：

```sh
goproxy -listen=0.0.0.0:8080 -cache=/path/to/cache
```

#### 4. 设置环境变量

在每个客户端机器上，设置 `GOPROXY` 环境变量指向你的代理服务器。例如，如果你的服务器 IP 是 `192.168.1.100`：

```sh
export GOPROXY=http://192.168.1.100:8080
```

或者将其添加到 `~/.bashrc` 或 `~/.zshrc` 文件中：

```sh
echo "export GOPROXY=http://192.168.1.100:8080" >> ~/.bashrc
source ~/.bashrc
```

### 使用 Athens 搭建 GOPROXY

[Athens](https://github.com/gomods/athens) 是另一个用于 Go 模块代理的开源项目，具有更多的功能和更强的可扩展性。

#### 1. 安装 Athens

首先，确保你的系统上已经安装了 Docker。然后，你可以使用 Docker 来运行 Athens：

```sh
docker run -d \
  --name athens \
  -p 3000:3000 \
  -v /path/to/storage:/var/lib/athens \
  gomods/athens:latest
```

这会在 `3000` 端口上运行 Athens，你可以根据需要更改端口号和存储路径。

#### 2. 配置 Athens

你可以通过环境变量来配置 Athens。例如，创建一个 `.env` 文件：

```sh
ATHENS_STORAGE_TYPE=disk
ATHENS_DISK_STORAGE_ROOT=/var/lib/athens
```

然后启动容器时加载这个文件：

```sh
docker run -d \
  --name athens \
  --env-file .env \
  -p 3000:3000 \
  -v /path/to/storage:/var/lib/athens \
  gomods/athens:latest
```

#### 3. 设置环境变量

在每个客户端机器上，设置 `GOPROXY` 环境变量指向你的 Athens 服务器。例如，如果你的服务器 IP 是 `192.168.1.100`：

```sh
export GOPROXY=http://192.168.1.100:3000
```

或者将其添加到 `~/.bashrc` 或 `~/.zshrc` 文件中：

```sh
echo "export GOPROXY=http://192.168.1.100:3000" >> ~/.bashrc
source ~/.bashrc
```

### 总结

通过使用 `goproxy.io` 或 `Athens`，你可以在局域网内轻松搭建一个 Go 模块代理。选择适合你的方案，按照上述步骤进行配置和部署，就能为团队提供快速稳定的 Go 模块下载服务。