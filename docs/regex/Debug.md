This section covers two things: what to do when a regex is written wrong, and how to tell why it does not match as expected.

## Error handling for regular expressions

### 1. Overview of error handling

A badly written regex either fails to compile or fails to match the expected result. Putting error handling and validation up front is what lets you be sure the regex behaves as intended.

### 2. Common regex errors

**2.1 Syntax errors**
- **Description**: the regex syntax is incorrect, which usually raises a compilation error or exception. For example, an unclosed parenthesis or a mismatched character class.
- **Example**: `(abc` (missing a closing parenthesis)

**2.2 Capturing group errors**
- **Description**: capturing groups are used incorrectly, for example with redundant groups or unnecessary groups.
- **Example**: `(abc)(` (an unclosed capturing group)

**2.3 Quantifier errors**
- **Description**: quantifiers are used incorrectly, for example mixing greedy and non-greedy quantifiers.
- **Example**: `a{2,1}` (the minimum count exceeds the maximum count)

### 3. Error handling strategies

**3.1 Using the error handling built into the regex library**
- Most regex libraries (including Go's `regexp` package) return an error message indicating that compilation of the regex failed. Checking and handling these errors avoids runtime exceptions.

```go
re, err := regexp.Compile(`(abc`)
if err != nil {
    fmt.Println("Regex compilation error:", err)
}
_ = re // when compilation fails re is nil; this line is just a placeholder
```

**3.2 Validating a regex with test cases**
- Write test cases to verify that the regex behaves as expected. Cover both matching correct input and handling non-matching input.

```go
import (
    "regexp"
    "testing"
)

func TestRegex(t *testing.T) {
    re := regexp.MustCompile(`\d+`)
    matches := re.FindString("123abc")
    if matches != "123" {
        t.Errorf("Expected '123', got '%s'", matches)
    }
}
```

## Debugging regular expressions

### 1. Overview of debugging

When a match comes out wrong, break the regex apart and verify it piece by piece, using tests and print statements to see what it actually captured.

### 2. Using debugging tools

**2.1 Online regex testing tools**
- Tools such as [regex101](https://regex101.com/) and [RegExr](https://regexr.com/) give you live match results and expand detailed match information and explanations.

**2.2 Regex debugging libraries**
- **Tools**: some languages ship a regex debugging library that lets you inspect match details. For example, Go's `regexp` package can be used to test regular expressions.

### 3. Debugging techniques

**3.1 Step-by-step debugging**
- Break a complex regex down into simple parts and debug the behaviour of each part one at a time.

**3.2 Using debug output**
- Add debug output to the code so you can inspect the details of what the regex matched.

```go
re := regexp.MustCompile(`\d+`)
matches := re.FindAllString("123abc", -1)
fmt.Println("Matches:", matches)
```

**3.3 Recording intermediate results**
- Record intermediate results while debugging to understand how the regex behaves across different inputs.

**3.4 Consulting the documentation**
- Read the official documentation and references for regular expressions to make sure the syntax and usage are correct.

### 4. Troubleshooting common problems

**4.1 A regex does not match**
- Check that the regex correctly captures the intended pattern.
- Make sure the quantifiers, character classes, and boundary anchors are correct.

**4.2 Performance problems**
- For complex regexes, consider optimizing the pattern to improve match performance; avoid too many greedy quantifiers and complex capturing groups.

**4.3 Handling special characters**
- Make sure special characters (such as `.`, `*`, `?`) are escaped correctly to prevent unintended matching.

The order to work through is: first look at the compilation error, then split the pattern and test it piece by piece, and finally pin the behaviour down with test cases.

## References

- [regexp standard library](https://pkg.go.dev/regexp)
- [regexp/syntax syntax documentation](https://pkg.go.dev/regexp/syntax)

## Sibling pages

- [Advanced](/regex/Advanced.md)
- [Lib](/regex/Lib.md)
- [Readme](/regex/Readme.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Advanced](/regex/Advanced.md)
- [Lib](/regex/Lib.md)
- [Readme](/regex/Readme.md)
- [Use](/regex/Use.md)
- [Usual](/regex/Usual.md)
