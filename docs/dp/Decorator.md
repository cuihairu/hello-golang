### Decorator Pattern

#### Intent
The Decorator pattern is a structural design pattern: wrap an object in a decorator class to add responsibilities dynamically without changing the original class.

#### Problem
In the real world, consider a simple text editor. Its most basic function is displaying text, but sometimes you need to apply different effects to the text, such as bold, italic, or underline. Adding these features directly to the text class increases the class's complexity and makes it hard to maintain and extend.

#### Solution
The approach is to write one decorator class per effect and then wrap them around the text object in layers as needed.

#### Pattern structure
1. **Component**: defines the interface of the objects that will have responsibilities added dynamically.
2. **Concrete Component**: implements the component interface; it's the object to be decorated.
3. **Decorator**: implements the component interface, holds a component object, and extends its functionality on that basis.
4. **Concrete Decorator**: inherits from the decorator and implements a specific decoration.

#### Code
Here's the Decorator pattern in Go:

```go
package main

import "fmt"

// Component interface
type Component interface {
    Operation() string
}

// Concrete component - text
type Text struct {
    content string
}

func (t *Text) Operation() string {
    return t.content
}

// Decorator base class
type Decorator struct {
    component Component
}

func (d *Decorator) Operation() string {
    if d.component != nil {
        return d.component.Operation()
    }
    return ""
}

// Concrete decorator - bold
type BoldDecorator struct {
    Decorator
}

func (b *BoldDecorator) Operation() string {
    return "<b>" + b.Decorator.Operation() + "</b>"
}

// Concrete decorator - italic
type ItalicDecorator struct {
    Decorator
}

func (i *ItalicDecorator) Operation() string {
    return "<i>" + i.Decorator.Operation() + "</i>"
}

// Concrete decorator - underline
type UnderlineDecorator struct {
    Decorator
}

func (u *UnderlineDecorator) Operation() string {
    return "<u>" + u.Decorator.Operation() + "</u>"
}

func main() {
    text := &Text{content: "Hello, World!"}

    boldText := &BoldDecorator{Decorator{component: text}}
    italicBoldText := &ItalicDecorator{Decorator{component: boldText}}
    underlinedItalicBoldText := &UnderlineDecorator{Decorator{component: italicBoldText}}

    fmt.Println("原始文本:", text.Operation())
    fmt.Println("加粗文本:", boldText.Operation())
    fmt.Println("加粗斜体文本:", italicBoldText.Operation())
    fmt.Println("加粗斜体下划线文本:", underlinedItalicBoldText.Operation())
}
```

#### Use cases
- When you need to add responsibilities to an object dynamically without changing the original class.
- When you need to add the same responsibilities to a group of objects, and those responsibilities can be combined dynamically.

#### Implementation
1. Define the component interface, declaring the interface of the objects that will have responsibilities added dynamically.
2. Create the concrete component, implementing the component interface.
3. Create the decorator base class, implementing the component interface and holding a component object.
4. Create concrete decorators, inheriting from the decorator base class and implementing specific decorations.
5. In the client code, use the decorator classes to add responsibilities to the component object dynamically.

#### Pros and cons
**Pros**:
- Adds new responsibilities to an object dynamically without affecting other objects.
- Combining multiple decorators can build up complex functionality.
- Follows the open-closed principle; you can extend the system by adding new decorator classes without affecting existing code.

**Cons**:
- Can lead to a large number of small classes, increasing system complexity.
- Combining multiple decorators can make debugging harder.

#### Relations to other patterns
- **Proxy Pattern**: structurally similar to the Decorator, but a proxy controls access while a decorator adds responsibilities.
- **Adapter Pattern**: an adapter converts one interface into another; a decorator doesn't change the interface, it only adds responsibilities.
- **Composite Pattern**: Composite assembles objects into a tree structure to represent a "part-whole", while a Decorator wraps a single object in layers.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Creational](/dp/Creational.md)
- [DesignPatterns](/dp/DesignPatterns.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Creational](/dp/Creational.md)
- [DesignPatterns](/dp/DesignPatterns.md)
