### 2. Go's regular expression library

Regular expression support in Go is provided by the `regexp` package, covering compilation, matching, searching, replacement, and splitting.

#### 2.1 Introduction to the `regexp` package

**Overview**
- The `regexp` package is part of the Go standard library and provides support for regular expressions.
- Features included: compiling, matching, replacing, and splitting with regular expressions.

**Import**
```go
import "regexp"
```

**Main data types**
- `*regexp.Regexp`: represents a compiled regular expression object, used for matching, replacement, and splitting operations.

#### 2.2 Matching and searching

**1. Compiling a regular expression**
- Use `regexp.MustCompile` to compile a regular expression and return a `*regexp.Regexp` object. If the expression is invalid, a panic is triggered.
```go
re := regexp.MustCompile(`pattern`)
```

**2. Matching a string**
- **`MatchString`**: checks whether the string contains a part matching the regular expression (unanchored matching; to match the whole string, add `^` and `$` at both ends of the pattern).
```go
matched := re.MatchString("test string")
```

**3. Finding matches**
- **`FindString`**: returns the first string matched by the regular expression.
```go
matched := re.FindString("test string")
```

- **`FindStringIndex`**: returns the position index of the first string matched by the regular expression.
```go
index := re.FindStringIndex("test string")
```

- **`FindAllString`**: returns all strings matched by the regular expression.
```go
matches := re.FindAllString("test string", -1)
```

- **`FindAllStringSubmatch`**: returns all strings matched by the regular expression along with their substrings.
```go
matches := re.FindAllStringSubmatch("test string", -1)
```

#### 2.3 Replacing and splitting

**1. Replacing matched strings**
- **`ReplaceAllString`**: replaces all parts matched by the regular expression with the given string.
```go
result := re.ReplaceAllString("test string", "replacement")
```

- **`ReplaceAllFunc`**: replaces all parts matched by the regular expression with a string returned by a function.
```go
result := re.ReplaceAllFunc([]byte("test string"), func(b []byte) []byte {
    return []byte("replacement")
})
```

**2. Splitting a string**
- **`Split`**: splits a string according to the regular expression and returns the resulting substrings.
```go
parts := re.Split("test string", -1)
```

#### 2.4 Main functions of the `regexp` package

**1. Compiling a regular expression**
- **`Compile`**: compiles a regular expression and returns a `*regexp.Regexp` object; if the expression is invalid, it returns an error.
```go
re, err := regexp.Compile(`pattern`)
if err != nil {
    // handle the error
}
```

- **`MustCompile`**: compiles a regular expression and returns a `*regexp.Regexp` object; if the expression is invalid, a panic is triggered.
```go
re := regexp.MustCompile(`pattern`)
```

**2. Checking for a match**
- **`MatchString`**: checks whether the string contains a match (unanchored matching; to match the whole string, add `^` and `$` at both ends of the pattern).
```go
matched := re.MatchString("test string")
```

- **`Match`**: checks whether a byte slice matches the regular expression.
```go
matched := re.Match([]byte("test string"))
```

**3. Finding matches**
- **`FindString`**: finds and returns the first string matched by the regular expression.
```go
result := re.FindString("test string")
```

- **`FindAllString`**: finds and returns all strings matched by the regular expression.
```go
results := re.FindAllString("test string", -1)
```

- **`FindStringSubmatch`**: finds and returns the first string matched by the regular expression along with its substrings.
```go
matches := re.FindStringSubmatch("test string")
```

- **`FindAllStringSubmatch`**: finds and returns all strings matched by the regular expression along with their substrings.
```go
matches := re.FindAllStringSubmatch("test string", -1)
```

**4. Replacing matches**
- **`ReplaceAllString`**: replaces all parts matched by the regular expression with the given string.
```go
result := re.ReplaceAllString("test string", "replacement")
```

- **`ReplaceAllFunc`**: replaces all parts matched by the regular expression with a string returned by a function.
```go
result := re.ReplaceAllFunc([]byte("test string"), func(b []byte) []byte {
    return []byte("replacement")
})
```

**5. Splitting a string**
- **`Split`**: splits a string according to the regular expression and returns the resulting substrings.
```go
parts := re.Split("test string", -1)
```

**6. Finding the position of a match**
- **`FindStringIndex`**: finds the position index of the first string matched by the regular expression.
```go
index := re.FindStringIndex("test string")
```

The ones used most day to day are these: `MustCompile` to compile, `MatchString` to test whether something matches, `FindAllString` to get all results, and `ReplaceAllString` to replace. When the pattern comes from a source only known at runtime (such as user input), switch to `Compile` and handle the returned error.

## References

- [regexp standard library](https://pkg.go.dev/regexp)
- [regexp/syntax syntax documentation](https://pkg.go.dev/regexp/syntax)

## Sibling pages

- [Advanced](/regex/Advanced.md)
- [Debug](/regex/Debug.md)
- [Readme](/regex/Readme.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Advanced](/regex/Advanced.md)
- [Debug](/regex/Debug.md)
- [Readme](/regex/Readme.md)
- [Use](/regex/Use.md)
- [Usual](/regex/Usual.md)
