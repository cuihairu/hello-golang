### 工厂方法模式 (Factory Method Pattern)

#### 意图
工厂方法模式是一种创建型设计模式，它定义了一个创建对象的接口，但由子类决定实例化哪一个类。工厂方法使一个类的实例化延迟到其子类。

#### 问题
在现实世界中，考虑一个在线支付系统。该系统需要支持多种支付方式，例如信用卡支付、支付宝支付和微信支付。每种支付方式都有不同的处理逻辑。如果在主应用中硬编码这些支付方式，会导致代码难以维护和扩展。

#### 解决方案
使用工厂方法模式，我们可以定义一个支付接口和多个支付方式的实现类，并通过工厂方法来创建具体的支付对象。这样可以在不修改客户端代码的情况下，轻松添加新的支付方式。

#### 模式结构
1. **产品接口（Product）**：定义支付方式的接口。
2. **具体产品（ConcreteProduct）**：实现支付方式接口的具体支付类，例如信用卡支付、支付宝支付和微信支付。
3. **工厂接口（Creator）**：声明创建产品对象的工厂方法。
4. **具体工厂（ConcreteCreator）**：实现工厂接口的具体工厂类，负责实例化具体的支付方式。

#### 代码
以下是使用Go语言实现的工厂方法模式示例：

```go
package main

import "fmt"

// PaymentMethod 是支付方式接口
type PaymentMethod interface {
    Pay(amount float64) string
}

// CreditCard 是具体的支付方式 - 信用卡
type CreditCard struct{}

func (c *CreditCard) Pay(amount float64) string {
    return fmt.Sprintf("Paid %f using Credit Card", amount)
}

// AliPay 是具体的支付方式 - 支付宝
type AliPay struct{}

func (a *AliPay) Pay(amount float64) string {
    return fmt.Sprintf("Paid %f using AliPay", amount)
}

// WeChatPay 是具体的支付方式 - 微信支付
type WeChatPay struct{}

func (w *WeChatPay) Pay(amount float64) string {
    return fmt.Sprintf("Paid %f using WeChatPay", amount)
}

// PaymentFactory 是工厂接口
type PaymentFactory interface {
    CreatePaymentMethod() PaymentMethod
}

// CreditCardFactory 是具体的工厂类 - 信用卡支付工厂
type CreditCardFactory struct{}

func (ccf *CreditCardFactory) CreatePaymentMethod() PaymentMethod {
    return &CreditCard{}
}

// AliPayFactory 是具体的工厂类 - 支付宝支付工厂
type AliPayFactory struct{}

func (apf *AliPayFactory) CreatePaymentMethod() PaymentMethod {
    return &AliPay{}
}

// WeChatPayFactory 是具体的工厂类 - 微信支付工厂
type WeChatPayFactory struct{}

func (wpf *WeChatPayFactory) CreatePaymentMethod() PaymentMethod {
    return &WeChatPay{}
}

// main 函数演示了工厂方法模式的使用
func main() {
    var factory PaymentFactory

    // 使用信用卡支付
    factory = &CreditCardFactory{}
    paymentMethod := factory.CreatePaymentMethod()
    fmt.Println(paymentMethod.Pay(100.0))

    // 使用支付宝支付
    factory = &AliPayFactory{}
    paymentMethod = factory.CreatePaymentMethod()
    fmt.Println(paymentMethod.Pay(200.0))

    // 使用微信支付
    factory = &WeChatPayFactory{}
    paymentMethod = factory.CreatePaymentMethod()
    fmt.Println(paymentMethod.Pay(300.0))
}
```

#### 适用场景
- 需要在代码中避免创建对象的具体类时。
- 当一个类不知道它所需要的对象的类时。
- 当一个类希望由子类来指定创建对象的类时。
- 需要在系统中提供一个产品类的库，且只显示它们的接口而不是实现时。

#### 实现方式
1. 创建一个产品接口，定义产品的通用行为。
2. 创建具体产品类，实现产品接口。
3. 创建工厂接口，声明创建产品对象的工厂方法。
4. 创建具体工厂类，实现工厂接口，负责实例化具体的产品对象。

#### 优缺点
**优点**：
- 使一个类的实例化延迟到其子类。
- 符合单一职责原则，工厂类只负责对象的创建。
- 遵循开闭原则，可以通过添加新的具体产品类来扩展系统，而不修改已有代码。

**缺点**：
- 每增加一个具体产品类，就需要增加一个相应的具体工厂类，增加了代码量。

#### 其他模式的关系
- **抽象工厂模式（Abstract Factory Pattern）**：工厂方法模式通常与抽象工厂模式一起使用，通过在抽象工厂中定义工厂方法来创建产品对象。
- **模板方法模式（Template Method Pattern）**：工厂方法可以与模板方法模式结合使用，以在创建对象时执行通用行为。
- **策略模式（Strategy Pattern）**：工厂方法模式可以与策略模式结合使用，动态选择和创建策略对象。