A regular expression (Regex) does matching, searching, extraction, and replacement with a single pattern string; in Go the corresponding package is `regexp`.

### 1. Text searching and replacement

**1.1 Searching for a specific pattern**
- **Use case**: find text matching a specific pattern in a document or log. For example, finding all email addresses or phone numbers.
- **Example**:
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      re := regexp.MustCompile(`[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`)
      matches := re.FindAllString("Contact us at support@example.com or admin@example.com", -1)
      fmt.Println(matches) // Output: [support@example.com admin@example.com]
  }
  ```

**1.2 Replacing text**
- **Use case**: replace sensitive information or formatting in text. For example, normalizing all phone numbers to an international format.
- **Example**:
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      re := regexp.MustCompile(`\d{3}-\d{2}-\d{4}`)
      result := re.ReplaceAllString("My number is 123-45-6789.", "XXX-XX-XXXX")
      fmt.Println(result) // Output: My number is XXX-XX-XXXX.
  }
  ```

### 2. Data validation

**2.1 Validating an email address**
- **Use case**: ensure the email address entered by the user matches the standard format.
- **Example**:
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      email := "user@example.com"
      re := regexp.MustCompile(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)
      isValid := re.MatchString(email)
      fmt.Println(isValid) // Output: true
  }
  ```

**2.2 Validating a phone number**
- **Use case**: verify that the phone number entered by the user matches the international format.
- **Example**:
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      phone := "+1234567890"
      re := regexp.MustCompile(`^\+?[1-9]\d{1,14}$`)
      isValid := re.MatchString(phone)
      fmt.Println(isValid) // Output: true
  }
  ```

### 3. Information extraction

**3.1 Extracting information from text**
- **Use case**: extract IP addresses or URLs from a log file.
- **Example**:
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      re := regexp.MustCompile(`\b(\d{1,3}\.){3}\d{1,3}\b`)
      matches := re.FindAllString("Server IPs: 192.168.1.1, 10.0.0.1", -1)
      fmt.Println(matches) // Output: [192.168.1.1 10.0.0.1]
  }
  ```

**3.2 Extracting a substring**
- **Use case**: extract a date or other information from text.
- **Example**:
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      re := regexp.MustCompile(`(\d{4}-\d{2}-\d{2})`)
      match := re.FindStringSubmatch("The event will be held on 2024-08-02.")
      if len(match) > 1 {
          fmt.Println(match[1]) // Output: 2024-08-02
      }
  }
  ```

### 4. Data cleaning

**4.1 Removing useless characters**
- **Use case**: clean up extra whitespace or non-printable characters in text data.
- **Example**:
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      re := regexp.MustCompile(`\s+`)
      cleaned := re.ReplaceAllString("This   is  a    sample text.", " ")
      fmt.Println(cleaned) // Output: This is a sample text.
  }
  ```

**4.2 Normalizing formats**
- **Use case**: normalize dates, times, or other formats.
- **Example**:
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      re := regexp.MustCompile(`(\d{2})/(\d{2})/(\d{4})`)
      result := re.ReplaceAllString("Today's date is 08/02/2024.", "2024-08-02")
      fmt.Println(result) // Output: Today's date is 2024-08-02.
  }
  ```

### 5. Log analysis and processing

**5.1 Parsing log entries**
- **Use case**: extract the request path and status code from a server log.
- **Example**:
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      re := regexp.MustCompile(`\[(\d{3})\] "GET (\/[^"\s]*)`)
      matches := re.FindAllStringSubmatch(`[200] "GET /index.html"`, -1)
      if len(matches) > 0 {
          fmt.Println("Status Code:", matches[0][1]) // Output: Status Code: 200
          fmt.Println("Request Path:", matches[0][2]) // Output: Request Path: /index.html
      }
  }
  ```

### 6. Web development

**6.1 Validating user input**
- **Use case**: validate user input in a web form, such as checking password strength.
- **Example**:
  Go's standard library `regexp` uses the RE2 engine, which does not support lookahead assertions like `(?=...)`. Password strength checks should be split into several regexes, each checking one condition:

  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      password := "P@ssw0rd123"
      // check each condition separately: has an uppercase letter, has a digit, has a special character, length and character set
      hasUpper := regexp.MustCompile(`[A-Z]`).MatchString(password)
      hasDigit := regexp.MustCompile(`\d`).MatchString(password)
      hasSpecial := regexp.MustCompile(`[@$!%*?&]`).MatchString(password)
      hasValidLength := regexp.MustCompile(`^[A-Za-z\d@$!%*?&]{8,}$`).MatchString(password)
      isValid := hasUpper && hasDigit && hasSpecial && hasValidLength
      fmt.Println(isValid) // Output: true
  }
  ```

**6.2 Extracting URL parameters**
- **Use case**: extract query parameters from a URL.
- **Example**:
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      re := regexp.MustCompile(`[?&]param=([^&]+)`)
      match := re.FindStringSubmatch("https://example.com?param=value")
      if len(match) > 1 {
          fmt.Println("Parameter Value:", match[1]) // Output: Parameter Value: value
      }
  }
  ```

All six categories of scenarios above use `regexp.MustCompile`: it compiles the pattern once at program start, panics outright if the pattern is invalid, and suits regexes hardcoded in source. For patterns only known at runtime, use `regexp.Compile` and check the error.

## References

- [regexp standard library](https://pkg.go.dev/regexp)
- [regexp/syntax syntax documentation](https://pkg.go.dev/regexp/syntax)


## Sibling pages

- [Advanced](/regex/Advanced.md)
- [Debug](/regex/Debug.md)
- [Lib](/regex/Lib.md)
- [Readme](/regex/Readme.md)
- [Usual](/regex/Usual.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Usual](/regex/Usual.md)
