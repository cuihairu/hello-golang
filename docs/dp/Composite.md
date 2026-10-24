### Composite Pattern

#### Intent
The Composite pattern is a structural design pattern that composes objects into a tree structure to represent a "part-whole" hierarchy, so the client never has to tell single objects from composite objects — one and the same set of calls works for both.

#### Problem
In the real world, consider a graphics editor. A graphic can be a simple shape (a line, a circle, a rectangle) or a complex graphic made of several simple shapes. Without the Composite pattern, the client code has to handle simple shapes and complex graphics separately, which adds to the complexity of the code.

#### Solution
The Composite pattern defines one unified interface; both simple shapes and complex graphics implement it, and the client only calls that interface.

#### Pattern structure
1. **Component**: defines the unified interface shared by composite objects and leaf objects.
2. **Leaf**: a basic element of the composition that contains no child objects.
3. **Composite**: holds child components; it represents an object that can contain other leaves or composites.
4. **Client**: interacts with the objects in the composition structure through the component interface.

#### Code
Here's an example of the Composite pattern implemented in Go:

```go
package main

import "fmt"

// Component interface
type Graphic interface {
    Draw()
}

// Leaf - circle
type Circle struct{}

func (c *Circle) Draw() {
    fmt.Println("绘制一个圆形")
}

// Leaf - rectangle
type Rectangle struct{}

func (r *Rectangle) Draw() {
    fmt.Println("绘制一个矩形")
}

// Composite - complex graphic
type CompositeGraphic struct {
    graphics []Graphic
}

func (cg *CompositeGraphic) Add(graphic Graphic) {
    cg.graphics = append(cg.graphics, graphic)
}

func (cg *CompositeGraphic) Remove(graphic Graphic) {
    for i, g := range cg.graphics {
        if g == graphic {
            cg.graphics = append(cg.graphics[:i], cg.graphics[i+1:]...)
            break
        }
    }
}

func (cg *CompositeGraphic) Draw() {
    for _, graphic := range cg.graphics {
        graphic.Draw()
    }
}

func main() {
    circle1 := &Circle{}
    circle2 := &Circle{}
    rectangle := &Rectangle{}

    // create a composite graphic and add the basic shapes
    composite := &CompositeGraphic{}
    composite.Add(circle1)
    composite.Add(circle2)
    composite.Add(rectangle)

    // draw the composite graphic
    fmt.Println("绘制组合图形:")
    composite.Draw()

    // remove one basic shape, then draw the composite graphic again
    composite.Remove(circle1)
    fmt.Println("移除一个圆形后，绘制组合图形:")
    composite.Draw()
}
```

#### Use cases
- When you need to represent a part-whole hierarchy of objects.
- When you want the client to handle single objects and composite objects in the same way.

#### Implementation
The implementation goes in four steps: define the component interface first and declare the unified operations; then write the leaf classes that implement that interface; next write the composite class, which holds a set of child components and implements the add and remove methods; and throughout, the client only faces the component interface.

#### Pros and cons
**Pros**:
- The hierarchy is clear, so adding a new leaf or composite object doesn't require changing the client.
- Single objects and composite objects share the same calls, so the client code is shorter.

**Cons**:
- The design is somewhat complex and may need more classes and interfaces.
- Overusing the Composite pattern can make the system hierarchy too complex.

#### Relations to other patterns
- **Decorator Pattern**: the Decorator pattern adds responsibilities to a single object dynamically, while the Composite pattern organizes objects into a tree.
- **Flyweight Pattern**: Flyweight saves memory by sharing objects, which is a different problem from the one Composite solves.
- **Iterator Pattern**: the Composite pattern can be used together with the Iterator pattern to traverse every object in a composite structure.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Command](/dp/Command.md)
- [Creational](/dp/Creational.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Command](/dp/Command.md)
- [Creational](/dp/Creational.md)
