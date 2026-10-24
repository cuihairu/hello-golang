Regular expression patterns are used to match and manipulate specific text in a string. Common patterns and usages are listed below:

### 1. Basic character matching

**1.1 Exact match**
- **Pattern**: `abc`
- **Description**: matches the string "abc" where it appears.

**1.2 Any single character**
- **Pattern**: `a.c`
- **Description**: matches a string that starts with "a" and ends with "c", with any single character in between. For example, "abc" and "a-c".

### 2. Character classes

**2.1 Digit characters**
- **Pattern**: `\d`
- **Description**: matches any digit character, equivalent to `[0-9]`.

**2.2 Non-digit characters**
- **Pattern**: `\D`
- **Description**: matches any non-digit character.

**2.3 Word characters**
- **Pattern**: `\w`
- **Description**: matches any letter, digit, or underscore, equivalent to `[a-zA-Z0-9_]`.

**2.4 Non-word characters**
- **Pattern**: `\W`
- **Description**: matches any character that is not a letter, digit, or underscore.

**2.5 Whitespace characters**
- **Pattern**: `\s`
- **Description**: matches any whitespace character, such as a space, tab, or newline.

**2.6 Non-whitespace characters**
- **Pattern**: `\S`
- **Description**: matches any non-whitespace character.

### 3. Quantifiers

**3.1 Zero or more**
- **Pattern**: `a*`
- **Description**: matches "a" zero or more times. For example, "", "a", and "aaa".

**3.2 One or more**
- **Pattern**: `a+`
- **Description**: matches "a" one or more times. For example, "a" and "aaa".

**3.3 Exact count**
- **Pattern**: `a{3}`
- **Description**: matches exactly three "a"s. For example, "aaa".

**3.4 Minimum count**
- **Pattern**: `a{2,}`
- **Description**: matches at least two "a"s. For example, "aa" and "aaa".

**3.5 Range count**
- **Pattern**: `a{2,4}`
- **Description**: matches two to four "a"s. For example, "aa", "aaa", and "aaaa".

### 4. Boundary matching

**4.1 Word boundary**
- **Pattern**: `\bword\b`
- **Description**: matches the whole word "word". For example, it matches "word" in "a word here", but not "word" in "wording" (a letter follows, so there is no word boundary).

**4.2 Non-word boundary**
- **Pattern**: `\Bword\B`
- **Description**: matches "word" when it appears at non-word boundaries, meaning neither side is a word boundary. For example, "word" in "sworded" ("s" precedes it and "e" follows, so both sides are word characters).

**4.3 Start of line**
- **Pattern**: `^abc`
- **Description**: matches a line that starts with "abc".

**4.4 End of line**
- **Pattern**: `abc$`
- **Description**: matches a line that ends with "abc".

### 5. Capturing groups and non-capturing groups

**5.1 Capturing group**
- **Pattern**: `(abc)`
- **Description**: captures and stores the matched "abc" portion.

**5.2 Non-capturing group**
- **Pattern**: `(?:abc)`
- **Description**: groups without capturing the matched content.

**5.3 Reference to a capturing group**
- **Pattern**: `(a)(b)\1\2`
- **Description**: matches "ab" followed by a repeated "a" and "b", such as "abab".
- **Note**: the RE2 engine in Go's standard library `regexp` does not support backreferences `\1`, `\2` (compilation reports `invalid escape sequence`); this pattern works in engines such as PCRE/Python.

### 6. Lookahead and lookbehind assertions

**Note**: the RE2 engine in Go's standard library `regexp` does not support the four assertion syntaxes in this section (compilation reports `invalid or unsupported Perl syntax`); the following patterns only apply to engines such as PCRE/Python; in Go you need to match the context together and then extract it with a capturing group.

**6.1 Lookahead assertion**
- **Pattern**: `a(?=b)`
- **Description**: matches "a" only if it is followed by "b".

**6.2 Negative lookahead**
- **Pattern**: `a(?!b)`
- **Description**: matches "a" only if it is not followed by "b".

**6.3 Lookbehind assertion**
- **Pattern**: `(?<=b)a`
- **Description**: matches "a" only if it is preceded by "b".

**6.4 Negative lookbehind**
- **Pattern**: `(?<!b)a`
- **Description**: matches "a" only if it is not preceded by "b".

### 7. Alternation

**7.1 Alternation**
- **Pattern**: `a|b`
- **Description**: matches "a" or "b".

**7.2 Grouped alternation**
- **Pattern**: `(?:a|b)`
- **Description**: groups a match of "a" or "b" without capturing.

### 8. Special characters

**8.1 Escape characters**
- **Pattern**: `\.`, `\*`
- **Description**: matches a literal dot `.` or asterisk `*`.

**8.2 Any character**
- **Pattern**: `a.`
- **Description**: matches "a" followed by any single character.

### 9. Greedy and non-greedy matching

**9.1 Greedy matching**
- **Pattern**: `a.*b`
- **Description**: matches as many characters as possible until it hits "b".

**9.2 Non-greedy matching**
- **Pattern**: `a.*?b`
- **Description**: matches as few characters as possible until it hits "b".

Go's `regexp` uses the RE2 engine, so the backreferences and assertions in sections 5 and 6 fail to compile in Go. Before writing a Go regex, check it against the syntax RE2 actually supports.

## References

- [regexp standard library](https://pkg.go.dev/regexp)
- [regexp/syntax syntax documentation](https://pkg.go.dev/regexp/syntax)


## Sibling pages

- [Advanced](/regex/Advanced.md)
- [Debug](/regex/Debug.md)
- [Lib](/regex/Lib.md)
- [Use](/regex/Use.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Use](/regex/Use.md)
