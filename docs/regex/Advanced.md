正则表达式的高级用法处理更复杂的文本模式：断言、非捕获组、命名捕获、贪婪控制、动态构建。

### 1. 先行断言和后行断言

注意：Go 标准库 `regexp` 使用 RE2 引擎，**不支持**前瞻（`(?=...)`、`(?!...)`）和后行断言（`(?<=...)`、`(?<!...)`），使用这类语法会直接报错。下面先介绍这两个概念（在 PCRE/Python 等引擎中可用），再给出在 Go 中的等价写法。

**1.1 先行断言（Lookahead）**
- **定义**：先行断言用于检查某个模式是否在另一个模式之前出现，但不会包括在匹配结果中。
- **语法**：`(?=pattern)` 表示前瞻断言，`(?!pattern)` 表示否定前瞻断言。
- **Go 中的等价写法**：把"前面的模式 + 后面的模式"作为一个整体匹配，再取出需要的捕获组。
- **示例**：查找所有跟在数字后面的字母（不包括数字本身）。
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      // 等价于 \d(?=[a-zA-Z])：数字与字母一起匹配，再取出数字部分
      re := regexp.MustCompile(`(\d)([a-zA-Z])`)
      matches := re.FindAllStringSubmatch("123abc 456def 789", -1)
      var digits []string
      for _, m := range matches {
          digits = append(digits, m[1])
      }
      fmt.Println(digits) // Output: [3 6]
  }
  ```

**1.2 后行断言（Lookbehind）**
- **定义**：后行断言用于检查某个模式是否在另一个模式之后出现，但不会包括在匹配结果中。
- **语法**：`(?<=pattern)` 表示正向后瞻断言，`(?<!pattern)` 表示否定后瞻断言。
- **Go 中的等价写法**：把"前面的模式 + 要取出的模式"作为一个整体匹配，再取出后半部分捕获组。
- **示例**：查找所有前面跟有“abc”的字母。
  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      // 等价于 (?<=abc)[a-zA-Z]：abc 与字母一起匹配，再取出字母部分
      re := regexp.MustCompile(`abc([a-zA-Z])`)
      matches := re.FindAllStringSubmatch("abcD abcE fgh", -1)
      var letters []string
      for _, m := range matches {
          letters = append(letters, m[1])
      }
      fmt.Println(letters) // Output: [D E]
  }
  ```

### 2. 非捕获组

**2.1 非捕获组（Non-Capturing Groups）**
- **定义**：非捕获组用于分组，但不会捕获匹配的内容。
- **语法**：`(?:pattern)`
- **示例**：匹配一系列的数字，但不捕获分组。
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

### 3. 命名捕获组

**3.1 命名捕获组**
- **定义**：命名捕获组允许你为捕获的组指定一个名字，便于在代码中引用。
- **语法**：`(?P<name>pattern)`
- **示例**：提取日期的年、月、日，并为它们命名。
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

### 4. 贪婪与非贪婪匹配

**4.1 贪婪匹配（Greedy Matching）**
- **定义**：贪婪匹配尽可能多地匹配字符。
- **示例**：匹配一个或多个字母，包括可能的多个匹配项。
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

**4.2 非贪婪匹配（Non-Greedy Matching）**
- **定义**：非贪婪匹配尽可能少地匹配字符。
- **语法**：在量词后面加上 `?`（如 `*?`, `+?`, `??`）
- **示例**：匹配最短的字母序列。
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

### 5. 捕获和引用

**5.1 捕获组**
- **定义**：捕获组用于提取匹配的子串，并可以在替换操作中引用。
- **语法**：`(pattern)`
- **示例**：将匹配的子串反转。
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

**5.2 组的引用**
- **定义**：在替换字符串中引用捕获组。
- **语法**：`$n`（n 是组的编号）
- **示例**：将匹配的数字组逆序。
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

### 6. 动态正则表达式

**6.1 动态构建正则表达式**
- **定义**：根据运行时数据动态生成正则表达式。
- **示例**：动态创建用于匹配用户提供的关键字。
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

这些语法里，Go `regexp` 支持非捕获组、命名捕获组、贪婪/非贪婪量词、捕获引用和动态构建；先行/后行断言不支持，得按第 1 节的方式改写成等价模式。
