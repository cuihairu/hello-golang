### JSON (JavaScript Object Notation)

JSON (JavaScript Object Notation) is a lightweight data interchange format with simple syntax that is easy for humans to read and write. It is based on the JavaScript object notation but is language-independent, and is widely used for data transfer and storage in Web applications.

#### 1. The basic structure of JSON

The basic structure of JSON includes objects, arrays, strings, numbers, booleans, and `null`. The basic data types and structures of JSON are as follows:

1. **Object**

   - An object consists of key-value pairs. The key (key name) must be a string, and the value can be any JSON data type. An object is wrapped in curly braces (`{}`), with key-value pairs separated by commas (`,`). For example:
     ```json
     {
       "name": "John",
       "age": 30,
       "city": "New York"
     }
     ```

2. **Array**

   - An array is an ordered collection of values, and the values can be any JSON data type. An array is wrapped in square brackets (`[]`), with values separated by commas (`,`). For example:
     ```json
     [ "apple", "banana", "cherry" ]
     ```

3. **String**

   - A string is a sequence of characters wrapped in double quotes (`"`). A string can contain any Unicode character and may use escape characters, such as `\"` and `\\`. For example:
     ```json
     "Hello, World!"
     ```

4. **Number**

   - A number can be an integer or a floating-point number, and leading zeros are not supported. JSON numbers have a format similar to JavaScript numbers. For example:
     ```json
     42
     3.14
     ```

5. **Boolean**

   - A boolean can only be `true` or `false`. For example:
     ```json
     true
     false
     ```

6. **null**

   - `null` represents an empty value or a missing value. For example:
     ```json
     null
     ```

#### 2. Syntax rules of JSON

1. **Key names must be strings**: Key names must be wrapped in double quotes. For example:
   ```json
   { "key": "value" }
   ```

2. **Data structures**: JSON supports nested objects and arrays. For example:
   ```json
   {
     "person": {
       "name": "John",
       "age": 30,
       "children": [
         {
           "name": "Alice",
           "age": 5
         },
         {
           "name": "Bob",
           "age": 7
         }
       ]
     }
   }
   ```

3. **No comments**: JSON does not support comments. All comments must be removed from the data structure, otherwise it will cause a parsing error.

4. **Escape characters in strings**: Use escape characters (`\`) in JSON strings to represent special characters. For example:
   ```json
   "This is a \"quoted\" string."
   ```

#### 3. Applications of JSON

1. **Web applications**

   - JSON is the most commonly used data interchange format in Web applications. The browser and the server transfer data via JSON, and the JavaScript language natively supports JSON parsing and generation. For example:
     ```javascript
     // parse a JSON string
     let obj = JSON.parse('{"name":"John","age":30,"city":"New York"}');
     
     // generate a JSON string
     let jsonString = JSON.stringify({ name: "John", age: 30, city: "New York" });
     ```

2. **APIs**

   - Many Web APIs use JSON as the data interchange format. JSON is simple and lightweight, making it suitable for fast data transfer over the network. For example, both the GitHub API and the Twitter API use JSON.

3. **Configuration files**

   - JSON is often used in configuration files because its structure is clear and easy to edit. Many modern applications and frameworks use JSON-formatted configuration files, such as `package.json` (Node.js) and `composer.json` (PHP).

4. **Data storage**

   - JSON can be used for simple data storage. Although a JSON file is not a dedicated database format, it can be used to store configuration, logs, or other small data collections.

#### 4. Advantages of JSON

JSON has simple syntax and a compact format, making it suitable for network transfer and storage. Almost all modern programming languages and frameworks have built-in support for parsing and generating JSON.

#### 5. Comparison of JSON with other formats

- **XML**: XML is another commonly used data interchange format that supports complex data structures and custom tags. Compared with JSON, XML is usually more verbose but supports more data-description features.

- **YAML**: YAML is a highly readable format for configuration files that supports complex structures and custom data types. Compared with JSON, YAML is more flexible, but its looser syntax can cause parsing errors.

- **TOML**: TOML is a format for configuration files designed to be easy to read and write. Compared with JSON, TOML pays more attention to the structure and readability of configuration files, but it is not as widely used as JSON.

#### 6. Parsing and generating JSON

In Go, the common ways to handle JSON data are as follows:

```go
package main

import (
    "encoding/json"
    "fmt"
)

type Person struct {
    Name    string   `json:"name"`
    Age     int      `json:"age"`
    City    string   `json:"city"`
    Children []Child `json:"children"`
}

type Child struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}

func main() {
    // JSON data
    jsonData := `{
        "name": "John",
        "age": 30,
        "city": "New York",
        "children": [
            {"name": "Alice", "age": 5},
            {"name": "Bob", "age": 7}
        ]
    }`

    // parse the JSON data
    var person Person
    err := json.Unmarshal([]byte(jsonData), &person)
    if err != nil {
        fmt.Println(err)
        return
    }

    fmt.Println(person)

    // generate the JSON data
    newPerson := Person{
        Name:    "Jane",
        Age:     25,
        City:    "San Francisco",
        Children: []Child{
            {Name: "Charlie", Age: 3},
        },
    }

    newJsonData, err := json.Marshal(newPerson)
    if err != nil {
        fmt.Println(err)
        return
    }

    fmt.Println(string(newJsonData))
}
```

#### Summary

JSON has few rules: key names must be double-quoted strings, comments are not supported, and special characters rely on escaping. In Go, with `Marshal` and `Unmarshal` from `encoding/json`, almost all JSON handling is covered.

## References

- [encoding standard library series (json as an example)](https://pkg.go.dev/encoding/json)
- [Official blog · JSON and Go](https://go.dev/blog/json)


## Sibling pages

- [JsonV2](/encoding/JsonV2.md)
- [Base64](/encoding/Base64.md)
- [Binary](/encoding/Binary.md)
- [Ini](/encoding/Ini.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Ini](/encoding/Ini.md)
