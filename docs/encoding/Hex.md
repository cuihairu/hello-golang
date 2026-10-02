# Hex 编码

Hex（十六进制）编码把二进制数据表示为十六进制字符串。每个字节用两个十六进制字符（`0-9`、`a-f`）表示，所以编码后的长度是原始数据的两倍。Hex 编码主要用于调试、数据展示和协议中的二进制表示，例如打印内存内容、展示哈希值和摘要。

Go 标准库 `encoding/hex` 提供了 Hex 编码和解码的实现。

## 基本用法

`hex.EncodeToString` 把字节切片编码为十六进制字符串，`hex.DecodeString` 完成逆过程：

```go
package main

import (
	"encoding/hex"
	"fmt"
)

func main() {
	data := []byte("Hello, Go!")

	// 编码为十六进制字符串
	encoded := hex.EncodeToString(data)
	fmt.Println("编码结果:", encoded)

	// 解码回原始数据
	decoded, err := hex.DecodeString(encoded)
	if err != nil {
		fmt.Println("解码失败:", err)
		return
	}
	fmt.Println("解码结果:", string(decoded))
}
```

输出：

```
编码结果: 48656c6c6f2c20476f21
解码结果: Hello, Go!
```

注意编码结果默认使用小写字母。如果需要大写形式，可以对结果调用 `strings.ToUpper`，或直接逐字节用 `fmt.Sprintf("%02X", b)` 拼接。

## 流式编解码

对于较大的数据，可以使用实现了 `io.Reader` / `io.Writer` 的流式接口：

```go
package main

import (
	"bytes"
	"encoding/hex"
	"fmt"
	"io"
	"strings"
)

func main() {
	// 流式编码：写入 encoder 的字节会以十六进制形式写入 buf
	var buf bytes.Buffer
	enc := hex.NewEncoder(&buf)
	if _, err := enc.Write([]byte("stream data")); err != nil {
		fmt.Println("编码失败:", err)
		return
	}
	fmt.Println("流式编码:", buf.String())

	// 流式解码：从十六进制文本中还原出原始字节
	dec := hex.NewDecoder(strings.NewReader(buf.String()))
	out, err := io.ReadAll(dec)
	if err != nil {
		fmt.Println("解码失败:", err)
		return
	}
	fmt.Println("流式解码:", string(out))
}
```

`hex.NewEncoder(w io.Writer) io.Writer` 会把写入其中的字节以十六进制形式写到 `w`；`hex.NewDecoder(r io.Reader) io.Reader` 则把读到的十六进制文本还原为字节。

## 解码的错误处理

`hex.DecodeString` 要求输入长度为偶数且只包含合法的十六进制字符，否则返回 `hex.InvalidByteError` 或长度错误：

```go
package main

import (
	"encoding/hex"
	"fmt"
)

func main() {
	if _, err := hex.DecodeString("abc"); err != nil {
		fmt.Println("长度错误:", err) // 编码后的长度必须是偶数
	}
	if _, err := hex.DecodeString("zz"); err != nil {
		fmt.Printf("非法字符: %v\n", err)
	}
}
```

## 与 Base64 的对比

- Hex 每个字节固定展开为 2 个字符，数据膨胀 100%；Base64 平均膨胀约 33%，更节省空间。
- Hex 字符集简单、可读性更好，常用于日志、调试和哈希值展示；Base64 更适合在文本协议中携带较大的二进制数据。
- 两者都只是编码而非加密，不能用于保护数据机密性。

## 总结

Hex 是最简单直接的二进制文本表示方式，`encoding/hex` 提供的 `EncodeToString` / `DecodeString` 和流式的 `NewEncoder` / `NewDecoder` 覆盖了绝大多数场景。需要展示或调试二进制内容时优先使用 Hex；需要在文本协议中传输大块二进制数据时，可以改用 Base64 以减小体积。
