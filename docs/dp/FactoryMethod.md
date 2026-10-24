### Factory Method Pattern

#### Intent
The Factory Method pattern is a creational design pattern that defines an interface for creating objects, but leaves it to subclasses to decide which class to instantiate. It defers the instantiation of a class to its subclasses.

#### Problem
Take an online payment system as an example: it has to support credit card, Alipay, and WeChat Pay, and the handling logic differs for each method. Once those methods are hardcoded into the main application, the code becomes hard to maintain and extend.

#### Solution
With the Factory Method pattern, define a payment interface plus implementation classes for each payment method, and let factory methods create the concrete payment objects. Adding a new payment method afterwards doesn't require changing the client code.

#### Pattern structure
1. **Product interface**: defines the interface for a payment method.
2. **Concrete Product**: the concrete payment classes that implement the payment method interface, such as credit card, Alipay, and WeChat Pay.
3. **Creator interface**: declares the factory method that creates a product object.
4. **Concrete Creator**: the concrete factory classes that implement the creator interface and are responsible for instantiating specific payment methods.

#### Code

```go
package main

import "fmt"

// PaymentMethod is the payment method interface
type PaymentMethod interface {
    Pay(amount float64) string
}

// CreditCard is a concrete payment method - credit card
type CreditCard struct{}

func (c *CreditCard) Pay(amount float64) string {
    return fmt.Sprintf("Paid %f using Credit Card", amount)
}

// AliPay is a concrete payment method - Alipay
type AliPay struct{}

func (a *AliPay) Pay(amount float64) string {
    return fmt.Sprintf("Paid %f using AliPay", amount)
}

// WeChatPay is a concrete payment method - WeChat Pay
type WeChatPay struct{}

func (w *WeChatPay) Pay(amount float64) string {
    return fmt.Sprintf("Paid %f using WeChatPay", amount)
}

// PaymentFactory is the factory interface
type PaymentFactory interface {
    CreatePaymentMethod() PaymentMethod
}

// CreditCardFactory is a concrete factory class - credit card factory
type CreditCardFactory struct{}

func (ccf *CreditCardFactory) CreatePaymentMethod() PaymentMethod {
    return &CreditCard{}
}

// AliPayFactory is a concrete factory class - Alipay factory
type AliPayFactory struct{}

func (apf *AliPayFactory) CreatePaymentMethod() PaymentMethod {
    return &AliPay{}
}

// WeChatPayFactory is a concrete factory class - WeChat Pay factory
type WeChatPayFactory struct{}

func (wpf *WeChatPayFactory) CreatePaymentMethod() PaymentMethod {
    return &WeChatPay{}
}

// The main function demonstrates how to use the Factory Method pattern
func main() {
    var factory PaymentFactory

    // pay with credit card
    factory = &CreditCardFactory{}
    paymentMethod := factory.CreatePaymentMethod()
    fmt.Println(paymentMethod.Pay(100.0))

    // pay with Alipay
    factory = &AliPayFactory{}
    paymentMethod = factory.CreatePaymentMethod()
    fmt.Println(paymentMethod.Pay(200.0))

    // pay with WeChat Pay
    factory = &WeChatPayFactory{}
    paymentMethod = factory.CreatePaymentMethod()
    fmt.Println(paymentMethod.Pay(300.0))
}
```

#### Use cases
- When you need to avoid referencing concrete creation classes in the code.
- When a class doesn't know the classes of the objects it needs.
- When a class wants its subclasses to specify the class of the objects being created.
- When you need to provide a library of product classes in the system, showing only their interfaces rather than their implementations.

#### Implementation
1. Create a product interface defining the product's general behavior.
2. Create concrete product classes that implement the product interface.
3. Create a creator interface that declares the factory method for creating product objects.
4. Create concrete creator classes that implement the creator interface and are responsible for instantiating concrete product objects.

#### Pros and cons
**Pros**:
- Defers the instantiation of a class to its subclasses.
- Follows the single responsibility principle; a factory class is only responsible for creating objects.
- Follows the open-closed principle; you can extend the system by adding new concrete product classes without modifying existing code.

**Cons**:
- Every new concrete product class requires a corresponding concrete creator class, which adds to the amount of code.

#### Relations to other patterns
- **Abstract Factory Pattern**: the Factory Method pattern is usually used together with the Abstract Factory pattern, which defines factory methods inside an abstract factory to create product objects.
- **Template Method Pattern**: Factory Method can be combined with the Template Method pattern to perform common behavior when creating objects.
- **Strategy Pattern**: the Factory Method pattern can be combined with the Strategy pattern to select and create strategy objects dynamically.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Facade](/dp/Facade.md)
- [Flyweight](/dp/Flyweight.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Facade](/dp/Facade.md)
- [Flyweight](/dp/Flyweight.md)
