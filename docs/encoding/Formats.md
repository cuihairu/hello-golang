### Data Encoding Standards

Data encoding standards define how data moves from one format to another. Without shared standards, systems, platforms, and applications cannot exchange data with each other. Below I list common formats in three groups: text, binary, and image/audio.

#### 1. Text Encoding Standards

1. **ASCII (American Standard Code for Information Interchange)**
   - **Definition**: ASCII is a character encoding standard that uses 7 bits per character and supports 128 characters, including English letters, digits, and some control characters (the extended character sets that came later use 8 bits for 256 characters, but they are not standard ASCII).
   - **Usage**: mainly for English text and basic symbols. 7 bits cannot hold characters from other languages, so Unicode-based encodings eventually took over.

2. **UTF-8 (8-bit Unicode Transformation Format)**
   - **Definition**: UTF-8 is a variable-length Unicode encoding that uses 1 to 4 bytes per character. It is ASCII-compatible and supports characters from nearly every language in the world.
   - **Usage**: widely used on the web, in files, and in network communication; especially important in internationalized applications.
   - **Trait**: ASCII characters still take 1 byte.

3. **UTF-16 (16-bit Unicode Transformation Format)**
   - **Definition**: UTF-16 uses 16 bits (two bytes) or 32 bits (four bytes) per character and can represent all Unicode characters. UTF-16 mainly relies on surrogate pairs to handle characters outside the basic multilingual plane.
   - **Usage**: mainly in the Windows operating system, Java, and other Unicode-aware platforms.
   - **Trait**: handles multilingual text well, but is less storage-efficient than UTF-8.

4. **UTF-32 (32-bit Unicode Transformation Format)**
   - **Definition**: UTF-32 uses a fixed 32 bits (four bytes) per character. It provides a fixed-length encoding but takes up a lot of space.
   - **Usage**: mainly in applications that need fast random access to characters.
   - **Trait**: fixed length simplifies character handling, but it does not save storage space.

#### 2. Binary Encoding Standards

1. **Base64**
   - **Definition**: Base64 encodes binary data as an ASCII string, using 64 distinct characters to represent each 6-bit group of binary data. It encodes every three bytes of binary data as four ASCII characters.
   - **Usage**: common in email and URLs so binary data can travel through text environments.
   - **Trait**: the encoded data is about 33% larger than the original.

2. **Hex (hexadecimal)**
   - **Definition**: Hex encoding represents binary data as a hexadecimal string, two hex characters per byte. It is a simple way to convert between binary and text data.
   - **Usage**: common in debugging, data display, and storage.
   - **Trait**: two characters per byte, so the data is 100% larger than the original.

3. **GOB**
   - **Definition**: GOB is a Go-specific binary encoding that serializes Go data structures into a binary format and decodes it back into Go data structures. It is mainly used for data persistence and network transfer inside Go applications.
   - **Usage**: mainly for efficient serialization and deserialization in Go programs.
   - **Trait**: designed for the Go language, and supports serializing Go data structures.

#### 3. Image and Audio Encoding Standards

1. **JPEG (Joint Photographic Experts Group)**
   - **Definition**: JPEG is a common image compression standard that uses lossy compression algorithms to reduce image file size. It is mainly used in digital photography and image storage.
   - **Usage**: widely used in digital cameras, web images, and digital media.
   - **Trait**: high compression ratio, but image quality suffers.

2. **PNG (Portable Network Graphics)**
   - **Definition**: PNG is a lossless image compression standard that supports transparency and higher image quality. It is mainly used for transferring and storing images over the network.
   - **Usage**: fits scenarios that need transparent backgrounds and high-quality images.
   - **Trait**: lossless compression; the file is larger, but image quality is preserved.

3. **MP3 (MPEG Audio Layer III)**
   - **Definition**: MP3 is a lossy audio compression standard that reduces audio file size while keeping as much sound quality as possible.
   - **Usage**: widely used in digital music and audio streaming.
   - **Trait**: high compression ratio, but some sound quality is lost.

4. **WAV (Waveform Audio File Format)**
   - **Definition**: WAV is a lossless audio encoding format that uses PCM (pulse-code modulation) to encode audio data. It delivers high-quality audio data, but the files are large.
   - **Usage**: for high-fidelity audio storage and editing.
   - **Trait**: lossless encoding, large file size.

#### Summary

Pick an encoding by what it is for: UTF-8 for cross-language text, Base64 or Hex when binary data has to go through a text channel, GOB for structs passed between Go programs; JPEG when images need to be small, PNG for lossless and transparency. The Go standard library supports all of these directly.

## References

- [encoding standard library family (json as the example)](https://pkg.go.dev/encoding/json)


## Sibling pages

- [JsonV2](/encoding/JsonV2.md)
- [Base64](/encoding/Base64.md)
- [Binary](/encoding/Binary.md)
- [Encoding](/encoding/Encoding.md)
- [Gob](/encoding/Gob.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Encoding](/encoding/Encoding.md)
- [Gob](/encoding/Gob.md)
