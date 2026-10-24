### CGO Call Records

CGO is a feature of Go that lets Go code and C/C++ code call each other: from the Go side you can call C functions and access C structs and arrays, and with `//export` you can export Go functions for C to call. Here I collect calling C/C++ functions, type conversion, memory management, linking external libraries, and common pitfalls.


### 1. Calling C Functions

Calling a C function with CGO takes these steps:

1. **Import the C package**: use the `import "C"` statement.
2. **Write C code**: put the C code in the comment block before `import "C"`.
3. **Call the C function**: call it with the `C.<function_name>` syntax.

Example:

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

> Note: `C.free` needs the C `free` declaration, so the comment must `#include <stdlib.h>`, otherwise you get `could not determine what C.free refers to`.

### 2. Type Conversion

##### Go types to C types

- **Strings**: use `C.CString` to convert a Go string to a C string.
- **Pointers**: use `unsafe.Pointer` for pointer conversion.

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

##### C types to Go types

- **C strings**: use `C.GoString` to convert a C string to a Go string.
- **Pointers**: use `unsafe.Pointer` and type conversion.

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

### 3. Struct Access

Define a C struct and access it from Go:

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

### 4. Array Access

Define a C array and access it from Go:

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

### 5. Calling C++ Code

Define the header file in the C++ code:

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

**Go code**:

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

Build command:

```sh
go build -o myprogram
./myprogram
```

### 6. C Calling Go Functions

Put a line of `//export` above the function declaration and that Go function gets exported as a C function, which C code can call directly.

One rule to watch: in a file that has `//export`, the preamble comment before `import "C"` can only hold declarations, not function definitions — cgo copies the preamble into multiple compilation units, so a definition there fails at link time with `multiple definition`. So put the C-side wrapper function in a `caller.c` in the same directory, and `go build` compiles it along automatically.

**Go code**:

```go
package main

/*
// declare the C functions, defined in caller.c
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

**caller.c** (same directory as the .go file above):

```c
#include <stdio.h>

extern void goHello();

void callGoHello() {
    goHello();
}
```

Build command:

```sh
go build -o myprogram
./myprogram
```

It prints `Hello from Go!`.

### 7. Memory Management

Memory allocated on the C side is not managed by Go's GC — you have to free it yourself:

1. **Free memory manually**: for memory allocated through C code, call the matching free function yourself, for example `C.free`.
2. **Use `defer`**: in Go, a `defer` statement can ensure the memory is freed when the function returns.

Example:

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

### 8. Common Type Conversions

Go provides some built-in definitions for C type conversion, mostly in the `C` package. Some common conversions:

##### Go to C

- `C.int` for `int`
- `C.char` for `char`
- `C.long` for `long`
- `C.float` for `float`
- `C.double` for `double`
- `C.CString(s)` converts a Go string `s` to a C string (`char*`); the memory must be freed with `C.free`

##### C to Go

- `C.GoString(cstr)` converts a C string `cstr` to a Go string
- `C.GoBytes(ptr, length)` converts a C byte array `ptr` to a Go byte slice

### 9. Using External Libraries

In practice a project will link against an external static or dynamic library. Here are examples of using external libraries with CGO.

#### Using an external static library

Suppose we have a static library `libmylib.a`; it can be used like this:

**C code (mylib.h)**:

```c
void myFunction();
```

**Go code**:

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

Build command:

```sh
go build -o myprogram
./myprogram
```

#### Using an external dynamic library

Suppose we have a dynamic library `libmylib.so`; it can be used like this:

**C code (mylib.h)**:

```c
void myFunction();
```

**Go code**:

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

Build command:

```sh
go build -o myprogram
LD_LIBRARY_PATH=. ./myprogram
```

### 10. Common Pitfalls

1. **Cross-language call overhead**: frequent calls between Go and C carry a performance cost.
2. **Memory management**: you have to watch allocation and deallocation to avoid memory leaks.
3. **Concurrency issues**: Go's concurrency model differs from C's threading model, so shared state needs careful handling.
4. **Platform dependency**: CGO code can depend on a specific platform and compiler, which reduces portability.
5. **Harder debugging**: CGO code mixes Go and C, which makes debugging more complex.
6. **Error handling**: passing error information between Go and C can be awkward.

Of these, memory management and concurrency are the ones that actually bite: an allocation like `C.CString` needs a matching `C.free`, deferred inside the same function; and since Go's concurrency model differs from C's threading model, code that comes in through a callback needs careful handling of shared state.

## References

- [cgo command documentation](https://pkg.go.dev/cmd/cgo)
- [Official · A Quick Guide to Go's Assembler](https://go.dev/doc/asm)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Internals](/cgo/Internals.md)
