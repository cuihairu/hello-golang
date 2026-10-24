### Image and audio encoding

Image and audio encoding convert raw data into specific formats that are easier to store and transfer. Common image standards are JPEG, PNG, and GIF, and audio standards are MP3 and WAV.

#### 4.1 Image encoding

Image encoding involves compressing image data and storing it in a specific format. Common image encoding standards include JPEG, PNG, and GIF.

##### 4.1.1 JPEG

**JPEG (Joint Photographic Experts Group)** is a lossy image compression standard, widely used for digital photos and Web images. It uses DCT (Discrete Cosine Transform) to compress the image, reducing the file size.

**Features**: Lossy compression with a high compression ratio but some loss of image quality; used for digital photography and Web images.

**Go example code** (note that you need to anonymously import the corresponding image decoding package so that `image.Decode` can recognize the format):
```go
package main

import (
    "fmt"
    "image"
    _ "image/jpeg"
    "os"
)

func main() {
    // open the JPEG image file
    file, err := os.Open("example.jpg")
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    // decode the JPEG image
    img, _, err := image.Decode(file)
    if err != nil {
        fmt.Println("Error decoding image:", err)
        return
    }

    // print the image info
    fmt.Printf("Image: %v\n", img.Bounds())
}
```

##### 4.1.2 PNG

**PNG (Portable Network Graphics)** is a lossless image compression standard that supports transparency. It is suitable for scenarios that need high-quality images and transparent backgrounds.

**Features**: Lossless compression that preserves image quality but produces larger files; supports transparency, used for Web images and icons.

**Go example code**:
```go
package main

import (
    "fmt"
    "image"
    _ "image/png"
    "os"
)

func main() {
    // open the PNG image file
    file, err := os.Open("example.png")
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    // decode the PNG image
    img, _, err := image.Decode(file)
    if err != nil {
        fmt.Println("Error decoding image:", err)
        return
    }

    // print the image info
    fmt.Printf("Image: %v\n", img.Bounds())
}
```

##### 4.1.3 GIF

**GIF (Graphics Interchange Format)** is an image encoding standard that supports animation and transparency, suitable for simple animations and images.

**Features**: Lossless, supports animation and transparency, but has limited color depth; used for simple animations and images.

**Go example code**:
```go
package main

import (
    "fmt"
    "image"
    _ "image/gif"
    "os"
)

func main() {
    // open the GIF image file
    file, err := os.Open("example.gif")
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    // decode the GIF image
    img, _, err := image.Decode(file)
    if err != nil {
        fmt.Println("Error decoding image:", err)
        return
    }

    // print the image info
    fmt.Printf("Image: %v\n", img.Bounds())
}
```

#### 4.2 Audio encoding

Audio encoding is used to convert audio data into a specific format for easier storage and transfer. Common audio encoding standards include MP3 and WAV.

##### 4.2.1 MP3

**MP3 (MPEG Audio Layer III)** is a lossy audio compression standard aimed at reducing the size of audio files while preserving as much audio quality as possible. It is widely used for digital music and streaming services.

**Features**: Lossy with a high compression ratio but some loss of audio quality; used for digital music and audio streams.

**Go example code** (the Go standard library does not support MP3 encoding and decoding; playing MP3 files requires a third-party library such as `github.com/faiface/beep` or `github.com/hajimehoshi/oto`):
```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // open the MP3 file
    file, err := os.Open("example.mp3")
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    // decoding and playing an MP3 file requires an appropriate third-party library,
    // for example mp3.NewDecoder(file) provided by github.com/hajimehoshi/go-mp3
    fmt.Println("MP3 file opened. Playback requires a media player library.")
}
```

##### 4.2.2 WAV

**WAV (Waveform Audio File Format)** is a lossless audio encoding format, typically used for storing high-quality audio. It uses PCM (Pulse-Code Modulation) to encode the audio data.

**Features**: Lossless with good audio quality but larger files; used for audio editing and high-fidelity audio storage.

**Go example code**:
```go
package main

import (
    "fmt"
    "os"

    "github.com/go-audio/wav"
)

func main() {
    // open the WAV file
    file, err := os.Open("example.wav")
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    // decode the WAV file; IsValidFile reads and validates the file header
    decoder := wav.NewDecoder(file)
    if !decoder.IsValidFile() {
        fmt.Println("Error: not a valid WAV file")
        return
    }

    // print the audio info
    fmt.Printf("Sample Rate: %d\n", decoder.SampleRate)
    fmt.Printf("Channels: %d\n", decoder.NumChans)
    fmt.Printf("Bits Per Sample: %d\n", decoder.BitDepth)
}
```

#### Summary

- **Image encoding**: JPEG, PNG, and GIF, used respectively for lossy compression, lossless compression, and animated images.
- **Audio encoding**: MP3 and WAV, used for lossy and lossless audio compression.

The Go standard library comes with decoders for JPEG, PNG, and GIF, registered through anonymous imports of packages such as `image/jpeg`; MP3 and WAV encoding and decoding rely on third-party libraries.

## References

- [encoding standard library series (json as an example)](https://pkg.go.dev/encoding/json)


## Sibling pages

- [JsonV2](/encoding/JsonV2.md)
- [Base64](/encoding/Base64.md)
- [Binary](/encoding/Binary.md)
- [Text](/encoding/Text.md)
- [XML](/encoding/XML.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Text](/encoding/Text.md)
- [XML](/encoding/XML.md)
