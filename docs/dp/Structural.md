### Structural patterns

Structural patterns concern how objects are composed, using inheritance and interfaces to build larger structures. The goal is a system that is easier to maintain. Here are the concepts and applicable ranges of seven common structural patterns:

1. **Adapter Pattern**:
   - **Concept**: Convert the interface of a class into another interface clients expect, so that classes with incompatible interfaces can work together.
   - **Applicable range**: Scenarios where you want to use an existing class but its interface does not fit your needs.

2. **Bridge Pattern**:
   - **Concept**: Decouple an abstraction from its implementation, so that the two can vary independently.
   - **Applicable range**: Scenarios where you want to decouple the abstraction from its implementation and let them vary independently.

3. **Composite Pattern**:
   - **Concept**: Compose objects into a tree structure to represent a "part-whole" hierarchy, so that clients can treat individual objects and compositions of objects uniformly.
   - **Applicable range**: Scenarios where you need to represent a part-whole hierarchy of objects and want clients to treat individual objects and composites uniformly.

4. **Decorator Pattern**:
   - **Concept**: Dynamically add responsibilities to an object. Compared to subclassing, the Decorator pattern is more flexible for extending functionality.
   - **Applicable range**: Scenarios where you want to add responsibilities to a single object dynamically and transparently, without affecting other objects.

5. **Facade Pattern**:
   - **Concept**: Provide a unified interface to a set of interfaces in a subsystem, making the subsystem easier to use.
   - **Applicable range**: Scenarios where you want to provide a simple interface for a complex subsystem.

6. **Flyweight Pattern**:
   - **Concept**: Use sharing to support a large number of fine-grained objects efficiently.
   - **Applicable range**: Scenarios where you need to create many similar objects that would consume a large amount of memory.

7. **Proxy Pattern**:
   - **Concept**: Provide a surrogate for another object to control access to that object.
   - **Applicable range**: Scenarios where you need to control access to an object, or add extra operations when accessing it.

## References

- [GoF "Design Patterns" Overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru Design Patterns Catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Strategy](/dp/Strategy.md)
- [TemplateMethod](/dp/TemplateMethod.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Strategy](/dp/Strategy.md)
- [TemplateMethod](/dp/TemplateMethod.md)
