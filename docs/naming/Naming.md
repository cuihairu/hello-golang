# 命名

命名是影响代码可读性的第一要素。Go 社区在命名上有一套约定俗成的规则，其中一部分由编译器和工具链强制执行，另一部分则是官方文档（如 [Effective Go](https://go.dev/doc/effective_go#names) 和 [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)）中推荐的风格。本章汇总 Go 命名的核心规则与常见惯例。

### 命名的基本规则

1. **组成**：标识符由字母、数字、下划线组成，且不能以数字开头。Go 的标识符理论上是 Unicode 敏感的，但惯例上只使用 ASCII 字母。
2. **大小写决定可见性**：这是 Go 与其他语言最大的不同——**标识符首字母大写即导出（public），小写即未导出（包内私有）**。没有 `public`、`private` 等关键字。
3. **不能与关键字冲突**：`break`、`func`、`interface` 等 25 个关键字不能作为标识符，部分预声明标识符（如 `int`、`len`、`nil`）虽可覆盖但不建议。

```go
package user

type Profile struct {  // 导出类型，其他包可用
    Name    string     // 导出字段
    email   string     // 未导出字段，仅包内可见
}

func NewProfile() *Profile { ... }  // 导出构造函数
func validate() bool       { ... }  // 未导出函数
```

### 命名风格惯例

#### 包名

- 全小写、单个单词、不用下划线或驼峰：`strconv`、`httputil`，而不是 `str_conv`、`httpUtil`。
- 使用名词的复数形式表示集合包：`bytes`、`errors`。
- 避免与标准库包重名（如不要给自己的工具包命名为 `sync`、`time`）。
- 包名应该描述包"提供什么"，而不是"包含什么"：`net/http` 而不是 `util`、`common`。

#### 变量与函数

- 使用驼峰命名（camelCase），不用下划线：`parseRequest`、`maxRetryCount`。
- 名字越长作用域越大：短作用域的局部变量可以用 `i`、`n`、`buf` 这类短名字；包级别的导出标识符则应完整描述用途。
- 避免无意义的名字：`data`、`info`、`temp`、`foo`。
- 函数名用动词或动宾短语：`Read`、`ParseIP`、`NewServer`。

```go
// 不推荐
func GetDataFromDBAndConvertIt() []byte { ... }

// 推荐
func LoadConfig() []byte { ... }
```

#### 接口

- 单方法接口通常命名为"方法名 + er"：`Reader`、`Writer`、`Formatter`、`Clock`。
- 多方法接口可以用描述其角色的名词：`Conn`、`Handler`。
- 标准库的典范：`io.Reader`、`io.Writer`、`fmt.Stringer`（方法 `String()`）。

```go
type Stringer interface {
    String() string
}

type Speaker interface {
    Speak() string
}
```

#### 结构体方法：避免 Get 前缀

Go 惯例中**访问器不用 `Get` 前缀**：`obj.Name()` 而不是 `obj.GetName()`；对应的设置器则使用 `SetXxx`：

```go
type Counter struct {
    mu    sync.Mutex
    count int
}

func (c *Counter) Count() int { // 读：直接用字段名
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.count
}

func (c *Counter) SetCount(n int) { // 写：用 Set 前缀
    c.mu.Lock()
    c.count = n
    c.mu.Unlock()
}
```

#### 错误类型与错误变量

- 错误类型以 `Error` 结尾：`type ParseError struct { ... }`。
- 哨兵错误变量以 `Err` 开头：`var ErrNotFound = errors.New("not found")`。

```go
var ErrTimeout = errors.New("operation timed out")

type ParseError struct {
    Input string
}

func (e *ParseError) Error() string {
    return fmt.Sprintf("cannot parse %q", e.Input)
}
```

#### 缩写词

缩写词保持统一大小写，遵循惯例：`URL` → `ServeHTTP` 中的 `URL`、`id`（或 `ID`，选定一种全项目统一）、`HTTP`、`IP`。标准库的风格是大写缩写词在导出位置整体大写（`ReadFile` 的 `File`、`MarshalJSON` 的 `JSON`）。

```go
// 推荐
type HTTPClient struct { ... }
func (c *HTTPClient) FetchURL(u string) error { ... }

// 不推荐
type HttpClient struct { ... }
func (c *HttpClient) FetchUrl(u string) error { ... }
```

### 常见反模式

| 反模式 | 问题 | 建议 |
| ------ | ---- | ---- |
| `GetUser()` 读取字段 | 不符合 Go 惯例 | `User()` |
| `userListArr` | 冗余后缀 | `users` |
| `DoProcess()` | 无信息量动词 | 按实际动作命名，如 `Parse`、`Sync` |
| 包名 `utils`、`common`、`misc` | 什么都装，职责不清 | 按功能拆分成具体名字的包 |
| `myProject/internal2` | 数字后缀无意义 | 按模块命名 |
| 接口名 `IUser` | 匈牙利前缀，非 Go 风格 | `User` 或按方法命名 `UserReader` |

### 工具辅助

- **gofmt / gofmt -s**：统一代码格式，消除格式争论。
- **go vet**：检查可疑的命名相关错误，如结构体标签格式（`structtag`）。
- **staticcheck / revive / golangci-lint**：可配置的命名风格检查（如导出标识符缺少注释、包名不符合规范等）。

```sh
go vet ./...
golangci-lint run
```

### 总结

Go 命名的核心原则是：**简短、准确、一致**。可见性由大小写决定，包名短小且不驼峰，变量随作用域调整长度，接口以 "er" 结尾，错误用 `Err` 前缀的哨兵变量。遵守这些惯例，代码就能自然融入 Go 生态，让协作者"一眼看懂"。
