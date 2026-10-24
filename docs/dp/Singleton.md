### Singleton Pattern

#### Intent
The Singleton pattern is a creational design pattern: a class is allowed to have only one instance, and it exposes a fixed entry point for getting that instance. Globally unique objects such as configuration and logging commonly use it.

#### Problem
Consider a logging system in the real world. Every module in the system needs to record logs. If each module creates its own logger, it wastes resources and leads to inconsistent logs.

#### Solution
With the Singleton pattern we can ensure the logging system has only one instance. All modules share that instance, which keeps resource use reasonable and logs consistent.

#### Pattern structure
1. **Singleton**: holds a private static variable to store the single instance, and provides a public static method to get that instance.
2. **Client**: accesses the single instance through the Singleton class's public static method.

#### Eager implementation
The eager Singleton creates its instance when the class loads. It is thread-safe, but it can waste resources unnecessarily.

```go
package main

import "fmt"

// Singleton class - eager initialization
type Singleton struct{}

var instance = &Singleton{}

// Public method to get the instance
func GetInstance() *Singleton {
    return instance
}

func main() {
    singleton1 := GetInstance()
    singleton2 := GetInstance()

    if singleton1 == singleton2 {
        fmt.Println("饿汉式: singleton1 和 singleton2 是相同的实例")
    } else {
        fmt.Println("饿汉式: singleton1 和 singleton2 是不同的实例")
    }
}
```

#### Lazy implementation
The lazy Singleton creates its instance on first use. Initialization is deferred and resources are saved, but you have to think about thread safety.

```go
package main

import (
    "fmt"
    "sync"
)

// Singleton class - lazy initialization
type Singleton struct{}

var instance *Singleton
var mu sync.Mutex

// Public method to get the instance
func GetInstance() *Singleton {
    if instance == nil {
        mu.Lock()
        defer mu.Unlock()
        if instance == nil {
            instance = &Singleton{}
        }
    }
    return instance
}

func main() {
    singleton1 := GetInstance()
    singleton2 := GetInstance()

    if singleton1 == singleton2 {
        fmt.Println("饱汉式: singleton1 和 singleton2 是相同的实例")
    } else {
        fmt.Println("饱汉式: singleton1 和 singleton2 是不同的实例")
    }
}
```

#### Applicable scenarios
- When you need a globally unique object, such as configuration management or logging.
- When you need to control access to a resource, to avoid the waste or inconsistency that multiple instances cause.

#### Implementation
1. Create a class with a private static variable that stores the single instance.
2. Provide a public static method to get that instance.
3. Make sure the class's constructor is private so external code cannot create new instances.

#### Pros and cons
**Pros**:
- Ensures a class has only one instance, saving resources.
- Provides a global access point, making it easy to control and manage.

**Cons**:
- The eager version creates the instance when the class loads, which can waste resources unnecessarily.
- The lazy version has to handle thread safety, which adds implementation complexity.

#### Relationship to other patterns
- **Factory Method Pattern**: the Factory Method pattern uses factory classes to create objects, while the Singleton pattern ensures the factory class itself has only one instance.
- **Prototype Pattern**: the Prototype pattern creates new objects by copying an existing one, while the Singleton pattern ensures a class has only one instance.

### Extending the Singleton pattern
When one instance is not enough (for example, a database connection pool), use the Multiton pattern: each key maps to one unique instance.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Reactor](/dp/Reactor.md)
- [State](/dp/State.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Reactor](/dp/Reactor.md)
- [State](/dp/State.md)
