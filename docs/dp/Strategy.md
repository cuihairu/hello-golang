### 策略模式 (Strategy Pattern)

#### 意图
策略模式是一种行为型设计模式：定义一系列算法，把每个算法封装成可互换的策略，算法怎么变都不影响使用算法的客户端。

#### 问题
在现实世界中，考虑一个支付系统，不同的支付方式（如信用卡、支付宝、PayPal）需要不同的处理逻辑。如果将所有支付逻辑都写在一个类中，会导致类变得复杂且难以维护。策略模式通过将不同的支付方式封装为不同的策略对象，并在运行时选择合适的策略，简化了支付逻辑的管理。

#### 解决方案
使用策略模式，我们可以定义一个策略接口，声明算法的方法。然后，创建具体策略类来实现这些方法。上下文类（Context）持有一个策略对象，并在运行时委托给策略对象来执行算法。通过改变策略对象，可以在运行时改变上下文的行为。

#### 模式结构
1. **策略接口（Strategy）**：定义算法的方法。
2. **具体策略（Concrete Strategy）**：实现策略接口，定义具体的算法。
3. **上下文（Context）**：持有策略对象，并将算法的执行委托给策略对象。

#### 代码

```go
package main

import "fmt"

// 策略接口
type PaymentStrategy interface {
    Pay(amount float64)
}

// 具体策略 - 信用卡支付
type CreditCardPayment struct {
    cardNumber string
}

func (c *CreditCardPayment) Pay(amount float64) {
    fmt.Printf("使用信用卡 %s 支付 %.2f 元\n", c.cardNumber, amount)
}

// 具体策略 - 支付宝支付
type AlipayPayment struct {
    account string
}

func (a *AlipayPayment) Pay(amount float64) {
    fmt.Printf("使用支付宝账户 %s 支付 %.2f 元\n", a.account, amount)
}

// 具体策略 - PayPal支付
type PayPalPayment struct {
    email string
}

func (p *PayPalPayment) Pay(amount float64) {
    fmt.Printf("使用PayPal账户 %s 支付 %.2f 元\n", p.email, amount)
}

// 上下文 - 支付处理
type PaymentContext struct {
    strategy PaymentStrategy
}

func (p *PaymentContext) SetStrategy(strategy PaymentStrategy) {
    p.strategy = strategy
}

func (p *PaymentContext) ExecutePayment(amount float64) {
    p.strategy.Pay(amount)
}

func main() {
    // 创建支付上下文
    paymentContext := &PaymentContext{}

    // 使用信用卡支付
    paymentContext.SetStrategy(&CreditCardPayment{cardNumber: "1234-5678-9876-5432"})
    paymentContext.ExecutePayment(100.50)

    // 使用支付宝支付
    paymentContext.SetStrategy(&AlipayPayment{account: "example@alipay.com"})
    paymentContext.ExecutePayment(200.75)

    // 使用PayPal支付
    paymentContext.SetStrategy(&PayPalPayment{email: "example@paypal.com"})
    paymentContext.ExecutePayment(300.00)
}
```

#### 适用场景
- 当需要定义一系列算法，并使它们可以互换时，例如在支付系统中选择不同的支付方式。
- 当算法的使用场景多变，且需要在运行时动态选择不同的算法时。
- 当算法的实现复杂，而希望将其封装在不同的策略对象中，从而提高系统的可维护性时。

#### 实现方式
1. 定义策略接口，声明算法的方法。
2. 创建具体策略类，分别实现策略接口中的方法，定义具体的算法实现。
3. 定义上下文类，持有策略对象，并将算法的执行委托给策略对象。
4. 客户端代码创建上下文对象和具体策略对象，并设置合适的策略对象来执行算法。

#### 优缺点
**优点**：
- 算法封装进策略对象，客户端运行时换策略不用改上下文类。
- 替代了大量条件分支，加一种算法就是加一个策略类。

**缺点**：
- 策略一多就要多写一堆类，上下文与策略之间的依赖也增加复杂度。

#### 其他模式的关系
- **策略模式与状态模式（State Pattern）**：状态模式用于管理对象的状态并改变其行为，而策略模式用于将算法封装在不同的策略对象中。两者可以结合使用，例如在状态模式中使用策略模式来定义不同状态下的行为。
- **策略模式与工厂模式（Factory Pattern）**：工厂模式用于创建对象，而策略模式用于封装算法并使其可以互换。可以结合使用，例如使用工厂模式创建策略对象并在策略模式中使用。
- **策略模式与命令模式（Command Pattern）**：命令模式用于封装请求的操作，而策略模式用于封装不同的算法。可以结合使用，例如在策略模式中使用命令模式来执行策略操作。