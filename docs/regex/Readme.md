### 1. Regular expression basics

A regular expression (Regex) is a syntax for describing string patterns, used to search, replace, and validate text. In Go it is provided by the `regexp` package; the libraries in Python, JavaScript, and Java look much the same.

#### 1.1 Overview of regular expressions

**Definition**
- A single regex describes a class of strings; once matched, you can extract them, replace them, or validate a format.

**Use cases**
- **Search and replace**: find a matching pattern in text and replace it.
- **Data validation**: check whether user input matches a specific format (email addresses, phone numbers).
- **Information extraction**: pull specific information out of text (such as extracting IP addresses from a log file).

**Tools and libraries**
- Concretely, for Go it is the `regexp` package, using the RE2 engine.

#### 1.2 Basic regex syntax

**1. Character classes**
- **`.`**: matches any single character (except a newline).
  - For example: `a.b` matches an `a` followed by any character followed by a `b`, such as `a1b` or `a_b`.
- **`\d`**: matches any digit, equivalent to `[0-9]`.
  - For example: `\d{3}` matches three digits, such as `123`.
- **`\D`**: matches any non-digit character.
  - For example: `\D` matches non-digit characters such as `a`, `@`, `#`.
- **`\w`**: matches any letter, digit, or underscore, equivalent to `[a-zA-Z0-9_]`.
  - For example: `\w+` matches one or more letters, digits, or underscores.
- **`\W`**: matches any character that is not a letter, digit, or underscore.
  - For example: `\W` matches characters such as `!`, `@`, `#`.
- **`\s`**: matches any whitespace character (such as a space or tab).
  - For example: `\s+` matches one or more whitespace characters.
- **`\S`**: matches any non-whitespace character.
  - For example: `\S` matches non-whitespace characters such as `a`, `1`, `_`.

**2. Character sets**
- **`[abc]`**: matches the character `a`, `b`, or `c`.
  - For example: `[a-c]` matches `a`, `b`, or `c`.
- **`[^abc]`**: matches any character not in the set.
  - For example: `[^a-c]` matches any character other than `a`, `b`, and `c`.
- **`[a-z]`**: matches any lowercase letter from `a` to `z`.
  - For example: `[a-z]` matches any lowercase letter.
- **`[0-9]`**: matches any digit.
  - For example: `[0-9]` matches any digit.

**3. Metacharacters**
- **`^`**: matches the start of a string.
  - For example: `^Hello` matches a string that starts with `Hello`.
- **`$`**: matches the end of a string.
  - For example: `world$` matches a string that ends with `world`.
- **`*`**: matches the preceding character zero or more times.
  - For example: `a*` matches zero or more `a`s, such as `aa`, `a`, or the empty string.
- **`+`**: matches the preceding character one or more times.
  - For example: `a+` matches one or more `a`s, such as `a`, `aa`.
- **`?`**: matches the preceding character zero or one time, or marks a non-greedy match.
  - For example: `a?` matches zero or one `a`, such as `a` or the empty string.
- **`{n}`**: matches the preceding character exactly n times.
  - For example: `a{3}` matches `aaa`.
- **`{n,}`**: matches the preceding character at least n times.
  - For example: `a{2,}` matches two or more `a`s, such as `aa`, `aaa`.
- **`{n,m}`**: matches the preceding character at least n times and at most m times.
  - For example: `a{2,4}` matches 2 to 4 `a`s, such as `aa`, `aaa`, `aaaa`.

**4. Grouping and capturing**
- **`()`**: groups a match and captures the matched substring.
  - For example: `(ab)+` matches `ab`, `abab`, `ababab`.
- **`(?:)`**: groups without capturing.
  - For example: `(?:ab)+` matches `ab`, `abab`, `ababab` without capturing `ab`.
- **`\1`, `\2`, ...**: reference a capturing group.
  - Note: Go's standard library `regexp` uses the RE2 engine and **does not support backreferences**; the pattern `(\d)\1` reports `invalid escape sequence`. If you need to match repeated digits, you can only match two characters of the same class or handle it in code.

**5. Alternation**
- **`a|b`**: matches `a` or `b`.
  - For example: `cat|dog` matches `cat` or `dog`.

**6. Escape characters**
- **`\`**: escapes a special character so it is treated as a literal.
  - For example: `\.` matches the literal dot `.`, and `\*` matches the literal asterisk `*`.

#### 1.3 Common regex patterns and usages

**1. Matching an email address**
```regexp
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```
- Matches a standard email address.

**2. Matching an IP address (IPv4)**
```regexp
^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$
```
- Matches a valid IPv4 address.

**3. Matching a phone number**
```regexp
^\+?[1-9]\d{1,14}$
```
- Matches the international phone number format (E.164).

**4. Matching a date (YYYY-MM-DD)**
```regexp
^\d{4}-\d{2}-\d{2}$
```
- Matches a date format such as `2024-08-02`.

**5. Matching a URL**
```regexp
https?:\/\/[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\/\S*)?
```
- Matches a URL using `http` or `https`.

These patterns can be handed straight to Go's `regexp` package; note that RE2 does not support backreferences, so repeated-match needs like that have to be worked around another way.

## References

- [regexp standard library](https://pkg.go.dev/regexp)
- [regexp/syntax syntax documentation](https://pkg.go.dev/regexp/syntax)

## Sibling pages

- [Advanced](/regex/Advanced.md)
- [Debug](/regex/Debug.md)
- [Lib](/regex/Lib.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Advanced](/regex/Advanced.md)
- [Debug](/regex/Debug.md)
- [Lib](/regex/Lib.md)
- [Use](/regex/Use.md)
