### Behavioral patterns

Behavioral patterns concern how objects distribute responsibilities, organizing the control flow through message passing. The goal is a clearer division of responsibilities and a system that is easier to maintain. Here are the concepts and applicable ranges of eleven common behavioral patterns:

1. **Chain of Responsibility Pattern**:
   - **Concept**: Pass a request along a chain of handlers until one of them handles it.
   - **Applicable range**: Scenarios where multiple objects can handle a request but the handler is not determined.

2. **Command Pattern**:
   - **Concept**: Encapsulate a request as an object, so that users can be parameterized with different requests.
   - **Applicable range**: Scenarios where you need to encapsulate a request as an object to support undoable operations.

3. **Interpreter Pattern**:
   - **Concept**: Define a grammar for a given language, and build an interpreter to interpret sentences in the language.
   - **Applicable range**: Scenarios where you need to interpret and execute a specific language.

4. **Iterator Pattern**:
   - **Concept**: Provide a way to access the elements of an aggregate object sequentially without exposing its internal representation.
   - **Applicable range**: Scenarios where you need to access an aggregate object sequentially.

5. **Mediator Pattern**:
   - **Concept**: Encapsulate the interactions of a series of objects in a single mediator object, so that these objects do not need to refer to each other explicitly.
   - **Applicable range**: Scenarios where objects have complex interactions and you want to simplify the dependencies through a mediator.

6. **Memento Pattern**:
   - **Concept**: Without breaking encapsulation, capture the internal state of an object and save that state outside the object, so the object can be restored later.
   - **Applicable range**: Scenarios where you need to save and restore the state of an object.

7. **Observer Pattern**:
   - **Concept**: Define a one-to-many dependency between objects, so that whenever one object changes state, all of its dependents are notified and update themselves automatically.
   - **Applicable range**: Scenarios where a change of state in one object needs to notify other objects.

8. **State Pattern**:
   - **Concept**: Allow an object to change its behavior when its internal state changes.
   - **Applicable range**: Scenarios where an object exhibits different behavior in different states.

9. **Strategy Pattern**:
   - **Concept**: Define a family of algorithms, encapsulate each one, and make them interchangeable.
   - **Applicable range**: Scenarios where you need to select an algorithm dynamically.

10. **Template Method Pattern**:
    - **Concept**: Define the skeleton of an algorithm in an operation, deferring some steps to subclasses. This lets subclasses redefine certain steps of an algorithm without changing its structure.
    - **Applicable range**: Scenarios where the skeleton of an algorithm is fixed but some steps need to be implemented in subclasses.

11. **Visitor Pattern**:
    - **Concept**: Represent an operation to be performed on the elements of an object structure, allowing you to define new operations on those elements without changing the classes of the elements.
    - **Applicable range**: Scenarios where you need to perform operations on the elements of an object structure without changing the definitions of those element classes.

## References

- [GoF "Design Patterns" Overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru Design Patterns Catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)

## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Bridge](/dp/Bridge.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
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
