### Object-oriented software design: the SOLID principles

#### 1. Single Responsibility Principle (SRP)

Description: A class or module should have only one responsibility. Put simply, a module, class, or method shouldn't take on too many tasks.

As a rule, when you design a class you shouldn't make it a big catch-all. Design small-grained classes with a single function. If a class contains two or more unrelated responsibilities, it violates the Single Responsibility Principle and should be split into several classes that each do one thing at finer granularity.

In real software work you don't have to follow the principle strictly. It's fine to design a coarse-grained class first and refactor later as the business grows.

In practice, use the following guidelines to guide refactoring or design:

- When a class depends on too many other classes, or the direct dependency graph gets overly complex — in other words, when it no longer fits the high-cohesion, low-coupling idea — consider splitting the code.
- When a class name has little or no relation to what it actually does, split it at a finer grain and move the unrelated functionality out on its own.
- When a class has too many functions and readability or maintainability suffers, split at the method level.

#### 2. Open/Closed Principle (OCP)

Description: Software entities (modules, classes, methods, etc.) should be open for extension but closed for modification. Put plainly, adding a feature should mean extending existing code, not modifying it.

The point of OCP is extensibility, while avoiding the risk that changes to existing code bring to the software. Extensibility assumes you already know the future extension points. So how do you find all of them in real development? A few approaches:

- For business-driven systems, you need a solid grasp of the requirements before you can locate the extension points. If there are too many unknowns or requirements churn too fast, focus your design on the spots that are fairly certain, likely to be extended soon, and where adding an extension point clearly improves code stability and development speed.
- For general-purpose technical work — frameworks, components, libraries — you need to think about how users will consume the framework, what extension points to leave for feature upgrades, and how to keep versions compatible.
- Even with a good understanding of the system's business or technical framework, you don't have to design every extension point. Leaving an extension point everywhere something might change in the future only adds complexity, and the implementation effort is no small thing. Weigh development cost, blast radius, and actual benefit (including time and staffing cost).

#### 3. Liskov Substitution Principle (LSP)

Description: A subclass object can be substituted for a superclass object anywhere in the program, and the original program's behavior stays correct and unchanged.

Polymorphism in OOP can be used to achieve this. Polymorphism and LSP share a similar goal, but they come from different angles: polymorphism is a feature of OOP, while Liskov substitution is a principle that guides how to design a subclass in an inheritance hierarchy. A subclass must guarantee that substituting it for the superclass doesn't change the original program's logic or break its correctness.

Concretely, when designing a subclass, follow the superclass's behavioral contract. The superclass defines what a method does; a subclass may change the internal implementation, but not the method's original contract — the interface, the functionality the method declaration promises, the conventions around argument values, return values, and exceptions, and even any special notes listed in the comments.

#### 4. Interface Segregation Principle (ISP)

Description: Clients shouldn't be forced to depend on interfaces they don't use.

Here are a few ways to apply it:

1. For interfaces, if one carries definitions unrelated to its purpose, it violates ISP. Strip the unrelated parts off. Slim down fat, miscellaneous interfaces.
2. For shared functionality, break it into fine-grained points and add them as needed, rather than defining one big catch-all interface that subclasses are forced to implement.

#### 5. Dependency Inversion Principle (DIP)

Description: High-level modules shouldn't depend on low-level modules. Both should depend on abstractions. Moreover, abstractions shouldn't depend on concrete implementation details — concrete details depend on abstractions.

In this context, a high-level module is a caller and a low-level module is a callee. So callers shouldn't depend on concrete implementations but on abstractions. Take Spring's `*Aware` callbacks: the framework depends on the concrete implementation of an `Aware` interface to gain functionality, and the implementation gains functionality by implementing that interface. The implementation and the framework aren't directly coupled.

#### 6. Law of Demeter

Also known as the Least Knowledge Principle, it says an object should know as little as possible about other objects. Put simply, only talk to your immediate friends.

First, what counts as an immediate friend? Every object has coupling relationships with others; whenever two objects are coupled, we call them friends. Coupling takes many forms — dependency, association, composition, aggregation, and so on. A class counts as an immediate friend when it appears as a member variable, a method parameter, or a method return type. A class that appears only as a local variable is not an immediate friend. In other words, avoid surfacing unfamiliar classes as local variables inside a class.

For the depended-upon class, no matter how complex the logic, keep it encapsulated inside the class, expose `public` methods, and leak nothing to the outside.

#### 7. Composite/Aggregate Reuse Principle

The Composite/Aggregate Reuse Principle means using existing objects inside a new one so they become part of it; the new object reuses their functionality by delegating to them.

In OOP design, inheriting from a base class directly breaks encapsulation, because inheritance exposes the base class's implementation details to the subclass; if the base implementation changes, the subclass has to change too; and what's inherited is static, fixed at compile time and unable to change at runtime, so it lacks enough flexibility. That's why the Composite/Aggregate Reuse Principle exists: in real development and design, prefer composition/aggregation over class inheritance.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/zh/dp/AbstractFactory.md)
- [Adapter](/zh/dp/Adapter.md)
- [Behavioral](/zh/dp/Behavioral.md)
- [Decorator](/zh/dp/Decorator.md)
- [Facade](/zh/dp/Facade.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Decorator](/zh/dp/Decorator.md)
- [Facade](/zh/dp/Facade.md)
