### 单例模式 (Singleton Pattern)

#### 意图
单例模式是一种创建型设计模式，它确保一个类只有一个实例，并提供一个全局访问点来访问这个实例。单例模式常用于需要一个全局唯一对象的场景。

#### 问题
在现实世界中，考虑一个日志系统。系统中所有模块都需要记录日志，如果每个模块都创建一个日志对象，会浪费资源并导致日志的不一致。

#### 解决方案
使用单例模式，我们可以确保日志系统只有一个实例，所有模块共享这个实例，从而保证资源的合理利用和日志的一致性。

#### 模式结构
1. **单例（Singleton）**：包含一个私有静态变量来保存唯一实例，并提供一个公共静态方法来获取这个实例。
2. **客户端（Client）**：通过单例类的公共静态方法来访问唯一实例。

#### 饿汉式实现
饿汉式单例在类加载时就创建实例，线程安全，但可能会造成不必要的资源浪费。

```go
package main

import "fmt"

// 单例类 - 饿汉式
type Singleton struct{}

var instance = &Singleton{}

// 获取实例的公共方法
func GetInstance() *Singleton {
    return instance
}

func main() {
    singleton1 := GetInstance()
    singleton2 := GetInstance()

    if singleton1 == singleton2 {
        fmt.Println("饿汉式: singleton1 和 singleton2 是相同的实例")
    } else {
        fmt.Println("饿汉式: singleton1 和 singleton2 是不同的实例")
    }
}
```

#### 饱汉式实现
饱汉式单例在第一次使用时创建实例，延迟初始化，节省资源，但需要考虑线程安全问题。

```go
package main

import (
    "fmt"
    "sync"
)

// 单例类 - 饱汉式
type Singleton struct{}

var instance *Singleton
var mu sync.Mutex

// 获取实例的公共方法
func GetInstance() *Singleton {
    if instance == nil {
        mu.Lock()
        defer mu.Unlock()
        if instance == nil {
            instance = &Singleton{}
        }
    }
    return instance
}

func main() {
    singleton1 := GetInstance()
    singleton2 := GetInstance()

    if singleton1 == singleton2 {
        fmt.Println("饱汉式: singleton1 和 singleton2 是相同的实例")
    } else {
        fmt.Println("饱汉式: singleton1 和 singleton2 是不同的实例")
    }
}
```

#### 适用场景
- 需要一个全局唯一对象的场景，例如配置管理、日志管理等。
- 需要控制资源访问，避免多个实例导致资源浪费或不一致的场景。

#### 实现方式
1. 创建一个包含私有静态变量来保存唯一实例的类。
2. 提供一个公共静态方法来获取这个实例。
3. 确保类的构造方法是私有的，防止外部创建新实例。

#### 优缺点
**优点**：
- 确保一个类只有一个实例，节约资源。
- 提供全局访问点，便于控制和管理。

**缺点**：
- 饿汉式在类加载时就创建实例，可能造成不必要的资源浪费。
- 饱汉式需要处理线程安全问题，增加了实现的复杂性。

#### 其他模式的关系
- **工厂方法模式（Factory Method Pattern）**：工厂方法模式用于创建对象的工厂类，而单例模式确保工厂类本身只有一个实例。
- **原型模式（Prototype Pattern）**：原型模式通过复制现有对象创建新对象，而单例模式确保类只有一个实例。

### 单例模式的扩展
在一些场景中，可能需要创建多个单例实例（例如数据库连接池），这种情况下可以使用多例模式（Multiton Pattern），确保每个关键字对应一个唯一实例。