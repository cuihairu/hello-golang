Idioms and patterns refer to the conventional ways of writing in a programming language, used to solve common problems. The boundary between the two is not strict: "patterns" can also refer more broadly to programming habits that recur in a given language.

### Related terminology

1. **Idioms** (idiomatic / habitual usage):
    - Common, widely accepted ways of writing in a given language.
    - Concise, effective ways of writing that solve specific problems.

2. **Patterns**:
    - Usually refers to software design patterns: problems that recur in a specific context and their solutions.
    - More broadly, can refer to common programming patterns and idioms in a given language.

### Related examples

#### Idioms in Go
- **Comma ok idiom** for type assertions, map lookups, and channel receives.
- **Short variable declaration** using `:=`.
- **Blank identifier** (`_`) for ignoring values.
- **Defer** for resource management and cleanup.

#### Patterns in Go
- **Multiple return values** for error handling and results.
- **Named return values** for clarity and simplicity.
- **Type switch** for handling multiple types in a type-safe manner.
- **Select statement** for multiplexing on channels.
- **Anonymous functions and closures** for encapsulating behavior.

### Official resources

- [Effective Go](https://go.dev/doc/effective_go): Go's official guide to idioms and best practices.
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments): Go code review comments, covering many idioms and recommendations.

### Summary

Comma ok, `:=`, the blank identifier `_`, `defer`, multiple return values, and type switch are all covered in Effective Go and Go Code Review Comments. Write to those conventions and the people reading your code don't have to guess why you wrote it that way.

## References

- [Effective Go (official)](https://go.dev/doc/effective_go)


## Sibling pages

- [EffectiveGo](/idioms/EffectiveGo.md)
- [StructTags](/idioms/StructTags.md)
- [BlankIdentifier](/idioms/BlankIdentifier.md)
- [Labels](/idioms/Labels.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Labels](/idioms/Labels.md)
