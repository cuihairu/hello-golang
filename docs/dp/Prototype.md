### Prototype Pattern

#### Intent
The Prototype Pattern is a creational design pattern that creates new objects by copying existing ones instead of instantiating classes. It lets an object copy itself, ensuring each object has its own copy.

#### Problem
In the real world, consider a game development scenario where the game has various monsters (for example zombies, dragons, giants, and so on). Each monster has different attributes and behaviors. Creating these monsters by instantiating classes in the main application would make the code long and hard to maintain.

#### Solution
With the Prototype Pattern, we can define a monster prototype interface and several concrete monster classes, then create new monsters by copying existing monster objects — avoiding repeated instantiation of the same monster type.

#### Structure
1. **Prototype**: defines the method for copying itself.
2. **ConcretePrototype**: implements the prototype interface and provides the concrete copy method.
3. **Client**: creates new objects by calling the prototype object's copy method.

#### Code
Here is a Prototype Pattern example implemented in Go:

```go
package main

import "fmt"

// monster prototype interface
type MonsterPrototype interface {
    Clone() MonsterPrototype
    GetType() string
}

// Zombie struct, a concrete prototype
type Zombie struct {
    Type string
}

func (z *Zombie) Clone() MonsterPrototype {
    return &Zombie{Type: z.Type}
}

func (z *Zombie) GetType() string {
    return z.Type
}

// Dragon struct, a concrete prototype
type Dragon struct {
    Type string
}

func (d *Dragon) Clone() MonsterPrototype {
    return &Dragon{Type: d.Type}
}

func (d *Dragon) GetType() string {
    return d.Type
}

// client code
func main() {
    // create the concrete prototype objects
    zombiePrototype := &Zombie{Type: "Zombie"}
    dragonPrototype := &Dragon{Type: "Dragon"}

    // create new objects via the prototypes
    newZombie := zombiePrototype.Clone()
    newDragon := dragonPrototype.Clone()

    fmt.Println("Original Zombie Type:", zombiePrototype.GetType())
    fmt.Println("Cloned Zombie Type:", newZombie.GetType())
    fmt.Println("Original Dragon Type:", dragonPrototype.GetType())
    fmt.Println("Cloned Dragon Type:", newDragon.GetType())
}
```

#### Applicable scenarios
- You need to create copies of an object rather than new instances.
- The system has many similar objects and needs to avoid repeatedly creating the same ones.
- You need to add or remove product classes dynamically at runtime.

#### Implementation
The implementation has three steps: first define a prototype interface with `Clone()`, then have each concrete prototype implement it; the client holds a prototype object and calls `Clone()` repeatedly to get new objects.

#### Pros and cons
**Pros**:
- Avoids repeatedly initializing identical objects; creation is cheap.
- Product classes can be added or removed dynamically at runtime.

**Cons**:
- Every concrete prototype class needs a clone method, which adds code.
- If the object's internal structure is complex, the cloning process can get tedious.

#### Relationship to other patterns
- **Factory Method Pattern**: the Prototype Pattern can be combined with the Factory Method Pattern — the factory method picks the right prototype object, and the prototype pattern then copies it.
- **Builder Pattern**: the Builder Pattern focuses on constructing complex objects step by step, while the Prototype Pattern focuses on copying existing objects.
- **Singleton Pattern**: the Singleton Pattern ensures a class has only one instance, while the Prototype Pattern creates new objects by copying an existing instance.

## References

- [GoF "Design Patterns" Overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru Design Patterns Catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Proactor](/dp/Proactor.md)
- [Proxy](/dp/Proxy.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Proactor](/dp/Proactor.md)
- [Proxy](/dp/Proxy.md)
