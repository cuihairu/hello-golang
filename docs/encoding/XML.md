### XML (eXtensible Markup Language)

XML (eXtensible Markup Language) is a markup language that defines document structure and describes data using tags. It is self-describing and extensible, and is commonly found in data exchange, configuration files, and document storage. It is defined and standardized by the W3C (World Wide Web Consortium).

#### 1. The basic structure of XML

The basic structure of XML includes elements, attributes, text, CDATA sections, and more. The basic components of XML are as follows:

1. **XML declaration**

   - An XML declaration is an optional declaration placed at the beginning of the document, specifying the XML version and encoding. For example:
     ```xml
     <?xml version="1.0" encoding="UTF-8"?>
     ```

2. **Element**

   - An element is a basic building block of an XML document, consisting of a start tag, content, and an end tag. For example:
     ```xml
     <name>John</name>
     ```
   - An element can contain child elements, attributes, and text content. For example:
     ```xml
     <person>
       <name>John</name>
       <age>30</age>
     </person>
     ```

3. **Attribute**

   - An attribute provides additional information for an element and is defined in the start tag. For example:
     ```xml
     <person id="1">
       <name>John</name>
       <age>30</age>
     </person>
     ```
   - Attributes are typically used to describe the characteristics of an element, but they do not support multi-level complex structures.

4. **Text**

   - The content of an element can be text. Text content is placed between the start tag and the end tag. For example:
     ```xml
     <description>This is a sample description.</description>
     ```

5. **CDATA section**

   - A CDATA section is used to include text that should not be parsed, such as HTML code or scripts. For example:
     ```xml
     <script><![CDATA[
       function hello() {
         alert("Hello, world!");
       }
     ]]></script>
     ```

6. **Comment**

   - A comment is used to insert explanations or notes into an XML document. Comments are wrapped in `<!--` and `-->`. For example:
     ```xml
     <!-- This is a comment -->
     ```

7. **Processing instruction**

   - A processing instruction is used to include application-specific instructions in an XML document. For example:
     ```xml
     <?xml-stylesheet type="text/xsl" href="style.xsl"?>
     ```

#### 2. Rules of XML

1. **Document structure**

   - An XML document must have one and only one root element. The root element contains all other elements. For example:
     ```xml
     <root>
       <child>Content</child>
     </root>
     ```

2. **Tag matching**

   - Every element must correctly match its start tag and end tag. For example:
     ```xml
     <person>
       <name>John</name>
     </person>
     ```

3. **Attribute values must be quoted**

   - Attribute values must be wrapped in single quotes (`'`) or double quotes (`"`). For example:
     ```xml
     <person id="1" name="John"/>
     ```

4. **Valid XML names**

   - Element names and attribute names must follow XML naming rules. They cannot start with a digit, and they cannot contain spaces or special characters. Example of a valid name:
     ```xml
     <personName>John</personName>
     ```

5. **Case-sensitive**

   - XML is case-sensitive; that is, `<Person>` and `<person>` are treated as different elements.

6. **Empty elements**

   - XML allows using an empty element tag to represent an element that contains no content. For example:
     ```xml
     <item/>
     ```

#### 3. Applications of XML

1. **Data exchange**

   - Web services and APIs use XML to transfer data between different systems. Both sides only need to agree on the same set of tags.

2. **Configuration files**

   - Application configuration and system settings are written as text in XML, so changing configuration does not require recompiling the program.

3. **Document storage**

   - Rich-text documents such as e-books and Office documents use XML to store structure, with paragraphs and styles each occupying a tag.

4. **RSS and Atom**

   - XML is used in the RSS and Atom specifications, which are used to subscribe to and publish Web content such as news and blogs.

#### 4. Advantages of XML

1. **Self-describing**

   - XML documents contain tags and structure that describe the data, making the meaning and structure of the data self-explanatory and easy to understand and maintain.

2. **Extensible**

   - XML allows custom tags and structures, adapting to different requirements and application scenarios. New tags and attributes can be defined as needed.

3. **Platform-independent**

   - XML is platform-independent and can exchange data across different operating systems and programming languages.

4. **Structured**

   - XML data is structured and can represent complex data relationships and hierarchical structures.

#### 5. Disadvantages of XML

1. **Verbose**

   - XML's markup is fairly verbose, leading to larger data files and lower efficiency in transfer and storage.

2. **Parsing complexity**

   - XML parsers are relatively complex. Especially for large XML documents, they may require substantial computational and memory resources.

3. **No data types**

   - XML does not support the definition of data types. All data is treated as text, and extra processing is needed to parse and convert data types.

#### 6. Parsing and generating XML

In Go, the common ways to handle XML data are as follows:

```go
package main

import (
    "encoding/xml"
    "fmt"
)

// define the struct corresponding to the XML element
type Person struct {
    XMLName xml.Name `xml:"person"`
    Name    string   `xml:"name"`
    Age     int      `xml:"age"`
}

func main() {
    // XML data
    xmlData := `
    <person>
      <name>John</name>
      <age>30</age>
    </person>
    `
    
    // parse the XML data
    var person Person
    err := xml.Unmarshal([]byte(xmlData), &person)
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    
    fmt.Println(person)
    
    // generate the XML data
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

#### Summary

XML uses custom tags to express structured data and is transferred across platforms. The cost is verbose markup and parsing that costs memory. Choose XML when you need a human-readable, extensible text format. When you are only passing data back and forth inside a program, JSON is less trouble. In Go, parse with `xml.Unmarshal` and generate with `xml.MarshalIndent`.

## References

- [encoding standard library series (json as an example)](https://pkg.go.dev/encoding/json)
- [encoding/xml standard library](https://pkg.go.dev/encoding/xml)


## Sibling pages

- [JsonV2](/encoding/JsonV2.md)
- [Base64](/encoding/Base64.md)
- [Binary](/encoding/Binary.md)
- [Voice](/encoding/Voice.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Voice](/encoding/Voice.md)
