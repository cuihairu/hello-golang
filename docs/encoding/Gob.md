# Gob 编码

Gob（Go binary）是 Go 语言特有的二进制序列化格式，由标准库 `encoding/gob` 提供。它可以把 Go 的数据结构编码为紧凑的二进制流，再在另一端解码回相同结构的值，常用于 Go 程序之间的 RPC 通信和数据持久化。与 JSON、XML 等文本格式相比，Gob 体积更小、编解码更快，并且原生支持结构体、切片、map、接口等 Go 类型，但只适用于 Go 语言环境。

## 基本用法

使用 `gob.NewEncoder` 编码、`gob.NewDecoder` 解码，两者都作用于 `io.Writer` / `io.Reader`：

```go
package main

import (
	"bytes"
	"encoding/gob"
	"fmt"
	"log"
)

type Address struct {
	City    string
	ZipCode string
}

type Person struct {
	Name    string
	Age     int
	Emails  []string
	Address Address
}

func main() {
	p := Person{
		Name:    "Alice",
		Age:     30,
		Emails:  []string{"alice@example.com", "a@work.com"},
		Address: Address{City: "Beijing", ZipCode: "100000"},
	}

	// 编码到内存缓冲区
	var buf bytes.Buffer
	if err := gob.NewEncoder(&buf).Encode(p); err != nil {
		log.Fatal("编码失败:", err)
	}
	fmt.Printf("编码后字节数: %d\n", buf.Len())

	// 解码回结构体
	var got Person
	if err := gob.NewDecoder(&buf).Decode(&got); err != nil {
		log.Fatal("解码失败:", err)
	}
	fmt.Printf("%+v\n", got)
}
```

## 序列化到文件

把结构体写入文件，再从文件恢复，就是最简单的持久化方式：

```go
package main

import (
	"encoding/gob"
	"fmt"
	"log"
	"os"
)

type Config struct {
	Theme    string
	FontSize int
	Tags     []string
}

func main() {
	cfg := Config{Theme: "dark", FontSize: 14, Tags: []string{"go", "dev"}}

	// 保存
	f, err := os.Create("config.gob")
	if err != nil {
		log.Fatal(err)
	}
	if err := gob.NewEncoder(f).Encode(cfg); err != nil {
		f.Close()
		log.Fatal(err)
	}
	f.Close()

	// 读取
	r, err := os.Open("config.gob")
	if err != nil {
		log.Fatal(err)
	}
	defer r.Close()

	var loaded Config
	if err := gob.NewDecoder(r).Decode(&loaded); err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%+v\n", loaded)
}
```

## 注册接口的具体类型

当被编码的字段是接口类型时，gob 传输的是具体的动态类型，编码前必须用 `gob.Register` 注册所有可能出现的具体类型，否则解码时会报 `gob: name not registered for interface`：

```go
package main

import (
	"bytes"
	"encoding/gob"
	"fmt"
	"log"
)

type Message interface{ Body() string }

type Text struct{ Content string }

func (t Text) Body() string { return t.Content }

type Image struct{ URL string }

func (i Image) Body() string { return "image: " + i.URL }

func main() {
	gob.Register(Text{})
	gob.Register(Image{})

	var buf bytes.Buffer
	enc := gob.NewEncoder(&buf)
	if err := enc.Encode(Text{Content: "hello"}); err != nil {
		log.Fatal(err)
	}
	if err := enc.Encode(Image{URL: "https://example.com/a.png"}); err != nil {
		log.Fatal(err)
	}

	dec := gob.NewDecoder(&buf)
	for i := 0; i < 2; i++ {
		var m Message
		if err := dec.Decode(&m); err != nil {
			log.Fatal(err)
		}
		fmt.Println(m.Body())
	}
}
```

## 使用注意事项

- **字段必须可导出**：gob 只编码导出字段（首字母大写），未导出字段会被忽略，解码后保持零值。
- **结构标签**：支持 `gob:"name"` 标签重命名字段，`gob:"-"` 表示跳过该字段。
- **零值省略**：gob 会省略值为零值的字段以减小体积，因此未导出或零值字段在解码端会自动恢复为零值，这要求编解码两端的类型结构兼容。
- **编解码两端类型要匹配**：字段名、类型需要一致；多余或缺失的字段按 gob 的规则做兼容处理，但类型不兼容时会返回错误。
- **不跨语言**：gob 是 Go 专有格式，需要与 JSON、Protobuf 等通用格式交互时应选择后者。

## 总结

`encoding/gob` 为 Go 程序提供了高效的自描述二进制序列化能力：普通场景直接 `Encode` / `Decode`，涉及接口时用 `gob.Register` 注册具体类型。它适合 Go 服务之间的内部通信与本地持久化；跨语言场景则应改用 JSON、XML 或 Protobuf。
