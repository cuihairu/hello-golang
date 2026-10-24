`GOPROXY` is the environment variable Go uses to configure a module proxy; a module proxy caches and forwards Go module downloads. Connecting directly to the official `proxy.golang.org` from mainland China is often slow, so switching to a domestic proxy can noticeably speed up downloads and builds.

### Commonly used Go module proxies in mainland China

1. **GOPROXY.cn**
   - Address: `https://goproxy.cn`
   - A free Go module proxy provided by Qiniu Cloud.

2. **goproxy.io**
   - Address: `https://goproxy.io`
   - A Go module proxy mainly aimed at global users; it also works from mainland China.

3. **Aliyun Go mirror**
   - Address: `https://mirrors.aliyun.com/goproxy/`
   - A Go module proxy provided by Alibaba Cloud, suitable for use in mainland China.

### Configuring GOPROXY

You can configure the `GOPROXY` environment variable in a terminal with the following steps:

```sh
export GOPROXY=https://goproxy.cn
```

Or add it to your `~/.bashrc` or `~/.zshrc` file so it takes effect every time you open a terminal:

```sh
echo "export GOPROXY=https://goproxy.cn" >> ~/.bashrc
source ~/.bashrc
```

For `zsh` users:

```sh
echo "export GOPROXY=https://goproxy.cn" >> ~/.zshrc
source ~/.zshrc
```

### Setting multiple proxies

`GOPROXY` supports configuring multiple proxy servers, separated by commas. If the first proxy is unavailable, the Go toolchain automatically tries the next one. For example:

```sh
export GOPROXY=https://goproxy.cn,https://proxy.golang.org,direct
```

Try `goproxy.cn` first, then `proxy.golang.org` if that fails, and finally fall back to connecting to the source repository directly.

### Verifying the configuration

Use this command to see the currently active configuration:

```sh
go env GOPROXY
```

The output is the current value of `GOPROXY`.

### Summary

The three proxies commonly used in mainland China are `goproxy.cn`, `goproxy.io`, and the Aliyun mirror; configuring several lets you fall back in order.

### Setting up a LAN proxy

Setting up a Go module proxy inside your LAN lets every team member's module downloads go through it, which also works when the external network is restricted or too slow. Here are two implementations:

### A proxy service using goproxy

[goproxy](https://github.com/goproxy/goproxy) provides an open source Go module proxy server that you can run inside your LAN.

#### 1. Install goproxy

First install Go on the server, then run:

```sh
go install github.com/goproxy/goproxy/cmd/goproxy@latest
```

#### 2. Start goproxy

Once installed, you can start `goproxy` with the following command:

```sh
goproxy server --address 0.0.0.0:8080
```

This listens on port `8080` on all network interfaces; you can change the port number as needed.

#### 3. Configure the cache directory (optional)

You can configure a cache directory to store downloaded modules, avoiding repeated downloads. The startup command looks like this:

```sh
goproxy server --address 0.0.0.0:8080 --cacher dir --cacher-dir /path/to/cache
```

#### 4. Set the environment variable

On each client machine, set the `GOPROXY` environment variable to point at your proxy server. For example, if your server IP is `192.168.1.100`:

```sh
export GOPROXY=http://192.168.1.100:8080
```

Or add it to the `~/.bashrc` or `~/.zshrc` file:

```sh
echo "export GOPROXY=http://192.168.1.100:8080" >> ~/.bashrc
source ~/.bashrc
```

### Setting up GOPROXY with Athens

[Athens](https://github.com/gomods/athens) is another open source Go module proxy project, configured with environment variables and with pluggable storage (the example below uses disk).

#### 1. Install Athens

First, make sure Docker is installed on your system. Then you can use Docker to run Athens:

```sh
docker run -d \
  --name athens \
  -p 3000:3000 \
  -v /path/to/storage:/var/lib/athens \
  gomods/athens:latest
```

This runs Athens on port `3000`; you can change the port number and storage path as needed.

#### 2. Configure Athens

You can configure Athens through environment variables. For example, create a `.env` file:

```sh
ATHENS_STORAGE_TYPE=disk
ATHENS_DISK_STORAGE_ROOT=/var/lib/athens
```

Then load that file when starting the container:

```sh
docker run -d \
  --name athens \
  --env-file .env \
  -p 3000:3000 \
  -v /path/to/storage:/var/lib/athens \
  gomods/athens:latest
```

#### 3. Set the environment variable

On each client machine, set the `GOPROXY` environment variable to point at your Athens server. For example, if your server IP is `192.168.1.100`:

```sh
export GOPROXY=http://192.168.1.100:3000
```

Or add it to the `~/.bashrc` or `~/.zshrc` file:

```sh
echo "export GOPROXY=http://192.168.1.100:3000" >> ~/.bashrc
source ~/.bashrc
```

### Summary

Both routes work: use `goproxy server` to start the service with a single command if you want it simple, or use Athens if you want more configuration options; on the client side, just point `GOPROXY` at that machine.

## References

- [Official · Installing and managing the Go toolchain](https://go.dev/doc/manage-install)
- [Go Official Documentation · Getting started (external link)](https://go.dev/doc/tutorial/getting-started)
- [Official · Go Modules usage guide](https://go.dev/doc/modules/)
- [Go Modules Reference · GOPROXY](https://go.dev/ref/mod)

## Sibling pages

- [Env](/env/Env.md)
- [Install](/env/Install.md)
- [Goland](/env/Goland.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Goland](/env/Goland.md)
- [Modules](/env/Modules.md)
- [Tools](/env/Tools.md)
- [Vim](/env/Vim.md)
- [ide](/env/ide.md)
- [vscode](/env/vscode.md)
