###  Files and IO

#### 1.1 What are files and IO

Files are the units in which data is stored, and input/output (IO) is the mechanism by which a program exchanges data with the outside world. A file can be text, binary data, or some other format; IO operations cover things like reading data from user input, printing information to the screen, and receiving data from a network.

The basic concepts of files and IO include:

- **File**: On a computer, a file is a container used to store data. A file can hold many kinds of data, including text, images, audio, and video. File operations include creating, opening, reading from, writing to, closing, and deleting a file.
  
- **Input/output (IO)**: IO is how a program interacts with the environment outside the computer. Input fetches data from the outside environment; output sends data to it. IO operations include reading input from the keyboard, writing data to the screen, reading data from a file, and writing data to a file.

#### 1.2 Why files and IO matter

If files and IO are handled poorly, both a program's performance and reliability suffer:

- **Data persistence**: Files let a program store data persistently on disk, where it stays available after a program or system restart. Saving user data, writing logs, and storing configuration files all rely on it.

- **Data exchange**: IO operations let different programs or systems exchange data. For example, a program can read configuration settings from a file, write its results to a file, or communicate with a remote server over network IO.

- **Performance optimization**: Caching and asynchronous IO reduce the wait time for file reads and writes.

- **User interaction**: Reading user input, displaying results, and saving settings all go through IO.

## References

- [io standard library](https://pkg.go.dev/io)
- [os standard library](https://pkg.go.dev/os)


## Sibling pages

- [Advanced](/io/Advanced.md)
- [CommonFormats](/io/CommonFormats.md)
- [EfficientIO](/io/EfficientIO.md)
- [FileOperation](/io/FileOperation.md)
- [InputOutput](/io/InputOutput.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [FileOperation](/io/FileOperation.md)
- [InputOutput](/io/InputOutput.md)
