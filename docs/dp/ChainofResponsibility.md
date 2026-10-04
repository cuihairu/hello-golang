### 责任链模式 (Chain of Responsibility Pattern)

#### 意图
责任链模式是一种行为型设计模式：请求沿着一串处理对象传递，链上每个对象都有机会处理它。发送者不知道最终由谁处理，两者因此解耦。

#### 问题
拿客服系统举例：请求有技术支持、账单查询等多种类型，发送方如果要判断每种请求该给谁处理，就得知道全部处理对象，耦合和复杂度都会上去。让请求沿着处理链自己往下走，发送方就不用关心这些。

#### 解决方案
把多个处理对象串成一条链：每个对象处理自己认得的请求类型，不认得的转发给下一个。换处理者、调顺序都不用动发送方的代码。

#### 模式结构
1. **处理者（Handler）**：定义了处理请求的接口，包括设置下一个处理者的方法。
2. **具体处理者（Concrete Handler）**：实现了处理请求的逻辑，并将请求传递给链中的下一个处理者。
3. **客户端（Client）**：创建处理链并发起请求。

#### 代码
Go 实现：

```go
package main

import "fmt"

// 处理者接口
type Handler interface {
    SetNext(handler Handler)
    HandleRequest(request string)
}

// 具体处理者 - 技术支持处理者
type TechSupportHandler struct {
    next Handler
}

func (t *TechSupportHandler) SetNext(handler Handler) {
    t.next = handler
}

func (t *TechSupportHandler) HandleRequest(request string) {
    if request == "技术支持" {
        fmt.Println("技术支持处理请求:", request)
    } else if t.next != nil {
        t.next.HandleRequest(request)
    }
}

// 具体处理者 - 账单查询处理者
type BillingHandler struct {
    next Handler
}

func (b *BillingHandler) SetNext(handler Handler) {
    b.next = handler
}

func (b *BillingHandler) HandleRequest(request string) {
    if request == "账单查询" {
        fmt.Println("账单查询处理请求:", request)
    } else if b.next != nil {
        b.next.HandleRequest(request)
    }
}

// 具体处理者 - 客户服务处理者
type CustomerServiceHandler struct {
    next Handler
}

func (c *CustomerServiceHandler) SetNext(handler Handler) {
    c.next = handler
}

func (c *CustomerServiceHandler) HandleRequest(request string) {
    if request == "客户服务" {
        fmt.Println("客户服务处理请求:", request)
    } else if c.next != nil {
        c.next.HandleRequest(request)
    }
}

func main() {
    // 创建处理链
    techSupport := &TechSupportHandler{}
    billing := &BillingHandler{}
    customerService := &CustomerServiceHandler{}

    techSupport.SetNext(billing)
    billing.SetNext(customerService)

    // 客户请求
    requests := []string{"技术支持", "账单查询", "客户服务", "其他请求"}

    for _, request := range requests {
        fmt.Println("处理请求:", request)
        techSupport.HandleRequest(request)
        fmt.Println()
    }
}
```

#### 适用场景
- 需要处理多个不同类型的请求，并且这些请求可以由多个处理对象来处理时。
- 请求的处理逻辑可以动态地调整，例如根据不同的条件选择不同的处理者时。
- 需要将请求的处理解耦，以便于系统的扩展和维护。

#### 实现方式
实现分三步：接口里声明"设置下一个"和"处理请求"；每个具体处理者写自己的判断，不认识的请求转给 `next`；客户端负责创建对象、按顺序 `SetNext` 接好链，然后发起请求。

#### 优缺点
**优点**：
- 请求的发送者和接收者解耦，使得系统的扩展和维护更加灵活。
- 可以动态地调整处理链的顺序或添加新的处理者。
- 有利于请求的处理过程的分离和集中管理。

**缺点**：
- 可能会导致调试困难，因为请求的处理链是动态的，可能涉及多个处理者。
- 如果处理链较长，可能会增加请求处理的延迟。

#### 其他模式的关系
策略模式定义一系列可互换的算法，责任链则是让请求沿链传递，链上的每一环可以各用一种策略。命令模式把请求封装成对象，这些对象正好可以作为链上传递的载荷。中介者模式把对象间的多对多交互收拢到一个中介者身上，当交互复杂到一条链排不下时，就该换成中介者。