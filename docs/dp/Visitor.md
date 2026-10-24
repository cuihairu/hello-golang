### Visitor Pattern

#### Intent
The Visitor pattern is a behavioral design pattern: it wraps operations in visitor objects, so you can add new operations to objects without changing their classes. Operations are separated from the object structure, and adding a new operation only touches the visitors.

#### Problem
Consider a complex document structure in the real world, containing different kinds of document elements such as text, images, and tables. If you need to perform different operations on those elements (for example, counting the words in a document or generating HTML), every new operation means modifying the document element classes. By wrapping operations in visitor objects, the Visitor pattern lets us add new operations without changing the document element classes.

#### Solution
With the Visitor pattern we can define a visitor interface that contains a visit method for each kind of element. Then we create concrete visitor classes that implement the visitor interface and define the concrete operation logic. Element classes provide an interface for accepting a visitor and pass themselves to the visitor object. Through the visitor object you can perform operations on element objects without modifying the element classes' code.

#### Pattern structure
1. **Visitor interface**: declares a visit method for each kind of element.
2. **Concrete Visitor**: implements the visitor interface and defines the concrete operation logic.
3. **Element interface**: declares the interface for accepting a visitor.
4. **Concrete Element**: implements the element interface and defines the element's specific behavior.
5. **Object Structure**: holds a collection of element objects and provides the ability to accept a visitor.

#### Code

```go
package main

import "fmt"

// Visitor interface
type Visitor interface {
    VisitTextElement(element *TextElement)
    VisitImageElement(element *ImageElement)
}

// Concrete visitor - word count
type WordCountVisitor struct {
    wordCount int
}

func (v *WordCountVisitor) VisitTextElement(element *TextElement) {
    v.wordCount += len(element.text)
}

func (v *WordCountVisitor) VisitImageElement(element *ImageElement) {
    // Ignore image elements
}

// Concrete visitor - HTML generation
type HTMLVisitor struct {
    html string
}

func (v *HTMLVisitor) VisitTextElement(element *TextElement) {
    v.html += "<p>" + element.text + "</p>"
}

func (v *HTMLVisitor) VisitImageElement(element *ImageElement) {
    v.html += "<img src='" + element.src + "' />"
}

// Element interface
type Element interface {
    Accept(visitor Visitor)
}

// Concrete element - text element
type TextElement struct {
    text string
}

func (e *TextElement) Accept(visitor Visitor) {
    visitor.VisitTextElement(e)
}

// Concrete element - image element
type ImageElement struct {
    src string
}

func (e *ImageElement) Accept(visitor Visitor) {
    visitor.VisitImageElement(e)
}

// Object structure - document
type Document struct {
    elements []Element
}

func (d *Document) AddElement(element Element) {
    d.elements = append(d.elements, element)
}

func (d *Document) Accept(visitor Visitor) {
    for _, element := range d.elements {
        element.Accept(visitor)
    }
}

func main() {
    // Create the document
    doc := &Document{}

    // Add elements
    doc.AddElement(&TextElement{text: "Hello, World!"})
    doc.AddElement(&ImageElement{src: "image.jpg"})
    doc.AddElement(&TextElement{text: "Welcome to the visitor pattern!"})

    // Count words
    wordCountVisitor := &WordCountVisitor{}
    doc.Accept(wordCountVisitor)
    fmt.Printf("Word Count: %d\n", wordCountVisitor.wordCount)

    // Generate HTML
    htmlVisitor := &HTMLVisitor{}
    doc.Accept(htmlVisitor)
    fmt.Println("HTML Output:")
    fmt.Println(htmlVisitor.html)
}
```

#### Applicable scenarios
- When the object structure is relatively stable but operations change frequently.
- When you need to add new operations without changing existing objects.

#### Implementation
Define a visitor interface (`Visitor`) that declares a visit method for each kind of element, and write the operation logic into concrete visitors (such as `WordCountVisitor` and `HTMLVisitor`); elements implement `Accept(visitor Visitor)` to hand themselves over; the object structure (`Document`) holds the element collection and calls `Accept` on each element while iterating.

#### Pros and cons
**Pros**:
- You can add new operations without changing the element classes, and the operations live together in one visitor.
- Operations are separated from the element structure, which makes maintenance easier.

**Cons**:
- The number of visitor classes can grow, especially as the number of element classes grows.
- If the element classes' structure changes, the visitor implementations may need to be modified.

#### Relationship to other patterns
- **Visitor Pattern and Template Method Pattern**: the Template Method pattern defines an algorithm's skeleton, while the Visitor pattern lets you add new operations without changing the objects' structure. They can be combined, for example using the Visitor pattern inside a template method to handle a specific step.
- **Visitor Pattern and Strategy Pattern**: the Strategy pattern defines a family of interchangeable algorithms, while the Visitor pattern wraps operations in visitor objects. They can be combined, for example using the Strategy pattern inside the Visitor pattern to define different operations.
- **Visitor Pattern and Command Pattern**: the Command pattern wraps the operations of a request, while the Visitor pattern separates operations from the objects' structure. They can be combined, for example using the Command pattern inside the Visitor pattern to handle operations.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Adapter](/dp/Adapter.md)
- [Behavioral](/dp/Behavioral.md)
- [TemplateMethod](/dp/TemplateMethod.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [TemplateMethod](/dp/TemplateMethod.md)
