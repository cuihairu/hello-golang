### Abstract Factory Pattern

#### Intent
The Abstract Factory pattern is a creational design pattern that provides an interface for creating families of related or dependent objects without specifying their concrete classes. By using an abstract factory, a client can use different product families without modifying code.

#### Problem
Take a cross-platform GUI framework: it has to support Windows, macOS, and Linux, and each platform has its own implementation of widgets (buttons, text boxes, checkboxes, and so on). Once these widgets are hardcoded into the main application, the code becomes hard to maintain and hard to extend.

#### Solution
With the abstract factory pattern, define a widget factory interface and a widget factory for each platform, hand all widget creation off to the factory, and the client code becomes independent of the concrete platform.

#### Structure
1. **AbstractProduct**: defines the product interface, for example a button or a text box.
2. **ConcreteProduct**: concrete product classes that implement the product interface, for example a Windows button, a macOS button, a Linux button.
3. **AbstractFactory**: declares the factory methods that create a family of related product objects.
4. **ConcreteFactory**: concrete factory classes that implement the abstract factory interface and are responsible for instantiating concrete product objects.

#### Code

```go
package main

import "fmt"

// Button is the abstract product interface for a button
type Button interface {
    Render() string
}

// TextBox is the abstract product interface for a text box
type TextBox interface {
    Render() string
}

// WindowsButton is a concrete product - a Windows button
type WindowsButton struct{}

func (wb *WindowsButton) Render() string {
    return "Rendering Windows Button"
}

// WindowsTextBox is a concrete product - a Windows text box
type WindowsTextBox struct{}

func (wtb *WindowsTextBox) Render() string {
    return "Rendering Windows TextBox"
}

// MacOSButton is a concrete product - a macOS button
type MacOSButton struct{}

func (mb *MacOSButton) Render() string {
    return "Rendering macOS Button"
}

// MacOSTextBox is a concrete product - a macOS text box
type MacOSTextBox struct{}

func (mtb *MacOSTextBox) Render() string {
    return "Rendering macOS TextBox"
}

// LinuxButton is a concrete product - a Linux button
type LinuxButton struct{}

func (lb *LinuxButton) Render() string {
    return "Rendering Linux Button"
}

// LinuxTextBox is a concrete product - a Linux text box
type LinuxTextBox struct{}

func (ltb *LinuxTextBox) Render() string {
    return "Rendering Linux TextBox"
}

// GUIFactory is the abstract factory interface
type GUIFactory interface {
    CreateButton() Button
    CreateTextBox() TextBox
}

// WindowsFactory is a concrete factory - the Windows factory
type WindowsFactory struct{}

func (wf *WindowsFactory) CreateButton() Button {
    return &WindowsButton{}
}

func (wf *WindowsFactory) CreateTextBox() TextBox {
    return &WindowsTextBox{}
}

// MacOSFactory is a concrete factory - the macOS factory
type MacOSFactory struct{}

func (mf *MacOSFactory) CreateButton() Button {
    return &MacOSButton{}
}

func (mf *MacOSFactory) CreateTextBox() TextBox {
    return &MacOSTextBox{}
}

// LinuxFactory is a concrete factory - the Linux factory
type LinuxFactory struct{}

func (lf *LinuxFactory) CreateButton() Button {
    return &LinuxButton{}
}

func (lf *LinuxFactory) CreateTextBox() TextBox {
    return &LinuxTextBox{}
}

// main demonstrates using the abstract factory pattern
func main() {
    var factory GUIFactory

    // use the Windows factory
    factory = &WindowsFactory{}
    button := factory.CreateButton()
    textBox := factory.CreateTextBox()
    fmt.Println(button.Render())
    fmt.Println(textBox.Render())

    // use the macOS factory
    factory = &MacOSFactory{}
    button = factory.CreateButton()
    textBox = factory.CreateTextBox()
    fmt.Println(button.Render())
    fmt.Println(textBox.Render())

    // use the Linux factory
    factory = &LinuxFactory{}
    button = factory.CreateButton()
    textBox = factory.CreateTextBox()
    fmt.Println(button.Render())
    fmt.Println(textBox.Render())
}
```

#### Use cases
- When you need to create a family of related or interdependent objects.
- When the system needs to be independent of how its products are created and composed.
- When you need to provide a library of product classes and expose only their interfaces rather than their implementations.

#### Implementation
1. Create the abstract product interface, defining the product's common behavior.
2. Create the concrete product classes, implementing the abstract product interface.
3. Create the abstract factory interface, declaring the factory methods that create product objects.
4. Create the concrete factory classes, implementing the abstract factory interface and responsible for instantiating concrete product objects.

#### Pros and cons
**Pros**:
- Separates the creation of concrete classes, making the code easier to maintain and extend.
- Follows the Single Responsibility Principle: factory classes only handle object creation.
- Follows the Open/Closed Principle: the system can be extended by adding new concrete factories and concrete products without modifying existing code.

**Cons**:
- Every new product family requires a corresponding concrete factory class, which adds code.

#### Relationship to other patterns
- **Factory Method Pattern**: the abstract factory pattern is usually used together with the factory method pattern; concrete factory classes can use factory methods to create concrete product objects.
- **Singleton Pattern**: concrete factory classes can use the singleton pattern to ensure each concrete factory has only one instance.
- **Dependency Injection**: the abstract factory pattern can be used together with dependency injection to inject concrete factory objects into client code.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)

## Sibling pages

- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Bridge](/dp/Bridge.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Bridge](/dp/Bridge.md)
- [Builder](/dp/Builder.md)
- [ChainofResponsibility](/dp/ChainofResponsibility.md)
- [Command](/dp/Command.md)
- [Composite](/dp/Composite.md)
- [Creational](/dp/Creational.md)
- [Decorator](/dp/Decorator.md)
- [DesignPatterns](/dp/DesignPatterns.md)
- [Facade](/dp/Facade.md)
- [FactoryMethod](/dp/FactoryMethod.md)
- [Flyweight](/dp/Flyweight.md)
- [Iterator](/dp/Iterator.md)
- [Mediator](/dp/Mediator.md)
- [Memento](/dp/Memento.md)
- [ObjectPool](/dp/ObjectPool.md)
- [Observer](/dp/Observer.md)
- [Proactor](/dp/Proactor.md)
- [Prototype](/dp/Prototype.md)
- [Proxy](/dp/Proxy.md)
- [Reactor](/dp/Reactor.md)
- [Singleton](/dp/Singleton.md)
- [State](/dp/State.md)
- [Strategy](/dp/Strategy.md)
- [Structural](/dp/Structural.md)
- [TemplateMethod](/dp/TemplateMethod.md)
- [Visitor](/dp/Visitor.md)
