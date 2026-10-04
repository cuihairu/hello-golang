### XML（eXtensible Markup Language）

XML（eXtensible Markup Language）是一种标记语言，用标签定义文档结构、描述数据。它自描述、可扩展，常出现在数据交换、配置文件、文档存储这几类场景，由 W3C（World Wide Web Consortium）定义并标准化。

#### 1. XML 的基本结构

XML 的基本结构包括元素、属性、文本、CDATA 区段等。以下是 XML 的基本组件：

1. **XML 声明**

   - XML 声明是一个可选的声明，位于文档的开头，指定 XML 的版本和编码。例如：
     ```xml
     <?xml version="1.0" encoding="UTF-8"?>
     ```

2. **元素（Element）**

   - 元素是 XML 文档的基本组成部分，由开始标签、内容和结束标签组成。例如：
     ```xml
     <name>John</name>
     ```
   - 元素可以包含子元素、属性和文本内容。例如：
     ```xml
     <person>
       <name>John</name>
       <age>30</age>
     </person>
     ```

3. **属性（Attribute）**

   - 属性为元素提供附加信息，定义在开始标签中。例如：
     ```xml
     <person id="1">
       <name>John</name>
       <age>30</age>
     </person>
     ```
   - 属性通常用于描述元素的特征，但不支持多层级的复杂结构。

4. **文本（Text）**

   - 元素的内容部分可以是文本。文本内容位于开始标签和结束标签之间。例如：
     ```xml
     <description>This is a sample description.</description>
     ```

5. **CDATA 区段**

   - CDATA 区段用于包含不需要解析的文本，例如 HTML 代码或脚本。例如：
     ```xml
     <script><![CDATA[
       function hello() {
         alert("Hello, world!");
       }
     ]]></script>
     ```

6. **注释（Comment）**

   - 注释用于在 XML 文档中插入解释或说明，注释用 `<!--` 和 `-->` 括起来。例如：
     ```xml
     <!-- This is a comment -->
     ```

7. **处理指令（Processing Instruction）**

   - 处理指令用于在 XML 文档中包含应用程序特定的指令。例如：
     ```xml
     <?xml-stylesheet type="text/xsl" href="style.xsl"?>
     ```

#### 2. XML 的规则

1. **文档结构**

   - XML 文档必须有且仅有一个根元素。根元素包含所有其他元素。例如：
     ```xml
     <root>
       <child>Content</child>
     </root>
     ```

2. **标签匹配**

   - 所有元素必须正确匹配开始标签和结束标签。例如：
     ```xml
     <person>
       <name>John</name>
     </person>
     ```

3. **属性值必须用引号括起来**

   - 属性值必须用单引号（`'`）或双引号（`"`）括起来。例如：
     ```xml
     <person id="1" name="John"/>
     ```

4. **合法的 XML 名称**

   - 元素名和属性名必须遵循 XML 的命名规则。不能以数字开头，不能包含空格或特殊字符。合法名称示例：
     ```xml
     <personName>John</personName>
     ```

5. **大小写敏感**

   - XML 是大小写敏感的，即 `<Person>` 和 `<person>` 被视为不同的元素。

6. **空元素**

   - XML 允许使用空元素标签来表示不包含任何内容的元素。例如：
     ```xml
     <item/>
     ```

#### 3. XML 的应用

1. **数据交换**

   - Web 服务、API 用 XML 在不同系统之间传递数据，双方约定同一套标签即可。

2. **配置文件**

   - 应用程序配置、系统设置用 XML 写成文本，改动配置不需要重新编译程序。

3. **文档存储**

   - 电子书、Office 文档这类富文本用 XML 存结构，段落、样式各占标签。

4. **RSS 和 Atom**

   - XML 用于 RSS 和 Atom 规范，这些规范用于订阅和发布 Web 内容，如新闻、博客等。

#### 4. XML 的优点

1. **自描述性**

   - XML 文档包含描述数据的标签和结构，使得数据的含义和结构自解释，易于理解和维护。

2. **可扩展性**

   - XML 允许自定义标签和结构，适应不同的需求和应用场景。可以根据需要定义新的标签和属性。

3. **平台无关**

   - XML 是平台无关的，可以在不同的操作系统和编程语言之间交换数据。

4. **结构化**

   - XML 数据是结构化的，可以表示复杂的数据关系和层级结构。

#### 5. XML 的缺点

1. **冗长**

   - XML 的标记语言比较冗长，导致数据文件较大，传输和存储效率较低。

2. **解析复杂**

   - XML 解析器较为复杂，尤其对于大型 XML 文档，可能需要较高的计算和内存资源。

3. **不支持数据类型**

   - XML 不支持数据类型的定义，一切数据都作为文本处理，需要额外的处理来解析和转换数据类型。

#### 6. XML 的解析和生成

在 Go 语言中，处理 XML 数据的常用方式如下：

```go
package main

import (
    "encoding/xml"
    "fmt"
)

// 定义结构体对应 XML 元素
type Person struct {
    XMLName xml.Name `xml:"person"`
    Name    string   `xml:"name"`
    Age     int      `xml:"age"`
}

func main() {
    // XML 数据
    xmlData := `
    <person>
      <name>John</name>
      <age>30</age>
    </person>
    `
    
    // 解析 XML 数据
    var person Person
    err := xml.Unmarshal([]byte(xmlData), &person)
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    
    fmt.Println(person)
    
    // 生成 XML 数据
    newPerson := Person{
        Name: "Jane",
        Age:  25,
    }
    
    newXmlData, err := xml.MarshalIndent(newPerson, "", "  ")
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    
    fmt.Println(string(newXmlData))
}
```

#### 总结

XML 用自定义标签表达结构化的数据，跨平台传递，代价是标记冗长、解析要花内存。需要人可读、可扩展的文本格式时选 XML，只在程序内部来回传数据时 JSON 更省事。Go 解析用 `xml.Unmarshal`，生成用 `xml.MarshalIndent`。