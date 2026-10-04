在 Go 语言中，作用域回答"这个名字在哪里能用"，生命周期回答"这块内存什么时候被回收"。两者都由变量声明的位置决定。

### 变量的作用域

作用域（Scope）是指程序中变量可以被引用的范围。Go 语言中变量的作用域主要包括以下几种：

1. **包作用域（Package Scope）**：
   - 在包级别声明的变量可以在同一个包内的所有文件中访问。
   - 包作用域的变量通常使用 `var` 关键字在包级别声明。
   - 如果变量名以大写字母开头，则该变量是导出的，可以被其他包访问。

   例如：
   ```go
   // file1.go
   package main

   var PackageVar = "I am accessible throughout the package"

   func main() {
       fmt.Println(PackageVar)
   }

   // file2.go
   package main

   func anotherFunction() {
       fmt.Println(PackageVar) // 可以访问 PackageVar
   }
   ```

2. **函数作用域（Function Scope）**：
   - 在函数内声明的变量只能在该函数内访问。
   - 函数作用域的变量包括函数参数和在函数内使用 `var` 或 `:=` 声明的变量。

   例如：
   ```go
   func exampleFunction() {
       var functionVar = "I am only accessible within this function"
       fmt.Println(functionVar)
   }

   func anotherFunction() {
       // fmt.Println(functionVar) // 无法访问 functionVar
   }
   ```

3. **块作用域（Block Scope）**：
   - 在代码块内（例如 `if`、`for`、`switch` 等）声明的变量只能在该代码块内访问。
   - 块作用域的变量可以使用 `var` 或 `:=` 声明。

   例如：
   ```go
   func exampleFunction() {
       if true {
           var blockVar = "I am only accessible within this block"
           fmt.Println(blockVar)
       }
       // fmt.Println(blockVar) // 无法访问 blockVar
   }
   ```

### 变量的生命周期

生命周期（Lifetime）是指变量从创建到销毁的整个过程。Go 语言中变量的生命周期主要受其作用域的影响：

1. **包级变量**：
   - 包级变量在程序启动时分配内存，并在程序结束时释放。
   - 其生命周期贯穿整个程序运行期间。

   例如：
   ```go
   var packageVar = "I live for the lifetime of the program"
   ```

2. **局部变量**：
   - 局部变量在其所在函数或代码块执行时分配内存，并在该函数或代码块执行结束时释放。
   - 局部变量的生命周期通常较短，局限于函数或代码块的执行时间。

   例如：
   ```go
   func exampleFunction() {
       var localVar = "I live for the lifetime of this function"
       fmt.Println(localVar)
   }
   ```

3. **动态分配的变量**：
   - 使用 `new` 或 `make` 关键字动态分配的变量，其生命周期由程序控制，可以在函数外部继续使用。
   - 动态分配的变量无需手动释放，当它们不再被引用时，Go 语言的垃圾回收器会自动回收其占用的内存。

   例如：
   ```go
   func exampleFunction() {
       ptr := new(int)   // 动态分配
       *ptr = 100
       fmt.Println(*ptr) // 动态分配的变量可以在函数外部继续使用
   }
   ```

### 示例代码

三种作用域放在一个程序里看：

```go
package main

import "fmt"

// 包级变量
var packageVar = "I am a package-level variable"

func main() {
    fmt.Println(packageVar) // 访问包级变量

    // 局部变量
    var functionVar = "I am a function-level variable"
    fmt.Println(functionVar)

    if true {
        // 块级变量
        var blockVar = "I am a block-level variable"
        fmt.Println(blockVar)
    }
    // fmt.Println(blockVar) // 无法访问 blockVar

    anotherFunction()
}

func anotherFunction() {
    fmt.Println(packageVar) // 访问包级变量
    // fmt.Println(functionVar) // 无法访问 functionVar
}
```

### 总结

包级变量整个进程存活，局部变量随函数调用结束消失，`new`/`make` 分配的内存等没有引用时由 GC 回收。作用域和生命周期是同一件事的两面：声明在哪个块里，决定了名字在哪里可见，也决定了内存活多久。