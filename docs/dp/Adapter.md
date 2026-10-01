### 适配器模式 (Adapter Pattern)

#### 意图
适配器模式是一种结构型设计模式，通过将一个类的接口转换成客户希望的另一个接口，使得原本接口不兼容的类可以一起工作。适配器模式主要用于解决两个现有接口不兼容的问题。

#### 问题
在现实世界中，考虑一个旧的音频播放系统只能播放MP3格式的音频文件，而新的音频播放器可以播放多种格式（例如MP4、FLAC等）。如果想在旧的系统上使用新的播放器，就需要一个适配器来转换新的播放器接口，使其与旧系统兼容。

#### 解决方案
使用适配器模式，我们可以创建一个适配器类，实现旧系统所期望的接口，并在适配器内部调用新的播放器接口，从而使得旧系统可以使用新的播放器。

#### 模式结构
1. **目标接口（Target）**：定义客户端使用的接口。
2. **适配者（Adaptee）**：定义已经存在且需要适配的接口。
3. **适配器（Adapter）**：实现目标接口，并调用适配者接口的方法，以实现接口的转换。
4. **客户端（Client）**：使用目标接口与适配器交互。

#### 代码
以下是使用Go语言实现的适配器模式示例：

```go
package main

import "fmt"

// 目标接口 - 旧系统期望的接口
type MediaPlayer interface {
    Play(fileType, fileName string)
}

// 适配者 - 新的音频播放器，可以播放多种格式
type AdvancedMediaPlayer interface {
    PlayMP4(fileName string)
    PlayFLAC(fileName string)
}

// 具体适配者 - MP4播放器
type MP4Player struct{}

func (p *MP4Player) PlayMP4(fileName string) {
    fmt.Println("Playing MP4 file. Name:", fileName)
}

func (p *MP4Player) PlayFLAC(fileName string) {
    // MP4Player 不支持播放 FLAC 文件
}

// 具体适配者 - FLAC播放器
type FLACPlayer struct{}

func (p *FLACPlayer) PlayMP4(fileName string) {
    // FLACPlayer 不支持播放 MP4 文件
}

func (p *FLACPlayer) PlayFLAC(fileName string) {
    fmt.Println("Playing FLAC file. Name:", fileName)
}

// 适配器 - 适配新的音频播放器到旧系统
type MediaAdapter struct {
    advancedPlayer AdvancedMediaPlayer
}

func NewMediaAdapter(fileType string) *MediaAdapter {
    if fileType == "mp4" {
        return &MediaAdapter{&MP4Player{}}
    } else if fileType == "flac" {
        return &MediaAdapter{&FLACPlayer{}}
    }
    return nil
}

func (a *MediaAdapter) Play(fileType, fileName string) {
    if fileType == "mp4" {
        a.advancedPlayer.PlayMP4(fileName)
    } else if fileType == "flac" {
        a.advancedPlayer.PlayFLAC(fileName)
    }
}

// 具体目标 - 旧的音频播放器，只能播放 MP3 文件
type AudioPlayer struct {
    adapter *MediaAdapter
}

func (p *AudioPlayer) Play(fileType, fileName string) {
    if fileType == "mp3" {
        fmt.Println("Playing MP3 file. Name:", fileName)
    } else if fileType == "mp4" || fileType == "flac" {
        p.adapter = NewMediaAdapter(fileType)
        p.adapter.Play(fileType, fileName)
    } else {
        fmt.Println("Invalid media. ", fileType, " format not supported")
    }
}

func main() {
    audioPlayer := &AudioPlayer{}

    audioPlayer.Play("mp3", "song.mp3")
    audioPlayer.Play("mp4", "movie.mp4")
    audioPlayer.Play("flac", "audio.flac")
    audioPlayer.Play("avi", "video.avi")
}
```

#### 适用场景
- 系统需要使用现有的类，但其接口不符合系统的需求。
- 创建一个可复用的类，用于与不兼容接口的其他类一起工作。
- 需要转换多个现有类接口成为一个统一接口的场景。

#### 实现方式
1. 定义目标接口，声明客户端所期待的接口。
2. 创建适配者类，实现现有的接口。
3. 创建适配器类，实现目标接口，并在适配器类内部调用适配者的接口方法。
4. 在客户端代码中，通过目标接口与适配器交互。

#### 优缺点
**优点**：
- 分离了客户端代码与不兼容接口的实现细节，增加了代码的可复用性和灵活性。
- 符合开闭原则，增加新的适配器不会影响现有代码。
- 可以提高现有类的复用性。

**缺点**：
- 增加了系统的复杂性，需要定义额外的适配器类。
- 适配器模式的使用可能会导致过多的适配器类，从而使得系统更加复杂和难以维护。

#### 其他模式的关系
- **装饰器模式（Decorator Pattern）**：装饰器模式用于增强对象的功能，而适配器模式用于改变对象的接口。
- **桥接模式（Bridge Pattern）**：桥接模式分离抽象部分和实现部分，使它们可以独立变化。适配器模式用于将现有类的接口转换为客户希望的接口。
- **外观模式（Facade Pattern）**：外观模式为子系统中的一组接口提供一个统一的接口，适配器模式则是使不兼容的接口能够协同工作。