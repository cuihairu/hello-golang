### Data Encoding

#### 1.1 Overview of Data Encoding

Data encoding converts data into a specific format so it can be stored, transmitted, and processed. Which encoding you pick directly affects processing efficiency and storage cost.

Types of data encoding include text encoding, binary encoding, and image/audio encoding:

- **Text encoding**: converts characters into byte sequences. Common text encodings include ASCII, UTF-8, UTF-16, and so on.
- **Binary encoding**: converts binary data into another representation, for example Base64 and Hex.
- **Image and audio encoding**: compresses and encodes image and audio data for storage and transmission. Examples include JPEG, PNG, MP3, WAV, and so on.

#### 1.2 Data Encoding in Go

The Go standard library covers most encoding and decoding needs. The commonly used packages are:

- **`encoding/base64`**: encodes binary data as Base64 so it can be transmitted and stored in text environments.
- **`encoding/hex`**: encodes binary data as a hexadecimal string, commonly used for debugging and data display.
- **`unicode/utf8`**: handles UTF-8 encoded text data, including encoding and decoding UTF-8 characters.
- **`encoding/json`** and **`encoding/xml`**: encode data as JSON or XML for storing and transmitting structured data.

Below I go through text encoding and binary encoding in Go, and where each one fits.

## References

- [encoding standard library family (json as the example)](https://pkg.go.dev/encoding/json)


## Sibling pages

- [JsonV2](/encoding/JsonV2.md)
- [Base64](/encoding/Base64.md)
- [Binary](/encoding/Binary.md)
- [CSV](/encoding/CSV.md)
- [Formats](/encoding/Formats.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Formats](/encoding/Formats.md)
