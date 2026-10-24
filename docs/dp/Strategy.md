### Strategy Pattern

#### Intent
The Strategy pattern is a behavioral design pattern: it defines a family of algorithms, wraps each one as an interchangeable strategy, and lets the algorithms change without affecting the clients that use them.

#### Problem
Consider a payment system in the real world. Different payment methods (credit card, Alipay, PayPal) need different processing logic. Writing all the payment logic into a single class makes that class complex and hard to maintain. The Strategy pattern wraps each payment method in its own strategy object and picks the right one at runtime, which simplifies managing the payment logic.

#### Solution
With the Strategy pattern we can define a strategy interface that declares the algorithm's method. Then we create concrete strategy classes that implement it. The context class holds a strategy object and delegates execution of the algorithm to it at runtime. Swapping the strategy object changes the context's behavior at runtime.

#### Pattern structure
1. **Strategy interface**: defines the algorithm's method.
2. **Concrete Strategy**: implements the strategy interface and defines the concrete algorithm.
3. **Context**: holds the strategy object and delegates execution of the algorithm to it.

#### Code

```go
package main

import "fmt"

// Strategy interface
type PaymentStrategy interface {
    Pay(amount float64)
}

// Concrete strategy - credit card payment
type CreditCardPayment struct {
    cardNumber string
}

func (c *CreditCardPayment) Pay(amount float64) {
    fmt.Printf("使用信用卡 %s 支付 %.2f 元\n", c.cardNumber, amount)
}

// Concrete strategy - Alipay payment
type AlipayPayment struct {
    account string
}

func (a *AlipayPayment) Pay(amount float64) {
    fmt.Printf("使用支付宝账户 %s 支付 %.2f 元\n", a.account, amount)
}

// Concrete strategy - PayPal payment
type PayPalPayment struct {
    email string
}

func (p *PayPalPayment) Pay(amount float64) {
    fmt.Printf("使用PayPal账户 %s 支付 %.2f 元\n", p.email, amount)
}

// Context - payment processing
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
    // Create the payment context
    paymentContext := &PaymentContext{}

    // Pay with a credit card
    paymentContext.SetStrategy(&CreditCardPayment{cardNumber: "1234-5678-9876-5432"})
    paymentContext.ExecutePayment(100.50)

    // Pay with Alipay
    paymentContext.SetStrategy(&AlipayPayment{account: "example@alipay.com"})
    paymentContext.ExecutePayment(200.75)

    // Pay with PayPal
    paymentContext.SetStrategy(&PayPalPayment{email: "example@paypal.com"})
    paymentContext.ExecutePayment(300.00)
}
```

#### Applicable scenarios
- When you need to define a family of algorithms and make them interchangeable, for example when choosing among payment methods in a payment system.
- When the scenarios in which an algorithm is used vary a lot and you need to pick a different algorithm dynamically at runtime.
- When an algorithm's implementation is complex and you want to wrap it in separate strategy objects to make the system more maintainable.

#### Implementation
1. Define a strategy interface that declares the algorithm's method.
2. Create concrete strategy classes, each implementing the strategy interface's method with its own algorithm.
3. Define a context class that holds a strategy object and delegates execution of the algorithm to it.
4. Client code creates the context object and the concrete strategy objects, and sets the right strategy object to run the algorithm.

#### Pros and cons
**Pros**:
- Algorithms live in strategy objects, so a client can swap strategies at runtime without touching the context class.
- Replaces a pile of conditional branches; adding an algorithm means adding a strategy class.

**Cons**:
- Many strategies means writing a whole bunch of classes, and the dependency between context and strategy adds complexity.

#### Relationship to other patterns
- **Strategy Pattern and State Pattern**: the State pattern manages an object's state and changes its behavior, while the Strategy pattern wraps algorithms in separate strategy objects. The two can be combined, for example using the Strategy pattern inside the State pattern to define the behavior of each state.
- **Strategy Pattern and Factory Pattern**: the Factory pattern creates objects, while the Strategy pattern wraps algorithms and makes them interchangeable. They can be combined, for example using the Factory pattern to create strategy objects that are then used by the Strategy pattern.
- **Strategy Pattern and Command Pattern**: the Command pattern wraps the operations of a request, while the Strategy pattern wraps different algorithms. They can be combined, for example using the Command pattern inside the Strategy pattern to execute a strategy's operations.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [State](/dp/State.md)
- [Structural](/dp/Structural.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [State](/dp/State.md)
- [Structural](/dp/Structural.md)
