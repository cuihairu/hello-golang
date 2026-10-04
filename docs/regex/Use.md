正则表达式（Regex）用一条模式串完成匹配、查找、提取和替换，在 Go 里对应的包是 `regexp`。

### 1. 文本搜索与替换

**1.1 搜索特定模式**
- **用例**：在文档或日志中查找符合特定模式的文本。例如，找到所有的电子邮件地址或电话号码。
- **示例**：
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

**1.2 替换文本**
- **用例**：将文本中的敏感信息或格式进行替换。例如，将所有的电话号码格式统一为国际标准。
- **示例**：
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

### 2. 数据验证

**2.1 验证电子邮件地址**
- **用例**：确保用户输入的电子邮件地址符合标准格式。
- **示例**：
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

**2.2 验证电话号码**
- **用例**：验证用户输入的电话号码是否符合国际格式。
- **示例**：
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

### 3. 信息提取

**3.1 从文本中提取信息**
- **用例**：从日志文件中提取 IP 地址或 URL。
- **示例**：
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

**3.2 提取子串**
- **用例**：从文本中提取日期或其他信息。
- **示例**：
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

### 4. 数据清理

**4.1 移除无用字符**
- **用例**：清理文本数据中的多余空格或非打印字符。
- **示例**：
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

**4.2 格式标准化**
- **用例**：将日期、时间或其他格式进行标准化。
- **示例**：
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

### 5. 日志分析与处理

**5.1 解析日志条目**
- **用例**：从服务器日志中提取请求路径和状态码。
- **示例**：
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

### 6. Web 开发

**6.1 验证用户输入**
- **用例**：在 Web 表单中验证用户输入，如密码强度检查。
- **示例**：
  Go 标准库的 `regexp` 使用 RE2 引擎，不支持 `(?=...)` 前瞻断言。密码强度检查应拆分为多个正则分别判断：

  ```go
  package main

  import (
      "fmt"
      "regexp"
  )

  func main() {
      password := "P@ssw0rd123"
      // 分别检查：含大写字母、含数字、含特殊字符、长度与字符集
      hasUpper := regexp.MustCompile(`[A-Z]`).MatchString(password)
      hasDigit := regexp.MustCompile(`\d`).MatchString(password)
      hasSpecial := regexp.MustCompile(`[@$!%*?&]`).MatchString(password)
      hasValidLength := regexp.MustCompile(`^[A-Za-z\d@$!%*?&]{8,}$`).MatchString(password)
      isValid := hasUpper && hasDigit && hasSpecial && hasValidLength
      fmt.Println(isValid) // Output: true
  }
  ```

**6.2 提取 URL 参数**
- **用例**：从 URL 中提取查询参数。
- **示例**：
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

上面六类场景都用了 `regexp.MustCompile`：它在程序启动时把模式编译一次，模式非法直接 panic，适合写死在代码里的正则；运行期才拿到的模式该用 `regexp.Compile` 并检查错误。
