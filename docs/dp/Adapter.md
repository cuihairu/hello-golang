### Adapter Pattern

#### Intent
The Adapter pattern is a structural design pattern that converts the interface of a class into another interface the client expects, so classes with otherwise incompatible interfaces can work together.

#### Problem
In the real world, consider an old audio playback system that can only play MP3 files, while a newer audio player can play multiple formats (such as MP4, FLAC, and so on). If you want to use the new player on the old system, you need an adapter to convert the new player's interface so that it is compatible with the old system.

#### Solution
With the Adapter pattern, you can create an adapter class that implements the interface the old system expects and calls the new player's interface internally, so the old system can use the new player.

#### Structure
1. **Target**: defines the interface the client uses.
2. **Adaptee**: defines the interface that already exists and needs to be adapted.
3. **Adapter**: implements the target interface and calls methods on the adaptee's interface to perform the conversion.
4. **Client**: interacts with the adapter through the target interface.

#### Code

```go
package main

import "fmt"

// Target interface - the interface the old system expects
type MediaPlayer interface {
    Play(fileType, fileName string)
}

// Adaptee - the new audio player, which can play multiple formats
type AdvancedMediaPlayer interface {
    PlayMP4(fileName string)
    PlayFLAC(fileName string)
}

// Concrete adaptee - MP4 player
type MP4Player struct{}

func (p *MP4Player) PlayMP4(fileName string) {
    fmt.Println("Playing MP4 file. Name:", fileName)
}

func (p *MP4Player) PlayFLAC(fileName string) {
    // MP4Player does not support playing FLAC files
}

// Concrete adaptee - FLAC player
type FLACPlayer struct{}

func (p *FLACPlayer) PlayMP4(fileName string) {
    // FLACPlayer does not support playing MP4 files
}

func (p *FLACPlayer) PlayFLAC(fileName string) {
    fmt.Println("Playing FLAC file. Name:", fileName)
}

// Adapter - adapts the new audio player to the old system
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

// Concrete target - the old audio player, which can only play MP3 files
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

#### Use cases
- The system needs to use an existing class, but its interface does not meet the system's needs.
- You want to create a reusable class that works together with other classes that have incompatible interfaces.
- You need to convert multiple existing class interfaces into a single unified interface.

#### Implementation
1. Define the target interface, declaring the interface the client expects.
2. Create the adaptee class, implementing the existing interface.
3. Create the adapter class, implementing the target interface and calling the adaptee's interface methods internally.
4. In the client code, interact with the adapter through the target interface.

#### Pros and cons
**Pros**:
- The client code is decoupled from the implementation details of incompatible interfaces, and existing classes can be reused.
- Follows the Open/Closed Principle: adding a new adapter does not affect existing code.

**Cons**:
- Every incompatible interface requires an extra adapter class, so once there are many interfaces the system becomes complex and hard to maintain.

#### Relationship to other patterns
- **Decorator Pattern**: the Decorator pattern enhances an object's functionality, while the Adapter pattern changes an object's interface.
- **Bridge Pattern**: the Bridge pattern separates the abstraction from the implementation so that the two can vary independently. The Adapter pattern converts the interface of an existing class into the interface the client expects.
- **Facade Pattern**: the Facade pattern provides a unified interface for a set of interfaces in a subsystem, while the Adapter pattern makes incompatible interfaces work together.

## References

- [GoF Design Patterns overview (Wikipedia)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring.Guru design patterns catalog](https://refactoring.guru/design-patterns)
- [Effective Go (official)](https://go.dev/doc/effective_go)

## Sibling pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Behavioral](/dp/Behavioral.md)
- [Bridge](/dp/Bridge.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [AbstractFactory](/dp/AbstractFactory.md)
- [Behavioral](/dp/Behavioral.md)
- [Bridge](/dp/Bridge.md)
- [Builder](/dp/Builder.md)
- [ChainofResponsibility](/dp/ChainofResponsibility.md)
- [Command](/dp/Command.md)
- [Composite](/dp/Composite.md)
- [Creational](/dp/Creational.md)
- [Decorator](/dp/Decorator.md)
- [DesignPatterns](/dp/DesignPatterns.md)
- [Facade](/dp/Facade.md)
- [FactoryMethod](/dp/FactoryMethod.md)
- [Flyweight](/dp/Flyweight.md)
- [Iterator](/dp/Iterator.md)
- [Mediator](/dp/Mediator.md)
- [Memento](/dp/Memento.md)
- [ObjectPool](/dp/ObjectPool.md)
- [Observer](/dp/Observer.md)
- [Proactor](/dp/Proactor.md)
- [Prototype](/dp/Prototype.md)
- [Proxy](/dp/Proxy.md)
- [Reactor](/dp/Reactor.md)
- [Singleton](/dp/Singleton.md)
- [State](/dp/State.md)
- [Strategy](/dp/Strategy.md)
- [Structural](/dp/Structural.md)
- [TemplateMethod](/dp/TemplateMethod.md)
- [Visitor](/dp/Visitor.md)
