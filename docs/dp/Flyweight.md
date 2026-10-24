### Flyweight Pattern

#### Intent
The Flyweight pattern is a structural design pattern that reduces memory usage by sharing objects. It suits managing large numbers of similar objects.

#### Problem
In the real world, consider a graphics editor that has to handle a large number of graphics objects, such as many identical icons. If every graphics object is stored independently, the memory cost becomes very high.

#### Solution
With the Flyweight pattern we can share identical objects, storing only one common shared part and keeping the unique, varying parts in external data. This cuts down object creation and memory usage significantly.

#### Pattern structure
1. **Flyweight**: defines the object's interface and can provide a shared, reusable object.
2. **Concrete Flyweight**: implements the Flyweight interface and defines the object's shared part.
3. **Flyweight Factory**: manages the creation and sharing of flyweight objects, ensuring they are shared and reused.
4. **Unshared Flyweight**: defines the interface for the non-shared part, used to store the object's unique portion.

#### Code

```go
package main

import "fmt"

// Flyweight interface
type Flyweight interface {
    Operation(extrinsicState string)
}

// Concrete Flyweight - icon
type ConcreteFlyweight struct {
    intrinsicState string
}

func (f *ConcreteFlyweight) Operation(extrinsicState string) {
    fmt.Printf("图标状态: %s, 外部状态: %s\n", f.intrinsicState, extrinsicState)
}

// Flyweight factory
type FlyweightFactory struct {
    flyweights map[string]Flyweight
}

func NewFlyweightFactory() *FlyweightFactory {
    return &FlyweightFactory{flyweights: make(map[string]Flyweight)}
}

func (f *FlyweightFactory) GetFlyweight(key string) Flyweight {
    if flyweight, exists := f.flyweights[key]; exists {
        return flyweight
    }
    // create a new flyweight object and store it
    flyweight := &ConcreteFlyweight{intrinsicState: key}
    f.flyweights[key] = flyweight
    return flyweight
}

func main() {
    factory := NewFlyweightFactory()

    // get shared flyweight objects
    flyweight1 := factory.GetFlyweight("图标1")
    flyweight2 := factory.GetFlyweight("图标2")
    flyweight3 := factory.GetFlyweight("图标1") // reuse an existing flyweight object

    // operate on the flyweight objects
    flyweight1.Operation("外部状态1")
    flyweight2.Operation("外部状态2")
    flyweight3.Operation("外部状态3")
}
```

#### Applicable scenarios
- The system has a large number of similar objects and storing each independently costs too much memory.
- You need to separate an object's intrinsic and extrinsic state, and changes to either state should not affect the shared part.

#### Implementation
1. Define the Flyweight interface, declaring operations on the shared part.
2. Create a Concrete Flyweight class that implements the Flyweight interface and defines the shared part.
3. Create a Flyweight Factory class that manages the creation and sharing of flyweight objects.
4. In client code, obtain shared objects through the Flyweight factory and operate on them.

#### Pros and cons
**Pros**:
- Identical objects are stored only once, so memory usage drops.
- The factory reuses objects, eliminating repeated-creation overhead, and can still create dynamically when needed.

**Cons**:
- The sharing and management strategy has to be designed correctly, or reuse won't kick in.
- Coordination between the flyweight factory and flyweight objects adds a layer of complexity.

#### Relationship to other patterns
- **Flyweight Pattern and Decorator Pattern**: Decorator adds responsibilities to objects dynamically, while Flyweight shares objects to reduce memory usage. They can be combined, for example applying a decorator to a flyweight object to enhance its functionality.
- **Flyweight Pattern and Proxy Pattern**: Proxy controls access to an object, while Flyweight shares objects to reduce memory consumption. The two can be combined, for example accessing flyweight objects through a proxy.
- **Flyweight Pattern and Composite Pattern**: Composite combines objects into a tree structure to represent a part-whole hierarchy, while Flyweight reduces the memory usage of large numbers of similar objects. Within Composite you can use Flyweight to manage and share similar leaf objects.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [FactoryMethod](/dp/FactoryMethod.md)
- [Iterator](/dp/Iterator.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [FactoryMethod](/dp/FactoryMethod.md)
- [Iterator](/dp/Iterator.md)
