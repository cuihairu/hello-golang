### CGO 使用指南

CGO 是 Go 语言的一个特性，让 Go 代码能和 C/C++ 代码互相调用：既可以从 Go 侧调 C 函数、访问 C 结构体和数组，也可以用 `//export` 把 Go 函数导出给 C 调用。本文按调用 C/C++ 函数、类型转换、内存管理、引用外部库、常见的坑这几块来讲。


### 1. 调用 C 函数

使用 CGO 调用 C 函数需要以下步骤：

1. **导入 C 包**: 使用 `import "C"` 语句。
2. **编写 C 代码**: 在 `import "C"` 之前的注释块中编写 C 代码。
3. **调用 C 函数**: 使用 `C.<function_name>` 语法调用 C 函数。

示例：

```go
package main

/*
#include <stdio.h>
#include <stdlib.h>

void myPrint(char* s) {
    printf("%s\n", s);
}
*/
import "C"
import "unsafe"

func main() {
    str := "Hello from Go!"
    cstr := C.CString(str)
    defer C.free(unsafe.Pointer(cstr))
    C.myPrint(cstr)
}
```

> 注意：`C.free` 需要 C 的 `free` 函数声明，因此注释中必须 `#include <stdlib.h>`，否则会报 `could not determine what C.free refers to`。

### 2. 类型转换

##### Go 类型转换为 C 类型

- **字符串**: 使用 `C.CString` 将 Go 字符串转换为 C 字符串。
- **指针**: 使用 `unsafe.Pointer` 进行指针转换。

```go
package main

/*
#include <stdlib.h>
*/
import "C"
import "unsafe"

func main() {
    str := "Hello"
    cstr := C.CString(str)
    defer C.free(unsafe.Pointer(cstr))
}
```

##### C 类型转换为 Go 类型

- **C 字符串**: 使用 `C.GoString` 将 C 字符串转换为 Go 字符串。
- **指针**: 使用 `unsafe.Pointer` 和类型转换。

```go
package main

/*
#include <stdlib.h>
*/
import "C"
import "unsafe"
import "fmt"

func main() {
    cstr := C.CString("Hello")
    defer C.free(unsafe.Pointer(cstr))
    gostr := C.GoString(cstr)
    fmt.Println(gostr)
}
```

### 3. 结构体访问

定义 C 结构体并在 Go 中访问：

```go
package main

/*
#include <stdio.h>

typedef struct {
    int x;
    int y;
} Point;

void printPoint(Point* p) {
    printf("Point(%d, %d)\n", p->x, p->y);
}
*/
import "C"
import "fmt"

func main() {
    p := C.Point{x: 10, y: 20}
    C.printPoint(&p)
    fmt.Println(p.x, p.y)
}
```

### 4. 数组访问

定义 C 数组并在 Go 中访问：

```go
package main

/*
#include <stdio.h>

void printArray(int* arr, int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}
*/
import "C"
import "unsafe"

func main() {
    arr := []C.int{1, 2, 3, 4, 5}
    C.printArray((*C.int)(unsafe.Pointer(&arr[0])), C.int(len(arr)))
}
```

### 5. 调用 C++ 代码

在 C++ 代码中定义头文件：

**myclass.h**:

```cpp
#ifdef __cplusplus
extern "C" {
#endif

typedef struct MyClass MyClass;

MyClass* NewMyClass();
void MyClass_sayHello(MyClass* obj);

#ifdef __cplusplus
}
#endif
```

**myclass.cpp**:

```cpp
#include <iostream>
#include "myclass.h"

class MyClass {
public:
    void sayHello() {
        std::cout << "Hello from C++" << std::endl;
    }
};

extern "C" {
    MyClass* NewMyClass() {
        return new MyClass();
    }
    void MyClass_sayHello(MyClass* obj) {
        obj->sayHello();
    }
}
```

**Go 代码**:

```go
package main

/*
#cgo CXXFLAGS: -std=c++11
#cgo LDFLAGS: -lstdc++
#include "myclass.h"
*/
import "C"

func main() {
    obj := C.NewMyClass()
    C.MyClass_sayHello(obj)
}
```

编译命令：

```sh
go build -o myprogram
./myprogram
```

### 6. C 调用 Go 函数

在函数声明上加一行 `//export`，这个 Go 函数就会被导出成 C 函数，C 代码可以直接调。

注意一条规则：带 `//export` 的文件里，`import "C"` 的前置注释只能放声明、不能放函数定义——cgo 会把前置注释复制进多个编译单元，定义放这里会在链接期报 `multiple definition`。所以 C 侧的包装函数放到同目录的 `caller.c` 里，`go build` 会自动一起编译。

**Go 代码**:

```go
package main

/*
// 声明C函数，定义在 caller.c 中
extern void goHello();
extern void callGoHello();
*/
import "C"

//export goHello
func goHello() {
    println("Hello from Go!")
}

func main() {
    C.callGoHello()
}
```

**caller.c**（与上面的 .go 文件同目录）:

```c
#include <stdio.h>

extern void goHello();

void callGoHello() {
    goHello();
}
```

编译命令：

```sh
go build -o myprogram
./myprogram
```

运行输出 `Hello from Go!`。

### 7. 内存管理

C 侧分配的内存，Go 的 GC 不管，得自己释放：

1. **手动释放内存**: 对于通过 C 代码分配的内存，需要手动调用相应的释放函数，例如 `C.free`。
2. **使用 `defer`**: 在 Go 中，可以使用 `defer` 语句来确保在函数返回时释放内存。

示例：

```go
package main

/*
#include <stdlib.h>
*/
import "C"
import "unsafe"

func main() {
    str := C.CString("Hello")
    defer C.free(unsafe.Pointer(str))
}
```

### 8. 常见的类型转换

Go 提供了一些与 C 类型转换的内置定义，主要在 `C` 包中。以下是一些常见类型转换：

##### Go to C

- `C.int` 对应 `int`
- `C.char` 对应 `char`
- `C.long` 对应 `long`
- `C.float` 对应 `float`
- `C.double` 对应 `double`
- `C.CString(s)` 将 Go 字符串 `s` 转换为 C 字符串（`char*`），需要使用 `C.free` 释放内存

##### C to Go

- `C.GoString(cstr)` 将 C 字符串 `cstr` 转换为 Go 字符串
- `C.GoBytes(ptr, length)` 将 C 字节数组 `ptr` 转换为 Go 字节切片

### 9. 引用外部库

通常情况下，项目中会引用外部静态库或动态库。以下是如何在 CGO 中使用外部库的示例。

#### 使用外部静态库

假设我们有一个静态库 `libmylib.a`，可以如下方式使用：

**C 代码（mylib.h）**:

```c
void myFunction();
```

**Go 代码**:

```go
package main

/*
#cgo LDFLAGS: -L. -lmylib
#include "mylib.h"
*/
import "C"

func main() {
    C.myFunction()
}
```

编译命令：

```sh
go build -o myprogram
./myprogram
```

#### 使用外部动态库

假设我们有一个动态库 `libmylib.so`，可以如下方式使用：

**C 代码（mylib.h）**:

```c
void myFunction();
```

**Go 代码**:

```go
package main

/*
#cgo LDFLAGS: -L. -lmylib
#include "mylib.h"
*/
import "C"

func main() {
    C.myFunction()
}
```

编译命令：

```sh
go build -o myprogram
LD_LIBRARY_PATH=. ./myprogram
```

### 10. 常见的坑

1. **跨语言调用开销**: 频繁的 Go 和 C 之间调用会有性能开销。
2. **内存管理**: 必须注意内存的分配和释放，避免内存泄漏。
3. **并发问题**: Go 的并发模型和 C 的线程模型不同，需要小心处理并发问题。
4. **平台依赖**: CGO 代码可能依赖于特定的平台和编译器，降低了可移植性。
5. **调试困难**: CGO 代码混合了 Go 和 C，调试可能更加复杂。
6. **错误处理**: 在 Go 和 C 之间传递错误信息可能会比较复杂。

这几条里内存管理和并发最容易出事：`C.CString` 这类分配要配 `C.free`，用 `defer` 挂在同个函数里；Go 的并发模型和 C 的线程模型不同，回调进来的代码要小心处理共享状态。