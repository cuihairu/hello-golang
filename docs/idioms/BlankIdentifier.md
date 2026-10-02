# 空标识符

`_` 是 Go 语言中的空标识符（blank identifier）。它可以像普通标识符一样出现在声明或赋值中，但所有赋给它的值都会被直接丢弃——它不占用内存，也不能在后续代码中引用。空标识符是 Go 中"显式忽略"惯用法的基础。

### 基本用途

#### 1. 忽略函数的部分返回值

Go 的函数经常返回多个值，当只需要其中一部分时，用 `_` 显式忽略其余的值：

```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	// 只关心转换结果，忽略错误（确定输入合法时）
	n, _ := strconv.Atoi("42")
	fmt.Println(n * 2) // 输出: 84

	// 只关心下标，忽略值
	s := []string{"a", "b", "c"}
	for i, _ := range s {
		fmt.Print(i, " ")
	}
	fmt.Println()
}
```

#### 2. 忽略 range 中的键或值

当不需要某个迭代值时，使用 `_` 代替：

```go
sum := 0
for _, v := range numbers { // 忽略下标，只取值
	sum += v
}
```

实际上，当循环体只用到下标时，习惯上直接写成 `for i := range s`，它与 `for i, _ := range s` 语义相同且更简洁。

#### 3. 触发包的副作用初始化

这是空标识符最重要的用途之一。导入一个包却不直接使用它的任何标识符时，必须用 `_` 前缀，否则编译错误。典型例子是注册数据库驱动：

```go
import (
	"database/sql"
	_ "github.com/go-sql-driver/mysql" // 只为执行包的 init()，注册 mysql 驱动
)

func main() {
	// 驱动已在 init 中注册，这里可以直接使用 "mysql"
	db, err := sql.Open("mysql", "user:password@/dbname")
	if err != nil {
		panic(err)
	}
	defer db.Close()
}
```

`database/sql` 通过驱动注册表解耦了具体驱动：驱动包的 `init()` 调用 `sql.Register` 完成注册，业务代码只依赖 `database/sql` 接口。

#### 4. 类型断言的"检查但不使用"

在 `switch` 或类型断言中，用 `_` 表示不关心具体值：

```go
var v interface{} = "hello"

// 断言成功与否，但不使用具体值
if _, ok := v.(string); ok {
	fmt.Println("v 是字符串")
}
```

#### 5. 在声明中强制编译期检查

利用"常量/变量声明必须被使用"或"导入必须被使用"的规则，可以用空标识符做编译期断言。标准库中常见的技巧是让类型实现接口：

```go
package main

import "fmt"

type Shape interface {
	Area() float64
}

type Square struct{ Side float64 }

func (s Square) Area() float64 { return s.Side * s.Side }

// 编译期断言：*Square 一定实现了 Shape，否则无法编译
var _ Shape = (*Square)(nil)

func main() {
	var s Shape = &Square{Side: 3}
	fmt.Println(s.Area()) // 输出: 9
}
```

如果日后 `Square` 的 `Area` 方法被删除或改名，`var _ Shape = (*Square)(nil)` 这行会在编译期立刻报错，而不是等到运行时才发现。

#### 6. 忽略不需要的赋值结果

```go
package main

import "fmt"

func main() {
	// map 取值时忽略第二个返回值（键是否存在）
	m := map[string]int{"a": 1}
	v, _ := m["a"] // 只要值，不关心键是否存在（不存在时 v 为零值）
	fmt.Println(v)  // 输出: 1

	// 不关心键是否存在（与 m["a"] 为零值的场景不同，仅检查值是否为零值时才用）
	_, exists := m["b"]
	fmt.Println(exists) // 输出: false
}
```

### 空标识符与未使用变量

注意区分两种情况：

- **变量声明但未使用**（`x := 10` 之后没有用到 `x`）会编译错误。临时不需要时，可以 `_ = x` 显式"使用"它（调试时很常用）。
- **赋值给 `_`** 永远合法，因为 `_` 不算新声明的变量，也不需要被使用。

```go
func f() (int, error) { return 1, nil }

func main() {
	x, _ := f() // 合法
	_ = x       // 若暂时不用 x，用空标识符显式丢弃
}
```

### 使用注意

- **不要滥用 `_` 忽略 error**：忽略错误意味着错误发生时程序会带着错误的中间状态继续运行，这是许多线上事故的根源。只有确信失败无关紧要（或已在别处记录）时才应忽略。
- **`_` 不能出现在使用处**：`fmt.Println(_)` 是非法的——空标识符只能在赋值/声明语句中"接住"被丢弃的值，不能作为表达式引用。

### 总结

空标识符是 Go 中表达"我知道这里有值，但我故意不用它"的标准方式：忽略多余的返回值、引入仅有副作用的包、编写编译期接口断言。合理使用可以让意图一目了然，滥用（尤其是吞掉 error）则会埋下隐患。
