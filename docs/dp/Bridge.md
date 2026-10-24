### Bridge Pattern

#### Intent
The Bridge pattern is a structural design pattern that separates the abstraction from the implementation, so the two can vary and extend independently.

#### Problem
In the real world, consider a graphics drawing system that has to draw different kinds of shapes (such as circles and rectangles), and those shapes can have different colors. If you hardcode color information into every shape class, the number of classes grows quickly and becomes hard to maintain and extend.

#### Solution
Keep shapes on the abstraction side and colors on the implementation side, and connect the two through composition: a shape holds a reference to a color interface, so adding a new shape does not touch the colors and adding a new color does not touch the shapes.

#### Structure
1. **Abstraction**: defines the abstraction interface and maintains a reference to the implementation side.
2. **Refined Abstraction**: extends the abstraction interface.
3. **Implementor**: defines the implementation interface; this interface is not necessarily consistent with the abstraction interface. Typically it only provides basic operations, and those operations are components of the more complex operations in the abstraction interface.
4. **Concrete Implementor**: implements the implementation interface.

#### Code

```go
package main

import "fmt"

// Implementation interface - color
type Color interface {
    Fill() string
}

// Concrete implementor - red
type Red struct{}

func (r *Red) Fill() string {
    return "红色"
}

// Concrete implementor - blue
type Blue struct{}

func (b *Blue) Fill() string {
    return "蓝色"
}

// Abstraction - shape
type Shape interface {
    Draw() string
}

// Refined abstraction - circle
type Circle struct {
    color Color
}

func NewCircle(color Color) *Circle {
    return &Circle{color: color}
}

func (c *Circle) Draw() string {
    return fmt.Sprintf("绘制一个%s的圆形", c.color.Fill())
}

// Refined abstraction - rectangle
type Rectangle struct {
    color Color
}

func NewRectangle(color Color) *Rectangle {
    return &Rectangle{color: color}
}

func (r *Rectangle) Draw() string {
    return fmt.Sprintf("绘制一个%s的矩形", r.color.Fill())
}

func main() {
    red := &Red{}
    blue := &Blue{}

    redCircle := NewCircle(red)
    blueCircle := NewCircle(blue)

    redRectangle := NewRectangle(red)
    blueRectangle := NewRectangle(blue)

    fmt.Println(redCircle.Draw())
    fmt.Println(blueCircle.Draw())
    fmt.Println(redRectangle.Draw())
    fmt.Println(blueRectangle.Draw())
}
```

#### Use cases
- You need more flexibility between the abstraction and the implementation.
- You need to avoid creating a static coupling between the abstraction and the implementation.
- You want to extend class functionality through composition rather than inheritance.

#### Implementation
1. Define the abstraction interface and the implementation interface.
2. Create the concrete implementor classes, implementing the implementation interface.
3. Create the refined abstraction classes, implementing the abstraction interface and holding a reference to the implementation interface.
4. In the refined abstraction's methods, call the concrete implementor's methods through the implementation interface reference.

#### Pros and cons
**Pros**:
- Separates the abstraction from the implementation, decoupling the interface from the implementation side.
- Improves the system's extensibility: the abstraction side and the implementation side can be extended independently.
- Follows the Open/Closed Principle: the system can be extended by introducing new abstraction and implementation sides without affecting existing code.

**Cons**:
- Adds complexity to the system and requires extra development work.
- The abstraction and implementation interfaces must be designed correctly, which can be a design challenge.

#### Relationship to other patterns
- **Adapter Pattern**: the Adapter pattern converts one interface into another so incompatible interfaces can work together. The Bridge pattern separates the abstraction from the implementation so they can vary independently.
- **Decorator Pattern**: the Decorator pattern enhances an object's functionality by dynamically adding responsibilities to it, while the Bridge pattern makes the abstraction and implementation vary independently by separating them.
- **Composite Pattern**: the Composite pattern composes objects into a tree structure to represent a "part-whole" hierarchy. The Bridge pattern separates the abstraction from the implementation so they can vary independently.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)

## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Builder](/dp/Builder.md)
