### plugin 插件

`plugin` 包让程序在运行时加载编译好的共享库（`.so`），按名字取符号、断言成函数或变量后调用。它是 Go 里"插件系统"的标准形态，动态补丁（热更新逻辑）走的就是这条路。

### 基本用法

插件侧是一个普通包，导出函数或变量：

```go
package main

// Greet 返回问候语，导出给插件使用者
func Greet(name string) string {
	return "Hello, " + name
}
```

用 `-buildmode=plugin` 编成共享库：

```sh
go build -buildmode=plugin -o greet.so greet.go
```

宿主侧用 `plugin.Open` 加载，`Lookup` 按名字取符号：

```go
package main

import (
	"fmt"
	"plugin"
)

func main() {
	p, err := plugin.Open("greet.so")
	if err != nil {
		panic(err)
	}
	sym, err := p.Lookup("Greet")
	if err != nil {
		panic(err)
	}
	greet := sym.(func(string) string)
	fmt.Println(greet("Go")) // 输出：Hello, Go
}
```

### 限制

- 平台受限：`-buildmode=plugin` 只在 Linux、macOS、FreeBSD 可用，Windows 不支持。
- 只进不出：插件一经 `Open` 不能卸载，卸载函数不存在。
- 同路径只加载一次：对同一路径重复 `Open` 返回的是同一个插件实例。
- 版本敏感：插件与宿主必须用一致的工具链和依赖编译，不匹配会在 `Open` 时报 `plugin was built with a different version` 之类的错。
- 类型靠断言：`Lookup` 返回 `Symbol`（`any`），签名对不对要自己断言，错了运行时 panic。

### 动态补丁的现实

用 plugin 做热更新，流程是"改代码 → 重编 `.so` → 换路径 `Open`"。因为不能卸载，旧版本的代码和数据会一直留在内存里，长期热更的进程要按"每版一个文件名"管理，避免重复加载同一文件。多数场景更稳的路子是把变化的部分放进子进程或用数据驱动（配置、规则引擎），plugin 留给真正的原生扩展点。

交叉阅读：加载外部代码的安全边界见 [官方安全口径](../security/Security.md)。
