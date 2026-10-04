### 图像和音频编码

图像和音频编码把原始数据转成便于存储、传输的特定格式。常见的图像标准是 JPEG、PNG、GIF，音频是 MP3 和 WAV。

#### 4.1 图像编码

图像编码涉及将图像数据压缩和存储成特定格式。常见的图像编码标准包括 JPEG、PNG 和 GIF。

##### 4.1.1 JPEG

**JPEG (Joint Photographic Experts Group)** 是一种有损图像压缩标准，广泛用于数码照片和网页图像。它使用 DCT（离散余弦变换）对图像进行压缩，以减少文件大小。

**特点**：有损压缩，压缩比高但会损失部分画质；用于数字摄影和网页图像。

**Go 示例代码**（注意需要匿名导入对应的图像解码包，`image.Decode` 才能识别该格式）：
```go
package main

import (
    "fmt"
    "image"
    _ "image/jpeg"
    "os"
)

func main() {
    // 打开 JPEG 图像文件
    file, err := os.Open("example.jpg")
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    // 解码 JPEG 图像
    img, _, err := image.Decode(file)
    if err != nil {
        fmt.Println("Error decoding image:", err)
        return
    }

    // 打印图像信息
    fmt.Printf("Image: %v\n", img.Bounds())
}
```

##### 4.1.2 PNG

**PNG (Portable Network Graphics)** 是一种无损图像压缩标准，支持透明度。它适用于需要高质量图像和透明背景的场景。

**特点**：无损压缩，保留图像质量、文件较大；支持透明度，用于网页图像和图标。

**Go 示例代码**：
```go
package main

import (
    "fmt"
    "image"
    _ "image/png"
    "os"
)

func main() {
    // 打开 PNG 图像文件
    file, err := os.Open("example.png")
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    // 解码 PNG 图像
    img, _, err := image.Decode(file)
    if err != nil {
        fmt.Println("Error decoding image:", err)
        return
    }

    // 打印图像信息
    fmt.Printf("Image: %v\n", img.Bounds())
}
```

##### 4.1.3 GIF

**GIF (Graphics Interchange Format)** 是一种支持动画和透明度的图像编码标准，适用于简单的动画和图像。

**特点**：无损，支持动画和透明度，但颜色深度有限；用于简单动画和图像。

**Go 示例代码**：
```go
package main

import (
    "fmt"
    "image"
    _ "image/gif"
    "os"
)

func main() {
    // 打开 GIF 图像文件
    file, err := os.Open("example.gif")
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    // 解码 GIF 图像
    img, _, err := image.Decode(file)
    if err != nil {
        fmt.Println("Error decoding image:", err)
        return
    }

    // 打印图像信息
    fmt.Printf("Image: %v\n", img.Bounds())
}
```

#### 4.2 音频编码

音频编码用于将音频数据转换为特定格式，以便于存储和传输。常见的音频编码标准包括 MP3 和 WAV。

##### 4.2.1 MP3

**MP3 (MPEG Audio Layer III)** 是一种有损音频压缩标准，旨在减少音频文件的大小，同时尽量保留音质。它广泛用于数字音乐和流媒体服务。

**特点**：有损，压缩比高但损失部分音质；用于数字音乐和音频流。

**Go 示例代码**（Go 标准库不支持 MP3 编解码，播放 MP3 文件需要第三方库，如 `github.com/faiface/beep` 或 `github.com/hajimehoshi/oto`）：
```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 打开 MP3 文件
    file, err := os.Open("example.mp3")
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    // 解码和播放 MP3 文件需要使用合适的第三方库，
    // 例如 github.com/hajimehoshi/go-mp3 提供的 mp3.NewDecoder(file)
    fmt.Println("MP3 file opened. Playback requires a media player library.")
}
```

##### 4.2.2 WAV

**WAV (Waveform Audio File Format)** 是一种无损音频编码格式，通常用于高质量音频的存储。它使用 PCM（脉冲编码调制）来编码音频数据。

**特点**：无损，音质好但文件较大；用于音频编辑和高保真音频存储。

**Go 示例代码**：
```go
package main

import (
    "fmt"
    "os"

    "github.com/go-audio/wav"
)

func main() {
    // 打开 WAV 文件
    file, err := os.Open("example.wav")
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    // 解码 WAV 文件，IsValidFile 会读取并校验文件头
    decoder := wav.NewDecoder(file)
    if !decoder.IsValidFile() {
        fmt.Println("Error: not a valid WAV file")
        return
    }

    // 打印音频信息
    fmt.Printf("Sample Rate: %d\n", decoder.SampleRate)
    fmt.Printf("Channels: %d\n", decoder.NumChans)
    fmt.Printf("Bits Per Sample: %d\n", decoder.BitDepth)
}
```

#### 总结

- **图像编码**：JPEG、PNG 和 GIF，分别用于有损压缩、无损压缩和动画图像。
- **音频编码**：MP3 和 WAV，用于有损和无损音频压缩。

Go 标准库自带 JPEG、PNG、GIF 的解码，通过匿名导入 `image/jpeg` 这类包注册；MP3 和 WAV 的编解码要靠第三方库。