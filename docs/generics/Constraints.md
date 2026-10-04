### 类型约束

类型约束用接口定义，限定类型参数能接受哪些类型、必须有哪些方法。本章讲预定义约束、接口类型约束和类型集三块。

#### 3.1 预定义约束

Go语言提供了一些预定义的类型约束，以简化常见的类型限制。这些预定义约束包括`any`和`comparable`。

**any**：
`any`是一个特殊的预定义约束，表示类型参数可以是任意类型。在Go 1.18之前，`any`是通过空接口`interface{}`表示的，但现在推荐使用`any`作为泛型的默认约束。

示例：
```go
func PrintSlice[T any](s []T) {
    for _, v := range s {
        fmt.Println(v)
    }
}
```

`T`被约束为`any`，表示可以是任何类型。

**comparable**：
`comparable`是另一个预定义约束，表示类型参数必须是可以进行比较操作的类型。具有`comparable`约束的类型可以用于比较操作（如`==`和`!=`）。

示例：
```go
func Contains[T comparable](s []T, v T) bool {
    for _, item := range s {
        if item == v {
            return true
        }
    }
    return false
}
```

`T`被约束为`comparable`，表示可以进行比较操作，以确保`Contains`函数能够正确判断元素是否存在。

#### 3.2 接口类型约束

接口类型约束用接口指定类型参数必须实现哪些方法，复杂的限制按需求自己组合。

**定义接口类型约束**：
先定义带方法的接口，再在类型参数里写这个接口名，类型参数必须实现接口中的方法。

示例：
```go
type Stringer interface {
    String() string
}

func PrintStrings[T Stringer](s []T) {
    for _, v := range s {
        fmt.Println(v.String())
    }
}
```

`T`被约束为`Stringer`接口，表示类型参数必须实现`String`方法。

**使用接口类型约束**：
接口类型约束可以用在泛型函数、泛型方法和泛型类型中。

示例：
```go
type Box[T Stringer] struct {
    content T
}

func (b *Box[T]) PrintContent() {
    fmt.Println(b.content.String())
}
```

`Box`类型被约束为`Stringer`接口，表示类型参数必须实现`String`方法。

#### 3.3 类型集

类型集（Type Sets）定义一组具体类型，类型参数只能从这组类型中选。它写在接口里，用`~`操作符和具体类型组合。

**定义类型集**：
类型集通过在接口中使用`~`操作符和具体类型来定义。类型集可以包含一个或多个具体类型。

示例：
```go
type Integer interface {
    ~int | ~int8 | ~int16 | ~int32 | ~int64
}

func SumIntegers[T Integer](a, b T) T {
    return a + b
}
```

`Integer`接口定义了一个类型集，包括`int`、`int8`、`int16`、`int32`和`int64`。`SumIntegers`函数的类型参数`T`被约束为`Integer`类型集中的任意一种类型。

**使用类型集**：
类型集可以用在泛型函数、泛型方法和泛型类型中，确保类型参数属于定义的类型集合。

示例：
```go
type Number interface {
    ~int | ~float64
}

func AddNumbers[T Number](a, b T) T {
    return a + b
}
```

`Number`接口定义了一个类型集，包括`int`和`float64`。`AddNumbers`函数的类型参数`T`被约束为`Number`类型集中的任意一种类型。

#### 3.4 多重约束

类型参数可以同时受多个约束，必须全部满足。做法是把接口组合起来，比如一个接口嵌入另一个。

示例：
```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type ReadWriter interface {
    Reader
    Writer
}

func Copy[T ReadWriter](src, dst T) error {
    buf := make([]byte, 1024)
    for {
        n, err := src.Read(buf)
        if err == io.EOF {
            return nil // 读到末尾，正常结束
        }
        if err != nil {
            return err
        }
        if n == 0 {
            break
        }
        if _, err := dst.Write(buf[:n]); err != nil {
            return err
        }
    }
    return nil
}
```

`ReadWriter`接口同时包含了`Reader`和`Writer`接口的方法，`Copy`函数的类型参数`T`必须实现`ReadWriter`接口。

#### 3.5 小结

三类约束各管一段：`any` 和 `comparable` 是现成的，方法集用接口类型约束，具体类型集合用类型集，多个约束合起来写在类型参数上。