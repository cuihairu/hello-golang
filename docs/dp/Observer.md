### 观察者模式 (Observer Pattern)

#### 意图
观察者模式是一种行为型设计模式：一个对象状态变了，订阅它的对象挨个收到通知、跟着更新。这是事件发布-订阅机制的原型，发布者不必知道订阅者是谁。

#### 问题
拿新闻发布来说，报社发一条新闻，订了的读者都要收到。若报社代码里逐个写死通知逻辑，加一个渠道就得改报社那边。观察者模式把"被通知的人"抽象成观察者，发布者只负责按名单广播。

#### 解决方案
定一个主题接口（Subject），带添加、删除观察者和广播通知的方法；再定一个观察者接口（Observer），带一个更新方法。主题持有观察者列表，状态一变就把列表挨个调一遍；观察者在更新方法里响应这次变化。

#### 模式结构
1. **主题接口（Subject）**：声明添加、删除观察者的方法，以及通知观察者的方法。
2. **具体主题（Concrete Subject）**：实现主题接口，维护观察者列表，并在状态发生变化时通知观察者。
3. **观察者接口（Observer）**：声明更新的方法，用于在主题状态变化时进行响应。
4. **具体观察者（Concrete Observer）**：实现观察者接口，并定义在主题状态变化时的具体响应操作。

#### 代码
用 Go 实现一遍：

```go
package main

import "fmt"

// 观察者接口
type Observer interface {
    Update(subject Subject)
}

// 主题接口
type Subject interface {
    AddObserver(observer Observer)
    RemoveObserver(observer Observer)
    NotifyObservers()
}

// 具体主题 - 价格更新器
type PriceUpdater struct {
    observers []Observer
    price     float64
}

func (p *PriceUpdater) AddObserver(observer Observer) {
    p.observers = append(p.observers, observer)
}

func (p *PriceUpdater) RemoveObserver(observer Observer) {
    for i, o := range p.observers {
        if o == observer {
            p.observers = append(p.observers[:i], p.observers[i+1:]...)
            break
        }
    }
}

func (p *PriceUpdater) NotifyObservers() {
    for _, observer := range p.observers {
        observer.Update(p)
    }
}

func (p *PriceUpdater) SetPrice(price float64) {
    p.price = price
    p.NotifyObservers()
}

func (p *PriceUpdater) GetPrice() float64 {
    return p.price
}

// 具体观察者 - 消费者
type Consumer struct {
    name string
}

func (c *Consumer) Update(subject Subject) {
    if priceUpdater, ok := subject.(*PriceUpdater); ok {
        fmt.Printf("%s 收到价格更新: %.2f\n", c.name, priceUpdater.GetPrice())
    }
}

func main() {
    // 创建价格更新器
    priceUpdater := &PriceUpdater{}

    // 创建消费者
    consumer1 := &Consumer{name: "Alice"}
    consumer2 := &Consumer{name: "Bob"}

    // 注册消费者到价格更新器
    priceUpdater.AddObserver(consumer1)
    priceUpdater.AddObserver(consumer2)

    // 更新价格
    priceUpdater.SetPrice(99.99)
    priceUpdater.SetPrice(89.99)
}
```

#### 适用场景
- 需要在一个对象状态发生变化时自动通知多个对象时，例如在事件驱动的系统中。
- 需要减少对象之间的耦合，使得系统更容易扩展和维护时。
- 需要实现发布-订阅机制时，例如在消息传递系统或实时数据更新系统中。

#### 实现方式
通知的两端各定一个接口：主题接口管登记和广播，观察者接口管响应。具体主题维护观察者列表，具体观察者写自己的反应。客户端把观察者登记进主题，之后只管改状态，通知由主题去广播。

#### 优缺点
**优点**：
- 发布者和订阅者互相不认识，换掉任何一方都不用改对方。
- 观察者可以运行时动态添加、删除，通知名单随业务变。
- 天然贴合事件驱动、实时推送这类场景。

**缺点**：
- 观察者多了，一次通知就是一次遍历，通知本身有开销。
- 观察者之间若互相依赖，通知顺序一乱就难查，系统复杂度上来了。

#### 其他模式的关系
- **观察者模式与中介者模式（Mediator Pattern）**：中介者负责协调对象之间的交互，观察者负责状态变化后的通知；在中介者内部用观察者来派发通知，两者可以叠着用。
- **观察者模式与策略模式（Strategy Pattern）**：策略管算法可互换，观察者管状态变化的广播；策略变了要通知使用方时，正好用观察者发出去。
- **观察者模式与事件驱动模型**：观察者模式是事件驱动模型的实现方式之一，事件的发布和订阅就落在它身上。