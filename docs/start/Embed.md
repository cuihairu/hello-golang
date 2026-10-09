### embed 包嵌入

`embed`（Go 1.16+）把静态资源打进二进制：模板、配置、前端产物随程序一起发布，部署时不再拖一堆文件。写法是包级变量上加 `//go:embed` 注释，变量类型决定嵌入形态——`string`/`[]byte` 嵌单个文件，`embed.FS` 嵌文件树。

### 基本用法

```go
package main

import (
	"embed"
	"fmt"
)

//go:embed hello.txt
var hello string

//go:embed hello.txt
var helloBytes []byte

//go:embed static
var static embed.FS

func main() {
	fmt.Print(hello)                    // 输出：hello embed
	fmt.Println("bytes:", len(helloBytes)) // 输出：bytes: 12
	data, err := static.ReadFile("static/config.json")
	fmt.Println(string(data), err)      // 输出：{"mode":"test"} <nil>
}
```

同一个文件可以嵌进多个变量；`embed.FS` 的路径从模块里被嵌入的位置算起，带目录前缀。`ReadDir` 可以列目录，遍历用 `fs.WalkDir`。

### 提供静态文件服务

`embed.FS` 实现了 `fs.FS` 接口，用 `http.FS` 包一层就能直接挂到文件服务器上（片段，`static` 为上面定义的变量）：

```go
mux := http.NewServeMux()
mux.Handle("/", http.FileServer(http.FS(static)))
http.ListenAndServe(":8080", mux)
```

### 限制与注意

- 模式只能匹配包所在目录及子目录，写 `..` 直接编译错：`pattern ../outside.txt: invalid pattern syntax`。
- 模式里的路径用正斜杠，Windows 也不例外。
- 变量必须声明在包级，函数内的局部变量不能用；未使用的嵌入变量要写 `_` 接收。
- `go:generate`、条件编译都能和嵌入配合：给平台差异的资源加构建约束，见 [构建约束](BuildConstraint.md)。

### 小结

嵌入的口诀：注释声明模式、变量决定类型、`embed.FS` 承接文件树。资源进二进制后，发布物就只有一个可执行文件，换来的是改资源要重新编译。
