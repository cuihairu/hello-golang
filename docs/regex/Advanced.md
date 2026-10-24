Advanced regex usage handles more complex text patterns: assertions, non-capturing groups, named captures, greediness control, and dynamic construction.

### 1. Lookahead and lookbehind assertions

Note: Go's standard library `regexp` uses the RE2 engine, which **does not support** lookahead (`(?=...)`, `(?!...)`) or lookbehind assertions (`(?<=...)`, `(?<!...)`); using this syntax fails outright. Below, these two concepts are introduced first (they are available in engines like PCRE/Python), followed by the equivalent way to write them in Go.

**1.1 Lookahead**
- **Definition**: a lookahead assertion checks whether one pattern appears after another, without including it in the match result.
- **Syntax**: `(?=pattern)` is a positive lookahead, `(?!pattern)` is a negative lookahead.
- **Equivalent in Go**: match "the preceding pattern + the following pattern" as a whole, then take out the capturing group you need.
- **Example**: find all letters that follow a digit (not including the digit itself).
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      // equivalent to \d(?=[a-zA-Z]): match the digit and the letter together, then take the digit part
      re := regexp.MustCompile(`(\d)([a-zA-Z])`)
      matches := re.FindAllStringSubmatch("123abc 456def 789", -1)
      var digits []string
      for _, m := range matches {
          digits = append(digits, m[1])
      }
      fmt.Println(digits) // Output: [3 6]
  }
  ```

**1.2 Lookbehind**
- **Definition**: a lookbehind assertion checks whether one pattern appears before another, without including it in the match result.
- **Syntax**: `(?<=pattern)` is a positive lookbehind, `(?<!pattern)` is a negative lookbehind.
- **Equivalent in Go**: match "the preceding pattern + the pattern you want to extract" as a whole, then take the trailing capturing group.
- **Example**: find all letters preceded by "abc".
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      // equivalent to (?<=abc)[a-zA-Z]: match abc and the letter together, then take the letter part
      re := regexp.MustCompile(`abc([a-zA-Z])`)
      matches := re.FindAllStringSubmatch("abcD abcE fgh", -1)
      var letters []string
      for _, m := range matches {
          letters = append(letters, m[1])
      }
      fmt.Println(letters) // Output: [D E]
  }
  ```

### 2. Non-capturing groups

**2.1 Non-capturing groups**
- **Definition**: a non-capturing group is used for grouping but does not capture the matched content.
- **Syntax**: `(?:pattern)`
- **Example**: match a series of digits without capturing the group.
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      re := regexp.MustCompile(`(?:\d{3}-\d{2}-\d{4})`)
      matches := re.FindAllString("123-45-6789 987-65-4321", -1)
      fmt.Println(matches) // Output: [123-45-6789 987-65-4321]
  }
  ```

### 3. Named capturing groups

**3.1 Named capturing groups**
- **Definition**: a named capturing group lets you give the captured group a name, making it easy to reference in code.
- **Syntax**: `(?P<name>pattern)`
- **Example**: extract the year, month, and day of a date and give them names.
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      re := regexp.MustCompile(`(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})`)
      match := re.FindStringSubmatch("2024-08-02")
      if len(match) > 0 {
          fmt.Println("Year:", match[re.SubexpIndex("year")])   // Output: Year: 2024
          fmt.Println("Month:", match[re.SubexpIndex("month")]) // Output: Month: 08
          fmt.Println("Day:", match[re.SubexpIndex("day")])     // Output: Day: 02
      }
  }
  ```

### 4. Greedy and non-greedy matching

**4.1 Greedy matching**
- **Definition**: greedy matching matches as many characters as possible.
- **Example**: match one or more letters, including potentially multiple matches.
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      re := regexp.MustCompile(`[a-z]+`)
      matches := re.FindAllString("abc 123 def ghi", -1)
      fmt.Println(matches) // Output: [abc def ghi]
  }
  ```

**4.2 Non-greedy matching**
- **Definition**: non-greedy matching matches as few characters as possible.
- **Syntax**: add `?` after a quantifier (as in `*?`, `+?`, `??`)
- **Example**: match the shortest sequence of letters.
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      re := regexp.MustCompile(`<.*?>`)
      matches := re.FindAllString("<a> <b> <c>", -1)
      fmt.Println(matches) // Output: [<a> <b> <c>]
  }
  ```

### 5. Capturing and referencing

**5.1 Capturing groups**
- **Definition**: capturing groups are used to extract matched substrings and can be referenced in replacement operations.
- **Syntax**: `(pattern)`
- **Example**: reverse the matched substring.
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      re := regexp.MustCompile(`(\d{3})-(\d{2})-(\d{4})`)
      result := re.ReplaceAllString("123-45-6789", "$3-$2-$1")
      fmt.Println(result) // Output: 6789-45-123
  }
  ```

**5.2 Referencing groups**
- **Definition**: reference a capturing group inside the replacement string.
- **Syntax**: `$n` (where n is the group number)
- **Example**: reverse the matched digit groups.
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      re := regexp.MustCompile(`(\d+)-(\d+)`)
      result := re.ReplaceAllString("123-456 789-012", "$2-$1")
      fmt.Println(result) // Output: 456-123 012-789
  }
  ```

### 6. Dynamic regular expressions

**6.1 Building regexes dynamically**
- **Definition**: generate a regular expression from runtime data.
- **Example**: dynamically create a regex that matches a user-provided keyword.
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      keyword := "example"
      re := regexp.MustCompile(fmt.Sprintf(`\b%s\b`, keyword))
      matches := re.FindAllString("This is an example of dynamic regex.", -1)
      fmt.Println(matches) // Output: [example]
  }
  ```

Of these syntaxes, Go's `regexp` supports non-capturing groups, named capturing groups, greedy/non-greedy quantifiers, capture references, and dynamic construction; lookahead and lookbehind assertions are not supported and have to be rewritten as equivalent patterns the way section 1 describes.

## References

- [regexp standard library](https://pkg.go.dev/regexp)
- [regexp/syntax syntax documentation](https://pkg.go.dev/regexp/syntax)

## Sibling pages

- [Debug](/regex/Debug.md)
- [Lib](/regex/Lib.md)
- [Readme](/regex/Readme.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Debug](/regex/Debug.md)
- [Lib](/regex/Lib.md)
- [Readme](/regex/Readme.md)
- [Use](/regex/Use.md)
- [Usual](/regex/Usual.md)
