### Facade Pattern

#### Intent
The Facade pattern is a structural design pattern: add a facade class that keeps a subsystem's set of interfaces under its own name, so the client only deals with it and never has to feel its way through the subsystem's modules one by one.

#### Problem
Take a graphics library as an example: it's split into modules for rendering, shape handling, and color handling. Using it directly means the client has to remember how to call every module.

#### Solution
Add a facade interface to the library. The client only calls methods like `DrawColoredCircle` and `DrawColoredRectangle`, and the facade arranges the order internally — create the part, fill the color, then render.

#### Pattern structure
1. **Facade**: provides a high-level interface through which the client can access the subsystem's functionality.
2. **Subsystem**: represents one or more classes containing the subsystem's concrete functionality. The subsystem doesn't know the facade exists; it just handles its own work.

#### Code
Here's the Facade pattern implemented in Go:

```go
package main

import "fmt"

// Subsystem 1 - rendering
type Renderer struct{}

func (r *Renderer) RenderShape(shape string) {
    fmt.Println("渲染形状:", shape)
}

// Subsystem 2 - shape handling
type ShapeMaker struct{}

func (s *ShapeMaker) CreateCircle() string {
    return "圆形"
}

func (s *ShapeMaker) CreateRectangle() string {
    return "矩形"
}

// Subsystem 3 - color handling
type ColorFiller struct{}

func (c *ColorFiller) FillColor(shape, color string) {
    fmt.Println("为", shape, "填充颜色:", color)
}

// Facade
type GraphicFacade struct {
    renderer   *Renderer
    shapeMaker *ShapeMaker
    colorFiller *ColorFiller
}

func NewGraphicFacade() *GraphicFacade {
    return &GraphicFacade{
        renderer:   &Renderer{},
        shapeMaker: &ShapeMaker{},
        colorFiller: &ColorFiller{},
    }
}

func (g *GraphicFacade) DrawColoredCircle(color string) {
    shape := g.shapeMaker.CreateCircle()
    g.colorFiller.FillColor(shape, color)
    g.renderer.RenderShape(shape)
}

func (g *GraphicFacade) DrawColoredRectangle(color string) {
    shape := g.shapeMaker.CreateRectangle()
    g.colorFiller.FillColor(shape, color)
    g.renderer.RenderShape(shape)
}

func main() {
    graphic := NewGraphicFacade()

    fmt.Println("绘制红色圆形:")
    graphic.DrawColoredCircle("红色")

    fmt.Println("绘制蓝色矩形:")
    graphic.DrawColoredRectangle("蓝色")
}
```

#### Use cases
- When you need to provide a simple interface for a complex subsystem.
- When you need to reduce the coupling between a subsystem and its client.
- When you need to organize the different parts of a subsystem into a single high-level interface.

#### Implementation
1. Create the subsystem classes, containing the subsystem's concrete functionality.
2. Create the facade class, which holds instances of the subsystem classes.
3. In the facade class, provide a simplified interface that calls the subsystem classes' functionality.
4. The client interacts with the subsystem through the facade class rather than using the subsystem classes directly.

#### Pros and cons
**Pros**:
- The client only knows a handful of facade methods, so swapping the subsystem's implementation doesn't force changes on the caller.
- The call order is collected in one place, the facade, so the client has to memorize half the flow.

**Cons**:
- A poorly implemented facade class can grow bloated and become a god class.
- It adds an extra layer, which may come with performance overhead.

#### Relations to other patterns
- **Adapter Pattern**: the Adapter pattern converts one interface into another, while the Facade pattern simplifies how a subsystem is used by providing it a unified interface.
- **Proxy Pattern**: the Proxy pattern controls access to an object, while the Facade pattern provides a simple interface for a subsystem.
- **Abstract Factory Pattern**: the Abstract Factory pattern can be combined with the Facade pattern to give the client a high-level interface for creating subsystem objects.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [DesignPatterns](/dp/DesignPatterns.md)
- [FactoryMethod](/dp/FactoryMethod.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [DesignPatterns](/dp/DesignPatterns.md)
- [FactoryMethod](/dp/FactoryMethod.md)
