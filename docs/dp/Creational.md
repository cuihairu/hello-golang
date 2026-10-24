### Creational patterns

Creational patterns concern the creation process of objects, separating creation from usage. Here are the concepts and applicable ranges of five common patterns:

1. **Singleton Pattern**:
   - **Concept**: Ensure that a class has only one instance, and provide a global point of access to it.
   - **Applicable range**: Scenarios where you need to control the number of instances, such as configuration objects or logging objects.

2. **Factory Method Pattern**:
   - **Concept**: Define an interface for creating objects, but let subclasses decide which class to instantiate. The factory method lets the instantiation of a class be deferred to subclasses.
   - **Applicable range**: Scenarios where you need to separate the creation of an object from its usage, and the instantiation process is complex.

3. **Abstract Factory Pattern**:
   - **Concept**: Provide an interface for creating families of related or dependent objects without specifying the concrete classes.
   - **Applicable range**: Scenarios where you need to create a family of related or dependent objects, such as GUI toolkits or database-related objects.

4. **Builder Pattern**:
   - **Concept**: Separate the construction of a complex object from its representation, so that the same construction process can create different representations.
   - **Applicable range**: Scenarios where you need to create complex objects, the construction process is stable, but the representation can vary flexibly.

5. **Prototype Pattern**:
   - **Concept**: Create new objects by cloning an existing object, avoiding the overhead of creating an object from scratch.
   - **Applicable range**: Scenarios where you need to create many similar objects and want to avoid creating objects directly with the `new` keyword.

## References

- [GoF "Design Patterns" Overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru Design Patterns Catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Composite](/dp/Composite.md)
- [Decorator](/dp/Decorator.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Composite](/dp/Composite.md)
- [Decorator](/dp/Decorator.md)
