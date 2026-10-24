### Memento Pattern

#### Intent
The Memento pattern is a behavioral design pattern: it stores an object's state in a separate object, so the state can be retrieved and restored later without exposing the internal state. It is usually used to implement undo and redo.

#### Problem
In the real world, consider a text editor where users may need to undo or redo some operations while editing. If the object's state is modified directly every time, undo and restore operations can become complicated. The Memento pattern can simplify these operations by saving and restoring object state.

#### Solution
With the Memento pattern, we can define a memento class to save an object's state, and define an originator class to create and restore mementos. The originator holds the state to be saved and restored, while the memento class only stores that state and does not allow direct modification. A caretaker class (such as a memento manager) is used to store and manage memento instances.

#### Pattern structure
1. **Originator**: responsible for creating a memento object to save the current state, and for restoring state using the memento object.
2. **Memento**: stores the internal state of the originator object. The memento class can only be accessed by the originator and does not allow direct modification.
3. **Caretaker**: responsible for saving and restoring memento objects, but not allowed to access the memento's internal state.

#### Code

```go
package main

import "fmt"

// Originator - text editor
type Editor struct {
    text string
}

func (e *Editor) SetText(text string) {
    e.text = text
}

func (e *Editor) CreateMemento() *Memento {
    return &Memento{state: e.text}
}

func (e *Editor) Restore(memento *Memento) {
    e.text = memento.state
}

func (e *Editor) GetText() string {
    return e.text
}

// Memento - stores the state
type Memento struct {
    state string
}

// Caretaker - memento manager
type Caretaker struct {
    mementos []*Memento
}

func (c *Caretaker) AddMemento(memento *Memento) {
    c.mementos = append(c.mementos, memento)
}

func (c *Caretaker) GetMemento(index int) *Memento {
    if index >= 0 && index < len(c.mementos) {
        return c.mementos[index]
    }
    return nil
}

func main() {
    editor := &Editor{}
    caretaker := &Caretaker{}

    // set the text
    editor.SetText("版本 1")
    caretaker.AddMemento(editor.CreateMemento())

    editor.SetText("版本 2")
    caretaker.AddMemento(editor.CreateMemento())

    editor.SetText("版本 3")
    caretaker.AddMemento(editor.CreateMemento())

    // restore to version 1
    editor.Restore(caretaker.GetMemento(0))
    fmt.Println("恢复后的文本:", editor.GetText())

    // restore to version 2
    editor.Restore(caretaker.GetMemento(1))
    fmt.Println("恢复后的文本:", editor.GetText())
}
```

#### Applicable scenarios
- You need to implement undo and redo, for example in a text editor or a graphics editor.
- You need to save historical states and restore to any of them at any time, without exposing the object's internal state.

#### Implementation
1. Define the originator class, which holds the state to be saved and provides methods for creating and restoring mementos.
2. Define the memento class, which stores the internal state of the originator object and allows only the originator to access it.
3. Define the caretaker class, which is responsible for saving and restoring memento objects and provides a method for retrieving mementos.
4. Client code creates the originator, memento, and caretaker objects and performs the save and restore operations.

#### Pros and cons
**Pros**:
- Enables undo and restore, making object state management more flexible.
- Does not expose the object's internal state, which protects its encapsulation.
- Allows saving multiple states of an object and restoring to any of them as needed.

**Cons**:
- When an object's state is large, mementos take up a lot of memory, and the problem gets worse as their number grows.
- Storing mementos and managing their lifecycle is on you, which adds a bit of complexity.

#### Relationship to other patterns
- **Memento Pattern and Command Pattern**: Command encapsulates a request's operations and Memento stores state; the Command pattern uses Memento to implement undo and redo.
- **Memento Pattern and State Pattern**: the State pattern switches behavior based on the current state, while Memento is used to store historical records of state.
- **Memento Pattern and Observer Pattern**: Observer notifies observers when state changes, while Memento keeps the restorable copy of the state; the two can work together to implement undo.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [Mediator](/dp/Mediator.md)
- [ObjectPool](/dp/ObjectPool.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Mediator](/dp/Mediator.md)
- [ObjectPool](/dp/ObjectPool.md)
